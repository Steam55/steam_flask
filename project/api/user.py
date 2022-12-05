import json
from math import prod
import os
from unicodedata import category, name
from flask import Blueprint, jsonify, request
from project.models import *
from project import db
from werkzeug.utils import secure_filename
from project.models.user import User
from project.utils import create_notification_message, create_slug, get_order_delivery_men, list_in_string_sharp_to_list
import re
from datetime import datetime
from geopy import distance


user = Blueprint('user', __name__)

product_directory = "./project/static/images/food/product/"
seller_cover_directory = "./project/static/images/seller/cover/"
seller_profile_directory = "./project/static/images/seller/profile/"
user_identity_card_directory = "./project/static/images/user/identity_card/"
user_passport_directory = "./project/static/images/user/passport/"


@user.route('/get_user_role', methods=['POST'])
def get_user_role():
    user_id = request.form.get('user_id')
    if user_id:
        my_user: User = User.query.filter_by(id=int(user_id)).first()
        if my_user:
            is_delivery_man = DeliveryMan.query.filter_by(
                user_id=my_user.id, status=2).first()
            is_seller = Seller.query.filter_by(
                user_id=my_user.id, status=2).first()
            return jsonify({
                "status": True,
                "is_delivery_man": True if is_delivery_man else False,
                "is_seller": True if is_seller else False,
                "is_verified": my_user.is_verified
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue. Utilisateur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_user_addresses', methods=['POST'])
def get_user_addresses():
    user_id = request.form.get('user_id')
    if user_id:
        my_addresses:Address = Address.query.filter_by(
            user_id=int(user_id)).all()
        if my_addresses:
            user_addresses = []
            for item in my_addresses:
                address_details = {
                    "address_id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "lng": item.lng,
                    "lat": item.lat,
                    "is_primary": item.is_primary,
                    "user_id": int(user_id)
                }
                if item.is_primary:
                    # Insérer à la première position pour avoir l'addresse primaire à la première place lors des affichages
                    user_addresses.insert(0, address_details)
                else:
                    user_addresses.append(address_details)

            return jsonify({
                "status": True,
                "user_addresses": user_addresses
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue. Addresse non trouvée."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_product_seller_address', methods=['POST'])
def get_product_seller_address():
    product_id = request.form.get('product_id')
    if product_id:
        product:Product = Product.query.filter_by(id=int(product_id)).first()
        if product:
            product_seller:Seller = Seller.query.filter_by(id=product.seller_id).first()
            if product_seller:
                return jsonify({
                    "status": True,
                    "lng": product_seller.address_lng,
                    "lat": product_seller.address_lat
                })
            else:
                return jsonify({
                "status": False,
                "reason": "Une erreur est survenue. Vendeur non trouvé."
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue. Produit non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })

@user.route('/get_delivery_tool_types', methods=['POST'])
def get_delivery_tool_types():
    all_delivery_tool_types: DeliveryToolType = DeliveryToolType.query.all()
    finalDeliveryToolTypes = []
    for tool in all_delivery_tool_types:
        newDeliveryToolType = {
            "id": tool.id,
            "name": tool.name,
        }
        finalDeliveryToolTypes.append(newDeliveryToolType)

    if finalDeliveryToolTypes:
        return jsonify({
            "status": True,
            "delivery_tool_types": finalDeliveryToolTypes
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, aucun outil de livraison trouvé."
        })


@user.route('/become_delivery_man', methods=['POST'])
def become_delivery_man():
    # values about images
    cardType = request.form.get("card_type")
    cardImage = request.files.get('card_image')

    # values about principal delivery zone
    zone_name = request.form.get("zone_name")
    zone_lat = float(request.form.get('zone_lat'))
    zone_lng = float(request.form.get('zone_lng'))
    zone_description = request.form.get("zone_description")
    zone_radius = float(request.form.get("zone_radius"))

    # values about restaurant and user asking to become seller
    user_id = int(request.form.get('user_id'))
    can_make_delivery = request.form.get("can_make_delivery")
    delivery_tools_id = list_in_string_sharp_to_list(
        request.form.get("delivery_tools_id"))
    can_make_video_conference = request.form.get("can_make_video_conference")
    accept_responsibilities = request.form.get("accept_responsibilities")
    about_you = request.form.get("about_you")

    if zone_name and zone_lat and zone_lng and zone_radius and can_make_delivery and delivery_tools_id and can_make_video_conference and accept_responsibilities and about_you:
        user = User.query.filter_by(id=user_id).first()
        if user:
            is_accepted_delivery_man = DeliveryMan.query.filter_by(
                user_id=user.id, status=2).first()
            if not is_accepted_delivery_man:
                if cardImage != "" and cardImage != None:
                    cardImageName = cardImage.filename

                    try:
                        # saving images files to directories
                        if int(cardType) == 1:
                            cardImage.save(
                                user_identity_card_directory + secure_filename(cardImageName))
                        elif int(cardType) == 2:
                            cardImage.save(
                                user_passport_directory + secure_filename(cardImageName))

                    except Exception as e:
                        return jsonify({
                            "status": False,
                            "reason": "L'image de la pièce d'identité n'a pas pu être enrégistrée. Erreur: " + str(e)
                        })

                try:
                    new_delivery_man = DeliveryMan(
                        can_make_delivery=True if int(
                            can_make_delivery) == 1 else False,
                        accept_responsibilities=True if int(
                            accept_responsibilities) == 1 else False,
                        about_you=about_you,
                        can_make_video_conference=True if int(
                            can_make_video_conference) == 1 else False,
                        status=1,
                        user_id=user.id
                    )
                    db.session.add(new_delivery_man)
                    db.session.commit()

                    for tool_id in delivery_tools_id:
                        new_delivery_tool_type_and_delivery_man = DeliveryToolAndDeliveryMan(
                            delivery_tool_type_id=int(tool_id),
                            delivery_man_id=new_delivery_man.id
                        )
                        db.session.add(new_delivery_tool_type_and_delivery_man)
                        db.session.commit()

                    if cardImage != "" and cardImage != None:
                        cardImageName = cardImage.filename
                        new_card = Card(
                            uploaded_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
                            image=cardImageName,
                            type_id=int(cardType),
                            user_id=user.id
                        )
                        db.session.add(new_card)
                        db.session.commit()

                    new_delivery_zone = DeliveryZone(
                        name=zone_name,
                        description=zone_description,
                        radius=zone_radius,
                        lat=zone_lat,
                        lng=zone_lng,
                        delivery_man_id=new_delivery_man.id
                    )
                    db.session.add(new_delivery_zone)
                    db.session.commit()

                except Exception as e:
                    print(str(e))
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, votre demande n'a pas pu être envoyée, veuillez réessayer. Raison: " + str(e)
                    })
                else:
                    # Delete old request of same user
                    old_become_delivery_man_requests_for_user = []
                    old_become_delivery_man_requests = DeliveryMan.query.filter(
                        DeliveryMan.status.in_([1, 3])).all()
                    for item in old_become_delivery_man_requests:
                        if item.user_id == user.id:
                            old_become_delivery_man_requests_for_user.append(
                                item)
                    for my_request in old_become_delivery_man_requests_for_user:
                        if my_request != next(reversed(old_become_delivery_man_requests)):

                            old_delivery_man_and_delivery_tool = DeliveryToolAndDeliveryMan.query.filter_by(
                                delivery_man_id=my_request.id).all()
                            for item in old_delivery_man_and_delivery_tool:
                                # delete these associations
                                db.session.delete(item)
                                db.session.commit()

                            # delete delivery zone associated to that request of delivery man
                            associated_delivery_zone = DeliveryZone.query.filter_by(
                                delivery_man_id=my_request.id).first()
                            db.session.delete(associated_delivery_zone)
                            db.session.commit()

                            # delete the request
                            db.session.delete(my_request)
                            db.session.commit()

                            if user.is_verified == False:
                                # on supprime ses cartes enrégistrées à part celle qu'il vient d'enregistrer
                                old_request_card = Card.query.filter_by(
                                    user_id=user.id).all()
                                for old_request_card_item in old_request_card:

                                    if old_request_card_item != next(reversed(old_request_card)):
                                        # remove card file from directories
                                        if old_request_card_item.type_id == 1:
                                            os.remove(os.path.join(
                                                user_identity_card_directory, old_request_card_item.image))
                                        elif old_request_card_item.type_id == 2:
                                            os.remove(os.path.join(
                                                user_passport_directory, old_request_card_item.image))
                                        db.session.delete(
                                            old_request_card_item)
                                        db.session.commit()

                    return jsonify({
                        "status": True,
                        "message": "Félicitation! Votre demande est envoyée. Vous serez notifié dans les plus brefs délais."
                    })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, l'utilisateur est déjà un vendeur."
                })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, utilisateur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })


