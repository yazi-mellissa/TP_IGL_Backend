from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database import Base
from models.Institution import Institution

class Auteur(Base):
    __tablename__ = "Auteurs"
    __table_args__ = {'extend_existing': True}

    ID_Auteur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Email : Mapped[str] = mapped_column(String(200))
    ID_Institution : Mapped[int] = mapped_column(ForeignKey('Institutions.ID_Institution', ondelete='CASCADE', onupdate='CASCADE'))

    Institution : Mapped["Institution"] = relationship("Institution", foreign_keys=[ID_Institution])
    
    def __init__(self, Nom : str, Email : str, ID_Institution : int):
        self.Nom = Nom
        self.Email = Email
        self.ID_Institution = ID_Institution

    def get_Object(self):
        return {
            "ID_Auteur" : self.ID_Auteur,
            "Nom" : self.Nom,
            "Email" : self.Email,
            "ID_Institution" : self.ID_Institution,
            "Institution" : self.Institution.get_Object()
        }