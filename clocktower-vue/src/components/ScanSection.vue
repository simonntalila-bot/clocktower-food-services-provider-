<script setup>
import { computed } from 'vue';
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';

const lang = useLangStore();
const SITE_URL = 'https://simonntalila-bot.github.io/clocktower-food-services-provider-/';

const qrUrl = computed(() => SITE_URL);
const qrImg = computed(() => 'https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=4&data=' + encodeURIComponent(SITE_URL));

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
  <div class="scan-layout" style="display:flex;justify-content:center;align-items:center;flex-direction:column;text-align:center">
    <div class="scan-qr">
      <img :src="qrImg" alt="QR Code" width="220" height="220" style="border-radius:8px">
      <p style="margin-top:10px;font-size:12px;color:#666;word-break:break-all">https://simonntalila-bot.github.io/clocktower-food-services-provider-/</p>
      
      <div class="qr-actions" style="margin-top:16px;display:flex;gap:8px;justify-content:center">
        <button class="btn btn-ghost" type="button" @click="printQr"><LineIcon name="print" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.print')"></span></button>
        <button class="btn btn-ghost" type="button" @click="downloadQr"><LineIcon name="download" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.download')"></span></button>
        <button class="btn btn-ghost" type="button" @click="copyLink"><LineIcon name="copy" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.copy')"></span></button>
      </div>
    </div>
  </div>
</template>