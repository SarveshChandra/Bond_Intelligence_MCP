from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

TWO_DECIMAL_PLACES = Decimal("0.01")

CurveShape = Literal[
    "normal",
    "flat",
    "inverted",
    "humped"
]

def calculate_oversubscription_ratio(
        tranche_size: Decimal,
        final_orderbook: Decimal
) -> Decimal:
    if tranche_size <= 0:
        raise ValueError("tranche size must be greater than zero")
    if final_orderbook < 0:
        raise ValueError("final orderbook cannot be negative")

    ratio = final_orderbook / tranche_size

    return ratio.quantize(
        TWO_DECIMAL_PLACES,
        rounding=ROUND_HALF_UP
    )

def calculate_attrition_percentage(
        peak_orderbook: Decimal,
        final_orderbook: Decimal,
) -> Decimal | None:
    if peak_orderbook < 0 or final_orderbook < 0:
        raise ValueError("order book values cannot be negative")
    if final_orderbook > peak_orderbook:
        raise ValueError(
            "final orderbook cannot exceed peak orderbook"
        )

    if peak_orderbook == 0:
        return None

    percentage = (
        (peak_orderbook - final_orderbook)
        / peak_orderbook
        * Decimal("100")
    )

    return percentage.quantize(
        TWO_DECIMAL_PLACES,
        rounding=ROUND_HALF_UP
    )

def calculate_pricing_tightening(
        ipt_spread_bps: Decimal,
        final_spread_bps: Decimal
) -> Decimal:
    tightening = ipt_spread_bps - final_spread_bps

    return tightening.quantize(
        TWO_DECIMAL_PLACES,
        rounding=ROUND_HALF_UP
    )

def calculate_nic(
        final_spread_bps: Decimal,
        fair_value_spread_bps: Decimal
) -> Decimal:
    nic = final_spread_bps - fair_value_spread_bps

    return nic.quantize(
        TWO_DECIMAL_PLACES,
        rounding=ROUND_HALF_UP
    )

def classify_curve_shape(
        points: list[tuple[Decimal, Decimal]],
        flat_tolerance_pct: Decimal = Decimal("0.10"),
        hump_threshold_pct: Decimal = Decimal("0.10")
) -> CurveShape:
    if len(points) < 3:
        raise ValueError(
            "at least 3 curve points are required."
        )

    if flat_tolerance_pct < 0:
        raise ValueError(
            "flat tolerance pct cannot be negative."
        )

    if hump_threshold_pct < 0:
        raise ValueError(
            "hump threshold pct cannot be negative"
        )

    sorted_points = sorted(
        points,
        key=lambda point: point[0]
    )

    tenors = [tenor for tenor, _ in sorted_points]

    if any(tenor <= 0 for tenor in tenors):
        raise ValueError(
            "tenor years must be greater than 0"
        )

    if len(set(tenors)) != len(tenors):
        raise ValueError(
            "curve points must have unique tenors"
        )

    short_yield = sorted_points[0][1]
    long_yield = sorted_points[-1][1]

    middle_yields = [curve_yield for _, curve_yield in sorted_points[1:-1]]

    highest_middle_yield = max(middle_yields)

    if (
        highest_middle_yield - max(short_yield, long_yield) >= hump_threshold_pct
    ):
        return "humped"

    end_to_end_change = long_yield - short_yield

    if end_to_end_change > flat_tolerance_pct:
        return "normal"

    if end_to_end_change < -flat_tolerance_pct:
        return "inverted"

    return "flat"