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


def run_result_loop(method, user_id, api, max_count=600):
    user_list = []
    if method == 'followers':
        action = api.user_followers
    if method == 'following':
        action = api.user_following

    results = action(user_id)
    user_list.extend(results.get('users', []))
    next_max_id = results.get('next_max_id')
    
    while next_max_id and len(user_list) < max_count:
        results = action(user_id, max_id=next_max_id)
        user_list.extend(results.get('users', []))
        next_max_id = results.get('next_max_id')

    user_list.sort(key=lambda x: x['pk'])
    return user_list

def bc_main(api, user_id, debug):
    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api - crawler')
    logger.setLevel(logging.WARNING)
    if debug:
        logger.setLevel(logging.DEBUG)

    user_profile = extract_user_info(user_id, api)
    followers = run_result_loop('followers', user_id, api)
    following = run_result_loop('following', user_id, api)
    
    # validation
    try:
        assert abs(len(followers)-user_profile['follower_count']) < 2
        assert abs(len(following)-user_profile['following_count']) < 2
    except:
        import ipdb; ipdb.set_trace()

    return user_profile, followers, following