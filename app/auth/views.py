"""
View functions that pertain specifically to user authentification,
login, and logout.
"""

import sys
from flask import request, session, render_template, redirect, url_for
from flask_login import login_user, logout_user
from .req_lib import ReqLib
from . import auth
from .. import db, cas_client
from ..models import User

@auth.route("/login")
def login():
    """
    Redirects to CAS authentification, which returns a ticket to
    validate. If successful, redirects to login prcoessing function.
    """
    try:
        next = request.args.get("next")
        ticket = request.args.get("ticket")
        if not ticket:
            # No ticket, request came from end user, send to CAS login
            cas_login_url = cas_client.get_login_url()
            return redirect(cas_login_url)
        
        netid, _, _ = cas_client.verify_ticket(ticket)
        if not netid:
            return render_template("error.html",
                                   message="Failed to verify ticket")
        
        # Login successfully, redirect according to "next" parameter
        session["netid"] = netid
        if User.query.get(netid) is None:
            return redirect(url_for(".new_user"))
        else:
            login_user(User.query.get(netid))
            return redirect(url_for(next))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@auth.route("/newuser", methods=["GET", "POST"])
def new_user():
    """
    Uses netid retrieved from CAS authentification to make a request to
    the Princeton ActiveDirectory API for information on a member of the
    Princeton community. Returns with:

    department (which department the user belongs to)
    displayname (Full name of the user)
    dn
    eduPersonPrimaryAffiliation (student or faculty)
    mail (user's email address)
    pustatus (is the user a undergraduate, graduate, or faculty?)
    sn (surname)
    uid (NetID)
    universityid (PUID number)
    """
    try:
        netid = session["netid"]
        req_lib = ReqLib()

        req = req_lib.getJSON(req_lib.configs.USERS, uid=netid)
        info = req[0] # req returns as a list containing only one dict
        name_data = info["displayname"].split(" ")
        first = name_data[0]
        last = name_data[-1]
        status = info["pustatus"]
        user_type = "instructor" if status == "faculty" else "student"
        
        # TODO
        email = netid + "@princeton.edu"
        user = User(netid=netid, email=email)
        db.session.add(user)
        db.session.commit()
        login_user(User.query.get(netid))
        return redirect(url_for("main.hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@auth.route("/logout")
def logout():
    """
    Deletes current user session and logs out of CAS
    """
    redirect_url = url_for("auth.logout_callback", _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    return redirect(cas_logout_url)

@auth.route("/logout_callback")
def logout_callback():
    """
    Redirects user to index page after successful logout
    """
    # redirect from CAS logout request after CAS logout successfully
    session.pop("netid", None)
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/testlogin/student")
def test_login_student():
    user = User.query.get("teststudent")
    session["netid"] = "teststudent"
    login_user(user)
    return redirect(url_for("main.hub"))

@auth.route("/testlogin/instructor")
def test_login_instructor():
    user = User.query.get("testinstructor")
    session["netid"] = "testinstructor"
    login_user(user)
    return redirect(url_for("main.hub"))
