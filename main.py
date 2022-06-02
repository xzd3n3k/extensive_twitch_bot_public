from claimItem import claim_item
from checkPoints import check_points
import requests
import datetime
import json
import time


channel_id = ''
item_id = ''
accounts = [
    {'username': '', 'jwt_token': '', 'btc_address': '', 'eth_address': ''},
    {'username': '', 'jwt_token': '', 'btc_address': '', 'eth_address': ''}
]

while True:
    to_be_claimed_nonfiltered = check_points(channel_id, item_id, accounts)
    to_be_claimed_filtered = [acc for acc in to_be_claimed_nonfiltered if acc]

    for user in to_be_claimed_filtered:
        while True:
            get_response = requests.get(f"https://api.streamelements.com/kappa/v2/store/{channel_id}/items")     # get request - checking store with items

            if get_response.status_code == 200:     # if response successful unpack data
                response = json.loads(get_response.text)
                wanted = [i for i in response if i["_id"] == item_id]  # there is stored my item I want to claim

                if wanted[0]['quantity']['current'] != 0:  # if item is in store (is not sold)
                    if 'Bitcoin' in wanted[0]['name']:
                        completed = claim_item(channel_id, item_id, user['jwt_token'], user['btc_address'], user['username'], wanted[0]['name'])  # claim it

                        if completed == 1:
                            time.sleep(8.15)
                            break

                    elif 'Ethereum' in wanted[0]['name']:
                        completed = claim_item(channel_id, item_id, user['jwt_token'], user['eth_address'], user['username'], wanted[0]['name'])
                        if completed == 1:
                            time.sleep(8.15)
                            break

                    else:      # TESTING PURPOSES ONLY
                        completed = claim_item(channel_id, item_id, user['jwt_token'], 'trying user input', user['username'], wanted[0]['name'])
                        if completed == 1:
                            time.sleep(8.15)
                            break
                    time.sleep(8.15)

            elif get_response.status_code == 503:
                print(get_response.status_code)
                time.sleep(30)

            elif get_response.status_code == 524 or get_response.status_code == 520 or get_response.status_code == 502:   # with this type of error I do not want to show response text since
                # it shows whole html page
                print(get_response.status_code)
                print(datetime.datetime.today())
                continue

            else:   # else show any other response statuses if it is not successful
                print(datetime.datetime.today())
                print(get_response.status_code)
                print(get_response.text)
                continue    # and go on start of while cycle
