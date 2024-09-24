from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import Base

class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='band')

    def concerts(self):
        return self.concerts

    def venues(self):
        return {concert.venue for concert in self.concerts}

    def play_in_venue(self, venue, date):
        concert = Concert(band_id=self.id, venue_id=venue.id, date=date)
        return concert

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        return session.query(cls).join(Concert).group_by(cls.id).order_by(func.count(Concert.id).desc()).first()

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='venue')

    def concerts(self):
        return self.concerts

    def bands(self):
        return {concert.band for concert in self.concerts}

    def concert_on(self, date):
        return next((concert for concert in self.concerts if concert.date == date), None)

    def most_frequent_band(self):
        return max(set(self.bands()), key=lambda band: len([concert for concert in self.concerts if concert.band == band]))
