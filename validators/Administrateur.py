from pydantic import BaseModel

class Admin(BaseModel):
    token : str

class Admin_Upload_Article(Admin):
    link : str

class Admin_Ajouter_Moderateur(Admin):
    nom : str
    email : str
    password : str

class Admin_Supprimer_Moderateur(Admin):
    ID_Moderateur : int