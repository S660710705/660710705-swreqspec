import { render, screen } from '@testing-library/react'

import SlotPicker from '../pages/SlotPicker.jsx'

test('T-09 แสดงรายการ slot และจำนวนที่นั่งคงเหลือ', async () => {
  const fakeClient = {
    async getSlots({ packageCode }) {
      return {
        slots: [
          { slot_date: '2026-09-24', start_time: '09:00', package_code: packageCode, capacity: 10, remaining: 3 },
          { slot_date: '2026-09-24', start_time: '10:00', package_code: packageCode, capacity: 10, remaining: 1 },
        ],
      }
    },
  }

  render(<SlotPicker client={fakeClient} />)

  expect(await screen.findByText('เลือกแพ็กเกจและช่วงเวลา')).toBeTruthy()
  expect(screen.getAllByText('2026-09-24').length).toBeGreaterThan(0)
  expect(screen.getByText('เวลา: 09:00')).toBeTruthy()
  expect(screen.getByText('เวลา: 10:00')).toBeTruthy()
  expect(screen.getByText(/เหลือ 3 ที่/)).toBeTruthy()
  expect(screen.getByText(/เหลือ 1 ที่/)).toBeTruthy()
})
