# Event Management System - Postman API Endpoints Guide
Base URL: `http://127.0.0.1:8000`

# ------------------------
# 1. Authentication Endpoints
# ------------------------

# 1.1 Get JWT Token
Endpoint: `POST /api/auth/token/`

Headers:
Content-Type: application/json

Body (raw JSON):
{
    "username": "admin",
    "password": "admin"
}

Example Response (200 OK):
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

# 1.2 Refresh JWT Token
Endpoint: `POST /api/auth/token/refresh/`

Headers:
Content-Type: application/json

Body (raw JSON):
{
    "refresh": "your_refresh_token_here"
}

Example Response (200 OK):
{
    "access": "new_access_token_here"
}

# ------------------------
# 2. Events Endpoints
# ------------------------

# 2.1 List All Events (Public)
Endpoint: `GET /api/events/`

Headers:
Content-Type: application/json

Query Parameters (optional):
- `page`: Page number for pagination
- `search`: Search in title, description, location
- `is_public`: Filter by public/private (true/false)
- `organizer`: Filter by organizer ID
- `ordering`: Order by field (-created_at, start_time, etc.)

Example:
GET /api/events/?search=concert&is_public=true&ordering=-start_time

Example Response (200 OK):
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Music Concert",
            "description": "Annual music festival",
            "organizer": {
                "id": 1,
                "username": "tom",
                "email": "tom@gmail.com",
                "first_name": "",
                "last_name": ""
            },
            "location": "Central Park",
            "start_time": "2025-01-15T18:00:00Z",
            "end_time": "2025-01-15T22:00:00Z",
            "is_public": true,
            "created_at": "2025-01-10T10:00:00Z",
            "updated_at": "2025-01-10T10:00:00Z",
            "rsvp_count": 15,
            "average_rating": 4.5
        }
    ]
}

# 2.2 Create New Event
Endpoint: `POST /api/events/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "title": "Tech Conference 2025",
    "description": "Annual technology conference featuring latest innovations",
    "location": "Convention Center, New York",
    "start_time": "2025-02-20T09:00:00Z",
    "end_time": "2025-02-20T17:00:00Z",
    "is_public": true
}

Example Response (201 Created):
{
    "id": 2,
    "title": "Tech Conference 2025",
    "description": "Annual technology conference featuring latest innovations",
    "organizer": {
        "id": 1,
        "username": "tom",
        "email": "tom@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "location": "Convention Center, New York",
    "start_time": "2025-02-20T09:00:00Z",
    "end_time": "2025-02-20T17:00:00Z",
    "is_public": true,
    "created_at": "2025-01-12T14:30:00Z",
    "updated_at": "2025-01-12T14:30:00Z",
    "rsvp_count": 0,
    "average_rating": 0
}

# 2.3 Get Event Details
Endpoint: `GET /api/events/{id}/`

Example: `GET /api/events/1/`

Headers:
Content-Type: application/json

Example Response (200 OK):
{
    "id": 1,
    "title": "Music Concert",
    "description": "Annual music festival",
    "organizer": {
        "id": 1,
        "username": "tom",
        "email": "tom@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "location": "Central Park",
    "start_time": "2025-01-15T18:00:00Z",
    "end_time": "2025-01-15T22:00:00Z",
    "is_public": true,
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-10T10:00:00Z",
    "rsvp_count": 15,
    "average_rating": 4.5
}

# 2.4 Update Event
Endpoint: `PUT /api/events/{id}/`

Example: `PUT /api/events/1/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "title": "Updated Music Concert",
    "description": "Annual music festival with special guests",
    "location": "Central Park Amphitheater",
    "start_time": "2025-01-15T19:00:00Z",
    "end_time": "2025-01-15T23:00:00Z",
    "is_public": true
}

Example Response (200 OK):
{
    "id": 1,
    "title": "Updated Music Concert",
    "description": "Annual music festival with special guests",
    "organizer": {
        "id": 1,
        "username": "tom",
        "email": "tom@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "location": "Central Park Amphitheater",
    "start_time": "2025-01-15T19:00:00Z",
    "end_time": "2025-01-15T23:00:00Z",
    "is_public": true,
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-12T15:00:00Z",
    "rsvp_count": 15,
    "average_rating": 4.5
}

# 2.5 Delete Event
Endpoint: `DELETE /api/events/{id}/`

Example: `DELETE /api/events/1/`

Headers:
Authorization: Bearer <your_access_token>
Response: 204 No Content

# 2.6 RSVP to Event
Endpoint: `POST /api/events/{id}/rsvp/`

Example: `POST /api/events/1/rsvp/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "status": "Going"
}

Available Status Values: "Going", "Maybe", "Not Going"

Example Response (200 OK):
{
    "id": 1,
    "event": {
        "id": 1,
        "title": "Music Concert",
        "description": "Annual music festival",
        "organizer": {
            "id": 1,
            "username": "tom",
            "email": "tom@gmail.com",
            "first_name": "",
            "last_name": ""
        },
        "location": "Central Park",
        "start_time": "2025-01-15T18:00:00Z",
        "end_time": "2025-01-15T22:00:00Z",
        "is_public": true,
        "created_at": "2025-01-10T10:00:00Z",
        "updated_at": "2025-01-10T10:00:00Z",
        "rsvp_count": 16,
        "average_rating": 4.5
    },
    "user": {
        "id": 2,
        "username": "jerry",
        "email": "jerry@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "status": "Going",
    "created_at": "2025-01-12T16:00:00Z",
    "updated_at": "2025-01-12T16:00:00Z"
}

# 2.7 Get Event Reviews
Endpoint: `GET /api/events/{id}/reviews/`

Example: `GET /api/events/1/reviews/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Example Response (200 OK):
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "event": 1,
            "user": {
                "id": 2,
                "username": "jerry",
                "email": "jerry@gmail.com",
                "first_name": "",
                "last_name": ""
            },
            "rating": 5,
            "comment": "Amazing event! Great organization.",
            "created_at": "2025-01-11T10:00:00Z",
            "updated_at": "2025-01-11T10:00:00Z"
        },
        {
            "id": 2,
            "event": 1,
            "user": {
                "id": 3,
                "username": "bob_wilson",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Wilson"
            },
            "rating": 4,
            "comment": "Good event, but could use better sound system.",
            "created_at": "2025-01-12T11:00:00Z",
            "updated_at": "2025-01-12T11:00:00Z"
        }
    ]
}

