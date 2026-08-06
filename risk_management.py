from config import CAPITAL, RISK_PERCENT


def calculate_risk():
    risk_amount = CAPITAL * (RISK_PERCENT / 100)
    return risk_amount


def calculate_position_size(entry_price, stop_loss):
    risk_amount = calculate_risk()

    risk_per_unit = abs(entry_price - stop_loss)

    if risk_per_unit == 0:
        return 0

    quantity = int(risk_amount / risk_per_unit)

    return quantity


def calculate_targets(entry_price, stop_loss):
    risk = abs(entry_price - stop_loss)

    if entry_price > stop_loss:
        target_1 = entry_price + risk
        target_2 = entry_price + (risk * 2)
        target_3 = entry_price + (risk * 3)
    else:
        target_1 = entry_price - risk
        target_2 = entry_price - (risk * 2)
        target_3 = entry_price - (risk * 3)

    return target_1, target_2, target_3


if __name__ == "__main__":
    print("Maximum Risk: ₹", calculate_risk())
