from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import mysql.connector
from datetime import timedelta, datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "hello_developer"
jwt = JWTManager(app)

def db_database():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "******",
        database = "sample"
    )

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    
    if username == "hari" and password == "Helloworld":  
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(seconds=30),  
            additional_claims={"issued_at": datetime.utcnow().isoformat()}  
        )
        return jsonify(token=access_token)
 
    return jsonify(msg="Invalid credentials"), 401

@app.route("/create_data", methods=["POST"])
@jwt_required()
def create_data():
    data = request.get_json()
    name = data.get('name')
    marks = data.get('marks')

    if not name or not marks:
        return jsonify({"error": "Missing name or marks"}), 400
    
    curr = db_database()
    cursor = curr.cursor()
    sql_query = "INSERT INTO student(name,marks) VALUES (%s,%s)"
    cursor.execute(sql_query, (name, marks))
    curr.commit()
    cursor.close()
    curr.close()

    return jsonify({"message": "Data posted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
