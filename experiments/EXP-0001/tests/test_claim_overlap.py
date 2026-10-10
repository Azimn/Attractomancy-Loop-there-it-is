import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("check_claim_overlap",ROOT/"check_claim_overlap.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ClaimOverlapTests(unittest.TestCase):
    def test_overlapping_source_lines_are_flags_not_deletions(self):
        p=lambda identity,s,e: {"id":identity,"d_path":"Apocalypse.txt",
                                 "d_line_start":s,"d_line_end":e}
        out=m.examine([p("E-1",1,2),p("E-2",2,3)])
        self.assertEqual(out["exactly_same_citation_groups"],[])
        self.assertEqual(out["overlapping_source_lines"][0]["line"],2)
        self.assertEqual(out["auto_removed"],0)
    def test_exact_duplicate_citation_requires_review(self):
        p=lambda x:{"id":x,"d_path":"Apocalypse.txt","d_line_start":2,"d_line_end":4}
        out=m.examine([p("E-1"),p("E-2")])
        self.assertEqual(len(out["exactly_same_citation_groups"]),1)
    def test_non_overlap(self):
        a={"id":"A","d_path":"Apocalypse.txt","d_line_start":1,"d_line_end":1}
        b=dict(a,id="B",d_line_start=2,d_line_end=2)
        self.assertFalse(m.examine([a,b])["needs_semantic_duplicate_review"])
if __name__=="__main__":unittest.main()
