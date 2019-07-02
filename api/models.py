from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, inspect
from sqlalchemy.orm import relationship
from .settings import engine

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)

    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True, unique=True)

    birthday = Column(Date, nullable=True)
    first_name = Column(String(35), nullable=True)
    last_name = Column(String(35), nullable=True)

    def __repr__(self):
        return "<User(id={}, email={})>".format(self.id, self.email)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def formatted_birthday(self):
        return self.birthday.strftime("%m/%d/%Y")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    datetime = Column(DateTime)
    title = Column(String(120), nullable=False)
    text = Column(String(500), nullable=True)

    def __repr__(self):
        return "<Note(id={}, title={})>".format(self.id, self.title)


Base.metadata.create_all(engine)
