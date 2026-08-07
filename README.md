

```markdown
# Datastraw Customer Support CRM System

A full-stack web application built for the Datastraw Engineering Assessment. This lightweight CRM system allows teams to manage customer support tickets efficiently.

## Live Demo
* **Web Application:** https://datastraw-crm-2zri.onrender.com

## Core Features
* **Create Tickets:** Add new support tickets with auto-generated unique IDs.
* **List Tickets:** View all active and closed tickets in a clean dashboard.
* **Update Status & Notes:** Instantly change ticket statuses (Open, In Progress, Closed) and automatically save context-specific notes.
* **Advanced Filter & Search:** Filter by status and search simultaneously across Ticket ID, Customer Name, Email, and Description.
* **Timezone Handling:** Automatically standardizes server database timestamps to Indian Standard Time (IST).

## Tech Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite
* **Frontend:** HTML, Vanilla JavaScript, Tailwind CSS (via CDN)
* **Deployment:** Render

## Local Setup Instructions

1. **Clone the repository:**
```bash
git clone [https://github.com/Asmita871/datastraw-crm.git](https://github.com/Asmita871/datastraw-crm.git)
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
Open your web browser and navigate to http://127.0.0.1:8000/.

## Architecture Note

To ensure a stable, on-time deployment for the MVP, the architecture was kept intentionally streamlined, focusing on a core CRUD pipeline. The frontend is served directly from the FastAPI backend using `StaticFiles` to eliminate cross-origin resource sharing (CORS) overhead and simplify deployment. Data is managed via a lightweight SQLite database equipped with built-in timezone conversion to ensure reliable timestamps regardless of the hosting server's default configuration.

```

```
