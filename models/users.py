from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database.config import Base


class User(Base):
    """
    SQLAlchemy User Model
    """
    __tablename__ = 'User'  # noqa

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"
