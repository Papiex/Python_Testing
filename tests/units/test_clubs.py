import datetime


def test_should_less_than_actual_date(past_competition):
    """test if a false competition date is less than the actual date"""
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert past_competition['date'] < actual_date


def test_should_greater_than_actual_date(to_come_competition):
    """test if a false competition date is greater than the actual date"""
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert to_come_competition['date'] > actual_date


def test_should_buy_actual_competition(client):
    """test for taking places in actual competition"""
    response = client.post('/showSummary', data = {"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b'The competition Future Competition is already passed' not in response.data


def test_should_not_buy_past_competition(client):
    """test for taking places in past competition"""
    response = client.post('/showSummary', data = {"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b'The competition Past Competition is already passed' in response.data

