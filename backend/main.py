from flask import Flask, request, jsonify
from flask_cors import CORS
from . import models, database, worker

app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

@app.route("/transactions/upload", methods=["POST"])
def upload_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        content = file.read().decode("utf-8")
        
        # Create initial record
        db_transaction = models.Transaction(status="pending")
        database.db_session.add(db_transaction)
        database.db_session.commit()
        
        # Launch background task
        worker.start_processing(db_transaction.id, content)

        return jsonify(db_transaction.to_dict()), 200

@app.route("/transactions/<id>", methods=["GET"])
def read_transaction(id):
    transaction = database.db_session.query(models.Transaction).filter(models.Transaction.id == id).first()
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction.to_dict())

@app.route("/transactions", methods=["GET"])
def read_transactions():
    transactions = database.db_session.query(models.Transaction).all()
    return jsonify([t.to_dict() for t in transactions])

def main():
    database.init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == "__main__":
    main()
