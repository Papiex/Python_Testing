from urllib import response
from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task()
    def index(self):
        response = self.client.get('')
    

    @task()
    def display_board(self):
        response = self.client.get('display_board')
    

    @task()
    def show_summary(self):
        response = self.client.post('show_summary', data = {"email": "john@simplylift.co"})
    

    @task()
    def booking(self):
        response = self.client.get('book/Spring Festival/Simply Lift')
    

    @task()
    def purchase_places(self):
        response = self.client.post('purchase_places', data = {
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": 1
        })
    

    @task()
    def logout(self):
        self.client.get('logout')