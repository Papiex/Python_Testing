from urllib import response


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


def test_should_deduct_competition_points(client):
    """Test for deduct 2 points of Test Competition"""
    data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 2
    }

    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert b'''Number of Places: 6\n            \n                
    <a href="/book/Test%20Competition/Simply%20Lift">' in response.data'''


def test_should_deduct_club_points(client, capsys):
    """Test for deduct 2 points of Simply Lift club """
    data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 2
    }

    response = client.post('/purchasePlaces', data=data)
    with capsys.disabled():
        print(response.data)
    assert response.status_code == 200
    assert b'Points available: 11' in response.data
