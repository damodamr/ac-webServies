from .models import User, get_todays_recent_posts, fill_states, fill_roles, fill_events, fill_activities, fill_objects
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    posts = get_todays_recent_posts()
    statesFill = fill_states()
    rolesFill = fill_roles()
    eventsFill = fill_events()
    activitiesFill = fill_activities()
    objectsFill = fill_objects()
    return render_template('index.html', posts=posts, propsStates=statesFill, propsRoles=rolesFill, propsEvents=eventsFill, propsActivities=activitiesFill, propsObjects=objectsFill)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

      #  if len(username) < 1:
      #      flash('Your username must be at least one character.')
      #  elif len(password) < 5:
      #      flash('Your password must be at least 5 characters.')
        if not User(username).register(password):
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
    object = request.form['object']
    activity = request.form['activity']

    if stateR:
        states, states2 = User(session['username']).get_statesR(stateR)
        for r in states:
            # get the node you return in your query
            my_node = r[0]
            # get the properties of your node
            props = my_node.get_properties()
            flash('This state is connected with following entity: %s .' %my_node, ' with properties: %s.' %props)
        for r in states2:
            my_node = r[0]
            props = my_node.get_properties()
            flash('This state is created in the following event: %s .' %my_node, ' with properties: %s.' %props)

    if stateO:
        states, states2 = User(session['username']).get_statesO(stateO)
        for r in states:
            # get the node you return in your query
            my_node = r[0]
            # get the properties of your node
            props = my_node.get_properties()
            flash('This state is connected with following entity: %s .' %my_node, ' with properties: %s.' %props)
        for r in states2:
            my_node = r[0]
            props = my_node.get_properties()
            flash('This state is created in the following event: %s .' %my_node, ' with properties: %s.' %props)

    if event:
        events, events2 = User(session['username']).get_events(event)
        for r in events:
            # get the node you return in your query
            my_node = r[0]
            # get the properties of your node
            props = my_node.get_properties()
            flash('This event creates following business process state: %s.' %my_node, ' with properties: %s.' %props )
        for r in events2:
            my_node = r[0]
            props = my_node.get_properties()
            flash('This event is part of the following business process activity: %s .' %my_node, ' with properties: %s.' %props)

    if role:
        roles, roles2 = User(session['username']).get_roles(role)
        for r in roles:
            my_node = r[0]
            props = my_node.get_properties()
            flash('This role is part of the following activity: %s .' %my_node, ' with properties: %s.' %props)
        for r in roles2:
            my_node = r[0]
            props = my_node.get_properties()
            flash('This role is in state of: %s .' %my_node, ' with properties: %s.' %props)

    if object:
        objects, objects2= User(session['username']).get_objects(object)
        for r in objects:
             my_node = r[0]
             props = my_node.get_properties()
             flash('This object is manipulated in the following business process state: %s .' %my_node, ' with properties: %s.' %props)

        for r in objects2:
             my_node = r[0]
             props = my_node.get_properties()
             flash('This object is part of the following business process activity: %s .' %my_node, ' with properties: %s.' %props)

    if activity:
        activities = User(session['username']).get_activities(activity)
        for r in activities:
            # get the node you return in your query
            my_node = r[0]
            # get the properties of your node
            props = my_node.get_properties()
            flash('This Activity is made of following business process entities: %s.' %my_node, ' with properties: %s.' %props )

    return redirect(url_for('index'))

@app.route('/add_post2', methods=['POST'])
def add_post2():
    stateCreateR = request.form['stateCreateR']
    stateCreateO = request.form['stateCreateO']
    eventCreate = request.form['eventCreate']
    roleCreate = request.form['roleCreate']
    objectCreate = request.form['objectCreate']
    activityCreate = request.form['activityCreate']

    if not (stateCreateR and stateCreateO and roleCreate and eventCreate and activityCreate and objectCreate):
        flash('You must fill in all boxes to create pattern!')
    else:
        #flash('Creating new pattern: %s, %s, %s, %s, %s') %stateCreate %roleCreate %eventCreate %activityCreate %objectCreate
        User(session['username']).add_node(stateCreateR, stateCreateO, roleCreate, eventCreate, activityCreate, objectCreate)

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
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )