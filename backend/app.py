# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import SessionLocal, engine
from models import Product, Order
import logging

app = Flask(__name__)
CORS(app, origins=["https://www.myfrontenddomain.com", "https://my-frontend-cloudfront.cloudfront.net"])  # set your front-end origin(s)

logging.basicConfig(level=logging.INFO)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/products", methods=["GET"])
def list_products():
    session = SessionLocal()
    try:
        products = session.query(Product).all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])
    finally:
        session.close()

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    product_id = data.get("product_id")
    qty = int(data.get("qty", 1))
    session = SessionLocal()
    try:
        # basic validation
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            return jsonify({"error": "product not found"}), 404

        order = Order(product_id=product_id, qty=qty)
        session.add(order)
        session.commit()
        return jsonify({"order_id": order.id}), 201
    except Exception as e:
        session.rollback()
        app.logger.exception("Failed to create order")
        return jsonify({"error": "internal"}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
