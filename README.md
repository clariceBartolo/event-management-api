Event Management API

This project is a RESTful API for managing events, attendees, venues, ticket bookings, and multimedia assets. It is built using Python, FastAPI, and MongoDB Atlas, and is publicly hosted for external access.

Project Features

CRUD operations for:
Events
Attendees
Venues
Ticket bookings

Uploading multimedia files:
Event posters (images)
Promotional videos
Venue photos

Secure MongoDB Atlas connection
Input validation and sanitisation to prevent injection attacks
Hosted API with Swagger documentation

Environment Setup

1. Clone the Repository
   git clone https://github.com/clariceBartolo/event-management-api
   cd event-management-api

2. Create a Virtual Environment
   python3 -m venv .venv
   source .venv/bin/activate # for macOS

3. Install Dependencies
   pip install -r requirements.txt

4. Environment Variables

Create a .env file in the root directory:

MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/event_management_db

Important:
The .env file is added to .gitignore to prevent database credentials from being pushed to GitHub.

Project Structure
event-management-api/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── vercel.json

Running the API Locally
uvicorn main:app --reload

Local URL:
http://127.0.0.1:8000/docs

Swagger UI is used to test all endpoints and file uploads.

Hosted API

Public API URL:
https://event-management-aratv01zn-claricebartolos-projects.vercel.app/docs

API Endpoints

Events
POST /events
GET /events
GET /events/{event_id}
PUT /events/{event_id}
DELETE /events/{event_id}

Attendees
POST /attendees
GET /attendees
GET /attendees/{attendee_id}
PUT /attendees/{attendee_id}
DELETE /attendees/{attendee_id}

Venues
POST /venues
GET /venues
GET /venues/{venue_id}
PUT /venues/{venue_id}
DELETE /venues/{venue_id}

Bookings
POST /bookings
GET /bookings
GET /bookings/{booking_id}
PUT /bookings/{booking_id}
DELETE /bookings/{booking_id}

File Uploads
POST /upload_event_poster/{event_id}
POST /upload_promo_video/{event_id}
POST /upload_venue_photo/{venue_id}

Database Security Measures

Secure Credentials: MongoDB credentials are stored in environment variables

IP Whitelisting: MongoDB Atlas access is restricted to trusted IP addresses

Injection Prevention: Pydantic models validate and sanitise all user input

Git Usage

Git repository used with regular commits

.env, .venv, and cache files are excluded using .gitignore

Public GitHub repository provided as proof of individual work

Tools Used
Python 3.13
FastAPI
Uvicorn
Pydantic
MongoDB Atlas
Vercel
Datagrip

Author
Clarice Bartolo
ITMSD‑506‑2301 | Database Essentials
