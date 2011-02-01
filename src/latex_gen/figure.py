from latex_gen.document import LatexEnvironment
from contextlib import contextmanager

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
        
        
