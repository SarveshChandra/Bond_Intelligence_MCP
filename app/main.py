from fastapi import FastAPI, Depends, HTTPException, status, Path, Query

from sqlalchemy import text, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import BondTranche
from app.schemas import (
    BondTrancheCreate,
    BondTrancheRead,
    BondOrderbookAnalytics,
    BondPricingAnalytics
)
from app.analytics import (
    calculate_attrition_percentage,
    calculate_nic,
    calculate_oversubscription_ratio,
    calculate_pricing_tightening
)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

def get_bond_or_404(
        db: Session,
        bond_id: int
) -> BondTranche:
    bond = db.get(BondTranche, bond_id)

    if bond is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bond not found"
        )

    return bond    

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

@app.get(
    "/bonds",
    response_model=list[BondTrancheRead],
    tags=["Bonds"]
)
def list_bonds(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db)
) -> list[BondTranche]:
    statement = (
        select(BondTranche)
        .order_by(BondTranche.id)
        .offset(skip)
        .limit(limit)
    )

    bonds = db.scalars(statement).all()

    return list(bonds)

@app.get(
    "/bonds/{bond_id}",
    response_model=BondTrancheRead,
    tags=["Bonds"]
)
def get_bond(
    bond_id: int = Path(gt=0),
    db: Session = Depends(get_db)
) -> BondTranche:
    return get_bond_or_404(db, bond_id)

@app.get(
    "/bonds/{bond_id}/orderbook",
    response_model=BondOrderbookAnalytics,
    tags=["Analytics"]
)
def get_orderbook_analytics(
    bond_id: int = Path(gt=0),
    db: Session = Depends(get_db)
) -> BondOrderbookAnalytics:
    bond = get_bond_or_404(db, bond_id)

    return BondOrderbookAnalytics(
        bond_id=bond.id,
        isin=bond.isin,
        currency=bond.currency,
        tranche_size=bond.tranche_size,
        peak_orderbook=bond.peak_orderbook,
        final_orderbook=bond.final_orderbook,
        oversubscription_ratio=(
            calculate_oversubscription_ratio(
                tranche_size=bond.tranche_size,
                final_orderbook=bond.final_orderbook
            )
        ),
        attrition_pct=calculate_attrition_percentage(
            peak_orderbook=bond.peak_orderbook,
            final_orderbook=bond.final_orderbook
        )
    )

@app.get(
    "/bonds/{bond_id}/pricing",
    response_model=BondPricingAnalytics,
    tags=["Analytics"]
)
def get_pricing_analytics(
    bond_id: int = Path(gt=0),
    db: Session = Depends(get_db)
) -> BondPricingAnalytics:
    bond = get_bond_or_404(db, bond_id)

    return BondPricingAnalytics(
        bond_id=bond.id,
        isin=bond.isin,
        ipt_spread_bps=bond.ipt_spread_bps,
        final_spread_bps=bond.final_spread_bps,
        fair_value_spread_bps=bond.fair_value_spread_bps,
        pricing_tightening_bps=(
            calculate_pricing_tightening(
                ipt_spread_bps=bond.ipt_spread_bps,
                final_spread_bps=bond.final_spread_bps
            )
        ),
        nic_bps=calculate_nic(
            final_spread_bps=bond.final_spread_bps,
            fair_value_spread_bps=bond.fair_value_spread_bps
        )
    )