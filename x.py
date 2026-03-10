from flask import request, make_response
import mysql.connector
import re # Regular expressions also called Regex
from functools import wraps
from datetime import datetime # to be able to convert string date into epoch

##############################
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "rejseapp"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)

##############################
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


##############################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
REGEX_USER_FIRST_NAME = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if not re.match(REGEX_USER_FIRST_NAME, user_first_name):
        raise Exception("company_exception user_first_name")
    return user_first_name

##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_USER_LAST_NAME = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(REGEX_USER_LAST_NAME, user_last_name):
        raise Exception("company_exception user_last_name")
    return user_last_name

##############################
REGEX_USER_EMAIL = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_USER_EMAIL, user_email):
        raise Exception("company_exception user_email")
    return user_email

##############################
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password):
        raise Exception("company_exception user_password")
    return user_password

##############################
TRAVEL_TITLE_MIN = 2
TRAVEL_TITLE_MAX = 200
REGEX_TRAVEL_TITLE = f"^.{{{TRAVEL_TITLE_MIN},{TRAVEL_TITLE_MAX}}}$"
def validate_travel_title():
    travel_title = request.form.get("travel_title", "").strip()
    if not re.match(REGEX_TRAVEL_TITLE, travel_title):
        raise Exception("company_exception travel_title")
    return travel_title

##############################
TRAVEL_COUNTRY_MIN = 2
TRAVEL_COUNTRY_MAX = 100
REGEX_TRAVEL_COUNTRY = f"^.{{{TRAVEL_COUNTRY_MIN},{TRAVEL_COUNTRY_MAX}}}$"
def validate_travel_country():
    travel_country = request.form.get("travel_country", "").strip()
    if not re.match(REGEX_TRAVEL_COUNTRY, travel_country):
        raise Exception("company_exception travel_country")
    return travel_country

##############################
TRAVEL_LOCATION_MIN = 2
TRAVEL_LOCATION_MAX = 100
REGEX_TRAVEL_LOCATION = f"^.{{{TRAVEL_LOCATION_MIN},{TRAVEL_LOCATION_MAX}}}$"
def validate_travel_location():
    travel_location = request.form.get("travel_location", "").strip()
    if not re.match(REGEX_TRAVEL_LOCATION, travel_location):
        raise Exception("company_exception travel_location")
    return travel_location

##############################
TRAVEL_DESCRIPTION_MIN = 2
TRAVEL_DESCRIPTION_MAX = 5000
REGEX_TRAVEL_DESCRIPTION = f"^.{{{TRAVEL_DESCRIPTION_MIN},{TRAVEL_DESCRIPTION_MAX}}}$"
def validate_travel_description():
    travel_description = request.form.get("travel_description", "").strip()
    if not re.match(REGEX_TRAVEL_DESCRIPTION, travel_description):
        raise Exception("company_exception travel_description")
    return travel_description

##############################
def validate_travel_start_date():
    travel_start_date = request.form.get("travel_start_date", "").strip()

    if not travel_start_date:
        raise Exception("company_exception travel_start_date")

    try:
        date_obj = datetime.strptime(travel_start_date, "%Y-%m-%d")
        return int(date_obj.timestamp())
    except:
        raise Exception("company_exception travel_start_date")


##############################
def validate_travel_end_date():
    travel_end_date = request.form.get("travel_end_date", "").strip()

    if not travel_end_date:
        raise Exception("company_exception travel_end_date")

    try:
        date_obj = datetime.strptime(travel_end_date, "%Y-%m-%d")
        return int(date_obj.timestamp())
    except:
        raise Exception("company_exception travel_end_date")