from sqlalchemy import inspect, text
from core.base import Base
from core.session import engine
from db.models.user import User
from db.models.account import Account
from db.models.category import Category
from db.models.transaction import Transaction

Base.metadata.create_all(bind=engine)
insp = inspect(engine)
