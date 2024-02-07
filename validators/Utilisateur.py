from pydantic import BaseModel

class User(BaseModel):
    token : str

class User_Get_Favoris(User):
    pass

class User_Ajouter_Favoris(User):
    ID_Article : int
    
class User_Supprimer_Favoris(User_Ajouter_Favoris):
    pass

class User_Rechercher(User):
    query: str