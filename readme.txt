Domain Name: https://sc20osc.pythonanywhere.com/

Admin Credentials {
    [
        "username": "admin",
        "password": "admin"
    ],
    [
        "username": "ammar",
        "password": "ammar"
    ]
}

To use the service as an admin, you may access the admin functions using https://sc20osc.pythonanywhere.com/admin/ using the provided admin credentials. This will allow you to access and modify the database. Note that this will automatically make the changes on other impacted services also.

To use the service with its API functionality, see the provided swagger.pdf file for information on each endpoint including its method, request and response formats. The two provided endpoints (not including all the different implemented methods) are;

- https://sc20osc.pythonanywhere.com/api/flights/ (this supports GET, PUT, PATCH and DELETE)
- https://sc20osc.pythonanywhere.com/api/bookings (this supports GET, PUT, PATCH and DELETE)
