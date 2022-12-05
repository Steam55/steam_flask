from curses import flash
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.models import *
from project.utils import create_balance_for_user, create_user_first_address


auth = Blueprint('auth', __name__)

# @auth.route('/login')
# def login():
#     if current_user.is_authenticated :
#         return redirect(url_for('main.dashboard'))
#     # flash('Vous devez vous connecter.', 'login_error')
#     return render_template('index.html', login_error = True)
#     # return redirect(url_for('main.index', login_required = True))

@auth.route('/login', methods=['POST'])
def login_post():
    celphone = request.form.get('celphone')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    # check if the user actually exists
    user:User = User.query.filter_by(celphone=celphone).first()
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return jsonify({
                "status": False,
                "reason": "Télephone ou mot de passe erroné. Veuille réessayer."
            })

    else:
        login_user(user)
        is_delivery_man = DeliveryMan.query.filter_by(user_id=user.id).first()
        is_seller = Seller.query.filter_by(user_id=user.id).first()
            
        return jsonify({
            "status": True,
            "message": "Connexion réussie !",
            "user_id": user.id,
            "is_delivery_man": True if is_delivery_man else False,
            "is_seller": True if is_seller else False
        })


@auth.route('/signup', methods=['POST'])
def signup_post():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    celphone = request.form.get('celphone')
    password = request.form.get('password')
    address_lat = float(request.form.get('address_lat'))
    address_lng = float(request.form.get('address_lng'))
    address_name = request.form.get('address_name')
    address_description = request.form.get('address_description')
    


    if not firstname or not lastname or not celphone or not password or not address_lat or not address_lng or not address_name :
        return jsonify({
                "status": False,
                "reason": "Veuillez remplir tous les champs."
            })

    # role_client = Role.query.filter_by(name="client").first()
    user = User.query.filter_by(celphone=celphone).first() # if this returns a user, then the email already exists in database

    if user : # if a user is found, we want to redirect back to signup page so user can try again
        return jsonify({
                "status": False,
                "reason": "Email ou Numéro de télephone déjà utilisé. Veuillez en utiliser d'autre."
            })
    
    else:

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(
            firstname=firstname, 
            lastname=lastname,
            celphone=celphone,
            password=generate_password_hash(password, method='sha256'),
            is_verified=False,
            is_admin=False
            )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # creation de la nouvelle balance
        create_balance = create_balance_for_user(new_user.id)
        if not create_balance.get('success'):
            
            db.session.delete(new_user)
            db.session.commit()
            return jsonify({
                "status": False,
                "reason": "La creation du compte n'a pas aboutit, veuillez réessayer."
            })
        else:
            first_address = create_user_first_address(new_user.id, address_name, address_description, address_lat, address_lng)
            if not first_address.get('success'):
                db.session.delete(new_user)
                db.session.delete(first_address)
                db.session.commit()
                return jsonify({
                    "status": False,
                    "reason": "La creation du compte n'a pas aboutit, veuillez réessayer."
                })

        return jsonify({
                "status": True,
                "message": "Compte créé avec succès!! \n Veuillez entrer vos informations pour vous connecter."
            })


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    jsonify({
                "status": True,
                "message": "Vous n'êtes plus connecté"
            })