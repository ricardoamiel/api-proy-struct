from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "3.219.70.47"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "your_database"
schema_name = "medicos_schema"

@app.get("/medicos")
def get_medicos():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute("SELECT * FROM medicos")
    result = cursor.fetchall()
    mydb.close()
    return {"medicos": result}

@app.get("/medicos/{id}")
def get_medico(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"SELECT * FROM medicos WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"medico": result}
    raise HTTPException(status_code=404, detail="Medico not found")

@app.post("/medicos")
def add_medico(item: schemas.Medico):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "INSERT INTO medicos (name, specialty) VALUES (%s, %s)"
    val = (item.name, item.specialty)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Medico added successfully"}

@app.put("/medicos/{id}")
def update_medico(id: int, item: schemas.Medico):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    sql = "UPDATE medicos SET name=%s, specialty=%s WHERE id=%s"
    val = (item.name, item.specialty, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Medico updated successfully"}

@app.delete("/medicos/{id}")
def delete_medico(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"DELETE FROM medicos WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Medico deleted successfully"}
