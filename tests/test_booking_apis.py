import pytest

from test_utils.test_booking_utils import create_token_auth, get_all_booking_ids, \
    get_booking_ids_with_firstname_and_lastname, get_booking_ids_with_checkin_and_checkout, get_all_booking_details, \
    create_booking, partial_update_bookings, delete_booking_details_with_id


def test_authentication_token_with_positive_testcases():
    create_token_auth_response, status_code = create_token_auth("admin", "password123")

    assert status_code == 200
    assert "token" in create_token_auth_response.keys()
    # assert create_token_auth_response["reason"] == "Bad credentials"

@pytest.mark.parametrize("username",[(""), ("vinay"), (75347), ("&*^%"), ("vinay6515"), ("vinay%$^"),
                                     ("1123$%"), ("GF%$769"), ("F @15h "), ("VINAY"), ("VInaY"),("   "), ("  Vinay")])
def test_authentication_token_with_negative_testcases_for_username(username):
    create_token_auth_response, status_code = create_token_auth(username, password = "password123")
    assert create_token_auth_response["reason"] == "Bad credentials"

@pytest.mark.parametrize("password",[(""), ("VHjvh"), (673487), ("&*%$"), ("vhg715"), ("vhgj%$^"),
                                     ("11$%"), ("GF%$79"), ("k @15p "), ("HFVHJ"), ("VIjhgY"),("   "), ("  nfHj")])
def test_authentication_token_with_negative_testcases_for_password(password):
    create_token_auth_response, status_code = create_token_auth("admin" , password)
    assert create_token_auth_response["reason"] == "Bad credentials"

def test_received_booking_ids():
    get_all_booking_ids_response = get_all_booking_ids()
    assert len(get_all_booking_ids_response)>0

@pytest.mark.parametrize("firstname, lastname",[("James","Brown"),("Vinay", "Kumar"), ("Doraemon", "Nobita")])
def test_received_booking_id_with_firstname_and_lastname(firstname, lastname):
    get_booking_ids_with_firstname_and_lastname_response = get_booking_ids_with_firstname_and_lastname(firstname, lastname)
    assert len(get_booking_ids_with_firstname_and_lastname_response) == 1

@pytest.mark.parametrize("firstname",[("James"), ("    "), (652467), ("%^#@$"), ("56^%9"),
                                      ("cfg%$"),("3#4Ty"),("2 tr 6H%#"), ("Vinay Kumar")])
def test_received_booking_id_with_negativefirstname_and_positivelastname(firstname):
    get_booking_ids_with_firstname_and_lastname_response = get_booking_ids_with_firstname_and_lastname(firstname, "brown")
    assert get_booking_ids_with_firstname_and_lastname_response["error"] == "Enter the valid firstname"

@pytest.mark.parametrize("lastname",[("Kumar"), ("  "), (2354098), (")(*&^"), ("$%87*9"),
                                      ("%gf$jn"),("3#4Ty"),("d 459 gd^$"), ("Kumar Reddy")])
def test_received_booking_id_with_positivefirstname_and_negativelastname(lastname):
    get_booking_ids_with_firstname_and_lastname_response = get_booking_ids_with_firstname_and_lastname("Vinay", lastname)
    assert get_booking_ids_with_firstname_and_lastname_response["error"] == "Enter the valid lastname"

@pytest.mark.parametrize("checkin, checkout",[("",""),("2014-03-13", "2014-05-21"), ("", "2014-03-13"), ("2014-02-21","")])
def test_received_booking_id_with_checkin_and_checkout(checkin, checkout):
    get_booking_ids_with_checkin_and_checkout_response = get_booking_ids_with_checkin_and_checkout(checkin, checkout)
    assert len(get_booking_ids_with_checkin_and_checkout_response) > 0

@pytest.mark.parametrize("checkin",[("vcjyf"), ("  "),(")(*&^"), ("$%43"),
                                    ("d 459 gd^$"), ("2015-03-17")])
def test_received_booking_id_with_negativecheckin_and_positivecheckout(checkin):
    get_booking_ids_with_checkin_and_checkout_response = get_booking_ids_with_checkin_and_checkout(checkin, "2014-05-21")
    assert get_booking_ids_with_checkin_and_checkout_response["error"] == "Enter the valid checkin"

