import logging
import time
import insta_data_model as idm
from instagram_private_api.errors import ClientThrottledError


logging.basicConfig()
logger = logging.getLogger('instagram_private_api - crawler')

class InstaCrawler(object):
    def __init__(self, api):
        self.n_crawls = 0
        self.init_time = time.time()
        self.last_crawl_time = None
        self.api = api
       
    def extract_user_info_from_username(self, username):
        try:
            user_info = self.api.username_info(username)
        except ClientThrottledError:
            print('some throttling error')
            print(self.n_crawls, self.last_crawl_time-self.init_time, (self.last_crawl_time-self.init_time)/self.n_crawls)
        self.last_crawl_time = time.time()
        self.n_crawls += 1
        return idm.parse_insta_user_obj(user_info['user'])

    def extract_user_info_from_id(self, user_id):
        try:
            user_info = self.api.user_info(user_id)
        except ClientThrottledError:
            print('Got the right except in id')
            print(self.n_crawls, self.last_crawl_time-self.init_time, (self.last_crawl_time-self.init_time)/self.n_crawls)
        self.last_crawl_time = time.time()
        self.n_crawls += 1
        return idm.parse_insta_user_obj(user_info['user'])

    def run_result_loop(self, method, user_id, max_count=1000):
        user_list = []
        if method == 'followers':
            raise Exception('I disabled this method')
            #action = self.api.user_followers
        if method == 'following':
            action = self.api.user_following

        try:
            results = action(user_id)
        except ClientThrottledError:
            print('Got the right except in following')
            print(self.n_crawls, self.last_crawl_time-self.init_time, (self.last_crawl_time-self.init_time)/self.n_crawls)
        self.last_crawl_time = time.time()
        self.n_crawls += 1
        user_list.extend(results.get('users', []))
        next_max_id = results.get('next_max_id')
        while next_max_id and len(user_list) < max_count:
            results = action(user_id, max_id=next_max_id)
            user_list.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')

        user_list.sort(key=lambda x: x['pk'])
        return user_list

    def bc_main(self, user_id, debug):
        logger.setLevel(logging.WARNING)
        if debug:
            logger.setLevel(logging.DEBUG)

        user_profile = self.extract_user_info_from_id(user_id)
        #followers = run_result_loop('followers', user_id,)
        following = self.run_result_loop('following', user_id)
        # validation
        try:
            #assert abs(len(followers)-user_profile['follower_count']) < 2
            assert abs(len(following)-user_profile['following_count']) < 2
        except:
            logger.warn('discrepancy between crawled followers and reported followers for %s\n'\
            % user_profile)
        followers = []
        return user_profile, following, followers
