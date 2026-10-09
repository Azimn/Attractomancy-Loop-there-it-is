import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("calibrate_scores",ROOT/"calibrate_scores.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class CalibrationTests(unittest.TestCase):
    def test_agreement(self):
        self.assertEqual(m.weighted_kappa([0,1,2,3,4],[0,1,2,3,4]),1.)
    def test_disagreement(self):
        self.assertLess(m.weighted_kappa([0,1,2,3,4],[4,3,2,1,0]),0.)
    def test_stratified_one_per_arm(self):
        key=[];packet=[]
        for model in ["modela","modelb"]:
            for arm in "ABCD":
                for j in range(5):
                    ident=model+arm+str(j)
                    key.append({"blind_id":ident,"run_id":ident,"model":model,"condition":arm})
                    packet.append({"blind_id":ident,"response":"unlabelled"})
        sample,runs=m.review_subset(key,packet)
        self.assertEqual(runs,8)
        self.assertEqual(len(sample),8)
if __name__=="__main__":unittest.main()
