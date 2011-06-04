import mimetypes, os
from StringIO import StringIO
from contextlib import contextmanager

from .utils import latex_escape


        
class LatexContext:
    def __init__(self, graphics_path="."):
        self.f = StringIO()
        self.preamble = StringIO()
        self.graphics_path = graphics_path
        self.parent = None
        self.count = 0
        
    def generate_file_id(self):
        if self.parent:
            return self.parent.generate_file_id()
        f = "file%s" % self.count
        self.count += 1 
        return f 
    
    def child(self):
        ''' Generates a child context; sharing some data '''
        c = LatexContext(self.graphics_path)
        c.parent = self
        return c


class LatexEnvironment:
    def __init__(self, context):
        self.context = context
                
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
        ''' Writes the text on the stream (it will be escaped, use :py:func:`tex`
            for raw TeX. '''
        self.context.f.write(latex_escape(t))
        
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
            row_tex = ['\\makebox[5cm][r]{%s}' % row] + ['\\makebox[1cm]{%s}' % x for x in data[i]]
            write_row_tex(row_tex)
            hline()
            
        self.context.f.write('\\end{tabular}\n')
        
    def tex(self, tex):
        ''' Writes raw TeX string. '''
        self.context.f.write(tex)
        
    def input(self, filename):
        self.context.f.write('\\input{%s}\n' % filename)
    
    def use_package(self, name, options=""):
        self.context.preamble.write('\\usepackage[%s]{%s}\n' % (options, name))
        
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
        return self.tabular(alignment, env='longtable')
        
    def graphics_data(self, data, mime, width="3cm", id=None):
        suffix = mimetypes.guess_extension(mime)
        if id is None:
            id = self.context.generate_file_id()
        # cannot have '.' in the filename, otherwise latex gets confused
        id = id.replace('.', '_')
        id = id.replace('/', ':')
            
        filename = os.path.join(self.context.graphics_path, id + suffix)
        # make sure dir exists
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(filename, 'w') as f:
            f.write(data)
        self.context.f.write('\\includegraphics[width=%s]{%s}%%\n' % (width, id))
   
    @contextmanager
    def minipage(self, width, align=''):
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\begin{minipage}[%s]{%s}\n' % (align, width))
        self.context.f.write(env.context.f.getvalue())    
        self.context.f.write('\\end{minipage}\n')
        
    @contextmanager
    def fbox(self):
        env = LatexEnvironment(self.context.child())
        yield env
        self.context.preamble.write(self.context.preamble.getvalue())
        self.context.f.write('\\fbox{%\n')
        self.context.f.write(env.context.f.getvalue())    
        self.context.f.write('}%\n')
    
    
class LatexDocument(LatexEnvironment):
    def __init__(self, document_class, class_options, graphics_path="."):
        self.context = LatexContext(graphics_path)
        self.document_class = document_class
        self.class_options = class_options 
        
    def dump_stream(self, file):
        file.write('\\documentclass[%s]{%s}\n' % (self.class_options,
                                                  self.document_class))
        file.write('\\usepackage{graphicx}\n')
        file.write('\\usepackage{xcolor}\n')
        file.write('\\usepackage{subfig}\n') 
        file.write('\\graphicspath{{%s/}}\n' % self.context.graphics_path)
        file.write(self.context.preamble.getvalue())
        file.write('\\begin{document}\n')
        file.write(self.context.f.getvalue())
        file.write('\\end{document}\n')


