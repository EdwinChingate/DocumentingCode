from __future__ import annotations

from collect_used_names import *
# TODO: could not auto-resolve the following names —
#   from ??? import all_names
#   from ??? import direct_calls
#   from ??? import locally_defined
#   from ??? import root_names



def get_external_names(source: str) -> Set[str]:
    """
    Return all names used in source that are not defined inside it.
    Convenience wrapper around collect_used_names().
    No global variables, no classes.
    """
    direct_calls, root_names, all_names, locally_defined = collect_used_names(source)
    used = direct_calls | root_names | all_names
    return used - locally_defined
