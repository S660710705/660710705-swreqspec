# แผนทางเทคนิค: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง

ฟีเจอร์นี้จะให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาว่าง เพื่อจองคิวตรวจสุขภาพ และรับหมายเลขคิวที่ถูกต้องตามเวลาท้องถิ่นของโรงพยาบาล

ระบบจะประกอบด้วยหน้าจอแสดงช่วงเวลาว่าง การตรวจคิวซ้ำก่อนบันทึกการจอง การสร้างหมายเลขคิว และการส่งข้อความยืนยันแบบ asynchronous โดยไม่รอผลส่งข้อความ

การออกแบบจะเน้นความถูกต้องของตรรกะธุรกิจ เช่น การปฏิเสธเมื่อมีคิวที่ยังไม่ได้ใช้ การลดจำนวนที่นั่งเมื่อยืนยันสำเร็จ และการบันทึก audit log สำหรับทุกการเข้าถึงข้อมูลสุขภาพ

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Frontend: React + Vite | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับหน้าแสดงช่วงเวลา จองคิว และแสดงผลยืนยัน |
| Backend: Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ API ดึงช่วงเวลาว่าง ตรวจสิทธิ์ และบันทึกจอง |
| Database: MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจอง คิว และ audit log |
| ระบบยืนยันตัวตนภายนอก | IF-IDP-01 | ต้องยืนยันสำเร็จก่อนเข้าถึงข้อมูลผู้รับบริการ |
| HIS lookup | IF-HIS-01 | ใช้เลขบัตรประชาชนเพื่อค้นหาผู้รับบริการ แล้วเก็บ HN แทนในตารางการจอง |
| ระบบแจ้งเตือน SMS/LINE | IF-NOT-01 | ส่งข้อความยืนยันแบบ asynchronous ไม่ให้จองรอผลส่ง |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ requirement |
|---|---|---|
| UserProfile | user_id, hn, verified_at, status | IF-IDP-01, FR-BKG-02, FR-BKG-04 |
| Booking | booking_id, user_id, hn, package_id, booking_date, slot_start, slot_end, queue_no, booking_status, created_at | FR-BKG-01, FR-BKG-02, FR-BKG-04, FR-BKG-05 |
| SlotCapacity | slot_id, booking_date, slot_start, slot_end, max_capacity, remaining_capacity | FR-BKG-01, FR-BKG-03, FR-BKG-04 |
| NotificationQueue | notification_id, booking_id, channel, payload, status, scheduled_at, retry_count, created_at | FR-BKG-05, NFR-REL-02, IF-NOT-01 |
| AuditLog | log_id, actor_id, accessed_hn, action, accessed_at, metadata | DOM-PDPA-01 |

ข้อสังเกต:
- ไม่เก็บเลขบัตรประชาชนในตารางการจอง ตาม IF-HIS-01
- การคำนวณ remaining_capacity จะลดลงเมื่อบันทึกการจองสำเร็จ และเพิ่มกลับได้เฉพาะกรณีที่มีการยกเลิกหรือเลื่อนในอนาคต ซึ่งอยู่ใน Out of scope ปัจจุบัน
- Booking มีสถานะ เช่น pending, confirmed, expired, failed_notification เพื่อรองรับ FR-BKG-02 และ FR-BKG-05

## 4. API / หน้าจอ

| รายการ | รายละเอียด | รองรับ FR |
|---|---|---|
| GET /api/booking/slots | คืนรายการวันและช่วงเวลาว่างภายใน 30 วัน พร้อมจำนวนที่นั่งคงเหลือ | FR-BKG-01 |
| GET /api/packages | คืนแพ็กเกจที่พร้อมให้เลือก | FR-BKG-01, FR-BKG-06 |
| POST /api/booking/validate | ตรวจว่าผู้ใช้มีคิวที่ยังไม่ได้ใช้ในวันเดียวกันหรือไม่ | FR-BKG-02 |
| POST /api/booking/create | สร้างรายการจองใหม่ พร้อมคำนวณ queue_no และลด remaining_capacity | FR-BKG-03, FR-BKG-04 |
| POST /api/booking/alternatives | คืนช่วงเวลาใกล้เคียง 3 ตัวเลือก เมื่อช่วงเวลาที่เลือกเต็ม | FR-BKG-03 |
| POST /api/notifications/retry | ส่งซ้ำข้อความยืนยันเมื่อการส่งมีความล้มเหลว | FR-BKG-05, NFR-REL-02 |
| GET /api/bookings/:id | แสดงหมายเลขคิวและสถานะการจองให้ผู้ใช้เห็น | FR-BKG-04, FR-BKG-05 |

