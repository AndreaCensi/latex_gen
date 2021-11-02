from zuper_commons.test_utils import known_failure
from .utils import LatexTestUtils


class TestEscaping(LatexTestUtils):
    # examples = ["", "$", "\\", "\\$[\\]"]
    #

    def test_escaping1(self):
        self.assert_compilable_fragment("")

    @known_failure
    def test_escaping2(self):
        self.assert_compilable_fragment("$")

    @known_failure
    def test_escaping3(self):
        self.assert_compilable_fragment("\\")

    @known_failure
    def test_escaping4(self):
        self.assert_compilable_fragment("\\$[\\]")

    def test_compiling_works(self):
        """Check that it throws an exception for invalid latex."""
        self.assertRaises(Exception, self.assert_compilable_fragment, "\\ciao")
