import os

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://{user}:{password}@db:{host}/{name}".format(user=os.environ.get('DB_USER'),
                                                                                         password=os.environ.get(
                                                                                             'DB_PASSWORD'),
                                                                                         host=os.environ.get('DB_HOST'),
                                                                                         name=os.environ.get(
                                                                                             'DB_NAME')), echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
