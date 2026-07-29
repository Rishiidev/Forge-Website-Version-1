/*
 * forge-bespoke / cro-mood-picker.js
 *
 * CRO engine: mood-picker
 * Used by: restaurant, café, bakery
 *
 * Data shape (window.CRO_DATA.moods):
 * [
 *   {
 *     "id": "date_night",
 *     "label": "Date night",
 *     "description": "Quiet corner, slow service, candle-friendly.",
 *     "default_table": 2,
 *     "default_time": "dinner",
 *     "recommended_slots": ["Fri 7:30 PM", "Sat 7:30 PM", "Sat 8:00 PM"]
 *   }
 * ]
 *
 * State machine:
 *   IDLE -> PICK (a mood) -> ADJUST (table + time) -> PICK (a slot) -> CTA-VISIBLE
 *
 * No deps. Vanilla JS. ~3 KB minified.
 */

(function () {
  'use strict';

  var DATA = window.CRO_DATA || { moods: [] };
  var MOODS = DATA.moods || [];
  var WHATSAPP = document.body.getAttribute('data-whatsapp') || '';

  var engine = document.querySelector('[data-engine="mood-picker"]');
  if (!engine) return;

  var results = engine.querySelector('[data-cro-results]');
  var detail = engine.querySelector('[data-cro-detail]');
  var cta = engine.querySelector('[data-whatsapp-prefill]');

  var state = { mood: null, table: null, time: null, slot: null };

  function render() {
    if (MOODS.length === 0) {
      results.innerHTML = '<p class="cro-engine__empty">No occasions configured yet.</p>';
      return;
    }
    results.innerHTML = MOODS.map(function (m) {
      return [
        '<button type="button" class="cro-engine__card" data-pick="', m.id, '"',
        (state.mood && state.mood.id === m.id) ? ' aria-pressed="true"' : '',
        '>',
        '<span class="cro-engine__card-name">', escapeHtml(m.label), '</span>',
        '<span class="cro-engine__card-meta">', escapeHtml(m.description || ''), '</span>',
        '</button>'
      ].join('');
    }).join('');
  }

  function showDetail(mood) {
    state.table = mood.default_table;
    state.time = mood.default_time;
    state.slot = null;
    detail.hidden = false;
    detail.innerHTML = [
      '<h3 class="cro-engine__detail-heading">', escapeHtml(mood.label), '</h3>',
      '<form class="cro-engine__detail-form" data-detail-form>',
        '<label><span>Table size</span>',
          '<select name="table">',
            [2, 4, 6, 8].map(function (n) { return '<option value="' + n + '"' + (n === state.table ? ' selected' : '') + '>' + n + ' people</option>'; }).join(''),
          '</select>',
        '</label>',
        '<label><span>Time of day</span>',
          '<select name="time">',
            ['lunch', 'afternoon', 'dinner', 'late'].map(function (t) {
              return '<option value="' + t + '"' + (t === state.time ? ' selected' : '') + '>' + t.charAt(0).toUpperCase() + t.slice(1) + '</option>';
            }).join(''),
          '</select>',
        '</label>',
      '</form>',
      '<div class="cro-engine__slots">',
        '<p class="cro-engine__slots-label">Suggested slots (confirm by WhatsApp):</p>',
        '<ul class="cro-engine__slots-list">',
          (mood.recommended_slots || []).map(function (s) {
            return '<li><button type="button" class="cro-engine__slot" data-slot="' + escapeHtml(s) + '">' + escapeHtml(s) + '</button></li>';
          }).join(''),
        '</ul>',
      '</div>'
    ].join('');
    cta.hidden = true;
  }

  function showCta(mood) {
    var msg = [
      'Hi, I\'d like to book a table.',
      'Occasion: ' + mood.label + '.',
      'Table size: ' + state.table + ' people.',
      'Time: ' + state.time + '.',
      (state.slot ? 'Preferred slot: ' + state.slot + '.' : ''),
      '',
      'Could you confirm availability?'
    ].filter(Boolean).join('\n');
    cta.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(msg);
    cta.hidden = false;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  results.addEventListener('click', function (e) {
    var card = e.target.closest('[data-pick]');
    if (card) {
      var id = card.getAttribute('data-pick');
      state.mood = MOODS.find(function (m) { return m.id === id; }) || null;
      if (state.mood) showDetail(state.mood);
    }
  });

  detail.addEventListener('change', function (e) {
    if (!state.mood) return;
    if (e.target.name === 'table') state.table = parseInt(e.target.value, 10);
    if (e.target.name === 'time') state.time = e.target.value;
    state.slot = null;
    cta.hidden = true;
  });

  detail.addEventListener('click', function (e) {
    var slot = e.target.closest('[data-slot]');
    if (slot && state.mood) {
      state.slot = slot.getAttribute('data-slot');
      showCta(state.mood);
    }
  });

  render();
})();