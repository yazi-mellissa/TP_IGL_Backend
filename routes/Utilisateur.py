from fastapi import APIRouter, status, Depends
from validators.Utilisateur import *
from controllers.UserController import UserController
from utils.HTTPResponse import HTTPResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
    
@router.get("/")
def read_root():
    raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Guerrout User")

@router.post("/articles-favoris")
def handle_liste_des_favoris(user : User_Get_Favoris, db: Session = Depends(get_db)):
    UserController.liste_des_favoris(db, user.token)

@router.post("/ajouter-article-favoris")
def handle_ajouter_favoris(user : User_Ajouter_Favoris, db: Session = Depends(get_db)):
    UserController.ajouter_favori(db, user.token, user.ID_Article)

@router.post("/telecharger-article-favoris")
def handle_ajouter_favoris(user : User_Ajouter_Favoris, db: Session = Depends(get_db)):
    UserController.telecharger_favori(db, user.token, user.ID_Article)

@router.post("/search")
def handle_search(user : User_Rechercher, db: Session = Depends(get_db)):
    UserController.rechercher(db, user.token, user.query)
    
@router.post("/get-article")
def handle_get_article(user: User_Get_Article, db: Session = Depends(get_db)):
    UserController.get_article(db, user.token, user.ID_Article)
    
@router.post("/supprimer-article-favoris")
def handle_supprimer_favoris(user : User_Supprimer_Favoris, db: Session = Depends(get_db)):
    UserController.supprimer_favori(db, user.token, user.ID_Article)
