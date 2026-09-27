#!/usr/bin/env python3
"""Checks for the product-support static site.

Layout: root index.html is the app hub; each app lives in its own subdir
(e.g. wallpapers/). Run: python3 tests/check.py. Exit 0 = all pass.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "wallpapers"
GK = ROOT / "gifking"
failures = []


def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href:
                self.links.append(href)


for fname in ["index.html", "README.md", "wallpapers/index.html",
              "wallpapers/privacy.html", "wallpapers/privacy-zh.html",
              "wallpapers/support.html", "wallpapers/support-zh.html",
              "gifking/index.html",
              "gifking/privacy.html", "gifking/privacy-zh.html",
              "gifking/support.html", "gifking/support-zh.html"]:
    check(f"{fname}-exists", (ROOT / fname).exists())

privacy_en = (WP / "privacy.html").read_text()
privacy_zh = (WP / "privacy-zh.html").read_text()
support_en = (WP / "support.html").read_text()
support_zh = (WP / "support-zh.html").read_text()
hub = (ROOT / "index.html").read_text()
wp_index = (WP / "index.html").read_text()
readme = (ROOT / "README.md").read_text()
gk_index = (GK / "index.html").read_text()
gk_privacy_en = (GK / "privacy.html").read_text()
gk_privacy_zh = (GK / "privacy-zh.html").read_text()
gk_support_en = (GK / "support.html").read_text()
gk_support_zh = (GK / "support-zh.html").read_text()

# English privacy page: required disclosures (must match PrivacyInfo.xcprivacy + ATT).
for kw in ["Tracking", "AdMob", "IDFA", "googleads.g.doubleclick.net",
            "googlesyndication.com", "App Tracking Transparency",
            "Unsplash", "Pexels", "Pixabay", "Flickr", "Openverse",
            "Wikimedia", "Bing",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"en-has-{kw[:24]}", kw in privacy_en, f"missing {kw!r}")

# English pages must not contain Chinese body copy (split pages, not combined).
check("en-no-chinese-body", "隐私政策" not in privacy_en and "跟踪透明度" not in privacy_en,
      "English page should link the Chinese page, not embed it")

# Chinese privacy page: full translation present.
for kw in ["隐私政策", "跟踪", "广告标识符", "生效日期", "IDFA", "AdMob",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"zh-has-{kw[:12]}", kw in privacy_zh, f"missing {kw!r}")

# Cross-links between language versions + hub backlinks.
check("en-links-zh", "privacy-zh.html" in privacy_en, "EN privacy must link 中文版")
check("zh-links-en", "privacy.html" in privacy_zh, "ZH privacy must link English version")
check("support-en-links-zh", "support-zh.html" in support_en, "EN support must link 中文版")
check("support-zh-links-en", 'href="support.html"' in support_zh,
      "ZH support must link English version")
check("support-en-links-privacy", "privacy.html" in support_en, "EN support must link privacy")
check("support-zh-links-privacy", "privacy-zh.html" in support_zh, "ZH support must link privacy")
for name, text in [("privacy_en", privacy_en), ("privacy_zh", privacy_zh),
                   ("support_en", support_en), ("support_zh", support_zh)]:
    check(f"{name}-links-hub", "../index.html" in text, "app page must link hub")

# Effective dates on both privacy pages.
check("en-date", "September 27, 2026" in privacy_en, "EN effective date missing")
check("zh-date", "2026 年 9 月 27 日" in privacy_zh, "ZH effective date missing")

# No leftover placeholders in any page.
for kw in ["TODO", "FIXME", "your-email@", "example.com", "lorem"]:
    check(f"no-{kw.lower()}", all(kw.lower() not in t.lower()
           for t in [privacy_en, privacy_zh, support_en, support_zh, hub, wp_index,
                     gk_privacy_en, gk_privacy_zh, gk_support_en, gk_support_zh,
                     gk_index]),
           "placeholder left")

# Support pages: FAQ content in the right language.
for kw in ["wallpaper", "Use as Wallpaper", "Tracking", "AdMob", "cache",
            "Favorites", "iOS 15",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"support-en-{kw[:20]}", kw in support_en, f"missing {kw!r}")
check("support-en-no-chinese", "设为壁纸" not in support_en and "常见问题" not in support_en,
      "EN support should link the Chinese page, not embed it")
for kw in ["设为壁纸", "用作墙纸", "跟踪", "缓存", "收藏", "常见问题",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"support-zh-{kw[:12]}", kw in support_zh, f"missing {kw!r}")

# HTML parses + internal links resolve (relative to each file's directory).
pages = [("index.html", ROOT, hub), ("wallpapers/index.html", WP, wp_index),
         ("wallpapers/privacy.html", WP, privacy_en),
         ("wallpapers/privacy-zh.html", WP, privacy_zh),
         ("wallpapers/support.html", WP, support_en),
         ("wallpapers/support-zh.html", WP, support_zh),
         ("gifking/index.html", GK, gk_index),
         ("gifking/privacy.html", GK, gk_privacy_en),
         ("gifking/privacy-zh.html", GK, gk_privacy_zh),
         ("gifking/support.html", GK, gk_support_en),
         ("gifking/support-zh.html", GK, gk_support_zh)]
for fname, base, text in pages:
    p = LinkParser()
    try:
        p.feed(text)
        check(f"{fname}-parses", True)
    except Exception as e:  # noqa: BLE001
        check(f"{fname}-parses", False, str(e))
        continue
    for href in p.links:
        if href.startswith("http"):
            continue
        target = (base / href).resolve()
        check(f"{fname}-link-{href}", str(target).startswith(str(ROOT)) and target.exists(),
              "broken internal link")

# Hub lists the app with sub-links to all its pages.
check("hub-links-wallpapers", "wallpapers/" in hub, "hub must link the wallpapers app")
check("hub-product-section", 'id="wallpapers"' in hub and "Our Apps" in hub,
      "hub must be a products page with a wallpapers section")
for page in ["wallpapers/support.html", "wallpapers/support-zh.html",
             "wallpapers/privacy.html", "wallpapers/privacy-zh.html"]:
    check(f"hub-sublink-{page.split('/')[-1]}", page in hub, f"hub must sub-link {page}")
for page in ["support.html", "support-zh.html", "privacy.html", "privacy-zh.html"]:
    check(f"wp-index-links-{page}", page in wp_index, f"app landing must link {page}")
    check(f"gk-index-links-{page}", page in gk_index, f"gifking landing must link {page}")

# Hub lists gifking with sub-links to all its pages.
check("hub-links-gifking", "gifking/" in hub, "hub must link the gifking app")
check("hub-product-section-gk", 'id="gifking"' in hub,
      "hub must have a gifking product section")
for page in ["gifking/support.html", "gifking/support-zh.html",
             "gifking/privacy.html", "gifking/privacy-zh.html"]:
    check(f"hub-sublink-gk-{page.split('/')[-1]}", page in hub, f"hub must sub-link {page}")

# GifKing (Emoji King GIF): same page conventions as wallpapers.
for kw in ["Tracking", "AdMob", "UMeng", "NO-IDFA", "Device ID",
            "googleads.g.doubleclick.net", "googlesyndication.com",
            "PrivacyInfo.xcprivacy",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"gk-en-{kw[:24]}", kw in gk_privacy_en, f"missing {kw!r}")
check("gk-en-no-chinese-body",
      "隐私政策" not in gk_privacy_en and "常见问题" not in gk_privacy_en,
      "English page should link the Chinese page, not embed it")
for kw in ["隐私政策", "跟踪", "友盟", "广告", "生效日期", "IDFA",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"gk-zh-{kw[:12]}", kw in gk_privacy_zh, f"missing {kw!r}")
check("gk-en-links-zh", "privacy-zh.html" in gk_privacy_en, "EN privacy must link 中文版")
check("gk-zh-links-en", "privacy.html" in gk_privacy_zh, "ZH privacy must link English version")
check("gk-support-en-links-zh", "support-zh.html" in gk_support_en,
      "EN support must link 中文版")
check("gk-support-zh-links-en", 'href="support.html"' in gk_support_zh,
      "ZH support must link English version")
check("gk-support-en-links-privacy", "privacy.html" in gk_support_en,
      "EN support must link privacy")
check("gk-support-zh-links-privacy", "privacy-zh.html" in gk_support_zh,
      "ZH support must link privacy")
for name, text in [("gk_privacy_en", gk_privacy_en), ("gk_privacy_zh", gk_privacy_zh),
                   ("gk_support_en", gk_support_en), ("gk_support_zh", gk_support_zh)]:
    check(f"{name}-links-hub", "../index.html" in text, "app page must link hub")
check("gk-en-date", "September 27, 2026" in gk_privacy_en, "EN effective date missing")
check("gk-zh-date", "2026 年 9 月 27 日" in gk_privacy_zh, "ZH effective date missing")
for kw in ["GIF", "Favorites", "Share", "AdMob", "Dark Mode", "Photos",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"gk-support-en-{kw[:20]}", kw in gk_support_en, f"missing {kw!r}")
check("gk-support-en-no-chinese",
      "常见问题" not in gk_support_en and "收藏" not in gk_support_en,
      "EN support should link the Chinese page, not embed it")
for kw in ["表情", "收藏", "分享", "广告", "深色", "常见问题",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"gk-support-zh-{kw[:12]}", kw in gk_support_zh, f"missing {kw!r}")

# README documents the new public URLs.
for url in ["product-support/wallpapers/support.html",
            "product-support/wallpapers/privacy.html",
            "product-support/gifking/support.html",
            "product-support/gifking/privacy.html"]:
    check(f"readme-{url.split('/')[-1]}", url in readme, "README must document " + url)

print()
if failures:
    print(f"{len(failures)} FAILURES: {failures}")
    sys.exit(1)
print("All site checks passed.")
