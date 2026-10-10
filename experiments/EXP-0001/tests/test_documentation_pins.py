import importlib.util
import pathlib
import unittest

HERE=pathlib.Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(HERE))
spec=importlib.util.spec_from_file_location("audit_documentation_pins",HERE/"audit_documentation_pins.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class SourceDocumentationTests(unittest.TestCase):
    def test_canonical_reference(self):
        self.assertEqual(audit.verify_texts({"README.md":"Pinned "+audit.PIN},audit.PIN),[])
    def test_one_digit_drift_is_detected(self):
        mutated=audit.PIN.replace("930503","930523")
        findings=audit.verify_texts({"README.md":"Pinned "+mutated},audit.PIN)
        self.assertTrue(findings)
    def test_missing_source_commit_is_detected(self):
        self.assertTrue(audit.verify_texts({"README.md":"Source forthcoming"},audit.PIN))
    def test_correct_pin_and_wrong_pin_in_same_document_rejected(self):
        mutated=audit.PIN.replace("930503","930523")
        self.assertTrue(audit.verify_texts({"README.md":audit.PIN+" "+mutated},audit.PIN))
if __name__=="__main__":unittest.main()
