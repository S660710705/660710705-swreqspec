import SlotPicker from './pages/SlotPicker.jsx'

// โครงเริ่มต้นของรายวิชา: เปลี่ยนหน้าหลักให้แสดงหน้าจอของ T-09
export default function App() {
  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <SlotPicker />
    </main>
  )
}