@user.route('/become_seller', methods=['POST'])
def become_seller():
    # values about images
    cardImage = request.files.get('card_image')
    profilePicture = request.files.get('profile_picture')
    coverPicture = request.files.get('cover_picture')
    cardType = request.form.get('card_type')

    # values about restaurant and user asking to become seller
    user_id = int(request.form.get('user_id'))
    name = request.form.get('name')
    celphone = request.form.get('celphone')
    email = request.form.get('email')
    description = request.form.get('description')

    # values about principal address of future restaurant
    address_lng = float(request.form.get('address_lng'))
    address_lat = float(request.form.get('address_lat'))

    if name and celphone and email and description and profilePicture and coverPicture and address_lng and address_lat:
        user = User.query.filter_by(id=user_id).first()
        if user:
            is_accepted_seller = Seller.query.filter_by(
                user_id=user.id, status=2).first()
            if not is_accepted_seller:

                profilePictureName = profilePicture.filename
                coverPictureName = coverPicture.filename

                try:
                    # saving images files to directories
                    if cardImage != "" and cardImage != None:
                        cardImageName = cardImage.filename
                        if int(cardType) == 1:
                            cardImage.save(user_identity_card_directory +
                                           secure_filename(cardImageName))
                        elif int(cardType) == 2:
                            cardImage.save(user_passport_directory +
                                           secure_filename(cardImageName))

                    profilePicture.save(
                        seller_profile_directory + secure_filename(profilePictureName))
                    coverPicture.save(seller_cover_directory +
                                      secure_filename(coverPictureName))

                except Exception as e:
                    return jsonify({
                        "status": False,
                        "reason": "Les images n'ont pas pu être enrégistrées. Erreur: " + str(e)
                    })
                else:
                    # if all is ok, continue the process
                    try:
                        new_seller = Seller(
                            name,
                            email,
                            celphone,
                            description,
                            profilePictureName,
                            coverPictureName,
                            address_lng,
                            address_lat,
                            1,
                            user.id
                        )
                        db.session.add(new_seller)
                        db.session.commit()

                        if cardImage != "" and cardImage != None:
                            cardImageName = cardImage.filename
                            new_card = Card(
                                uploaded_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                image=cardImageName,
                                type_id=int(cardType),
                                user_id=user.id
                            )
                            db.session.add(new_card)
                            db.session.commit()

                    except Exception as e:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, votre demande n'a pas pu être envoyée, veuillez réessayer."
                        })
                    else:
                        # Delete old request of same user
                        old_become_seller_requests_for_user = []
                        old_become_seller_requests = Seller.query.filter(
                            Seller.status.in_([1, 3])).all()
                        for item in old_become_seller_requests:
                            if item.user_id == user.id:
                                old_become_seller_requests_for_user.append(
                                    item)
                        for my_request in old_become_seller_requests_for_user:
                            if my_request != next(reversed(old_become_seller_requests)):
                                # if isn't last request of user...
                                # remove cover and profile files from directories
                                os.remove(os.path.join(
                                    seller_cover_directory, my_request.cover_picture))
                                os.remove(os.path.join(
                                    seller_profile_directory, my_request.profile_picture))

                                # delete the request
                                db.session.delete(my_request)
                                db.session.commit()
                                # delete card about it
                                old_request_card = Card.query.filter_by(
                                    user_id=user.id).all()
                                for old_request_card_item in old_request_card:

                                    if old_request_card_item != next(reversed(old_request_card)):
                                        # remove card file from directories
                                        if old_request_card_item.type_id == 1:
                                            os.remove(os.path.join(
                                                user_identity_card_directory, old_request_card_item.image))
                                        elif old_request_card_item.type_id == 2:
                                            os.remove(os.path.join(
                                                user_passport_directory, old_request_card_item.image))
                                        db.session.delete(
                                            old_request_card_item)
                                        db.session.commit()

                        return jsonify({
                            "status": True,
                            "message": "Félicitation! Votre demande est envoyée. Vous serez notifié dans les plus brefs délais."
                        })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, l'utilisateur est déjà un vendeur."
                })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, utilisateur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })


