import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import motor.motor_asyncio
from bson import ObjectId
from bson.errors import InvalidId

# ---------------------------
# Environment
# ---------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# ---------------------------
# App
# ---------------------------
app = FastAPI(title="Event Management API")

# ---------------------------
# Database
# ---------------------------
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.event_management_db

# ---------------------------
# Helpers
# ---------------------------
def obj_to_str(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# ---------------------------
# Root
# ---------------------------
@app.get("/")
async def root():
    return {"message": "API is running!"}

# ---------------------------
# Models (Sanitised & Validated)
# ---------------------------
class Event(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    description: constr(strip_whitespace=True, min_length=1)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # <-- Pydantic v2 uses `pattern`
    venue_id: str
    max_attendees: int = Field(..., gt=0)

class Attendee(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    phone: Optional[constr(strip_whitespace=True, min_length=6)] = None

class Venue(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    address: constr(strip_whitespace=True, min_length=1)
    capacity: int = Field(..., gt=0)

class Booking(BaseModel):
    event_id: str
    attendee_id: str
    ticket_type: constr(strip_whitespace=True, min_length=1)
    quantity: int = Field(..., gt=0)

# ---------------------------
# EVENTS
# ---------------------------
@app.post("/events")
async def create_event(event: Event):
    result = await db.events.insert_one(event.model_dump())
    return {"message": "Event created", "id": str(result.inserted_id)}

@app.get("/events")
async def get_events():
    events = await db.events.find().to_list(100)
    return [obj_to_str(e) for e in events]

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    event = await db.events.find_one({"_id": validate_object_id(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return obj_to_str(event)

@app.put("/events/{event_id}")
async def update_event(event_id: str, event: Event):
    result = await db.events.update_one(
        {"_id": validate_object_id(event_id)},
        {"$set": event.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event updated"}

@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    result = await db.events.delete_one({"_id": validate_object_id(event_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}

# ---------------------------
# ATTENDEES
# ---------------------------
@app.post("/attendees")
async def create_attendee(attendee: Attendee):
    result = await db.attendees.insert_one(attendee.model_dump())
    return {"message": "Attendee created", "id": str(result.inserted_id)}

@app.get("/attendees")
async def get_attendees():
    attendees = await db.attendees.find().to_list(100)
    return [obj_to_str(a) for a in attendees]

@app.get("/attendees/{attendee_id}")
async def get_attendee(attendee_id: str):
    attendee = await db.attendees.find_one({"_id": validate_object_id(attendee_id)})
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return obj_to_str(attendee)

@app.put("/attendees/{attendee_id}")
async def update_attendee(attendee_id: str, attendee: Attendee):
    result = await db.attendees.update_one(
        {"_id": validate_object_id(attendee_id)},
        {"$set": attendee.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return {"message": "Attendee updated"}

@app.delete("/attendees/{attendee_id}")
async def delete_attendee(attendee_id: str):
    result = await db.attendees.delete_one({"_id": validate_object_id(attendee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return {"message": "Attendee deleted"}

# ---------------------------
# VENUES
# ---------------------------
@app.post("/venues")
async def create_venue(venue: Venue):
    result = await db.venues.insert_one(venue.model_dump())
    return {"message": "Venue created", "id": str(result.inserted_id)}

@app.get("/venues")
async def get_venues():
    venues = await db.venues.find().to_list(100)
    return [obj_to_str(v) for v in venues]

@app.get("/venues/{venue_id}")
async def get_venue(venue_id: str):
    venue = await db.venues.find_one({"_id": validate_object_id(venue_id)})
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return obj_to_str(venue)

@app.put("/venues/{venue_id}")
async def update_venue(venue_id: str, venue: Venue):
    result = await db.venues.update_one(
        {"_id": validate_object_id(venue_id)},
        {"$set": venue.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {"message": "Venue updated"}

@app.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str):
    result = await db.venues.delete_one({"_id": validate_object_id(venue_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {"message": "Venue deleted"}

# ---------------------------
# BOOKINGS
# ---------------------------
@app.post("/bookings")
async def create_booking(booking: Booking):
    result = await db.bookings.insert_one(booking.model_dump())
    return {"message": "Booking created", "id": str(result.inserted_id)}

@app.get("/bookings")
async def get_bookings():
    bookings = await db.bookings.find().to_list(100)
    return [obj_to_str(b) for b in bookings]

@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    booking = await db.bookings.find_one({"_id": validate_object_id(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return obj_to_str(booking)

@app.put("/bookings/{booking_id}")
async def update_booking(booking_id: str, booking: Booking):
    result = await db.bookings.update_one(
        {"_id": validate_object_id(booking_id)},
        {"$set": booking.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking updated"}

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: str):
    result = await db.bookings.delete_one({"_id": validate_object_id(booking_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}

# ---------------------------
# FILE UPLOADS
# ---------------------------
@app.post("/upload_event_poster/{event_id}")
async def upload_event_poster(event_id: str, file: UploadFile = File(...)):
    content = await file.read()
    doc = {
        "event_id": event_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.event_posters.insert_one(doc)
    return {"message": "Event poster uploaded", "id": str(result.inserted_id)}

@app.post("/upload_promo_video/{event_id}")
async def upload_promo_video(event_id: str, file: UploadFile = File(...)):
    content = await file.read()
    doc = {
        "event_id": event_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.promo_videos.insert_one(doc)
    return {"message": "Promotional video uploaded", "id": str(result.inserted_id)}

@app.post("/upload_venue_photo/{venue_id}")
async def upload_venue_photo(venue_id: str, file: UploadFile = File(...)):
    content = await file.read()
    doc = {
        "venue_id": venue_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.venue_photos.insert_one(doc)
    return {"message": "Venue photo uploaded", "id": str(result.inserted_id)}
