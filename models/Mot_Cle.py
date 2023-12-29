from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Mot_Cle(Base):
    __tablename__ = "Mots_Cles"
    __table_args__ = {'extend_existing': True}

    ID_Mot_Cle : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Mot_Cle : Mapped[str] = mapped_column(String(200))

    def __init__(self, Mot_Cle : str):
        self.Mot_Cle = Mot_Cle

    def get_Object(self):
        return {
            "ID_Mot_Cle" : self.ID_Mot_Cle,
            "Mot_Cle" : self.Mot_Cle
        }