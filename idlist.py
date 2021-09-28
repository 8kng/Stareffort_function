import os
import sqlalchemy

from flask import Request, Response
from flask.helpers import make_response
from typing import Union
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base

connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['DB_NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base = declarative_base()

def main(request: Request) -> Union[Response, None]:
    if request.method == 'POST':
        request_json = request.get_json()
        getid = request_json['id']
        getuser = request_json['user']

        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername = driver_name,
                username = db_user,
                password = db_password,
                database = db_name,
                query = query_string,
            ),
            pool_size = 5,
            max_overflow = 2,
            pool_timeout = 30,
            pool_recycle = 1800
        )
        SessionClass = sessionmaker(engine)
        session = SessionClass()

        idadd = Question(id = getid, user = getuser)
        session.add(idadd)
        session.commit()
        
        return make_response('201 uploaded', 201)

    elif request.method == 'GET':
        return 'get'
    return 'Helloo'

class Question(Base):
    __tablename__="userlist"
    number = Column(Integer, primary_key=True)
    id = Column(String(255))
    user = Column(String(255))
    state = Column(Integer)