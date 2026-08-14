from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import BondTranche
from app.schemas import BondTrancheCreate, BondTrancheRead

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}

# Readiness Check
@app.get("/ready", tags=["System"])
def readiness_check(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from error

    return {
        "status": "ready",
        "database": "available",
    }

@app.post(
    "/bonds",
    response_model=BondTrancheRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Bonds"]
)
def create_bond(
    bond_data: BondTrancheCreate,
    db: Session = Depends(get_db)
) -> BondTranche:
    bond = BondTranche(**bond_data.model_dump())

    try:
        db.add(bond)
        db.commit()
        db.refresh(bond)
    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="A bond with this ISIN already exists."
        ) from error

    return bond