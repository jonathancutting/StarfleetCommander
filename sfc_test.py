import unittest
from sfc import buildCommandDict

class Tests(unittest.TestCase):
    def test_buildCommandDict_blank(self):
        passed = ""
        expected = {"cmd": "", "args": []}
        self.assertEqual(buildCommandDict(passed), expected)

    def test_buildCommandDict_only_command(self):
        passed = "planets"
        expected = {"cmd": "planets", "args": []}
        self.assertEqual(buildCommandDict(passed), expected)

    def test_buildCommandDict_one_arg(self):
        passed = "fleet -h"
        expected = {"cmd": "fleet", "args": ["-h"]}
        self.assertEqual(buildCommandDict(passed), expected)

    def test_buildCommandDict_multiple_args(self):
        passed = "fleet --return Molos"
        expected = {"cmd": "fleet", "args": ["--return", "Molos"]}
        self.assertEqual(buildCommandDict(passed), expected)

if __name__ == "__main__":
    unittest.main()