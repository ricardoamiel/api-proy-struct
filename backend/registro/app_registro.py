from fastapi import FastAPI, HTTPException
import mysql.connector
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

host_name = "3.219.70.47"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "your_database"
schema_name = "registro_schema"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    mydb.close()
    if not user:
        return False
    if not verify_password(password, user[2]):  # user[2] should be the hashed_password column
        return False
    return user

@app.post("/signup/", response_model=schemas.User)
def create_user(user: schemas.User):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"USE {schema_name}")
    hashed_password = get_password_hash(user.password)
    sql = "INSERT INTO users (username, hashed_password) VALUES (%s, %s)"
    val = (user.username, hashed_password)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return user

@app.post("/token/", response_model=schemas.Token)
def login_for_access_token(user: schemas.User):
    user_auth = authenticate_user(user.username, user.password)
    if not user_auth:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
