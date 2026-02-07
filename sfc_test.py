import unittest
from sfc import buildCommandDict
from sfc import loadConfig
from planet import parseLocation

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

    def test_loadConfig(self):
        expected = {"plogger": {"output": "file", "filePath": "sfc.log", "level": "DEBUG"}}
        self.assertEqual(loadConfig(), expected)
    
    def test_parseLocation(self):
        passed = "8:41:3m"
        expected = {"galaxy": 8, "system": 41, "slot": 3, "moon": True}
        self.assertEqual(parseLocation(passed), expected)

if __name__ == "__main__":
    unittest.main()