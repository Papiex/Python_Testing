import datetime


def test_should_not_buy_past_competition(client, past_competition):
    """test a date with false competition"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert past_competition['date'] < now


def test_should_buy_actual_competition(client, to_come_competition):
    """test a date with false competition"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert to_come_competition['date'] > now

