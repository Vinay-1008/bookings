
import requests
import json

from configuration.booking_link_apis import AUTHENTICATION, GET_ALL_BOOKING_IDS, GET_BOOKING_IDS_WITH_FIRSTNAME_AND_LASTNAME, \
    GET_BOOKING_IDS_WITH_CHECKIN_AND_CHECKOUT, GET_BOOKING_DETAILS, CREATE_BOOKING, PARTIAL_UPDATE_BOOKING_DETAILS, \
    DELETE_BOOKING_DETAILS_WITH_ID1


def create_token_auth(username, password):
    body = {
            "username": username ,
            "password": password
    }
    response = requests.post(AUTHENTICATION, json = body)
    return response.json(), response.status_code

def get_all_booking_ids():
    response = requests.get(GET_ALL_BOOKING_IDS)
    return response.json()


def get_booking_ids_with_firstname_and_lastname(firstname, lastname):
    response = requests.get(f"{GET_BOOKING_IDS_WITH_FIRSTNAME_AND_LASTNAME}booking?firstname={firstname}&lastname={lastname}")
    return response.json()

def get_booking_ids_with_checkin_and_checkout1(checkin, checkout):
    auth_response = requests.post("https://restful-booker.herokuapp.com/auth", {
    "username" : "admin",
    "password" : "password123"
        }, headers= {"User-Agent":"PostmanRuntime/7.42.0"})
    headers = {"Authorization": auth_response.json()["token"]}
    response = requests.get(f"{GET_BOOKING_IDS_WITH_CHECKIN_AND_CHECKOUT}booking?checkin={checkin}&checkout={checkout}", headers=headers)
    return response.json(), response.status_code

def get_all_booking_details(id):
    response = requests.get(f"{GET_BOOKING_DETAILS}{id}")
    return response.json() ,response.status_code

def create_booking(firstname, lastname, totalprice, depositpaid, checkin, checkout, breakfast):
    body = {
        "firstname" : firstname,
        "lastname" : lastname,
        "totalprice" : totalprice,
        "depositpaid" : depositpaid,
        "bookingdates" : {
            "checkin" : checkin,
            "checkout" : checkout
        },
        "additionalneeds" : breakfast
    }
    response = requests.post(CREATE_BOOKING, json = body)
    if response.status_code == 200:
        return response.json(), response.status_code

def partial_update_bookings(id, depositpaid):
    body = { "depositpaid" : depositpaid }
    response = requests.patch(f"{PARTIAL_UPDATE_BOOKING_DETAILS}{id}", json = body)
    if response.status_code == 200:
        return response.json(), response.status_code

def delete_booking_details_with_id(id):
    response = requests.delete(f"{DELETE_BOOKING_DETAILS_WITH_ID1}{id}")
    return response.status_code