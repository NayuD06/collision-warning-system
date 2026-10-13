from fastapi import APIRouter

from app.routes import alert_routes, collision_event_routes

api_router = APIRouter()
api_router.include_router(alert_routes.router)
api_router.include_router(collision_event_routes.router)
