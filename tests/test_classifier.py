import os
import unittest
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.classifier import classify_file, load_rules

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.rules = load_rules()

    def test_classify_ramadhan(self):
        # Tes deteksi Ramadhan musiman
        dtype, risk, status, folder, notes = classify_file(
            "E:\\SUARA BUMI LASINRANG 2025\\RAMADHAN\\Tips Sahur SBL.mp3", 
            "Tips Sahur SBL.mp3", 
            self.rules
        )
        self.assertEqual(dtype, "ramadhan_only")
        self.assertEqual(risk, "CRITICAL")
        self.assertEqual(status, "SEASONAL_RAMADHAN_ARCHIVE")

    def test_classify_adzan(self):
        # Tes deteksi adzan
        dtype, risk, status, folder, notes = classify_file(
            "E:\\SUARA BUMI LASINRANG\\Adzan Maghrib.mp3", 
            "Adzan Maghrib.mp3", 
            self.rules
        )
        self.assertEqual(dtype, "adzan")
        self.assertEqual(risk, "HIGH")
        self.assertEqual(status, "ADZAN_REVIEW")

    def test_classify_ilm(self):
        # Tes deteksi ILM
        dtype, risk, status, folder, notes = classify_file(
            "E:\\SUARA BUMI LASINRANG\\Stop Judi Online.mp3", 
            "Stop Judi Online.mp3", 
            self.rules
        )
        self.assertEqual(dtype, "ilm_spot")
        self.assertEqual(status, "APPROVED")
        self.assertEqual(folder, "03_ILM")

    def test_classify_dirty_metadata(self):
        # Tes deteksi kotor
        dtype, risk, status, folder, notes = classify_file(
            "E:\\agus lagu baru\\Kangen Band - Bintang di Surga - PlanetLagu.com.mp3", 
            "Kangen Band - Bintang di Surga - PlanetLagu.com.mp3", 
            self.rules
        )
        self.assertTrue("DIRTY_METADATA" in notes)
        self.assertEqual(status, "REVIEW")

if __name__ == "__main__":
    unittest.main()
