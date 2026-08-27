import { defineStore } from 'pinia';
import { ref } from 'vue';
import { FOODS as baseFoods, CATEGORY_META } from '../foods';

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

  return { foods, currentCat, searchTerm, byId, specialList, filteredFoods, setFilter, catCount, catMeta, CATEGORY_META };
});
