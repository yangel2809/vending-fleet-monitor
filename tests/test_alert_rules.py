import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import AlertSeverity, AlertType, TelemetryReading
from src.monitoring.alert_rules import evaluate


def make_reading(**overrides):
    defaults = dict(
        machine_id="M-001",
        stock_percentage=100.0,
        payment_errors_last_hour=0,
        is_online=True,
    )
    defaults.update(overrides)
    return TelemetryReading(**defaults)


def test_no_alerts_when_everything_is_fine():
    reading = make_reading()
    assert evaluate(reading) == []


def test_out_of_stock_is_critical():
    reading = make_reading(stock_percentage=0)
    alerts = evaluate(reading)
    assert len(alerts) == 1
    assert alerts[0].alert_type == AlertType.OUT_OF_STOCK
    assert alerts[0].severity == AlertSeverity.CRITICAL


def test_low_stock_is_warning():
    reading = make_reading(stock_percentage=15)
    alerts = evaluate(reading)
    assert alerts[0].alert_type == AlertType.LOW_STOCK
    assert alerts[0].severity == AlertSeverity.WARNING


def test_payment_errors_trigger_critical_alert():
    reading = make_reading(payment_errors_last_hour=5)
    alerts = evaluate(reading)
    assert any(a.alert_type == AlertType.PAYMENT_ERROR for a in alerts)


def test_offline_machine_triggers_alert():
    reading = make_reading(is_online=False)
    alerts = evaluate(reading)
    assert any(a.alert_type == AlertType.OFFLINE for a in alerts)


def test_multiple_problems_produce_multiple_alerts():
    reading = make_reading(stock_percentage=0, payment_errors_last_hour=10, is_online=False)
    alerts = evaluate(reading)
    assert len(alerts) == 3
