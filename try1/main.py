import logging
import json
import os.path
import argparse
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
import instapi as ia
import basic_crawler as bc

def sanitize_inputs(*args):
    newargs = []
    for arg in args:
        if arg == '':
            yield None
        else:
            yield arg

def seed(target):
        origin = api.username_info(target)
        user_id = origin['user']['pk']
        user_profile, followers, following=bc.bc_main(api, user_id, debug=args.debug)
        
        base_query = """insert into %s.users\
            (user_id,user_name,follower_count,following_count,bio,city_id,email,phone,latitude,longitude,crawl_date)""" % global_settings.get('db_name')

        dbengine.execute(base_query + """values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            ( *sanitize_inputs(user_id
            , target
            , user_profile.get('follower_count')
            , user_profile.get('following_count')
            , user_profile.get('bio')
            , user_profile.get('city_id')
            , user_profile.get('email')
            , user_profile.get('phone')
            , user_profile.get('latitude')
            , user_profile.get('longitude')
            , str(dt.date.today())
            ))
        )

def crawl_db(max_crawl):
        pass


if __name__ == '__main__':
    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -target "names.txt"
    parser = argparse.ArgumentParser(description='Crawling')
    parser.add_argument('-debug', '--debug', action='store_true')
    parser.add_argument('-s', '--settings',
                        dest='settings_file_path', type=str, required=True)
    parser.add_argument('-m', '--mode', dest='mode', type=str, required=True)
    parser.add_argument('-t', '--target', dest='target', type=str, default='roablep')

    args = parser.parse_args()
    settings_file = args.settings_file_path

    logging.basicConfig()
    logger = logging.getLogger('instafoo')
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    if not os.path.isfile(settings_file):
        print('Unable to find file: {0!s}'.format(settings_file))
    else:
        with open(settings_file) as file_data:
            global_settings = json.load(file_data)
    
    logger.debug('starting insta api connection')
    api = ia.main(global_settings.get('debug'),
        global_settings.get('insta_settings_file_path'),
        global_settings.get('insta_user'),
        global_settings.get('insta_pass')
        )
    
    logger.debug('starting db connection')
    dbengine=create_engine("mysql://%s:%s@%s/%s"
        % (global_settings.get('db_user'), 
        global_settings.get('db_pass'),
        global_settings.get('db_host'),
        global_settings.get('db_name')))

    if args.mode == 'seed':
        seed(args.target)
    elif args.mode == 'crawl':
        crawl_db(max_crawl=1)
    else:
        raise Exception('Bad method')
