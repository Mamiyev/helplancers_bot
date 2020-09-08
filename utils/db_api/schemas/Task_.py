from sqlalchemy import sql, Integer, Column, Sequence, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from utils.db_api.database import db
from utils.db_api.schemas.Client import Client_
from utils.db_api.schemas.model import TimedBaseModel


class Task_(TimedBaseModel):
    __tablename__ = "Task_"
    query: sql.Select

    # Id заказа
    id = Column(Integer, primary_key=True)

    category_code = Column(String(20))
    category_name = Column(String(50))

    subcategory_code = Column(String(20))
    subcategory_name = Column(String(50))

    description = Column(String(255))
    salary = Column(Integer)

    status = Column(Boolean, default=False)

    # Id заказчика
    client_id = Column(BigInteger)

    def __repr__(self):
        return f"""
📌Категория: {self.category_name}
Подкатегория: {self.subcategory_name}
✍️Описание:{self.description}
💰 Цена:{self.salary}
"""


