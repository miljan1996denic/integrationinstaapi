from collections import Counter
import json
import os
from app.routers.helpers import calculate_reels_stats, most_liked_photos_with_and_without_tags

from fastapi import APIRouter

router = APIRouter()

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/instagram_data.json")

@router.get(
    "/average_likes_per_post",
    summary="Get average likes per post",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_average_likes = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            total_likes = 0
            total_posts = len(posts)  
            
            for post in posts:
                total_likes += post['like_count']  
            
            if total_posts > 0:
                average_likes = total_likes / total_posts
                user_average_likes[username] = average_likes

    return user_average_likes

@router.get(
    "/most_liked_photos_with_and_without_tags_per_user",
    summary="Comparison of most liked photos with and without tags per user",
    )
async def get_most_liked_photos_with_and_without_tags_per_user():
    with open(path, 'r') as file:
        data = json.load(file)

    most_liked_photos = most_liked_photos_with_and_without_tags(data)
    result = {}
    for username, photos in most_liked_photos.items():
        with_tags = photos["most_liked_with_tags"]
        without_tags = photos["most_liked_without_tags"]
        message = f"User {username} has more likes on tagged photos than on untagged photos."
        if with_tags["like_count"] < without_tags["like_count"]:
            message = f"User {username} has more likes on untagged photos than on tagged photos."
        result[username] = {
            "most_liked_with_tags": with_tags,
            "most_liked_without_tags": without_tags,
            "message": message
        }
    return result

@router.get(
    "/most_liked_post_per_user",
    summary="The most liked post per user",
    )
async def get_most_liked_photos_with_and_without_tags_per_user():
    with open(path, 'r') as file:
        data = json.load(file)

    most_liked_posts = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            max_likes = 0
            most_liked_post = None
            
            for post in posts:
                if post['like_count'] > max_likes:
                    max_likes = post['like_count']
                    most_liked_post = {
                        'like_count': post['like_count'],
                        'caption': post['caption'],
                        'permalink': post['permalink']
                    }
            
            if most_liked_post is not None:
                most_liked_posts[username] = most_liked_post

    return most_liked_posts

@router.get(
    "/most_liked_tagged_photo_per_user",
    summary="The most liked tagged photo per user",
    )
async def get_most_liked_tagged_photo_per_user():
    with open(path, 'r') as file:
        data = json.load(file)

    most_liked_tagged_photos = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            most_liked_tagged_photo = {"permalink": "", "like_count": 0, "caption": ""}

            for post in posts:

                if post.get('hashtags_from_caption'):

                    if post['like_count'] > most_liked_tagged_photo['like_count']:

                        most_liked_tagged_photo['permalink'] = post['permalink']
                        most_liked_tagged_photo['like_count'] = post['like_count']
                        most_liked_tagged_photo['caption'] = post['caption']
            most_liked_tagged_photos[username] = most_liked_tagged_photo

    return most_liked_tagged_photos

@router.get(
    "/followers_likes_ratio",
    summary="get the ratio of likes to followers for each user",
    )
async def get_followers_likes_ratio():
    with open(path, 'r') as file:
        data = json.load(file)

    followers_likes_ratio = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            total_followers = 0
            total_likes = 0

            for post in posts:
                total_followers = post['followers_count']
                total_likes += post['like_count']

            if total_followers > 0:
                followers_likes_ratio[username] = total_likes / total_followers

    return {"followers_likes_ratio": followers_likes_ratio}


@router.get(
    "/followers_following_ratio",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_followers_following_ratio = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            followers_count = posts[0]['followers_count']  
            follows_count = posts[0]['follows_count']  

            if followers_count > 0:
                followers_following_ratio = followers_count / follows_count
                user_followers_following_ratio[username] = round(followers_following_ratio, 2)

    return user_followers_following_ratio

@router.get(
    "/average_comments_per_post",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_average_comments_per_post = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            total_comments = 0
            total_posts = len(posts)

            for post in posts:
                total_comments += post['comments_count']

            if total_posts > 0:
                average_comments = total_comments / total_posts
                user_average_comments_per_post[username] = round(average_comments, 2)

    return user_average_comments_per_post

@router.get(
    "/engagement_rate",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_average_comments_per_post = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            total_comments = 0
            total_posts = len(posts)

            for post in posts:
                total_comments += post['comments_count']

            if total_posts > 0:
                average_comments = total_comments / total_posts
                user_average_comments_per_post[username] = round(average_comments, 2)
    
    return user_average_comments_per_post

@router.get(
    "/user_reels_stats",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_reels_stats = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            reels_count, average_likes_per_reel = calculate_reels_stats(posts)
            user_reels_stats[username] = {
                'reels_count': reels_count,
                'average_likes_per_reel': round(average_likes_per_reel, 2)
            }
    return user_reels_stats

@router.get(
    "/trending_hashtags",
    )
async def get_average_likes_per_post():
    with open(path, 'r') as file:
        data = json.load(file)

    user_hashtags_counter = {}

    for user_posts in data:
        for username, posts in user_posts.items():
            hashtags_counter = Counter()
            for post in posts:
                hashtags = post.get('hashtags_from_caption', [])
                hashtags_counter.update(hashtags)
            user_hashtags_counter[username] = hashtags_counter

    return user_hashtags_counter
