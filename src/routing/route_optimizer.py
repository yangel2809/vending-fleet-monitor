"""Optimización simple de rutas de reabastecimiento.

Usa el algoritmo de "vecino más cercano" (nearest neighbor): no garantiza
la ruta óptima global (eso sería un problema NP-difícil, tipo TSP), pero
para el tamaño real de estas rutas (10-30 paradas por técnico al día) da
resultados suficientemente buenos y es fácil de entender y mantener.

Si el tamaño de las rutas creciera mucho, el siguiente paso natural sería
usar un solver como OR-Tools — pero eso sería sobre-ingeniería en este caso.
"""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from src.models import Machine

EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def build_route(depot: Machine, stops: list[Machine]) -> list[Machine]:
    """Construye una ruta empezando en `depot`, visitando cada parada
    y saltando siempre a la más cercana no visitada aún.
    """
    remaining = list(stops)
    route: list[Machine] = []
    current = depot

    while remaining:
        nearest = min(
            remaining,
            key=lambda m: haversine_distance_km(current.latitude, current.longitude, m.latitude, m.longitude),
        )
        route.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return route


def total_distance_km(depot: Machine, route: list[Machine]) -> float:
    if not route:
        return 0.0

    points = [depot, *route]
    return sum(
        haversine_distance_km(a.latitude, a.longitude, b.latitude, b.longitude)
        for a, b in zip(points, points[1:])
    )
