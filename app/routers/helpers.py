import json
import os
import re
import requests
from typing import Dict, List

def most_liked_photos_with_and_without_tags(data: List[Dict[str, List[Dict[str, any]]]]) -> Dict[str, Dict[str, Dict[str, any]]]:
    most_liked_photos = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            most_liked_with_tags = {"permalink": "", "like_count": 0, "caption": ""}
            most_liked_without_tags = {"permalink": "", "like_count": 0, "caption": ""}

            for post in posts:

                if post.get('hashtags_from_caption'):

                    if post['like_count'] > most_liked_with_tags['like_count']:

                        most_liked_with_tags['permalink'] = post['permalink']
                        most_liked_with_tags['like_count'] = post['like_count']
                        most_liked_with_tags['caption'] = post['caption']
                else:

                    if post['like_count'] > most_liked_without_tags['like_count']:

                        most_liked_without_tags['permalink'] = post['permalink']
                        most_liked_without_tags['like_count'] = post['like_count']
                        most_liked_without_tags['caption'] = post['caption']

            most_liked_photos[username] = {
                "most_liked_with_tags": most_liked_with_tags,
                "most_liked_without_tags": most_liked_without_tags
            }

    return most_liked_photos

def extract_hashtags_from_caption(caption):
    hashtags = re.findall(r'#(\w+)', caption)
    return hashtags

def save_to_json(data):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/instagram_data.json")
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4) 

def get_instagram_account_info(username, access_token, my_insta_acc_id):
    api_url = f'https://graph.facebook.com/v18.0/{my_insta_acc_id}?fields=business_discovery.username({username})%7Bfollowers_count,follows_count,media%7Bthumbnail_url,permalink,like_count,comments_count,caption,tags%7D%7D&access_token={access_token}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_data = response.json()

        if 'error' in response_data:
            print(f"Error in API response: {response_data['error']['message']}")
            return None

        followers_count = response_data.get('business_discovery', {}).get('followers_count')
        follows_count = response_data.get('business_discovery', {}).get('follows_count')

        media_data = response_data.get('business_discovery', {}).get('media', {}).get('data', [])

        for media_item in media_data:
            media_item['followers_count'] = followers_count
            media_item['follows_count'] = follows_count
            media_item['comments_count'] = media_item.get('comments_count', 0)

            caption = media_item.get('caption')
            if caption:
                hashtags_from_caption = extract_hashtags_from_caption(caption)
                media_item['hashtags_from_caption'] = hashtags_from_caption

        print(f"The Instagram account has {followers_count} followers.")
        return media_data

    except requests.exceptions.RequestException as req_ex:
        print(f"Request error: {req_ex}")
        return None

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        print("Response content:", response.content if hasattr(response, 'content') else None)
        return None
    
def calculate_reels_stats(posts):
    reels_count = 0
    total_likes = 0

    for post in posts:
        permalink = post.get('permalink', '')
        if 'reel' in permalink:
            reels_count += 1
            total_likes += post.get('like_count', 0)

    average_likes_per_reel = total_likes / reels_count if reels_count > 0 else 0
    return reels_count, average_likes_per_reel