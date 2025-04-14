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
    assert updated_club["points"] == 1