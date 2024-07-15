from locust import User, TaskSet, task, between
import psycopg2

class DatabaseTasks(TaskSet):

    def on_start(self):
        # Establish database connection
        self.connection = psycopg2.connect(
            host='odoo-prod-postgresql-1.clwwsggk6315.ap-south-1.rds.amazonaws.com',
            user='odoo',
            password='oh:zZ3gTYfa702hq',
            dbname='odoo',
            port='5432'
        )
        self.cursor = self.connection.cursor()

    @task
    def query_database(self):
        # Simple query to fetch data from a table
        query = "SELECT name, email FROM res_partner LIMIT 10;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # Handle the result (for demo, we just print it)
        print(result)

    def on_stop(self):
        # Close database connection
        self.cursor.close()
        self.connection.close()

class DatabaseUser(User):
    tasks = [DatabaseTasks]
    wait_time = between(1, 5)  # Adjust the wait time as needed

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
