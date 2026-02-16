/**
 * サービスワーカー：キャッシュ管理とオフライン対応
 */

// キャッシュの名前（バージョン管理を兼ねる）
const CACHE_NAME = "shelter-cache-v1";

// キャッシュに保存するリソースのリスト
const urlsToCache = [
    "/",                // メインページ（ルート）
    "/static/manifest.json",
    "/static/icon-192.png",
    "/static/icon-512.png",
];

/**
 * インストールイベント:
 * サービスワーカーが登録された際に実行され、指定したリソースをキャッシュに保存します。
 */
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log("Opened cache");
            return cache.addAll(urlsToCache);
        })
    );
});

/**
 * フェッチイベント:
 * ネットワークリクエストが発生した際に割り込みます。
 * 1. キャッシュに該当するデータがあればそれを返す（キャッシュ優先）
 * 2. なければ通常通りネットワークから取得する
 */
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            // キャッシュヒット（responseがある場合）はそれを返し、なければfetchを実行
            return response || fetch(event.request);
        })
    );
});