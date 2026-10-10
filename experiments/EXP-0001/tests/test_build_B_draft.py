import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("build_B_draft",ROOT/"build_B_draft.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PreviewTests(unittest.TestCase):
    def item(self,n,line):
        return dict(id=n,sentence_fr="Une voix attribue un sens à un signe.",
            d_line_start=line,d_line_end=line,
            d_path="Le_refuge/MUST-READ/Apocalypse.txt",
            contradiction_group="identity_scope",attribution="unattributed",
            review_status="editorial_draft_requires_independent_audit")
    def test_unapproved_register_preserves_provenance_and_order(self):
        a=self.item("E-0002",5)
        b=self.item("E-0001",2)
        text,trace=m.build({"status":"editorial_draft_semantic_audit_open",
                            "propositions":[a,b]})
        self.assertEqual(trace[0]["id"],"E-0001")
        self.assertEqual(trace[0]["source_lines"],[2,2])
        self.assertEqual(len(text.splitlines()),2)
        self.assertIn("identity_scope",[x["contradiction_group"] for x in trace])
    def test_duplicate_rejected(self):
        x=self.item("E-0001",2)
        with self.assertRaises(ValueError):
            m.build({"status":"editorial_draft_semantic_audit_open","propositions":[x,x]})
    def test_status_cannot_be_misrepresented(self):
        x=self.item("E-0001",2)
        x["review_status"]="approved"
        with self.assertRaises(ValueError):
            m.build({"status":"editorial_draft_semantic_audit_open","propositions":[x]})
if __name__=="__main__":unittest.main()
