import requests
from sqlalchemy.orm import Session
from fastapi import status
from models.Article import Article
from models.Moderateur import Moderateur
from utils.Auth import check_token, Token_Payload
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse
from utils import get_file_path
from passlib.hash import sha256_crypt

# Done

def is_admin (token : str) -> Token_Payload:
    checked_token = check_token(token=token)
    if (not checked_token ):
        raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    elif (checked_token.get_role() != Role.ADMIN ):
        raise HTTPResponse(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this section")
    return checked_token

class AdminController():
    
    # Partially Done | Wait for merge with hiba elastic search and samy get data from pdf
    def upload_article (db: Session, token : str, link : str):
        is_admin(token=token)
        data = requests.api.get(url=link)
        if (data.headers.get('content-type') == "application/pdf" ): # is PDF file
            # truc traitement
            titre = ''
            texte = ''
            resume = ''
            date = ''
            # truc indexation elastic search

            # insert in the database
            nouveau_article = Article(Texte=texte, Resume=resume, Titre=titre, Valide=False, Date_Publication=date)
            db.add(nouveau_article)
            db.commit()
            db.refresh(nouveau_article)
            # write the file
            file_name = get_file_path(nouveau_article.ID_Article)
            file = open(file_name,'wb')
            file.write(data.content)
            file.close()
            raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Success")
        else: # is not PDF file
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST,detail="Not a PDF file")
        
    # Done | Works
    def ajouter_moderateur(db: Session, token : str, nom : str, email : str, password : str):
        checked_token = is_admin(token=token)
        password = sha256_crypt.hash(password)
        nouveau_moderateur = Moderateur(Nom=nom, Email=email, Password=password, ID_Admin_Valide=checked_token.get_id())
        db.add(nouveau_moderateur)
        db.commit()
        raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Success")

    # Done | Works
    def supprimer_moderateur(db: Session, token : str, ID_mod : int):
        checked_token = is_admin(token=token)
        mod = db.query(Moderateur).where(Moderateur.ID_Moderateur == ID_mod).first()
        if ( mod.ID_Admin_Valide == checked_token.id ):
            db.delete(mod)
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Moderateur deleted successfully")
        else:
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossible de supprimer un moderateur que vous n'avez pas validé")

    # Done | Works
    def moderateurs(db: Session, token : str):
        is_admin(token=token)
        result = db.query(Moderateur).with_entities(Moderateur.ID_Moderateur, Moderateur.Nom, Moderateur.Email).all()
        new_result = []
        for mod in result:
            new_result.append({
                "ID_Moderateur": mod[0],
                "Nom": mod[1],
                "Email": mod[2]
            })
        raise HTTPResponse(
            status_code=status.HTTP_200_OK,
            detail=new_result
        )

