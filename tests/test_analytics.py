from decimal import Decimal
import pytest
from app.analytics import (
    calculate_attrition_percentage,
    calculate_nic,
    calculate_oversubscription_ratio,
    calculate_pricing_tightening,
)

def test_calculate_oversubscription_ratio() -> None:
    result = calculate_oversubscription_ratio(
        tranche_size=Decimal("1000000000.00"),
        final_orderbook=Decimal("3000000000.00")
    )

    assert result == Decimal("3.00")

def test_calculate_attrition_percentage() -> None:
    result = calculate_attrition_percentage(
        peak_orderbook=Decimal("3500000000.00"),
        final_orderbook=Decimal("3000000000.00")
    )

    assert result == Decimal("14.29")

def test_attrition_is_unavailable_when_peak_is_zero() -> None:
    result = calculate_attrition_percentage(
        peak_orderbook=Decimal("0"),
        final_orderbook=Decimal("0")
    )

    assert result is None

def test_calculate_pricing_tightening() -> None:
    result = calculate_pricing_tightening(
        ipt_spread_bps=Decimal("145.00"),
        final_spread_bps=Decimal("125.00")
    )

    assert result == Decimal("20.00")

def test_calculate_nic() -> None:
    result = calculate_nic(
        final_spread_bps=Decimal("125.00"),
        fair_value_spread_bps=Decimal("118.00")
    )

    assert result == Decimal("7.00")

def test_oversubscription_rejects_zero_tranche_size() -> None:
    with pytest.raises(
        ValueError,
        match="tranche size must be greater than zero"
    ):
        calculate_oversubscription_ratio(
            tranche_size=Decimal("0"),
            final_orderbook=Decimal("100.00")
        )