@user.route('/getallproducts', methods=['POST'])
def get_all_products():
    allProducts = Product.query.all()
    if allProducts:
        finalAllProducts = []
        for product in allProducts:
            # productCategories_id: liste des id des catégories du produit
            productCategories = ProductAndCategory.query.filter_by(
                product_id=product.id).all()
            productCategories_id = [
                item.category_id for item in productCategories]
            newProduct = {
                "name": product.name,
                "image": product.image,
                "primary_price": product.primary_price,
                "slug": product.slug,
                "description": product.description,
                "author": product.seller.designation,
                "is_available": product.is_available,
                "hot": product.hot,
                "note": product.note,
                "seller_id": product.seller_id,
                "categories": productCategories_id
            }
            finalAllProducts.append(newProduct)

        return jsonify({
            "status": True,
            "products": finalAllProducts
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, aucun produit trouvé."
        })


@user.route('/getallCategories', methods=['POST'])
def get_all_categories():
    allCategories = Category.query.all()
    finalAllCategories = []
    for category in allCategories:
        newCategory = {
            "slug": category.slug,
            "name": category.name,
            "icon": category.icon
        }
        finalAllCategories.append(newCategory)

    if finalAllCategories:
        return jsonify({
            "status": True,
            "categories": finalAllCategories
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, aucune catégorie n'est trouvée."
        })


@user.route('/get_product', methods=['POST'])
def get_product():
    product_id = int(request.form.get('product_id'))

    product = Product.query.filter_by(id=product_id).first()
    if product:
        # productCategories_id: liste des id des catégories du produit
        productCategories = ProductAndCategory.query.filter_by(
            product_id=product.id).all()
        productCategories_id = [item.category_id for item in productCategories]
        newProductShape = {
            "name": product.name,
            "image": product.image,
            "primary_price": product.primary_price,
            "slug": product.slug,
            "description": product.description,
            "author": product.seller.designation,
            "is_available": product.is_available,
            "hot": product.hot,
            "note": product.note,
            "seller_id": product.seller_id,
            "categories": productCategories_id
        }
        return jsonify({
            "status": True,
            "product": newProductShape
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, le produit n'est pas trouvé."
        })


@user.route('/get_product_with_order', methods=['POST'])
def get_product_with_order():
    order_id = request.form.get('order_id')

    print(order_id)
    if order_id:
        order: Order = Order.query.filter_by(
            id=int(order_id)).first()
        if order:
            product = Product.query.filter_by(id=order.product_id).first()
            if product:
                # productCategories_id: liste des id des catégories du produit
                productCategories = ProductAndCategory.query.filter_by(
                    product_id=product.id).all()
                productCategories_id = [item.category_id for item in productCategories]
                newProductShape = {
                    "name": product.name,
                    "image": product.image,
                    "primary_price": product.primary_price,
                    "slug": product.slug,
                    "description": product.description,
                    "author": product.seller.designation,
                    "is_available": product.is_available,
                    "hot": product.hot,
                    "note": product.note,
                    "seller_id": product.seller_id,
                    "categories": productCategories_id
                }
                return jsonify({
                    "status": True,
                    "product": newProductShape
                })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, le produit n'est pas trouvé."
                })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, le produit en panier n'est pas trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })

@user.route('/getsellerproducts', methods=['POST'])
def get_seller_products():
    user_id = int(request.form.get('user_id'))

    finalSellerProducts = []
    is_seller = Seller.query.filter_by(user_id=user_id, status=2).first()
    if is_seller:
        # tous les produits du vendeur
        sellerProducts = Product.query.filter_by(seller_id=is_seller.id).all()
        for product in sellerProducts:
            # productCategories_id: liste des id des catégories du produit
            productCategories = ProductAndCategory.query.filter_by(
                product_id=product.id).all()
            productCategories_id = [
                item.category_id for item in productCategories]
            newProductShape = {
                "name": product.name,
                "image": product.image,
                "primary_price": product.primary_price,
                "slug": product.slug,
                "description": product.description,
                "author": product.seller.designation,
                "is_available": product.is_available,
                "hot": product.hot,
                "note": product.note,
                "seller_id": product.seller_id,
                "categories": productCategories_id
            }
            finalSellerProducts.append(newProductShape)
        return jsonify({
            "status": True,
            "products": finalSellerProducts
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, vous n'êtes pas un vendeur."
        })


