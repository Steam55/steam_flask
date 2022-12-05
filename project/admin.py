from crypt import methods
from random import random
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash

from project.utils import get_admin_dashbord_utils
from .models import *
from . import db
from datetime import date, datetime, timedelta
import random

admin = Blueprint('admin', __name__)


# ********************* AUTHENTICATION *********************

@admin.route('/admin_login', methods=['GET'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('admin.dashboard'))
    # flash('Vous devez vous connecter.', 'login_error')
    return render_template('index.html', login_error = True)
    # return redirect(url_for('main.index', login_required = True))


@admin.route('/admin_login', methods=['POST'])
def login_post():
    celphone = request.form.get('celphone')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user exists
    user:User = User.query.filter_by(celphone=celphone).first()
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Numéro de téléphone ou mot de passe erroné. Veuille réessayer.', 'login_error')
        return redirect(url_for('admin.login')) # if the user doesn't exist or password is wrong, reload the page
    else:
        login_user(user, remember=remember)
        return redirect(url_for('admin.dashboard'))


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


# ************************ / AUTHENTICATION ***********************

@admin.route('/admin')
@login_required
def dashboard():
    admin_dashbord_utils = get_admin_dashbord_utils()
    return render_template('admin-dashboard.html', 
        become_seller_request_global_list = admin_dashbord_utils.get('become_seller_request_global_list'), 
        become_delivery_man_request_global_list = admin_dashbord_utils.get('become_delivery_man_request_global_list'), 
    )


@admin.route('/admin', methods=["POST"])
@login_required
def dashboard_post():
    become_seller_request_to_validate_id = request.form.get('become_seller_request_to_validate_id')
    become_deliver_man_request_to_validate_id = request.form.get('become_deliver_man_request_to_validate_id')

    if become_seller_request_to_validate_id:
        my_request:Seller = Seller.query.filter_by(id=int(become_seller_request_to_validate_id), status=1).first()
        if my_request:
            my_request.status = 2
            db.session.commit()

            concerned_user:User = User.query.filter_by(id=my_request.user_id).first()
            concerned_user.is_verified = True
            db.session.commit()


            flash('Demande validée. Génial, nous venons d\'accepter un nouveau vendeur.', 'become_seller_validation_success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Désolé, la demande sélectionnée n\'existe pas ou est déjà validée.', 'become_seller_validation_error')
            return redirect(url_for('admin.dashboard'))

    elif become_deliver_man_request_to_validate_id:
        my_request:DeliveryMan = DeliveryMan.query.filter_by(id=int(become_deliver_man_request_to_validate_id), status=1).first()
        if my_request:
            my_request.status = 2
            db.session.commit()

            concerned_user:User = User.query.filter_by(id=my_request.user_id).first()
            concerned_user.is_verified = True
            db.session.commit()


            flash('Demande validée. Génial, nous venons d\'accepter un nouveau livreur.', 'become_delivery_man_validation_success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Désolé, la demande sélectionnée n\'existe pas ou est déjà validée.', 'become_delivery_man_validation_error')
            return redirect(url_for('admin.dashboard'))

    return redirect(url_for('admin.dashboard'))