from decimal import Decimal, ROUND_HALF_UP

TWO_DECIMAL_PLACES = Decimal("0.01")

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