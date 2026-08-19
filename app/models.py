from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, Text, func, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class BondTranche(Base):
    __tablename__ = "bond_tranches"

    id: Mapped[int] = mapped_column(primary_key = True)

    isin: Mapped[str] = mapped_column(String(12), unique = True, index = True)

    issuer: Mapped[str] = mapped_column(String(200), index=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    rating: Mapped[str] = mapped_column(String(10))
    currency: Mapped[str] = mapped_column(String(3))

    tranche_size: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    coupon: Mapped[Decimal] = mapped_column(Numeric(7, 4))
    maturity_date: Mapped[date] = mapped_column(Date)
    redemption_terms: Mapped[str] = mapped_column(
        Text,
        default="Redeemed at par on maturity",
    )

    ipt_spread_bps: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    final_spread_bps: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    fair_value_spread_bps: Mapped[Decimal] = mapped_column(Numeric(8, 2))

    peak_orderbook: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    final_orderbook: Mapped[Decimal] = mapped_column(Numeric(18, 2))

    syndicate: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

class YieldCurvePoint(Base):
    __tablename__ = "yield_curve_points"

    __table_args__ = (
        UniqueConstraint(
            "issuer",
            "currency",
            "observation_date",
            "tenor_years",
            name="uq_yield_curve_point"
        ),
        Index(
            "ix_yield_curve_points_lookup",
            "issuer",
            "currency",
            "observation_date"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    issuer: Mapped[str] = mapped_column(String(200))
    currency: Mapped[str] = mapped_column(String(3))
    observation_date: Mapped[date] = mapped_column(Date)

    tenor_years: Mapped[Decimal] = mapped_column(Numeric(6,2))
    yield_pct: Mapped[Decimal] = mapped_column(Numeric(7,4))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )