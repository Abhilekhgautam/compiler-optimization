import json
import sys

TERMINATORS = 'br', 'jmp', 'ret'

class Block:
    def __init__(self, name, instrs, predecessors, successors):
        self.name = name
        self.instrs = instrs
        self.predecessors = predecessors
        self.successors = successors;

# create a cfg:
def get_cfg(block_map):
    out = []
    for index, (name, block) in enumerate(block_map.items()):
        # get the last instruction
        last_instr = block[-1]
        predecessors = [block.name for block in out if name in block.successors]
        if last_instr['op'] in ('jmp', 'br'):
            block = Block(name, block, predecessors, last_instr['labels'])
            # out[name] = last_instr['labels']
            #print(out[name])
            # print(last_instr['labels'][0])
        elif last_instr['op'] == 'ret':
            block = Block(name, block, predecessors, [])
        else:
            if index + 1 == len(block_map):
                block = Block(name, block, predecessors, [])
            else:
                block = Block(name, block, predecessors, list(block_map)[index + 1])
        out.append(block)        
    return out



def block_map(blocks):
    out = {}
    for block in blocks:
        if len(block) >= 1:
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


def mycfg(prog):
    #prog = json.load(sys.stdin)
    blocks = []
    for func in prog['functions']:
        val = block_map(form_block(func))
        blocks.append(get_cfg(val))
    return blocks

if __name__ == '__main__':
    mycfg({})


