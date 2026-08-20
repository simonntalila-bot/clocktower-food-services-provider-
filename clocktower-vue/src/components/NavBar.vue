<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useCartStore } from '../stores/cart';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const cart = useCartStore();
const lang = useLangStore();
const menu = useMenuStore();

const emit = defineEmits(['open-cart', 'set-filter']);
const menuDropOpen = ref(false);
const mobileOpen = ref(false);
const scrolled = ref(false);

const categories = [
  { key: 'breakfast', icon: 'fa-egg', bg: 'rgba(255,184,77,0.12)' },
  { key: 'lunch', icon: 'fa-bowl-food', bg: 'rgba(52,211,153,0.12)' },
  { key: 'dinner', icon: 'fa-drumstick-bite', bg: 'rgba(167,139,250,0.14)' },
  { key: 'drinks', icon: 'fa-glass-water', bg: 'rgba(56,189,248,0.14)' },
  { key: 'desserts', icon: 'fa-ice-cream', bg: 'rgba(251,191,36,0.14)' }
];

const navLinks = [
  { id: 'home', icon: 'fa-house', labelKey: 'nav.home' },
  { id: 'services', icon: 'fa-concierge-bell', labelKey: 'nav.services' },
  { id: 'about', icon: 'fa-circle-info', labelKey: 'nav.about' },
  { id: 'scan', icon: 'fa-qrcode', labelKey: 'nav.scan' },
  { id: 'contact', icon: 'fa-envelope', labelKey: 'nav.contact' },
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

function onScroll() {
  scrolled.value = window.scrollY > 20;
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }));
onUnmounted(() => window.removeEventListener('scroll', onScroll));
</script>

<template>
  <header class="nav" :class="{ 'nav-scrolled': scrolled }">
    <div class="nav-inner">
      <a class="brand" href="#home" @click.prevent="scrollTo('home')">
        <span class="b1">CLOCKTOWER<em>.</em></span>
        <span class="b2">Food Service Provider</span>
      </a>
      <nav>
        <ul class="nav-links">
          <li v-for="link in navLinks" :key="link.id">
            <a :href="'#' + link.id" @click.prevent="scrollTo(link.id)">
              <i class="fas" :class="link.icon" aria-hidden="true"></i>
              <span>{{ lang.$t(link.labelKey) }}</span>
            </a>
          </li>
          <li class="drop" :class="{ open: menuDropOpen }">
            <button class="drop-trigger" type="button" @click="toggleDrop">
              <i class="fas fa-utensils" aria-hidden="true"></i>
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
          <li>
            <a href="admin.html" class="nav-login-link">
              <i class="fas fa-right-to-bracket" aria-hidden="true"></i>
              <span>Login</span>
            </a>
          </li>
        </ul>
      </nav>
      <div class="nav-actions">
        <div class="lang-switch">
          <button class="lang-btn" :class="{ active: lang.lang === 'en' }" type="button" @click="lang.setLang('en')">EN</button>
          <button class="lang-btn" :class="{ active: lang.lang === 'sw' }" type="button" @click="lang.setLang('sw')">SW</button>
        </div>
        <a href="admin.html" class="login-btn">
          <i class="fas fa-right-to-bracket" aria-hidden="true"></i>
          <span class="lbl">Login</span>
        </a>
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
    <a href="#home" @click.prevent="scrollTo('home')">
      <i class="fas fa-house" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.home') }}</span>
    </a>
    <a href="#menu" @click.prevent="scrollTo('menu')">
      <i class="fas fa-utensils" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.menu') }}</span>
    </a>
    <a v-for="cat in categories" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat.key)" class="mobile-sub">
      <i class="fas" :class="cat.icon" aria-hidden="true"></i>
      <span>{{ lang.$t('cat.' + cat.key) }}</span>
    </a>
    <a href="#services" @click.prevent="scrollTo('services')">
      <i class="fas fa-concierge-bell" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.services') }}</span>
    </a>
    <a href="#about" @click.prevent="scrollTo('about')">
      <i class="fas fa-circle-info" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.about') }}</span>
    </a>
    <a href="#scan" @click.prevent="scrollTo('scan')">
      <i class="fas fa-qrcode" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.scan') }}</span>
    </a>
    <a href="#contact" @click.prevent="scrollTo('contact')">
      <i class="fas fa-envelope" aria-hidden="true"></i>
      <span>{{ lang.$t('nav.contact') }}</span>
    </a>
    <a href="admin.html" class="mobile-login">
      <i class="fas fa-right-to-bracket" aria-hidden="true"></i>
      <span>Login</span>
    </a>
  </div>
</template>