@user.route('/save_product_image', methods=['POST'])
def save_product_image():
    fileImage = request.files.get('file_image')

    if fileImage:
        imageName = fileImage.filename
        try:
            # saving image file to products directory
            fileImage.save(product_directory + secure_filename(imageName))

        except Exception as e:
            return jsonify({
                "status": False,
                "reason": "L'image n'a pas pu être enrégistrée. Erreur: " + str(e)
            })
        else:
            return jsonify({
                "status": True,
                "message": "Image enregistrée.",
                "image_name": imageName
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })


@user.route('/create_product', methods=['POST'])
def create_product():
    user_id = int(request.form.get('user_id'))
    productName = request.form.get('name')
    imageName = request.form.get('image_name')

    primary_price = float(request.form.get('primary_price'))
    description = request.form.get('description')
    hot = request.form.get('hot')
    categories_slug = list_in_string_sharp_to_list(
        request.form.get('categories'))

    is_seller = Seller.query.filter_by(user_id=user_id, status=2).first()
    if is_seller:
        new_slug = create_slug()
        new_product = Product(
            name=productName,
            image=imageName,
            primary_price=primary_price,
            slug="product-" + new_slug,
            description=description,
            is_available=False,
            hot=True if hot == "true" else False,
            note=0,
            promotion_id=1,
            seller_id=is_seller.id)

        db.session.add(new_product)
        db.session.commit()

        for item in categories_slug:
            category = Category.query.filter_by(slug=item).first()
            new_product_and_category = ProductAndCategory(
                product_id=new_product.id, category_id=category.id)
            db.session.add(new_product_and_category)
            db.session.commit()

        return jsonify({
            "status": True,
            "message": "Félicitation! Votre plat est ajouté"
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, vous n'êtes pas un vendeur."
        })


@user.route('/delete_product', methods=['POST'])
def delete_product():
    product_slug = request.form.get('product_slug')

    is_product = Product.query.filter_by(slug=product_slug).first()
    if is_product:

        # try to delete product image
        try:
            os.remove(os.path.join(product_directory, is_product.image))
        except:
            return jsonify({
                "status": False,
                "reason": "L'image du produit n'a pas pu être supprimée."
            })
        else:
            # all things are been make

            # delete ProductAndCategory lines concerned now
            productAndCategories = ProductAndCategory.query.filter_by(
                product_id=is_product.id).all()
            for item in productAndCategories:
                db.session.delete(item)
                db.session.commit()

            # delete product finally
            db.session.delete(is_product)
            db.session.commit()

            return jsonify({
                "status": True,
                "message": "Plat supprimé avec succès."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, ce produit rencontre un problème. Veuillez réessayer plus tard."
        })


@user.route('/update_product_availablity', methods=['POST'])
def update_product_availablity():
    product_slug = request.form.get('product_slug')
    value = request.form.get('value')

    product = Product.query.filter_by(slug=product_slug).first()
    if product:
        try:
            product.is_available = True if value == "true" else False
            db.session.commit()
            return jsonify({
                "status": True,
                "message": "Disponibilité du plat changé avec succès."
            })
        except Exception as e:
            return jsonify({
                "status": False,
                "reason": "Impossible de changer la disponibilité du produit. Erreur: " + str(e)
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Désolé, ce produit n'est pas reconnu. Veuillez réessayer plus tard."
        })


@user.route('/add_product_to_cart', methods=['POST'])
def add_product_to_cart():
    user_id = int(request.form.get('user_id'))
    product_slug = request.form.get('product_slug')
    quantity = int(request.form.get('number'))

    product = Product.query.filter_by(slug=product_slug).first()
    user = User.query.filter_by(id=user_id).first()
    if user:
        if product:
            anotherCartProduct = CartProduct.query.filter_by(
                user_id=user.id, product_id=product.id).first()
            if anotherCartProduct:
                # Produit déjà dans le panier, on procède à la modification de la quantité choisie cette fois-ci
                try:
                    anotherCartProduct.quantity = quantity
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status": False,
                        "reason": "Impossible de mettre à jour le produit dans votre panier. Erreur: " + str(e)
                    })
                else:
                    return jsonify({
                        "status": True,
                        "message": "Félicitation. Produit modifié dans votre panier."
                    })
            else:
                # Produit pas déjà dans le panier
                try:
                    new_cart_product = CartProduct(
                        name=product.name,
                        image=product.image,
                        primary_price=product.primary_price,
                        quantity=quantity,
                        product_id=product.id,
                        # promotion_id=product.promotion_id,
                        user_id=user.id
                    )
                    db.session.add(new_cart_product)
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status": False,
                        "reason": "Impossible d'ajouter au panier. Erreur: " + str(e)
                    })
                else:
                    return jsonify({
                        "status": True,
                        "message": "Félicitation. Produit ajouté au panier."
                    })
        else:
            return jsonify({
                "status": False,
                "reason": "Produit introuvable. Veuillez réessayer."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "L'utilisateur n'est pas trouvé. Veuillez réessayer."
        })


@user.route('/get_user_cart_products', methods=['POST'])
def get_user_cart_products():
    user_id = int(request.form.get('user_id'))

    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            userCartProducts = CartProduct.query.filter_by(
                user_id=user.id).all()
        except Exception as e:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue, contenu du panier non trouvé. Erreur: " + str(e)
            })
        else:
            finalCartProducts = []
            for cartProduct in userCartProducts:
                seller_name = cartProduct.product.seller.designation
                newCartProductInMap = {
                    "name": cartProduct.name,
                    "image": cartProduct.image,
                    "primary_price": cartProduct.primary_price,
                    "author": seller_name,
                    "quantity": cartProduct.quantity,
                    "product_id": cartProduct.product_id,
                    # "promotion_id": cartProduct.promotion_id,
                    "user_id": cartProduct.user_id
                }
                finalCartProducts.append(newCartProductInMap)
            return jsonify({
                "status": True,
                "cart_product": finalCartProducts
            })
    return jsonify({
        "status": False,
        "reason": "Utilisateur introuvable. Veuillez réessayer."
    })


