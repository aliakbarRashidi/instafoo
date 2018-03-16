import logging
import numpy as np
import insta_data_model as idm

logging.basicConfig()
logger = logging.getLogger('instagram_private_api - crawler')

def extract_user_info(user_id, api):
    user_info = api.user_info(user_id)
    return idm.parse_insta_user_obj(user_info['user'])

def run_result_loop(method, user_id, api, max_count=1000):
    user_list = []
    if method == 'followers':
        action = api.user_followers
    if method == 'following':
        action = api.user_following

    results = action(user_id)
    logger.debug('got initial results')
    user_list.extend(results.get('users', []))
    next_max_id = results.get('next_max_id')
    
    while next_max_id and len(user_list) < max_count:
        results = action(user_id, max_id=next_max_id)
        user_list.extend(results.get('users', []))
        next_max_id = results.get('next_max_id')
        logger.debug('current user list length: %s' %len(user_list))

    user_list.sort(key=lambda x: x['pk'])
    return user_list

def bc_main(api, user_id, debug):
    logger.setLevel(logging.WARNING)
    if debug:
        logger.setLevel(logging.DEBUG)

    logger.debug('getting user_profile')
    user_profile = extract_user_info(user_id, api)
    logger.debug('getting followers')
    followers = run_result_loop('followers', user_id, api)
    logger.debug('getting following')
    following = run_result_loop('following', user_id, api)
    
    # validation
    try:
        assert abs(len(followers)-user_profile['follower_count']) < 2
        assert abs(len(following)-user_profile['following_count']) < 2
    except:
        logger.warn('discrepancy between crawled followers and reported followers for %s\n' % user_profile)

    return user_profile, followers, following