# ------------------------
# 3. RSVP Endpoints
# ------------------------

# 3.1 Get User's RSVPs
Endpoint: `GET /api/rsvps/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Example Response (200 OK):
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "event": {
                "id": 1,
                "title": "Music Concert",
                "description": "Annual music festival",
                "organizer": {
                    "id": 1,
                    "username": "tom",
                    "email": "tom@gmail.com",
                    "first_name": "",
                    "last_name": ""
                },
                "location": "Central Park",
                "start_time": "2025-01-15T18:00:00Z",
                "end_time": "2025-01-15T22:00:00Z",
                "is_public": true,
                "created_at": "2025-01-10T10:00:00Z",
                "updated_at": "2025-01-10T10:00:00Z",
                "rsvp_count": 16,
                "average_rating": 4.5
            },
            "user": {
                "id": 2,
                "username": "jerry",
                "email": "jerry@gmail.com",
                "first_name": "",
                "last_name": ""
            },
            "status": "Going",
            "created_at": "2025-01-12T16:00:00Z",
            "updated_at": "2025-01-12T16:00:00Z"
        }
    ]
}

# 3.2 Create RSVP
Endpoint: `POST /api/rsvps/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "event": 1,
    "status": "Maybe"
}

Example Response (201 Created):
{
    "id": 2,
    "event": {
        "id": 1,
        "title": "Music Concert",
        "description": "Annual music festival",
        "organizer": {
            "id": 1,
            "username": "tom",
            "email": "tom@gmail.com",
            "first_name": "",
            "last_name": ""
        },
        "location": "Central Park",
        "start_time": "2025-01-15T18:00:00Z",
        "end_time": "2025-01-15T22:00:00Z",
        "is_public": true,
        "created_at": "2025-01-10T10:00:00Z",
        "updated_at": "2025-01-10T10:00:00Z",
        "rsvp_count": 17,
        "average_rating": 4.5
    },
    "user": {
        "id": 2,
        "username": "jerry",
        "email": "jerry@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "status": "Maybe",
    "created_at": "2025-01-12T17:00:00Z",
    "updated_at": "2025-01-12T17:00:00Z"
}

# 3.3 Update RSVP
Endpoint: `PUT /api/rsvps/{id}/`

Example: `PUT /api/rsvps/1/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "status": "Not Going"
}

Example Response (200 OK):
{
    "id": 1,
    "event": {
        "id": 1,
        "title": "Music Concert",
        "description": "Annual music festival",
        "organizer": {
            "id": 1,
            "username": "tom",
            "email": "tom@gmail.com",
            "first_name": "",
            "last_name": ""
        },
        "location": "Central Park",
        "start_time": "2025-01-15T18:00:00Z",
        "end_time": "2025-01-15T22:00:00Z",
        "is_public": true,
        "created_at": "2025-01-10T10:00:00Z",
        "updated_at": "2025-01-10T10:00:00Z",
        "rsvp_count": 16,
        "average_rating": 4.5
    },
    "user": {
        "id": 2,
        "username": "jerry",
        "email": "jerry@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "status": "Not Going",
    "created_at": "2025-01-12T16:00:00Z",
    "updated_at": "2025-01-12T18:00:00Z"
}

# ------------------------
# 4. Reviews Endpoints
# ------------------------

# 4.1 Get User's Reviews
Endpoint: `GET /api/reviews/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Example Response (200 OK):
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "event": 1,
            "user": {
                "id": 2,
                "username": "jerry",
                "email": "jerry@gmail.com",
                "first_name": "",
                "last_name": ""
            },
            "rating": 5,
            "comment": "Amazing event! Great organization.",
            "created_at": "2025-01-11T10:00:00Z",
            "updated_at": "2025-01-11T10:00:00Z"
        }
    ]
}

# 4.2 Create Review
Endpoint: `POST /api/reviews/`

Headers:
Content-Type: application/json
Authorization: Bearer <your_access_token>

Body (raw JSON):
{
    "event": 1,
    "rating": 4,
    "comment": "Great event overall, but the food could be better."
}

Example Response (201 Created):
{
    "id": 3,
    "event": 1,
    "user": {
        "id": 2,
        "username": "jerry",
        "email": "jerry@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "rating": 4,
    "comment": "Great event overall, but the food could be better.",
    "created_at": "2025-01-12T19:00:00Z",
    "updated_at": "2025-01-12T19:00:00Z"
}