@user.route('/update_cart_product_quantity', methods=['POST'])
def update_cart_product_quantity():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity'))

    cartProduct = CartProduct.query.filter_by(product_id=product_id).first()
    if cartProduct:
        try:
            cartProduct.quantity = quantity,
            db.session.commit()
            return jsonify({
                "status": True,
                "message": "Félicitation, quantité mise à jour."
            })
        except Exception as e:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue, produit du panier non trouvé. Erreur: " + str(e)
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Produit introuvable. "
        })


@user.route('/delete_cart_product', methods=['POST'])
def delete_cart_product():
    product_id = int(request.form.get('product_id'))

    cartProduct = CartProduct.query.filter_by(product_id=product_id).first()
    if cartProduct:
        try:
            db.session.delete(cartProduct)
            db.session.commit()
            return jsonify({
                "status": True,
                "message": "Félicitation, produit retiré du panier."
            })
        except Exception as e:
            return jsonify({
                "status": False,
                "reason": "Une erreur est survenue, le produit n'a pas pu être retiré du panier. Erreur: " + str(e)
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Produit introuvable. "
        })


@user.route('/get_notification_types', methods=['POST'])
def get_notification_types():
    notification_types:NotificationType = Notification.query.all()
    all_notification_types = []
    for type in notification_types:
        newNotificationTypeInMap = {
            "name": type.name,
            "icon": type.icon,
            "background_color": type.background_color,
        }
        all_notification_types.append(newNotificationTypeInMap)
    return jsonify({
        "status": True,
        "notification_types": all_notification_types
    })


@user.route('/get_user_notifications', methods=['POST'])
def get_user_notifications():
    user_id = request.form.get('user_id')
    if user_id:
        my_notifications: Notification = Notification.query.filter_by(
            user_id=int(user_id)).all()
        user_notifications = []
        for item in my_notifications:
            notification_details = {
                "notification_id": item.id,
                "message": item.message,
                "seen": True if item.seen == True else False,
                # "order_identifier": item.order_identifier,
                "type_id": item.type_id,
                "user_id": int(user_id)
            }
            user_notifications.append(notification_details)

        return jsonify({
            "status": True,
            "user_notifications": user_notifications
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_user_orders', methods=['POST'])
def get_user_orders():
    user_id = request.form.get('user_id')
    if user_id:
        user_orders: Order = Order.query.filter_by(user_id=int(user_id)).all()
        user_final_orders = []
        for item in user_orders:
            order_product = Product.query.filter_by(id=item.product_id).first()
            if order_product:
                product_seller = Seller.query.filter_by(id=order_product.seller_id).first()
                if product_seller:
                    order_payment_method = PaymentMethod.query.filter_by(id=item.payment_method_id).first()
                    if order_payment_method:
                        order_details = {
                            "order_id": item.id,
                            "quantity": item.quantity,
                            "product_final_price": item.product_final_price,
                            "status": item.status,
                            "slug": item.slug,
                            "user_address_lng": item.user_address_lng,
                            "user_address_lat": item.user_address_lat,
                            "product_name": order_product.name,
                            "seller_name": product_seller.designation,
                            "payment_method_name": order_payment_method.name
                        }
                        user_final_orders.append(order_details)

                    else:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, méthode de paiement non trouvée."
                        })
                else:
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, vendeur non trouvé."
                    })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, produit non trouvé."
                })
        return jsonify({
            "status": True,
            "user_orders": user_final_orders
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_an_order', methods=['POST'])
def get_an_order():
    order_id = request.form.get('order_id')
    if order_id:
        order: Order = Order.query.filter_by(id=int(order_id)).first()
        if order:
            order_product = Product.query.filter_by(id=order.product_id).first()
            if order_product:
                product_seller = Seller.query.filter_by(id=order_product.seller_id).first()
                if product_seller:
                    order_payment_method = PaymentMethod.query.filter_by(id=order.payment_method_id).first()
                    if order_payment_method:
                        order_details = {
                            "order_id": order.id,
                            "quantity": order.quantity,
                            "product_final_price": order.product_final_price,
                            "status": order.status,
                            "slug": order.slug,
                            "user_address_lng": order.user_address_lng,
                            "user_address_lat": order.user_address_lat,
                            "product_name": order_product.name,
                            "seller_name": product_seller.designation,
                            "payment_method_name": order_payment_method.name
                        }

                        return jsonify({
                            "status": True,
                            "order": order_details
                        })
                    else:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, méthode de paiement non trouvée."
                        })
                else:
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, vendeur non trouvé."
                    })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, produit non trouvé."
                })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, Commande non trouvée."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_seller_orders', methods=['POST'])
