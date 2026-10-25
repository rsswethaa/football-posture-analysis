import unittest
from src.geometry import angle
from src.posture import extract_features, classify_posture

class PostureTests(unittest.TestCase):
    def test_right_angle(self):
        self.assertAlmostEqual(angle((1,0),(0,0),(0,1)), 90, places=2)

    def test_upright(self):
        f = extract_features({"shoulder":(0,0),"hip":(0,2),"knee":(0,4),"ankle":(0,6)})
        self.assertEqual(classify_posture(f), "UPRIGHT")

    def test_missing_keypoint(self):
        with self.assertRaises(ValueError):
            extract_features({"hip":(0,0)})

if __name__ == "__main__":
    unittest.main()
