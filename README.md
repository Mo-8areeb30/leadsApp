# leadsApp
- A python flask application as a backend to a leads retrieval app.

Endpoints: 

- /leads that 
POST receives {name, email, phone, business} and sends an email to commercial team telling them these details and inserts this data into database
GET retrieve all leads from the database and returns them

- GET /leads/<id> retrieves individual lead from the database. 

You do not need to create a database or have an SQL connection. I just want the sql query string as an example function that just prints the sql instead of actually running the sql.
