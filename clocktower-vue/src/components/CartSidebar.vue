<script setup>
import { useLangStore } from '../stores/lang';
import { useCartStore } from '../stores/cart';
import { useMenuStore } from '../stores/menu';
import LineIcon from './LineIcon.vue';

const props = defineProps({ show: Boolean });
const emit = defineEmits(['close', 'open-checkout', 'open-history']);
const lang = useLangStore();
const cart = useCartStore();
const menu = useMenuStore();

function fmt(n) { return 'TSh ' + n.toLocaleString('en'); }
</script>

<template>
  <div class="overlay" :class="{ show: show }" @click="emit('close')"></div>
  <aside class="cart-sidebar" :class="{ show: show }">
    <div class="cart-head">
      <h3 v-html="lang.$t('cart.head')"></h3>
      <button class="close-x" type="button" aria-label="Close" @click="emit('close')">&times;</button>
    </div>

    <template v-if="cart.cartQuantity === 0">
      <div class="cart-empty">
        <span class="em"><LineIcon name="cart" size="26" color="#0A9A4A" /></span>
        <h3 style="margin:0;font-family:'Space Grotesk',sans-serif;">{{ lang.$t('cart.empty') }}</h3>
        <p>{{ lang.$t('cart.emptySub') }}</p>
        <button class="btn btn-primary" type="button" @click="emit('close')">{{ lang.$t('cart.browse') }}</button>
      </div>
    </template>

    <template v-else>
      <div class="cart-list">
        <div class="cart-item" v-for="item in cart.items" :key="item.foodId">
          <div class="ci-img">
            <template v-if="menu.byId(item.foodId)?.img">
              <img :src="menu.byId(item.foodId).img" :alt="lang.$foodName(menu.byId(item.foodId))" loading="lazy" />
            </template>
            <template v-else>
              <span style="font-size:26px;">{{ menu.byId(item.foodId)?.icon }}</span>
            </template>
          </div>
          <div class="ci-mid">
            <div class="ci-name">{{ lang.$foodName(menu.byId(item.foodId)) }}</div>
            <div class="ci-unit">{{ fmt(menu.byId(item.foodId).price) }} {{ lang.$t('cart.each') }}</div>
            <div class="ci-bottom">
              <div class="qty">
                <button type="button" @click="cart.changeQty(item.foodId, -1)">−</button>
                <span class="qv">{{ item.quantity }}</span>
                <button type="button" @click="cart.changeQty(item.foodId, 1)">+</button>
              </div>
              <button type="button" class="cart-remove" aria-label="Remove" @click="cart.removeItem(item.foodId)">
                <LineIcon name="trash" size="14" color="#e5484d" />
              </button>
            </div>
          </div>
          <div class="ci-line">{{ fmt(menu.byId(item.foodId).price * item.quantity) }}</div>
        </div>
      </div>
      <div class="cart-foot">
        <div class="cart-total-row">
          <span>{{ lang.$t('cart.subtotal') }}</span>
          <b>{{ fmt(cart.cartSubtotal) }}</b>
        </div>
        <button class="checkout-btn" type="button" @click="emit('open-checkout')">{{ lang.$t('cart.checkout') }}</button>
        <button class="history-btn" type="button" @click="emit('open-history')">
          <LineIcon name="history" size="14" color="#0A9A4A" />
          <span>{{ lang.$t('history.btn') }}</span>
        </button>
      </div>
    </template>
  </aside>
</template>
