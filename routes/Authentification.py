from fastapi import APIRouter
from validators.Authentification import *
from controllers.Authentification import Authentification
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.post("/login")
def handle_login(account : Account_To_LogIn, db : Session = Depends(get_db)):
    Authentification.log_in(db, account.email, account.password)

@router.post("/signup")
def handle_signup(account : Account_To_SignUp, db : Session = Depends(get_db)):
    Authentification.sign_up(db, account.email, account.password, account.nom)

@router.post("/my-account")
def handle_my_account(account : Account, db : Session = Depends(get_db)):
    Authentification.get_profile(db, account.token)

@router.post("/update-account")
def handle_update_account(account : Account_To_Update, db : Session = Depends(get_db)):
    Authentification.edit_profile(db, account.token, account.nom, account.password)
