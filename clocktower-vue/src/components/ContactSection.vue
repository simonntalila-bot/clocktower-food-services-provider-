<script setup>
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';
const lang = useLangStore();
</script>

<template>
  <div class="contact-grid">
    <a class="contact-card" href="https://wa.me/255677220022" target="_blank" rel="noopener">
      <span class="em"><LineIcon name="whatsapp" size="18" color="#25D366" /></span>
      <span>
        <span class="nm">0677 220 022</span>
        <span class="tg" style="display:block;" v-html="lang.$t('contact.chat')"></span>
      </span>
    </a>
    <a class="contact-card" href="tel:+255677220022">
      <span class="em"><LineIcon name="phone" size="18" color="#0A9A4A" /></span>
      <span>
        <span class="nm">0677 220 022</span>
        <span class="tg" style="display:block;" v-html="lang.$t('contact.call')"></span>
      </span>
    </a>
    <a class="contact-card" href="mailto:clocktowercafetz2020@gmail.com">
      <span class="em"><LineIcon name="envelope" size="18" color="#ffb84d" /></span>
      <span>
        <span class="nm">clocktowercafetz2020@gmail.com</span>
        <span class="tg" style="display:block;">{{ lang.$t('contact.email') }}</span>
      </span>
    </a>
  </div>
</template>
