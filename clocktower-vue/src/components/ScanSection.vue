<script setup>
import { computed } from 'vue';
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';

const lang = useLangStore();
const SITE_URL = 'https://simonntalila-bot.github.io/clocktower-food-services-provider-/';

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
  <div class="scan-layout">
    <div class="scan-qr">
      <div class="qr-table">
        <div class="qr-table-head">
          <LineIcon name="clocktower" size="22" color="#F57C00" />
          <span class="qt-w">{{ lang.$t('qr.welcome') }}</span>
          <span class="qt-brand">CLOCKTOWER</span>
          <span class="qt-sub">{{ lang.$t('qr.welcome2') }}</span>
        </div>
        <div class="qr-table-code">
          <img :src="qrImg" alt="QR Code" width="300" height="300">
        </div>
        <div class="qr-table-foot">
          <LineIcon name="heart" size="13" color="#F57C00" />
          {{ lang.$t('qr.thanks') }}
          <LineIcon name="heart" size="13" color="#F57C00" />
        </div>
      </div>

      <div class="qr-actions">
        <button class="btn btn-ghost" type="button" @click="printQr"><LineIcon name="print" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.print')"></span></button>
        <button class="btn btn-ghost" type="button" @click="downloadQr"><LineIcon name="download" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.download')"></span></button>
        <button class="btn btn-ghost" type="button" @click="copyLink"><LineIcon name="copy" size="14" color="#0A5C36" style="vertical-align:-2px" /> <span v-html="lang.$t('qr.copy')"></span></button>
      </div>
    </div>
  </div>
</template>