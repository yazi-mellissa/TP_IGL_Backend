import requests
from sqlalchemy.orm import Session
from fastapi import status
from models.Article import Article
from models.Auteur import Auteur
from models.Institution import Institution
from models.Mot_Cle import Mot_Cle
from models.Reference import Reference
from models.Moderateur import Moderateur
from utils.Auth import check_token, Token_Payload
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse
from utils.ExtendedArticle import ExtendedArticle
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
    
    # Done | Wait for merge with hiba elastic search and samy get data from pdf in ExtendedArticle class
    def upload_article (db: Session, token : str, link : str):
        is_admin(token=token)
        data = requests.api.get(url=link)
        if (data.headers.get('content-type') == "application/pdf" ): # is PDF file
            # truc traitement est fait dans l'initialisation de l'objet
            temp_article = ExtendedArticle(Link=link)
            
            # truc indexation elastic search
            temp_article.indexer()

            # insert in the database
            nouveau_article = Article(Texte=temp_article.Texte, Resume=temp_article.Resume, Titre=temp_article.Titre, Valide=False, Date_Publication=temp_article.get_date())
            
            # insert in the database : Les Auteurs si ca n'existe pas
            for aut in temp_article.Auteurs:
                auteur = db.query(Auteur).where(Auteur.Nom == aut[0]).first()
                if (auteur):
                    nouveau_article.Auteurs.append(auteur)
                else:
                    institution = db.query(Institution).where(Institution.Nom == aut[2][0]).first()
                    nouveau_auteur = None
                    if (institution):
                        nouveau_auteur = Auteur(Nom=aut[0],Email=aut[1],ID_Institution=institution.ID_Institution)
                    else:
                        nouvelle_institution = Institution(Nom=aut[2][0],Adresse=aut[2][1])
                        db.add(nouvelle_institution)
                        db.commit()
                        db.refresh(nouvelle_institution)
                        nouveau_auteur = Auteur(Nom=aut[0],Email=aut[1],ID_Institution=nouvelle_institution.ID_Institution)
                    db.add(nouveau_auteur)
                    db.commit()
                    db.refresh(nouveau_auteur)
                    nouveau_article.Auteurs.append(nouveau_auteur)

            # insert in the database : Les Mots Cles si ca n'existe pas
            for mot in temp_article.Mots_Cles:
                mot_cle = db.query(Mot_Cle).where(Mot_Cle.Mot_Cle == mot).first()
                if (mot_cle is not None):
                    nouveau_article.Mots_Cles.append(mot_cle)
                else:
                    nouveau_mot_cle = Mot_Cle(Mot_Cle=mot)
                    db.add(nouveau_mot_cle)
                    db.commit()
                    db.refresh(nouveau_mot_cle)
                    nouveau_article.Mots_Cles.append(nouveau_mot_cle)

            # insert in the database : Les References si ca n'existe pas
            for ref in temp_article.References:
                reference = db.query(Reference).where(Reference.Reference == ref).first()
                if (reference is not None):
                    nouveau_article.References.append(reference)
                else:
                    nouvelle_reference = Reference(Reference=ref)
                    db.add(nouvelle_reference)
                    db.commit()
                    db.refresh(nouvelle_reference)
                    nouveau_article.References.append(nouvelle_reference)

            db.add(nouveau_article)
            db.commit()
            db.refresh(nouveau_article)
            
            # write the file
            temp_article.set_id(ID=nouveau_article.ID_Article)
            temp_article.save_pdf(data=data.content)
            
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

