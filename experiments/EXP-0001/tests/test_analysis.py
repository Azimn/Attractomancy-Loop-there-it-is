import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analysis", ROOT / "analysis.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)

def full_run(model="a",condition="A",run="0",base="1",post="4"):
    output=[]
    for q in sorted(analysis.REQUIRED_IDS):
        phase=analysis.EXPECTED_PHASES[q]
        val=post if q=="Q11" else base
        output.append(dict(model=model,condition=condition,run_id=run,question_id=q,phase=phase,
            response="synthetic unit test",factual_recall=val,characteristic_judgment=val,
            relationship_continuity=val,identity_consistency="",spontaneous_expression="",resistance=""))
    return output

class TestAnalysis(unittest.TestCase):
    def test_null_not_invented(self):
        with self.assertRaises(ValueError):
            analysis.summarize([])
    def test_cliffs(self):
        self.assertEqual(analysis.cliffs([2,3],[0,1]),1.0)
        self.assertEqual(analysis.cliffs([0,1],[2,3]),-1.0)
    def test_cluster_complete(self):
        rows=[]
        for m in ("a","b"):
            for c in "ABCD":
                for i in range(5):
                    rows+=full_run(m,c,str(i),str("ABCD".index(c)),post="4")
        result=analysis.summarize(rows)
        self.assertEqual(len(result["models"]),2)
        self.assertEqual(result["valid_complete_runs"],40)
        self.assertEqual(len(result["models"]["a"]["comparisons"]),4)
    def test_partial_run_never_counted(self):
        rows=full_run()[:-1]
        out=analysis.summarize(rows)
        self.assertEqual(out["valid_complete_runs"],0)
        self.assertEqual(out["models"],{})
        self.assertEqual(len(out["invalid_or_incomplete_runs"]),1)
    def test_duplicate_prompt_never_counted(self):
        rows=full_run()
        rows.append(rows[0])
        self.assertEqual(analysis.summarize(rows)["valid_complete_runs"],0)
    def test_recovery_not_attributed(self):
        rows=[dict(model="a",condition="D",run_id="1",question_id="Q12",
            phase="cue_only_new_session",response="x",factual_recall="4",
            identity_consistency="4",characteristic_judgment="",relationship_continuity="",
            spontaneous_expression="",resistance="")]
        self.assertEqual(analysis.run_mean(rows),{})
if __name__=="__main__": unittest.main()
