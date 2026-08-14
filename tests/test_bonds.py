from sqlalchemy import delete
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import BondTranche

client = TestClient(app)

TEST_ISIN = "XSTEST000001"

def remove_test_bond() -> None:
    with SessionLocal() as db:
        db.execute(
            delete(BondTranche).where(
                BondTranche.isin == TEST_ISIN
            )
        )
        db.commit()

def test_create_bond() -> None:
    remove_test_bond()

    try:
        response = client.post(
            "/bonds",
            json={
                "isin": TEST_ISIN,
                "issuer": "Test Industries",
                "ticker": "TEST",
                "rating": "A",
                "currency": "USD",
                "tranche_size": "1000000000.00",
                "coupon": "4.2500",
                "maturity_date": "2031-08-13",
                "redemption_terms": (
                    "Redeemed at par on maturity"
                ),
                "ipt_spread_bps": "145.00",
                "final_spread_bps": "125.00",
                "fair_value_spread_bps": "118.00",
                "peak_orderbook": "3500000000.00",
                "final_orderbook": "3000000000.00",
                "syndicate": "Bank A, Bank B",

            }
        )

        assert response.status_code == 201

        response_data=response.json()

        assert response_data["id"] > 0
        assert response_data["isin"] == TEST_ISIN
        assert response_data["issuer"] == "Test Industries"
        assert response_data["created_at"] is not None
    finally:
        remove_test_bond()