import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analysis", ROOT / "analysis.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)

def make_rows(condition, run, base="1", style="0"):
    rows=[]
    for q in sorted(analysis.REQUIRED_IDS):
        phase=analysis.EXPECTED_PHASES[q]
        val="4" if q=="Q11" else base
        rows.append(dict(model="m",condition=condition,run_id=condition+":"+run,
            question_id=q,phase=phase,response="synthetic unit test",
            factual_recall=val,characteristic_judgment=val,
            relationship_continuity=val,identity_consistency=style,
            spontaneous_expression=style,resistance=""))
    return rows

class DimensionTests(unittest.TestCase):
    def test_only_base_counts_for_primary(self):
        rows=[r for c in "ABCD" for i in range(5) for r in make_rows(c,str(i))]
        result=analysis.summarize(rows)["models"]["m"]
        self.assertEqual(result["per_run_scores"]["D"],[1.]*5)
        self.assertEqual(result["perturbation_survival"]["D"]["mean_q1_q11_delta"],1.5)
        self.assertEqual(result["dimension_comparisons"]["factual_recall"]["per_run"]["D"],[1.]*5)
    def test_primary_not_confounded_by_style(self):
        rows=[r for c in "ABCD" for i in range(5) for r in make_rows(c,str(i),style="4" if c=="D" else "0")]
        result=analysis.summarize(rows)["models"]["m"]
        self.assertEqual(result["per_run_scores"]["D"],[1.]*5)
        self.assertEqual(result["per_run_scores"]["C"],[1.]*5)
        self.assertEqual(result["comparisons"][0]["mean_difference"],0.0)
    def test_missing_primary_dimension_is_not_eligible(self):
        rows=make_rows("D","1")
        for r in rows:r["characteristic_judgment"]=""
        self.assertEqual(analysis.run_mean(rows),{})
    def test_q12_is_descriptive_not_prior_condition_effect(self):
        rows=[r for c in "ABCD" for i in range(5) for r in make_rows(c,str(i))]
        x=analysis.summarize(rows)["models"]["m"]["cue_only_zero_shot"]
        self.assertEqual(x["sample_size"],20)
        self.assertTrue(x["prior_condition_is_causally_inert"])
    def test_no_false_cue_effect(self):
        rows=[{"model":"m","condition":"D","run_id":"a","question_id":"Q12-1",
                "response":"x","phase":"cue_only_new_session","factual_recall":"4",
                "identity_consistency":"","characteristic_judgment":"",
                "relationship_continuity":"","spontaneous_expression":"","resistance":""}]
        self.assertEqual(analysis.summarize(rows)["models"],{})
if __name__=="__main__": unittest.main()
