from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################################
@app.get("/")
@x.no_cache
def show_index():
    try:
        return render_template("page_index.html", x=x)
    except Exception as ex:
        ic(ex)
        return "oops...", 500    

##############################################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "oops...", 500    

##############################################
@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        user_hashed_password = generate_password_hash(user_password)
        # ic(user_hashed_password) 'scrypt:32768:8:1$YSDh1wLwPlKLdF6E$5fc1e1d3b3d036165f3564cd9ad60e6d0bbb9d520e2e726227c73eab1fd99e8bb69eb29844bc9ae493791986453268eb7fccc52c5696a2675c14030da6709e07'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
            <browser mix-replace="form">{form_signup}</browser>
            <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already in the system"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################################
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user:
            return render_template("page_login.html", user=user, x=x)
        return redirect("/profile")
    except Exception as ex:
        ic(ex)
        return "oops...", 500

##############################################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400
        
        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        user.pop("user_password")
        session["user"] = user

        return f"""<browser mix-redirect="/profile"></browser>"""

    except Exception as ex:
        ic(ex)

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser> """, 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################################
@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")

        db, cursor = x.db()
        q = "SELECT * FROM travels WHERE user_fk = %s ORDER BY travel_created_at DESC"
        cursor.execute(q, (user["user_pk"],))
        travels = cursor.fetchall()

        return render_template("page_profile.html", user=user, travels=travels, x=x)
    except Exception as ex:
        ic(ex)
        return "oops...", 500

##############################################
@app.get("/logout")
def logout():
    try:
       session.clear()
       return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "oops...", 500

##############################################
@app.post("/api-create-travel")
def api_create_travel():
    try:
        user = session.get("user", "") # Checks if a user is logged in, if not, return 401 (Unauthorized credentials)
        if not user:
            return "Unauthorized", 401

        travel_title = x.validate_travel_title()
        travel_country = x.validate_travel_country()
        travel_location = x.validate_travel_location()
        travel_start_date = x.validate_travel_start_date()
        travel_end_date = x.validate_travel_end_date()
        travel_description = x.validate_travel_description()

        travel_pk = uuid.uuid4().hex
        travel_created_at = int(time.time())

        db, cursor = x.db()
        q = """
        INSERT INTO travels VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NULL,%s,NULL)
        """
        cursor.execute(q, (travel_pk, user["user_pk"], travel_title, travel_country, travel_location, travel_start_date, travel_end_date, travel_description, travel_created_at))
        db.commit()

        return """<browser mix-redirect="/profile"></browser>""", 201

    except Exception as ex:
        ic(ex)
        return "oops...", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################################
@app.get("/travel/<travel_pk>")
@x.no_cache
def show_travel_single(travel_pk):
    try:
        user = session.get("user", "")
        if not user:
            return redirect("/login")

        db, cursor = x.db()

        q = "SELECT * FROM travels WHERE travel_pk = %s AND user_fk = %s"
        cursor.execute(q, (travel_pk, user["user_pk"]))
        travel = cursor.fetchone()

        if not travel:
            return "Travel not found", 404


        return render_template("page_travel_singleview.html", travel=travel, user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "oops...", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################################
@app.delete("/travel/<travel_pk>")
def delete_travel_single(travel_pk):
    try:
        user = session.get("user", "")
        if not user:
            return redirect("/login")

        db, cursor = x.db()

        q = """DELETE FROM travels WHERE travel_pk = %s AND user_fk = %s"""
        cursor.execute(q, (travel_pk, user["user_pk"]))
        db.commit()

        if cursor.rowcount == 0:
            return "Travel not found", 404

        return """<browser mix-redirect="/profile"></browser>""", 200   

    except Exception as ex:
        ic(ex)
        return "oops...", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()                