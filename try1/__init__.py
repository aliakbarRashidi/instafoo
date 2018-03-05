import logging
import json
import os.path
import argparse
import pandas as pd
from sqlalchemy import create_engine
import instapi as ia
import basic_crawler as bc



if __name__ == '__main__':
    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -target "names.txt"
    parser = argparse.ArgumentParser(description='Crawling')
    parser.add_argument('-debug', '--debug', action='store_true')
    parser.add_argument('-s', '--settings',
                        dest='settings_file_path', type=str, required=True)
    parser.add_argument('-m', '--mode', dest='mode', type=str, required=True)

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
    dbengine=create_engine("mysql://%s:%s$@%s/%s"
        % (global_settings.get('db_user'), 
        global_settings.get('db_pass'),
        global_settings.get('db_host'),
        global_settings.get('db_name')))

    if args.mode == 'seed':
        target = 'roablep'
        seed(target)
    elif args.mode == 'crawl':
        crawl_db(max_crawl=1)
    else:
        raise Exception('Bad method')

    def seed(target):
        origin = api.username_info(target)
        user_id = origin['user']['pk']
        user_profile, followers, following=bc.main(api, user_id, config=None)
        import ipdb; ipdb.set_trace()
        pd.DataFrame(user_profile).to_sql('users', dbengine, if_exists = 'append', index = False)

    def crawl_db(max_crawl):
        pass
