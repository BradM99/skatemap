# SkateMap

**SkateMap** is a web app for skateboarders to discover, share, and review street skate spots.

---

## Features (MVP)
- Interactive map displaying skate spots using **OpenStreetMap**  
- Add new skate spots with name, description, and location  
- View spot details and images  

---

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, SQLAlchemy (2.0), Alembic, Pydantic  
- **Frontend:** Next.js, React-Leaflet, Tailwind CSS  
- **Image Storage:** Local folder served via FastAPI `StaticFiles`  
- **Map:** OpenStreetMap + Leaflet.js  

---

## Setup (local development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

- Configure database URL in `.env`  
- Setup database tables (`python -m db.create_db`)
- Start server: `uvicorn app.main:app --reload`


- Visit `http://localhost:3000` to view the app

---

## Notes
- All database IDs are UUIDs  
- Images stored locally as files, paths handled with `pathlib.Path`  
- Deleting a spot removes its reviews and images automatically  
- Leaflet used for interactive map markers