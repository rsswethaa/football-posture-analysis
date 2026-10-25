import tempfile
import unittest
from pathlib import Path

import app as football_app
from src.biomechanics import extract_biomechanics
from src.pipeline import analyse_keypoint_sequence
from src.reporting import summarise_analysis


def pose(dx=0.0):
    return {
        'left_shoulder':(.44+dx,.20),'right_shoulder':(.56+dx,.20),
        'left_hip':(.46+dx,.45),'right_hip':(.54+dx,.45),
        'left_knee':(.45+dx,.65),'right_knee':(.55+dx,.65),
        'left_ankle':(.43+dx,.90),'right_ankle':(.57+dx,.90),
    }


class FootballProductTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        football_app.app.config.update(TESTING=True,DATABASE=str(Path(self.tmp.name)/'football.db'))
        self.client=football_app.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_extended_biomechanics(self):
        result=extract_biomechanics(pose(),.9)
        self.assertIn('stride',result)
        self.assertIn('balance',result)
        self.assertGreaterEqual(result['balance'],0)
        self.assertLessEqual(result['balance'],1)

    def test_temporal_sequence_detects_motion(self):
        frames=[{'points':pose(i*.02),'frame_number':i} for i in range(5)]
        results=analyse_keypoint_sequence(frames,fps=30)
        self.assertEqual(len(results),5)
        self.assertIn(results[-1]['movement'],{'RUNNING','SPRINTING','CONTROLLED','DEFENDING'})
        self.assertGreater(results[-1]['horizontal_speed'],0)

    def test_summary(self):
        frames=[{'points':pose(i*.02)} for i in range(4)]
        summary=summarise_analysis(analyse_keypoint_sequence(frames,30))
        self.assertEqual(summary['frames_analysed'],4)
        self.assertIn('average' if False else 'averages',summary)

    def test_keypoint_api_persists_session(self):
        frames=[{'points':pose(i*.018),'frame_number':i,'timestamp_ms':i*100} for i in range(6)]
        response=self.client.post('/api/analyse-keypoints',json={'source_name':'test-drill','player_ref':'p1','fps':30,'frames':frames})
        self.assertEqual(response.status_code,200)
        payload=response.get_json()
        self.assertEqual(payload['summary']['frames_analysed'],6)
        self.assertEqual(len(payload['history']),1)
        self.assertTrue(payload['report_url'].endswith('.md'))

    def test_video_route_requires_file(self):
        self.assertEqual(self.client.post('/api/analyse-video').status_code,400)


if __name__=='__main__':
    unittest.main()
