__version__ = "7.3"
__date__ = ""

from zuper_commons.logs import ZLogger
from zuper_commons.logs import ZLoggerInterface

logger: ZLoggerInterface = ZLogger(__name__)
logger.hello_module(name=__name__, filename=__file__, version=__version__, date=__date__)

from .compile_latex import *
from .context import *
from .document import *
from .environment import *
from .envs import *
from .frags import *
from .ifs import *
from .structures import *
from .utils import *

logger.hello_module_finished(__name__)
