import requests
from requests.structures import CaseInsensitiveDict
import datetime
import json
import time
from sendMail import send_mail


def claim_item(channel_id, item_id, jwt, user_input, user, item_name):  # claim function which makes post requests and other stuff
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {jwt}"
    headers["Content-Type"] = "application/json"
    data = json.dumps({"input": [user_input]})  # headers settings and user input added

    claim_response = requests.post(
        f"https://api.streamelements.com/kappa/v2/store/{channel_id}/redemptions/{item_id}", headers=headers,
        data=data)  # post request - 'claim'

    time_to_retry = datetime.datetime.fromtimestamp(int(claim_response.headers["x-ratelimit-reset"]) / 1000.0)
    # variable to store when does number of posts per minute reset

    if claim_response.headers["x-ratelimit-remaining"] == '0':
        while (datetime.datetime.fromtimestamp(time.time())) <= (time_to_retry):  # waiting for restriction to expire
            pass

    if claim_response.status_code == 200:  # checking response status - if 200 it means
        # script successfully claimed item
        print(claim_response.status_code)
        print("claimed", user_input)
        print(datetime.datetime.today())
        send_mail(user, 'Roshtein', item_name)
        return 1

    else:  # else show any other response statuses if it is not successful
        print(claim_response.status_code)
        print(claim_response.text)
        print(datetime.datetime.today())

    return 0
