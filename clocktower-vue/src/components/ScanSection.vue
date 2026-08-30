<script setup>
import { computed } from 'vue';
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';

const lang = useLangStore();
const SITE_URL = 'http://localhost:5173/';

const qrUrl = computed(() => SITE_URL);
const qrImg = computed(() => 'https://api.qrserver.com/v1/create-qr-code/?size=340x340&margin=8&data=' + encodeURIComponent(SITE_URL));

function copyLink() {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(SITE_URL);
  }
}
function printQr() { window.print(); }
function downloadQr() {
  fetch(qrImg.value, { mode: 'cors' })
    .then(r => r.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'clocktower-qr-code.png';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
    })
    .catch(() => { window.open(qrImg.value, '_blank'); });
}
</script>

<template>
  <div class="qr-box">
    <div class="qr-frame">
      <img :src="qrImg" alt="QR Code" width="280" height="280">
    </div>
    <p class="qr-url">{{ qrUrl }}</p>
    <div class="qr-actions">
      <button class="btn btn-ghost" type="button" @click="printQr"><LineIcon name="print" size="14" color="#0A9A4A" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.print')"></span></button>
      <button class="btn btn-ghost" type="button" @click="downloadQr"><LineIcon name="download" size="14" color="#0A9A4A" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.download')"></span></button>
      <button class="btn btn-ghost" type="button" @click="copyLink"><LineIcon name="copy" size="14" color="#0A9A4A" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.copy')"></span></button>
    </div>
  </div>
</template>
