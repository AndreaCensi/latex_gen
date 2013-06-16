import os
from .file_utils import make_sure_dir_exists
from .environment import LatexEnvironment
from .context import LatexContext


__all__ = ['LatexDocument']


class LatexDocument(LatexEnvironment):
    def __init__(self, document_class='article',
                 class_options="", graphics_path="."):
        self.context = LatexContext(graphics_path)
        self.document_class = document_class
        self.class_options = class_options

    def dump_stream(self, f):
        f.write('\\documentclass[%s]{%s}\n' % (self.class_options,
                                                  self.document_class))

        self.context.dump_preamble(f)
        # f.write('% \\usepackage{xcolor}\n')
        # TODO: check bad chars in graphics_path
        f.write('\\usepackage{graphicx}\n')
        f.write('\\graphicspath{{%s/}}\n' % self.context.graphics_path)
        f.write(self.context.preamble.getvalue())
        f.write('\\begin{document}\n')
        f.write(self.context.f.getvalue())
        f.write('\\end{document}\n')

    def fullpage(self):
        ''' Use the fullpage package. '''
        self.use_package('fullpage')

    def write_to_file(self, filename):
        ''' Writes to a file, making sure the directory exists.'''
        dirname = os.path.dirname(filename)
        make_sure_dir_exists(dirname)
        with open(filename, 'w') as f:
            self.dump_stream(f)
