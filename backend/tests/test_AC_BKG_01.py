# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_2_remaining_reaches_zero(client, make_slot, db):
    """TC-BKG-01-2: ที่นั่งเริ่มจาก 1 แล้วลดลงเป็น 0 หลังยืนยันการจอง"""
    slot = make_slot(start="09:00", remaining=1)

    # Given: ผู้รับบริการยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    # When: ผู้รับบริการยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกการจองสำเร็จ แสดงหมายเลขคิว และที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    data = res.json()
    assert data["booking_id"] is not None
    assert data["queue_no"]

    db.refresh(slot)
    assert slot.remaining == 0


def test_TC_BKG_01_3_unverified_user(client, make_slot):
    """TC-BKG-01-3: ยังไม่ระบุผลตอบกลับสำหรับผู้ใช้ที่ยังไม่ได้ยืนยันตัวตน"""
    slot = make_slot(start="09:00", remaining=1)

    # Given: ผู้รับบริการยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    # When: ผู้รับบริการพยายามยืนยันการจองช่วง 09.00 น.
    client.post("/bookings", json={"slot_id": slot.id})

    # Then: spec ไม่ได้บอกผลตอบกลับหรือการบันทึก จึงยังไม่มี assertion
    # ตอนนี้ยังไม่ตรวจเพราะต้องรอคำตอบจากข้อกำหนด
