INSERT IGNORE INTO insta_crawl.fitness_influencers
(user_id, user_name, full_name, follower_count, following_count, bio, external_url, city_id, email, phone, latitude, longitude, crawl_date, mod_ts)
SELECT DISTINCT user_id, user_name, full_name, follower_count, following_count, bio, external_url, city_id, email, phone, latitude, longitude, crawl_date, mod_ts 
FROM users
INNER JOIN terms 
	ON LOWER(users.bio) LIKE concat('%',terms.term,'%')
;

INSERT IGNORE INTO insta_crawl.crm
(user_id, user_name, full_name, email, date_added, dist_id)
SELECT DISTINCT user_id, user_name, full_name, email, CURRENT_DATE, FLOOR(1 + RAND( ) *10)
FROM fitness_influencers
WHERE email IS NOT NULL
;