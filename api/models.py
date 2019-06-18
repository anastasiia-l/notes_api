from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from .settings import engine

Base = declarative_base()


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
        return "<User(id='%s', email='%s')>".format(self.id, self.email)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def formatted_birthday(self):
        return self.birthday.strftime("%m/%d/%Y")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    datetime = Column(DateTime)
    title = Column(String(120), nullable=False)
    text = Column(String(500), nullable=True)

    def __repr__(self):
        return "<Note(id='%s', title='%s')>".format(self.id, self.title)

Base.metadata.create_all(engine)
