import json
import sys

TERMINATORS = 'br', 'jmp', 'ret'

# create a cfg:

def get_cfg(block_map):
    out = {}
    for index, (name, block) in enumerate(block_map.items()):
        # get the last instruction
        last_instr = block[-1]
        if last_instr['op'] in ('jmp', 'br'):
            out[name] = last_instr['labels']
            print(out[name])
            # print(last_instr['labels'][0])
        elif last_instr['op'] == 'ret':
            out[name] = []
        else:
            if index + 1 == len(block_map):
                out[name] = []
            else:
                print("Inside if of else")
                out[name] = [list(block_map)[index + 1]]
    return out



def block_map(blocks):
    out = {}
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))

        out[name] = block
    return out

def form_block(body):
    cur_block = []

    for instr in body['instrs']:
        if 'op' in instr:
            cur_block.append(instr)
            if instr['op'] in TERMINATORS:
                # this is the end of the block
                yield cur_block
                cur_block = []
        else: # we encountered a label
            yield cur_block
            
            cur_block = [instr]

    yield cur_block


def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        val = block_map(form_block(func))
        print(get_cfg(val))

if __name__ == '__main__':
    mycfg()


