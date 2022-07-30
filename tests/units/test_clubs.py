def test_should_purchase_place(client):
    """Test buying basic reservations"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 10
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_should_not_enought_club_points(client):
    """Test buy more places than available club points"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 20
    })
    assert response.status_code == 200
    assert b'You cannot use more points then you have !' in response.data


def test_should_not_enought_competition_points(client):
    """Test buy more places than available"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 12
    })
    assert response.status_code == 200
    assert b'This competition does not have enough places' in response.data
