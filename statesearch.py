import os
import sqlalchemy
import datetime
import qrcode
import json
import h5py
import codecs
import io

from flask import json
from flask import Flask
from flask import *
from flask import Request, Response
from flask.helpers import make_response
from typing import Union
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify # <- `jsonify` instead of `json` 
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['DB_NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base = declarative_base()
ma = Marshmallow()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def friendstate(request: Request) -> Union[Response, None]:
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername = driver_name,
            username = db_user,
            password = db_password,
            database = db_name,
            query = query_string,
        ),
        encoding = "utf-8",
        pool_size = 5,
        max_overflow = 2,
        pool_timeout = 30,
        pool_recycle = 1800
    )
    SessionClass = sessionmaker(engine) 
    session = SessionClass()
    
    if request.method == 'POST':
        request_json = request.get_json()
        get_id = request_json['ids']
        #get_if = ["222", "a237246d0b96adf1d"]
        reslist = list()
        dictonary = {}
        oneuser = "nulll"

        tableget = session.query(table).all()

        for anid in get_id:
            #reslist.append(anid)
            for onetable in tableget:
                #reslist.append(onetable)
                if (onetable.id == anid):
                    dictonary = {"id":onetable.id ,"number":onetable.number ,"state":onetable.state, "user":onetable.user}
                    reslist.append(dictonary)

        #res_data = json.dumps(reslist)
        response_data = jsonify({'idlist': tableSchema(many = True).dump(reslist)})
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response

    elif request.method == 'GET':
        return 'GET'

class table(Base):
    __tablename__="userlist"
    number = Column(Integer, primary_key=True)
    id = Column(String(255))
    user = Column(String(255))
    state = Column(Integer)

class tableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=table
        load_instance=True

class dataclass:
    user: String
    state: String