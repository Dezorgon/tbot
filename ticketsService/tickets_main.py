import traceback
from flask import request, jsonify
from ticketsService import app, db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from ticketsService import tickets_db
from ticketsService import concert_db
from ticketsService import sold_tickets_db
from datetime import datetime


@app.route("/concerts", methods=["POST"])
def create_concert():
    name = request.json['name']
    date = datetime.strptime(request.json['date'], '%Y-%m-%d %H:%M:%S.%f')
    city = request.json['city']
    place = request.json['place']
    # tickets = renquest.json['tickets']
    description = None
    if 'description' in request.json:
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
    response['concert'] = response['concert'].to_json()
    return jsonify(response)


@app.route('/concerts/top/<int:count>', methods=['GET'])
def get_top_concerts(count):
    response = concert_db.read_top_concerts(count)

    if response['ok']:
        for i in range(len(response['concerts'])):
            response['concerts'][i] = response['concerts'][i].to_json()
    return jsonify(response)


@app.route('/concerts/<city>', methods=['GET'])
def get_concerts_by_city(city):
    response = concert_db.read_concerts_by_city(city)

    if response['ok']:
        for i in range(len(response['concerts'])):
            response['concerts'][i] = response['concerts'][i].to_json()
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


@app.route('/tickets/<int:tickets_id>', methods=['PUT'])
def update_tickets(tickets_id):
    raise NotImplemented


@app.route('/tickets/<int:tickets_id>', methods=['DELETE'])
def delete_tickets(tickets_id):
    response = tickets_db.delete_tickets(tickets_id)
    return jsonify(response)


@app.route('/tickets/<int:tickets_id>', methods=['GET'])
def get_tickets(tickets_id):
    response = tickets_db.read_concert_tickets(tickets_id)
    if response['ok']:
        response['tickets'] = response['tickets'].to_json()
    return jsonify(response)


@app.route('/concerts/<int:concert_id>/tickets', methods=['GET'])
def get_concert_tickets(concert_id):
    response = tickets_db.read_all_concert_tickets_by_concert_id(concert_id)
    if response['ok']:
        for i in range(len(response['all_tickets'])):
            response['all_tickets'][i] = response['all_tickets'][i].to_json()
    return jsonify(response)


@app.route("/concerts/<int:concert_id>/buy", methods=["POST"])
def buy_ticket(concert_id):
    response = sold_tickets_db.filter_sold_tickets(
        concert_id, request.json['user_id'], type_name=request.json['type'])

    if response['ok']:
        t = response['all_sold_tickets'][0]
        sold_tickets_db.update_sold_tickets(t.id, count=t.count + 1)
        return jsonify({'ok': True})
    else:
        sold_tickets_db.create_sold_tickets(1, request.json['concert_id'], current_user.id, request.json['type_id'])

    return jsonify({'ok': False})


if __name__ == '__main__':
    app.run(debug=True, port=80)
