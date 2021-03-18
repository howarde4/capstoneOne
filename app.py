from flask import Flask, redirect, render_template, session, request, flash, jsonify
from models import db, connect_db, User, Allstar
from forms import AddUser, LoginForm
from sqlalchemy.exc import IntegrityError
import os 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///dragdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'shhsecret')

connect_db(app)

@app.route('/')
def home():
    '''home'''
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_form():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = AddUser()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(username, email, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username or email taken. Please try another.')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', 'success')
        return redirect('/users/{user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user: 
            flash(f"Welcome back, {user.username}!", 'primary')
            session['username'] = user.username
            return redirect('/users/{user.username}')
        else:
            form.username.errors = ['Invalid username or password']
    
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')
    
    user = User.query.get_or_404(username)

    return render_template("user.html", user=user)

@app.route('/users/<username>/allstars')
def allstar_list(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')
    
    user = User.query.get_or_404(username)

    return render_template("allstars.html", user=user)

@app.route('/users/<username>/allstars', methods=["POST"])
def create_allstar(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')

    new_allstar = Allstar(name=request.json["name"], img=request.json["image"], quote=request.json["quote"], username=username)
    db.session.add(new_allstar)
    db.session.commit()
    response_json = jsonify(allstar=new_allstar.serialize())
    return (response_json, 201)

@app.route('/allstars/<int:star_id>/delete', methods=["POST"])
def delete_allstar(star_id):
    allstar = Allstar.query.get(star_id)
    if "username" not in session or allstar.username != session['username']:
        flash("Please login first!", 'danger')
        return redirect('/login')

    db.session.delete(allstar)
    db.session.commit()
    flash("Allstar deleted!", "danger")
    return redirect(f'/users/{allstar.username}/allstars')

@app.route('/users/<username>/delete', methods=["POST"])
def deleteuser(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username')
    flash("Goodbye!", 'primary')
    return redirect('/login')