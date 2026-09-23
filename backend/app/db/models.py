from datetime import datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# รองรับ CON-TECH-01, IF-HIS-01
class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slot_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    package_code: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")

    __table_args__ = (
        UniqueConstraint("slot_date", "start_time", "package_code", name="uq_slot_date_time_package"),
    )


# รองรับ FR-BKG-04, IF-HIS-01
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False)
    booking_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    queue_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="booked")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    slot: Mapped[Slot] = relationship(back_populates="bookings")


# รองรับ DOM-PDPA-01
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )
