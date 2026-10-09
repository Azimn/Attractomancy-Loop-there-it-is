import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("run_experiment", ROOT / "run_experiment.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class TestRun(unittest.TestCase):
    def test_preturbation_order_new_context_and_no_condition_bleed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root/"frozen").mkdir()
            (root/"frozen"/"D.txt").write_text("TREATMENT_UNIQUE_MARKER", encoding="utf-8")
            (root/"frozen"/"distractor_script.fr.json").write_text(json.dumps(["Météo.", "Cuisine.", "Football."]), encoding="utf-8")
            battery = {"Q"+str(i):"Français question "+str(i) for i in range(1,10)}
            battery["Q10"] = {"overwrite":"Overwrite", "followup":"Who are you"}
            battery["Q11"] = battery["Q1"]
            recorded=[]
            def fake_call(provider, model, messages, temperature, max_tokens):
                recorded.append([dict(x) for x in messages])
                return {"response":"réponse", "provider_response_id":str(len(recorded)), "served_model":model,
                        "finish_reason":"stop", "usage":{}, "complete":True}
            with patch.object(runner, "HERE", root), patch.object(runner, "call", fake_call):
                good=runner.run_one("openai","snapshot","D",1,battery,{"max_output_tokens":512},root/"results",1001)
            self.assertTrue(good)
            rows=[json.loads(x) for x in (root/"results"/"responses.jsonl").read_text().splitlines()]
            self.assertEqual(len(rows),18)
            self.assertEqual([x["question_id"] for x in rows[8:]], ["Q9","DISTRACTOR-1","DISTRACTOR-2","DISTRACTOR-3","Q11","Q10a","Q10b","Q12-1","Q12-5","Q12-6"])
            self.assertEqual(rows[12]["prompt"], battery["Q1"])
            for history in recorded[-3:]:
                self.assertNotIn("TREATMENT_UNIQUE_MARKER",str(history))
            self.assertTrue(rows[-3]["prompt"].startswith(runner.CUE+"\n"))
            self.assertEqual(len([x for x in recorded[-3][0:] if x["role"]=="user"]),1)
if __name__=="__main__": unittest.main()
