/*
 * forge-bespoke / map-fallback.js
 *
 * If the Google Maps iframe fails to load within 1.5s, swap to an
 * OpenStreetMap embed. Keeps the contact page useful even on flaky
 * Indian mobile networks where maps.googleapis.com can be blocked.
 *
 * No deps. Vanilla JS. ~1 KB minified.
 */

(function () {
  'use strict';

  var frames = document.querySelectorAll('[data-map-fallback] iframe');
  frames.forEach(function (iframe) {
    var parent = iframe.parentNode;
    var address = parent.parentNode.querySelector('.contact-map__address');
    if (!address) return;

    var loaded = false;
    iframe.addEventListener('load', function () { loaded = true; });

    setTimeout(function () {
      if (loaded) return;

      // Pull address string from sibling
      var addrText = address ? address.textContent.trim() : '';

      // Build OSM embed URL
      var osm = document.createElement('iframe');
      osm.src = 'https://www.openstreetmap.org/export/embed.html?bbox=' +
                encodeURIComponent('77.5,12.9,77.7,13.1') +
                '&layer=mapnik&marker=' +
                encodeURIComponent('12.95,77.6') +
                '&q=' + encodeURIComponent(addrText);
      osm.width = '100%';
      osm.height = '400';
      osm.loading = 'lazy';
      osm.title = 'Map (OpenStreetMap fallback)';
      osm.referrerPolicy = 'no-referrer-when-downgrade';

      iframe.style.display = 'none';
      parent.appendChild(osm);

      // Add a small note
      var note = document.createElement('p');
      note.className = 'contact-map__fallback-note';
      note.textContent = 'Map by OpenStreetMap. (Google Maps blocked this region.)';
      parent.appendChild(note);
    }, 1500);
  });
})();