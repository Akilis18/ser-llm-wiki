import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock

from scripts.answer_wiki import ROOT, answer, log_run, render


SUFFICIENT = {"sufficient": True, "reason": "The passage defines MFCC."}
SUPPORTED = {"supported": [True], "answers_question": True, "reason": "Directly supported."}
UNSUPPORTED = {"supported": [False], "answers_question": True, "reason": "The claim overstates support."}
PASSAGE = "wiki/acoustics.md#L1"


def claim(passage=PASSAGE, source="S02", text="MFCCs summarize spectral properties."):
    return {"claims": [{"text": text, "citations": [{"passage_id": passage, "source_id": source}]}]}


class AnswerWikiTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "wiki").mkdir()
        (self.root / "wiki/acoustics.md").write_text(
            "# Audio features\n\nMFCCs summarize spectral properties. [S02](sources/S02.md), §4, p. 1.\n"
            "\nThe toolkit computes pitch as well. [S07], §2, p. 3.\n",
            encoding="utf-8",
        )
        self.question = "What are MFCCs?"

    def run_answer(self, **kwargs):
        return answer(self.question, root=self.root, **kwargs)

    def test_success_and_provenance(self):
        generator = Mock(return_value=claim())
        reviewer = Mock(side_effect=[SUFFICIENT, SUPPORTED])
        result = self.run_answer(generator=generator, reviewer=reviewer)
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["retries"], 0)
        self.assertEqual(result["attempts"][0]["deterministic"], "pass")
        self.assertEqual(result["attempts"][0]["semantic"], "pass")
        model_input = generator.call_args.args[0]
        self.assertEqual(model_input["phase"], "generate")
        evidence = model_input["passages"][0]
        self.assertEqual(evidence["passage_id"], PASSAGE)
        self.assertIn("[S02], §4, p. 1", evidence["blocks"][0])
        self.assertEqual(evidence["source_ids"], ["S02", "S07"])
        self.assertIn(f"[S02]({PASSAGE})", render(result))

    def test_invalid_citations_and_missing_citation_stop_before_semantic(self):
        for candidate in (
            claim(passage="wiki/absent.md#L1"),
            claim(source="S99"),
            {"claims": [{"text": "Missing citation.", "citations": []}]},
        ):
            with self.subTest(candidate=candidate):
                generator = Mock(return_value=candidate)
                reviewer = Mock(return_value=SUFFICIENT)
                result = self.run_answer(generator=generator, reviewer=reviewer)
                self.assertEqual(result["status"], "validation_failed")
                self.assertEqual(result["retries"], 2)
                self.assertEqual(result["claims"], [])
                self.assertEqual(generator.call_count, 3)
                self.assertEqual(reviewer.call_count, 1)
                self.assertTrue(all(a["deterministic"] == "fail" for a in result["attempts"]))

    def test_semantic_correction_uses_feedback(self):
        generator = Mock(side_effect=[claim(text="MFCCs reveal private feelings."), claim()])
        reviewer = Mock(side_effect=[SUFFICIENT, UNSUPPORTED, SUPPORTED])
        result = self.run_answer(generator=generator, reviewer=reviewer)
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["retries"], 1)
        self.assertEqual([a["semantic"] for a in result["attempts"]], ["fail", "pass"])
        self.assertIn("Unsupported claim numbers: [1]",
                      generator.call_args.args[0]["correction_feedback"])

    def test_semantic_exhaustion_withholds_all_claims(self):
        generator = Mock(return_value=claim())
        reviewer = Mock(side_effect=[SUFFICIENT, UNSUPPORTED, UNSUPPORTED, UNSUPPORTED])
        result = self.run_answer(generator=generator, reviewer=reviewer)
        self.assertEqual((result["status"], result["retries"], result["claims"]),
                         ("validation_failed", 2, []))

    def test_semantic_insufficiency_skips_generation(self):
        generator = Mock()
        reviewer = Mock(return_value={"sufficient": False, "reason": "Related evidence only."})
        result = self.run_answer(generator=generator, reviewer=reviewer)
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertEqual(result["sufficiency"]["semantic"], "fail")
        generator.assert_not_called()

    def test_no_hits_and_dry_run_do_not_call_model(self):
        model = Mock()
        missing = answer("zzznomatch", root=self.root, generator=model)
        self.assertEqual(missing["status"], "insufficient_evidence")
        dry = self.run_answer(generator=model, dry_run=True)
        self.assertEqual(dry["status"], "dry_run")
        self.assertEqual(dry["sufficiency"]["semantic"], "skipped")
        self.assertEqual(dry["attempts"], [])
        model.assert_not_called()

    def test_adapter_errors_and_malformed_review_are_not_successes(self):
        model = Mock(side_effect=OSError("Unavailable adapter"))
        self.assertEqual(self.run_answer(generator=model)["status"], "model_error")
        reviewer = Mock(side_effect=[SUFFICIENT, {}, {}, {}])
        result = self.run_answer(generator=Mock(return_value=claim()), reviewer=reviewer)
        self.assertEqual(result["status"], "model_error")
        self.assertEqual(result["retries"], 2)
        self.assertTrue(all(a["semantic"] == "error" for a in result["attempts"]))

    def test_log_and_cli_default_dry_run(self):
        path = self.root / "runs.log"
        result = self.run_answer()
        log_run(path, result)
        command = [sys.executable, "-B", str(ROOT / "scripts/answer_wiki.py"),
                   "spectrogram frequency", "--log", str(path), "--json"]
        execution = subprocess.run(command, cwd=self.root, capture_output=True,
                                   encoding="utf-8", check=True)
        self.assertEqual(json.loads(execution.stdout)["status"], "dry_run")
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([record["status"] for record in records], ["dry_run", "dry_run"])
        self.assertEqual(records[0]["retrieved"][0]["passage_id"], PASSAGE)
        self.assertNotIn("blocks", records[0]["retrieved"][0])

    def test_cli_command_adapter_round_trip_with_mock_responses(self):
        adapter = self.root / "adapter.py"
        adapter.write_text(
            "import json, sys\n"
            "request = json.load(sys.stdin)\n"
            "phase = request['phase']\n"
            "if phase == 'sufficiency':\n"
            "    response = {'sufficient': True, 'reason': 'Mock decision.'}\n"
            "elif phase == 'generate':\n"
            "    passage = next(p for p in request['passages'] if 'S06' in p['source_ids'])\n"
            "    response = {'claims': [{'text': 'Domain mismatch can cause negative transfer.',\n"
            "                 'citations': [{'passage_id': passage['passage_id'], 'source_id': 'S06'}]}]}\n"
            "else:\n"
            "    response = {'supported': [True], 'answers_question': True, 'reason': 'Mock decision.'}\n"
            "json.dump(response, sys.stdout)\n",
            encoding="utf-8",
        )
        execution = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts/answer_wiki.py"), "negative transfer",
             "--model-command", sys.executable, "--model-arg", str(adapter),
             "--log", str(self.root / "adapter.log"), "--json"],
            capture_output=True, encoding="utf-8", check=True,
        )
        result = json.loads(execution.stdout)
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["attempts"][0]["semantic"], "pass")
        self.assertEqual(result["claims"][0]["citations"][0]["source_id"], "S06")
