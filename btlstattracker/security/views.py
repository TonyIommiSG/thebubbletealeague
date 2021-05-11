#security.views.py

from flask import Blueprint,render_template,request
from flask import redirect,url_for

from flask_security import login_required,Security,current_user

from models import *
from btlstattracker import db,app
from btlstattracker.security.forms import ExtendedRegisterForm

@security.register_context_processor
def security_register_processor():
    return dict(register_user_form = ExtendedRegisterForm())

@security.route('/register',methods=['GET','POST'])
def regster_user():
    form = ExtendedRegisterForm()

    if form.validate_on_submit():
        user_datastore.create_user(email=form.email.data,
                                    username = form.username.data,
                                    password = form.password.data)
        # user = User(email=form.email.data,
        #             username=form.username.data,
        #             password=form.password.data)
        #
        # db.session.add(user)
        # db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('security.login'))
    return render_template('security.register_user.html', register_user_form=form)
