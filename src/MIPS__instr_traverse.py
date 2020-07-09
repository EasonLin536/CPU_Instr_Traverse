import sys
import math
from BitStr import BitStr

"""Define Functions"""
def readfile(fname):
    instr_list = []
    
    f = open(fname, "r")
    for line in f:
        line = line.split('//')
        if len(line) < 3: continue # not instr
        instr = line[0].replace('_', '')
        instr_list.append(instr)
        
    instr_list = [x for x in instr_list if x != '']

    return instr_list


def instr_decode(curr_instr):
    """
    curr_instr: 32 bit string
    """
    Op     = curr_instr[0:6]           # string
    funct  = curr_instr[26:32]         # string
    rs     = int(curr_instr[6 :11], 2) # int
    rt     = int(curr_instr[11:16], 2) # int
    rd     = int(curr_instr[16:21], 2) # int
    sa     = int(curr_instr[21:26], 2) # int
    j_addr = curr_instr[6 :32]         # 26 bits string
    imm    = int(curr_instr[16:32], 2) # int

    return Op, funct, rs, rt, rd, sa, j_addr, imm


def print_reg(registers):
    # for i in range(len(registers)):
    for i in range(32):
        print(f'[{i}]\t{registers[i].dec()}', end='\t')
        if (i + 1) % 4 == 0:
            print()


def exec_instr(instr_list, curr_idx, registers):
    # get instruction
    curr_instr = instr_list[curr_idx]
    # decode instruction
    Op, funct, rs, rt, rd, sa, j_addr, imm = instr_decode(curr_instr)
    
    print(f'addr:{hex(curr_idx * 4)}, instr:{hex(int(curr_instr, 2))}')

    # execute instruction
    if int(curr_instr, 2) == 0: print('nop')
    # R-type
    elif Op == '000000':
        if funct == '100000':
            print(f'add r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] + registers[rt]

        elif funct == '100010':
            print(f'sub r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] - registers[rt]
        
        elif funct == '100100':
            print(f'and r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] & registers[rt]

        elif funct == '100101':
            print(f'or r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] | registers[rt]

        elif funct == '100110':
            print(f'xor r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] ^ registers[rt]
        
        elif funct == '100111':
            print(f'nor r{rd} r{rs} r{rt}')
            registers[rd] = ~(registers[rs] | registers[rt])
        
        elif funct == '000000':
            print(f'sll r{rd} r{rt} {sa}')
            registers[rd] = registers[rt] << sa
        
        elif funct == '000010':
            print(f'srl r{rd} r{rt} {sa}')
            registers[rd] = registers[rt] >> sa
            
        elif funct == '000011':
            print(f'sra r{rd} r{rt} {sa}')
            registers[rd] = registers[rt].sra(sa)   
        
        elif funct == '101010':
            print(f'slt r{rd} r{rs} r{rt}')
            if registers[rs] < registers[rt]: registers[rd] = BitStr(value=1)
            else: registers[rd] = BitStr(value=0)

        elif funct == '011000':
            print(f'mult r{rs} r{rt}')
            registers[32], registers[33] = registers[rs] * registers[rt]
        
        elif funct == '011010':
            print(f'div r{rs} r{rt}')
            registers[32], registers[33] = registers[rs] / registers[rt]

        elif funct == '010010':
            print(f'mflo {rd}')
            registers[rd] = registers[33]
        
        elif funct == '010000':
            print(f'mfhi {rd}')
            registers[rd] = registers[32]
        
        elif funct == '001000':
            print(f'jr r{rs}')
            curr_idx = registers[rs].dec() // 4 - 1 # -1: idx + 1 in the end
        
        elif funct == '001001':
            print(f'jalr r{rd} r{rs}')
            registers[rd] = BitStr(value=(curr_idx + 1) * 4)
            curr_idx = registers[rs].dec() // 4 - 1 # -1: idx + 1 in the end
        
        else:
            print('unk')

    # J-type
    elif Op == '000010':
        print(f'j {hex(int(j_addr, 2))}')
        curr_idx = int(j_addr, 2) - 1 # -1: idx + 1 in the end
    
    elif Op == '000011':
        print(f'jal {hex(int(j_addr, 2))}')
        registers[31] = BitStr((curr_idx + 1) * 4)
        curr_idx = int(j_addr, 2) - 1 # -1: idx + 1 in the end
    
    # B-type
    elif Op == '000100':
        print(f'beq r{rs} r{rt} {hex(imm)}')
        if registers[rs] == registers[rt]:
            curr_idx = int((curr_idx + imm) % math.pow(2, 14))

    elif Op == '000101':
        print(f'bne r{rs} r{rt} {hex(imm)}')
        if registers[rs] != registers[rt]:
            curr_idx = int((curr_idx + imm) % math.pow(2, 14))
  
    # I-type
    elif Op == '001000':
        print(f'addi r{rt} r{rs} {imm}')
        registers[rt] = registers[rs] + imm
    
    elif Op == '001010':
        print(f'slti r{rt} r{rs} {imm}')
        if registers[rs] < imm: registers[rt] = BitStr(value=1)
        else: registers[rt] = BitStr(value=0)
    
    elif Op == '001100':
        print(f'andi r{rt} r{rs} {imm}')
        registers[rt] = registers[rs] & imm
    
    elif Op == '001101':
        print(f'ori r{rt} r{rs} {imm}')
        registers[rt] = registers[rs] | imm
    
    elif Op == '001110':
        print(f'xori r{rt} r{rs} {imm}')
        registers[rt] = registers[rs] ^ imm
    
    # Load
    elif Op == '100011':
        print(f'lw r{rt} r{rs} {imm}')
        mem_idx = (registers[rs] + imm).dec() // 4
        registers[rt] = D_mem[mem_idx]
        print(f"load D_mem[{mem_idx}]={D_mem[mem_idx].dec()} to r{rt}")
    
    # Store
    elif Op == '101011':
        print(f'sw r{rt} r{rs} {imm}')
        mem_idx = (registers[rs] + imm).dec() // 4
        D_mem[mem_idx] = registers[rt]
        print(f"store r{rt}={registers[rt].dec()} to D_mem[{mem_idx}]")
    
    else:
        print('unk')

    # update curr_idx
    return curr_idx + 1

"""Main"""
# define
fname     = sys.argv[1]
registers = [BitStr(value=0)] * 34 # 2 for HI & LO
D_mem     = [BitStr(value=0)] * 1024

# output instructions 1 by 1 or not
one_at_a_time = True
if int(sys.argv[2]) == 0: 
    one_at_a_time = False
else: 
    one_at_a_time = True

# get all instructions
instr_list = []
instr_list = readfile(fname)

index = 0
curr_idx = 0
while (curr_idx < len(instr_list)):
    if one_at_a_time:
        cmd = input()
        if cmd != '': break

    print(f'\n[{index}]', end=' ')
    # execute instruction and update curr_idx
    curr_idx = exec_instr(instr_list, curr_idx, registers)
    # print updated registers
    print_reg(registers)
    index += 1