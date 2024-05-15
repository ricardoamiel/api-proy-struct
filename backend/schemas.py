from pydantic import BaseModel

class Medico(BaseModel):
    name: str
    specialty: str

class Paciente(BaseModel):
    name: str
    age: int

class Cita(BaseModel):
    medico_id: int
    paciente_id: int
    date: str

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
