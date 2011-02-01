import unittest 
from latex_gen import Latex

from .utils import LatexTestUtils
from latex_gen.tests.utils import doc_idiom


class TestIdioms(LatexTestUtils): 

    @doc_idiom
    def testEmpty(doc):
        pass

    @doc_idiom
    def testEmptyFigure(doc):
        with doc.figure(caption="") as fig: #@UnusedVariable
            pass

    @doc_idiom
    def testSubFigure(doc):
        with doc.figure(caption="") as fig:
            with fig.subfigure(caption="fig1") as sub:
                sub.text('ciao')
            with fig.subfigure(caption="fig2") as sub:
                sub.text('hello')
                    
#    def testGraphics(self):
#        with tempfile.NamedTemporaryFile(suffix='tex') as tmp:
#            filename = tmp.name
#            with Latex.document(filename) as doc:
#                with doc.figure(caption="") as fig:
#                    with fig.subfigure(caption="fig1") as sub:
#                        sub.text('ciao')
#                    with fig.subfigure(caption="fig2") as sub:
#                        sub.text('hello')
#                    
#            self.try_compile(tmp)


        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
