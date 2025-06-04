import json
import sys

import gen_kill_definitions
from src.cfg.cfg import get_cfg
 
def Diff(list_a, list_b):
    return [val for val in list_a if val not in list_b]


def Union(*args):
    result = []
    seen = set()

    for lst in args:
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result

def get_reaching_defn(block):
    """
    OUT[B] = gen_b union (IN[B] - kill_b)
    IN[B] = Union OUT[p], p = predecessor of B
    """
    
    gen_b = gen_kill_definitions.get_generated_definition(block)
    kill_b = gen_kill_definitions.get_killed_definition(block)

    # in_into_block = Union()
    # out_from_block = Union(gen_b, Diff())
    

def reaching_defn():
    prog = json.load(sys.stdin)
    print(prog)

if __name__ == "__main__":
    reaching_defn()
