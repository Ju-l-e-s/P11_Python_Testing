import pytest
from server import app
import html
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        },
        {
            "name": "test",
            "email": "valid@gmail.fr",
            "points": "12"
        }
    ]

@pytest.fixture
def mock_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]

@pytest.fixture
def decoded_response():
    def decode(response):
       return html.unescape(response.data.decode("utf-8"))
    return decode