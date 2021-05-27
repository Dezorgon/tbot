import traceback
from flask import request, jsonify
from flask_admin.contrib.sqla import ModelView
from ticketsService import app, db
from ticketsService import tickets_db
from ticketsService import concert_db
from ticketsService import sold_tickets_db
from datetime import datetime
from ticketsService.tickets_models import Concert, Tickets, Sold, Type

from flask_admin import Admin
from flask_admin.contrib import sqla as flask_admin_sqla
from flask_admin import AdminIndexView
from flask_admin import expose
from flask import Flask, flash, redirect, render_template, request, session, abort


class DefaultModelView(flask_admin_sqla.ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        return session.get('logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")

    @expose('/')
    def index(self):
        if not self.is_accessible():
            return redirect("/")
        return super(MyAdminIndexView, self).index()


admin = Admin(
        app,
        name='My App',
        template_mode='bootstrap4',
        index_view=MyAdminIndexView()
    )

admin.add_view(ModelView(Concert, db.session))
admin.add_view(ModelView(Tickets, db.session))
admin.add_view(ModelView(Sold, db.session))
admin.add_view(ModelView(Type, db.session))


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/admin')


@app.route('/admin_login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        pass
        # flash('wrong password!')
    return redirect('/')


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify('ticketsService')


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
        response['ticket'] = response['ticket'].to_json()
        response['ticket']['left'] = response['left']
        del response['left']
    return jsonify(response)


@app.route('/concerts/<int:concert_id>/tickets', methods=['GET'])
def get_concert_tickets(concert_id):
    response = tickets_db.read_all_concert_tickets_by_concert_id(concert_id)
    if response['ok']:
        for i in range(len(response['tickets'])):
            response['tickets'][i]['ticket'] = response['tickets'][i]['ticket'].to_json()
            response['tickets'][i]['ticket']['left'] = response['tickets'][i]['left']
            del response['tickets'][i]['left']
            response['tickets'][i] = response['tickets'][i]['ticket']
    return jsonify(response)


@app.route('/sold_tickets/<int:user_id>', methods=['GET'])
def get_user_sold_tickets(user_id):
    response = sold_tickets_db.filter_sold_tickets(user_id=user_id)
    if response['ok']:
        for i in range(len(response['sold_tickets'])):
            response['sold_tickets'][i] = response['sold_tickets'][i].to_json()
            response['sold_tickets'][i]['concert'] =\
                concert_db.read_concert(response['sold_tickets'][i]['concert_id'])['concert'].name
            del response['sold_tickets'][i]['user_id']
    return jsonify(response)


@app.route("/concerts/<int:concert_id>/buy", methods=["POST"])
def buy_ticket(concert_id):
    response = sold_tickets_db.filter_sold_tickets(user_id=request.json['user_id'])

    ticket = None
    if response['ok']:
        for t in response['sold_tickets']:
            if t.concert_id == concert_id and t.type.type == request.json['type']:
                ticket = t

    if ticket:
        response = sold_tickets_db.update_sold_tickets(ticket.id, count=ticket.count + 1)
    else:
        response = sold_tickets_db.create_sold_tickets(1, concert_id, request.json['user_id'],
                                                       tickets_type_name=request.json['type'])
    return jsonify({'ok': response['ok']})
