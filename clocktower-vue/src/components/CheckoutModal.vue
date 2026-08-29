<script setup>
import { ref } from 'vue';
import { useLangStore } from '../stores/lang';
import { useCartStore } from '../stores/cart';
import { useMenuStore } from '../stores/menu';
import LineIcon from './LineIcon.vue';
import { API_BASE } from '../api.js';

const props = defineProps({ show: Boolean });
const emit = defineEmits(['close', 'order-placed']);
const lang = useLangStore();
const cart = useCartStore();
const menu = useMenuStore();

const name = ref('');
const phone = ref('');
const payment = ref('M-Pesa');

const table = ref('');
const notes = ref('');
const comments = ref('');
const shareBill = ref(false);
const sharePayment = ref('');
const sharePhone = ref('');
const nameError = ref(false);
const phoneError = ref(false);
const tableError = ref(false);
const processing = ref(false);
const done = ref(false);


function fmt(n) { return 'TSh ' + n.toLocaleString('en'); }

function normalizePhone(p) {
  p = (p || '').replace(/[^\d+]/g, '');
  if (p.charAt(0) === '+') p = p.slice(1);
  else if (p.charAt(0) === '0') p = '255' + p.slice(1);
  return p;
}

function buildOrderMessage(orderNum) {
  const lines = [];
  lines.push('\uD83C\uDF7D\uFE0F NEW ORDER \u2014 CLOCKTOWER FOOD SERVICE PROVIDER');
  lines.push('Order Number: ' + orderNum);
  lines.push('');
  lines.push('CUSTOMER');
  lines.push('Name: ' + (name.value.trim() || '-'));
  lines.push('Phone: ' + (phone.value.trim() || '-'));
  lines.push('Table / Location: ' + (table.value.trim() || '-'));
  lines.push('Payment: ' + payment.value);
  if (shareBill.value) {
    const sp = sharePayment.value;
    const spp = sharePhone.value.trim();
    if (sp || spp) {
      lines.push('--- SHARE BILL ---');
      if (sp) lines.push('Share Payment Method: ' + sp);
      if (spp) lines.push('Share Payment Phone: ' + spp);
    }
  }
  lines.push('Notes: ' + (notes.value.trim() || '-'));
  lines.push('Comments: ' + (comments.value.trim() || '-'));
  lines.push('');
  lines.push('Naomba order hii ipelekewe mteja hivi sasa. Asante!');
  lines.push('');
  lines.push('ORDER ITEMS');
  cart.items.forEach(i => {
    const f = menu.byId(i.foodId);
    if (f) lines.push('- ' + lang.$foodName(f) + ' x' + i.quantity + ': ' + fmt(f.price * i.quantity));
  });
  lines.push('');
  lines.push('TOTAL: ' + fmt(cart.cartSubtotal));
  lines.push('Items: ' + cart.cartQuantity);
  return lines.join('\n');
}

const ORDER_EMAIL = 'clocktowercafetz2020@gmail.com';
const ORDER_WHATSAPP_ADMIN = '255677220022';
const ORDER_WHATSAPP_RECEPTION = '255677220022';

function sendOrderToProviders(msg) {
  const providers = [ORDER_WHATSAPP_ADMIN, ORDER_WHATSAPP_RECEPTION];
  providers.forEach((num, i) => {
    setTimeout(() => {
      window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(msg), '_blank');
    }, i * 400);
  });
  const subject = encodeURIComponent('NEW ORDER — ClockTower Food Service Provider');
  window.open('mailto:' + ORDER_EMAIL + '?subject=' + subject + '&body=' + encodeURIComponent(msg), '_blank');
}

