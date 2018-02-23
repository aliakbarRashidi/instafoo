import json
import os.path
import logging
import argparse
import ipdb

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='Pagination demo')
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: %s' % client_version)
    api = Client(args.username, args.password)

    # user_id = '2958144170'
    origin = api.username_info('roablep')
    user_id = origin['user']['pk']
    followers = []
    print(api.user_info(user_id))
    
    def run_result_loop(method, user_id):
        user_list = []
        if method == 'followers':
            action = api.user_followers
        if method == 'following':
            action = api.user_following
        
        results = action(user_id)

        user_list.extend(results.get('users', []))

        next_max_id = results.get('next_max_id')
        while next_max_id:
            try:
                print(api.user_info(next_max_id))
            except Exception as e:
                print(e)
                pass
            results = action(user_id, max_id=next_max_id)
            user_list.extend(results.get('users', []))
            if len(user_list) >= 500:       # get only first 600 or so
                break
            next_max_id = results.get('next_max_id')

        user_list.sort(key=lambda x: x['pk'])
        return user_list
    
    followers = run_result_loop('followers',user_id)
    following = run_result_loop('following',user_id)
    
    # print list of user IDs
    print(json.dumps([u['username'] for u in followers], indent=2))
    print(json.dumps([u['username'] for u in following], indent=2))
    # for u in followers