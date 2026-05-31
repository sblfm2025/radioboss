import os
import unittest
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.path_security import is_safe_path, safe_join

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.allowed_root = "D:\\RADIO_SBL_FRESH"

    def test_safe_path(self):
        # Jalur normal di dalam root allowed harus lolos
        safe_path = "D:\\RADIO_SBL_FRESH\\01_MUSIC_ACTIVE\\Lagu.mp3"
        self.assertTrue(is_safe_path(safe_path, self.allowed_root))

    def test_path_traversal_detection(self):
        # Jalur traversal ke luar root harus terdeteksi tidak aman
        unsafe_path = "D:\\RADIO_SBL_FRESH\\..\\..\\Windows\\System32\\cmd.exe"
        self.assertFalse(is_safe_path(unsafe_path, self.allowed_root))

    def test_safe_join(self):
        # Penggabungan aman harus menghasilkan path absolut
        result = safe_join(self.allowed_root, "01_MUSIC_ACTIVE", "Lagu.mp3")
        self.assertTrue(os.path.isabs(result))
        
        # Penggabungan traversal harus memicu PermissionError
        with self.assertRaises(PermissionError):
            safe_join(self.allowed_root, "..", "..", "Windows")

if __name__ == "__main__":
    unittest.main()
