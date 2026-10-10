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
    def test_wrong_claim_line_blocked(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(5,5,"proposition","E-0001")],5,{"E-0001"},proposition_spans={"E-0001":(1,1)})
    def test_duplicate_from_other_source_line_accepted(self):
        result=audit.inspect([row(1,1,"proposition","E-0001"),
                              row(2,2,"duplicate_proposition","E-0001",reason="Repeated symbolic alphabet meaning")],
                             2,{"E-0001"},True,proposition_spans={"E-0001":(1,1)})
        self.assertTrue(result["eligible_for_review_signoff"])
    def test_duplicate_claim_on_original_line_blocked(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"duplicate_proposition","E-0001",reason="Same letter mapping")],
                          1,{"E-0001"},proposition_spans={"E-0001":(1,1)})
    def test_nonclaim_with_claim_id_blocked(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"paratext","E-0001")],1,{"E-0001"})
    def test_full_line_review_without_claim_coverage_is_not_approval(self):
        result=audit.inspect([row(1,1,"paratext"),row(2,2,"no_proposition")],
                             2,{"E-0001"},proposition_spans={"E-0001":(1,1)})
        self.assertEqual(result["claim_ids_without_direct_decision_count"],1)
        self.assertFalse(result["eligible_for_review_signoff"])
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"paratext"),row(2,2,"no_proposition")],
                          2,{"E-0001"},True,proposition_spans={"E-0001":(1,1)})
    def test_repeated_mapping_does_not_substitute_for_direct_provenance(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"no_proposition"),
                           row(2,2,"duplicate_proposition","E-0001",reason="Same mapping in another section")],
                          2,{"E-0001"},True,proposition_spans={"E-0001":(1,1)})
    def test_unresolved_blocks_strict(self):
        with self.assertRaises(ValueError):
            audit.inspect([row(1,1,"unresolved")],1,{"E-0001"},True)
if __name__=="__main__": unittest.main()
