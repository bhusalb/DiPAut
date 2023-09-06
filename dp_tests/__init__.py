from . import disclosing_cycle
from . import privacy_violating_path
from . import leaking_cycle
from . import leaking_pair
from . import output_distinction

active_tests = [
    leaking_cycle,
    disclosing_cycle,
    leaking_pair,
    privacy_violating_path
]
