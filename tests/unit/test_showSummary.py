from tests.conftest import client, mock_clubs, mock_competitions

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

    assert response.status_code == 401
    assert b"Invalid email" in response.data
