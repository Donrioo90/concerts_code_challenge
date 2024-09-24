# tests/test_models.py
import unittest
from app import SessionLocal, engine
from models import Base, Band, Venue, Concert

class TestConcertModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.session = SessionLocal()

    def setUp(self):
        self.session.query(Concert).delete()
        self.session.query(Band).delete()
        self.session.query(Venue).delete()
        self.session.commit()

    def test_concert_relationships(self):
        band = Band(name="The Rolling Stones", hometown="London")
        venue = Venue(title="O2 Arena", city="London")
        concert = Concert(band=band, venue=venue, date="2024-10-10")
        self.session.add_all([band, venue, concert])
        self.session.commit()

        # Check concert relationships
        self.assertEqual(concert.band(), band)
        self.assertEqual(concert.venue(), venue)

    def test_band_venues(self):
        band = Band(name="The Beatles", hometown="Liverpool")
        venue = Venue(title="Anfield", city="Liverpool")
        concert = Concert(band=band, venue=venue, date="2024-12-12")
        self.session.add_all([band, venue, concert])
        self.session.commit()

        self.assertIn(venue, band.venues())

    def test_concert_introduction(self):
        band = Band(name="Coldplay", hometown="London")
        venue = Venue(title="Wembley Stadium", city="London")
        concert = Concert(band=band, venue=venue, date="2024-11-11")
        self.session.add_all([band, venue, concert])
        self.session.commit()

        intro = concert.introduction()
        self.assertEqual(intro, "Hello London!!!!! We are Coldplay and we're from London")

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
