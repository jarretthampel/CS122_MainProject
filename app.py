from os import access
import jwt.utils
import time
import math
import requests

accessKey = {"developer_id": "fba373c0-78b6-4903-b575-7448c8392172",
    "key_id": "9bd3b7ac-7547-4e69-96ef-fb4896592333",
    "signing_secret": "B1JPQQOuN6CtySk4qJKUJ8fFFEHRXgqxU0M3bSji-0Q"}

token = jwt.encode(
    {
        "aud": "doordash",
        "iss": accessKey["developer_id"],
        "kid": accessKey["key_id"],
        "exp": str(math.floor(time.time() + 300)),
        "iat": str(math.floor(time.time())),
    },
    jwt.utils.base64url_decode(accessKey["signing_secret"]),
    algorithm="HS256",
    headers={"dd-ver": "DD-JWT-V1"})

print(token)


endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"

headers = {"Accept-Encoding": "application/json",
           "Authorization": "Bearer " + token,
           "Content-Type": "application/json"}

request_body = { # Modify pickup and drop off addresses below
    "external_delivery_id": "D-12345",
    "pickup_address": "901 Market Street 6th Floor San Francisco, CA 94103",
    "pickup_business_name": "Wells Fargo SF Downtown",
    "pickup_phone_number": "+16505555555",
    "pickup_instructions": "Enter gate code 1234 on the callbox.",
    "dropoff_address": "901 Market Street 6th Floor San Francisco, CA 94103",
    "dropoff_business_name": "Wells Fargo SF Downtown",
    "dropoff_phone_number": "+16505555555",
    "dropoff_instructions": "Enter gate code 1234 on the callbox.",
    "order_value": 1999
}

create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request


print(create_delivery.status_code)
print(create_delivery.text)
print(create_delivery.reason)