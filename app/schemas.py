from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

class BondTrancheBase(BaseModel):
    isin: str = Field(min_length=12, max_length=12)
    issuer: str = Field(min_length=1, max_length=200)
    ticker: str = Field(min_length=1, max_length=20)
    rating: str = Field(min_length=1, max_length=10)
    currency: str = Field(min_length=3, max_length=3)

    tranche_size: Decimal = Field(gt=0)
    coupon: Decimal = Field(ge=0, le=100)
    maturity_date: date
    redemption_terms: str = "Redeemed at par on maturity"

    ipt_spread_bps: Decimal
    final_spread_bps: Decimal
    fair_value_spread_bps: Decimal

    peak_orderbook: Decimal = Field(ge=0)
    final_orderbook: Decimal = Field(ge=0)

    syndicate: str | None = None

    # cross-field validation to ensure final_orderbook does not exceed peak_orderbook
    @model_validator(mode="after")
    def validate_orderbook(self) -> "BondTrancheBase":
        if self.final_orderbook > self.peak_orderbook:
            raise ValueError(
                "final_orderbook cannot exceed peak_orderbook"
            )

        return self

class BondTrancheCreate(BondTrancheBase):
    pass

class BondTrancheRead(BondTrancheBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)