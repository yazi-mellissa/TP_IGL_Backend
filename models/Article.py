from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean
from database import Base
from sqlalchemy.dialects.mysql import LONGTEXT

from models.Auteur import Auteur
from models.Auteur_Article import Auteur_Article

from models.Reference import Reference
from models.Article_Reference import Article_Reference

from models.Mot_Cle import Mot_Cle
from models.Article_Mot_Cle import Article_Mot_Cle

class Article(Base):
    __tablename__ = "Articles"
    __table_args__ = {'extend_existing': True}

    ID_Article : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Titre : Mapped[str] = mapped_column(String(1000))
    Resume : Mapped[str] = mapped_column(LONGTEXT)
    Texte : Mapped[str] = mapped_column(LONGTEXT)
    Date_Publication : Mapped[str] = mapped_column(String(100))
    Valide : Mapped[bool] = mapped_column(Boolean)

    Auteurs : Mapped[list["Auteur"]] = relationship(secondary=Auteur_Article)
    References : Mapped[list["Reference"]] = relationship(secondary=Article_Reference)
    Mots_Cles : Mapped[list["Mot_Cle"]] = relationship(secondary=Article_Mot_Cle)

    def __init__(self, Titre : str, Resume : str, Texte : str, Date_Publication : str, Valide : str):
        self.Titre = Titre
        self.Resume = Resume
        self.Texte = Texte
        self.Date_Publication = Date_Publication
        self.Valide = Valide


    def get_Object(self):
        temp_auteurs = []
        for i in [*self.Auteurs]:
            temp_auteurs.append(i.Nom)
        temp_references = []
        for i in [*self.References]:
            temp_references.append(i.Reference)
        temp_Mot_Cles = []
        for i in [*self.Mots_Cles]:
            temp_Mot_Cles.append(i.Mot_Cle)
        return {
            "ID_Article" : self.ID_Article,
            "Titre" : self.Titre,
            "Resume" : self.Resume,
            "Texte" : self.Texte,
            "Date_Publication" : self.Date_Publication,
            "Valide" : self.Valide,
            "Auteurs" : temp_auteurs,
            "References" : temp_references,
            "Mots_Cles" : temp_Mot_Cles
        }