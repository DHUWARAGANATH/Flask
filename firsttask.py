from flask import Flask,request,jsonify
import mysql.connector

file = Flask(__name__)

def db_database():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Adra@123",
        database = "sample"
    )


@file.route("/get_data",methods = ['POST'])
def get_data():
    curr = db_database()
    cursor = curr.cursor(dictionary=True)
    select_query = "SELECT * FROM student"
    cursor.execute(select_query)
    data = cursor.fetchall()

    cursor.close()
    curr.close()

    return jsonify(data)

@file.route("/create_data",methods = ['POST'])
def create_data():
    data = request.get_json()
    name = data.get('name')
    marks = data.get('marks')

    if not name or not marks:
        return jsonify({"error": "Missing name or marks"}), 400
    
    curr = db_database()
    cursor = curr.cursor()
    sql_query = "INSERT INTO student(name,marks) VALUES (%s,%s)"
    cursor.execute(sql_query,(name,marks))
    curr.commit()
    cursor.close()
    curr.close()

    return jsonify({"message":"posted"}),200

@file.route("/update_data", methods=['POST'])
def update_data():
    data = request.get_json()
    update_name = data.get("updated_name")
    id = data.get("id")
    marks = data.get("marks")

    if not id:
        return jsonify({"message": "ID is required!"}), 400

    # update_values = []

    # if update_name:
    #     update_values.append(update_name)

    # if marks:
    #     update_values.append(marks)

    if id:
        # update_values.append(id) 
        update_query = "UPDATE student SET name = %s, marks = %s WHERE id = %s"

        curr = db_database()
        cursor = curr.cursor()
        values = (update_name, marks,id)
        cursor.execute(update_query, values)
        curr.commit()
        cursor.close()
        curr.close()

        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"message": "No data provided!"}), 400

@file.route("/delete_data",methods = ['POST'])
def delete_data():
    data = request.get_json()
    id = data.get("id")

    if id:
        curr = db_database()
        cursor = curr.cursor()
        delete_query = "DELETE FROM student WHERE id = %s"
        cursor.execute(delete_query,(id,))
        curr.commit()
        cursor.close()
        curr.close()

        return jsonify({"message":"Data deleted successfully"}),200
    
    else:
        return jsonify({"message": "No data deleted"}), 400

    
if __name__ == "__main__":
    print("server underprocess")    
    file.run(debug=True)