from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Administrateur(Base):
    __tablename__ = "Administrateurs"
    __table_args__ = {'extend_existing': True}

    ID_Administrateur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Email : Mapped[str] = mapped_column(String(200))
    Password : Mapped[str] = mapped_column(String(200))

    def __init__(self, Nom : str, Email : str, Password : str):
        self.Nom = Nom
        self.Email = Email
        self.Password = Password

    def get_Object(self):
        return {
            "ID_Administrateur" : self.ID_Administrateur,
            "Nom" : self.Nom,
            "Email" : self.Email,
            "Password" : self.Password
        }