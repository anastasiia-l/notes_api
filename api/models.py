from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Date
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


Base.metadata.create_all(engine)
