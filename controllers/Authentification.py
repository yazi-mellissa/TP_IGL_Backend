from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import update
from passlib.hash import sha256_crypt

from models.Administrateur import Administrateur
from models.Moderateur import Moderateur
from models.Utilisateur import Utilisateur

from utils.Auth import generate_token, check_token
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse

class Authentification():
    
    # Done | Works
    def get_profile(db: Session, token : str):
        checked_token = check_token(token=token)
        if (not checked_token):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        if (checked_token.get_role() == Role.ADMIN):
            result = db.query(Administrateur).filter(Administrateur.ID_Administrateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        elif (checked_token.get_role() == Role.MOD):
            result = db.query(Moderateur).filter(Moderateur.ID_Moderateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        elif (checked_token.get_role() == Role.USER):
            result = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")
    
    # Done | Works
    def edit_profile(db: Session, token : str, nom : str = None , password : str = None):
        checked_token = check_token(token=token)
        if (not checked_token):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        if (checked_token.get_role() == Role.ADMIN):
            admin = db.query(Administrateur).filter(Administrateur.ID_Administrateur == checked_token.get_id()).first()
            if ( nom is not None):
                db.execute(update(Administrateur).where(Administrateur.ID_Administrateur == checked_token.get_id()).values(Nom=nom))
            if ( password is not None):
                # reste le hachage du password
                password = sha256_crypt.hash(password)
                db.execute(update(Administrateur).where(Administrateur.ID_Administrateur == checked_token.get_id()).values(Password=password))
            db.commit()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(admin),
                }
            )
        elif (checked_token.get_role() == Role.MOD):
            mod = db.query(Moderateur).filter(Moderateur.ID_Moderateur == checked_token.get_id()).first()
            if ( nom is not None):
                db.execute(update(Moderateur).where(Moderateur.ID_Moderateur == checked_token.get_id()).values(Nom=nom))
            if ( password is not None):
                # reste le hachage du password
                password = sha256_crypt.hash(password)
                db.execute(update(Moderateur).where(Moderateur.ID_Moderateur == checked_token.get_id()).values(Password=password))
            db.commit()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(mod),
                }
            )
        elif (checked_token.get_role() == Role.USER):
            user = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
            if ( nom is not None):
                db.execute(update(Utilisateur).where(Utilisateur.ID_Utilisateur == checked_token.get_id()).values(Nom=nom))
            if ( password is not None):
                # reste le hachage du password
                password = sha256_crypt.hash(password)
                db.execute(update(Utilisateur).where(Utilisateur.ID_Utilisateur == checked_token.get_id()).values(Password=password))
            db.commit()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(user),
                }
            )
        raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")

    # Done | Works
    def log_in(db: Session, email : str, password : str):
        # Search in admin
        print(sha256_crypt.hash(password))
        result = db.query(Administrateur).filter(Administrateur.Email == email).first()
        if (result is not None ):
            if (sha256_crypt.verify(password, result.Password)):
                # generat jwt and send token for admin
                raise HTTPResponse(
                    status_code=status.HTTP_200_OK,
                    detail={
                        "token": generate_token(result),
                        "role": Role.ADMIN.value
                    },
                )
            else:
                # error in the password
                raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
        else:
            # search in moderator
            result = db.query(Moderateur).filter(Moderateur.Email == email).first()
            if (result is not None ):
                if (sha256_crypt.verify(password, result.Password)):
                    # generat jwt and send token for mod
                    raise HTTPResponse(
                        status_code=status.HTTP_200_OK,
                        detail={
                            "token": generate_token(result),
                            "role": Role.MOD.value
                        },
                    )
                else:
                    # error in the password
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
            else:
                # serach in Utilisateur
                result = db.query(Utilisateur).filter(Utilisateur.Email == email).first()
                
                if (result is not None ):
                    if (sha256_crypt.verify(password, result.Password)):
                        # generat jwt and send token for user
                        raise HTTPResponse(
                            status_code=status.HTTP_200_OK,
                            detail={
                                "token": generate_token(result),
                                "role": Role.USER.value
                            },
                        )
                    else:
                        # error in the password
                        raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
                else:
                    # error in the email
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress not found")
    
    # Done | Works
    def sign_up(db: Session, email : str, password : str, nom : str):
        result = db.query(Administrateur).filter(Administrateur.Email == email).first()
        if (result is not None ):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
        else:
            # search in moderator
            result = db.query(Moderateur).filter(Moderateur.Email == email).first()
            if (result is not None ):
                raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
            else:
                # serach in Utilisateur
                result = db.query(Utilisateur).filter(Utilisateur.Email == email).first()
                if (result is not None ):
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
                else:
                    # account doesn't exist, account to be created
                    password = sha256_crypt.hash(password)
                    nouveau_utilisateur = Utilisateur(Nom=nom, Email=email, Password=password)
                    db.add(nouveau_utilisateur)
                    db.commit()
                    db.refresh(nouveau_utilisateur)
                    raise HTTPResponse(
                        status_code=status.HTTP_200_OK,
                        detail={
                            "token": generate_token(nouveau_utilisateur),
                            "role": Role.USER.value
                        }
                    )
