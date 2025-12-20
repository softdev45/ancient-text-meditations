const CACHE_NAME = 'browshare'
const assets2 = ['/',
  '/static/browshare.css',
  '/static/browshare.js',
  '/static/pagetools.js',

];

const assets = ['/', '/static/pagetools.js', '/static/icon50.png', '/static/TinyGesture.js', ['/static/fonts/OHfont.ttf', '/static/fonts/Cardo-Regular.ttf', '/static/fonts/GoudyBookletter1911-Regular.ttf', '/static/fonts/CrimsonPro-VariableFont_wght.ttf', '/static/fonts/Quattrocento-Regular.ttf', '/static/fonts/Average-Regular.ttf', '/static/fonts/Cormorant-VariableFont_wght.ttf', '/static/fonts/OHfont.woff', '/static/fonts/BBHHegarty-Regular.ttf', '/static/fonts/Petrona-Thin.ttf', '/static/fonts/Cormorant-Regular.ttf', '/static/fonts/HedvigLettersSerif-Regular-VariableFont_opsz.ttf', '/static/fonts/OldStandardTT-Regular.ttf', '/static/fonts/Petrona-Regular.ttf', '/static/fonts/Montaga-Regular.ttf', '/static/fonts/LindenHill-Regular.ttf', '/static/fonts/CrimsonText-Regular.ttf', '/static/fonts/LibreBaskerville-VariableFont_wght.ttf', '/static/fonts/Platypi-VariableFont_wght.ttf', '/static/fonts/Lancelot-Regular.ttf'], '/static/TinyGesture.min.js', '/static/browshare.js', '/static/DemoPannable.js', '/static/favicon.ico', '/static/browshare.css', '/static/hammer.min.js', '/static/DemoTransitions.js', '/static/icon100.png', '/static/swipeable.js', '/static/fonts.css']

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(assets)));
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});