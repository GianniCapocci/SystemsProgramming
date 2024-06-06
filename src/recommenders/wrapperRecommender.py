def generalRecommender(user_id: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return {"error": "User not found"}

    cursor.execute("SELECT * FROM coupons WHERE user_id = %s", (user_id,))
    coupons = cursor.fetchall()

    cursor.close()
    conn.close()

    if coupons:
        return frequencyRecommender(user_id)
    else:
        return randomRecommender(Event)


@app.route('/generate_recommendation', methods=['GET'])
def generate_recommendation():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        recommendation = generalRecommender(user_id)
        return jsonify(recommendation), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
