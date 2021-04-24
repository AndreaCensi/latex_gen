__version__ = "7.1.2104241741"
__date__ = "2021-04-24T17:41:52.692256"
from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
logger.hello_module(name=__name__, filename=__file__, version=__version__, date=__date__)

from .structures import *
from .compile_latex import *

from .envs import *
from .utils import *
from .ifs import *

from .context import *
from .environment import *
from .document import *
from .frags import *
