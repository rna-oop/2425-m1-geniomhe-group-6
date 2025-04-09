from . import Families, IO, Processing, Structure, Transformations
from .utils import *
from .viz import *

__all__ = ["Families", "IO", "Processing", "Structure", "Transformations", "utils", "viz"]
with open(os.path.join(os.path.dirname(__file__), "../VERSION")) as version_file:
    __version__ = version_file.read().strip()