import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useMenuStore } from './menu';

export const useCartStore = defineStore('cart', () => {
  const items = ref([]);
  const CART_KEY = 'ctfCart';
  const ORDER_KEY = 'ctfOrderCounter';
  const HISTORY_KEY = 'ctfOrders';

  function loadCart() {
    try {
      const raw = localStorage.getItem(CART_KEY);
      items.value = raw ? JSON.parse(raw) : [];
    } catch (e) {
      items.value = [];
    }
  }

  function saveCart() {
    try { localStorage.setItem(CART_KEY, JSON.stringify(items.value)); } catch (e) {}
  }

  const cartQuantity = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0);
  });

  const cartSubtotal = computed(() => {
    const menu = useMenuStore();
    return items.value.reduce((sum, item) => {
      const food = menu.byId(item.foodId);
      return sum + (food ? food.price * item.quantity : 0);
    }, 0);
  });

  function addToCart(id, qty = 1) {
    const existing = items.value.find(i => i.foodId === id);
    if (existing) {
      existing.quantity += qty;
    } else {
      items.value.push({ foodId: id, quantity: qty });
    }
    saveCart();
  }

  function changeQty(id, delta) {
    const line = items.value.find(i => i.foodId === id);
    if (!line) return;
    line.quantity += delta;
    if (line.quantity < 1) line.quantity = 1;
    saveCart();
  }

  function removeItem(id) {
    items.value = items.value.filter(i => i.foodId !== id);
    saveCart();
  }

  function clearCart() {
    items.value = [];
    saveCart();
  }

  function nextOrderNumber() {
    let n = parseInt(localStorage.getItem(ORDER_KEY) || '0', 10);
    if (isNaN(n)) n = 0;
    n++;
    try { localStorage.setItem(ORDER_KEY, String(n)); } catch (e) {}
    return '#CTF-' + String(n).padStart(6, '0');
  }

  function loadHistory() {
    try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') || []; } catch (e) { return []; }
  }

  function saveOrder(order) {
    const h = loadHistory();
    h.unshift(order);
    if (h.length > 20) h.length = 20;
    try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h)); } catch (e) {}
  }

  // Initialize
  loadCart();

  return { items, cartQuantity, cartSubtotal, addToCart, changeQty, removeItem, clearCart, nextOrderNumber, loadHistory, saveOrder };
});
