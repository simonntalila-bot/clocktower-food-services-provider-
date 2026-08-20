<script setup>
import { useLangStore } from '../stores/lang';
const lang = useLangStore();
const year = new Date().getFullYear();
</script>

<template>
  <footer>
    <div class="foot-social">
      <a href="https://wa.me/255629290952" target="_blank" rel="noopener" aria-label="WhatsApp">
        <i class="fab fa-whatsapp" style="font-size:18px" aria-hidden="true"></i>
      </a>
      <a href="https://www.facebook.com" target="_blank" rel="noopener" aria-label="Facebook">
        <i class="fab fa-facebook-f" style="font-size:18px" aria-hidden="true"></i>
      </a>
      <a href="https://www.instagram.com" target="_blank" rel="noopener" aria-label="Instagram">
        <i class="fab fa-instagram" style="font-size:18px" aria-hidden="true"></i>
      </a>
      <a href="https://www.tiktok.com" target="_blank" rel="noopener" aria-label="TikTok">
        <i class="fab fa-tiktok" style="font-size:18px" aria-hidden="true"></i>
      </a>
      <a href="https://www.youtube.com" target="_blank" rel="noopener" aria-label="YouTube">
        <i class="fab fa-youtube" style="font-size:18px" aria-hidden="true"></i>
      </a>
    </div>
    <div class="foot-note" v-html="lang.$t('foot.note')"></div>
    <div style="margin-top:10px;">&copy; {{ year }} <b>CLOCKTOWER FOOD SERVICE PROVIDER</b> &mdash; <span v-html="lang.$t('footer.tag')"></span></div>
  </footer>
</template>
