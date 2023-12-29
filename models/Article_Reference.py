from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Table, Integer, Column
from sqlalchemy import ForeignKey
from database import Base

Article_Reference = Table("Article_Reference",
    Base.metadata,
    Column('ID_Article_Reference', Integer, primary_key=True, autoincrement=True),
    Column('ID_Article', Integer, ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE')),
    Column('ID_Reference', Integer, ForeignKey('Les_References.ID_Reference', ondelete='CASCADE', onupdate='CASCADE'))
)