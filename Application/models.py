from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, ForeignKey
from Application import db, login_manager
from flask_login import UserMixin
from typing import List
import datetime

class User(db.Model, UserMixin): # type: ignore
    user_id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, init=True)
    name: Mapped[str] = mapped_column(String(16), nullable=False, init=True)
    password: Mapped[str] = mapped_column(String(16), nullable=False, init=True)
    joined_on: Mapped[datetime.date] = mapped_column(nullable=False, init=False, default=datetime.date.today())

    def get_id(self):
        return str(self.user_id)
    
    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))
    
    @validates('joined_on')
    def createdatValidator(self, key: str, value: datetime.date) -> datetime.date:
        if self.joined_on is not None:
            raise ValueError("The joined_on field is constant and cannot be modified")
        return value