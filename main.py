import random
import string
from datetime import datetime
from typing import Optional, List

from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr

from database import get_connection, init_db



app = FastAPI(title="Customer Support CRM API")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"


# -------------------------------------------------------------------
# Startup: ensure DB/table exist
# -------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()


# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------
class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: Optional[str] = None


class TicketStatusUpdate(BaseModel):
    status: str


class TicketOut(BaseModel):
    id: int
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: Optional[str]
    status: str
    created_at: str


class TicketCreateResponse(BaseModel):
    ticket_id: str


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
ALLOWED_STATUSES = {"Open", "In Progress", "Closed"}


def generate_ticket_id(conn) -> str:
    """
    Generates a unique ticket_id in the format TKT-<number>.
    Uses a random 3-6 digit number and retries on collision.
    """
    while True:
        candidate = f"TKT-{random.randint(100, 999999)}"
        existing = conn.execute(
            "SELECT 1 FROM tickets WHERE ticket_id = ?", (candidate,)
        ).fetchone()
        if not existing:
            return candidate


def row_to_dict(row) -> dict:
    return dict(row) if row else None


# -------------------------------------------------------------------
# 1. Create a ticket
# -------------------------------------------------------------------
@app.post("/api/tickets", response_model=TicketCreateResponse, status_code=201)
def create_ticket(payload: TicketCreate):
    with get_connection() as conn:
        ticket_id = generate_ticket_id(conn)

        conn.execute(
            """
            INSERT INTO tickets
                (ticket_id, customer_name, customer_email, subject, description, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                payload.customer_name,
                payload.customer_email,
                payload.subject,
                payload.description,
                "Open",
            ),
        )

    return TicketCreateResponse(ticket_id=ticket_id)


# -------------------------------------------------------------------
# 2. List all tickets (with optional filters)
# -------------------------------------------------------------------
@app.get("/api/tickets", response_model=List[TicketOut])
def list_tickets(
    status: Optional[str] = Query(None, description="Filter by exact status"),
    customer_name: Optional[str] = Query(None, description="Search by customer name (partial match)"),
):
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if customer_name:
        query += " AND customer_name LIKE ?"
        params.append(f"%{customer_name}%")

    query += " ORDER BY created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [row_to_dict(r) for r in rows]


# -------------------------------------------------------------------
# 3. Get single ticket
# -------------------------------------------------------------------
@app.get("/api/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found")

    return row_to_dict(row)


# -------------------------------------------------------------------
# 4. Update ticket status
# -------------------------------------------------------------------
@app.put("/api/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket_status(ticket_id: str, payload: TicketStatusUpdate):
    if payload.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(ALLOWED_STATUSES)}",
        )

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()

        if not existing:
            raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found")

        conn.execute(
            "UPDATE tickets SET status = ? WHERE ticket_id = ?",
            (payload.status, ticket_id),
        )

        row = conn.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()

    return row_to_dict(row)


# -------------------------------------------------------------------
# 5. Serve Frontend Dashboard (Always keep this at the very bottom)
# -------------------------------------------------------------------
@app.get("/")
def serve_frontend():
    if not TEMPLATE_PATH.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Could not find index.html at expected location: {TEMPLATE_PATH}"
        )
    return FileResponse(TEMPLATE_PATH)