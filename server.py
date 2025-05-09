import json
from datetime import datetime

from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    found_club = [club for club in clubs if club['email'] == request.form['email']]
    if found_club:
        club = found_club[0]
        flash('You were successfully logged in')

        for comp in competitions:
            date_obj = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
            comp['is_past'] = date_obj < datetime.now()

        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Invalid email')
        return render_template('index.html')

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub[0],competition=foundCompetition[0])
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")

    if placesRequired <= 0:
        flash("Number of places must be greater than zero")
        return render_template('booking.html', club=club, competition=competition)

    if competition_date < datetime.now():
        flash("You can't book a past competition")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > club_points:
        flash("You don't have enough points")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > 12:
        flash("You can't book more than 12 places")
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = str(club_points - placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/points')
def points_board():
    return render_template('points_board.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))