function postOrderToBackend(orderNum) {
  const payload = {
    name: name.value.trim(),
    phone: normalizePhone(phone.value.trim()),
    payment: (payment.value || 'M-Pesa').toLowerCase().replace(/[^a-z]/g, '') || 'mpesa',
    paid: false,
    table: table.value.trim(),
    notes: notes.value.trim(),
    comments: comments.value.trim(),
    share_bill: shareBill.value,
    share_payment: sharePayment.value.trim(),
    share_phone: sharePhone.value.trim(),
    items: cart.items
      .filter(i => menu.byId(i.foodId))
      .map(i => ({ v_id: i.foodId, quantity: i.quantity }))
  };
  fetch(API_BASE + '/api/order/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).catch(() => {});
}

function resetForm() {
  name.value = '';
  phone.value = '';
  payment.value = 'M-Pesa';
  table.value = '';
  notes.value = '';
  comments.value = '';
  shareBill.value = false;
  sharePayment.value = '';
  sharePhone.value = '';
  nameError.value = false;
  phoneError.value = false;
  tableError.value = false;
}

function handleSubmit() {
  nameError.value = name.value.trim().length < 2;
  tableError.value = !table.value.trim();
  phoneError.value = false;
  if (nameError.value || tableError.value) return;

  processing.value = true;

  setTimeout(() => {
    const orderNum = cart.nextOrderNumber();
    const total = cart.cartSubtotal;

    cart.saveOrder({
      num: orderNum,
      date: new Date().toISOString(),
      total: total,
      name: name.value.trim(),
      items: cart.items.map(i => {
        const f = menu.byId(i.foodId);
        return f ? lang.$foodName(f) + ' x' + i.quantity : '';
      })
    });

    const msg = buildOrderMessage(orderNum);
    sendOrderToProviders(msg);
    postOrderToBackend(orderNum);

    emit('order-placed', { orderNum, total, customerName: name.value.trim() });
    cart.clearCart();
    menu.refresh();
    processing.value = false;
    done.value = true;

    setTimeout(() => {
      done.value = false;
      resetForm();
    }, 4000);
  }, 5000);
}

function handleClose() {
  emit('close');
}

function handleOverlayClick(e) {
  if (e.target === e.currentTarget) handleClose();
}
</script>

<template>
  <div class="modal" :class="{ show }" @click="handleOverlayClick">
    <div class="modal-card" style="max-width:720px;">
      <button class="modal-close" type="button" aria-label="Close" @click="handleClose" v-show="!processing && !done">&times;</button>

      <div v-if="processing" class="pay-processing">
        <div class="pay-spinner"></div>
        <p>Inatafakari malipo yako...</p>
        <span>Processing payment</span>
      </div>

      <div v-else-if="done" class="pay-done">
        <div class="pay-done-circle">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
            <path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>Malipo yamekamilika!</h3>
        <p>Payment successful. Your order has been sent to Clocktower Food Service Provider.</p>
      </div>

      <template v-else>
      <div style="padding:24px 26px 0;text-align:center;">
        <h3 style="margin:0;font-family:'Space Grotesk',sans-serif;font-size:22px;" v-html="lang.$t('co.title')"></h3>
        <p style="color:var(--muted);font-size:13.5px;margin:6px 0 0;" v-html="lang.$t('co.sub')"></p>
      </div>
      <div class="checkout-grid">
        <div class="co-summary">
          <h4 v-html="lang.$t('co.summary')"></h4>
          <ul class="co-list">
            <li v-for="item in cart.items" :key="item.foodId">
              <span class="cl-name">
                <b>{{ lang.$foodName(menu.byId(item.foodId)) }}</b>
                <span class="cl-q">x{{ item.quantity }}</span>
                <span style="display:block;font-size:12px;color:var(--muted);">{{ fmt(menu.byId(item.foodId).price) }} {{ lang.$t('cart.each') }}</span>
              </span>
              <span class="cl-price">{{ fmt(menu.byId(item.foodId).price * item.quantity) }}</span>
            </li>
          </ul>
          <div class="co-total">
            <span v-html="lang.$t('co.total')"></span>
            <b>{{ fmt(cart.cartSubtotal) }}</b>
          </div>
          <div class="co-meta">{{ cart.cartQuantity }} {{ lang.$t('co.metaItems') }}{{ cart.cartQuantity === 1 ? '' : 's' }} &bull; {{ cart.items.length }} {{ lang.$t('co.metaFoods') }}{{ cart.items.length === 1 ? '' : 's' }}</div>
        </div>
        <div class="co-form">
          <h4 v-html="lang.$t('co.cust')"></h4>
          <form novalidate @submit.prevent="handleSubmit">
            <div class="field" :class="{ invalid: nameError }">
              <label v-html="lang.$t('co.lbl.name')"></label>
              <input type="text" v-model="name" :placeholder="lang.$t('co.ph.name')">
              <div class="err" v-html="lang.$t('co.err.name')"></div>
            </div>
            <div class="field">
              <label v-html="lang.$t('co.lbl.payment')"></label>
              <select v-model="payment">
                <option value="M-Pesa" v-html="lang.$t('co.pay.mpesa')"></option>
                <option value="Tigo Pesa" v-html="lang.$t('co.pay.tigo')"></option>
                <option value="Airtel Money" v-html="lang.$t('co.pay.airtel')"></option>
                <option value="Halopesa" v-html="lang.$t('co.pay.halo')"></option>
                <option value="Bank Transfer" v-html="lang.$t('co.pay.bank')"></option>
                <option value="Cash" v-html="lang.$t('co.pay.cash')"></option>
                <option value="Other" v-html="lang.$t('co.pay.other')"></option>
              </select>
            </div>
            <div class="field">
              <label v-html="lang.$t('co.lbl.phone')"></label>
              <input type="tel" v-model="phone" :placeholder="lang.$t('co.ph.phone')">
            </div>
            <div class="field" :class="{ invalid: tableError }">
              <label v-html="lang.$t('co.lbl.table')"></label>
              <input type="text" v-model="table" :placeholder="lang.$t('co.ph.table')">
              <div class="err" v-html="lang.$t('co.err.table')"></div>
            </div>

            <label class="share-toggle">
              <input type="checkbox" v-model="shareBill">
              <span class="toggle-track"></span>
              <span>
                <span class="toggle-label" v-html="lang.$t('co.share.label')"></span>
                <span class="toggle-desc" v-html="lang.$t('co.share.desc')"></span>
              </span>
            </label>
            <div class="share-bill-section" :class="{ active: shareBill }">
              <h4><LineIcon name="users" size="16" color="#0A9A4A" style="vertical-align:-2px" /> <span v-html="lang.$t('co.share.title')"></span></h4>
              <div class="field">
                <label v-html="lang.$t('co.lbl.sharepay')"></label>
                <select v-model="sharePayment">
                  <option value="">-- Chagua --</option>
                  <option value="M-Pesa">M-Pesa</option>
                  <option value="Tigo Pesa">Tigo Pesa</option>
                  <option value="Airtel Money">Airtel Money</option>
                  <option value="Halopesa">Halopesa</option>
                  <option value="Bank Transfer">Bank Transfer</option>
                  <option value="Cash">Cash</option>
                  <option value="Other">Nyingine</option>
                </select>
              </div>
              <div class="field">
                <label v-html="lang.$t('co.lbl.sharephone')"></label>
                <input type="tel" v-model="sharePhone" :placeholder="lang.$t('co.ph.sharephone')">
              </div>
            </div>
            <div class="field">
              <label v-html="lang.$t('co.lbl.notes')"></label>
              <textarea v-model="notes" :placeholder="lang.$t('co.ph.notes')"></textarea>
            </div>
            <div class="field">
              <label v-html="lang.$t('co.lbl.comments')"></label>
              <textarea v-model="comments" :placeholder="lang.$t('co.ph.comments')"></textarea>
            </div>
            <button class="place-btn" type="submit" v-html="(payment === 'Cash' || payment === 'Other') ? lang.$t('co.submitCash') : lang.$t('co.submit')"></button>
          </form>
        </div>
      </div>
      </template>
    </div>
  </div>
</template>
