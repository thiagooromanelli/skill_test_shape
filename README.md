# FPSO Management - API

### Assignment Objective
Create a backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading).

### Assignment Rules
1. Registering a vessel. The vessel data input is its code, which can’t be repeated (return the HTTP code appropriate and an error
message if the user tries to register an existing code). For instance, a valid input of a vessel is:“code”:“MV102”.

2. Registering a new equipment in a vessel. The data inputs of each equipment are name, code, location and status. Each equipment is
associated to a given vessel and has a unique code, which can’t be repeated (return the HTTP code appropriate and an error message if
the user tries to register a existing code). For each new equipment registered, the equipment status is automatically active. For instance, a
valid input of a new equipment related to a vessel “MV102”is: { "name": "compressor", "code": "5310B9D7", "location": "Brazil" }

3. Setting an equipment’s status to inactive. The input data should be one or a list of equipment code.

4. Returning all active equipment of a vessel Feel free to use the programming language and tools you would like.

5. Add an operation order with a cost to a equipment. For instance, a valid input of a new operation related to a equipment “5310B9D7”
is: {"code": "5310B9D7", type: "replacement", "cost": "10000"}

6. Return the total cost in operation of an equipment by code.

7. Return the total cost in operation of a set of equipments by name.

8. Return the average cost in operation in each vessel.

### Used tecnologies
#### Code
- Python
- Flask
- SQLAlchemy
#### Documentation
- Flasgger - Swagger
#### Database
- PostgreSQL
#### Tests
- Unittest

### Pre-requisites
- Docker
- docker-compose

### Running the application
- Clone the repository
- Inside the main directory run the following command:
    ```
    docker-compose up
    ```
- PostgreSQL will start with database FPSO already created
- The application will start on http://localhost:5000, and will create the tables in database
- The swagger documentation will be available on http://localhost:5000/apidocs