from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "3.219.70.47"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "your_database"
schema_name = "pacientes_schema"

@app.get("/pacientes")
def get_pacientes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute("SELECT * FROM pacientes")
    result = cursor.fetchall()
    mydb.close()
    return {"pacientes": result}

@app.get("/pacientes/{id}")
def get_paciente(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"SELECT * FROM pacientes WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"paciente": result}
    raise HTTPException(status_code=404, detail="Paciente not found")

@app.post("/pacientes")
def add_paciente(item: schemas.Paciente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "INSERT INTO pacientes (name, age) VALUES (%s, %s)"
    val = (item.name, item.age)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Paciente added successfully"}

@app.put("/pacientes/{id}")
def update_paciente(id: int, item: schemas.Paciente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "UPDATE pacientes SET name=%s, age=%s WHERE id=%s"
    val = (item.name, item.age, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Paciente updated successfully"}

@app.delete("/pacientes/{id}")
def delete_paciente(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"DELETE FROM pacientes WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Paciente deleted successfully"}
