// ClockTower Admin JS
document.addEventListener('DOMContentLoaded', function() {
  // Theme
  var saved = localStorage.getItem('ctfAdminTheme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);

  // Auto-dismiss messages
  document.querySelectorAll('.messages li').forEach(function(el) {
    setTimeout(function() { el.style.opacity = '0'; setTimeout(function() { el.remove(); }, 300); }, 4000);
  });

  // Notification dropdown
  var notifBtn = document.querySelector('.notif-btn');
  var notifDrop = document.querySelector('.notif-dropdown');
  if (notifBtn && notifDrop) {
    notifBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      notifDrop.classList.toggle('show');
    });
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.notif-dropdown') && !e.target.closest('.notif-btn')) {
        notifDrop.classList.remove('show');
      }
    });
  }

  // Sidebar toggle
  var hamburger = document.querySelector('.hamburger');
  var sidebar = document.querySelector('.sidebar');
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', function() { sidebar.classList.toggle('open'); });
  }

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
    var icon = btn.querySelector('i');
    if (inp.type === 'password') { inp.type = 'text'; icon.className = 'fas fa-eye-slash'; }
    else { inp.type = 'password'; icon.className = 'fas fa-eye'; }
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
              var icon = n.type && n.type.indexOf('WHATSAPP') >= 0 ? 'fa-whatsapp' : 'fa-bell';
              return '<div class="notif-item' + (n.read ? '' : ' unread') + '">' +
                '<div class="notif-icon" style="background:' + iconBg + ';color:' + iconColor + ';"><i class="fab ' + icon + '"></i></div>' +
                '<div class="notif-text"><strong>' + n.title + '</strong><span>' + (n.detail || '').replace(/\n/g, '<br>') + '</span></div>' +
                '</div>';
            }).join('');
          }
        }
      })
      .catch(function() {});
  }, 10000);
});
