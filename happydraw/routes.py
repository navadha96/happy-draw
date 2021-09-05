from happydraw import app
from flask import render_template, redirect, url_for, flash
from happydraw.models import User
from happydraw.forms import SignupForm, LoginForm
from happydraw import db
from flask_login import login_user, logout_user

@app.route("/", methods=['GET','POST'])  # decorator
@app.route("/login", methods=['GET','POST'])  # decorator
def home_page():
    form=LoginForm()
    if form.validate_on_submit():

        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcome, {attempted_user.username}', category='success')
            return redirect(url_for('my_canvas'))
        else:
            flash('Incorrect username or password! Please try again.', category='danger')

    
    return render_template('index.html', form=form)

@app.route("/canvas")  # decorator
def my_canvas():
    return render_template('drawingCanvas.html')

@app.route("/signup", methods=['GET','POST'])  # decorator
def signup_page():
    form = SignupForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('my_canvas'))

    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was a error with creating a user: {err_msg}', category='danger')
    return render_template('signuppage.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have successfully logged out!", category='info')
    return redirect(url_for('home_page'))