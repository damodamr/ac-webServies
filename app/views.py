from .models import User, get_todays_recent_posts, fill_objects, fill_activities
from flask import Flask, request, session, redirect, url_for, render_template, flash
import pprint
import json
from json2html import *
import HTMLParser

app = Flask(__name__)

@app.route('/')
def index():
    posts = get_todays_recent_posts()
    #statesFill = fill_states()
    #rolesFill = fill_roles()
    #eventsFill = fill_events()
    activitiesFill = fill_activities()
    objectsFill = fill_objects()
    return render_template('index.html', posts=posts,propsActivities=activitiesFill, propsObjects=objectsFill)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        group = request.form['group']
        age = request.form['age']

      #  if len(username) < 1:
      #      flash('Your username must be at least one character.')
      #  elif len(password) < 5:
      #      flash('Your password must be at least 5 characters.')
        if not User(username).register(password, group, age):
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    stateR = request.form['stateR']
    stateO = request.form['stateO']
    event = request.form['event']
    role = request.form['role']
    test = "Search results here"
    test2 = "Search results here"
    html_parser = HTMLParser.HTMLParser()

    if stateR:
        test = User(session['username']).TextSearch(stateR)
        #flash('Freesound output: %s .' %test)
        test = json2html.convert(json=test)


    if stateO:
        test2 = User(session['username']).searchJamendo(stateO)
        #flash('Jamendo output: %s .' %test2)
        test2 = json2html.convert(json=test2)

    if role:
        test, test2 = User(session['username']).get_roles(role)
        #flash('Freesound: %s .' % test)
        #flash('Jamendo: %s .' % test2)
        test = json2html.convert(json=test)
        test2 = json2html.convert(json=test2)

    if event:
        test, test2 = User(session['username']).get_events(event)
        #flash('Freesound list: %s .' %test)
        #flash('Jamendo list: %s .' %test2)
        #flash('DBPedia relations: %s .' % json.dumps(test3, indent=4, sort_keys=True))
        #flash('DBPedia relations: %s .' % json.dumps(test4, indent=4, sort_keys=True))
        test = json2html.convert(json=test)
        test2 = json2html.convert(json=test2)



    #return redirect(url_for('index'))
    return render_template('index.html', test=test, test2=test2 )

@app.route('/add_post2', methods=['POST'])
def add_post2():
    stateCreateR = request.form['options']

    licenceCalcCU = request.form['licenceCU']
    licenceCalcCH = request.form['licenceCH']
    licenceCalcDIST = request.form['licenceDIST']

    stateCreateO = request.form['licence']
    file = request.form['fileinput']
    newSound = request.form['newSound']
    g = User(session['username']).UploadFile(stateCreateR,stateCreateO, file, newSound)
    flash('Ledger output: %s .' % g)
    lice = 'dont know'

    if licenceCalcCU == 'licenceCU2' and licenceCalcCH == 'licenceCH2':
        lice = 'CC_BY_NC_ND'
    if licenceCalcCU == 'licenceCU2' and licenceCalcCH == 'licenceCH1' and licenceCalcDIST == 'licenceDIST2':
        lice = 'CC_BY_NC'
    if licenceCalcCU == 'licenceCU2' and licenceCalcCH == 'licenceCH1' and licenceCalcDIST == 'licenceDIST1':
        lice = 'CC_BY_NC_SA'
    if licenceCalcCU == 'licenceCU1' and licenceCalcCH == 'licenceCH2':
        lice = 'CC_BY_ND'
    if licenceCalcCU == 'licenceCU1' and licenceCalcCH == 'licenceCH1' and licenceCalcDIST == 'licenceDIST2':
        lice = 'CC_BY'
    if licenceCalcCU == 'licenceCU1' and licenceCalcCH == 'licenceCH1' and licenceCalcDIST == 'licenceDIST1':
        lice = 'CC_BY_SA'

    flash('You need licence: %s .' % lice)


    return redirect(url_for('index'))

@app.route('/add_tag', methods=['POST'])
def add_tag():
    file = request.form['fileinput']
    listOfTags = request.form['listOfTags']
    g = User(session['username']).TagFile(listOfTags, file)

    #flash('You added following tags: %s to the file %s.' % listOfTags %audiofile )

    return redirect(url_for('index'))


@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like a post.')
        return redirect(url_for('login'))

    User(username).like_post(post_id)

    flash('Liked post.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    similar = []
    similar2 = []

    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_other_users()
            similar2 = logged_in_user.get_other_users2()
            flash('similar %s' %similar2)
            #flash('similar %s' %similar)
        else:
            #common = logged_in_user.get_commonality_of_user(user_being_viewed)
            flash('common %s' %common)
    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        similar2=similar2,
        common=common
    )