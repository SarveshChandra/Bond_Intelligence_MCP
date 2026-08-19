from decimal import Decimal
import pytest
from app.analytics import (
    calculate_attrition_percentage,
    calculate_nic,
    calculate_oversubscription_ratio,
    calculate_pricing_tightening,
    classify_curve_shape
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

def test_classify_normal_curve() -> None:
    result = classify_curve_shape(
        [
            (Decimal("2"), Decimal("4.10")),
            (Decimal("5"), Decimal("4.30")),
            (Decimal("10"), Decimal("4.60")),
        ]
    )

    assert result == "normal"

def test_classify_flat_curve() -> None:
    result = classify_curve_shape(
        [
            (Decimal("2"), Decimal("4.20")),
            (Decimal("5"), Decimal("4.25")),
            (Decimal("10"), Decimal("4.28")),
        ]
    )

    assert result == "flat"

def test_classify_inverted_curve() -> None:
    result = classify_curve_shape(
        [
            (Decimal("2"), Decimal("4.80")),
            (Decimal("5"), Decimal("4.50")),
            (Decimal("10"), Decimal("4.20")),
        ]
    )

    assert result == "inverted"

def test_classify_humped_curve() -> None:
    result = classify_curve_shape(
        [
            (Decimal("2"), Decimal("4.20")),
            (Decimal("5"), Decimal("4.70")),
            (Decimal("10"), Decimal("4.30")),
        ]
    )

    assert result == "humped"

def test_curve_requires_three_points() -> None:
    with pytest.raises(
        ValueError,
        match="at least 3 curve points are required."
    ):
        classify_curve_shape(
            [
                (Decimal("2"), Decimal("4.20")),
                (Decimal("10"), Decimal("4.30")),
            ]
        )