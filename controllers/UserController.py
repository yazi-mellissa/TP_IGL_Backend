from fastapi import status
from utils.Auth import check_token, Token_Payload
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse
from sqlalchemy.orm import Session
from models.Article import Article
from models.Utilisateur import Utilisateur
from sqlalchemy import update

# Done

def is_user (token : str) -> Token_Payload:
    checked_token = check_token(token=token)
    if (not checked_token ):
        raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    elif (checked_token.get_role() != Role.USER ):
        raise HTTPResponse(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this section")
    return checked_token

class UserController():

    # Done | Works
    def liste_des_favoris(db: Session, token: str):
        checked_token = check_token(token=token)
        user = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
        liste_des_favoris = []
        for article in user.Articles_Favoris:
            liste_des_favoris.append(article.get_Object())
        raise HTTPResponse(status_code=status.HTTP_200_OK, detail=liste_des_favoris)
    
    # Done | Works
    def ajouter_favori(db: Session, token: str, ID_article : int):
        checked_token = check_token(token=token)
        user = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
        article = db.query(Article).filter(Article.ID_Article == ID_article).first()
        if ( not article ):
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Article inexistant")
        elif (article in user.Articles_Favoris):
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Article deja favoris")
        else:
            user.Articles_Favoris.append(article)
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article ajouter au favoris")

    # Done | Works
    def supprimer_favori(db: Session, token: str, ID_article : int):
        checked_token = check_token(token=token)
        user = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
        article = db.query(Article).filter(Article.ID_Article == ID_article).first()
        if ( not article ):
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Article non existant")
        elif (article not in user.Articles_Favoris):
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Article non existant dans la liste des favoris")
        else:
            index = 0
            for article in user.Articles_Favoris:
                if (article.ID_Article == ID_article):
                    break
                index +=1
            user.Articles_Favoris.pop(index)
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article supprimé de la liste des favoris")