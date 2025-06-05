import json
import sys

import gen_kill_definitions
from src.cfg.cfg import mycfg
 
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

# block to reaching definitioin
OUT = {}
IN = {}

def reaching_defn():
    prog = json.load(sys.stdin)
    
    block_lst = []
    for blocks in mycfg(prog):
        gen_kill_definitions.handle_blocks(blocks)
        for block in blocks:
            block_lst.append(block)

    for block in block_lst:
        OUT[block.name] = []

    has_out_changed = True

    while(has_out_changed):
        for block in block_lst:
            predecessor_gen = []
            for val in block.predecessors:
                op = OUT[val]
                if op:
                    predecessor_gen.append(op)

            IN[block.name]= Union([test for val in predecessor_gen for test in val ])
            gen_b = gen_kill_definitions.get_generated_definition(block.name)
            kill_b = gen_kill_definitions.get_killed_definition(block.name)
            prev_output = OUT[block.name]
            OUT[block.name] = Union([definition.name for definition in gen_b], Diff(IN[block.name], [definition.name for definition in kill_b]))

            if not Diff(prev_output, OUT[block.name]) : 
                has_out_changed = False;
            else:
                has_out_changed = True
            

    for block, definitions in OUT.items():
        print("Definiton output from "  + block + ":", definitions)
   
    for block, definitions in IN.items():
        print("Definition input to " + block + ":", definitions)

if __name__ == "__main__":
    reaching_defn()
