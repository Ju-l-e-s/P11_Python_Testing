import server

def test_points_board_accessible(client, mocker, mock_clubs,decoded_response):
    mocker.patch.object(server, "clubs", mock_clubs)

    response = client.get("/points")
    assert response.status_code == 200

    for club in mock_clubs:
        assert club["name"] in decoded_response(response)
        assert club["points"] in decoded_response(response)