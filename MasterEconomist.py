import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
from IPython import display
load_dotenv()
import json
import enum


import sys

from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, DateTime, Boolean, ARRAY, DATE, FLOAT, Enum
from sqlalchemy import select, insert, within_group
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Denominations(enum.Enum):
    k = 1
    m = 2
    b = 3

class RealGDP(Base):
    __tablename__ = "real_gdp"
    id = Column(Integer, primary_key=True)
    date = Column(DATE)
    currency = Column(String(3))
    value = Column(FLOAT)
    unit = Column(Enum(Denominations))
    interval = Column(String(1))

class Treasury_Yield(Base):
    __tablename__ = "sov_yc"
    id = Column(Integer, primary_key=True)
    maturity = Column(String(10))
    date = Column(DATE)
    rate = Column(FLOAT)
    currency = Column(String(3))