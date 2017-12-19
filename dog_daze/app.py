from flask import Flask, render, request, session, jsonify, flash
import dddb.client as client
import mail_alerts
import datetime
import time
import requests

app = Flask(__name__)

@app.route('/profile')
def profile(request):
    if session['ddaze_session'] != None:
        t_as_str = datetime.strptime(session['ddaze_session'], "%d/%m/%Y %H:%M:%S")
        time_in_seconds = time.mktime(t_as_str.timetuple())
        now_in_seconds = time.mktime(datetime.datetime.now().timetuple())

        if session['ddaze_session']['expr'] > now_in_seconds:
            user_data = decode_session(session)
            stats_url = request.host_url + "/api/stats/" + user_data['user_id']
            activity_url = request.host_url + "/api/activity/" + user_data['user_id']

            stats = requests.get(stats_url)
            activity = requests.get(activity_url)

            return render_template('templates/profile.html', user=session['ddaze_session']['user'],
                                                             stats=stats,
                                                             activity=activity)

@app.route('/', methods=["GET"])
def listings(request):
    if session['ddaze_session'] != None:
        t_as_str = datetime.strptime(session['ddaze_session'], "%d/%m/%Y %H:%M:%S")
        time_in_seconds = time.mktime(t_as_str.timetuple())
        now_in_seconds = time.mktime(datetime.datetime.now().timetuple())

        if session['ddaze_session']['expr'] > now_in_seconds:

            url = request.host_url + "/api/animals"
            listings = requests.get(url)
            return render_template('templates/listings.html', user=session['ddaze_session']['user'],
                                                              listings=listings)


@app.route('/register', methods=["GET", "POST"])
def register(request):
    if request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            new_user = client.create_new_user(username, password, email)
            mail_alerts.send_confirmation(new_user['email'], new_user['username'])
        except:
            flash("Error registering this user. Please try again.")
            redirect("/register")
    return render_template('templates/register.html')


@app.route('api/animals/', methods=["GET"])
def api_get_all_animals():
    try:
        all_animals = client.get_animals()
    except Exception as e:
        print("ERROR: -- `api_get_all_animals` failed; {}".format(e))
    return jsonify(all_animals)


@app.route('api/animals/<animal_type>', methods=["GET"])
def api_get_all_animals(animal_type):
    try:
        animals = client.get_animals(animal_type)
    except Exception as e:
        print("ERROR: -- `api_get_all_animals` failed; {}".format(e))
    return jsonify(animals)


@app.route('api/stats/<user_id>', methods=["GET"])
def api_get_stats(user_id):
    try:
        stats = client.get_user_stats(user_id)
    except Exception as e:
        print("ERROR: -- `api_get_stats` failed; {}".format(e))
    return jsonify(stats)


@app.route('api/activity/<user_id>', methods=["GET"])
def api_get_activity(user_id):
    try:
        stats = client.get_user_activity(user_id)
    except Exception as e:
        print("ERROR: -- `api_get_stats` failed; {}".format(e))
    return jsonify(stats)


if __name__ == "__main__":

    app.run()
