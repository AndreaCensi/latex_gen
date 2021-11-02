from contextlib import contextmanager

from . import LatexEnvironment


class Tabular(LatexEnvironment):
    allowed = ["c", "r", "l", "p"]
    envs = ["tabular", "longtable"]

    def __init__(self, alignment, context, env="tabular"):
        assert isinstance(alignment, list)

        for x in alignment:
            if "{" in x:
                x = x[: x.index("{")]
            assert x in Tabular.allowed, alignment
        assert env in Tabular.envs
        self.env = env
        self.ncols = len(alignment)
        self.alignment = alignment
        self.context = context

    def hline(self):
        self.context.f.write("\\hline\n")

    def endhead(self):
        self.context.f.write("\\endhead\n")

    class Row:
        def __init__(self, ncols, context):
            self.ncols = ncols
            self.col = 0
            self.cols = []
            self.context = context

        def cell_tex(self, tex=""):
            if self.col == self.ncols:
                raise Exception("Too many columns")
            self.cols.append(tex)
            self.col += 1

        @contextmanager
        def cell(self):
            if self.col == self.ncols:
                raise Exception("Too many columns")
            cell = LatexEnvironment(self.context.child())
            yield cell
            self.context.preamble.write(cell.context.preamble.getvalue())
            self.cols.append(cell.context.f.getvalue())
            self.col += 1

        def multicolumn_tex(self, n, align, tex):
            if self.col + n > self.ncols:
                raise Exception("Too many columns (ncols=%d,n=%d,cur=%d)" % (self.ncols, n, self.col))
            c = "\\multicolumn{%s}{%s}{%s}" % (n, align, tex)
            self.cols.append(c)
            self.col += n

    @contextmanager
    def row(self):
        row = Tabular.Row(self.ncols, self.context)
        yield row
        if len(row.cols) > self.ncols:
            raise Exception("Bad number of columns (found %s, required %s)" % (row.col + 1, self.ncols))
        tex = " & ".join(row.cols)
        self.context.f.write(tex)
        self.context.f.write("\\\\ \n ")

    def row_tex(self, *cols):
        if len(cols) > self.ncols:
            raise Exception("Got %d cols instead of %d expected." % (len(cols), self.ncols))
        tex = " & ".join(list(cols))
        self.context.f.write(tex)
        self.context.f.write("\\\\ \n ")

    def dump(self, main_context):
        main_context.preamble.write(self.context.preamble.getvalue())
        alignment = "".join(self.alignment)
        main_context.f.write("\\begin{%s}{%s}\n" % (self.env, alignment))
        main_context.f.write(self.context.f.getvalue())
        main_context.f.write("\\end{%s}\n" % self.env)
