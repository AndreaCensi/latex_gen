import mimetypes, os
from StringIO import StringIO
from contextlib import contextmanager

from .utils import latex_escape


def make_sure_dirs_exist(filename, graphics_path):
    dir = os.path.dirname(filename)
    if not os.path.exists(dir): 
        os.makedirs(dir)

    if not os.path.exists(graphics_path): 
        os.makedirs(graphics_path)

class Latex:
    
    @staticmethod
    @contextmanager
    def document(filename, graphics_path=None, document_class="article",
                 class_options=""):
        
        if graphics_path is None:
            graphics_path = os.path.dirname(filename)
        graphics_path = os.path.relpath(graphics_path, os.path.dirname(filename))
        
        make_sure_dirs_exist(filename, graphics_path)
        

        document = LatexDocument(graphics_path=graphics_path,
                                 document_class=document_class,
                                 class_options=class_options)
        yield document

        with open(filename, 'w') as f:
            document.dump_stream(f)
        
    @staticmethod
    @contextmanager
    def fragment(filename, graphics_path=None):
        if graphics_path is None:
            graphics_path = os.path.dirname(filename)
        graphics_path = os.path.relpath(graphics_path, os.path.dirname(filename))
 
        make_sure_dirs_exist(filename, graphics_path)
        
        context = LatexContext(graphics_path=graphics_path)
        environment = LatexEnvironment(context)
        
        yield environment

        with open(filename, 'w') as f:
            f.write(context.f.getvalue())    
    
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
            
        alignment_string = '|r||' + ('r|' * len(col_desc))
        self.context.f.write('\\begin{tabular}{%s}\n' % alignment_string)
        hline()
        if write_col_desc:
            row_tex = [''] + ['\\makebox[0.7cm]{%s}' % x for x in col_desc]
            write_row_tex(row_tex)
            hline()
            hline()
        
        for i, row in enumerate(row_desc):
            row_tex = ['\\makebox[2.3cm][r]{%s}' % row] + ['\\makebox[0.7cm]{%s}' % x for x in data[i]]
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
        figure = Figure(caption=caption, label=label, placement=placement,
                        context=self.context.child(), double=double)
        yield figure
        figure.dump(main_context=self.context)
    
    @contextmanager
    def tabular(self, alignment):
        tabular = Tabular(alignment, context=self.context.child())
        yield tabular
        tabular.dump(main_context=self.context)
        
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

class Figure(LatexEnvironment):
    def __init__(self, caption, label, placement, context, double):
        self.caption = caption
        self.label = label
        self.context = context
        self.placement = placement
        self.double = double
    
    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    @contextmanager
    def subfigure(self, caption="", label=None):
        subfigure = SubFigure(caption=caption, label=label,
                           context=self.context.child())
        yield subfigure
        subfigure.dump(main_context=self.context)
    
    def dump(self, main_context):
        # writes everything, and caption delayed
        main_context.preamble.write(self.context.preamble.getvalue())
        env = "figure*" if self.double else "figure"
        main_context.f.write('\\begin{%s}[%s]\n' % (env, self.placement))
        main_context.f.write(self.context.f.getvalue())
        if self.label:
            label = '\\label{%s}' % self.label
        else:
            label = "" 
        main_context.f.write('\\caption{%s%s}\n' % (label, self.caption))
        main_context.f.write('\\end{%s}\n' % env)
        
class Tabular(LatexEnvironment):
    allowed = ['c', 'r', 'l']
    def __init__(self, alignment, context):
        assert isinstance(alignment, list) 
        assert all(x in Tabular.allowed for x in alignment)
        self.ncols = len(alignment)
        self.alignment = alignment
        self.context = context
        
    def hline(self):
        self.context.f.write('\\hline\n')
    
    class Row():
        def __init__(self, ncols, context):
            self.ncols = ncols
            self.cols = []
            self.context = context
            
        def cell_tex(self, tex=''):
            if len(self.cols) == self.ncols:
                raise Exception('Too many columns')
            self.cols.append(tex)
        
        @contextmanager
        def cell(self):
            if len(self.cols) == self.ncols:
                raise Exception('Too many columns')
            cell = LatexEnvironment(self.context.child())
            yield cell
            self.context.preamble.write(cell.context.preamble.getvalue())
            self.cols.append(cell.context.f.getvalue())
            
            
    @contextmanager
    def row(self): 
        row = Tabular.Row(self.ncols, self.context)
        yield row
        if len(row.cols) < self.ncols:
            raise Exception('Too few columns')
        tex = " & ".join(row.cols)
        self.context.f.write(tex)
        self.context.f.write('\\\\ \n ')
        
    def row_tex(self, *cols):
        if len(cols) != self.ncols:
            raise Exception('Got %d cols instead of %d expected.' % 
                            (len(cols), self.ncols))
        tex = " & ".join(list(cols))
        self.context.f.write(tex)
        self.context.f.write('\\\\ \n ')

    
    def dump(self, main_context):
        main_context.preamble.write(self.context.preamble.getvalue())
        env = "tabular"
        alignment = "".join(self.alignment)
        main_context.f.write('\\begin{%s}{%s}\n' % (env, alignment))
        main_context.f.write(self.context.f.getvalue())
        main_context.f.write('\\end{%s}\n' % env)
        
        
class StructureError(Exception):
    pass

class SubFigure(LatexEnvironment):
    def __init__(self, caption, label, context):
        self.caption = caption
        self.label = label
        self.context = context
    
    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    def subfigure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    def dump(self, main_context):
        body = self.context.f.getvalue()
        if self.label:
            label = "\\label{%s}" % self.label
        else:
            label = ""
        caption = self.caption
        main_context.preamble.write('\\usepackage{subfig}\n')
        
        main_context.f.write('\\subfloat[%s%s]{%s}\n' % (label, caption, body))
