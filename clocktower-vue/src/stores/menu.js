import { defineStore } from 'pinia';
import { ref } from 'vue';
import { FOODS as baseFoods, CATEGORY_META } from '../foods';

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
      if (currentCat.value !== 'all' && f.category !== currentCat.value) return false;
      if (q && !f.name.toLowerCase().includes(q) && !(f.nameSw || '').toLowerCase().includes(q)) return false;
      return true;
    });
    list.sort((a, b) => (b.img ? 1 : 0) - (a.img ? 1 : 0));
    return list;
  }

  function setFilter(cat) {
    currentCat.value = cat;
  }

  function catCount(cat) {
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

  return { foods, currentCat, searchTerm, byId, filteredFoods, setFilter, catCount, catMeta, CATEGORY_META };
});
