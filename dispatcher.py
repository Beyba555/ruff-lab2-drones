def add_waypoint(
    drone_id: str,
    point: str | None,
    route: list[str] | None = None,
) -> list[str]:
    if route is None:
        route = []
    if point is not None:
        route.append(f"{drone_id}:{point}")
    return route


def _low_battery_mode(payload_kg: float) -> str:
    if payload_kg > 2.0:
        return "DROP_CARGO_AND_RETURN"
    return "RETURN_TO_BASE"


def _rain_mode(battery: int) -> str:
    if battery >= 80:
        return "ECO_FLIGHT"
    return "HOLD_POSITION"


def select_drone_mode(
    battery: int,
    payload_kg: float,
    is_raining: bool,
    emergency: bool,
) -> str:
    if emergency:
        return "LAND_IMMEDIATELY"
    if battery < 15:
        return _low_battery_mode(payload_kg)
    if is_raining:
        return _rain_mode(battery)
    if payload_kg > 5.0:
        return "HEAVY_LIFT"
    return "STANDARD"
