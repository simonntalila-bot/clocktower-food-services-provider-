<script setup>
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';
const lang = useLangStore();
const year = new Date().getFullYear();
</script>

<template>
  <footer>
    <div class="foot-social">
      <a href="https://wa.me/255677220022" target="_blank" rel="noopener" aria-label="WhatsApp">
        <LineIcon name="whatsapp" size="18" color="#25D366" />
      </a>
      <a href="https://www.facebook.com" target="_blank" rel="noopener" aria-label="Facebook">
        <LineIcon name="facebook" size="18" color="#1877F2" />
      </a>
      <a href="https://www.instagram.com" target="_blank" rel="noopener" aria-label="Instagram">
        <LineIcon name="instagram" size="18" color="#E4405F" />
      </a>
      <a href="https://www.tiktok.com" target="_blank" rel="noopener" aria-label="TikTok">
        <LineIcon name="tiktok" size="18" color="#25F4EE" />
      </a>
      <a href="https://www.youtube.com" target="_blank" rel="noopener" aria-label="YouTube">
        <LineIcon name="youtube" size="18" color="#FF0000" />
      </a>
    </div>
    <div class="foot-note" v-html="lang.$t('foot.note')"></div>
    <div style="margin-top:10px;">&copy; {{ year }} <b v-html="lang.$t('footer.brand')"></b> &mdash; <span v-html="lang.$t('footer.tag')"></span></div>
  </footer>
</template>
