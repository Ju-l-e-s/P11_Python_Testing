import server
from tests.conftest import decoded_response


def test_page_contains_form_initial_data(client, mocker, mock_clubs, mock_competitions):
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    mock_name = mock_clubs[0]["name"]
    mock_competition = mock_competitions[0]["name"]
    mock_places_available = mock_competitions[0]["numberOfPlaces"]

    response = client.get(f"/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}")
    assert response.status_code == 200

    assert mock_competition in decoded_response(response)
    assert mock_name in decoded_response(response)
    assert mock_places_available in decoded_response(response)

def test_page_does_not_contain_form_initial_data(client, mocker, mock_clubs, mock_competitions):
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.get(f"/book/something/somethingelse")
    assert response.status_code == 200
    assert "Something went wrong-please try again" in decoded_response(response)