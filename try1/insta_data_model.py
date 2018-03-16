def parse_insta_user_obj(user_obj):
    assert isinstance(user_obj, dict)
    parsed_obj = {
          'user_id'  : user_obj.get('pk')
        , 'user_name': user_obj.get('username')
        , 'full_name': user_obj.get('full_name')
        , 'follower_count': user_obj.get('follower_count')
        , 'following_count': user_obj.get('following_count')
        , 'bio': user_obj.get('biography')
        , 'external_url': user_obj.get('external_url')
        , 'email': user_obj.get('public_email')
        , 'phone': user_obj.get('contact_phone_number')
        , 'city_id': user_obj.get('city_id')
        , 'latitude': user_obj.get('latitude')
        , 'longitude': user_obj.get('longitude')
    }
    return parsed_obj