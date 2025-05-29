import unittest
import sfc

class Tests(unittest.TestCase):
    def test_buildCommandDict_blank(self):
        passed = ""
        expected = {"cmd": "", "opts": [], "args": []}
        self.assertEqual(sfc.buildCommandDict(passed), expected)

    def test_buildCommandDict_only_command(self):
        passed = "planets"
        expected = {"cmd": "planets", "opts": [], "args": []}
        self.assertEqual(sfc.buildCommandDict(passed), expected)

    # def test_buildCommandDict_one_short_option_no_args(self):
    #     passed = "fleet -h"
    #     expected = {"cmd": "fleet", "opts": [{"opt": "h", "args": []}]}
    #     self.assertEqual(sfc.buildCommandDict(passed), expected)

    # def test_buildCommandDict_one_long_option_no_args(self):
    #     passed = "fleet --help"
    #     expected = {"cmd": "fleet", "opts": [{"opt": "help", "args": []}]}
    #     self.assertEqual(sfc.buildCommandDict(passed), expected)

if __name__ == "__main__":
    unittest.main()