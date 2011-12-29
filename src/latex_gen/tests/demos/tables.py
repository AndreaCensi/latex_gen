from . import latex_gen_demo, latex_gen_demo_failure


@latex_gen_demo
def test_table1(doc): #@NoSelf
    ''' Completely yield-oriented '''
    with doc.tabular(['c', 'c']) as tabular:
        with tabular.row() as row:
            with row.cell() as c:  c.tex('a')
            with row.cell() as c:  c.tex('b')
        tabular.hline()
        with tabular.row() as row:
            with row.cell() as c:  c.tex('a')
            with row.cell() as c:  c.tex('b')

@latex_gen_demo
def test_table2(doc): #@NoSelf
    ''' with for rows, cell_tex '''
    with doc.tabular(['c', 'c']) as tabular:
        with tabular.row() as row:
            row.cell_tex('a')
            row.cell_tex('b')
        tabular.hline()
        with tabular.row() as row:
            row.cell_tex('a')
            row.cell_tex('b')

@latex_gen_demo
def test_table_multi(doc): #@NoSelf 
    with doc.tabular(['c', 'c', 'c']) as tabular:
        with tabular.row() as row:
            row.cell_tex('b')
            row.multicolumn_tex(2, 'c', 'a')
        with tabular.row() as row:
            row.multicolumn_tex(2, 'c', 'a')
            row.cell_tex('b')

@latex_gen_demo_failure
def test_table_multi_bad1(doc): #@NoSelf 
    with doc.tabular(['c', 'c', 'c']) as tabular:
        with tabular.row() as row:
            row.cell_tex('b')
            row.multicolumn_tex(3, 'c', 'a')

@latex_gen_demo_failure
def test_table_multi_bad2(doc): #@NoSelf 
    with doc.tabular(['c', 'c', 'c']) as tabular:
        with tabular.row() as row:
            row.cell_tex('b')
            row.multicolumn_tex(1, 'c', 'a')

@latex_gen_demo_failure
def test_table_multi_bad3(doc): #@NoSelf 
    with doc.tabular(['c', 'c', 'c']) as tabular:
        with tabular.row() as row:
            row.multicolumn_tex(3, 'c', 'a')
            row.cell_tex('b')


@latex_gen_demo
def test_table3(doc): #@NoSelf
    ''' with for rows, cell_tex '''
    with doc.tabular(['c', 'c']) as tabular:
        tabular.row_tex('a', 'b')
        tabular.row_tex('a', 'b')

@latex_gen_demo_failure
def test_table_bad_args(doc): #@NoSelf
    ''' Wrong args '''
    with doc.tabular(['c', 'd']) as tabular: #@UnusedVariable
        pass

@latex_gen_demo_failure
def test_table_bad_num1(doc): #@NoSelf
    ''' with for rows, cell_tex '''
    with doc.tabular(['c', 'c']) as tabular:
        tabular.row_tex('a', 'b')
        tabular.row_tex('a')

@latex_gen_demo_failure
def test_table_bad_num2(doc): #@NoSelf
    with doc.tabular(['c', 'c']) as tabular:
        tabular.row_tex('a', 'b')
        tabular.row_tex('a', 'b', 'c')
