from datetime import datetime
import random
import string
import uuid
from geopy import distance
from flask import Blueprint, jsonify, request

from sqlalchemy import lateral
from project import db
from project.models import *
from project.models.address import Address
from project.models.balance import Balance
from project.models.product import Product


def create_balance_for_user(user_id):
    
    new_balance = Balance(
        amount=0,
        updated_at=datetime.now().strftime("%d/%m/%Y %H:%M"), 
        user_id=user_id,
        )
    db.session.add(new_balance)
    db.session.commit()     # create balance by platform money and by wallet

    return {
            "success": True
        }

def create_user_first_address(user_id, name, description, lat, lng):
    
    first_address = Address(
        name=name,
        description=description,
        lat=lat,
        lng=lng,
        is_primary=True,
        user_id=user_id,
        )
    db.session.add(first_address)
    db.session.commit()     # create balance by platform money and by wallet

    return {
            "success": True
        }

def create_slug():
    new_slug = uuid.uuid4()
    return new_slug.hex

def list_in_string_sharp_to_list( list_in_string_sharp):
    list_in_list_sharp = list_in_string_sharp.strip('][').split(', ')
    return list_in_list_sharp

def create_notification_message(order_identifier, for_seller, for_user, for_delivery_man, step):
    
    final_order_identifier = order_identifier[:20] + order_identifier[len(order_identifier):]
    if for_seller == True:
        if step == 0:
            message = "Vous avez reçu une nouvelle commande. Veuillez accepter ou rejetter."
        elif step == 1:
            message = "Vous avez accepté la commande [" + final_order_identifier + "...]."
        elif step == 2:
            message = "Vous avez rejeté la commande [" + final_order_identifier + "...]."
        elif step == 3:
            message = "La commande [" + final_order_identifier + "...] vient d'être payée. Veuillez procéder à sa préparation."
        elif step == 4:
            message = "Vous avez entamé la préparation de la commande [" + final_order_identifier + "...]."
        elif step == 5:
            message = "La commande [" + final_order_identifier + "...] est prête."
        elif step == 6:
            message = "Vous avez lancé l'ajout d'un livreur à la commande [" + final_order_identifier + "...]."
        elif step == 7:
            message = "La livraison de votre commande reçue [" + final_order_identifier + "...] est acceptée par un livreur."
        elif step == 8:
            message = "La livraison de votre commande reçue [" + final_order_identifier + "...] est entamée par le livreur."
        elif step == 9:
            message = "Félicitaion!! Votre commande reçue [" + final_order_identifier + "...] vient d'être livrée au client."
        elif step == 10:
            message = "Félicitaion!! La réception de la commande [" + final_order_identifier + "...] que vous avez reçue est confirmée par le client."

    elif for_user == True:
        if step == 0:
            message = "Votre commande [" + final_order_identifier + "...] est enregistrée. Acceptation par le vendeur en cours."
        elif step == 1:
            message = "Votre commande [" + final_order_identifier + "...] est acceptée. Veuillez procéder au paiement."
        elif step == 2:
            message = "Votre commande [" + final_order_identifier + "...] est rejetée. Le plat n'est surement pas disponible"
        elif step == 3:
            message = "Votre commande [" + final_order_identifier + "...] est payée."
        elif step == 4:
            message = "Votre commande [" + final_order_identifier + "...] est en cours de préparation."
        elif step == 5:
            message = "Votre commande [" + final_order_identifier + "...] est prête."
        elif step == 7:
            message = "La livraison de votre commande [" + final_order_identifier + "...] est acceptée par un livreur."
        elif step == 8:
            message = "La livraison de votre commande [" + final_order_identifier + "...] est entamée par le livreur."
        elif step == 9:
            message = "Félicitaion!! Votre commande [" + final_order_identifier + "...] est livrée."
        elif step == 10:
            message = "Félicitaion!! Vous venez de confirmer la réception de la commande [" + final_order_identifier + "...]"


    elif for_delivery_man == True:
        if step == 6:
            message = "Une livraison vous est proposée. Vous l'acceptez?"
        elif step == 7:
            message = "Vous avez accepté livrer la commande [" + final_order_identifier + "...]."
        elif step == 8:
            message = "Livraison entamée pour la commande [" + final_order_identifier + "...]. Allez, bonne course."
        elif step == 9:
            message = "Livraison effectuée pour la commande [" + final_order_identifier + "...]. Belle course."
        elif step == 10:
            message = "La réception de la commande [" + final_order_identifier + "...] vient d'être confirmée."

    return message


def get_order_delivery_men(order_id):
    order: Order = Order.query.filter_by(id=int(order_id)).first()
    final_delivery_men = []
    if order:
        seller: Seller = Seller.query.filter_by(id=order.seller_id).first()
        seller_address_lng = seller.address_lng
        seller_address_lat = seller.address_lat

        seller_point = (seller_address_lat, seller_address_lng)
        user_point = (order.user_address_lat, order.user_address_lng)
        all_delivery_zones = DeliveryZone.query.all()
        for zone in all_delivery_zones:
            zone_lat = zone.lat
            zone_lng = zone.lng
            zone_point = (zone_lat, zone_lng)

            distance_user = distance.distance(user_point, zone_point).m
            distance_seller = distance.distance(seller_point, zone_point).m

            if distance_user <= zone.radius and distance_seller <= zone.radius:
                selected_delivery_man: DeliveryMan = DeliveryMan.query.filter_by(
                    id=zone.delivery_man_id).first()
                if selected_delivery_man:
                    user_delivery_man: User = User.query.filter_by(
                        id=selected_delivery_man.user_id).first()
                    delivery_man_details = {
                        "delivery_man_id": selected_delivery_man.id,
                        "name": user_delivery_man.firstname + " " + user_delivery_man.lastname,
                        "celphone": user_delivery_man.celphone,
                        "note": 4.3,
                    }
                    final_delivery_men.append(delivery_man_details)

                else:
                    return {
                        "status": False,
                        "reason": "Désolé, livreur non trouvé."
                    }

        return {
            "status": True,
            "delivery_men": final_delivery_men
        }
    else:
        return {
            "status": False,
            "reason": "Désolé, commande non trouvée."
        }



def get_admin_dashbord_utils():
    become_seller_request_global_list = []
    become_delivery_man_request_global_list = []
    become_seller_requests = Seller.query.filter_by(status=1).all()
    become_delivery_man_requests = DeliveryMan.query.filter_by(status=1).all()
       
    for item in become_seller_requests:
        request_user = User.query.filter_by(id=item.user_id).first()
        user_card = Card.query.filter_by(user_id=request_user.id).first()
        become_seller_request_global_list.append(
            {
                "user": request_user,
                "user_card": user_card,
                "request": item
            }
        )
    
    for request in become_delivery_man_requests:
        request_user = User.query.filter_by(id=request.user_id).first()
        user_card = Card.query.filter_by(user_id=request_user.id).first()

        delivery_tools_types = []
        tool_and_delivery_man:DeliveryToolAndDeliveryMan = DeliveryToolAndDeliveryMan.query.filter_by(delivery_man_id=request.id).all()
        for tool_and in tool_and_delivery_man:
            tool_type = DeliveryToolType.query.filter_by(id=tool_and.delivery_tool_type_id).first()
            delivery_tools_types.append(tool_type)

        become_delivery_man_request_global_list.append(
            {
                "user": request_user,
                "user_card": user_card,
                "request": request,
                "delivery_tools": delivery_tools_types
            }
        )

    return {
        "become_seller_request_global_list": become_seller_request_global_list,
        "become_delivery_man_request_global_list": become_delivery_man_request_global_list
    }