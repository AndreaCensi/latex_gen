from .. import latex_document
from contextlib import contextmanager
import os
import shutil
import subprocess
import tempfile
import unittest


def doc_idiom(f):
    def test_wrap(self):
        with self.check_doc_idiom() as doc:
            f(doc)
    test_wrap.__doc__ = f.__doc__
    return test_wrap


def doc_idiom_failure(f):
    f = doc_idiom(f)

    def test_wrap(self):
        self.assertRaises(Exception, f)
    test_wrap.__doc__ = f.__doc__
    return test_wrap


class LatexTestUtils(unittest.TestCase):

    @contextmanager
    def check_doc_idiom(self):
        with self.get_random_file() as filename:
            with latex_document(filename) as doc:
                yield doc
            self.assert_compilable_file(filename)

    def assert_compilable_fragment(self, tex):
        ''' Asserts that the string *tex* is a compilable latex fragment.'''
        with self.get_random_file() as filename:
            with latex_document(filename) as doc: #@UnusedVariable
                doc.tex(tex)
            self.assert_compilable_file(filename)

    def assert_compilable_file(self, filename):
        ''' Asserts that a given file contains a compilable latex document. '''
        basename = os.path.basename(filename)
        cwd = os.path.dirname(filename)
        command = ["pdflatex", "--interaction", "batchmode", basename]
        val = subprocess.call(command, cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if val != 0:
            d = self.get_error_file()
            shutil.copy(filename, d)
            raise Exception('Could not compile file %r. Dumped on %s.' %
                            (filename, d))

        # TODO: include error from stderr

    def get_error_file(self):
        pattern = 'error_doc_%03d.tex'
        for i in range(1000):
            candidate = pattern % i
            if not os.path.exists(candidate):
                return candidate
        assert False

    def setUp(self):
        self.test_directory = tempfile.mkdtemp(prefix='tmp-reprep-tests')

    def tearDown(self):
        # # TODO: cleanup, remove dir
        print(('Deleting %r..' % (self.test_directory)))
        pass

    @contextmanager
    def get_random_file(self):
        _, filename = tempfile.mkstemp(suffix='tex', dir=self.test_directory)
        yield filename
        # TODO: cleanup
