from sqlalchemy import delete
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import BondTranche

from decimal import Decimal

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

def create_test_bond() -> dict:
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

        return response_data
    finally:
        print("test bond created")

def test_get_bond() -> None:
    remove_test_bond()

    try:
        created_bond = create_test_bond()
        bond_id = created_bond["id"]

        response = client.get(f"/bonds/{bond_id}")

        assert response.status_code == 200
        assert response.json()["id"] == bond_id
        assert response.json()["isin"] == TEST_ISIN
    finally:
        remove_test_bond()

def test_list_bonds() -> None:
    remove_test_bond()

    try:
        create_test_bond()

        response = client.get("/bonds?skip=0&limit=100")

        assert response.status_code == 200

        bond_isins = [
            bond["isin"]
            for bond in response.json()
        ]

        assert TEST_ISIN in bond_isins
    finally:
        remove_test_bond()

def test_missing_bond_returns_404() -> None:
    response = client.get("/bonds/999999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Bond not found"
    }

def test_get_orderbook_analytics() -> None:
    remove_test_bond()

    try:
        created_bond = create_test_bond()
        bond_id = created_bond["id"]

        response = client.get(
            f"/bonds/{bond_id}/orderbook"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["bond_id"] == bond_id
        assert data["isin"] == TEST_ISIN
        assert Decimal(
            str(data["oversubscription_ratio"])
        ) == Decimal("3.00")
        assert Decimal(
            str(data["attrition_pct"])
        ) == Decimal("14.29")
    finally:
        remove_test_bond()

def test_get_pricing_analytics() -> None:
    remove_test_bond()

    try:
        created_bond = create_test_bond()
        bond_id = created_bond["id"]

        response = client.get(
            f"/bonds/{bond_id}/pricing"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["bond_id"] == bond_id
        assert data["isin"] == TEST_ISIN
        assert Decimal(
            str(data["pricing_tightening_bps"])
        ) == Decimal("20.00")
        assert Decimal(
            str(data["nic_bps"])
        ) == Decimal("7.00")
    finally:
        remove_test_bond()