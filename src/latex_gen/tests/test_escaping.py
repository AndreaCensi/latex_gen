from latex_gen.tests.utils import LatexTestUtils


class TestEscaping(LatexTestUtils):
    examples = ["", "$", "\\", "\\$[\\]"]

    def test_escaping(self):
        """ Check that we escape strings correctly. """
        for s in TestEscaping.examples:
            yield self.assert_compilable_fragment, s

    def test_compiling_works(self):
        """ Check that it throws an exception for invalid latex. """
        self.assertRaises(Exception, self.assert_compilable_fragment, "\\ciao")
