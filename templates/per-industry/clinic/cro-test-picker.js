/*
 * forge-bespoke / cro-test-picker.js
 *
 * CRO engine: test-picker
 * Used by: clinic, diagnostic-centre, dental, physio, vet
 *
 * Data shape (window.CRO_DATA.tests):
 * [
 *   {
 *     "id": "cbc",
 *     "name": "Complete Blood Count (CBC)",
 *     "category": "routine",
 *     "fasting": "none",
 *     "sample": "Blood",
 *     "report_timing": "Same day, 4-6 hours",
 *     "home_collection": true,
 *     "whatsapp_message": "Hi, I'd like to book the CBC test. Can you confirm availability and price?"
 *   }
 * ]
 *
 * State machine:
 *   IDLE -> FILTER (any) -> PICK (a test) -> CTA-VISIBLE
 *         ^                          |
 *         └──────────────────────────┘ (reset)
 *
 * No deps. Vanilla JS. ~3 KB minified.
 */

(function () {
  'use strict';

  var DATA = window.CRO_DATA || { tests: [] };
  var TESTS = DATA.tests || [];
  var WHATSAPP = document.body.getAttribute('data-whatsapp') || '';
  var PHONE = document.body.getAttribute('data-phone') || '';

  var engine = document.querySelector('[data-engine="test-picker"]');
  if (!engine) return;

  var filters = engine.querySelector('[data-cro-filters]');
  var results = engine.querySelector('[data-cro-results]');
  var detail = engine.querySelector('[data-cro-detail]');
  var cta = engine.querySelector('[data-whatsapp-prefill]');

  var state = {
    filters: { category: '', fasting: '', home: '' },
    picked: null
  };

  function render() {
    var filtered = TESTS.filter(function (t) {
      if (state.filters.category && t.category !== state.filters.category) return false;
      if (state.filters.fasting === 'none' && t.fasting !== 'none') return false;
      if (state.filters.fasting === '8h' && t.fasting !== '8h' && t.fasting !== '12h') return false;
      if (state.filters.fasting === '12h' && t.fasting !== '12h') return false;
      if (state.filters.home === 'true' && !t.home_collection) return false;
      return true;
    });

    if (filtered.length === 0) {
      results.innerHTML = '<p class="cro-engine__empty">No tests match. <button type="button" class="cro-engine__reset" data-reset>Reset filters</button></p>';
      return;
    }

    results.innerHTML = filtered.map(function (t) {
      return [
        '<button type="button" class="cro-engine__card" data-pick="', t.id, '"',
        (state.picked && state.picked.id === t.id) ? ' aria-pressed="true"' : '',
        '>',
        '<span class="cro-engine__card-name">', escapeHtml(t.name), '</span>',
        '<span class="cro-engine__card-meta">',
        (t.fasting === 'none' ? 'No fasting' : t.fasting + ' fasting') + ' · ',
        escapeHtml(t.sample) + ' · ',
        'Report: ' + escapeHtml(t.report_timing),
        '</span>',
        '</button>'
      ].join('');
    }).join('');
  }

  function showDetail(test) {
    detail.hidden = false;
    detail.innerHTML = [
      '<h3 class="cro-engine__detail-heading">', escapeHtml(test.name), '</h3>',
      '<dl class="cro-engine__detail-list">',
        '<dt>Fasting</dt><dd>', test.fasting === 'none' ? 'No fasting required' : escapeHtml(test.fasting) + ' hour fasting', '</dd>',
        '<dt>Sample</dt><dd>', escapeHtml(test.sample), '</dd>',
        '<dt>Report timing</dt><dd>', escapeHtml(test.report_timing), '</dd>',
        '<dt>Home collection</dt><dd>', test.home_collection ? 'Available' : 'Walk-in only', '</dd>',
      '</dl>'
    ].join('');
  }

  function showCta(test) {
    var msg = encodeURIComponent(test.whatsapp_message || ('Hi, I\'d like to book the ' + test.name + ' test. Could you confirm availability and price?'));
    cta.href = 'https://wa.me/' + WHATSAPP + '?text=' + msg;
    cta.hidden = false;

    var emailLink = engine.querySelector('[data-email-prefill]');
    if (emailLink && document.body.getAttribute('data-email')) {
      var subject = encodeURIComponent('Test enquiry: ' + test.name);
      var body = encodeURIComponent('Hi,\n\nI\'d like to book the ' + test.name + ' test.\n\nFasting: ' + test.fasting + '\nSample: ' + test.sample + '\nReport timing: ' + test.report_timing + '\nHome collection: ' + (test.home_collection ? 'Yes please' : 'No, walk-in') + '\n\nCould you confirm availability and price?\n');
      emailLink.href = 'mailto:' + document.body.getAttribute('data-email') + '?subject=' + subject + '&body=' + body;
      emailLink.hidden = false;
    }
  }

  function reset() {
    state.picked = null;
    state.filters = { category: '', fasting: '', home: '' };
    detail.hidden = true;
    detail.innerHTML = '';
    cta.hidden = true;
    if (filters) {
      var selects = filters.querySelectorAll('select');
      selects.forEach(function (s) { s.value = ''; });
    }
    render();
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Event delegation
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
    if (resetBtn) {
      reset();
      return;
    }
    var card = e.target.closest('[data-pick]');
    if (card) {
      var id = card.getAttribute('data-pick');
      state.picked = TESTS.find(function (t) { return t.id === id; }) || null;
      if (state.picked) {
        showDetail(state.picked);
        showCta(state.picked);
      }
    }
  });

  render();
})();