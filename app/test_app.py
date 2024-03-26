import unittest
import patterns

from app import check_patterns_in_file

class TestCheckPatternsInFile(unittest.TestCase):
    def test_matching_patterns(self):
        # path to logs/Goole_Pixel_5.txt
        file_path = './logs/Google_Pixel_5.txt'
        patterns_list = patterns.patterns_set
        expected_result =  {patterns.pattern_1, patterns.pattern_2}
        self.assertEqual(check_patterns_in_file(file_path, patterns_list), expected_result)

    def test_no_matching_patterns(self):
        # path to logs/OnePlus_8.txt
        file_path = './logs/Samsung_Galaxy_S10_Plus.txt'
        patterns_list = patterns.patterns_set
        expected_result =  set()
        self.assertEqual(check_patterns_in_file(file_path, patterns_list), expected_result)

if __name__ == '__main__':
    unittest.main()