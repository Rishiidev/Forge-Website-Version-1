/*
 * forge-bespoke / cro-quote-builder.js
 *
 * CRO engine: quote-builder
 * Used by: coach, tutor, consultant, B2B service, personal-brand
 *
 * Data shape (window.CRO_DATA.questions):
 * [
 *   { "id": "problem", "prompt": "What's the situation?", "type": "long_string", "required": true },
 *   { "id": "timeline", "prompt": "When do you need this?", "type": "enum", "options": ["This month", "1-3 months", "Just exploring"] },
 *   ...
 * ]
 *
 * State machine:
 *   Q1 -> Q2 -> Q3 -> Q4 -> SCOPE-SUMMARY -> CTA-VISIBLE
 *                                                     |
 *                                  ┌──────────────────┘
 *                                  v
 *                          WhatsApp / Email pre-fill
 *
 * No deps. Vanilla JS. ~3 KB minified.
 */

(function () {
  'use strict';

  var DATA = window.CRO_DATA || { questions: [] };
  var QUESTIONS = DATA.questions || [];
  var WHATSAPP = document.body.getAttribute('data-whatsapp') || '';
  var EMAIL = document.body.getAttribute('data-email') || '';

  var engine = document.querySelector('[data-engine="quote-builder"]');
  if (!engine) return;

  var results = engine.querySelector('[data-cro-results]');
  var detail = engine.querySelector('[data-cro-detail]');
  var ctaWa = engine.querySelector('[data-whatsapp-prefill]');
  var ctaEmail = engine.querySelector('[data-email-prefill]');

  var state = { index: 0, answers: {} };

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderQuestion() {
    var q = QUESTIONS[state.index];
    if (!q) return renderSummary();
    var input = '';
    if (q.type === 'enum') {
      input = '<select name="answer" data-answer required>' +
        '<option value="">Choose one</option>' +
        (q.options || []).map(function (o) { return '<option value="' + escapeHtml(o) + '">' + escapeHtml(o) + '</option>'; }).join('') +
        '</select>';
    } else if (q.type === 'long_string') {
      input = '<textarea name="answer" data-answer rows="4" required placeholder="A few sentences is plenty"></textarea>';
    } else {
      input = '<input type="text" name="answer" data-answer required>';
    }
    results.innerHTML = [
      '<div class="cro-engine__q">',
        '<p class="cro-engine__q-step">Question ', state.index + 1, ' of ', QUESTIONS.length, '</p>',
        '<label class="cro-engine__q-prompt">', escapeHtml(q.prompt), '</label>',
        input,
        '<div class="cro-engine__q-actions">',
          (state.index > 0 ? '<button type="button" data-back>Back</button>' : ''),
          '<button type="button" data-next>Next</button>',
        '</div>',
      '</div>'
    ].join('');
  }

  function renderSummary() {
    var lines = QUESTIONS.map(function (q, i) {
      return state.answers[q.id] ? escapeHtml(q.prompt) + ': ' + escapeHtml(state.answers[q.id]) : null;
    }).filter(Boolean);

    detail.hidden = false;
    detail.innerHTML = [
      '<h3 class="cro-engine__detail-heading">Here is what you sent.</h3>',
      '<dl class="cro-engine__summary">',
        lines.map(function (l, i) {
          var colonAt = l.indexOf(': ');
          return '<dt>' + escapeHtml(l.slice(0, colonAt)) + '</dt><dd>' + escapeHtml(l.slice(colonAt + 2)) + '</dd>';
        }).join(''),
      '</dl>',
      '<p class="cro-engine__summary-note">Edit any answer above and re-submit, or send as-is.</p>'
    ].join('');
  }

  function showCtas() {
    var body = QUESTIONS.map(function (q) {
      return state.answers[q.id] ? q.prompt + '\n' + state.answers[q.id] : null;
    }).filter(Boolean).join('\n\n');

    var waMsg = [
      'Hi, I\'d like to enquire about working together.\n',
      body,
      '\nCould we set up a discovery call?'
    ].join('\n');

    ctaWa.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(waMsg);
    ctaWa.hidden = false;

    if (ctaEmail && EMAIL) {
      ctaEmail.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Discovery call enquiry') + '&body=' + encodeURIComponent(waMsg);
      ctaEmail.hidden = false;
    }
  }

  results.addEventListener('click', function (e) {
    if (e.target.matches('[data-next]')) {
      var input = results.querySelector('[data-answer]');
      var q = QUESTIONS[state.index];
      if (!input || !input.value) {
        input && input.focus();
        return;
      }
      state.answers[q.id] = input.value.trim();
      state.index += 1;
      if (state.index >= QUESTIONS.length) {
        renderSummary();
        showCtas();
      } else {
        renderQuestion();
      }
    }
    if (e.target.matches('[data-back]')) {
      if (state.index > 0) {
        state.index -= 1;
        renderQuestion();
      }
    }
  });

  if (QUESTIONS.length > 0) renderQuestion();
})();