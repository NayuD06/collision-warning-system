from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import collision_event_controller
from app.core.database import get_db
from app.schemas.collision_event_schema import CollisionCheckRequest, CollisionCheckResponse

router = APIRouter(prefix="/collision-events", tags=["collision-events"])


@router.post("/check", response_model=CollisionCheckResponse)
def check_collision(payload: CollisionCheckRequest, db: Annotated[Session, Depends(get_db)]):
    return collision_event_controller.check_collision(db, payload)