def get_seller_orders():
    user_id = request.form.get('user_id')
    if user_id:
        seller = Seller.query.filter_by(user_id=int(user_id)).first()
        if seller:
            seller_orders: Order = Order.query.filter_by(seller_id=int(seller.id)).all()
            seller_final_orders = []
            for item in seller_orders:
                order_product = Product.query.filter_by(id=item.product_id).first()
                if order_product:
                    product_seller = Seller.query.filter_by(
                        id=order_product.seller_id).first()
                    if product_seller:
                        order_payment_method = PaymentMethod.query.filter_by(
                            id=item.payment_method_id).first()
                        if order_payment_method:
                            order_details = {
                                "order_id": item.id,
                                "quantity": item.quantity,
                                "product_final_price": item.product_final_price,
                                "status": item.status,
                                "slug": item.slug,
                                "user_address_lng": item.user_address_lng,
                                "user_address_lat": item.user_address_lat,
                                "product_name": order_product.name,
                                "seller_name": product_seller.designation,
                                "payment_method_name": order_payment_method.name
                            }
                            seller_final_orders.append(order_details)

                            
                        else:
                            return jsonify({
                                "status": False,
                                "reason": "Désolé, méthode de paiement non trouvée."
                            })
                    else:
                        return jsonify({
                        "status": False,
                        "reason": "Désolé, vendeur non trouvé."
                    })
                else:
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, produit non trouvé."
                    })

            return jsonify({
                "status": True,
                "seller_orders": seller_final_orders
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, vendeur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/accept_delivery', methods=['POST'])
def accept_delivery():
    user_id = request.form.get('user_id')
    order_id = request.form.get('order_id')

    if order_id and user_id:
        
        delivery_man: DeliveryMan = DeliveryMan.query.filter_by(user_id=int(user_id)).first()
        if delivery_man:
            order: Order = Order.query.filter_by(id=int(order_id)).first()
            if order:
                all_add_delivery_man_to_order = AddedDeliveryMan.query.filter_by(order_id=order.id).all()
                for delivery_man_add in all_add_delivery_man_to_order:
                    db.session.delete(delivery_man_add)
                    db.session.commit()

                # calculate delivery fees
                seller: Seller = Seller.query.filter_by(id=order.seller_id).first()
                seller_address_lng = seller.address_lng
                seller_address_lat = seller.address_lat

                seller_point = (seller_address_lat, seller_address_lng)
                user_point = (order.user_address_lat, order.user_address_lng)

                distance_user_seller = distance.distance(user_point, seller_point).m
                delivery_fees = (distance_user_seller / 1000 ) / 100

                # crete slug for the delivery
                delivery_slug = "delivery-" + create_slug()
                new_delivery = Delivery(
                    amount=int(delivery_fees),
                    made_at="",
                    status=1,
                    slug=delivery_slug,
                    order_id=order.id,
                    delivery_man_id=delivery_man.id
                )
                db.session.add(new_delivery)
                db.session.commit()

                
                return jsonify({
                    "status": True,
                    "message": "Livraison acceptée avec succes."
                })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, commande non trouvée."
                })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, livreur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })



