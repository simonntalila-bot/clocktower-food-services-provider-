<script setup>
import { ref } from 'vue';
import { useCartStore } from '../stores/cart';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const cart = useCartStore();
const lang = useLangStore();
const menu = useMenuStore();

const emit = defineEmits(['open-cart', 'set-filter']);
const menuDropOpen = ref(false);
const mobileOpen = ref(false);

const categories = [
  { key: 'breakfast', icon: 'fa-egg', bg: 'rgba(255,184,77,0.12)' },
  { key: 'lunch', icon: 'fa-bowl-food', bg: 'rgba(52,211,153,0.12)' },
  { key: 'dinner', icon: 'fa-drumstick-bite', bg: 'rgba(167,139,250,0.14)' },
  { key: 'drinks', icon: 'fa-glass-water', bg: 'rgba(56,189,248,0.14)' },
  { key: 'desserts', icon: 'fa-ice-cream', bg: 'rgba(251,191,36,0.14)' }
];

function handleFilter(cat) {
  emit('set-filter', cat);
  menuDropOpen.value = false;
  mobileOpen.value = false;
}

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  mobileOpen.value = false;
}

function toggleDrop() {
  menuDropOpen.value = !menuDropOpen.value;
}
</script>

<template>
  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="#home" @click.prevent="scrollTo('home')">
        <span class="b1">CLOCKTOWER<em>.</em></span>
        <span class="b2">Food Service Provider</span>
      </a>
      <nav>
        <ul class="nav-links">
          <li><a href="#home" @click.prevent="scrollTo('home')">{{ lang.$t('nav.home') }}</a></li>
          <li class="drop" :class="{ open: menuDropOpen }">
            <button class="drop-trigger" type="button" @click="toggleDrop">
              <span>{{ lang.$t('nav.menu') }}</span>
              <svg class="car" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
            </button>
            <div class="drop-menu">
              <a v-for="cat in categories" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat.key)">
                <span class="em" :style="{ background: cat.bg }"><i class="fas" :class="cat.icon" aria-hidden="true"></i></span>
                <span>{{ lang.$t('cat.' + cat.key) }}</span>
              </a>
            </div>
          </li>
          <li><a href="#services" @click.prevent="scrollTo('services')">{{ lang.$t('nav.services') }}</a></li>
          <li><a href="#about" @click.prevent="scrollTo('about')">{{ lang.$t('nav.about') }}</a></li>
          <li><a href="#scan" @click.prevent="scrollTo('scan')">{{ lang.$t('nav.scan') }}</a></li>
          <li><a href="#contact" @click.prevent="scrollTo('contact')">{{ lang.$t('nav.contact') }}</a></li>
          <li><a href="admin.html" style="color:var(--accent);font-weight:600;">Login</a></li>
        </ul>
      </nav>
      <div style="display:flex;align-items:center;gap:8px;">
        <div class="lang-switch">
          <button class="lang-btn" :class="{ active: lang.lang === 'en' }" type="button" @click="lang.setLang('en')">EN</button>
          <button class="lang-btn" :class="{ active: lang.lang === 'sw' }" type="button" @click="lang.setLang('sw')">SW</button>
        </div>
        <a href="admin.html" class="login-btn"> <span class="lbl">Login</span></a>
        <button class="cart-btn" :class="{ 'has-items': cart.cartQuantity > 0 }" type="button" @click="emit('open-cart')">
          <i class="fas fa-shopping-cart" aria-hidden="true"></i>
          <span class="lbl">{{ lang.$t('nav.cart') }}</span>
          <span class="cnt">{{ cart.cartQuantity }}</span>
        </button>
        <button class="nav-toggle" :class="{ active: mobileOpen }" type="button" aria-label="Menu" @click="mobileOpen = !mobileOpen">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-menu" :class="{ open: mobileOpen }">
    <a href="#home" @click.prevent="scrollTo('home')">{{ lang.$t('nav.home') }}</a>
    <a href="#menu" @click.prevent="scrollTo('menu')">{{ lang.$t('nav.menu') }}</a>
    <a v-for="cat in categories" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat.key)">
      <i class="fas" :class="cat.icon" aria-hidden="true"></i>
      <span>{{ lang.$t('cat.' + cat.key) }}</span>
    </a>
    <a href="#services" @click.prevent="scrollTo('services')">{{ lang.$t('nav.services') }}</a>
    <a href="#about" @click.prevent="scrollTo('about')">{{ lang.$t('nav.about') }}</a>
    <a href="#scan" @click.prevent="scrollTo('scan')">{{ lang.$t('nav.scan') }}</a>
    <a href="#contact" @click.prevent="scrollTo('contact')">{{ lang.$t('nav.contact') }}</a>
    <a href="admin.html" style="color:var(--accent);font-weight:600;">Login</a>
  </div>
</template>
