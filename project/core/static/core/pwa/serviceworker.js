const CACHE_NAME = "tla-cache-v1";
const URLS_TO_CACHE = [
  "/",
  "/static/css/",
  "/static/js/",
  "/static/images/"
];

// Install SW
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

// Activate SW
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== CACHE_NAME)
          .map(k => caches.delete(k))
        )
    )
  );
});

// Fetch
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(cacheResponse => {
      return (
        cacheResponse ||
        fetch(event.request).catch(() => cacheResponse)
      );
    })
  );
});

self.addEventListener("install", e => {
  console.log("Service Worker instalado");
});

self.addEventListener("fetch", e => {});
