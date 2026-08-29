// ClockTower Admin JS
var LINE_ICONS={
  grid:['M3 3h7v7H3z','M14 3h7v7h-7z','M3 14h7v7H3z','M14 14h7v7h-7z'],
  receipt:['M5 2h14v20l-2.5-1.6L14 22l-2.5-1.6L9 22l-2.5-1.6L4 22V2z','M9 7h6','M9 11h6','M9 15h4'],
  users:['M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2','circle:10,7,4','M23 21v-2a4 4 0 0 0-3-3.87','M16 3.13a4 4 0 0 1 0 7.75'],
  comments:['M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z','M8 9h8','M8 12.5h5'],
  comment:['M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'],
  utensils:['M3 2v7a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2V2','M6 2v20','M21 15V2a5 5 0 0 0-5 5v6a2 2 0 0 0 2 2h3zm0 0v7'],
  pluscircle:['M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18z','M12 8v8','M8 12h8'],
  shielduser:['M12 22s8-3.6 8-10V5l-8-3-8 3v7c0 6.4 8 10 8 10z','circle:12,8.5,3'],
  history:['M3.5 12a8.5 8.5 0 1 0 2.6-6.1L3.5 8.2','M3.5 3.5v4.7h4.7','M12 7.5V12l3 3'],
  user:['M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2','circle:12,7,4'],
  gear:['M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z','M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09a1.7 1.7 0 0 0-1-1.55 1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.7 1.7 0 0 0 .34-1.88 1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09a1.7 1.7 0 0 0 1.55-1 1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.7 1.7 0 0 0 1.88.34h.01a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 1.55h.01a1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.7 1.7 0 0 0-.34 1.88v.01a1.7 1.7 0 0 0 1.55 1H21a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-1.55 1z'],
  arrowleft:['M19 12H5','m12 19-7-7 7-7'],
  menu:['M4 6h16','M4 12h16','M4 18h16'],
  bell:['M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9','M13.7 21a2 2 0 0 1-3.4 0'],
  moon:['M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z'],
  sun:['M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z','M12 1v2','M12 21v2','M4.2 4.2l1.4 1.4','M18.4 18.4l1.4 1.4','M1 12h2','M21 12h2','M4.2 19.8l1.4-1.4','M18.4 5.6l1.4-1.4'],
  logout:['M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4','m16 17 5-5-5-5','M21 12H9'],
  whatsapp:['M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5z','M8.5 9.5c.5 2.5 3 4.5 5.5 5l1.5-1.5-2-1-1 1c-1-.5-1.8-1.3-2.3-2.3l1-1-1-2z'],
  check:['M20 6 9 17l-5-5'],
  checkcircle:['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z','m8.5 12 2.5 2.5 5-5'],
  edit:['M12 20h9','M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z'],
  userplus:['M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2','circle:9,7,4','M19 8v6','M16 11h6'],
  useredit:['M2 21a8 8 0 0 1 14-6.3','M16 3.13a4 4 0 0 1 0 7.75','M21 16a1.5 1.5 0 0 1 1 1.4V21h-3.4a1.5 1.5 0 0 1-1-2.6l.2-.2 3.2-2.2z'],
  trash:['M3 6h18','M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2','M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6','M10 11v6','M14 11v6'],
  eye:['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z','circle:12,12,3'],
  eyeslash:['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z','circle:12,12,3','M4 4l16 16'],
  download:['M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4','m7 10 5 5 5-5','M12 15V3'],
  money:['M2 6h20v12H2z','M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0z'],
  clipboard:['M9 2h6a1 1 0 0 1 1 1v1h2a2 2 0 0 1 2 2v15a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2V3a1 1 0 0 1 1-1z','M9 12h6','M9 16h4'],
  envelope:['M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z','m3 7.5 9 6 9-6'],
  alertcircle:['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z','M12 8v5','M12 16.5v.01'],
  alerttriangle:['M12 3 2 21h20L12 3z','M12 10v5','M12 17.5v.01'],
  fileexport:['M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z','M14 2v6h6','M12 12v6','m9 16 3-3 3 3'],
  fileinvoice:['M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z','M14 2v6h6','M8 13h8','M8 17h8','M12 9v0'],
  fire:['M12 22c-3.9 0-7-3-7-6.9 0-2.4 1.2-4 2.6-5.4.7-.7 1.3-1.3 1.8-2.4.5 1 1.1 1.6 1.8 2.3.8.8 1.5 1.7 1.8 3 .6-1.4.9-2.8.9-4.6C14.5 3.6 18 2 20 4.5 21.3 6.6 21 11 19.5 13c-1.4 1.9-3 3.9-5.2 5.6','M12 22c0-2 0-3-1.5-4.5'],
  key:['M21 2l-2 2m-7.6 7.6A5.5 5.5 0 1 1 6 12a5.5 5.5 0 0 1 5.4 0z','M15 7l2 2m2 2 2 2'],
  lock:['M5 11h14a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-8a1 1 0 0 1 1-1z','M8 11V7a4 4 0 0 1 8 0v4'],
  motorcycle:['M5 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z','M19 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z','M3 13h2l5-5h4l3 5h2','M8 13h13'],
  paperplane:['M22 2 11 13','M22 2l-7 20-4-9-9-4 20-7z'],
  plus:['M12 5v14','M5 12h14'],
  cart:['M3 3h2l2.4 12.2A2 2 0 0 0 9.4 17h8.9a2 2 0 0 0 2-1.6L22 7H6','M11 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2z','M18 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2z'],
  stickynote:['M15 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8z','M15 3v5h5','M9 13h6','M9 17h6']
};
function lineIcon(name,size,color){
  var paths=LINE_ICONS[name]||[];
  var s=size||16;
  var c=color||'currentColor';
  var parts=paths.map(function(d){
    if(d.indexOf('circle:')===0){var p=d.split(':')[1].split(',');return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="'+p[2]+'"/>';}
    if(d.indexOf('rect:')===0){var q=d.split(':')[1].split(',');return '<rect x="'+q[0]+'" y="'+q[1]+'" width="'+q[2]+'" height="'+q[3]+'" rx="'+(q[4]||2)+'"/>';}
    return '<path d="'+d+'"/>';
  }).join('');
  return '<svg width="'+s+'" height="'+s+'" viewBox="0 0 24 24" fill="none" stroke="'+c+'" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;display:inline-block" aria-hidden="true">'+parts+'</svg>';
}
function initLineIcons(root){
  var scope=(root&&root.querySelectorAll)?root:document;
  var all=scope.querySelectorAll('[class*="li-n-"]');
  for(var i=0;i<all.length;i++){
    var el=all[i];
    if(!el.getAttribute('data-li-done')){
      var cls=(el.className&&el.className.split)?el.className.split(/\s+/):[];
      for(var j=0;j<cls.length;j++){
        if(cls[j].indexOf('li-n-')===0){
          var name=cls[j].slice(5);
          var size=parseInt(el.getAttribute('data-li-size')||16,10);
          var color=el.getAttribute('data-li-color')||'currentColor';
          el.setAttribute('data-li-done','1');
          var r = lineIcon(name, size, color);
          if (el.id) { r = r.replace('<svg ', '<svg id="' + el.id + '" '); }
          el.outerHTML = r;
          break;
        }
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  initLineIcons();
  // White-only theme (dark mode removed)
  document.documentElement.setAttribute('data-theme', 'light');

  // Auto-dismiss messages
  document.querySelectorAll('.messages li').forEach(function(el) {
    setTimeout(function() { el.style.opacity = '0'; setTimeout(function() { el.remove(); }, 300); }, 4000);
  });

  // Confirm dialogs
  window.showConfirm = function(title, msg, callback) {
    var overlay = document.getElementById('confirmOverlay');
    if (!overlay) return;
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMsg').textContent = msg;
    overlay.classList.add('show');
    document.getElementById('confirmBtn').onclick = function() {
      overlay.classList.remove('show');
      if (callback) callback();
    };
  };

  window.closeConfirm = function() {
    var overlay = document.getElementById('confirmOverlay');
    if (overlay) overlay.classList.remove('show');
  };

  // Toggle password visibility
  window.togglePw = function(id, btn) {
    var inp = document.getElementById(id);
    var show = inp.type === 'password';
    inp.type = show ? 'text' : 'password';
    if (btn) btn.innerHTML = lineIcon(show ? 'eyeslash' : 'eye', 16, 'currentColor');
  };

  // Auto-poll notifications
  var unreadEl = document.getElementById('notifCount');
  var badgeEl = document.getElementById('orderBadge');
  var notifList = document.querySelector('.notif-dropdown');
  setInterval(function() {
    fetch('/api/notifications/')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (unreadEl) {
          if (data.unread > 0) { unreadEl.textContent = data.unread; unreadEl.classList.add('show'); }
          else { unreadEl.classList.remove('show'); }
        }
        if (badgeEl) badgeEl.classList.toggle('show', data.unread > 0);
        if (notifList && data.notifications) {
          var list = notifList.querySelector('.notif-list');
          if (list && data.notifications.length > 0) {
            list.innerHTML = data.notifications.map(function(n) {
              var iconBg = n.type && n.type.indexOf('WHATSAPP') >= 0 ? 'rgba(37,211,102,0.12)' : 'rgba(255,184,77,0.12)';
              var iconColor = n.type && n.type.indexOf('WHATSAPP') >= 0 ? '#25d366' : 'var(--accent)';
              var icon = n.type && n.type.indexOf('WHATSAPP') >= 0 ? 'whatsapp' : 'bell';
              return '<div class="notif-item' + (n.read ? '' : ' unread') + '">' +
                '<div class="notif-icon" style="background:' + iconBg + ';color:' + iconColor + ';">' + lineIcon(icon, 14, 'currentColor') + '</div>' +
                '<div class="notif-text"><strong>' + n.title + '</strong><span>' + (n.detail || '').replace(/\n/g, '<br>') + '</span></div>' +
                '</div>';
            }).join('');
          }
        }
      })
      .catch(function() {});
  }, 10000);
});