@user.route('/update_order_step', methods=['POST'])
def update_order_step():
    order_id = request.form.get('order_id')
    new_step = request.form.get('new_step')

    if order_id and new_step:
        order:Order = Order.query.filter_by(id=int(order_id)).first()
        if order:
            if order.status < int(new_step):
                order.status = int(new_step)
                db.session.commit()

                if int(new_step) in [1, 2, 3, 4, 5]:
                    user_message = create_notification_message(
                        order_identifier=order.slug,
                        for_user=True,
                        for_seller=False,
                        for_delivery_man=False,
                        step=int(new_step)
                    )
                    user_notification = Notification(
                        message=user_message,
                        seen=False,
                        order_identifier=order.slug,
                        type_id=1,
                        user_id=order.user_id
                    )
                    db.session.add(user_notification)
                    db.session.commit()

                    seller_message = create_notification_message(
                        order_identifier=order.slug,
                        for_user=False,
                        for_seller=True,
                        for_delivery_man=False,
                        step=int(new_step)
                    )

                    seller_notification = Notification(
                        message=seller_message,
                        seen=False,
                        order_identifier=order.slug,
                        type_id=1,
                        user_id=order.seller.user.id
                    )
                    db.session.add(seller_notification)
                    db.session.commit()

                if int(new_step) in [7, 8, 9, 10]:
                    delivery = Delivery.query.filter_by(order_id=order.id).first()
                    if delivery:
                        seller_message = create_notification_message(
                            order_identifier=order.slug,
                            for_user=False,
                            for_seller=True,
                            for_delivery_man=False,
                            step=int(new_step)
                        )

                        seller_notification = Notification(
                            message=seller_message,
                            seen=False,
                            order_identifier=order.slug,
                            type_id=1,
                            user_id=order.seller.user.id
                        )
                        db.session.add(seller_notification)
                        db.session.commit()

                        # delivery man notification
                        delivery_man_message = create_notification_message(
                            order_identifier=order.slug,
                            for_user=False,
                            for_seller=False,
                            for_delivery_man=True,
                            step=int(new_step)
                        )

                        delivery_man_notification = Notification(
                            message=delivery_man_message,
                            seen=False,
                            order_identifier=order.slug,
                            type_id=1,
                            user_id=delivery.delivery_man.user.id
                        )
                        db.session.add(delivery_man_notification)
                        db.session.commit()

                        if int(new_step) in [8, 9]:
                            # user notification
                            user_message = create_notification_message(
                                order_identifier=order.slug,
                                for_user=True,
                                for_seller=False,
                                for_delivery_man=False,
                                step=int(new_step)
                            )

                            user_notification = Notification(
                                message=user_message,
                                seen=False,
                                order_identifier=order.slug,
                                type_id=1,
                                user_id=order.user_id
                            )
                            db.session.add(user_notification)
                            db.session.commit()

                    else:
                        return jsonify({
                        "status": False,
                        "reason": "Désolé, livraison non trouvée."
                    })

                return jsonify({
                    "status": True,
                    "message": "Commande mise à jour avec succes."
                })
           
            else:
                return jsonify({
                "status": False,
                "reason": "Désolé, la nouvelle étape de la commande est inférieure à l'ancienne."
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, commande non trouvée."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })



@user.route('/get_delivery_man_deliveries', methods=['POST'])
def get_delivery_man_deliveries():
    user_id = request.form.get('user_id')
    if user_id:
        delivery_man = DeliveryMan.query.filter_by(user_id=int(user_id)).first()
        if delivery_man:
            delivery_man_missions: Delivery = Delivery.query.filter_by(
                delivery_man_id=int(delivery_man.id)).all()
            delivery_man_final_missions = []
            for item in delivery_man_missions:
                order = Order.query.filter_by(id=item.order_id).first()
                order_product = Product.query.filter_by(
                    id=order.product_id).first()
                if order_product:
                    product_seller = Seller.query.filter_by(
                        id=order_product.seller_id).first()
                    if product_seller:
                        order_payment_method = PaymentMethod.query.filter_by(
                            id=order.payment_method_id).first()
                        if order_payment_method:
                            order_details = {
                                "order_id": order.id,
                                "quantity": order.quantity,
                                "product_final_price": order.product_final_price,
                                "status": order.status,
                                "slug": order.slug,
                                "user_address_lng": order.user_address_lng,
                                "user_address_lat": order.user_address_lat,
                                "product_name": order_product.name,
                                "seller_name": product_seller.designation,
                                "payment_method_name": order_payment_method.name
                            }
                            delivery_man_final_missions.append(order_details)

                        else:
                            return jsonify({
                                "status": False,
                                "reason": "Désolé, méthode de paiement non trouvée."
                            })
                    else:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, vendeur non trouvé."
                        })
                else:
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, produit non trouvé."
                    })

            return jsonify({
                "status": True,
                "delivery_man_missions": delivery_man_final_missions
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, livreur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_delivery_man_additions', methods=['POST'])
def get_delivery_man_additions():
    user_id = request.form.get('user_id')
    if user_id:
        delivery_man = DeliveryMan.query.filter_by(
            user_id=int(user_id)).first()
        if delivery_man:
            delivery_man_additions:AddedDeliveryMan = AddedDeliveryMan.query.filter_by(
                delivery_man_id=int(delivery_man.id)).all()
            delivery_man_final_additions = []
            for item in delivery_man_additions:
                order = Order.query.filter_by(id=item.order_id).first()
                order_product = Product.query.filter_by(
                    id=order.product_id).first()
                if order_product:
                    product_seller = Seller.query.filter_by(
                        id=order_product.seller_id).first()
                    if product_seller:
                        order_payment_method = PaymentMethod.query.filter_by(
                            id=order.payment_method_id).first()
                        if order_payment_method:
                            order_details = {
                                "order_id": order.id,
                                "quantity": order.quantity,
                                "product_final_price": order.product_final_price,
                                "status": order.status,
                                "slug": order.slug,
                                "user_address_lng": order.user_address_lng,
                                "user_address_lat": order.user_address_lat,
                                "product_name": order_product.name,
                                "seller_name": product_seller.designation,
                                "payment_method_name": order_payment_method.name
                            }
                            delivery_man_final_additions.append(order_details)

                        else:
                            return jsonify({
                                "status": False,
                                "reason": "Désolé, méthode de paiement non trouvée."
                            })
                    else:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, vendeur non trouvé."
                        })
                else:
                    return jsonify({
                        "status": False,
                        "reason": "Désolé, produit non trouvé."
                    })

            return jsonify({
                "status": True,
                "delivery_man_additions": delivery_man_final_additions
            })
        else:
            return jsonify({
                "status": False,
                "reason": "Désolé, livreur non trouvé."
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/get_delivery_men_for_order', methods=['POST'])
def get_delivery_men_for_order():
    order_id = request.form.get('order_id')
    if order_id:
        getting = get_order_delivery_men(order_id)
        if getting["status"] == True:
            return jsonify({
                "status": True,
                "delivery_men": getting["delivery_men"]
            })
        else:
            return jsonify({
                "status": False,
                "reason": getting["reason"]
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


@user.route('/add_delivery_men_to_order', methods=['POST'])
def add_delivery_men_to_order():
    order_id = request.form.get('order_id')
    if order_id:
        getting = get_order_delivery_men(order_id)
        if getting["status"] == True:
            for man in getting["delivery_men"]:
                new_add = AddedDeliveryMan(
                    order_id=int(order_id),
                    delivery_man_id=man["delivery_man_id"]
                )
                db.session.add(new_add)
                db.session.commit()

                message = create_notification_message(
                    order_identifier="",
                    for_seller=False,
                    for_user=False,
                    for_delivery_man=True,
                    step=6
                )
                delivery_man:DeliveryMan = DeliveryMan.query.filter_by(id=man["delivery_man_id"]).first()
                new_notification = Notification(message=message,seen=False,order_identifier="",type_id=1,user_id=delivery_man.user_id)
                db.session.add(new_notification)
                db.session.commit()
            return jsonify({
                "status": True,
                "message": "Génial! Les livreurs seront informés de cette livraison et l'accepteront si possible." 
            })
        else:
            return jsonify({
                "status": False,
                "reason": getting["reason"]
            })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs."
        })


# @user.route('/update_order_step', methods=['POST'])
# def update_order_step():
#     order_id = request.form.get('order_id')
#     new_step = request.form.get('new_step')

#     if order_id and new_step:
#         order:Order = Order.query.filter_by(id=int(order_id)).first()
#         if order:
#             if order.status < int(new_step):
#                 order.status = int(new_step)
#                 db.session.commit()

#                 if int(new_step) in [1, 2, 3, 4, 5]:
#                     user_message = create_notification_message(
#                         order_identifier=order.slug,
#                         for_user=True,
#                         for_seller=False,
#                         for_delivery_man=False,
#                         step=int(new_step)
#                     )
#                     user_notification = Notification(
#                         message=user_message,
#                         seen=False,
#                         order_identifier=order.slug,
#                         type_id=1,
#                         user_id=order.user_id
#                     )
#                     db.session.add(user_notification)
#                     db.session.commit()

#                     seller_message = create_notification_message(
#                         order_identifier=order.slug,
#                         for_user=False,
#                         for_seller=True,
#                         for_delivery_man=False,
#                         step=int(new_step)
#                     )

#                     seller_notification = Notification(
#                         message=seller_message,
#                         seen=False,
#                         order_identifier=order.slug,
#                         type_id=1,
#                         user_id=order.seller_id
#                     )
#                     db.session.add(seller_notification)
#                     db.session.commit()


                
#                 return jsonify({
#                     "status": True,
#                     "message": "Commande mise à jour avec succes."
#                 })
#             else:
#                 return jsonify({
#                 "status": False,
#                 "reason": "Désolé, la nouvelle étape de la commande est inférieure à l'ancienne."
#             })
#         else:
#             return jsonify({
#                 "status": False,
#                 "reason": "Désolé, commande non trouvée."
#             })
#     else:
#         return jsonify({
#             "status": False,
#             "reason": "Veuillez remplir tous les champs"
#         })

@user.route('/create_order', methods=['POST'])
def create_order():
    quantity = request.form.get('quantity')
    product_final_price = request.form.get('product_final_price')
    payment_method_id = request.form.get('payment_method_id')

    user_address_lng = request.form.get('user_address_lng')
    user_address_lat = request.form.get('user_address_lat')

    product_id = request.form.get('product_id')
    user_id = request.form.get('user_id')

    if quantity and product_final_price and product_id and user_id:
        user = User.query.filter_by(id=int(user_id)).first()
        if user:
            concerned_product = Product.query.filter_by(id=int(product_id)).first()
            if concerned_product:
                payment_method = PaymentMethod.query.filter_by(id=int(payment_method_id)).first()
                if payment_method:
                    order_slug = create_slug()
                    new_order = Order(
                        quantity=int(quantity),
                        product_final_price=float(product_final_price),
                        status=0,
                        slug= "order-" + order_slug,
                        user_address_lng=float(user_address_lng),
                        user_address_lat=float(user_address_lat),
                        seller_id=concerned_product.seller_id,
                        product_id=concerned_product.id,
                        payment_method_id=payment_method.id,
                        user_id=user.id
                    )
                    db.session.add(new_order)
                    db.session.commit()

                    product_seller = Seller.query.filter_by(id=concerned_product.seller_id).first()

                    # create new notification for product seller and client
                    notification_message = create_notification_message(
                        order_identifier=new_order.slug,
                        for_user=True,
                        for_seller=False,
                        for_delivery_man=False,
                        step=0
                    )
                    new_client_notification = Notification(
                        notification_message,
                        False,
                        order_identifier=new_order.slug,
                        type_id=1,
                        user_id=user.id
                    )
                    db.session.add(new_client_notification)
                    db.session.commit()

                    seller_notification_message = create_notification_message(
                        order_identifier=new_order.slug,
                        for_user=False,
                        for_seller=True,
                        for_delivery_man=False,
                        step=0
                    )
                    new_seller_notification = Notification(
                        seller_notification_message,
                        False,
                        order_identifier=new_order.slug,
                        type_id=1,
                        user_id=product_seller.id
                    )
                    db.session.add(new_seller_notification)
                    db.session.commit()

                    # delete associated cart product
                    associated_cart_product = CartProduct.query.filter_by(product_id=concerned_product.id).first()
                    if associated_cart_product:
                        db.session.delete(associated_cart_product)
                        db.session.commit()
                    
                        return jsonify({
                            "status": True,
                            "message": "Félicitation, commande envoyée. Vous serez notifié(e) de la réponse du vendeur."
                        })
                    else:
                        return jsonify({
                            "status": False,
                            "reason": "Désolé, produit du panier non trouvé."
                        })
                else:
                    return jsonify({
                    "status": False,
                    "reason": "Désolé, méthode de paiement non trouvée."
                })
            else:
                return jsonify({
                    "status": False,
                    "reason": "Désolé, produit non trouvé."
                })
        else:
            return jsonify({
            "status": False,
            "reason": "Désolé, utilisateur non trouvé."
        })
    else:
        return jsonify({
            "status": False,
            "reason": "Veuillez remplir tous les champs"
        })
    # cartProduct = CartProduct.query.filter_by(product_id=product_id).first()
    # if cartProduct:
    #     try:
    #         db.session.delete(cartProduct)
    #         db.session.commit()
    #         return jsonify({
    #             "status": True,
    #             "message": "Félicitation, produit retiré du panier."
    #         })
    #     except Exception as e:
    #         return jsonify({
    #             "status": False,
    #             "reason": "Une erreur est survenue, le produit n'a pas pu être retiré du panier. Erreur: " + str(e)
    #         })
    # else:
    #     return jsonify({
    #         "status": False,
    #         "reason": "Produit introuvable. "
    #     })

# # TODO
# @user.route('/updateproduct', methods=['POST'])
# def updateproduct():
#     user_id = int(request.form.get('user_id'))
#     product_id = int(request.form.get('user_id'))

#     name = request.form.get('name')
#     image = request.form.get('image')
#     primary_price = float(request.form.get('primary_price'))
#     description = request.form.get('description')
#     available = request.form.get('available')
#     hot = bool(request.form.get('hot'))
#     note = request.form.get('note')

#     is_seller = User.query.filter_by(id=user_id, is_seller=1).first()
#     is_product = Product.query.filter_by(id=product_id, user_id=user_id).first()
#     if is_seller:
#         if is_product:
#             db.session.delete(is_product)
#             db.session.commit()

#             return jsonify({
#                 "status": True,
#                 "message": "Plat supprimé avec succès."
#             })
#         else:
#             return jsonify({
#                 "status": False,
#                 "reason": "Désolé, ce produit rencontre un problème. Veuillez réessayer plus tard."
#             })
#     else:
#         return jsonify({
#             "status": False,
#             "reason": "Désolé, vous n'êtes pas un vendeur."
#         })
