import os

from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import Session, declarative_base
from config_data.config import load_config

__abspath = os.path.abspath('.env')
__config = load_config(__abspath)
sql_url: str = __config.sql_url.token

engine = create_engine(sql_url, future=True)
engine.connect()
session = Session(bind=engine)

Base = declarative_base()
meta_data = MetaData()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer(), primary_key=True)
    last_name = Column(String(40), nullable=False)
    first_name = Column(String(40), nullable=True)
    middle_name = Column(String(40), nullable=True)
    birthday = Column(DateTime(), nullable=True)


class WorkTime(Base):
    __tablename__ = 'worktime'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    month_id = Column(Integer(), nullable=True)
    month = Column(String(10), nullable=False)
    time = Column(String(10), nullable=True)
    employee_id = Column(Integer(), ForeignKey('employees.id'))


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
