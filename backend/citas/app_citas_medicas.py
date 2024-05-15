from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "3.219.70.47"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "your_database"
schema_name = "citas_schema"

@app.get("/citas")
def get_citas():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute("SELECT * FROM citas")
    result = cursor.fetchall()
    mydb.close()
    return {"citas": result}

@app.get("/citas/{id}")
def get_cita(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"SELECT * FROM citas WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"cita": result}
    raise HTTPException(status_code=404, detail="Cita not found")

@app.post("/citas")
def add_cita(item: schemas.Cita):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "INSERT INTO citas (medico_id, paciente_id, date) VALUES (%s, %s, %s)"
    val = (item.medico_id, item.paciente_id, item.date)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Cita added successfully"}

@app.put("/citas/{id}")
def update_cita(id: int, item: schemas.Cita):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "UPDATE citas SET medico_id=%s, paciente_id=%s, date=%s WHERE id=%s"
    val = (item.medico_id, item.paciente_id, item.date, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Cita updated successfully"}

@app.delete("/citas/{id}")
def delete_cita(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"DELETE FROM citas WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Cita deleted successfully"}
