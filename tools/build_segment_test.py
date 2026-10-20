#!/usr/bin/env python3
"""Build the isolated mobile experiment from one pinned, already-published SVG.

This intentionally does not change build.py, README.md or scheduled generation.
The source hash guards the snapshot-specific element ranges below. For a new
layout, inspect the section boundaries again instead of blindly reusing them.
Requires the project's fonttools + brotli dependencies.
Run: python3 tools/build_segment_test.py
After the daily SVG changes, pass --source with a copy of assets/shinycolors.svg
from SOURCE_COMMIT. This keeps the production image untouched.
"""
import argparse
import base64
import copy
import hashlib
import io
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/shinycolors.svg"
OUT = ROOT / "assets/mobile-segment-test"
SOURCE_COMMIT = "650b5b923f19ef8c3d56f701f70160e238d4af28"
SOURCE_HASH = "9a761e9a6c4977e2ec0cd41bbc772ed5d07f977bd9aa43da6b6d0ca0b727d100"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ANIMATION = {"animate", "animateTransform", "animateMotion"}
# name, title, global top, bottom, top-level body range (end exclusive)
SECTIONS = [
    ("01-home", "首页", 0, 680, 6, 119),
    ("02-projects", "项目", 680, 1232, 119, 132),
    ("03-produce", "培育", 1232, 1924, 132, 204),
    ("04-producer", "制作人详情", 1924, 2438, 204, 337),
    ("05-missions", "任务", 2438, 3000, 337, 435),
    ("06-about", "关于", 3000, 3564, 435, 498),
    ("07-footer", "页脚", 3564, 3722, 498, 503),
]


def tag(e):
    return e.tag.rsplit("}", 1)[-1]


def references(e):
    found = set()
    for node in e.iter():
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1] == "href" and value.startswith("#"):
                found.add(value[1:])
            found.update(re.findall(r"url\(['\"]?#([^)'\"]+)", value))
    return found


def prune_definitions(svg):
    defs = svg.find(f"{{{NS}}}defs")
    original = list(defs)
    for child in original:
        defs.remove(child)
    # Keep styles, then subset their original font to this segment's text.
    retained = [e for e in original if tag(e) == "style"]
    for e in retained:
        defs.append(e)
    by_id = {n.get("id"): e for e in original for n in e.iter() if n.get("id")}
    while True:
        existing = {n.get("id") for n in svg.iter() if n.get("id")}
        missing = references(svg) - existing
        if not missing:
            break
        for ident in sorted(missing):
            if ident not in by_id:
                raise ValueError(f"Unresolved SVG reference: {ident}")
            e = by_id[ident]
            if e not in retained:
                retained.append(e)
                defs.append(e)
    # Restore source ordering; IDs themselves and all animation timings survive.
    for e in list(defs):
        defs.remove(e)
    for e in original:
        if e in retained:
            defs.append(e)


def subset_font(svg):
    text = "".join("".join(e.itertext()) for e in svg.iter() if tag(e) == "text")
    for style in svg.iter(f"{{{NS}}}style"):
        def replace(match):
            font = TTFont(io.BytesIO(base64.b64decode(match[1])), recalcTimestamp=False)
            options = subset.Options()
            options.recalc_timestamp = False
            sub = subset.Subsetter(options=options)
            sub.populate(text=text)
            sub.subset(font)
            data = io.BytesIO()
            font.save(data)
            return "data:font/woff2;base64," + base64.b64encode(data.getvalue()).decode()
        style.text = re.sub(r"data:font/woff2;base64,([A-Za-z0-9+/=]+)", replace, style.text or "")


def main(source_path=SOURCE):
    source = source_path.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_HASH:
        raise SystemExit("Source changed. Restore the pinned SVG or review section ranges before regenerating.")
    original = ET.fromstring(source)
    assert original.get("viewBox") == "0 0 1136 3722"
    assert len(original.find(f"{{{NS}}}g")) == 503
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"source_commit": SOURCE_COMMIT, "source_sha256": SOURCE_HASH,
                "source_bytes": len(source), "sections": []}
    all_animations = []
    for name, title, top, bottom, lo, hi in SECTIONS:
        svg = copy.deepcopy(original)
        svg.set("viewBox", f"0 {top} 1136 {bottom - top}")
        svg.set("height", str(bottom - top))
        svg.set("aria-label", f"Lisianthus · {title}")
        svg.find(f"{{{NS}}}title").text = f"Lisianthus · {title}"
        body = svg.find(f"{{{NS}}}g")
        for i, child in enumerate(list(body)):
            if i >= 6 and not lo <= i < hi:
                body.remove(child)
        frame = svg.find(f"{{{NS}}}clipPath")
        if top == 0 or bottom == 3722:
            # Preserve the outer corners using a section-sized clip, with square
            # internal edges. The middle sections need no extra root clip.
            frame.clear()
            frame.set("id", "frame")
            path = (f"M18 0H1118A18 18 0 0 1 1136 18V{bottom}H0V18A18 18 0 0 1 18 0Z"
                    if top == 0 else
                    f"M0 {top}H1136V3704A18 18 0 0 1 1118 3722H18A18 18 0 0 1 0 3704Z")
            ET.SubElement(frame, f"{{{NS}}}path", {"d": path})
        else:
            body.attrib.pop("clip-path", None)
            svg.remove(frame)
        prune_definitions(svg)
        subset_font(svg)
        animations = [ET.tostring(e) for e in svg.iter() if tag(e) in ANIMATION]
        all_animations.extend(animations)
        payload = ET.tostring(svg, encoding="utf-8", xml_declaration=True)
        (OUT / f"{name}.svg").write_bytes(payload)
        manifest["sections"].append({"file": f"{name}.svg", "title": title,
                                     "y": top, "height": bottom-top,
                                     "body_range": [lo, hi], "bytes": len(payload),
                                     "animations": len(animations),
                                     "embedded_images": sum(tag(e) == "image" for e in svg.iter())})
    expected = [ET.tostring(e) for e in original.iter() if tag(e) in ANIMATION]
    assert sorted(expected) == sorted(all_animations), "Animation was lost, duplicated or changed"
    assert sum(s["height"] for s in manifest["sections"]) == 3722
    manifest["total_bytes"] = sum(s["bytes"] for s in manifest["sections"])
    manifest["total_animations"] = len(all_animations)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    images = "".join(f'<img src="assets/mobile-segment-test/{s["file"]}?v=segments-1" width="100%" align="top" alt="{s["title"]}"/>' for s in manifest["sections"])
    markdown = f'''# 手机分段渲染测试

[打开同一份数据的原版长图对照](https://github.com/Gu-Haojia/Gu-Haojia/blob/{SOURCE_COMMIT}/README.md)

此页把原图拆成 7 张独立 SVG，保留底纹、文字、人物及动画参数。请用同一个手机浏览器分别停留首页、培育、任务，再上下滚动比较流畅度、发热和拼接处。测试快照：2026-10-21；本页不会每日更新。

<p align="center">{images}</p>

测试页独立于正式主页。数据与画面来源：`{SOURCE_COMMIT[:7]}`；复现脚本：[`tools/build_segment_test.py`](tools/build_segment_test.py)。
'''
    (ROOT / "mobile-segment-test.md").write_text(markdown)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    main(parser.parse_args().source)
