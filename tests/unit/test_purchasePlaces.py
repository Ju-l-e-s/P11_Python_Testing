import pytest

import server
from tests.conftest import mock_clubs, mock_competitions, decoded_response

def test_booking_more_than_available_points(client, mocker, mock_clubs, mock_competitions,decoded_response):
    # mocks
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    # Iron Temple has 4 points, we try to book 5 places
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "5"
        }
    )

    assert response.status_code == 400
    assert "You don't have enough points" in decoded_response(response)

def test_booking_less_than_available_points(client, mocker, mock_clubs, mock_competitions, decoded_response):
    # mocks
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    # Iron Temple has 4 points, we try to book 3 places
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "3"
        }
    )

    assert response.status_code == 200
    assert "Great-booking complete!" in decoded_response(response)

    # check if club points have been updated
    updated_club = next(c for c in mock_clubs if c["name"] == "Iron Temple")
    assert updated_club["points"] == "1"

def test_booking_more_than_12_places(client, mocker, mock_clubs, mock_competitions,decoded_response):
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "13"
        }
    )

    assert response.status_code == 400
    assert "You can't book more than 12 places" in decoded_response(response)

def test_booking_maximum_12_places(client, mocker, mock_clubs, mock_competitions, decoded_response):
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "12"
        }
    )

    assert response.status_code == 200
    assert "Great-booking complete!" in decoded_response(response)

    updated_club = next(c for c in mock_clubs if c["name"] == "Simply Lift")
    assert updated_club["points"] == "1"  # 13 - 12 = 1



def test_booking_past_competition(client, mocker, mock_clubs, mock_competitions, decoded_response):
    mocker.patch.object(server, "clubs", mock_clubs)

    # Mock a past competition (date < now)
    past_competitions = [
        {
            "name": "Old Classic",
            "date": "2000-01-01 10:00:00",
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch.object(server, "competitions", past_competitions)

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Old Classic",
            "places": "2"
        }
    )

    assert response.status_code == 400
    assert "You can't book a past competition" in decoded_response(response)

@pytest.mark.parametrize("invalid_places", ["0", "-1", "-134"])
def test_booking_invalid_number_of_places(client, mocker, mock_clubs, mock_competitions, decoded_response, invalid_places):
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": invalid_places
        }
    )

    assert response.status_code == 400
    assert "Number of places must be greater than zero" in decoded_response(response)