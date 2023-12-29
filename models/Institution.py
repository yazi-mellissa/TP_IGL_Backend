from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Institution(Base):
    __tablename__ = "Institutions"
    __table_args__ = {'extend_existing': True}

    ID_Institution : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Adresse : Mapped[str] = mapped_column(String(200))

    def __init__(self, Nom : str, Adresse : str):
        self.Nom = Nom
        self.Adresse = Adresse

    def get_Object(self):
        return {
            "ID_Institution": self.ID_Institution,
            "Nom": self.Nom,
            "Adresse": self.Adresse
        }