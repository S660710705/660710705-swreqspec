# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:35 | test: 8 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py: test_AC_BKG_05 ผ่าน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ยังไม่มีการตรวจสอบคิวในวันเดียวกันใน backend/app/booking/service.py: create_booking | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ยังไม่มีการค้นหา 3 ช่วงใกล้เคียงหรือการแสดงผลใน frontend/src/pages/ConfirmBooking.jsx | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py: create_booking; backend/app/booking/service.py: create_booking, next_queue_no | backend/tests/test_AC_BKG_01.py: test_AC_BKG_01 ผ่าน; test_TC_BKG_01_2_remaining_reaches_zero ผ่าน; test_TC_BKG_01_3_unverified_user ผ่าน (ไม่ตรวจผลของ TC-BKG-01-3 เพราะ spec ยังไม่ได้กำหนด) | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 | ยังไม่มีคิวส่งข้อความหรือการส่งซ้ำใน backend/app/notify/queue.py และ backend/app/booking/service.py | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-10 | frontend/src/pages/SlotPicker.jsx: SlotPicker; backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | frontend/src/__tests__/T09_SlotPicker.test.jsx ผ่าน แต่ไม่ตรวจแพ็กเกจเปลี่ยนวัน/ช่วงเวลาหรือผลที่นั่งตามแพ็กเกจ | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py: test_AC_BKG_05 ผ่าน โดยใช้ 200 คำขอแบบย่อส่วนใน SQLite | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีการเข้ารหัส TLS ใน backend/app หรือ frontend/src ที่ตรวจได้ | ไม่มี test ในโค้ด | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ยังไม่มีคิวส่งซ้ำหรือกำหนดเวลาส่งภายใน 5 นาที | ไม่มี test ในโค้ด | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีการวัดเวลาการจอง 8 ใน 10 คน หรือการติดตามผู้ใช้ใหม่ | ไม่มี test ในโค้ด | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL ชี้ SQLite ใน Codespace; ไม่มีการบังคับเป็น PostgreSQL ใน runtime | backend/tests/test_T01_schema.py ผ่าน แต่ไม่ตรวจ PostgreSQL | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-01, T-08 | backend/app/db/models.py: AuditLog; backend/app/main.py: ไม่มี middleware audit; backend/app/config.py: ไม่มีการเก็บ retention | backend/tests/test_T01_schema.py ผ่าน แต่ไม่ตรวจ audit log การเข้าถึง | ช่องโหว่ |
| IF-IDP-01 | AC-BKG-01 | T-03 | backend/app/auth/idp.py: get_verified_hn | backend/tests/test_AC_BKG_01.py: test_TC_BKG_01_3_unverified_user ไม่ตรวจผลเพราะ spec ไม่ระบุ; test AC-BKG-01 ทั้งหมดผ่าน | ช่องโหว่ |
| IF-HIS-01 | ไม่มี AC | T-01, T-09 | backend/app/db/models.py: Booking เก็บ hn เท่านั้น; backend/app/his/client.py ยังไม่พบอยู่จริง; API GET /patients/lookup ยังไม่พบอยู่จริง | backend/tests/test_T01_schema.py: test_T01_no_national_id ผ่าน | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ยังไม่มีการวางงานลงคิวหรือส่งซ้ำใน backend/app/notify/queue.py และ backend/app/booking/service.py | ไม่มี test ในโค้ด | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/booking/router.py: create_booking | FR-BKG-04 | ไม่ครบ | คืน booking_id, slot_id และ queue_no แต่ไม่มีการยืนยันว่าเป็น queue_no ตามรูปแบบที่ spec กำหนด เพราะ Q-02 ยังไม่ได้ตอบ |
| backend/app/booking/service.py: create_booking | FR-BKG-04 | ไม่ครบ | ตัดที่นั่งและบันทึกการจอง แต่ยังไม่มีเงื่อนไขการตรวจคิววันเดียวกัน (FR-BKG-02) และไม่มีการส่งข้อความยืนยันตาม IF-NOT-01 |
| backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | ไม่ครบ | ใช้รูปแบบ A001 และนับใหม่ทุกวัน แม้ Q-02 ยังไม่ได้ตอบ โดยไม่มีรหัสหรือ policy จากเจ้าหน้าที่เวชระเบียน |
| backend/app/booking/router.py: cancel_booking | Out of scope | ไม่ตรง | มี endpoint ยกเลิกการจอง แต่ spec ระบุว่า UC-02 อยู่ใน Out of scope |
| backend/app/booking/service.py: cancel_booking | Out of scope | ไม่ตรง | สามารถคืนที่นั่งและเปลี่ยน status เป็น CANCELLED แม้ spec ระบุว่าไม่ทำในฟีเจอร์นี้ |
| backend/app/slots/service.py: DAYS_AHEAD = 14 | FR-BKG-01 | ไม่ตรง | Spec ต้องการช่วงเวลาภายใน 30 วันข้างหน้า แต่โค้ดแสดงเฉพาะ 14 วัน และช่อง date_from กำหนดวันเริ่มต้น |
| backend/app/slots/service.py: list_available_slots | FR-BKG-01 | ไม่ครบ | ใช้เฉพาะช่วงที่ remaining > 0 แต่ไม่กำหนดว่าจะใช้ package_code ที่มีอยู่จริง และไม่ตรวจจำนวนวัน 30 ตาม spec |
| backend/app/config.py: DATABASE_URL | CON-TECH-01 | ไม่ครบ | ค่าเริ่มต้นเป็น SQLite ใน Codespace ไม่ใช่ PostgreSQL แม้ plan ระบุใช้ PostgreSQL ในระบบจริง |
| backend/app/db/models.py: Booking.queue_no | Q-02 | ไม่ครบ | คอลัมน์ถูกตั้งเป็น nullable และยังไม่กำหนดรูปแบบหรือการนับตาม Q-02 |
| backend/app/db/models.py: AuditLog | DOM-PDPA-01 | ไม่ครบ | มี schema audit log แต่ไม่มี middleware ที่บันทึกการเข้าถึงข้อมูลการจองตาม spec |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ไม่ครบ | ตรวจ token แต่ยังไม่มีการจัดเรียงและตรวจสิทธิ์ของผู้รับบริการที่ระบุใน spec ตามระบบยืนยันตัวตนจริง |
| frontend/src/api/client.js: createBooking | FR-BKG-04 | ไม่ครบ | เรียก POST /bookings แต่ไม่ได้ใส่ข้อมูลผู้รับบริการหรือจัดการผลตาม AC-BKG-01 และไม่มีการแสดง queue_no ใน UI |
| frontend/src/pages/SlotPicker.jsx: SlotPicker | FR-BKG-06 | ไม่ครบ | ระบุค่า package_code แต่ใช้ค่า basic/premium ที่ไม่ตรงกับระบบ backend ซึ่งใช้ BASIC ตาม fixture และ no test สำหรับภาวะเปลี่ยนแพ็กเกจ

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: DAYS_AHEAD = 14 | FR-BKG-01 | แสดงได้ 14 วัน แต่ spec ระบุภายใน 30 วันข้างหน้า |  |
| F-02 | โค้ดไม่มี FR | backend/app/booking/router.py: cancel_booking; backend/app/booking/service.py: cancel_booking | Out of scope | มีฟังก์ชันยกเลิกและคืนที่นั่ง แม้ spec ระบุ UC-02 อยู่ใน Out of scope |  |
| F-03 | เดา Q-xx | backend/app/booking/service.py: next_queue_no | Q-02, FR-BKG-04 | กำหนดรูปแบบ A001 และนับต่อวันเป็นการตัดสินใจแทนทีม เนื่องจาก Q-02 ยังไม่ได้คำตอบ |  |
| F-04 | โค้ดไม่มี FR | backend/app/main.py | DOM-PDPA-01 | ไม่มี middleware บันทึก audit log แม้ model AuditLog มีอยู่ |  |
| F-05 | ละเมิด Constraint | backend/app/booking/router.py: BookingRequest.national_id; backend/app/booking/router.py: logger.info | IF-HIS-01, DOM-PDPA-01 | รับและ log เลขบัตรประชาชน แม้ IF-HIS-01 ระบุไม่เก็บเลขบัตรประชาชนในตารางการจอง และ log โดยไม่จำเป็นอาจเปิดเผยข้อมูล |  |
| F-06 | FR ไม่มี AC | backend/app/slots/service.py: list_available_slots; frontend/src/pages/SlotPicker.jsx: SlotPicker | FR-BKG-06 | FR-BKG-06 มี implementation แต่ไม่มี AC ที่ตรวจการเปลี่ยนแพ็กเกจและการคำนวณช่วงเวลาว่างใหม่ |  |
| F-07 | AC ไม่มี test / test อ่อน | backend/tests/test_AC_BKG_01.py: test_AC_BKG_01 | AC-BKG-01 | test เดิมตรวจเฉพาะ status 201 โดยไม่ตรวจ queue_no และจำนวนที่นั่งหลังบันทึก แม้เพิ่ม test ใหม่แล้ว test เดิมยังเป็น test อ่อน |  |
| F-08 | test อ่อน | backend/tests/test_AC_BKG_01.py: test_TC_BKG_01_3_unverified_user | AC-BKG-01, IF-IDP-01 | แสดง no assertion เนื่องจาก spec ไม่ระบุผล แต่ยังเป็น test เดิมที่ไม่ตรวจกรณีไม่ยืนยันตัวตนและไม่สามารถทดสอบการป้องกันได้ |  |
| F-09 | AC ไม่มี test | specs/001-booking/spec.md: AC-BKG-02, AC-BKG-03, AC-BKG-04, AC-BKG-06 | FR-BKG-02, FR-BKG-03, FR-BKG-05, DOM-PDPA-01 | specification มี AC แต่ยังไม่มี test implementation ใน repository ตาม task |  |
| F-10 | test อ่อน | backend/tests/test_AC_BKG_05.py: test_AC_BKG_05 | NFR-PERF-01 | ใช้ SQLite ในหน่วยความจำและ 200 ครั้งแบบย่อส่วนจาก Codespace ต้องวัดจริงในสภาพแวดล้อมรันข้อมูลจริง |  |
| F-11 | AC ไม่มี test | frontend/src/__tests__/T09_SlotPicker.test.jsx | FR-BKG-01, FR-BKG-06 | test หน้าเลือกแพ็กเกจมีเพียงรายการ slot แต่ไม่มี test เพื่อเปลี่ยนแพ็กเกจและตรวจผลใหม่ |  |
| F-12 | โค้ดไม่มี FR | frontend/src/api/client.js: getSlots | FR-BKG-01 | API client ส่ง package_code เป็น basic/premium แต่ backend กำหนด package_code เป็น BASIC โดย fixture; ยังไม่ยืนยันว่า frontend API response schema ตรงกับ backend |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
