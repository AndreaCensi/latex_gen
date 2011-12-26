from . import LatexContext, LatexEnvironment


class LatexDocument(LatexEnvironment):
    def __init__(self, document_class, class_options, graphics_path="."):
        self.context = LatexContext(graphics_path)
        self.document_class = document_class
        self.class_options = class_options

    def dump_stream(self, f):
        f.write('\\documentclass[%s]{%s}\n' % (self.class_options,
                                                  self.document_class))
        f.write('\\usepackage{graphicx}\n')
        f.write('\\usepackage{xcolor}\n')
        f.write('\\usepackage{subfig}\n')
        f.write('\\graphicspath{{%s/}}\n' % self.context.graphics_path)
        f.write(self.context.preamble.getvalue())
        f.write('\\begin{document}\n')
        f.write(self.context.f.getvalue())
        f.write('\\end{document}\n')


