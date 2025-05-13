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
            # do nothing
            pass

        # Check for definition
        if 'dest' in instr and instr['dest'] not in defined_and_not_used:
            defined_and_not_used.update({key: instr for key in instr['dest']})
            continue

        optimized_instrs.append(instr)
    print(defined_and_not_used)
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
            print("Unused: ", instr)
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
        if prev_len == len(optimized_instr):
            break
    return optimized_instr

def dce():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        optimized_instr = strong_dce(func['instrs'])
        print("Optimized Instructions:")
        for instr in optimized_instr:
            print(instr)

if __name__ == '__main__':
    dce()
