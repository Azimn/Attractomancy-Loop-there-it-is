import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analysis", ROOT / "analysis.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)

class DimensionTests(unittest.TestCase):
    def test_only_base_counts_for_primary(self):
        rows = []
        for c in "ABCD":
            for i in range(5):
                common = {"model":"m","condition":c,"run_id":str(i),"response":"x"}
                for q, phase, val in [("Q1","base","1"),("Q11","post_distractor","4")]:
                    rows.append(dict(common, question_id=q,phase=phase,factual_recall=val,
                        identity_consistency=val, characteristic_judgment=val,relationship_continuity=val,
                        spontaneous_expression="",resistance=""))
        result = analysis.summarize(rows)["models"]["m"]
        self.assertEqual(result["per_run_scores"]["D"], [1.] * 5)
        self.assertEqual(result["perturbation_survival"]["D"]["mean_q1_q11_delta"], 3.)
        self.assertEqual(result["dimension_comparisons"]["factual_recall"]["per_run"]["D"], [1.] * 5)
    def test_primary_not_confounded_by_style(self):
        rows=[]
        for c in "ABCD":
            for i in range(5):
                rows.append(dict(model="m",condition=c,run_id=str(i),question_id="Q3",phase="base",response="x",
                    factual_recall="1",characteristic_judgment="1",relationship_continuity="1",
                    identity_consistency="4" if c=="D" else "0",spontaneous_expression="4" if c=="D" else "0",resistance=""))
        out=analysis.summarize(rows)["models"]["m"]
        self.assertEqual(out["per_run_scores"]["D"],[1.]*5)
        self.assertEqual(out["per_run_scores"]["C"],[1.]*5)
        self.assertEqual(out["comparisons"][0]["mean_difference"],0.0)
    def test_missing_primary_dimension_is_not_eligible(self):
        rows=[dict(model="m",condition="D",run_id="1",question_id="Q3",phase="base",response="x",factual_recall="4",
            characteristic_judgment="",relationship_continuity="4",identity_consistency="4",spontaneous_expression="",resistance="")]
        self.assertEqual(analysis.run_mean(rows),{})
    def test_no_false_cue_effect(self):
        rows = [{"model":"m","condition":"D","run_id":"a","question_id":"Q12-1",
                 "response":"x","phase":"cue_only_new_session","factual_recall":"4",
                 "identity_consistency":"","characteristic_judgment":"",
                 "relationship_continuity":"","spontaneous_expression":"","resistance":""}]
        result=analysis.summarize(rows)
        self.assertEqual(result["models"], {})
if __name__ == "__main__": unittest.main()