@pytest.mark.parametrize("checkout",[("NFDzxhj"), ("        "),("!#$^56"), ("$frd%43"),
                                    ("ky 34@^*"), ("2007-03-17")])
def test_received_booking_id_with_positivecheckin_and_negativecheckout(checkout):
    get_booking_ids_with_checkin_and_checkout_response = get_booking_ids_with_checkin_and_checkout("2014-03-13",checkout)
    assert get_booking_ids_with_checkin_and_checkout_response["error"] == "Enter the valid checkout"

@pytest.mark.parametrize("id", [(1), (30), (108)])
def test_get_all_booking_details_with_positive_entries(id):
    get_all_booking_details_response ,status_code= get_all_booking_details(id)
    assert status_code == 200
    assert len(get_all_booking_details_response) > 0

@pytest.mark.parametrize("id", [(599), ("gjfehyh"), ("   "), ("!@*^&"), ("mh%$Y"), ("Fg49H1k"),
                                ("54&^8@3"), (" 1@b$T#r")])
def test_get_all_booking_details_with_negative_entries(id):
    get_all_booking_details_response ,status_code_1= get_all_booking_details(id)
    assert status_code_1 != 200

@pytest.mark.parametrize("firstname", [("Vinay"), ("Vinay Kumar"), ("Kamatham")])
def test_create_bookings_with_positive_firstname(firstname):
    create_bookings_response = create_booking(firstname, "Brown", 111, True, "2018-01-01", "2019-01-01", "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == firstname
    assert create_bookings_response["booking"]["lastname"] == "Brown"
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2018-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("firstname", [("    "), (652467), ("%^#@$"), ("56^%9"),
                                      ("cfg%$"),("3#4Ty"),("2 tr 6H%#")])
def test_create_bookings_with_negative_firstname(firstname):
    create_bookings_response = create_booking(firstname, "Brown", 111, True, "2018-01-01", "2019-01-01", "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid firstname"

@pytest.mark.parametrize("lastname", [("Brown"), ("Kumar Reddy"), ("lastNAME")])
def test_create_bookings_with_positive_lastname(lastname):
    create_bookings_response = create_booking("Vinay", lastname, 111, True, "2018-01-01", "2019-01-01", "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == lastname
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2018-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("lastname", [("    "), (2143589), ("()*^%&)"), ("6^0%7"),
                                      ("kihi%$"),("0#9Jo"),("5 tr ^%#8")])
def test_create_bookings_with_negative_lastname(lastname):
    create_bookings_response , status_code = create_booking("Vinay Kumar", lastname, 111, True, "2018-01-01", "2019-01-01", "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid lastname"


@pytest.mark.parametrize("totalprice", [(189), (674689), (3527)])
def test_create_bookings_with_positive_totalprice(totalprice):
    create_bookings_response = create_booking("Vinay", "Kumar", totalprice, True, "2018-01-01", "2019-01-01", "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == "Kumar"
    assert create_bookings_response["booking"]["totalprice"] == totalprice
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2018-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("totalprice", [("    "), (21435.89), ("()*^%&)"), ("6^0%7"),
                                      ("kihi%$"),("0#9Jo"),("5 tr ^%#8")])
def test_create_bookings_with_negative_totalprice(totalprice):
    create_bookings_response, status_code= create_booking("Vinay", "Kumar", totalprice, True, "2018-01-01", "2019-01-01", "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid totalprice"

@pytest.mark.parametrize("depositpaid", [(True), (False)])
def test_create_bookings_with_positive_depositpaid(depositpaid):
    create_bookings_response = create_booking("Vinay", "Kumar", 111, depositpaid, "2018-01-01", "2019-01-01", "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == "Kumar"
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == depositpaid
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2018-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("depositpaid", [("    "), (21435.89), ("()*^%&)"), ("5 tr ^%#8")])
def test_create_bookings_with_negative_depositpaid(depositpaid):
    create_bookings_response, status_code= create_booking("Vinay", "Kumar", 111, depositpaid, "2018-01-01", "2019-01-01", "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid depositpaid"

@pytest.mark.parametrize("checkin", [("2018-01-01"), ("2024-12-23")])
def test_create_bookings_with_positive_checkin(checkin):
    create_bookings_response = create_booking("Vinay", "Kumar", 111, True, checkin, "2019-01-01", "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == "Kumar"
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == checkin
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("checkin", [("    "), ("2030-01-01"), ("2024-15-23"),
                                     ("2018-01-74"), ("2026-13-94"), ("5 tr ^%#8")])
def test_create_bookings_with_negative_checkin(checkin):
    create_bookings_response, status_code= create_booking("Vinay", "Kumar", 111, True, checkin, "2019-01-01", "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid checkin"

@pytest.mark.parametrize("checkout", [("2019-02-01"), ("2024-12-23")])
def test_create_bookings_with_positive_checkout(checkout):
    create_bookings_response = create_booking("Vinay", "Kumar", 111, True, "2019-01-01", checkout , "Breakfast")
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == "Kumar"
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2019-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == checkout
    assert create_bookings_response["booking"]["additionalneeds"] == "Breakfast"

@pytest.mark.parametrize("checkout", [("    "), ("2030-10-10"), ("2024-27-31"),
                                     ("2020-01-59"), ("2026-13-94"), ("Vtgj65# &9")])
def test_create_bookings_with_negative_checkout(checkout):
    create_bookings_response, status_code= create_booking("Vinay", "Kumar", 111, True, "2019-01-01", checkout, "Breakfast")
    assert create_bookings_response["error"] == "Enter the valid checkout"

@pytest.mark.parametrize("additionalneeds", [("Brown"), ("Kumar Reddy"), ("Additionalneeds")])
def test_create_bookings_with_positive_additionalneeds(additionalneeds):
    create_bookings_response = create_booking("Vinay", "Kumar", 111, True, "2018-01-01", "2019-01-01", additionalneeds)
    create_bookings_response = create_bookings_response[0]
    assert "bookingid" in create_bookings_response.keys()
    assert create_bookings_response["booking"]["firstname"] == "Vinay"
    assert create_bookings_response["booking"]["lastname"] == "Kumar"
    assert create_bookings_response["booking"]["totalprice"] == 111
    assert create_bookings_response["booking"]["depositpaid"] == True
    assert create_bookings_response["booking"]["bookingdates"]["checkin"] == "2018-01-01"
    assert create_bookings_response["booking"]["bookingdates"]["checkout"] == "2019-01-01"
    assert create_bookings_response["booking"]["additionalneeds"] == additionalneeds

@pytest.mark.parametrize("additionalneeds", [("    "), (2143589), ("()*^%&)"), ("6^0%7"),
                                      ("kihi%$"),("0#9Jo"),("5 tr ^%#8")])
def test_create_bookings_with_negative_additionalneeds(additionalneeds):
    create_bookings_response , status_code = create_booking("Vinay Kumar", "Reddy", 111, True, "2018-01-01", "2019-01-01", additionalneeds)
    assert create_bookings_response["error"] == "Enter the valid additionalneeds"

@pytest.mark.parametrize("id, depositpaid", [(3, True), (8, False)])
def test_partial_update_bookings_with_positive_depositpaid(id, depositpaid):
    partial_update_bookings_response = partial_update_bookings(id, depositpaid)
    partial_update_bookings_response = partial_update_bookings_response[0]
    assert "firstname" in partial_update_bookings_response.keys()
    assert "lastname" in partial_update_bookings_response.keys()
    assert "totalprice" in partial_update_bookings_response.keys()
    assert "depositpaid" in partial_update_bookings_response.keys()
    assert "bookingdates" in partial_update_bookings_response.keys()
    assert "additionalneeds" in partial_update_bookings_response.keys()

@pytest.mark.parametrize("id, depositpaid", [(34, "    "), ("hgfhj", 21435.89), ("HG^%l676", "()*^%&)"), ("564", "5 tr ^%#8")])
def test_partial_update_bookings_with_negative_depositpaid(id, depositpaid):
    create_bookings_response, status_code= create_booking(id, depositpaid)
    assert create_bookings_response["error"] == "Enter the valid depositpaid"

@pytest.mark.parametrize("id", [(1), (30), (108)])
def test_delete_booking_details_with_positive_entries(id):
    status_code= delete_booking_details_with_id(id)
    assert status_code == 200

@pytest.mark.parametrize("id", [(599), ("gjfehyh"), ("   "), ("!@*^&"), ("mh%$Y"), ("Fg49H1k"),
                                ("54&^8@3"), (" 1@b$T#r")])
def test_delete_booking_details_with_negative_entries(id):
    status_code= delete_booking_details_with_id(id)
    assert status_code != 200