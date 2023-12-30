import jwt
from models.Utilisateur import Utilisateur
from models.Moderateur import Moderateur
from models.Administrateur import Administrateur
from utils.HTTPResponse import HTTPResponse
from utils.Creds import JwtCreds
from utils.Date import Date
from utils.Role import Role
from fastapi import status

class Token_Payload():
    id : int
    nom : str
    role : Role
    expiration : Date

    def __init__(self, id : str = None, nom : str = None, role : Role = None, token_payload : dict = None) -> None:
        if (token_payload is not None):
            self.id = token_payload.get("id")
            self.nom = token_payload.get("nom")
            self.role = Role(token_payload.get("role"))
            self.expiration = Date(date=token_payload.get("expiration"))
            return
        if (token_payload is None):
            self.id = id
            self.nom = nom
            self.role = role
            self.expiration = Date.today().date_after_days(30)
            return
        
    def get_Token_Payload(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "role": self.role.value,
            "expiration": self.expiration.get_date()
        }
    
    def get_role(self) -> Role:
        return self.role
    def get_id(self) -> int:
        return self.id
    def get_expiration(self) -> Date:
        return self.expiration

def jwt_encode(payload : Token_Payload):
    payload = payload.get_Token_Payload()
    encoded_jwt = jwt.encode(payload=payload, key=JwtCreds["Secret"], algorithm="HS256")
    return encoded_jwt
def jwt_decode(token : str):
    decoded_jwt = jwt.decode(jwt=token, key=JwtCreds["Secret"], algorithms=["HS256"])
    token_payload = Token_Payload(token_payload=decoded_jwt)
    return token_payload

def generate_token(Account : Utilisateur | Moderateur | Administrateur):
    def generate_token_Utilisateur(User: Utilisateur):
        payload = Token_Payload(id=User.ID_Utilisateur, nom=User.Nom, role=Role.USER)
        return jwt_encode(payload=payload)
    def generate_token_Moderateur(Mod: Moderateur):
        payload = Token_Payload(id=Mod.ID_Moderateur, nom=Mod.Nom, role=Role.MOD)        
        return jwt_encode(payload=payload)
    def generate_token_Administrateur(Admin: Administrateur):
        payload = Token_Payload(id=Admin.ID_Administrateur, nom=Admin.Nom, role=Role.ADMIN)
        return jwt_encode(payload=payload)
    if (isinstance(Account, Utilisateur) ):
        return generate_token_Utilisateur(Account)
    elif (isinstance(Account, Moderateur) ):
        return generate_token_Moderateur(Account)
    elif (isinstance(Account, Administrateur) ):
        return generate_token_Administrateur(Account)
    else:
        return None
    
def check_token(token: str) -> bool | Token_Payload:
    try:
        payload = jwt_decode(token=token)
    except:
        raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Token invalid")
    expiration = payload.get_expiration()
    
    if (expiration.is_before_today() ):
        return False
    else:
        return payload