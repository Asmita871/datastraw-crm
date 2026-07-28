```markdown
# Datastraw Customer Support CRM System

A full-stack web application built for the Datastraw Engineering Assessment. This lightweight CRM system allows teams to manage customer support tickets efficiently.

## Core Features
* **Create Tickets:** Add new support tickets with auto-generated unique IDs.
* **List Tickets:** View all active and closed tickets in a clean dashboard.
* **Update Status:** Instantly change ticket statuses (Open, In Progress, Closed).
* **Filter & Search:** Filter by status and search by customer name.

## Tech Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite
* **Frontend:** HTML, Vanilla JavaScript, CSS (served directly via FastAPI)
* **Deployment:** Render

## Local Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/Asmita871/datastraw-crm.git
cd datastraw-crm

```

2. **Create and activate a virtual environment:**

```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Mac/Linux:
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Run the server:**

```bash
uvicorn main:app --reload

```

5. **Access the Dashboard:**
Open your web browser and navigate to `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)`.

## Architecture Note

To ensure a stable, on-time deployment for the MVP, the architecture was kept intentionally streamlined, focusing on the core CRUD pipeline (Create, List, Update, Filter). The frontend is served directly from the FastAPI backend using `StaticFiles` and `FileResponse` to eliminate cross-origin resource sharing (CORS) overhead and simplify deployment.

