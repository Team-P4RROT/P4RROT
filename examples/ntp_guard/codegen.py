import sys

sys.path.append("../../src/")

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.core.commands import *
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *
from p4rrot.standard_fields import *

UID.reset()
fp = FlowProcessor(
    istruct=[
        ("flags", uint8_t),
        ("peer_stratum", uint8_t),
        ("polling_interval", uint8_t),
        ("peer_precision", uint8_t),
        ("root_delay", uint32_t),
        ("root_dispersion", uint32_t),
        ("reference_id", uint32_t),
        ("reference_timestamp", uint32_t),
        ("origin_timestamp", uint32_t),
        ("receive_timestamp", uint32_t),
        ("transmit_timestamp", uint32_t),
    ],
    helpers=[("exploit", bool_t)],
    mstruct=[],
)
(
fp
.add(CheckControlPlaneSet(["origin_timestamp"], "exploit"))
.add(If("exploit"))
.add(DropPacket())
.EndIf()
)
fs = FlowSelector("IPV4_UDP", [], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("result.p4app")
