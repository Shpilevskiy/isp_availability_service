import json

import falcon
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

from ByFlyParser import ByflyIsXponParser

engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@db/postgres',
                       isolation_level="READ UNCOMMITTED", echo=True)
Session = sessionmaker()
Base = declarative_base()
Session.configure(bind=engine)

session = Session()


class ISP(Base):
    __tablename__ = 'providers'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    url = Column(String(100), unique=True)
    connections = relationship('Connection', back_populates='isp')


class Status(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True)


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True)
    isp_id = Column(Integer, ForeignKey('providers.id'))
    isp = relationship("ISP", back_populates="connections")
    region = Column(String)
    city = Column(String)
    street = Column(String)
    house_number = Column(String)


class ISP_Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        isps = session.query(ISP).all()
        isp_data = [{"name": isp.name, "url": isp.url} for isp in isps]
        resp.body = json.dumps(isp_data)


def cleanup_like_field(s):
    if '*' in s or '_' in s:
        looking_for = s.replace('_', '__')\
                            .replace('*', '%')\
                            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(s)
    return looking_for


class ConnectionResource(object):
    def on_get(self, req, resp):
        street = req.get_param('street', default="")
        region = req.get_param('region', default="")
        city = req.get_param('city', default="")
        number = req.get_param('number', default="")


        str_field = cleanup_like_field(street)
        connections = session.query(Connection).filter(Connection.street.ilike(str_field))
        connections_data = [
            {
                "isp_name": con.isp.name,
                "isp_url": con.isp.url,
                "region": con.region,
                "city": con.city,
                "street": con.street,
                "house_number": con.house_number,
            } for con in connections
        ]
        resp.body = json.dumps(connections_data)


def fill_db():
    Base.metadata.create_all(engine)

    byfly = ISP(name='ByFly', url='test')
    session.add(byfly)
    session.commit()
    byfly = session.query(ISP).filter(ISP.name == 'ByFly').first()

    for con in ByflyIsXponParser().check_street(street_name=u'Алибегова'):
        connection = Connection(isp=byfly, street=con['street'],
                                city=con['city'],
                                region=con['region'], house_number=con['number'])
        session.add(connection)
        session.commit()


def main():
    fill_db()

if __name__ == '__main__':
    main()

api = falcon.API()
api.add_route('/providers', ISP_Resource())
api.add_route('/connections', ConnectionResource())
