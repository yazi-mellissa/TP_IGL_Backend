from fastapi import APIRouter, status, Depends
from validators.Administrateur import *
from controllers.AdminController import AdminController
from utils.HTTPResponse import HTTPResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
    
@router.get("/")
def read_root():
    raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Guerrout Admin")

@router.post("/upload-article")
def handle_upload_article(user : Admin_Upload_Article, db: Session = Depends(get_db)):
    AdminController.upload_article(db, user.token, user.link)

@router.post("/ajouter-moderateur")
def handle_ajouter_moderateur(user : Admin_Ajouter_Moderateur, db: Session = Depends(get_db)):
    AdminController.ajouter_moderateur(db, user.token, user.nom, user.email, user.password)

@router.post("/supprimer-moderateur")
def handle_supprimer_moderateur(user : Admin_Supprimer_Moderateur, db: Session = Depends(get_db)):
    AdminController.supprimer_moderateur(db, user.token, user.ID_Moderateur)

@router.post("/liste-des-moderateurs")
def handle_liste_des_moderateurs(user : Admin, db: Session = Depends(get_db)):
    AdminController.moderateurs(db, user.token)

@router.post("/liste-des-articles")
def handle_liste_des_moderateurs(user : Admin, db: Session = Depends(get_db)):
    AdminController.articles(db, user.token)