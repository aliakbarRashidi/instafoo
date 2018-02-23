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
    following = []

    def result_loop(method, user_id, user_list):
        print (method)
        if method == 'followers':
            action = api.user_followers
        if method == 'following':
            action = api.user_following
            
        results = action(user_id)

        user_list.extend(results.get('users', []))
        print(len(user_list))
        next_max_id = results.get('next_max_id', [])
        print(next_max_id)

        while next_max_id:
            # https://github.com/LevPasha/Instagram-API-python/issues/214
            # https://github.com/instagrambot/instapro/blob/master/instabot/getter/getter.py
            print ('in while')
            try:
                ipdb.set_trace()
                print(api.user_info(next_max_id))
            except Exception as e:
                print(e)
                pass
            results = action(user_id, max_id=next_max_id)
            user_list.extend(results.get('users', []))
            print(len(user_list))
            if len(user_list) >= 500:       # get only first 600 or so
                break
            next_max_id = results.get('next_max_id', [])
        print(len(user_list))
        return user_list.sort(key=lambda x: x['pk'])
    
    '''
    results_followers = api.user_followers(user_id)

    followers.extend(results_followers.get('users', []))

    next_max_id = results_followers.get('next_max_id')
    while next_max_id:
        try:
            print(api.user_info(next_max_id))
        except Exception as e:
            print(e)
            pass
        results = api.user_followers(user_id, max_id=next_max_id)
        followers.extend(results.get('users', []))
        if len(followers) >= 500:       # get only first 600 or so
            break
        next_max_id = results.get('next_max_id')

    followers.sort(key=lambda x: x['pk'])
    '''
    ipdb.set_trace()
    followers = result_loop('followers', user_id, followers)
    print(len(followers))
    following = result_loop('following', user_id, following)
    print(len(followers))
    # print list of user IDs
    print('FOLLOWERS')
    print('\n')
    print(json.dumps([u['username'] for u in followers], indent=2))

    print('FOLLOWING')
    print('\n')
    print(json.dumps([u['username'] for u in following], indent=2))
    # for u in followers