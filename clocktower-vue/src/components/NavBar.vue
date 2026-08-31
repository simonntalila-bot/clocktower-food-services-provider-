<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '../stores/cart';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';
import LineIcon from './LineIcon.vue';

const router = useRouter();
const cart = useCartStore();
const lang = useLangStore();
const menu = useMenuStore();

const emit = defineEmits(['set-filter']);
const menuDropOpen = ref(false);
const mobileOpen = ref(false);
const scrolled = ref(false);

const dropCats = [
  { key: 'breakfast', icon: 'egg' },
  { key: 'visinia', icon: 'bowlfood' },
  { key: 'meals', icon: 'platewheat' },
  { key: 'drinks', icon: 'glasswater' }
];

function handleFilter(cat) {
  emit('set-filter', cat.key === 'meals' ? 'lunch' : cat.key);
  menuDropOpen.value = false;
  mobileOpen.value = false;
}

function onDocClick(e) {
  if (!e.target.closest('.nav-drop')) menuDropOpen.value = false;
}

function scrollTo(id) {
  if (window.location.pathname !== '/') {
    router.push('/');
    setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' }), 100);
  } else {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }
  mobileOpen.value = false;
}

function goToLogin() {
  router.push('/login');
  mobileOpen.value = false;
}

function toggleDrop() {
  menuDropOpen.value = !menuDropOpen.value;
}

function onScroll() {
  scrolled.value = window.scrollY > 20;
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('click', onDocClick);
});
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll);
  document.removeEventListener('click', onDocClick);
});
</script>

<template>
  <header class="nav" :class="{ 'nav-scrolled': scrolled }">
    <div class="nav-inner">
      <a class="brand" href="#home" @click.prevent="scrollTo('home')">
        <img class="brand-logo" src="../assets/logo.png" alt="ClockTower logo">
        <span class="b2">food service provider</span>
      </a>
      <nav>
        <ul class="nav-links">
          <li>
            <a href="#home" @click.prevent="scrollTo('home')">
              <LineIcon name="house" size="15" color="#0A9A4A" />
              <span>{{ lang.$t('nav.home') }}</span>
            </a>
          </li>
          <li class="drop nav-drop" :class="{ open: menuDropOpen }">
            <button class="drop-trigger" type="button" @click="toggleDrop">
              <LineIcon name="utensils" size="15" color="#0A9A4A" />
              <span>{{ lang.$t('nav.menu') }}</span>
              <svg class="car" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
            </button>
            <div class="drop-menu">
              <a v-for="cat in dropCats" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat)">
                <span class="em"><LineIcon :name="cat.icon" size="16" color="#0A9A4A" /></span>
                <span>{{ lang.$t('cat.' + cat.key) }}</span>
              </a>
            </div>
          </li>
          <li>
            <a href="#scan" @click.prevent="scrollTo('scan')">
              <LineIcon name="qrcode" size="15" color="#0A9A4A" />
              <span>{{ lang.$t('nav.scan') }}</span>
            </a>
          </li>
          <li>
            <a href="#contact" @click.prevent="scrollTo('contact')">
              <LineIcon name="envelope" size="15" color="#0A9A4A" />
              <span>{{ lang.$t('nav.contact') }}</span>
            </a>
          </li>
        </ul>
      </nav>
      <div class="nav-actions">
        <div class="lang-switch">
          <button class="lang-btn" :class="{ active: lang.lang === 'en' }" type="button" @click="lang.setLang('en')">EN</button>
          <button class="lang-btn" :class="{ active: lang.lang === 'sw' }" type="button" @click="lang.setLang('sw')">SW</button>
        </div>
        <button class="login-btn" type="button" @click="goToLogin">
          <LineIcon name="login" size="15" color="#ffb84d" />
          <span class="lbl">Login</span>
        </button>
        <button class="cart-btn" :class="{ 'has-items': cart.cartQuantity > 0 }" type="button" @click="cart.showCart = true">
          <LineIcon name="cart" size="16" color="#ffb84d" />
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
      <LineIcon name="house" size="15" color="#0A9A4A" />
      <span>{{ lang.$t('nav.home') }}</span>
    </a>
    <a href="#menu" @click.prevent="scrollTo('menu')">
      <LineIcon name="utensils" size="15" color="#0A9A4A" />
      <span>{{ lang.$t('nav.menu') }}</span>
    </a>
    <a v-for="cat in dropCats" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat)" class="mobile-sub">
      <LineIcon :name="cat.icon" size="15" color="#0A9A4A" />
      <span>{{ lang.$t('cat.' + cat.key) }}</span>
    </a>
    <a href="#scan" @click.prevent="scrollTo('scan')">
      <LineIcon name="qrcode" size="15" color="#0A9A4A" />
      <span>{{ lang.$t('nav.scan') }}</span>
    </a>
    <a href="#contact" @click.prevent="scrollTo('contact')">
      <LineIcon name="envelope" size="15" color="#0A9A4A" />
      <span>{{ lang.$t('nav.contact') }}</span>
    </a>
    <button class="mobile-login" type="button" @click="goToLogin">
      <LineIcon name="login" size="15" color="#ffb84d" />
      <span>Login</span>
    </button>
    <button class="mobile-login muted" type="button" @click="router.push('/admin-panel/activity')">
      <LineIcon name="history" size="15" color="#ffb84d" />
      <span>Activity Logs</span>
    </button>
  </div>
</template>
