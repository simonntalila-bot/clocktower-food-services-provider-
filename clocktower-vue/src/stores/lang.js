import { defineStore } from 'pinia';
import { ref } from 'vue';
import { t, foodName, foodDesc, LANG } from '../i18n';

export const useLangStore = defineStore('lang', () => {
  const lang = ref(localStorage.getItem('ctfLang') || 'en');

  function setLang(l) {
    lang.value = l;
    localStorage.setItem('ctfLang', l);
    document.documentElement.lang = l;
    document.title = l === 'sw'
      ? 'CLOCKTOWER FOOD SERVICE PROVIDER — Agiza Chakula'
      : 'CLOCKTOWER FOOD SERVICE PROVIDER — Order Food Online';
  }

  function $t(key) { return t(key, lang.value); }
  function $foodName(f) { return foodName(f, lang.value); }
  function $foodDesc(f) { return foodDesc(f, lang.value); }

  // Initialize
  document.documentElement.lang = lang.value;

  return { lang, setLang, $t, $foodName, $foodDesc };
});
