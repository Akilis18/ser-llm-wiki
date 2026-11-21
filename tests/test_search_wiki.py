import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.search_wiki import ROOT, load_passages, search


class SearchWikiTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def test_rank_and_limit(self):
        self.write("wiki/features.md", "# Pitch contours\n\nA pitch contour tracks pitch over time.")
        self.write("wiki/intro.md", "# Intro\n\nSome systems use pitch.")
        results = search("What is a pitch contour?", root=self.root)
        self.assertEqual([result.path for result in results], ["wiki/features.md", "wiki/intro.md"])
        self.assertGreater(results[0].score, results[1].score)
        self.assertEqual(search("What is a pitch contour?", root=self.root, limit=1), results[:1])

    def test_empty_queries(self):
        self.write("wiki/index.md", "# Intro\n\nPitch over time.")
        for query in ("", " \t\n", "?!", "what is the"):
            with self.subTest(query=query):
                self.assertEqual(search(query, root=self.root), [])

    def test_mfcc_alias_and_comparison_snippet_on_real_wiki(self):
        singular = search("What is MFCC?")
        self.assertEqual(singular, search("What are MFCCs?"))
        self.assertTrue(any("transformed summary" in item.snippet for item in singular))
        comparison = search("What is the difference between MFCCs and a mel spectrogram?")[0]
        self.assertIn("mel-spectrogram", comparison.snippet)
        self.assertIn("MFCCs give", comparison.snippet)
        self.assertEqual(comparison.source_ids, ("S01", "S07"))

    def test_no_matches_and_wiki_only(self):
        self.write("wiki/intro.md", "# Intro\n\n[Pitch](https://example.com/urlterm).")
        self.write("wiki/notes.txt", "alienword")
        self.write("docs/notes.md", "alienword")
        self.write("raw/S01.pdf", "alienword")
        for query in ("alienword", "urlterm"):
            self.assertEqual(search(query, root=self.root), [])
        self.assertEqual(search("pitch", root=self.root)[0].source_ids, ())

    def test_headings_and_citations(self):
        self.write("wiki/topic.md",
                   "# Topic\n\nOverview.\n\n## Pitch\n\nPitch pattern [S02](sources/S02.md), §4, p. 1.\n"
                   "\n```\n## Fake heading\n```\n\n## Energy\n\nEnergy pattern [S07].")
        self.write("wiki/sources/S02.md", "# S02 · Features\n\n## Role\n\nToolkit architecture.")
        self.assertEqual([p.heading for p in load_passages(self.root)],
                         ["Role", "Topic", "Pitch", "Energy"])
        pitch = search("pitch", root=self.root)[0]
        self.assertEqual(pitch.heading, "Pitch")
        self.assertEqual(pitch.source_ids, ("S02",))
        self.assertIn("[S02], §4, p. 1", pitch.snippet)
        self.assertEqual(search("energy", root=self.root)[0].source_ids, ("S07",))
        self.assertEqual(search("toolkit", root=self.root)[0].source_ids, ("S02",))

    def test_source_table_uses_matching_row(self):
        self.write("wiki/sources/S04.md",
                   "# S04\n\n## Evidence\n\n| Claim | Location |\n|---|---|\n"
                   "| Valence ratings | [S04], §5.2, p. 13 |\n"
                   "| Session count | [S04], §3.2, p. 7 |\n")
        result = search("valence", root=self.root)[0]
        self.assertIn("§5.2, p. 13", result.snippet)
        self.assertNotIn("Session count", result.snippet)

    def test_determinism_and_tie_breaks(self):
        self.write("wiki/z.md", "## First\n\nSame data.")
        self.write("wiki/a.md", "## Third\n\nSame data.\n\n## First\n\nSame data.")
        first = search("same data", root=self.root)
        self.assertEqual(first, search("DATA same same", root=self.root))
        self.assertEqual([(r.path, r.heading) for r in first],
                         [("wiki/a.md", "Third"), ("wiki/a.md", "First"), ("wiki/z.md", "First")])
        self.assertEqual(len({r.score for r in first}), 1)

    def test_cli_search_and_no_matches(self):
        command = [sys.executable, str(ROOT / "scripts/search_wiki.py")]
        result = subprocess.run(command + ["negative transfer", "--limit", "1"],
                                cwd=self.root, capture_output=True, encoding="utf-8", check=True)
        self.assertIn("wiki/concepts/ser-limitations.md | When transfer can fail", result.stdout)
        self.assertIn("sources [S06]", result.stdout)
        missing = subprocess.run(command + ["zzznomatch"], cwd=self.root,
                                 capture_output=True, encoding="utf-8", check=True)
        self.assertIn("No matching Wiki passages", missing.stdout)
        empty = subprocess.run(command, cwd=self.root, capture_output=True,
                               encoding="utf-8", check=True)
        self.assertIn("No matching Wiki passages", empty.stdout)
