# product-support

Support site for apps by nightwolf-chen. Each app lives in its own subdir;
the root `index.html` is the hub.

- `wallpapers/` — Wallpapers (壁纸美图, iOS)
  - Support landing: `index.html`
  - Support article (English): `support.html` / （中文）: `support-zh.html`
  - Privacy Policy (English): `privacy.html` / （中文）: `privacy-zh.html`
- `gifking/` — Emoji King GIF (表情帝GIF, iOS)
  - Support landing: `index.html`
  - Support article (English): `support.html` / （中文）: `support-zh.html`
  - Privacy Policy (English): `privacy.html` / （中文）: `privacy-zh.html`

## Public URLs (after enabling GitHub Pages)

Hub: https://nightwolf-chen.github.io/product-support/

Wallpapers:
- https://nightwolf-chen.github.io/product-support/wallpapers/ ← landing
- https://nightwolf-chen.github.io/product-support/wallpapers/support.html ← use this
  as the **Support URL** in App Store Connect (English primary).
- https://nightwolf-chen.github.io/product-support/wallpapers/support-zh.html ← Chinese version.
- https://nightwolf-chen.github.io/product-support/wallpapers/privacy.html ← use this
  as the **Privacy Policy URL** in App Store Connect (English primary).
- https://nightwolf-chen.github.io/product-support/wallpapers/privacy-zh.html ← Chinese version.

GifKing (Emoji King GIF / 表情帝GIF):
- https://nightwolf-chen.github.io/product-support/gifking/ ← landing
- https://nightwolf-chen.github.io/product-support/gifking/support.html ← use this
  as the **Support URL** in App Store Connect (English primary).
- https://nightwolf-chen.github.io/product-support/gifking/support-zh.html ← Chinese version.
- https://nightwolf-chen.github.io/product-support/gifking/privacy.html ← use this
  as the **Privacy Policy URL** in App Store Connect (English primary).
- https://nightwolf-chen.github.io/product-support/gifking/privacy-zh.html ← Chinese version.

## Adding another app

Create `<appname>/` with the same page set, link it from the root `index.html`,
extend `tests/check.py`, and document its URLs here.

## Enable Pages

Repo Settings → Pages → Build and deployment → Deploy from a branch →
Branch: `main`, folder: `/ (root)` → Save.

## Contact

https://github.com/nightwolf-chen/product-support/issues
