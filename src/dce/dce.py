import json
import sys

def strong_dce(instrs):
    """
    Eliminates reassignment without the previous use of assignment
    """
    optimized_instrs = []
    defined_and_not_used = {}
    for instr in instrs:
        # Check for usage
        if 'args' in instr:
            keys_to_remove = [key for key, value in defined_and_not_used.items() if key in instr['args']]
            for key in keys_to_remove:
                optimized_instrs.append(defined_and_not_used[key])
                del defined_and_not_used[key]
            if 'dest' not in instr:
                optimized_instrs.append(instr)
        # Check for definition
        if 'dest' in instr and instr['dest'] not in defined_and_not_used:
            defined_and_not_used.update({instr['dest']: instr})
            continue

        # optimized_instrs.append(instr)
    return optimized_instrs

# Very basic dead code elimination
def check_dc(instrs):
    optimized_instr = []
    used = set()
    for instr in instrs:
        if 'args' in instr:
            used.update(instr['args'])

    for instr in instrs:
        if 'dest' in instr and instr['dest'] not in used:
            continue
        optimized_instr.append(instr)
    return optimized_instr

def perform_dce(instrs):
    """
    Repeatedly performs basic dead code elimination until convergence
    """
    optimized_instr = check_dc(instrs)
    while True:
        prev_len = len(optimized_instr)
        optimized_instr = check_dc(optimized_instr)
        instr = optimized_instr
        if prev_len == len(optimized_instr):
            break
    return optimized_instr

def dce():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        optimized_instr = perform_dce(func['instrs'])
        optimized_instr = strong_dce(optimized_instr)
        func['instrs'] = optimized_instr 
        #instr = optimized_instr
    return json.dump(prog, sys.stdout)

if __name__ == '__main__':
    dce()
