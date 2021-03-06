from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class Zone(db.Model):
    tablename = "zone"
    id = Column(Integer, primary_key=True)
    zone_code = Column(String(100), unique=True)
    name = Column(String(50), unique=True)
    color = Column(String(50))
    state = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    coordinates = relationship("ZoneCoordinate", back_populates="point")

    def as_dict(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
