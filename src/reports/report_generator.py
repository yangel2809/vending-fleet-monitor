"""Genera un reporte diario en CSV a partir de las alertas detectadas."""

from __future__ import annotations

import csv
from pathlib import Path

from src.models import Alert


def write_alerts_csv(alerts: list[Alert], output_path: str | Path) -> None:
    output_path = Path(output_path)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["machine_id", "alert_type", "severity", "message"])

        for alert in alerts:
            writer.writerow([alert.machine_id, alert.alert_type.value, alert.severity.value, alert.message])


def summarize(alerts: list[Alert]) -> str:
    if not alerts:
        return "Sin alertas — toda la red operando con normalidad."

    critical = sum(1 for a in alerts if a.severity.value == "critical")
    warning = len(alerts) - critical

    lines = [f"{len(alerts)} alerta(s): {critical} crítica(s), {warning} de advertencia."]
    for alert in alerts:
        lines.append(f"  [{alert.severity.value.upper()}] {alert.machine_id}: {alert.message}")

    return "\n".join(lines)
