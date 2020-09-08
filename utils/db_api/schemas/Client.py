from sqlalchemy import Column, BigInteger, Sequence, Integer, sql, DateTime, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship

from utils.db_api.database import db
from utils.db_api.schemas.model import TimedBaseModel


class Client_(TimedBaseModel):
    __tablename__="Client_"
    query:sql.Select

    id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50))
    current_task_id = Column(Integer)

    def __repr__(self):
        return f"""Id Клиента: {self.id}
        Текущее (последнее добавленое) задание: {self.current_task_id}
        """






