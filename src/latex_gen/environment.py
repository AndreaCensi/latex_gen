from .utils import latex_escape
from contextlib import contextmanager
import mimetypes
import os
from contracts import contract

MIME_PNG = 'image/png'
MIME_JPG = 'image/jpeg'
MIME_PLAIN = 'text/plain'


class LatexEnvironment(object):

    def __init__(self, context):
        self.context = context

    # todo: add verbatim
    def color(self, r, g, b):
        self.context.f.write('\\color[rgb]{%s,%s,%s}' % (r, g, b))

    def hfill(self):
        self.context.f.write('\\hfill\ \n')
    
    def vfill(self):
        self.context.f.write('\\vfill\ \n')

    def hspace(self, size):
        self.context.f.write('\\hspace{%s}' % size)

    def vspace(self, size):
        self.context.f.write('\\vspace{%s}' % size)

    def parbreak(self):
        self.context.f.write('\par%\n')
        # self.context.f.write('\n\n')

    def linebreak(self):
        self.context.f.write('\\\\')

    def pagebreak(self):
        self.context.f.write('\\pagebreak\ \n')

    def rule(self, width, height, color='gray'):
        self.context.f.write('{\\color{%s}\\rule{%s}{%s}}%%\n' % 
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

    def input(self, filename):  # @ReservedAssignment
        self.context.f.write('\\input{%s}\n' % filename)

    def use_package(self, name, options={}):
        self.context.use_package(name, options)

    @contextmanager
    def figure(self, caption=None, label=None, placement="t", double=False):
        self.use_package('caption')
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

    def textattachfile(self, basename, data, text):
    # %\textattachfile{myfile.cc}{extract my source code}
        filename = os.path.join(self.context.graphics_path, basename)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as f:
            f.write(data)
            
        self.context.f.write('\\textattachfile{%s}{%s}%%\n' % 
                              (filename, text))
    
    def save_graphics_data(self, data, mime, gid):
        suffix = mimetypes.guess_extension(mime)
        if mime == MIME_JPG:
            suffix = '.jpg'
        if mime == MIME_PLAIN:
            suffix = '.txt'
        
        filename = os.path.join(self.context.graphics_path,
                                '%s%s' % (gid, suffix))
        # make sure dir exists
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # sys.stderr.write('writing to %r' % filename)
        with open(filename, 'w') as f:
            f.write(data)
            
        return filename

    @contract(params='dict|None')
    def graphics_data(self, data, mime, gid=None, **params):    
        # TODO: allow free width
        # TODO: require graphicx
        if gid is None:
            gid = self.context.generate_file_id()
        # cannot have '.' in the filename, otherwise latex gets confused
        gid = gid.replace('.', '_')
        gid = gid.replace('/', ':')

        self.save_graphics_data(data, mime, gid)
        
        # TODO : add crop
#        if params is None:
#            params = {}
#        if width is not None:
#            params['width'] = width

        ps = make_options_string(**params)
            
        self.context.f.write('\\includegraphics[%s]{%s}%%\n' % 
                              (ps, gid))



    @contextmanager
    def minipage(self, width, align='', fbox=False):
        fix_alignment = False
        if fbox:
            with self.tightbox() as fb:
                # fb.hspace('-1pt')
#                 fb.tex('\\newlength{\\%s}' % x)
#                 fb.tex('\\setlength{\\%s}{%s plus 2pt}' % (x, width))
                with fb.minipage(width, align, fbox=False) as m:
                    yield m
                # fb.hspace('-1pt')
            return
                    
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\begin{minipage}[%s]{%s}%%\n' % (align, width))
        
        if fix_alignment:
            self.context.f.write('\\vspace{0pt}\\par%\n')
        
        self.context.f.write(env.context.f.getvalue())
        
        if fix_alignment:
            self.context.f.write('\\par\\vspace{0pt}%\n')
        
        self.context.f.write('\\end{minipage}%\n')


    @contextmanager
    def minipage_bottom(self, width):
        """ A minipage which will align the bottom with the current
            baseline. 
        """
        with self.minipage(width, 'b') as m:
            m.tex('\\vspace{0pt}\\par%\n')
            yield m
            m.tex('\\par\\vspace{0pt}%\n')

    @contextmanager
    def fbox(self, sep='1pt'):
        # TODO: add params
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('{\\setlength\\fboxsep{%s}%%\n' % sep)
        self.context.f.write('\\fbox{%\n')
        self.context.f.write(env.context.f.getvalue())
        self.context.f.write('}% fbox\n')
        self.context.f.write('}% setlength\n')

    @contextmanager
    def resizebox(self, width):
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\resizebox{%s}{!}{%%\n' % width)
        self.context.f.write(env.context.f.getvalue())
        self.context.f.write('}%resizebox\n')

    def medskip(self):
        self.context.f.write('\\medskip%%\n')

    def footnotesize(self):
        self.context.f.write('\\footnotesize%%\n')

    @contextmanager
    def mbox(self, width='', position='c'):  # XXX: FIXME
        """ Position: c, l, r. """
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\mbox[%s][%s]{%%\n' % (width, position))
        self.context.f.write(env.context.f.getvalue())
        self.context.f.write('}%\n')
        
    @contextmanager
    def tightbox(self):
        """ Fbox with no margin """
        with self.fbox('0pt') as x:
            yield x
 
    def lstlisting(self, code, language=None):
        params = ""
        if language is not None:
            params += 'language=%s' % language

        self.use_package('listings')
        self.context.f.write('\\begin{lstlisting}[%s]%%\n' % params)
        self.context.f.write(code)
        self.context.f.write('\\end{lstlisting}%\n')

    @contextmanager
    def subfigure(self, caption="", label=None):
        from .figure import SubFigure
        self.use_package('caption')
        self.use_package('subfig')
        subfigure = SubFigure(caption=caption, label=label,
                              context=self.context.child())
        yield subfigure
        subfigure.dump(main_context=self.context)


def make_options_string(**params):
    ss = []
    for k, v in list(params.items()):
        if v is None:
            continue
        if isinstance(v, bool) and v == True:
            ss.append(k)
        else:
            ss.append('%s=%s' % (k, v))
    return ",".join(ss)  
