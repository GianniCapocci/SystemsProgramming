from flask import Flask, request, jsonify
from pydantic import ValidationError
from schemas import User, Coupon, Event
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from database import db_config
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import KafkaAdmin
from src.database import db_util
from src.recommenders import wrapperRecommender as recommender

app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = db_config.user
app.config['MYSQL_DATABASE_PASSWORD'] = db_config.password
app.config['MYSQL_DATABASE_DB'] = db_config.dbname
app.config['MYSQL_DATABASE_HOST'] = db_config.host
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

consumer_users = KafkaConsumer('users')
consumer_events = KafkaConsumer('events')
consumer_coupons = KafkaConsumer('coupons')

consumer_users.start()
consumer_events.start()
consumer_coupons.start()

producer = KafkaProducer()

admin = KafkaAdmin()


@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        user = User(**request.json)
        db_util.db_register_user(user, conn, cursor)
        return jsonify(user.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


@app.route('/register_coupon', methods=['POST'])
def register_coupon():
    try:
        coupon = Coupon(**request.json)
        db_util.db_register_coupon(coupon, conn, cursor)
        return jsonify(coupon.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


@app.route('/register_event', methods=['POST'])
def register_event():
    try:
        event = Event(**request.json)
        db_util.db_register_event(event, conn, cursor)
        return jsonify(event.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    n = request.args.get('n')
    if user_id:
        try:
            return recommender.wrapperRecommender(user_id, n, cursor)
        except ValidationError as e:
            print(e)
            return jsonify(e.errors()), 400
    else:
        return jsonify({"error": "User ID is required"}), 400


@app.route('/users', methods=['GET'])
def get_messages_users():
    return jsonify(consumer_users.get_messages())


@app.route('/events', methods=['GET'])
def get_messages_events():
    return jsonify(consumer_events.get_messages())


@app.route('/coupons', methods=['GET'])
def get_messages_coupons():
    return jsonify(consumer_coupons.get_messages())


@app.route('/produce', methods=['POST'])
def produce_message():
    topic = request.json.get('topic')
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    producer.produce_message(topic, message)
    print(message)
    return jsonify({'status': 'Message produced'}), 200


@app.route('/create_topic', methods=['POST'])
def create_topic():
    topic_name = request.json.get('topic_name')
    if not topic_name:
        return jsonify({'error': 'Topic name is required'}), 400
    try:
        admin.create_topic(topic_name)
        return jsonify({'status': f'Topic {topic_name} created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    producer.send('users', b'Hello, Kafka!')
    return 'Message sent to Kafka!'


if __name__ == "__main__":
    app.run(debug=True)
