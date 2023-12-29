from sqlalchemy import Table, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

Article_Favori = Table("Articles_Favoris",
    Base.metadata,
    Column('ID_Article_Favori', Integer, primary_key=True, autoincrement=True),
    Column('ID_Article', Integer, ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE')),
    Column('ID_Compte', Integer, ForeignKey('Utilisateurs.ID_Utilisateur', ondelete='CASCADE', onupdate='CASCADE'))
)