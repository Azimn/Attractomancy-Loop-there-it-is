import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("open_review_worklist",ROOT/"open_review_worklist.py")
work=importlib.util.module_from_spec(spec)
spec.loader.exec_module(work)

class ReviewWorklistTests(unittest.TestCase):
    def sample(self):
        lines=[{"line":str(i),"classification":"prose_candidate" if i in (5,6,22) else
                "symbolic_candidate" if i in (3,4,15,16,17) else "unresolved_fragment"}
                for i in range(1,31)]
        queued=[{"line":i,"id":"X"+str(i)} for i in (5,6,22)]
        decisions=[{"start_line":"1","end_line":"2","decision":"proposition"},
                   {"start_line":"29","end_line":"29","decision":"unresolved"}]
        props=[{"d_line_start":5,"d_line_end":5}]
        return lines,queued,decisions,props
    def test_prioritize_unresolved_before_lexical_coverage(self):
        result=work.rank(*self.sample(),width=10,limit=5)
        self.assertEqual(result["batches"][0]["start_line"],21)
        self.assertEqual(result["batches_total"],3)
        self.assertEqual(result["unadjudicated_source_lines"],27)
        self.assertEqual(result["explicitly_unresolved_lines"],1)
    def test_completed_source_has_no_batches(self):
        lines=[{"line":str(i),"classification":"blank"} for i in range(1,11)]
        decisions=[{"start_line":"1","end_line":"10","decision":"paratext"}]
        r=work.rank(lines,[],decisions,[],width=10)
        self.assertEqual(r["batches_total"],0)
    def test_open_queued_line_with_existing_draft_not_misrepresented(self):
        rows,queue,decisions,propositions=self.sample()
        result=work.rank(rows,queue,decisions,propositions,width=10)
        band=next(b for b in result["batches"] if b["start_line"]==1)
        self.assertEqual(band["unadjudicated_queued_starts_without_draft"],1)
    def test_overlap_rejected(self):
        lines,queued,decisions,props=self.sample()
        decisions.append({"start_line":"2","end_line":"3","decision":"paratext"})
        with self.assertRaises(ValueError):
            work.rank(lines,queued,decisions,props)
if __name__=="__main__":unittest.main()
