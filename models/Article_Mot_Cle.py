from sqlalchemy import Table, Integer, Column
from sqlalchemy import ForeignKey
from database import Base

Article_Mot_Cle = Table("Article_Mots_Cles",
    Base.metadata,
    Column('ID_Article_Mot_Cle', Integer, primary_key=True, autoincrement=True),
    Column('ID_Article', Integer, ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE')),
    Column('ID_Mot_Cle', Integer, ForeignKey('Mots_Cles.ID_Mot_Cle', ondelete='CASCADE', onupdate='CASCADE'))
)