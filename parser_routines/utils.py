from sqlalchemy import exists

from models import ISP, Status, Connection
from exceptions import WrongProvider


def fill_db_from_connections(session, connections):
    """
    Adds connections objects to the database
    """
    for connection in connections:
        # Check whether provider exists
        isp = session.query(ISP).filter(ISP.name == connection.provider).first()
        if not isp:
            raise WrongProvider('No such provider: {}'.format(connection.provider))
        # Add new connection status if it is not already present
        if not session.query(exists().where(Status.status == connection.status)).scalar():
            session.add(Status(status=connection.status))
            session.commit()
        status = session.query(Status).filter(Status.status == connection.status).first()
        # If the connection is not already in the database - add it
        if not session.query(Connection).filter(Connection.region == connection.region,
                                                Connection.city == connection.city,
                                                Connection.street == connection.street,
                                                Connection.house_number == connection.house).count():
            session.add(Connection(region=connection.region, city=connection.city,
                                   street=connection.street, house_number=connection.house,
                                   isp=isp, status=status))
            session.commit()
        else:
            # Otherwise update existent connection status
            exist_connection = session.query(Connection).filter(Connection.region == connection.region,
                                                                Connection.city == connection.city,
                                                                Connection.street == connection.street,
                                                                Connection.house_number == connection.house).first()
            if exist_connection.status != status:
                exist_connection.status = status
                session.commit()


def call_db_filling(session, connections):
    """
    Fill connections data into the database verifying the provider is
    mentioned in the database
    """
    try:
        fill_db_from_connections(session, connections)
    except WrongProvider as error:
        print(error)
