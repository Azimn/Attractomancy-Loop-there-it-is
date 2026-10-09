import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analysis", ROOT / "analysis.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)

class TestAnalysis(unittest.TestCase):
    def test_null_not_invented(self):
        with self.assertRaises(ValueError):
            analysis.summarize([])
    def test_cliffs(self):
        self.assertEqual(analysis.cliffs([2, 3], [0, 1]), 1.0)
        self.assertEqual(analysis.cliffs([0, 1], [2, 3]), -1.0)
    def test_cluster_complete(self):
        rows=[]
        for m in ["a","b"]:
            for c in "ABCD":
                for i in range(5):
                    rows.append(dict(model=m, condition=c, run_id=str(i), question_id="Q1",
                        response="real text not simulated", factual_recall=str("ABCD".index(c)),
                        identity_consistency="", characteristic_judgment="",
                        relationship_continuity="", spontaneous_expression="", resistance=""))
        result=analysis.summarize(rows)
        self.assertEqual(len(result["models"]), 2)
        self.assertEqual(len(result["models"]["a"]["comparisons"]), 4)
    def test_recovery_not_attributed(self):
        rows=[dict(model="a", condition="D", run_id="1", question_id="Q12",
                   response="x", factual_recall="4", identity_consistency="4",
                   characteristic_judgment="", relationship_continuity="",
                   spontaneous_expression="", resistance="")]
        self.assertEqual(analysis.run_mean(rows), {})
if __name__ == "__main__": unittest.main()
