import importlib.util
from pathlib import Path

from sqlalchemy import inspect, text
from sqlalchemy.engine import create_engine

migration_path = Path(__file__).resolve().parents[1] / "app" / "db" / "migrations" / "001_init.py"
spec = importlib.util.spec_from_file_location("migration_001_init", migration_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_T01_creates_required_booking_schema():
    engine = create_engine("sqlite:///:memory:")

    module.upgrade(engine)
    inspector = inspect(engine)

    assert inspector.has_table("slots")
    assert inspector.has_table("bookings")
    assert inspector.has_table("audit_logs")

    with engine.connect() as conn:
        bookings_columns = [row[1] for row in conn.execute(text("PRAGMA table_info('bookings')"))]
        slots_columns = [row[1] for row in conn.execute(text("PRAGMA table_info('slots')"))]
        audit_columns = [row[1] for row in conn.execute(text("PRAGMA table_info('audit_logs')"))]

    assert "hn" in bookings_columns
    assert "national_id" not in bookings_columns
    assert "remaining" in slots_columns
    assert "capacity" in slots_columns
    assert "actor_id" in audit_columns
    assert "accessed_at" in audit_columns
    assert "hn" in audit_columns
