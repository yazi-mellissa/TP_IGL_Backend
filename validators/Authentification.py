from pydantic import BaseModel

class Account(BaseModel):
    token : str

class Account_To_LogIn(BaseModel):
    email : str
    password : str

class Account_To_SignUp(Account_To_LogIn):
    nom : str

class Account_To_Update(Account):
    nom : str = None
    password : str = None