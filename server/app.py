#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# ✅ GET /bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(all_bakeries, 200)

# ✅ GET /bakeries/<int:id>
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return make_response(bakery.to_dict(), 200)
    return make_response({"error": "Bakery not found"}, 404)

# ✅ GET /baked_goods/by_price
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    return make_response(baked_goods_list, 200)

# ✅ GET /baked_goods/most_expensive
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return make_response(baked_good.to_dict(), 200)
    return make_response({"error": "No baked goods found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
