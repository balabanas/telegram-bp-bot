from bpb.settings.base import *

try:
    from bpb.settings.prod import *
except ImportError:
    pass