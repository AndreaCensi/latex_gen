from contextlib import contextmanager
import os

from .file_utils import make_sure_dir_exists
from .document import LatexEnvironment, LatexContext, LatexDocument

@contextmanager
def latex_document(filename_or_stream,
             graphics_path=None, document_class="article",
             class_options=""):
    is_filename = isinstance(filename_or_stream, str)
    if is_filename:
        if graphics_path is None:
            graphics_path = os.path.dirname(filename_or_stream)
        make_sure_dir_exists(graphics_path)
        graphics_path = os.path.relpath(graphics_path,
                                        os.path.dirname(filename_or_stream))
    else:
        if graphics_path is None:
            graphics_path = os.getcwd()

    document = LatexDocument(graphics_path=graphics_path,
                             document_class=document_class,
                             class_options=class_options)
    yield document

    if is_filename:
        with open(filename_or_stream, 'w') as f:
            document.dump_stream(f)
    else:
        document.dump_stream(filename_or_stream)
    
@contextmanager
def latex_fragment(filename_or_stream, graphics_path=None):
    is_filename = isinstance(filename_or_stream, str)
    if is_filename:
        if graphics_path is None:
            graphics_path = os.path.dirname(filename_or_stream)
        make_sure_dir_exists(graphics_path)
        graphics_path = os.path.relpath(graphics_path,
                                        os.path.dirname(filename_or_stream))
    else:
        if graphics_path is None:
            graphics_path = os.getcwd()

    ###        
    context = LatexContext(graphics_path=graphics_path)
    environment = LatexEnvironment(context)
    
    yield environment
    ###        
    if is_filename:
        with open(filename_or_stream, 'w') as f:
            f.write(context.f.getvalue())    
    else:
        filename_or_stream.write(context.f.getvalue())


