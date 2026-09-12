import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import Machine
from src.routing.route_optimizer import build_route, haversine_distance_km, total_distance_km

DEPOT = Machine("DEPOT", "Depósito", 10.19, -68.00)
CLOSE = Machine("M-CLOSE", "Cercana", 10.191, -68.001)
FAR = Machine("M-FAR", "Lejana", 10.30, -68.15)
MID = Machine("M-MID", "Intermedia", 10.22, -68.03)


def test_haversine_distance_is_zero_for_same_point():
    assert haversine_distance_km(10.0, -68.0, 10.0, -68.0) == 0.0


def test_route_visits_all_stops_exactly_once():
    route = build_route(DEPOT, [FAR, CLOSE, MID])
    assert len(route) == 3
    assert {m.machine_id for m in route} == {"M-FAR", "M-CLOSE", "M-MID"}


def test_route_picks_closest_stop_first():
    route = build_route(DEPOT, [FAR, CLOSE, MID])
    assert route[0].machine_id == "M-CLOSE"


def test_total_distance_is_positive_for_non_empty_route():
    route = build_route(DEPOT, [FAR, CLOSE, MID])
    assert total_distance_km(DEPOT, route) > 0


def test_total_distance_is_zero_for_empty_route():
    assert total_distance_km(DEPOT, []) == 0.0
