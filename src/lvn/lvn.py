import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.dce.dce import dce

COMMUTATIVE_OPERATOR = 'add', 'mul'

class lvn_table_value:
    def __init__(self, op, value, index1, index2):
        self.op = op
        self.value = value
        self.index1 = index1
        self.index2 = index2

    def __eq__(self, other):
        return (
                self.op == other.op and
                self.value == other.value and
                self.index1 == other.index1 and
                self.index2 == other.index2
                )
   
    def __str__(self):
        return f'({self.op}, {self.value}, {self.index1}, {self.index2})'

class lvn_table:
    def __init__(self):
        self.table = {}
    def add_to_table(self, index, value, canonical_name):
        self.table[index] = (value, canonical_name)

    def print_table(self):
        print(f"{'#':<6} | {'value':<12} | {'canonical name'}")
        print('-' * 40)
        for key, value in self.table.items():
            print(f"{key:<6} | {value[0]} | {value[1]}")

    def doesnot_have(self, value):
        for val in self.table.values():
            if val[0] == value:
                return False
        return True

def lvn(function):
    # hold the current state (environment)
    name2index = {}
    my_table = lvn_table()
    # index
    count = 0
    for instr in function['instrs']:
        # only do if not labels
        if 'op' in instr:
            # case 1: const value
            if 'value' in instr:
                val = lvn_table_value(instr['op'], instr['value'], None, None)
                if 'dest' in instr:
                    if my_table.doesnot_have(val):
                        count = count + 1
                        my_table.add_to_table(count, val, instr['dest'])

                    name2index[instr['dest']] = count

                else:
                    if my_table.doesnot_have(val):
                        count = count + 1
                        my_table.add_to_table(count, val, None)
                    
                    name2index[instr['dest']] = count
            # case 2: variable reference
            elif 'args' in instr:
                # Check if the operand is in the current environment
                result = [name2index.get(item, item) for item in instr['args']]
                # Check If the operator takes 2 operands
                if len(result) == 2 and result[1] not in name2index:
                    # handle commutative property: smaller index first and then larger
                    if instr['op'] in COMMUTATIVE_OPERATOR and result[0] > result[1]:
                        val = lvn_table_value(instr['op'], None, result[1], result[0])
                    else:
                        val = lvn_table_value(instr['op'], None, result[0], result[1])

                    if 'dest' in instr:
                        # If value is already present, no new table entry
                        if my_table.doesnot_have(val):
                            count = count + 1
                            my_table.add_to_table(count, val, instr['dest'])
                            canonical_name_first = my_table.table[result[0]][1]
                            canonical_name_second = my_table.table[result[1]][1]
                            instr['args'][0] = canonical_name_first
                            instr['args'][1] = canonical_name_second

                        name2index[instr['dest']] = count

                elif len(result) == 2 and result[1] in name2index:
                    name2index[instr['dest']] = count

                elif result[0] not in name2index:
                    val = lvn_table_value(instr['op'], None, result[0], None)
                    if 'dest' in instr:
                        if my_table.doesnot_have(val):
                            count = count + 1
                            my_table.add_to_table(count, val, instr['dest'])
                            # Get the canonical name for index in the lvn_value tuple
                            canonical_name = my_table.table[result[0]][1]
                            instr['args'][0] = canonical_name

                        
                        name2index[instr['dest']] = count

                elif result[0] in name2index:
                    name2index[instr['dest']] = count

    
                 
    return my_table


def entry():
    prog = json.load(sys.stdin)
    for function in prog['functions']:
        lvn(function)
    return json.dump(prog, sys.stdout)

if __name__ == '__main__':
    entry()
