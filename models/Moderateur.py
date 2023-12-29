from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database import Base
from typing import Optional
from models.Administrateur import Administrateur

class Moderateur(Base):
    __tablename__ = "Moderateurs"
    __table_args__ = {'extend_existing': True}

    ID_Moderateur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Email : Mapped[str] = mapped_column(String(200))
    Password : Mapped[str] = mapped_column(String(200))
    ID_Admin_Valide : Mapped[int] = mapped_column(ForeignKey('Administrateurs.ID_Administrateur'))

    Administrateur_Validateur : Mapped["Administrateur"] = relationship("Administrateur", foreign_keys=[ID_Admin_Valide])

    def __init__(self, Nom : str, Email : str, Password : str, ID_Admin_Valide : int):
        self.Nom = Nom
        self.Email = Email
        self.Password = Password
        self.ID_Admin_Valide = ID_Admin_Valide

    def get_Object(self):
        return {
                "ID_Moderateur": self.ID_Moderateur,
                "Nom": self.Nom,
                "Email": self.Email,
                "Password": self.Password,
                "ID_Admin_Valide": self.ID_Admin_Valide,
                "Administrateur_Validateur": self.Administrateur_Validateur.get_Object()
            }