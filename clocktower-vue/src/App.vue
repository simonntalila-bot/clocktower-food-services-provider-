<script setup>
import { ref, nextTick } from 'vue';
import { useCartStore } from './stores/cart';
import { useMenuStore } from './stores/menu';
import { useLangStore } from './stores/lang';

import NavBar from './components/NavBar.vue';
import HeroSection from './components/HeroSection.vue';
import ServiceCategories from './components/ServiceCategories.vue';
import HowItWorks from './components/HowItWorks.vue';
import MenuSection from './components/MenuSection.vue';
import ScanSection from './components/ScanSection.vue';
import Testimonials from './components/Testimonials.vue';
import ContactSection from './components/ContactSection.vue';
import AppFooter from './components/AppFooter.vue';
import FoodDetailModal from './components/FoodDetailModal.vue';
import CartSidebar from './components/CartSidebar.vue';
import CheckoutModal from './components/CheckoutModal.vue';
import ConfirmModal from './components/ConfirmModal.vue';
import OrderHistory from './components/OrderHistory.vue';
import Toast from './components/Toast.vue';

const cart = useCartStore();
const menu = useMenuStore();
const lang = useLangStore();

const toastRef = ref(null);
const detailFood = ref(null);
const showDetail = ref(false);
const showCart = ref(false);
const showCheckout = ref(false);
const showHistory = ref(false);
const showConfirm = ref(false);
const confirmData = ref({ orderNum: '', total: 0, customerName: '' });

function scrollToMenu() {
  document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' });
}

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
}

function handleSetFilter(cat) {
  menu.setFilter(cat);
  nextTick(() => scrollToMenu());
}

function openDetail(foodId) {
  detailFood.value = menu.byId(foodId);
  showDetail.value = true;
}

function addToCart(foodId, qty) {
  cart.addToCart(foodId, qty);
  const food = menu.byId(foodId);
  toastRef.value?.showToast(
    (food ? (lang.lang === 'sw' && food.nameSw ? food.nameSw : food.name) : 'Item') + ' added to cart',
    '✓'
  );
}

function handleOrderPlaced(info) {
  showCheckout.value = false;
  confirmData.value = info;
  showConfirm.value = true;
}
</script>

<template>
  <NavBar
    @open-cart="showCart = true"
    @set-filter="handleSetFilter"
  />

  <HeroSection
    @scroll-to-menu="scrollToMenu"
    @open-cart="showCart = true"
  />

  <main>
    <ServiceCategories @set-filter="handleSetFilter" />

    <MenuSection
      id="menu"
      @open-food="openDetail"
    />

    <HowItWorks @scroll-to-menu="scrollToMenu" />

    <section id="scan" class="section">
      <div class="container">
        <div class="section-head" style="justify-content:center;text-align:center">
          <div class="dot"></div>
          <h2>{{ lang.$t('qr.title') }}</h2>
          <div class="line"></div>
        </div>
        <ScanSection />
      </div>
    </section>

    <section id="testi" class="section">
      <div class="container">
        <div class="section-head" style="justify-content:center;text-align:center">
          <div class="dot"></div>
          <h2>{{ lang.$t('testi.title') }}</h2>
          <div class="line"></div>
        </div>
        <Testimonials />
      </div>
    </section>

    <section id="contact" class="section">
      <div class="container">
        <div class="section-head" style="justify-content:center;text-align:center">
          <div class="dot"></div>
          <h2>{{ lang.$t('contact.head') }}</h2>
          <div class="line"></div>
        </div>
        <ContactSection />
      </div>
    </section>
  </main>

  <AppFooter />

  <FoodDetailModal
    :show="showDetail"
    :food="detailFood"
    @close="showDetail = false"
    @add-to-cart="addToCart"
  />

  <CartSidebar
    :show="showCart"
    @close="showCart = false"
    @open-checkout="showCart = false; showCheckout = true"
    @open-history="showCart = false; showHistory = true"
  />

  <CheckoutModal
    :show="showCheckout"
    @close="showCheckout = false"
    @order-placed="handleOrderPlaced"
  />

  <ConfirmModal
    :show="showConfirm"
    :order-num="confirmData.orderNum"
    :total="confirmData.total"
    :customer-name="confirmData.customerName"
    @close="showConfirm = false"
  />

  <OrderHistory
    :show="showHistory"
    @close="showHistory = false"
  />

  <Toast ref="toastRef" />
</template>
