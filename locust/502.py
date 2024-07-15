from locust import HttpUser, TaskSet, task, between
import odoorpc
from datetime import datetime
import random
import string
import time

def random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class UserBehavior(TaskSet):
    def on_start(self):
        """Setup code to run before any task is scheduled"""
        self.odoo = odoorpc.ODOO('ecs-lb-1919862548.ap-south-1.elb.amazonaws.com', port=80, timeout=600)
        self.odoo.login('test', 'test', 'test')

    @task(1)
    def perform_odoo_operations(self):
        # Perform a GET request to the specified endpoint
        self.client.get("http://ecs-lb-1919862548.ap-south-1.elb.amazonaws.com", timeout=600)  # Replace with your task's endpoint

        # Check available databases
        print(self.odoo.db.list())

        # Current user
        user = self.odoo.env.user
        print(user.name)            # name of the user connected
        print(user.company_id.name) # the name of its company

        # Simple 'raw' query
        user_data = self.odoo.execute('res.users', 'read', [user.id])
        print(user_data)

    @task(2)
    def create_employees_and_attendance(self):
        hr_employee = self.odoo.env['hr.employee']
        hr_attendance = self.odoo.env['hr.attendance']

        for _ in range(1):
            # Create a new employee with a random name
            employee_name = random_string()
            new_employee = hr_employee.create({'name': employee_name})
            new_employee_get = hr_employee.browse(new_employee)
            print(f"New employee created: {new_employee_get.name}")

            # Convert the datetime to a string in the appropriate format
            check_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Add an attendance record for the new employee
            attendance = hr_attendance.create({
                'check_in': check_in_time,
                'employee_id': new_employee_get.id
            })
            print(f"Attendance added for employee {new_employee_get.name}: {attendance}")

    # @task(3)
    # def list_latest_employees(self, count=1):
    #     hr_employee = self.odoo.env['hr.employee']

    #     # Get the latest employees based on ID descending order
    #     employee_ids = hr_employee.search([], order='id desc', limit=count)
    #     employees = hr_employee.read(employee_ids, ['name'])
    #     for emp in employees:
    #         print(f"Employee ID: {emp['id']}, Employee Name: {emp['name']}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(10, 15)
