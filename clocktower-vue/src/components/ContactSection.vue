<script setup>
import { useLangStore } from '../stores/lang';
const lang = useLangStore();
</script>

<template>
  <div class="contact-grid">
    <a class="contact-card" href="https://wa.me/255629290952" target="_blank" rel="noopener">
      <span class="em"><i class="fab fa-whatsapp" aria-hidden="true"></i></span>
      <span>
        <span class="nm">0629 290 952</span>
        <span class="tg" style="display:block;" v-html="lang.$t('contact.chat')"></span>
      </span>
    </a>
    <a class="contact-card" href="https://wa.me/255759597199" target="_blank" rel="noopener">
      <span class="em"><i class="fas fa-phone" aria-hidden="true"></i></span>
      <span>
        <span class="nm">0759 597 199</span>
        <span class="tg" style="display:block;" v-html="lang.$t('contact.call')"></span>
      </span>
    </a>
  </div>
</template>
