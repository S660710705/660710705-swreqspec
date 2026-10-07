import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

const PACKAGE_OPTIONS = [
  { value: 'basic', label: 'แพ็กเกจพื้นฐาน' },
  { value: 'premium', label: 'แพ็กเกจพรีเมียม' },
]

// รองรับ FR-BKG-01 และ FR-BKG-06
export default function SlotPicker({ client = api }) {
  const [packageCode, setPackageCode] = useState(PACKAGE_OPTIONS[0].value)
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    const loadSlots = async () => {
      try {
        setLoading(true)
        setError('')
        const today = new Date().toISOString().slice(0, 10)
        const response = await client.getSlots({ dateFrom: today, packageCode })
        const nextSlots = Array.isArray(response?.slots) ? response.slots : []

        if (isMounted) {
          setSlots(nextSlots)
        }
      } catch (err) {
        if (isMounted) {
          setSlots([])
          setError('ไม่สามารถโหลดช่วงเวลาว่างได้ กรุณาลองใหม่อีกครั้ง')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadSlots()
    return () => {
      isMounted = false
    }
  }, [client, packageCode])

  return (
    <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.08em] text-teal-700">เลือกช่วงเวลา</p>
          <h2 className="mt-1 text-2xl font-bold text-slate-800">เลือกแพ็กเกจและช่วงเวลา</h2>
        </div>
      </div>

      <label className="mb-4 block">
        <span className="mb-2 block text-sm font-medium text-slate-700">แพ็กเกจ</span>
        <select
          aria-label="แพ็กเกจ"
          value={packageCode}
          onChange={(event) => setPackageCode(event.target.value)}
          className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 outline-none focus:border-teal-500"
        >
          {PACKAGE_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>

      {loading ? (
        <p className="text-sm text-slate-500">กำลังโหลดช่วงเวลาว่าง...</p>
      ) : error ? (
        <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</p>
      ) : slots.length === 0 ? (
        <p className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">
          ยังไม่มีช่วงเวลาว่างในช่วงนี้
        </p>
      ) : (
        <div className="grid gap-3 md:grid-cols-2">
          {slots.map((slot) => (
            <button
              key={`${slot.slot_date}-${slot.start_time}-${slot.package_code ?? packageCode}`}
              type="button"
              className="rounded-xl border border-teal-200 bg-teal-50 p-4 text-left transition hover:border-teal-500 hover:bg-teal-100"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-base font-semibold text-slate-800">{slot.slot_date}</span>
                <span className="rounded-full bg-white px-2 py-1 text-xs font-semibold text-teal-700">
                  เหลือ {slot.remaining} ที่
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-600">เวลา: {slot.start_time}</p>
              <p className="mt-1 text-xs text-slate-500">ความจุ {slot.capacity} ที่</p>
            </button>
          ))}
        </div>
      )}
    </section>
  )
}
