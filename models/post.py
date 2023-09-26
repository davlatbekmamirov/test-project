from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DateTime
from sqlalchemy.orm import relationship

from database.config import Base


class Post(Base):
    __tablename__ = 'Posts'  # noqa

    id = Column(Integer, primary_key=True)
    body = Column(VARCHAR, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    created_at = Column(DateTime, default=lambda: datetime.now())
    last_edited = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post {self.id}>"
