from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base
from models.Article import Article
from models.Article_Favori import Article_Favori

class Utilisateur(Base):
    __tablename__ = "Utilisateurs"
    __table_args__ = {'extend_existing': True}

    ID_Utilisateur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Email : Mapped[str] = mapped_column(String(200))
    Password : Mapped[str] = mapped_column(String(200))

    Articles_Favoris : Mapped[list["Article"]] = relationship(secondary=Article_Favori)

    def __init__(self, Nom : str, Email : str, Password : str):
        self.Nom = Nom
        self.Email = Email
        self.Password = Password

    def get_Object(self):
        temp = []
        for i in [*self.Articles_Favoris]:
            temp.append(i.Titre)
        return {
            "ID_Utilisateur" : self.ID_Utilisateur,
            "Nom" : self.Nom,
            "Email" : self.Email,
            "Password" : self.Password,
            "Articles_Favoris" : temp
        }