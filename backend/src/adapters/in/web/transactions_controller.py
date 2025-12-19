from flask import Blueprint, request, current_app, jsonify
import tempfile
import os

api_bp = Blueprint("api", __name__)

def get_use_case(name):
    return current_app.config["USE_CASES"][name]

@api_bp.route("/transactions/upload", methods=["POST"])
def upload_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Save File
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"upload_{file.filename}")
        file.save(temp_path)

        # Ingest Transaction
        ingest_uc = get_use_case("ingest_transaction_use_case")
        transaction = ingest_uc.execute(temp_path)

        return jsonify(vars(transaction)), 200

@api_bp.route("/transactions/<id>", methods=["GET"])
def read_transaction(id):
    uc = get_use_case("get_transaction_use_case")
    transaction = uc.execute(id)
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(vars(transaction))

@api_bp.route("/transactions", methods=["GET"])
def read_transactions():
    uc = get_use_case("list_transactions_use_case")
    transactions = uc.execute()
    return jsonify([vars(t) for t in transactions])
