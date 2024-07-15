from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def my_task(self):
        self.client.get("http://ecs-lb-1919862548.ap-south-1.elb.amazonaws.com/web/login")  # Replace with your task's endpoint

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
