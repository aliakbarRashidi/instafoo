import os 

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)

import logging

def extract_user_info(user_id, api):
    user_info = api.user_info(user_id)
    processed_profile = {}
    processed_profile['bio'] = user_info['user'].get('biography')
    processed_profile['city'] = user_info['user'].get('city_id')
    processed_profile['latitude'] = user_info['user'].get('latitude')
    processed_profile['longitude'] = user_info['user'].get('longitude')
    processed_profile['email'] = user_info['user'].get('public_email')
    processed_profile['phone'] = user_info['user'].get(
        'contact_phone_number')
    processed_profile['follower_count'] = user_info['user'].get(
        'follower_count')
    processed_profile['following_count'] = user_info['user'].get(
        'following_count')
    return processed_profile


def run_result_loop(method, user_id, api):
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

def main(api, user_id, debug):
    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api - crawler')
    logger.setLevel(logging.WARNING)
    if debug:
        logger.setLevel(logging.DEBUG)

    user_profile = extract_user_info(user_id, api)
    followers = run_result_loop('followers', user_id, api)
    following = run_result_loop('following', user_id, api)
    
    # validation
    assert len(followers) == user_profile['follower_count']
    assert len(following) == user_profile['following_count']

    return user_profile, followers, following

if __name__ == '__main__':
    import json
    import os.path
    import argparse

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='Pagination demo')
    parser.add_argument('-u', '--username', dest='username',
                        type=str, required=True)
    parser.add_argument('-p', '--password', dest='password',
                        type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()

    print('Client version: %s' % client_version)
    api = Client(args.username, args.password)

    # user_id = '2958144170'
    origin = api.username_info('roablep')
    user_id = origin['user']['pk']

    user_profile, followers, following = main(api, user_id, args.debug)
    # print list of user IDs
    print(json.dumps([u['username'] for u in followers], indent=2))
    print(json.dumps([u['username'] for u in following], indent=2))
    # for u in followers
