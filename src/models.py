"""Modelos de dominio para la red de máquinas expendedoras."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AlertType(str, Enum):
    OUT_OF_STOCK = "out_of_stock"
    LOW_STOCK = "low_stock"
    PAYMENT_ERROR = "payment_error"
    OFFLINE = "offline"


class AlertSeverity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"


@dataclass(frozen=True)
class Machine:
    machine_id: str
    name: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class TelemetryReading:
    machine_id: str
    stock_percentage: float  # 0-100
    payment_errors_last_hour: int
    is_online: bool


@dataclass(frozen=True)
class Alert:
    machine_id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
