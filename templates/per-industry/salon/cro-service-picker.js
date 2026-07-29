/*
 * forge-bespoke / cro-service-picker.js
 *
 * CRO engine: service-picker
 * Used by: salon, beauty, spa
 *
 * Data shape (window.CRO_DATA.services):
 * [
 *   {
 *     "id": "haircut_basic",
 *     "name": "Haircut — Basic",
 *     "category": "hair",
 *     "length_minutes": 30,
 *     "stylists": ["any", "senior"]
 *   }
 * ]
 *
 * State machine:
 *   IDLE -> FILTER (any) -> PICK (a service) -> LENGTH + STYLIST + DAY -> CTA-VISIBLE
 *
 * No deps. Vanilla JS. ~3 KB minified.
 */

(function () {
  'use strict';

  var DATA = window.CRO_DATA || { services: [] };
  var SERVICES = DATA.services || [];
  var WHATSAPP = document.body.getAttribute('data-whatsapp') || '';

  var engine = document.querySelector('[data-engine="service-picker"]');
  if (!engine) return;

  var filters = engine.querySelector('[data-cro-filters]');
  var results = engine.querySelector('[data-cro-results]');
  var detail = engine.querySelector('[data-cro-detail]');
  var cta = engine.querySelector('[data-whatsapp-prefill]');

  var state = {
    filters: { category: '', max_length: '' },
    picked: null,
    length: null,
    stylist: 'any',
    day: 'today'
  };

  function render() {
    var max = state.filters.max_length ? parseInt(state.filters.max_length, 10) : Infinity;
    var filtered = SERVICES.filter(function (s) {
      if (state.filters.category && s.category !== state.filters.category) return false;
      if (s.length_minutes > max) return false;
      return true;
    });

    if (filtered.length === 0) {
      results.innerHTML = '<p class="cro-engine__empty">No services match. <button type="button" class="cro-engine__reset" data-reset>Reset filters</button></p>';
      return;
    }

    results.innerHTML = filtered.map(function (s) {
      return [
        '<button type="button" class="cro-engine__card" data-pick="', s.id, '"',
        (state.picked && state.picked.id === s.id) ? ' aria-pressed="true"' : '',
        '>',
        '<span class="cro-engine__card-name">', escapeHtml(s.name), '</span>',
        '<span class="cro-engine__card-meta">',
        s.length_minutes + ' min · ',
        escapeHtml(s.category),
        '</span>',
        '</button>'
      ].join('');
    }).join('');
  }

  function showDetail(svc) {
    state.length = svc.length_minutes;
    detail.hidden = false;
    detail.innerHTML = [
      '<h3 class="cro-engine__detail-heading">', escapeHtml(svc.name), '</h3>',
      '<p class="cro-engine__detail-length">Length: ', svc.length_minutes, ' minutes</p>',
      '<form class="cro-engine__detail-form" data-detail-form>',
        '<label><span>Stylist preference</span>',
          '<select name="stylist">',
            (svc.stylists || ['any']).map(function (x) { return '<option value="' + x + '">' + x + '</option>'; }).join(''),
          '</select>',
        '</label>',
        '<label><span>Day</span>',
          '<select name="day">',
            '<option value="today">Today</option>',
            '<option value="tomorrow">Tomorrow</option>',
            '<option value="weekday">This weekday</option>',
            '<option value="weekend">This weekend</option>',
          '</select>',
        '</label>',
      '</form>'
    ].join('');
  }

  function showCta(svc) {
    var msg = [
      'Hi, I\'d like to book: ' + svc.name + '.',
      'Length: ' + svc.length_minutes + ' minutes.',
      'Stylist preference: ' + state.stylist + '.',
      'Day: ' + state.day + '.',
      '',
      'Could you confirm a slot?'
    ].join('\n');
    cta.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(msg);
    cta.hidden = false;
  }

  function reset() {
    state.picked = null;
    state.filters = { category: '', max_length: '' };
    detail.hidden = true;
    detail.innerHTML = '';
    cta.hidden = true;
    if (filters) {
      filters.querySelectorAll('select').forEach(function (s) { s.value = ''; });
    }
    render();
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  if (filters) {
    filters.addEventListener('change', function (e) {
      var t = e.target;
      if (t && t.dataset && t.dataset.filter) {
        state.filters[t.dataset.filter] = t.value;
        state.picked = null;
        detail.hidden = true;
        cta.hidden = true;
        render();
      }
    });
  }

  results.addEventListener('click', function (e) {
    var resetBtn = e.target.closest('[data-reset]');
    if (resetBtn) { reset(); return; }
    var card = e.target.closest('[data-pick]');
    if (card) {
      var id = card.getAttribute('data-pick');
      state.picked = SERVICES.find(function (s) { return s.id === id; }) || null;
      if (state.picked) showDetail(state.picked);
    }
  });

  detail.addEventListener('change', function (e) {
    if (!state.picked) return;
    if (e.target.name === 'stylist') state.stylist = e.target.value;
    if (e.target.name === 'day') state.day = e.target.value;
    showCta(state.picked);
  });

  render();
})();