หน้าจอหลัก:
- หน้าเลือกแพ็กเกจ
- หน้าแสดงตารางช่วงเวลาและจำนวนที่นั่งคงเหลือ
- หน้ายืนยันการจอง
- หน้ารับผลตอบกลับจากการจอง พร้อมหมายเลขคิว

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | Database section, Backend section | ใช้แล้ว |
| DOM-PDPA-01 | AuditLog entity, API / หน้าจอ section | ใช้แล้ว |
| IF-IDP-01 | UserProfile entity, API validation flow | ใช้แล้ว |
| IF-HIS-01 | UserProfile entity, data model, API flow | ใช้แล้ว |
| IF-NOT-01 | NotificationQueue entity, API / หน้าจอ section | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_booking_success_updates_capacity | สร้างสถานะ verified user, มีช่วง 09.00 ว่าง 1 ที่, ยืนยันการจอง แล้วตรวจว่าบันทึกสำเร็จ แสดง queue_no และ remaining_capacity = 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_duplicate_active_queue_same_day | สร้างคิวที่ยังไม่ได้ใช้ในวันเดียวกันและลองจองใหม่อีกครั้ง ตรวจว่าปฏิเสธและแสดงหมายเลขคิวเดิม |
| AC-BKG-03 | test_AC_BKG_03_show_alternatives_when_slot_full | จำลองช่วงเวลาเต็มระหว่างการยืนยัน แล้วตรวจว่าระบบแจ้ง “ช่วงเวลาเต็ม” และเสนอ 3 ตัวเลือก โดยไม่มีซ้อนรายการจอง |
| AC-BKG-04 | test_AC_BKG_04_booking_persists_when_notification_fails | จำลอง provider แจ้งเตือนล้มเหลว ตรวจว่าการจองยังถูกบันทึก และมีรายการใน NotificationQueue ส่งซ้ำภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_slot_lookup_performance_200_users | จำลอง 200 user concurrent request ตรวจ p95 response time <= 2 วินาที |
| AC-BKG-06 | test_AC_BKG_06_audit_log_written | จำลองการเปิดดูข้อมูลการจอง ตรวจว่ามี audit log ที่มีผู้เข้าถึง เวลา และรหัสผู้รับบริการ |

## 7. ลำดับงาน

1. สร้าง schema MySQL สำหรับ Booking, SlotCapacity, NotificationQueue และ AuditLog ตาม CON-TECH-01 และ DOM-PDPA-01
2. สร้าง API ดึงข้อมูลช่วงเวลาว่างภายใน 30 วัน พร้อมจำนวนที่นั่งคงเหลือ เพื่อรองรับ FR-BKG-01 และ AC-BKG-05
3. สร้างระบบตรวจสิทธิ์และ UserProfile/lookup กับ HIS เพื่อรองรับ IF-IDP-01, IF-HIS-01, และ FR-BKG-02
4. สร้าง flow จองคิวและลด remaining_capacity พร้อมการคำนวณ queue_no ตาม ASM-04 และ FR-BKG-04
5. สร้าง logic เมื่อช่วงเวลาคนเต็ม ให้แสดง “ช่วงเวลาเต็ม” และเสนอ 3 ตัวเลือก โดยไม่ให้ซ้อนการจอง ตาม FR-BKG-03 และ AC-BKG-03
6. สร้างระบบ NotificationQueue และ retry ภายใน 5 นาที เพื่อรองรับ FR-BKG-05 และ NFR-REL-02
7. สร้างหน้าเว็บผู้ใช้สำหรับเลือกแพ็กเกจ วันและช่วงเวลา การยืนยัน และแสดงหมายเลขคิว
8. ทดสอบความถูกต้องตามทุก AC และตรวจสอบประสิทธิภาพตาม NFR-PERF-01

## 8. สิ่งที่ยังไม่ทำ

- ไม่มี Open Question ที่ค้างอยู่ในสเปคนี้หลังจากคำตัดสินของทีมแล้ว เนื่องจากข้อ “ช่วงเวลาใกล้เคียง” ได้ถูกตัดสินว่า คำนวณเฉพาะวันเดียวกันเท่านั้น

## 9. ข้อสรุปด้านความเสี่ยง

- การ race condition ระหว่างผู้ใช้สองคนที่ยืนยันพร้อมกันสามารถเกิดขึ้นได้ และต้องใช้ transaction หรือ locking บน SlotCapacity เพื่อให้ AC-BKG-03 และความถูกต้องของ remaining_capacity เป็นไปตามที่คาดไว้
- การส่งข้อความยืนยันแบบ asynchronous ต้องแยกจาก flow การบันทึกการจองให้ชัด เพื่อให้ FR-BKG-05 ไม่กระทบต่อประสบการณ์การจองหลัก
- การจัดเก็บข้อมูลสุขภาพต้องมี audit log อย่างต่อเนื่อง เพื่อให้ DOM-PDPA-01 เป็นไปตามข้อกำหนดและสามารถทดสอบได้ง่าย
