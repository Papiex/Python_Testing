import json
import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs(clubs):
    with open(clubs) as c:
        clubs_list = json.load(c)["clubs"]
        return clubs_list


def load_competitions(competitions):
    with open(competitions) as comps:
        competitions_list = json.load(comps)["competitions"]
        return competitions_list


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = "something_special"
    if app.config["TESTING"] == True:
        competitions = load_competitions("tests/competitions_test.json")
        clubs = load_clubs("tests/clubs_test.json")
    else:
        competitions = load_competitions("competitions.json")
        clubs = load_clubs("clubs.json")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/show_summary", methods=["POST"])
    def show_summary():
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        try:
            club = [club for club in clubs if club["email"] == request.form["email"]][0]
            return render_template(
                "welcome.html",
                club=club,
                competitions=competitions,
                date_string=date_string,
            )
        except IndexError:
            error = "Sorry, that email wasn't found."
            return render_template("index.html", error=error), 401

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        try:
            found_club = [c for c in clubs if c["name"] == club][0]
            found_competition = [c for c in competitions if c["name"] == competition][0]
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )
        except IndexError:
            flash("Something went wrong-please try again")
            return render_template(
                "welcome.html",
                club=club,
                competitions=competitions,
                date_string=date_string,
            )

    @app.route("/purchase_places", methods=["POST"])
    def purchase_places():
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        places_required = int(request.form["places"])
        if int(club["points"]) < places_required * 3:
            flash("You cannot use more points then you have !")
            render_template("booking.html", club=club, competition=competition)
        elif int(competition["number_of_places"]) < places_required:
            flash("This competition does not have enough places")
            render_template("booking.html", club=club, competition=competition)
        elif int(request.form["places"]) > 12:
            flash("You cannot take more than 12 places")
            render_template("booking.html", club=club, competition=competition)
        elif "-" in request.form["places"]:
            flash("You cannot enter negative number")
            render_template("booking.html", club=club, competition=competition)
        else:
            competition["number_of_places"] = (
                int(competition["number_of_places"]) - places_required
            )
            club["points"] = int(club["points"]) - places_required * 3
            flash("Great-booking complete!")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            date_string=date_string,
        )

    @app.route("/display_board")
    def display_board():
        return render_template("board.html", clubs=clubs)

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app
