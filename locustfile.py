from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def list_competitions(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": "1"
        })
