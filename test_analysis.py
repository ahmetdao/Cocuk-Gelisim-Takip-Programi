import unittest
from analysis_service import AnalysisService

class TestAnalysisService(unittest.TestCase):
    def test_format_yas(self):
        self.assertEqual(AnalysisService.format_yas(5, 3.2), "5 Yıl 3 Ay")

    def test_calculate_lms(self):
        # Example values (can be cross checked with WHO data if needed, but checking math consistency here)
        # L=1, M=100, S=0.1, Val=100 -> Z=0
        z, p = AnalysisService.calculate_lms(100, 1, 100, 0.1)
        self.assertAlmostEqual(z, 0)
        self.assertAlmostEqual(p, 50)

    def test_perform_analysis_valid(self):
        # Random valid input
        # Boy: 100cm, Kilo: 15kg, 3 Years old roughly
        res = AnalysisService.perform_analysis(
            gun=1, ay=1, yil=2020, 
            k_gun=1, k_ay=1, k_yil=2023, 
            boy=100, kilo=15, cinsiyet='erkek'
        )
        self.assertNotIn("error", res)
        self.assertIn("boy", res)
        self.assertIn("kilo", res)
        self.assertIn("bmi", res)
        self.assertEqual(res["yas_str"], "3 Yıl 0 Ay")

    def test_perform_analysis_invalid_date(self):
        res = AnalysisService.perform_analysis(
            gun=1, ay=1, yil=2023, 
            k_gun=1, k_ay=1, k_yil=2020, # Kontrol before birth
            boy=100, kilo=15, cinsiyet='erkek'
        )
        self.assertIn("error", res)

if __name__ == '__main__':
    unittest.main()
