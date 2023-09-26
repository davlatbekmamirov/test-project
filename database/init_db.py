from database.config import Base, engine
from models.users import User
from models.post import Post

Base.metadata.create_all(bind=engine)
