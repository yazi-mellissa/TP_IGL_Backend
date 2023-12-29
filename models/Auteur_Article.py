from sqlalchemy import Table, Integer, Column
from sqlalchemy import ForeignKey
from database import Base

Auteur_Article = Table("Auteur_Article",
    Base.metadata,
    Column('ID_Auteur_Article', Integer, primary_key=True, autoincrement=True),
    Column('ID_Auteur', Integer, ForeignKey('Auteurs.ID_Auteur', ondelete='CASCADE', onupdate='CASCADE')),
    Column('ID_Article', Integer, ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE'))
)