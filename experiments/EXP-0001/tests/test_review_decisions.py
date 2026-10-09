import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("audit_review_decisions",ROOT/"audit_review_decisions.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def row(start,end,decision,ids="",reason="valid explanation"):
    return {"start_line":str(start),"end_line":str(end),"decision":decision,
            "proposition_ids":ids,"voice":"unattributed","reason":reason,
            "reviewer":"test-reviewer","review_date":"2026-10-08"}

class ReviewTests(unittest.TestCase):
    def test_incomplete_stays_unapproved(self):
        report=audit.inspect([row(1,1,"paratext")],3,{"E-0001"})
        self.assertFalse(report["eligible_for_review_signoff"])
        self.assertEqual(report["unadjudicated_source_lines"],2)
    def test_complete_with_claim(self):
        report=audit.inspect([row(1,1,"paratext"),row(2,2,"proposition","E-0001"),
                              row(3,3,"nonextractable_symbolic",reason="standalone phonetic fragment")],
                             3,{"E-0001"},True)
        self.assertTrue(report["eligible_for_review_signoff"])
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,2,"paratext"),row(2,3,"paratext")],3,{"E-0001"})
    def test_no_automatic_symbol_rejection(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"nonextractable_symbolic",reason="")],1,{"E-0001"})
    def test_unresolved_blocks_strict(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"unresolved")],1,{"E-0001"},True)
if __name__=="__main__": unittest.main()
