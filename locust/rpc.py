import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('ecs-lb-1919862548.ap-south-1.elb.amazonaws.com', port=80)

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