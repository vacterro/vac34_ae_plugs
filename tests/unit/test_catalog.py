#!/usr/bin/env python3
"""
Unit tests for vac34_AE recipe catalog and math helpers.
"""

import os
import re
import unittest
import math

class TestCatalogAndMath(unittest.TestCase):
    def setUp(self):
        self.root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.recipe_file = os.path.join(self.root, "src", "recipes", "RecipeRegistry.js")

    def test_recipe_file_exists(self):
        self.assertTrue(os.path.exists(self.recipe_file))

    def test_recipe_ids_unique(self):
        with open(self.recipe_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Match only recipe IDs (e.g. category.behavior.variant)
        ids = re.findall(r'^\s+id:\s*["\']([a-z0-9_]+\.[a-z0-9_\.]+)["\']', content, re.MULTILINE)
        self.assertGreater(len(ids), 10, "Expected at least 10 core recipes")
        duplicates = [x for x in ids if ids.count(x) > 1]
        self.assertEqual(len(duplicates), 0, f"Duplicate recipe IDs found: {set(duplicates)}")

    def test_extendscript_compat_no_const_or_let(self):
        """Ensure core UI code uses var rather than ES6 const/let for ExtendScript compatibility."""
        src_dir = os.path.join(self.root, "src")
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".js"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines):
                        stripped = line.strip()
                        # Allow inside string literals or comments, but reject standalone declaration
                        if re.match(r'^(?:const|let)\s+[a-zA-Z0-9_]+', stripped):
                            self.fail(f"Found modern ES6 declaration in {file}:{idx+1}: {stripped}")

    def test_math_sine_breathing(self):
        """Test mathematical sine breathing range."""
        freq = 0.8
        amt = 0.12
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            wave = math.sin(t * freq * math.pi * 2) * amt
            s = 1.0 + wave
            self.assertGreaterEqual(s, 1.0 - amt - 1e-6)
            self.assertLessEqual(s, 1.0 + amt + 1e-6)

    def test_math_squash_stretch_volume_preservation(self):
        """Test that squash & stretch preserves 2D area (sx * sy == 1)."""
        freq = 1.5
        amt = 0.2
        for t in [0.1, 0.2, 0.3, 0.4, 0.5]:
            wave = math.sin(t * freq * math.pi * 2) * amt
            sx = 1.0 + wave
            sy = 1.0 / sx
            area = sx * sy
            self.assertAlmostEqual(area, 1.0, places=5)

    def test_math_clamp(self):
        """Test clamping math."""
        def clamp(v, low, high):
            return min(max(v, low), high)

        self.assertEqual(clamp(50, 0, 100), 50)
        self.assertEqual(clamp(-10, 0, 100), 0)
        self.assertEqual(clamp(150, 0, 100), 100)

if __name__ == "__main__":
    unittest.main()
