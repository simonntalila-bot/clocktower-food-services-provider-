# MAELEKEZO KWA OPENCODE — Mfumo wa Akiba (Offline Backup Order System)

## LENGO
Ongeza mfumo mdogo, unaojitegemea (standalone), unaowezesha mteja kuvinjari menu,
kuona bei, na ku-order HATA BILA INTANETI — bila kugusa au kubadilisha mfumo mkuu
uliopo sasa.

---

## HATUA YA 1 — Weka faili mahali sahihi
Chukua folder `backup-order/` (kutoka `clock_tower_backup_order.zip`) na uiweke
kama route/directory TOFAUTI kabisa na mfumo mkuu, mfano:

```
/backup-order/          ← weka hapa (au /offline-order/, chagua jina lolote fupi)
    index.html
    photos/
        chips-yai-kisasa.jpg
        pizza-medium-combo.jpg
        ... (picha nyingine)
```

**MUHIMU:** Usiguse, usibadilishe, wala usiondoe faili zozote za mfumo mkuu
(routes, components, database, config). Hii ni addition tu — folder mpya
inayosimama peke yake.

---

## HATUA YA 2 — Fanya iwe accessible
Hakikisha mtu akiandika URL kama:
```
https://tovutiyenu.com/backup-order/
```
au
```
https://tovutiyenu.com/backup-order/index.html
```
inafungua ukurasa huo moja kwa moja (static file serving tu — HAIHITAJI
database connection, HAIHITAJI backend endpoint mpya, HAIHITAJI build step).

Kama app inatumia framework (Next.js, Django, Laravel, n.k.), weka folder
hii kwenye eneo la "public/static assets" la framework hiyo ili isipite kwenye
routing logic ya app kuu — mfano:
- Next.js → `public/backup-order/`
- Django → `static/backup-order/` au `staticfiles/`
- Laravel → `public/backup-order/`

---

## HATUA YA 3 — Weka namba ya WhatsApp
Fungua `index.html`, tafuta mstari huu (karibu mwanzo wa `<script>`):
```js
const RECEPTION_WHATSAPP_NUMBER = "255700000000"; // TODO: badilisha na namba halisi
```
Badilisha na namba HALISI ya WhatsApp ya Reception/Admin (bila alama ya `+`,
mfano: `255712345678`). Hii ndiyo namba itakayopokea order zote.

---

## JINSI MFUMO HUU UNAVYOFANYA KAZI (elewa kabla ya kuupeleka live)

1. **Menu na bei zote zipo ndani ya faili lenyewe** (embedded JSON kwenye
   `index.html`) — si kwenye database wala API. Ndiyo maana inafanya kazi
   bila intaneti: browser haihitaji kuomba data kutoka server yoyote.

2. Mteja anafungua ukurasa (mara moja tu anahitaji intaneti/au faili
   likishafunguliwa kwenye kifaa chake linabaki), anavinjari kategoria,
   anatafuta chakula, anaongeza kwenye Cart — YOTE haya ni JavaScript
   inayoendesha ndani ya browser ya mteja (localStorage), HAKUNA server
   inayohusika hapa.

3. Akimaliza kuchagua, anajaza **jina, namba ya simu, mahali** (meza/take away),
   kisha anabonyeza **"Tuma Order kwa WhatsApp"**.

4. **HAPA NDIPO PEKEE intaneti inahitajika** — button hii inafungua link ya
   `wa.me/<namba>?text=<order kamili>` ambayo inampeleka moja kwa moja
   WhatsApp na ujumbe tayari umeandikwa (majina ya vyakula, idadi, bei, jumla).
   Reception/Admin wanapokea ujumbe huo WhatsApp na wanaendelea kushughulikia
   order kama kawaida.

5. Hakuna order inayohifadhiwa kwenye database ya mfumo mkuu — hii ni
   "backup channel" tu ya kuhakikisha order inafika hata kama mfumo mkuu
   (app kuu, database, au tovuti) iko down.

---

## KAZI ZA OPENCODE (checklist)
- [ ] Weka `backup-order/` folder mahali pa static assets, bila kubadilisha
      mfumo mkuu
- [ ] Badilisha `RECEPTION_WHATSAPP_NUMBER` na namba halisi
- [ ] Thibitisha URL inafunguka na inaonyesha menu (jaribu offline pia —
      zima WiFi/data, funga na fungua tena ukurasa, hakikisha menu bado
      inaonekana)
- [ ] Jaribu ku-add item kwenye cart, kisha bonyeza "Tuma Order kwa
      WhatsApp" — hakikisha WhatsApp inafunguka na ujumbe uko sahihi
- [ ] Weka link/kitufe kidogo mahali fulani kwenye mfumo mkuu (mfano
      "Order Offline" kwenye menu ya app) kinachoelekeza kwenye
      `/backup-order/` — hii si lazima lakini inasaidia mteja aipate rahisi
- [ ] Nionyeshe screenshot au link ya kujaribu (live) baada ya kukamilisha

---

## MAMBO YA KUEPUKA
- Usibadilishe muundo wa folder za mfumo mkuu
- Usiongeze dependency mpya (npm packages, libraries) — faili hili
  halihitaji chochote zaidi ya browser ya kawaida
- Usibadilishe jinsi cart/menu data ilivyopangwa ndani ya `index.html`
  bila kuniuliza kwanza, kwa sababu bei/majina yamethibitishwa tayari
  kutoka kwenye menu posters halisi
