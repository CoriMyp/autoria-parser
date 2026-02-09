from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Date,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_id = Column(BigInteger, unique=True, index=True, nullable=False)
    url = Column(Text)
    title = Column(String(512))
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String(255))
    phone_number = Column(BigInteger)
    image_url = Column(Text)
    images_count = Column(Integer)
    car_number = Column(String(128))
    car_vin = Column(String(128))
    datetime_found = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
