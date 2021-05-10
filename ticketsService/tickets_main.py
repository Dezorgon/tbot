import traceback
from flask import request, jsonify
from ticketsService import app, db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import concert_db
import tickets_db
import sold_tickets_db


@app.route("/concerts", methods=["POST"])
def create_concert():
    name = request.json['name']
    date = request.json['date']
    city = request.json['city']
    place = request.json['place']
    # tickets = request.json['tickets']
    description = request.json['description']

    response = concert_db.create_concert(name=name, date=date, city=city, place=place, description=description)

    if response['ok']:
        # concert = response['concert']

        # for t in tickets:
        #     new_tickets = tickets_db.create_tickets(t['count'], t['price'], concert.id, tickets_type_name=t['type'])
        #     concert.tickets.append(new_tickets)

        response['concert'] = response['concert'].to_json()
        response = dict(**response, **{'message': 'signup'})

    return jsonify(response)


@app.route("/concerts/<int:concert_id>/tickets", methods=["POST"])
def create_tickets(concert_id):
    count = request.json['count']
    price = request.json['price']
    tickets_type = request.json['type']

    response = tickets_db.create_tickets(count, price, concert_id, tickets_type_name=tickets_type)

    if response['ok']:
        # tickets = response['tickets']
        #
        # new_tickets = tickets_db.create_tickets(tickets['count'], tickets['price'], concert_id, tickets_type_name=t['type'])
        # # concert.tickets.append(new_tickets)

        response['tickets'] = response['tickets'].to_json()

    return jsonify(response)


@app.route('/concerts/<int:concert_id>', methods=['PUT'])
def update_concert(concert_id):
    raise NotImplemented


@app.route('/concerts/<int:concert_id>', methods=['DELETE'])
def delete_concert(concert_id):
    response = concert_db.delete_concert(concert_id)
    return jsonify(response)


@app.route('/concerts/<int:concert_id>', methods=['GET'])
def get_concert(concert_id):
    response = concert_db.read_concert(concert_id)
    return jsonify(response)


@app.route('/concerts/<str:city>', methods=['GET'])
def get_concerts_by_city(city):
    response = concert_db.read_concerts_by_city(city)
    return jsonify(response)


@app.route('/buy', methods=['GET'])
def buy_ticket():
    response = sold_tickets_db.filter_sold_tickets(
        request.json['concert_id'], current_user.id, request.json['type_id'])

    if response['ok']:
        t = response['all_sold_tickets'][0]
        sold_tickets_db.update_sold_tickets(t.id, count=t.count+1)
        return jsonify({'ok': True})
    else:
        sold_tickets_db.create_sold_tickets(1, request.json['concert_id'], current_user.id, request.json['type_id'])

    return jsonify({'ok': False})




