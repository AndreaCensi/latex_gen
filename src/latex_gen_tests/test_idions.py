from .utils import LatexTestUtils, doc_idiom


# class TestIdioms(LatexTestUtils):
@doc_idiom
def testEmpty(doc):  # @NoSelf
    pass


@doc_idiom
def testEmptyFigure(doc):  # @NoSelf
    with doc.figure(caption="") as fig:  # @UnusedVariable
        pass


@doc_idiom
def testSubFigure(doc):  # @NoSelf
    with doc.figure(caption="") as fig:
        with fig.subfigure(caption="fig1") as sub:
            sub.text("ciao")
        with fig.subfigure(caption="fig2") as sub:
            sub.text("hello")
