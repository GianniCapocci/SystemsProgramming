import json
import os

from confluent_kafka import Producer as KafkaProducer
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sqlalchemy.orm import scoped_session, sessionmaker

from src.database.database import db
from src.kafka.admin import create_kafka_topics
from src.recommenders import wrapperRecommender as recommender
from src.schemas import user_schema, event_schema, coupon_schema

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    Session = scoped_session(sessionmaker(bind=db.engine))

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
topics = ['user_topic', 'event_topic', 'coupon_topic']

create_kafka_topics(bootstrap_servers, topics)

producer_config = {
    'bootstrap.servers': bootstrap_servers
}

producer = KafkaProducer(producer_config)


@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        print("inside register_user")
        user = request.json
        validate(instance=user, schema=user_schema)
        serialized_user = json.dumps(user).encode('utf-8')
        producer.produce('user_topic', value=serialized_user)
        return jsonify(user), 200
    except ValidationError as e:
        error_message = {'error': e.message}
        return jsonify(error_message), 400


@app.route('/register_coupon', methods=['POST'])
def register_coupon():
    try:
        coupon = request.json
        validate(instance=coupon, schema=coupon_schema)
        serialized_coupon = json.dumps(coupon).encode('utf-8')
        producer.produce('coupon_topic', value=serialized_coupon)
        return jsonify(coupon), 200
    except ValidationError as e:
        error_message = {'error': e.message}
        return jsonify(error_message), 400


@app.route('/register_event', methods=['POST'])
def register_event():
    try:
        event = request.json
        validate(instance=event, schema=event_schema)
        serialized_event = json.dumps(event).encode('utf-8')
        producer.produce('event_topic', value=serialized_event)
        return jsonify(event), 200
    except ValidationError as e:
        error_message = {'error': e.message}
        return jsonify(error_message), 400


# If n == 0 it means the user wants all the available similar events recommended
# If n > 0 it means the user wants n similar events recommended
# If n == -1 it means the user wants a random recommendation
@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = str(request.args.get('user_id'))
        n = int(request.args.get('n', -1))
    except ValueError as e:
        return jsonify({'error': 'Invalid parameter type. user_id and n must be integers.'}, {str(e)}), 400
    if user_id:
        try:
            result = recommender(user_id, n, Session)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': f'{str(e)}'}), 400
    else:
        return jsonify({"error": "User ID is required"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
