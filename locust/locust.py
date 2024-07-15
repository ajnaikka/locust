from locust import HttpUser, TaskSet, task, between

import odoorpc
from datetime import datetime
import random
import string


def random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class UserBehavior(TaskSet):
    @task(1)
    def perform_odoo_operations(self):
        self.client.get("http://ecs-lb-1919862548.ap-south-1.elb.amazonaws.com", timeout=60)  # Replace with your task's endpoint


        # Prepare the connection to the server
        odoo = odoorpc.ODOO('ecs-lb-1919862548.ap-south-1.elb.amazonaws.com', port=80,timeout=60)

        # Check available databases
        print(odoo.db.list())

        # Login
        odoo.login('test', 'test', 'test')

        # Current user
        user = odoo.env.user
        print(user.name)            # name of the user connected
        print(user.company_id.name) # the name of its company

        # Simple 'raw' query
        user_data = odoo.execute('res.users', 'read', [user.id])
        print(user_data)
       
        # hr_employee = odoo.env['hr.employee']
        # new_employee = hr_employee.create({'name': 'loyal'})
        # new_employee_get = hr_employee.browse(new_employee)
        # print("New employee created:", new_employee)


        # # Convert the datetime to a string in the appropriate format
        # check_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')



        # hr_attendance = odoo.env ['hr.attendance']
        # attendance = hr_attendance.create({
        #     'check_in':check_in_time,
        #     'employee_id':new_employee_get.id    
            
        #     })
        # print("attendance added:", attendance)



    @task(2)
    def create_employees_and_attendance(self):


        odoo = odoorpc.ODOO('ecs-lb-1919862548.ap-south-1.elb.amazonaws.com', port=80, timeout=60)
        odoo.login('test', 'test', 'test')

        # Create 1000 employees and add attendance for each
        hr_employee = odoo.env['hr.employee']
        hr_attendance = odoo.env['hr.attendance']

        for _ in range(3):
            # Create a new employee
            employee_name = random_string()
            # employee_name = str(i)
            new_employee = hr_employee.create({'name': employee_name,'work_phone':'9944094386','work_email':'test@loyalitsolutions.com'})
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

    @task(3)
    def list_all_employees(self):
        # Prepare the connection to the server
        odoo = odoorpc.ODOO('ecs-lb-1919862548.ap-south-1.elb.amazonaws.com', port=80, timeout=60)
        odoo.login('test', 'test', 'test')

        hr_employee = odoo.env['hr.employee']

        # List all employees
        employee_ids = hr_employee.search([])
        employees = hr_employee.read(employee_ids, ['name'])
        for emp in employees:
            print(f"Employee ID: {emp['id']}, Employee Name: {emp['name']}")
        

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 10)
