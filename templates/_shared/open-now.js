/*
 * forge-bespoke / open-now.js
 *
 * Open / Closed indicator driven by data-hours attribute on <body>.
 * Hours shape (JSON):
 * {
 *   "mon": [{"open": "09:00", "close": "19:00"}],
 *   "tue": [{"open": "09:00", "close": "19:00"}],
 *   ...
 *   "sun": []
 * }
 *
 * Updates every 60 seconds.
 * No deps. Vanilla JS. ~1 KB minified.
 */

(function () {
  'use strict';

  var els = document.querySelectorAll('[data-open-now]');
  if (els.length === 0) return;

  var raw = document.body.getAttribute('data-hours');
  if (!raw) return;

  var hours;
  try { hours = JSON.parse(raw); } catch (e) { return; }

  var days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];

  function toMinutes(hhmm) {
    var parts = hhmm.split(':');
    return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
  }

  function isOpen(now, dayKey) {
    var slots = hours[dayKey] || [];
    var m = now.getHours() * 60 + now.getMinutes();
    for (var i = 0; i < slots.length; i++) {
      var open = toMinutes(slots[i].open);
      var close = toMinutes(slots[i].close);
      if (m >= open && m < close) return true;
    }
    return false;
  }

  function update() {
    var now = new Date();
    var dayKey = days[now.getDay()];
    var open = isOpen(now, dayKey);
    var text = open ? 'Open now' : 'Closed now';
    els.forEach(function (el) {
      el.textContent = text;
      el.setAttribute('data-state', open ? 'open' : 'closed');
    });
  }

  update();
  setInterval(update, 60000);
})();