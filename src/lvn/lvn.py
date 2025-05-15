import json
import sys

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
    name2index = {}
    my_table = lvn_table()
    count = 0
    for instr in function['instrs']:
        if 'op' in instr:
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

            elif 'args' in instr:
                result = [name2index.get(item, item) for item in instr['args']]
                if len(result) == 2 and result[1] not in name2index:
                    val = lvn_table_value(instr['op'], None, result[0], result[1])
                    if 'dest' in instr:
                        if my_table.doesnot_have(val):
                            count = count + 1
                            my_table.add_to_table(count, val, instr['dest'])
                        name2index[instr['dest']] = count

                elif len(result) == 2 and result[1] in name2index:
                    name2index[instr['dest']] = count

                elif result[0] not in name2index:
                    val = lvn_table_value(instr['op'], None, result[0], None)
                    if 'dest' in instr:
                        if my_table.doesnot_have(val):
                            count = count + 1
                            my_table.add_to_table(count, val, instr['dest'])
                        
                        name2index[instr['dest']] = count

                elif result[0] in name2index:
                    name2index[instr['dest']] = count
    
    for key, value in name2index.items():
        print(f"{key}: {value}")
                 
    return my_table


def entry():
    prog = json.load(sys.stdin)
    for function in prog['functions']:
        table = lvn(function)
        table.print_table()

if __name__ == '__main__':
    entry()
