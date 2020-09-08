from sqlalchemy import sql, Column, String, BigInteger, Integer, Sequence, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from utils.db_api.database import db
from utils.db_api.schemas.model import TimedBaseModel


class Freelancer_(TimedBaseModel):
    query: sql.Select
    __tablename__ = "Freelancer_"

    id = Column(BigInteger, primary_key=True)

    name = Column(String(20))
    category_code = Column(String(60))
    category_name = Column(String(150))

    subcategory_code = Column(String(60))
    subcategory_name = Column(String(150))

    bio = Column(String(255))
    average_salary = Column(Integer)
    github = Column(String(50))

    status = Column(Boolean)

    def __repr__(self):
        return f"""
    📌Имя: {self.name}
Категории: {self.category_name}
Подкатегории: {self.subcategory_name}
Мини-резюме: \n{self.bio}\n
Средний чек за заказ: {self.average_salary}
    """


class Subscription_(TimedBaseModel):
    __tablename__ = "Subscription_"
    query: sql.Select
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    freelancer_id = Column(BigInteger)
    free_trial = Column(Boolean,default=True)

    async def check_free_trial(self):
        if self.free_trial:
            return "бесплатная подписка не использована"
        else:
            return "бесплатная подписка использована"

    def __repr__(self):
        return f"""Id фрилансера: {self.freelancer_id}
Начало подписки: {self.start_date}
Конец подписки: {self.end_date}
"""

Freelancer_.subscriptions = relationship("Subscriptions", order_by=Subscription_.id, back_populates="freelancer")
