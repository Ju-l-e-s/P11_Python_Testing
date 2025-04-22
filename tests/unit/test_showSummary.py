import server
from tests.conftest import client, mock_clubs, mock_competitions, decoded_response
from datetime import datetime, timedelta

def test_show_summary_valid_email(client, mocker, mock_clubs, mock_competitions):
    # Mock
    mocker.patch("server.loadClubs", return_value=mock_clubs)
    mocker.patch("server.loadCompetitions", return_value=mock_competitions)
    # POST request to /showSummary with a valid email
    response = client.post('/showSummary', data={"email": "john@simplylift.co"})

    assert response.status_code == 200
    assert b"You were successfully logged in" in response.data
    assert b"Spring Festival" in response.data


def test_show_summary_invalid_email(client, mocker, mock_clubs):
    # Mock
    mocker.patch("server.loadClubs", return_value=mock_clubs)

    # POST request to /showSummary with an invalid email
    response = client.post('/showSummary', data={"email": "invalid@email.com"})

    assert response.status_code == 200
    assert b"Invalid email" in response.data

def test_past_competition_not_displayed_for_booking(client, mocker, mock_clubs):

    mocker.patch.object(server, "clubs", mock_clubs)

    competitions = [
        {
            "name": "Old Competition",
            "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "10"
        },
        {
            "name": "Future Competition",
            "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "10"
        }
    ]

    mocker.patch.object(server, "competitions", competitions)

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    print(decoded_response(response))
    assert "Old Competition" in decoded_response(response)
    assert "Book Places" in decoded_response(response)  # only for Future Competition
    assert decoded_response(response).count("Book Places") == 1
