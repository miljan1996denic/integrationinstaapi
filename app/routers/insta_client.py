import datetime
import os
import requests
from app.insta_client.insta_client import debugAccessToken, get_instagram_account_id, get_page_id, getAccountInfo, getCreds, getLongLivedAccessToken
from app.routers.helpers import get_instagram_account_info, save_to_json

from fastapi import APIRouter

router = APIRouter()

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/instagram_data.json")

@router.get(
    "/token",
    summary="Get facebook api token",
    )
async def get_token():
    params = getCreds()
    params['debug'] = 'yes'
    response = getLongLivedAccessToken(params)

    print("\nACCESS TOKEN INFO\n")
    print("Access Token:")
    response = response['json_data']['access_token']
    print (response) # Copy this access token when you run this file and paste it to function getCreds() in define1.py file and you will see the expire date
    return response

@router.get(
    "/token_info",
    summary="Get info about facebook api token",
    )
async def get_token():
    params = getCreds()
    params['debug'] = 'yes'
    response = debugAccessToken(params)

    print ("\nData access expires at: ")
    print (datetime.datetime.fromtimestamp(response['json_data']['data']['data_access_expires_at']))

    print ("\nToken expires at: ")
    print (datetime.datetime.fromtimestamp(response['json_data']['data']['expires_at']))

    return response

@router.get(
    "/bussines_discovery",
    summary="Get info about facebook api token",
    )
async def bussines_discovery():
    params = getCreds()

    page_url = 'https://www.facebook.com/prismaprismaapp'

    page_id = get_page_id(page_url, params['access_token'])
    params['page_id'] = page_id

    if page_id:
        print(f"The Page ID for {page_url} is: {page_id}")
    else:
        print("Failed to retrieve the Page ID.")

    instagram_account_id = get_instagram_account_id(page_id, params['access_token'])

    if instagram_account_id:
        print(f"The Instagram Account ID for the page with ID {page_id} is: {instagram_account_id}")
    else:
        print("Failed to retrieve the Instagram Account ID.")

    params['insta_acc_id'] = instagram_account_id

    params['debug'] = 'no'
    response = getAccountInfo(params)

    print ("\nACC INFO\n")
    print ("username:")
    print(response['json_data']['business_discovery']['username'])
    # print ("\nwebsite:")
    # print(response['json_data']['business_discovery']['website'])
    print ("\nnumber of posts:")
    print(response['json_data']['business_discovery']['media_count'])
    print ("\nfollowers:")
    print(response['json_data']['business_discovery']['followers_count'])
    print ("\nfollowing:")
    print(response['json_data']['business_discovery']['follows_count'])
    print ("\nprofile picture url:")
    print(response['json_data']['business_discovery']['profile_picture_url'])
    print ("\nbiography:")
    print(response['json_data']['business_discovery']['biography'])

    return {
        "username": response['json_data']['business_discovery']['username'],
        # "website": response['json_data']['business_discovery']['website'],
        "number of posts": response['json_data']['business_discovery']['media_count'],
        "followers": response['json_data']['business_discovery']['followers_count'],
        "following": response['json_data']['business_discovery']['follows_count'],
        "profile picture url": response['json_data']['business_discovery']['profile_picture_url'],
        "biography": response['json_data']['business_discovery']['biography']   
    }

@router.get(
    "/users_insta_info",
    summary="Get info about facebook api token",
    )
async def get_users_insta_info():
    params = getCreds()

    page_url = 'https://www.facebook.com/prismaprismaapp'

    page_id = get_page_id(page_url, params['access_token'])
    params['page_id'] = page_id

    if page_id:
        print(f"The Page ID for {page_url} is: {page_id}")
    else:
        print("Failed to retrieve the Page ID.")

    instagram_account_id = get_instagram_account_id(page_id, params['access_token'])

    if instagram_account_id:
        print(f"The Instagram Account ID for the page with ID {page_id} is: {instagram_account_id}")
    else:
        print("Failed to retrieve the Instagram Account ID.")

    instagram_username = ['mudja','lepasvakidan', 'tamara', 'natasa_pejasinovic', 'tatindnevnik']
    
    all_instagram_data = []

    try:
        for name in instagram_username:
            print("\n\n/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
            print(f"\nINSTAGRAM INFO FOR: {name}\n")
            print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
            instagram_data = get_instagram_account_info(name, params['access_token'], instagram_account_id)
            if instagram_data:
                all_instagram_data.append({name: instagram_data})

        save_to_json(all_instagram_data)

    except requests.exceptions.RequestException as req_ex:
        print(f"Request error: {req_ex}")

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

        """
            Run this file and you will get instagram_data.json file with all the data.
        """

