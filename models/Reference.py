from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from database import Base

class Reference(Base):
    __tablename__ = "Les_References"
    __table_args__ = {'extend_existing': True}

    ID_Reference : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Reference : Mapped[str] = mapped_column(Text)

    def __init__(self, Reference : str):
        self.Reference = Reference

    def get_Object(self):
        return {
            "ID_Reference" : self.ID_Reference,
            "Reference" : self.Reference
        }