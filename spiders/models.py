from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, Float, ForeignKey, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from spiders import settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine("postgresql+psycopg2://{}:{}@localhost:port/{}".format(settings.DB_USER,
                                                                                settings.DB_PASSWORD,
                                                                                settings.DB_NAME),
                         encoding='utf8', echo=False)


def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Bank(DeclarativeBase):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class BankOffice(DeclarativeBase):
    __tablename__ = 'bank_office'

    id = Column(Integer, primary_key=True)

    bank_id = Column(Integer, ForeignKey('bank.id'), nullable=False)
    bank = relationship('Bank', backref=backref('offices', lazy=True))


class ExchangeRate(DeclarativeBase):
    __tablename__ = 'exchange_rate'

    id = Column(Integer, primary_key=True)
    currency = Column(String(3), index=True)
    type = Column(String(4), index=True)
    rate = Column(Float)
    date = Column(Date, index=True)
    scraping_date = Column(DateTime, index=True)

    bank_id = Column(Integer, ForeignKey('bank.id'), nullable=False)
    bank = relationship('Bank', backref=backref('rates', lazy=True))