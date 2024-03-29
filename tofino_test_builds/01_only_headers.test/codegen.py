import sys

sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *

UID.reset()
fp = FlowProcessor(
    istruct=[("a", uint32_t), ("b", uint32_t)],
    ostruct=[("s", uint32_t)],
    mstruct=[("t", uint32_t)],
    method="RESPOND",
)
gc = fp.get_generated_code()
script_dir = os.path.dirname(__file__)
dir_path = os.path.join(script_dir, "result.p4app")
gc.dump(dir_path)
