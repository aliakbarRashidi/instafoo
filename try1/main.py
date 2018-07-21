import logging
import json
import os.path
import argparse
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, exc
#import graph as graph_worker

import instapi as ia
import basic_crawler as bc
import insta_data_model as idm
import exclude_from_crawl as ec

def sanitize_inputs(*args):
    for arg in args:
        if arg == '':
            yield None
        else:
            yield arg

class MySQL_Worker(object):
    def __init__(self):
        self.base_insert_query = """insert into %s.users\
            (user_id,user_name,full_name,follower_count,following_count,bio,city_id,email,phone,latitude,longitude,crawl_date)""" % global_settings.get('db_name')
        self.base_update_query = """update %s.users set""" % global_settings.get('db_name')
        
        logger.debug('starting db connection')
        
        self.dbengine=create_engine("mysql://%s:%s@%s/%s?charset=utf8mb4" 
                % (global_settings.get('db_user'),
                global_settings.get('db_pass'),
                global_settings.get('db_host'),
                global_settings.get('db_name'))
            , echo = False
            , connect_args={"init_command":"SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'"}
        )
        self._mysql_initizlized = True
    
    def write_record(self, user_profile, mode):
        '''TODO add try/except duplicate since it's likely that ppl will be following/follow eachother'''
        self.user_profile = user_profile
        if mode == 'seed':
            crawl_date = None
        if mode == 'crawl':
            crawl_date = str(dt.date.today())

        try:
            self.dbengine.execute(self.base_insert_query + """values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                ( *sanitize_inputs(
                self.user_profile.get('user_id')
                , self.user_profile.get('user_name')
                , self.user_profile.get('full_name')
                , self.user_profile.get('follower_count')
                , self.user_profile.get('following_count')
                , self.user_profile.get('bio')
                , self.user_profile.get('city_id')
                , self.user_profile.get('email')
                , self.user_profile.get('phone')
                , self.user_profile.get('latitude')
                , self.user_profile.get('longitude')
                , crawl_date
                ))
            )
        except exc.IntegrityError as e:
            print (e)
            import ipdb;ipdb.set_trace()

    def update_record(self, user_profile):
        '''TODO add try/except duplicate since it's likely that ppl will be following/follow eachother'''
        logger.debug('updating record: %s' % user_profile)
        self.user_profile = user_profile
        try:
            self.dbengine.execute(self.base_update_query + """\
                follower_count = %s , following_count = %s\
                , bio = %s , city_id = %s\
                , email = %s , phone = %s\
                , latitude = %s , longitude = %s\
                , crawl_date = %s \
                where user_id = %s""",
                ( *sanitize_inputs(
                  self.user_profile.get('follower_count')
                , self.user_profile.get('following_count')
                , self.user_profile.get('bio')
                , self.user_profile.get('city_id')
                , self.user_profile.get('email')
                , self.user_profile.get('phone')
                , self.user_profile.get('latitude')
                , self.user_profile.get('longitude')
                , str(dt.date.today())
                , self.user_profile.get('user_id')
                ))
            )
        except exc.IntegrityError as e:
            print (e)
            pass

def crawl_and_add(user_name, user_id, full_name, method, debug):

    def _fetch_existing_users():
        existing_user_query = "select user_id from %s.users" % global_settings.get('db_name')
        exclude_user_query = "select user_id from %s.exclude_users" % global_settings.get('db_name')
        existing_users = pd.read_sql(existing_user_query, mysql_worker.dbengine)['user_id']
        exclude_users = pd.read_sql(exclude_user_query, mysql_worker.dbengine)['user_id']
        return existing_users.append(exclude_users)
    
    def _add_follower_folling(list_of_ppl, existing_users, added_users):
        for f in list_of_ppl:
            fp = idm.parse_insta_user_obj(f)
            fp_uid = fp.get('user_id')
            if fp_uid in added_users or fp_uid in existing_users.values:
                continue
            mysql_worker.write_record(fp, 'seed')
            #user1_in_graph = graph_worker.write_record(user_profile)
            added_users.append(fp_uid)
            '''TODO: Need to think about the logic for adding nodes/edges if already in the mysql db. 
            Though we have the record, we don't have the graph relationship
            If the UID is in MySQL, don't add to MySQL, but continue to graph
            '''

    existing_users = _fetch_existing_users()
    logger.debug('got existing users')
    added_users = []
    user_profile, following, followers=insta_crawler.bc_main(user_id, debug=debug)
    user_profile.update({'user_id': user_id, 'user_name': user_name, 'full_name':full_name})

    if method == 'seed':
        if user_profile['user_id'] in existing_users.values:
            logger.error('crawl_and_add\Seed: user already in DB\n\n%s' % user_profile)
            return 
        mysql_worker.write_record(user_profile, 'seed')
    if method == 'crawl':
        mysql_worker.update_record(user_profile)
    #graph_worker.write_record(user_profile)
    added_users.append(user_profile.get('user_id'))
    
    _add_follower_folling(following, existing_users, added_users)
    #_add_follower_folling(followers, existing_users, added_users)


def seed(target):
    if target is None:
        raise Exception('No seed user specified')
    origin = insta_crawler.extract_user_info_from_username(target)
    #user_name = origin.get('user_name')
    #user_id = origin.get('user_id')
    #full_name = origin.get('full_name') 
    #crawl_and_add(user_name,user_id,full_name, method='seed', debug=args.debug)
    mysql_worker.write_record(origin, 'seed')
        

def crawl(max_crawl, crawl_recursively, debug):
    def _fetch_crawl_queue():
        crawl_queue_query = "select * from %s.users where crawl_date is null order by mod_ts" % global_settings.get('db_name')
        return pd.read_sql(crawl_queue_query, mysql_worker.dbengine)
 
    def _update_excluded_users():
        excluded_user_names = set(ec.user_names)
        exclude_user_query = "select user_name from %s.exclude_users" % global_settings.get('db_name')
        existing_user_db = pd.read_sql(exclude_user_query, mysql_worker.dbengine)['user_name'].values
        base_query = """insert into %s.exclude_users (user_id,user_name)""" % global_settings.get('db_name')
        for user in excluded_user_names:
            if user in existing_user_db:
                continue
            user_id = insta_crawler.extract_user_info_from_username(user)['user_id']
            try:
                mysql_worker.dbengine.execute(base_query + """values (%s, %s)""" , (user_id, user))
            except exc.IntegrityError as e:
                print (e)
                pass        
    
    crawl_queue = _fetch_crawl_queue()
    _update_excluded_users()

    if len(crawl_queue) == 0:
        logger.warn('crawl_queue is empty')
        if crawl_recursively:
            crawl_db(max_crawl, crawl_recursively, debug=debug) # go wide before deep
        return

    for _ndx, row in crawl_queue.iloc[:max_crawl].iterrows():
        user_id = row['user_id']
        user_name = row['user_name']
        full_name = row['full_name']
        
        logger.debug('crawl and add %s %s' % (user_id, user_name))
        crawl_and_add(user_name,user_id,full_name, method='crawl', debug=debug)


if __name__ == '__main__':
    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -target "names.txt"
    parser = argparse.ArgumentParser(description='Crawling')
    parser.add_argument('-debug', '--debug', action='store_true')
    parser.add_argument('-s', '--settings',
                        dest='settings_file_path', type=str, required=True)
    parser.add_argument('-m', '--mode', dest='mode', type=str, required=True)
    parser.add_argument('-t', '--target', dest='target', type=str)

    args = parser.parse_args()
    settings_file = args.settings_file_path

    logging.basicConfig()
    logger = logging.getLogger('instafoo')
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    if not os.path.isfile(settings_file):
        logger.error('Unable to find file: {0!s}'.format(settings_file))
    else:
        with open(settings_file) as file_data:
            global_settings = json.load(file_data)
    api = ia.main(global_settings.get('debug'),
        global_settings.get('insta_settings_file_path'),
        global_settings.get('insta_user'),
        global_settings.get('insta_pass')
        )
    
    insta_crawler = bc.InstaCrawler(api)
    
    mysql_worker = MySQL_Worker()

    if args.mode == 'seed':
        logger.debug('starting seed with %s' % args.target)
        seed(args.target)
    elif args.mode == 'crawl':
        logger.debug('starting crawl')
        crawl(max_crawl=999, crawl_recursively=True, debug=args.debug)
    else:
        logger.error('bad method')
        raise Exception('Bad method')
