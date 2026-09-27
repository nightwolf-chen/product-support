#!/usr/bin/env python3
"""Checks for the product-support static site.

Run: python3 tests/check.py
Exit 0 = all pass.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


for fname in ["privacy.html", "privacy-zh.html", "support.html", "support-zh.html",
              "index.html", "README.md"]:
    check(f"{fname}-exists", (ROOT / fname).exists())

privacy_en = (ROOT / "privacy.html").read_text()
privacy_zh = (ROOT / "privacy-zh.html").read_text()
support_en = (ROOT / "support.html").read_text()
support_zh = (ROOT / "support-zh.html").read_text()
index = (ROOT / "index.html").read_text()

# English page: required disclosures (must match PrivacyInfo.xcprivacy + ATT behavior).
for kw in ["Tracking", "AdMob", "IDFA", "googleads.g.doubleclick.net",
            "googlesyndication.com", "App Tracking Transparency",
            "Unsplash", "Pexels", "Pixabay", "Flickr", "Openverse",
            "Wikimedia", "Bing",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"en-has-{kw[:24]}", kw in privacy_en, f"missing {kw!r}")

# English page must not contain Chinese body copy (split pages, not combined).
check("en-no-chinese-body", "隐私政策" not in privacy_en and "跟踪透明度" not in privacy_en,
      "English page should link the Chinese page, not embed it")

# Chinese page: full translation present.
for kw in ["隐私政策", "跟踪", "广告标识符", "生效日期", "IDFA", "AdMob",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"zh-has-{kw[:12]}", kw in privacy_zh, f"missing {kw!r}")

# Cross-links between language versions.
check("en-links-zh", "privacy-zh.html" in privacy_en, "EN page must link 中文版")
check("zh-links-en", "privacy.html" in privacy_zh, "ZH page must link English version")

# Effective dates on both.
check("en-date", "September 27, 2026" in privacy_en, "EN effective date missing")
check("zh-date", "2026 年 9 月 27 日" in privacy_zh, "ZH effective date missing")

# No leftover placeholders in any page.
for kw in ["TODO", "FIXME", "your-email@", "example.com", "lorem"]:
    check(f"no-{kw.lower()}", all(kw.lower() not in t.lower()
          for t in [privacy_en, privacy_zh, support_en, support_zh]),
          "placeholder left")

# Support pages: FAQ content in the right language, cross-linked.
for kw in ["wallpaper", "Use as Wallpaper", "Tracking", "AdMob", "cache",
            "Favorites", "iOS 15",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"support-en-{kw[:20]}", kw in support_en, f"missing {kw!r}")
check("support-en-no-chinese", "设为壁纸" not in support_en and "常见问题" not in support_en,
      "EN support should link the Chinese page, not embed it")
for kw in ["设为壁纸", "用作墙纸", "跟踪", "缓存", "收藏", "常见问题",
            "https://github.com/nightwolf-chen/product-support/issues"]:
    check(f"support-zh-{kw[:12]}", kw in support_zh, f"missing {kw!r}")
check("support-en-links-zh", "support-zh.html" in support_en, "EN support must link 中文版")
check("support-zh-links-en", 'href="support.html"' in support_zh,
      "ZH support must link English version")
check("support-en-links-privacy", "privacy.html" in support_en, "EN support must link privacy")
check("support-zh-links-privacy", "privacy-zh.html" in support_zh, "ZH support must link privacy")

# HTML parses + internal links resolve.
for fname, text in [("privacy.html", privacy_en), ("privacy-zh.html", privacy_zh),
                    ("support.html", support_en), ("support-zh.html", support_zh),
                    ("index.html", index)]:
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
        target = (ROOT / href).resolve()
        check(f"{fname}-link-{href}", str(target).startswith(str(ROOT)) and target.exists(),
              "broken internal link")

check("index-links-privacy-en", "privacy.html" in index, "index must link English privacy page")
check("index-links-support-en", "support.html" in index, "index must link English support page")
check("index-links-support-zh", "support-zh.html" in index, "index must link Chinese support page")
check("readme-links-support-url",
      "nightwolf-chen.github.io/product-support/support.html" in (ROOT / "README.md").read_text(),
      "README must document the public support URL")
check("index-links-privacy-zh", "privacy-zh.html" in index, "index must link Chinese privacy page")
check("readme-links-privacy-url",
      "nightwolf-chen.github.io/product-support/privacy.html" in (ROOT / "README.md").read_text(),
      "README must document the public privacy URL")

print()
if failures:
    print(f"{len(failures)} FAILURES: {failures}")
    sys.exit(1)
print("All site checks passed.")
