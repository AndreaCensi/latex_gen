from .utils import latex_escape
from contextlib import contextmanager
import mimetypes
import os


class LatexEnvironment:

    def __init__(self, context):
        self.context = context

    # todo: add verbatim
    def color(self, r, g, b):
        self.context.f.write('\\color[rgb]{%s,%s,%s}' % (r, g, b))

    def hfill(self):
        self.context.f.write('\\hfill\ \n')

    def hspace(self, size):
        self.context.f.write('\\hspace{%s}' % size)

    def vspace(self, size):
        self.context.f.write('\\vspace{%s}' % size)

    def parbreak(self):
        self.context.f.write('\n\n')

    def pagebreak(self):
        self.context.f.write('\\pagebreak\ \n')

    def rule(self, width, height, color='gray'):
        self.context.f.write('{\\color{%s}\\rule{%s}{%s}}\n' % \
                             (color, width, height))

    def text(self, t):
        ''' 
            Writes the text on the stream (it will be escaped, use 
            :py:func:`tex` for raw TeX. 
        '''
        self.context.f.write(latex_escape(t))

    # OLD function
    def tabular_simple(self, data, row_desc, col_desc, write_col_desc=True):
        ''' Writes a tabular environment with very simple options. '''
        def hline():
            self.context.f.write('\\hline\n')

        def write_row_tex(entries):
            self.context.f.write(" & ".join(entries))
            self.context.f.write(' \\tabularnewline\n')

        alignment_string = '|l||' + ('r|' * len(col_desc))
        self.context.f.write('\\begin{tabular}{%s}\n' % alignment_string)
        hline()
        if write_col_desc:
            row_tex = [''] + ['\\makebox[1cm]{%s}' % x for x in col_desc]
            write_row_tex(row_tex)
            hline()
            hline()

        for i, row in enumerate(row_desc):
            row_tex = (['\\makebox[5cm][r]{%s}' % row] +
                        ['\\makebox[1cm]{%s}' % x for x in data[i]])
            write_row_tex(row_tex)
            hline()

        self.context.f.write('\\end{tabular}\n')

    def tex(self, tex):
        ''' Writes raw TeX string. '''
        self.context.f.write(tex)

    def input(self, filename): #@ReservedAssignment
        self.context.f.write('\\input{%s}\n' % filename)

    def use_package(self, name, options={}):
        self.context.use_package(name, options)

    @contextmanager
    def figure(self, caption=None, label=None, placement="t", double=False):
        from .figure import Figure
        figure = Figure(caption=caption, label=label, placement=placement,
                        context=self.context.child(), double=double)
        yield figure
        figure.dump(main_context=self.context)

    @contextmanager
    def tabular(self, alignment, env='tabular'):
        from .tabular import Tabular
        tabular = Tabular(alignment, context=self.context.child(), env=env)
        yield tabular
        tabular.dump(main_context=self.context)

    def longtable(self, alignment):
        # XXX: add yield
        return self.tabular(alignment, env='longtable')

    def graphics_data(self, data, mime, width="3cm", gid=None):
        # TODO: allow free width
        # TODO: require graphicx
        suffix = mimetypes.guess_extension(mime)
        if gid is None:
            gid = self.context.generate_file_id()
        # cannot have '.' in the filename, otherwise latex gets confused
        gid = id.replace('.', '_')
        gid = id.replace('/', ':')

        filename = os.path.join(self.context.graphics_path, gid + suffix)
        # make sure dir exists
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as f:
            f.write(data)
        self.context.f.write('\\includegraphics[width=%s]{%s}%%\n' %
                              (width, gid))

    @contextmanager
    def minipage(self, width, align=''):
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\begin{minipage}[%s]{%s}\n' % (align, width))
        self.context.f.write(env.context.f.getvalue())
        self.context.f.write('\\end{minipage}%\n')

    @contextmanager
    def fbox(self):
        # TODO: add params
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\fbox{%\n')
        self.context.f.write(env.context.f.getvalue())
        self.context.f.write('}%\n')

    #@contextmanager
    #def tightbox(self):
        # TODO: add params

    def lstlisting(self, code, language=None):
#        \begin{lstlisting}
#        put your code here
#        \end{lstlisting}
        params = ""
        if language is not None:
            params += 'language=%s' % language

        self.use_package('listings')
        self.context.f.write('\\begin{lstlisting}[%s]%%\n' % params)
        self.context.f.write(code)
        self.context.f.write('\\end{lstlisting}%\n')
