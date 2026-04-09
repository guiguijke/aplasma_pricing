from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routers import config as config_router
from routers import materials as materials_router
from routers import quotes as quotes_router
from routers.config import seed_config
from routers.materials import seed_materials

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="aplasma_pricing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3500", "http://127.0.0.1:3500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router.router)
app.include_router(materials_router.router)
app.include_router(quotes_router.router)


@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        seed_config(db)
        seed_materials(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
