<script setup>
const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 16 },
  color: { type: String, default: 'currentColor' }
});

const ICONS = {
  house: ['M3 11l9-8 9 8', 'M5 9.8V21h14V9.8'],
  utensils: ['M3 2v7a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2V2', 'M6 2v20', 'M21 15V2a5 5 0 0 0-5 5v6a2 2 0 0 0 2 2h3zm0 0v7'],
  egg: ['M12 2C8.5 2 5.5 7.2 5.5 12a6.5 6.5 0 0 0 13 0C18.5 7.2 15.5 2 12 2z'],
  bowlfood: ['M4 11h16a1 1 0 0 1 1 1 8 8 0 0 1-8 8h-2a8 8 0 0 1-8-8 1 1 0 0 1 1-1z', 'M8 7c0-1 .6-1.5.6-2.5', 'M12 7c0-1 .6-1.5.6-2.5', 'M16 7c0-1 .6-1.5.6-2.5'],
  platewheat: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z', 'M12 16.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9z'],
  glasswater: ['M8 3h8l-1.2 17.2A1.8 1.8 0 0 1 13 22h-2a1.8 1.8 0 0 1-1.8-1.8L8 3z', 'M8.6 12.5c1-.8 2-.8 3 0s2 .8 3 0'],
  qrcode: ['M4 4h6v6H4z', 'M14 4h6v6h-6z', 'M4 14h6v6H4z', 'M14 14h2.5v2.5H14z', 'M20 14v.01', 'M14 20v.01', 'M17.5 17.5H20V20h-2.5z'],
  envelope: ['M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z', 'm3 7.5 9 6 9-6'],
  phone: ['M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.08 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z'],
  cart: ['circle:9,20,1.6', 'circle:19,20,1.6', 'M2.5 3h2l2.4 12.2a1.8 1.8 0 0 0 1.8 1.4h9.6a1.8 1.8 0 0 0 1.8-1.4L21.5 7H6'],
  trash: ['M3 6h18', 'M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2', 'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6', 'M10 11v6', 'M14 11v6'],
  history: ['M3.5 12a8.5 8.5 0 1 0 2.6-6.1L3.5 8.2', 'M3.5 3.5v4.7h4.7', 'M12 7.5V12l3 3'],
  users: ['M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2', 'circle:10,7,4', 'M23 21v-2a4 4 0 0 0-3-3.87', 'M16 3.13a4 4 0 0 1 0 7.75'],
  eye: ['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z', 'circle:12,12,3'],
  eyeslash: ['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z', 'circle:12,12,3', 'M4 4l16 16'],
  login: ['M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4', 'm10 17 5-5-5-5', 'M15 12H3'],
  copy: ['rect:9,9,12,12,2', 'M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1'],
  download: ['M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4', 'm7 10 5 5 5-5', 'M12 15V3'],
  print: ['M6 9V3h12v6', 'M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2', 'M6 14h12v7H6z'],
  arrowright: ['M5 12h14', 'm12 5 7 7-7 7'],
  whatsapp: ['M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 20l1-5.5A8.5 8.5 0 1 1 21 11.5z', 'M9.3 8.6c.3 2.9 3.2 5.8 6.1 6.1l1.4-1.4-2-1.3-1 .7a5.6 5.6 0 0 1-2.1-2.1l.7-1-1.3-2-1.8 1z'],
  facebook: ['M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V10H6.5v4H9v7h4v-7h2.5l.5-4h-3V7a1 1 0 0 1 1-1h2V3z'],
  instagram: ['rect:3,3,18,18,5', 'circle:12,12,4', 'M17.2 6.8v.01'],
  tiktok: ['M14 3v10.7a3.4 3.4 0 1 1-3-3.38', 'M14 3c.3 2.1 1.9 3.8 4 4.05'],
  youtube: ['rect:2.5,5.5,19,13,4', 'm10 9.3 4.5 2.7-4.5 2.7z'],
  rocket: ['M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z', 'M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z', 'M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0', 'M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5']
};
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
    :style="{ color }"
    aria-hidden="true"
  >
    <template v-for="(d, i) in ICONS[name] || []" :key="i">
      <circle v-if="String(d).startsWith('circle:')" :cx="d.split(':')[1].split(',')[0]" :cy="d.split(':')[1].split(',')[1]" :r="d.split(':')[1].split(',')[2]" />
      <rect v-else-if="String(d).startsWith('rect:')" :x="d.split(':')[1].split(',')[0]" :y="d.split(':')[1].split(',')[1]" :width="d.split(':')[1].split(',')[2]" :height="d.split(':')[1].split(',')[3]" :rx="d.split(':')[1].split(',')[4] || 2" />
      <path v-else :d="d" />
    </template>
  </svg>
</template>
