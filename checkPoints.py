import requests
import json
from sendMail import send_mail_availability
import time


def check_points_core(user, channel_id, item_id):

    get_response = requests.get(f"https://api.streamelements.com/kappa/v2/points/{channel_id}/{user['username']}")

    if get_response.status_code == 200:
        response_pts = json.loads(get_response.text)

        pts = response_pts['points']

        get_item_response = requests.get(
            f"https://api.streamelements.com/kappa/v2/store/{channel_id}/items")

        if get_item_response.status_code == 200:  # if response successful unpack data
            response = json.loads(get_item_response.text)
            wanted = [i for i in response if i["_id"] == item_id]   # find wanted item

            if pts >= wanted[0]['cost']:    # if user has enough points send me email
                send_mail_availability(user['username'], 'Roshtein', wanted[0]['name'])
                return user # returns user so i can save him into list

        elif get_item_response.status_code == 524 or get_item_response.status_code == 520 or get_item_response.status_code == 502:
            print(get_item_response.status_code, 'check points function')   # just to know where is problem
            return check_points_core(user, channel_id, item_id)    # recursively calling this so i dont lose any user

        elif get_item_response.status_code == 503:
            print(get_item_response.status_code, 'check points function')
            time.sleep(60)
            return check_points_core(user, channel_id, item_id)

        else:
            print(get_item_response.status_code, 'check points function')
            print(get_item_response.text)
            return check_points_core(user, channel_id, item_id)

    elif get_response.status_code == 404:
        print(user['username'], 'nema u streamera zadne pointy')

    else:
        return check_points_core(user, channel_id, item_id)


def check_points(channel_id, item_id, users):
    to_be_claimed = []  # queue which will be filled with available users

    for user in users:  # iterating users
        to_be_claimed.append(check_points_core(user, channel_id, item_id))  # calling function for each user

    return to_be_claimed
