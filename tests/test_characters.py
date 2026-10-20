"""Selection preserves the profile; the random pool excludes hana_old."""
import base64
import copy
import json
import re
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

from PIL import Image

import build


class CharacterTests(unittest.TestCase):
    def test_complete_catalog_has_28_current_characters_and_one_fixed_only_option(self):
        rows = build.character_catalog()
        self.assertEqual(len(rows), 29)
        self.assertEqual(len({r["id"] for r in rows}), 29)
        self.assertEqual([r["id"] for r in rows if not r.get("random", True)], ["hana_old"])
        for row in rows:
            with self.subTest(character=row["id"]):
                for alias in [row["id"], row["name"], *row["aliases"]]:
                    self.assertEqual(build.selected_character(alias)["id"], row["id"])
                with Image.open(build.ROOT / row["file"]) as im:
                    self.assertEqual(im.mode, "RGBA")
                    self.assertEqual(im.size, (1024, 1536))
                    self.assertEqual(im.getchannel("A").getextrema()[0], 0)

    def test_explicit_selection_changes_only_the_character_field(self):
        cfg = copy.deepcopy(build.load_config())
        before = copy.deepcopy(cfg)
        selected = build.config_with_character(cfg, "樋口 円香")
        self.assertEqual(selected, {**before, "character": "madoka"})
        self.assertEqual(cfg, before)
        self.assertEqual(build.config_with_character(cfg, "鈴木羽那（旧版）")["character"], "hana_old")
        for bad in ("missing", None, 5, ""):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                build.config_with_character(cfg, bad)

    def test_random_render_chooses_from_28_without_overwriting_saved_mode(self):
        cfg = {"nickname": "Example", "character": "random"}
        with patch.object(build.random, "choice", return_value=build.selected_character("madoka")) as choose, \
             patch.object(build, "compose", return_value=("", "", "", 100)) as compose:
            build.render(cfg, {}, {"level": 1, "streak": 0})
            self.assertEqual(compose.call_args.args[0]["character"], "madoka")
            self.assertEqual(cfg["character"], "random")
            choose.assert_called_once()
            candidates = choose.call_args.args[0]
            self.assertEqual(len(candidates), 28)
            self.assertNotIn("hana_old", [r["id"] for r in candidates])

    def test_old_hana_is_a_normal_fixed_catalog_choice(self):
        cfg = {"character": "hana_old"}
        with patch.object(build.random, "choice", side_effect=AssertionError("fixed selection rerolled")):
            self.assertEqual(build.resolve_character_choice(cfg), cfg)
        old = build.illustration_path(cfg)
        new = build.illustration_path({"character": "hana"})
        self.assertEqual(old.name, "hana_old-coding.webp")
        self.assertNotEqual(old.read_bytes(), new.read_bytes())

    def test_all_artwork_is_embedded_without_changing_pixels_or_float_distance(self):
        for row in build.character_catalog():
            with self.subTest(character=row["id"]), patch.object(build, "DEFS", {}):
                markup = build.character_artwork(0, {"character": row["id"]})
                root = ET.fromstring("<svg>" + build.DEFS["characterArtwork"] + markup + "</svg>")
                data = base64.b64decode(root.find("image").get("href").split(",", 1)[1])
                self.assertEqual(data, (build.ROOT / row["file"]).read_bytes())
                motion = root.find(".//animateTransform")
                self.assertEqual(motion.get("type"), "translate")
                self.assertEqual(motion.get("values"), "0 0;0 5;0 0")

    def test_watch_does_not_reroll_and_tracks_the_correct_assets(self):
        with patch.object(build.random, "choice", side_effect=AssertionError("watch rerolled")):
            a = build.watch_signature("random")
            self.assertEqual(a, build.watch_signature("random"))
        old = str(build.illustration_path({"character": "hana_old"}))
        self.assertNotIn(old, {p for p, _ in a})
        self.assertIn(old, {p for p, _ in build.watch_signature("hana_old")})
        expected = {str(build.ROOT / r["file"]) for r in build.character_catalog() if r.get("random", True)}
        self.assertTrue(expected <= {p for p, _ in a})

    def test_workflow_offers_old_hana_and_preserves_existing_schedule(self):
        workflow = (build.ROOT / ".github/workflows/shiny-refresh.yml").read_text()
        block = workflow.split("options:\n", 1)[1].split("  push:", 1)[0]
        choices = re.findall(r"^\s+- (.+)$", block, re.M)
        self.assertEqual(set(choices), {"from-config", "random", *[r["name"] for r in build.character_catalog()]})
        self.assertIn('cron: "0 16 * * *"', workflow)


if __name__ == "__main__":
    unittest.main()
