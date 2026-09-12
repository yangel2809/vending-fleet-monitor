"""CLI: lee telemetría de un CSV, genera alertas y una ruta de reabastecimiento
para las máquinas que lo necesitan.

Uso:
    python src/main.py data/sample_machines.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import AlertType, Machine, TelemetryReading
from src.monitoring.alert_rules import evaluate
from src.reports.report_generator import summarize, write_alerts_csv
from src.routing.route_optimizer import build_route, total_distance_km


def load_data(csv_path: str) -> tuple[dict[str, Machine], list[TelemetryReading]]:
    machines: dict[str, Machine] = {}
    readings: list[TelemetryReading] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            machine = Machine(
                machine_id=row["machine_id"],
                name=row["name"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )
            machines[machine.machine_id] = machine

            if machine.machine_id == "DEPOT":
                continue

            readings.append(
                TelemetryReading(
                    machine_id=machine.machine_id,
                    stock_percentage=float(row["stock_percentage"]),
                    payment_errors_last_hour=int(row["payment_errors_last_hour"]),
                    is_online=row["is_online"].strip().lower() == "true",
                )
            )

    return machines, readings


def main(csv_path: str) -> None:
    machines, readings = load_data(csv_path)

    all_alerts = [alert for reading in readings for alert in evaluate(reading)]

    print(summarize(all_alerts))
    write_alerts_csv(all_alerts, "alerts_report.csv")
    print("\nReporte guardado en alerts_report.csv")

    needs_restock_ids = {
        alert.machine_id for alert in all_alerts if alert.alert_type in (AlertType.OUT_OF_STOCK, AlertType.LOW_STOCK)
    }

    if not needs_restock_ids:
        return

    depot = machines["DEPOT"]
    stops = [machines[mid] for mid in needs_restock_ids]
    route = build_route(depot, stops)

    print(f"\nRuta de reabastecimiento sugerida ({len(route)} parada(s)):")
    for i, stop in enumerate(route, start=1):
        print(f"  {i}. {stop.name} ({stop.machine_id})")

    print(f"Distancia total estimada: {total_distance_km(depot, route):.1f} km")


if __name__ == "__main__":
    csv_arg = sys.argv[1] if len(sys.argv) > 1 else "data/sample_machines.csv"
    main(csv_arg)
