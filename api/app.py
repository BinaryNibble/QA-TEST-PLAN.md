from flask import Flask, jsonify, request

from services import get_account, get_balance, create_transfer
from database import initialize_database, seed_database

app = Flask(__name__)


@app.route("/api/accounts/<username>", methods=["GET"])
def account(username):
    user = get_account(username)

    if user is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(user)


@app.route("/api/accounts/<username>/balance", methods=["GET"])
def balance(username):
    result = get_balance(username)

    if result is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(result)


@app.route("/api/transfers", methods=["POST"])
def transfer():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    from_user = data.get("from")
    to_user = data.get("to")
    amount = data.get("amount")

    if not from_user or not to_user or amount is None:
        return jsonify({"error": "Missing required fields"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    transaction, error, status_code = create_transfer(
        from_user,
        to_user,
        amount
    )

    if error:
        return jsonify({"error": error}), status_code

    return jsonify(transaction), status_code


if __name__ == "__main__":
    initialize_database()
    seed_database()
    app.run(debug=True)