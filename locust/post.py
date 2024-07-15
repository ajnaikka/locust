from locust import HttpUser, TaskSet, task, between
from bs4 import BeautifulSoup

class UserBehavior(TaskSet):

    def on_start(self):
        """
        This method is called when a Locust user starts before any task is scheduled.
        It's a good place to add the login functionality.
        """
        self.login()

    def login(self):
        """
        Login to the Odoo application to obtain authentication.
        """
        # Step 1: Get the CSRF token and session cookie from the login page
        response = self.client.get("/web/login")
        
        # Extract the CSRF token from the response using BeautifulSoup
        csrf_token = self.extract_csrf_token(response.text)
        
        # Extract the session cookie from the response
        session_cookie = response.cookies
        
        # Step 2: Use the CSRF token and session cookie in the login request
        response = self.client.post("/web/login", data={
            "login": "test",      # replace with your username
            "password": "tesf",   # replace with your password
            "csrf_token": csrf_token  # include the CSRF token
        }, cookies=session_cookie)
        
        # Print the response content for debugging
        print("Login response status code:", response.status_code)
        print("Login response content:", response.text)
        
        # Check for successful login
        if response.status_code == 200 and "Your session expired" not in response.text:
            print("Login successful")
        else:
            print("Login failed")

    def extract_csrf_token(self, html):
        """
        Extract the CSRF token from the HTML of the login page.
        """
        soup = BeautifulSoup(html, 'html.parser')
        token = soup.find('input', {'name': 'csrf_token'})
        if token:
            return token['value']
        else:
            raise ValueError("CSRF token not found")

    @task(1)
    def get_request(self):
        self.client.get("http://ecs-lb-1919862548.ap-south-1.elb.amazonaws.com")

    # @task(2)
    # def post_request(self):
    #     """
    #     Example of a POST request.
    #     Modify the endpoint and payload according to your application's requirements.
    #     """
    #     response = self.client.post("/some_post_endpoint", json={
    #         "key1": "value1",
    #         "key2": "value2"
    #     }, headers={"Authorization": f"Bearer {self.token}"})
    #     print(response.status_code)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
