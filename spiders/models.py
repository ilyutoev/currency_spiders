from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import exists, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.url import URL
import settings

DeclarativeBase = declarative_base()


class Bank(DeclarativeBase):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    @staticmethod
    def create(bank_id=None, bank_name=None):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        if bank_id:
            check_bank = session.query(exists().where(Bank.id == bank_id)).scalar()

            if not check_bank:
                session.add(Bank(id=bank_id, name=bank_name))
                session.commit()
                print('bank item created')
        session.close()


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
    rate = Column(Numeric(7, 4), index=True)
    date = Column(Date, index=True)
    scraping_date = Column(DateTime, index=True)

    bank_id = Column(Integer, ForeignKey('bank.id'), nullable=False)
    bank = relationship('Bank', backref=backref('rates', lazy=True))

    @staticmethod
    def create(item):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        rate = session.query(ExchangeRate).filter(ExchangeRate.date == item['date'],
                                                  ExchangeRate.bank_id == item['bank_id'],
                                                  ExchangeRate.currency == item['currency'],
                                                  ExchangeRate.type == item['type'],
                                                  ExchangeRate.rate == item['rate']).first()
        if rate:
            rate.scraping_date = item['scraping_date']
            session.add(rate)
        else:
            temp = ExchangeRate(**item)
            session.add(temp)

        session.commit()
        session.close()


def db_connect():
    return create_engine(URL(**settings.DATABASE), client_encoding='utf8', encoding='utf8', echo=False)


def create_tables():
    engine = db_connect()
    DeclarativeBase.metadata.create_all(engine)