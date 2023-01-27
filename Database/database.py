from sqlalchemy import create_engine, update

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, scoped_session


Server = 'DESKTOP-SK86OU9\SQLEXPRESS'

Database = 'Flask_teste'

Driver= 'ODBC Driver 17 for SQL Server'

ConnectionString = f'mssql://@{Server}/{Database}?driver={Driver}'


engine = create_engine(ConnectionString, connect_args={"check_same_thread" : False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


Base.query = db_session.query_property()