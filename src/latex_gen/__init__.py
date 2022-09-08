__version__ = "7.3"
__date__ = ""

from zuper_commons.logs import ZLogger, ZLoggerInterface

logger: ZLoggerInterface = ZLogger(__name__)
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

logger.hello_module_finished(__name__)
