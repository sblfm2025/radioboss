import os
import unittest
import sys

# Tambahkan direktori root aplikasi ke system path agar modul dapat diimpor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.playlist_parser import parse_playlist

class TestPlaylistParser(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.m3u_path = os.path.join(self.test_dir, "test_playlist.m3u")
        
        # Buat playlist M3U dummy untuk pengujian
        with open(self.m3u_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1,Lagu Keren\n")
            f.write("Lagu_Keren.mp3\n")
            f.write("#EXTINF:-1,Lagu Religi\n")
            f.write("E:\\SUARA BUMI LASINRANG\\Lagu_Religi.mp3\n")

    def tearDown(self):
        # Bersihkan file dummy setelah tes
        if os.path.exists(self.m3u_path):
            os.remove(self.m3u_path)

    def test_parse_m3u(self):
        items = parse_playlist(self.m3u_path)
        self.assertEqual(len(items), 2)
        
        # Cek relative path resolution
        self.assertEqual(os.path.basename(items[0]["resolved_path"]), "Lagu_Keren.mp3")
        # Cek absolute path
        self.assertEqual(items[1]["resolved_path"], "E:\\SUARA BUMI LASINRANG\\Lagu_Religi.mp3")

if __name__ == "__main__":
    unittest.main()
