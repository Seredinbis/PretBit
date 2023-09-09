from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('postgresql+psycopg2://antonseredin:1111@localhost/theatre', echo=True, future=True)
engine.connect()
session = Session(bind=engine)

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(40), nullable=True)
    middle_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=False)
    birthday = Column(DateTime(), nullable=True)
    position_id = Column(Integer(), ForeignKey('positions.id'), nullable=False)


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(40), nullable=False)
    employees_id = Column(Integer(), ForeignKey('employees.id'))


class Perfomance(Base):
    __tablename__ = 'perfomances'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    genre = Column(String(10), nullable=False)
    date = Column(DateTime(), nullable=True)
    employees_id = Column(Integer(), ForeignKey('employees.id'))

# создание таблиц
# Base.metadata.create_all(engine)
