<script setup>
import { ref, computed, watch } from 'vue';
import { useLangStore } from '../stores/lang';
import { useCartStore } from '../stores/cart';
import { useMenuStore } from '../stores/menu';

const props = defineProps({ show: Boolean });
const emit = defineEmits(['close', 'order-placed']);
const lang = useLangStore();
const cart = useCartStore();
const menu = useMenuStore();

const name = ref('');
const phone = ref('');
const payment = ref('M-Pesa');
const paymentPhone = ref('');
const table = ref('');
const notes = ref('');
const comments = ref('');
const shareBill = ref(false);
const sharePayment = ref('');
const sharePhone = ref('');
const nameError = ref(false);
const phoneError = ref(false);

const mobilePayMethods = ['M-Pesa', 'Tigo Pesa', 'Airtel Money', 'Halopesa'];
const showPayPhone = computed(() => mobilePayMethods.includes(payment.value));

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
  const payPhone = paymentPhone.value.trim();
  if (payPhone) lines.push('Payment Phone: ' + payPhone);
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
  lines.push('TOTAL: ' + fmt(cart.cartSubtotal.value));
  lines.push('Items: ' + cart.cartQuantity.value);
  return lines.join('\n');
}

function sendOrderToProviders(msg) {
  const providers = ['255629290952', '255759597199'];
  providers.forEach(num => {
    window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(msg), '_blank');
  });
}

function resetForm() {
  name.value = '';
  phone.value = '';
  payment.value = 'M-Pesa';
  paymentPhone.value = '';
  table.value = '';
  notes.value = '';
  comments.value = '';
  shareBill.value = false;
  sharePayment.value = '';
  sharePhone.value = '';
  nameError.value = false;
  phoneError.value = false;
}

function handleSubmit() {
  nameError.value = name.value.trim().length < 2;
  phoneError.value = !/^[0-9+\s()-]{7,}$/.test(phone.value.trim());
  if (nameError.value || phoneError.value) return;

  const orderNum = cart.nextOrderNumber();
  const total = cart.cartSubtotal.value;

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

  emit('order-placed', { orderNum, total, customerName: name.value.trim() });
  cart.clearCart();
  resetForm();
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
      <button class="modal-close" type="button" aria-label="Close" @click="handleClose">&times;</button>
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
            <b>{{ fmt(cart.cartSubtotal.value) }}</b>
          </div>
          <div class="co-meta">{{ cart.cartQuantity.value }} {{ lang.$t('co.metaItems') }}{{ cart.cartQuantity.value === 1 ? '' : 's' }} &bull; {{ cart.items.length }} {{ lang.$t('co.metaFoods') }}{{ cart.items.length === 1 ? '' : 's' }}</div>
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
            <div class="payment-phone-field" :class="{ active: showPayPhone }">
              <label v-html="lang.$t('co.lbl.payphone')"></label>
              <input type="tel" v-model="paymentPhone" :placeholder="lang.$t('co.ph.payphone')">
            </div>
            <div class="field" :class="{ invalid: phoneError }">
              <label v-html="lang.$t('co.lbl.phone')"></label>
              <input type="tel" v-model="phone" :placeholder="lang.$t('co.ph.phone')">
              <div class="err" v-html="lang.$t('co.err.phone')"></div>
            </div>
            <div class="field">
              <label v-html="lang.$t('co.lbl.table')"></label>
              <input type="text" v-model="table" :placeholder="lang.$t('co.ph.table')">
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
              <h4><i class="fas fa-users"></i> <span v-html="lang.$t('co.share.title')"></span></h4>
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
            <button class="place-btn" type="submit" v-html="lang.$t('co.submit')"></button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
