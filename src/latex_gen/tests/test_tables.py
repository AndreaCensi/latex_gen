from .utils import LatexTestUtils, doc_idiom
from latex_gen.tests.utils import doc_idiom_failure


class TestTables(LatexTestUtils):

    @doc_idiom
    def test_table1(doc):
        ''' Completely yield-oriented '''
        with doc.tabular(['c', 'c']) as tabular:
            with tabular.row() as row:                        
                with row.cell() as c:  c.tex('a')
                with row.cell() as c:  c.tex('b')                
            tabular.hline()
            with tabular.row() as row:                        
                with row.cell() as c:  c.tex('a')
                with row.cell() as c:  c.tex('b')

    @doc_idiom
    def test_table2(doc):
        ''' with for rows, cell_tex '''
        with doc.tabular(['c', 'c']) as tabular:
            with tabular.row() as row:                        
                row.cell_tex('a')
                row.cell_tex('b')                
            tabular.hline()
            with tabular.row() as row:                        
                row.cell_tex('a')
                row.cell_tex('b')                

    @doc_idiom
    def test_table3(doc):
        ''' with for rows, cell_tex '''
        with doc.tabular(['c', 'c']) as tabular:
            tabular.row_tex('a', 'b')
            tabular.row_tex('a', 'b')

    @doc_idiom_failure
    def test_table_bad_args(doc):
        ''' Wrong args '''
        with doc.tabular(['c', 'd']) as tabular:
            pass

    @doc_idiom
    def test_table_bad_num(doc):
        ''' with for rows, cell_tex '''
        with doc.tabular(['c', 'c']) as tabular:
            tabular.row_tex('a', 'b')
            tabular.row_tex('a')

    @doc_idiom
    def test_table_bad_num(doc):
        with doc.tabular(['c', 'c']) as tabular:
            tabular.row_tex('a', 'b')
            tabular.row_tex('a', 'b', 'c')

