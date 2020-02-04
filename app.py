import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Contact

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG']= True
app.config['ENV']= 'development'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+ os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contacts", methods=['GET', 'POST'])
@app.route("/contacts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def contacts(id=None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(Contact.serialize()), 200
            else:
                return jsonify({"msg":"Contact not found"}), 404
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200

    if request.method == 'POST':
        name = request.json.get('name', None)
        phone = request.json.get('phone', None)

        if not name:
            return jsonify({"msg":"name is required"}), 422

        if not phone:
            return jsonify({"msg":"phone is required"}), 422

        contact = Contact()
        contact.name = name
        contact.phone = phone

        db.session.add(contact)
        db.session.commit()

        return jsonify(contact.serialize()), 201


    if request.method == 'PUT':
        name = request.json.get('name', None)
        phone = request.json.get('phone', None)

        if not name:
            return jsonify({"msg":"name is required"}), 422

        if not phone:
            return jsonify({"msg":"phone is required"}), 422

        contact = Contact.query.get(id)

        if not contact:
                return jsonify({"msg":"Contact not found"}), 404

        contact.name = name
        contact.phone = phone

        db.session.commit()

        return jsonify(contact.serialize()), 200

    if request.method == 'DELETE':

        contact = Contact.query.get(id)

        if not contact:
                return jsonify({"msg":"Contact not found"}), 404

        db.session.delete(contact)
        db.session.commit()

        return jsonify({"msg":"Contact deleted"}), 200


if __name__=="__main__":
    manager.run()