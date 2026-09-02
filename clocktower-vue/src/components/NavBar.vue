<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '../stores/cart';
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';

const router = useRouter();
const cart = useCartStore();
const lang = useLangStore();

const emit = defineEmits(['set-filter']);
const props = defineProps({
  ghost: { type: Boolean, default: false }
});
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
  mobileOpen.value = false;
}

function goSection(id) {
  if (router.currentRoute.value.path !== '/') {
    router.push('/').then(() => {
      requestAnimationFrame(() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' }));
    });
  } else {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }
  mobileOpen.value = false;
}

function goHome() {
  if (router.currentRoute.value.path !== '/') {
    router.push('/');
  } else {
    document.getElementById('home')?.scrollIntoView({ behavior: 'smooth' });
  }
  mobileOpen.value = false;
}

function goToLogin() {
  router.push('/login');
  mobileOpen.value = false;
}

function onScroll() {
  scrolled.value = window.scrollY > 20;
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true });
});
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll);
});
</script>

<template>
  <header class="nav" :class="{ 'nav-scrolled': scrolled, 'nav-ghost': props.ghost && !scrolled }">
    <div class="nav-inner">
      <a class="brand" href="#home" @click.prevent="goHome">
        <span class="brand-row">
          <img class="brand-logo" src="../assets/logo.png" alt="ClockTower logo">
          <span class="brand-badge" aria-hidden="true">
            <LineIcon name="clocktower" size="26" color="#0A5C36" />
          </span>
        </span>
        <span class="b2">{{ lang.$t('nav.brand') }}</span>
      </a>
      <nav>
        <ul class="nav-links">
          <li>
            <a href="#home" @click.prevent="goHome">
              <LineIcon name="house" size="15" />
              <span>{{ lang.$t('nav.home') }}</span>
            </a>
          </li>
          <li>
            <a href="#menu" @click.prevent="goSection('menu')">
              <LineIcon name="utensils" size="15" />
              <span>{{ lang.$t('nav.menu') }}</span>
            </a>
          </li>
          <li>
            <a href="#scan" @click.prevent="goSection('scan')">
              <LineIcon name="qrcode" size="15" />
              <span>{{ lang.$t('nav.scan') }}</span>
            </a>
          </li>
          <li>
            <a href="#contact" @click.prevent="goSection('contact')">
              <LineIcon name="phone" size="15" />
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
          <LineIcon name="login" size="15" color="#0A5C36" />
          <span class="lbl">{{ lang.$t('nav.login') || 'Login' }}</span>
        </button>
        <button class="cart-btn" :class="{ 'has-items': cart.cartQuantity > 0 }" type="button" @click="cart.showCart = true">
          <LineIcon name="cart" size="16" color="#ffffff" />
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
    <a href="#home" @click.prevent="goHome">
      <LineIcon name="house" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.home') }}</span>
    </a>
    <a href="#menu" @click.prevent="goSection('menu')">
      <LineIcon name="utensils" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.menu') }}</span>
    </a>
    <a v-for="cat in dropCats" :key="cat.key" href="#menu" @click.prevent="handleFilter(cat)" class="mobile-sub">
      <LineIcon :name="cat.icon" size="15" color="#0A5C36" />
      <span>{{ lang.$t('cat.' + cat.key) }}</span>
    </a>
    <a href="#scan" @click.prevent="goSection('scan')">
      <LineIcon name="qrcode" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.scan') }}</span>
    </a>
    <a href="#contact" @click.prevent="goSection('contact')">
      <LineIcon name="phone" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.contact') }}</span>
    </a>
    <button class="mobile-login" type="button" @click="goToLogin">
      <LineIcon name="login" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.login') || 'Login' }}</span>
    </button>
    <button class="mobile-login muted" type="button" @click="router.push('/admin-panel/activity')">
      <LineIcon name="history" size="15" color="#0A5C36" />
      <span>{{ lang.$t('nav.activityLogs') }}</span>
    </button>
  </div>
</template>