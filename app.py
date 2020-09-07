from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'#slite database lives after the root folder of the project.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

#tell sqlalchemy to create a table, use flask-decorator.
@app.before_first_request
def create_table():#before the first request run, it wil run this, which creates this file db.create_all, unless they exist aleady.
    db.create_all()

jwt = JWT(app, authenticate, identity) #authenticate

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    #circular import.  our item models are going to import db as well.  if we import db at the top and models at the top,
    #this will create a circular import
    db.init_app(app)
    app.run(port = 5000, debug = True)
