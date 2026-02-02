from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_user(self):
        # Assumes WireMock is running and has this mapping
        # In a real scenario, this would hit the actual Backend
        self.client.get("/api/users/101")

    @task(3)
    def health_check(self):
        self.client.get("/__admin")  # WireMock Admin as health check
