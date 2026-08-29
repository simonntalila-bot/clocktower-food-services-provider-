import { defineStore } from 'pinia';
import { ref } from 'vue';
import { FOODS as baseFoods, CATEGORY_META } from '../foods';
import { API_BASE } from '../api.js';

const VISINIA_RE = /visinia/i;

export const useMenuStore = defineStore('menu', () => {
  const foods = ref([...baseFoods]);
  const currentCat = ref('all');
  const searchTerm = ref('');

  function byId(id) {
    return foods.value.find(f => f.id === Number(id));
  }

  function filteredFoods() {
    const q = searchTerm.value.toLowerCase();
    let list = foods.value.filter(f => {
      if (q && !f.name.toLowerCase().includes(q) && !(f.nameSw || '').toLowerCase().includes(q)) return false;
      return true;
    });
    const sp = specialList(currentCat.value, list);
    if (sp) return sp;
    list = list.filter(f => currentCat.value === 'all' || f.category === currentCat.value);
    list.sort((a, b) => (b.img ? 1 : 0) - (a.img ? 1 : 0));
    return list;
  }

  function specialList(cat, source) {
    if (cat === 'visinia') return source.filter(f => f.category === 'visinia' || VISINIA_RE.test(f.name));
    if (cat === 'lunch' || cat === 'dinner') return source.filter(f => f.category === 'lunch' || f.category === 'dinner');
    return null;
  }

  function setFilter(cat) {
    currentCat.value = cat;
  }

  function catCount(cat) {
    const sp = specialList(cat, foods.value);
    if (sp) return sp.length;
    return foods.value.filter(f => f.category === cat).length;
  }

  function catMeta(cat) {
    return CATEGORY_META[cat] || CATEGORY_META.lunch;
  }

  // Load custom foods from localStorage
  try {
    const localFoods = JSON.parse(localStorage.getItem('ctfCustomFoods') || '[]') || [];
    localFoods.forEach(cf => {
      if (!foods.value.find(f => f.id === cf.id)) {
        foods.value.push(cf);
      }
    });
  } catch (e) {}

  // Fetch live menu from the Django backend so admin edits (esp. images)
  // show up on the user site. Falls back to the static food list when the
  // backend isn't reachable (e.g. static GitHub Pages deploy).
  // The cache-busting query + no-store mean the menu is never re-served from
  // a stale browser cache.
  function refresh() {
    const cacheBust = API_BASE + '/api/foods/?t=' + Date.now();
    return fetch(cacheBust, { cache: 'no-store' })
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(data => {
        if (!data || !Array.isArray(data.foods)) return;
        const byId = new Map((data.foods || []).map(f => [Number(f.id), f]));
        foods.value = foods.value.map(f => {
          const live = byId.get(Number(f.id));
          if (!live) return f;
          return {
            ...f,
            name: live.name || f.name,
            nameSw: live.nameSw || f.nameSw,
            category: live.category || f.category,
            price: live.price || f.price,
            icon: live.icon || f.icon,
            img: live.img || f.img,
            rating: live.rating || f.rating,
            popular: live.popular,
            desc: live.desc || f.desc,
            descSw: live.descSw || f.descSw,
          };
        });
        for (const live of data.foods || []) {
          if (!foods.value.find(f => f.id === Number(live.id))) {
            foods.value.push({ ...live, nameSw: live.nameSw || '', desc: live.desc || '', descSw: live.descSw || '' });
          }
        }
      })
      .catch(() => {});
  }

  refresh();

  return { foods, currentCat, searchTerm, byId, specialList, filteredFoods, setFilter, catCount, catMeta, CATEGORY_META, refresh };
});
