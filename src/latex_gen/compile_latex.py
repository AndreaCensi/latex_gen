import os
import subprocess
from .structures import BadTex

__all__ = [
    "compile_tex",
]


def compile_tex(filename, cwd=None):
    """Raises BadTex if the file is not compilable."""
    assert os.path.exists(filename)
    if cwd is None:
        cwd = os.path.dirname(filename)

    filename_rel = os.path.relpath(filename, cwd)
    basename = os.path.splitext(filename_rel)[0]
    run_pdflatex(basename, cwd)
    clean_temporary_files(basename)


def run_pdflatex(basename, cwd):
    command = ["pdflatex", "-halt-on-error", "-interaction=errorstopmode", basename]
    val = subprocess.call(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if val != 0:
        # TODO: return error:
        msg = "Could not compile %r." % basename
        raise BadTex(msg)


def clean_temporary_files(basename):
    for suff in ["aux", "log"]:
        f = basename + "." + suff
        print(f)
        if os.path.exists(f):
            os.unlink(f)
