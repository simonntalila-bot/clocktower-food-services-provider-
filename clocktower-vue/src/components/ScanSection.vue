<script setup>
import { computed } from 'vue';
import { useLangStore } from '../stores/lang';

const lang = useLangStore();
const SITE_URL = 'https://simonntalila-bot.github.io/clocktower-food-services-provider-';

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
      <button class="btn btn-ghost" type="button" @click="printQr"><i class="fas fa-print" aria-hidden="true"></i> <span v-html="lang.$t('qr.print')"></span></button>
      <button class="btn btn-ghost" type="button" @click="downloadQr"><i class="fas fa-download" aria-hidden="true"></i> <span v-html="lang.$t('qr.download')"></span></button>
      <button class="btn btn-ghost" type="button" @click="copyLink"><i class="fas fa-copy" aria-hidden="true"></i> <span v-html="lang.$t('qr.copy')"></span></button>
    </div>
  </div>
</template>
