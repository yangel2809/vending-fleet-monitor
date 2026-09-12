"""Reglas para convertir telemetría cruda en alertas accionables.

Cada regla es una función pura: recibe una lectura y devuelve una alerta
(o None). Esto hace trivial agregar, quitar o testear una regla sin tocar
las demás.
"""

from __future__ import annotations

from src.models import Alert, AlertSeverity, AlertType, TelemetryReading

LOW_STOCK_THRESHOLD = 20.0  # porcentaje
PAYMENT_ERROR_THRESHOLD = 3  # errores en la última hora


def check_stock(reading: TelemetryReading) -> Alert | None:
    if reading.stock_percentage <= 0:
        return Alert(
            machine_id=reading.machine_id,
            alert_type=AlertType.OUT_OF_STOCK,
            severity=AlertSeverity.CRITICAL,
            message="Máquina sin stock — requiere reabastecimiento inmediato.",
        )

    if reading.stock_percentage <= LOW_STOCK_THRESHOLD:
        return Alert(
            machine_id=reading.machine_id,
            alert_type=AlertType.LOW_STOCK,
            severity=AlertSeverity.WARNING,
            message=f"Stock bajo ({reading.stock_percentage:.0f}%) — programar reabastecimiento.",
        )

    return None


def check_payment_errors(reading: TelemetryReading) -> Alert | None:
    if reading.payment_errors_last_hour >= PAYMENT_ERROR_THRESHOLD:
        return Alert(
            machine_id=reading.machine_id,
            alert_type=AlertType.PAYMENT_ERROR,
            severity=AlertSeverity.CRITICAL,
            message=(
                f"{reading.payment_errors_last_hour} errores de pago en la última hora "
                "— posible falla del lector o del gateway."
            ),
        )
    return None


def check_connectivity(reading: TelemetryReading) -> Alert | None:
    if not reading.is_online:
        return Alert(
            machine_id=reading.machine_id,
            alert_type=AlertType.OFFLINE,
            severity=AlertSeverity.WARNING,
            message="Máquina sin reportar telemetría — posible corte de conectividad o de energía.",
        )
    return None


RULES = (check_stock, check_payment_errors, check_connectivity)


def evaluate(reading: TelemetryReading) -> list[Alert]:
    """Corre todas las reglas sobre una lectura y devuelve las alertas disparadas."""
    alerts = (rule(reading) for rule in RULES)
    return [alert for alert in alerts if alert is not None]
