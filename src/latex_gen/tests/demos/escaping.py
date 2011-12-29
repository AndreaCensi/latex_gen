from . import latex_gen_demo


@latex_gen_demo
def demo_escaping(doc):
    examples = [
        '$', '\\', '\\$[\\]'
    ]

    with doc.tabular(['c', 'c']) as table:

        for example in examples:

            with table.row() as row:

                with row.cell() as c:
                    c.text('a')

                with row.cell() as c:
                    c.text(example)

