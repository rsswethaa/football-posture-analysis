import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.storage import add_frame_result, create_session, init_db


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'posture.db'
        init_db(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_persist_analysis_result(self):
        session = create_session(self.db, 'demo.mp4', 'P1')
        frame = add_frame_result(self.db, session, 1, 40,
            {'left_knee_angle': 110, 'right_knee_angle': 115, 'hip_angle': 150, 'torso_lean': 8, 'confidence': 0.91},
            'athletic_stance', 0.84)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM frames').fetchone()[0], 1)
            self.assertEqual(db.execute('SELECT label FROM posture_predictions WHERE frame_id=?', (frame,)).fetchone()[0], 'athletic_stance')


if __name__ == '__main__':
    unittest.main()
