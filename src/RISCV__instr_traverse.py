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
    Op     = curr_instr[25:32]
    rs1    = 0
    rs2    = 0
    rd     = 0
    funct3 = '0' * 3  # 3 bit string
    funct7 = '0' * 7  # 7 bit string
    imm    = '0' * 32 # 32 bit string

    # R-type
    if Op == '0110011':
        funct7 = curr_instr[0:7]
        rs2    = int(curr_instr[7:12], 2)
        rs1    = int(curr_instr[12:17], 2)
        funct3 = curr_instr[17:20]
        rd     = int(curr_instr[20:25], 2)
        
    # I-type & load word & jalr
    elif Op == '0010011' or Op == '0000011' or Op == '1100111':
        imm    = f'{curr_instr[0]}' * 21 + curr_instr[1:12]
        rs1    = int(curr_instr[12:17], 2)
        funct3 = curr_instr[17:20]
        rd     = int(curr_instr[20:25], 2)

    # S-type
    elif Op == '0100011':
        imm    = f'{curr_instr[0]}' * 21 + curr_instr[1:7] + curr_instr[20:24] + curr_instr[24]
        rs2    = int(curr_instr[7:12], 2)
        rs1    = int(curr_instr[12:17], 2)
        funct3 = curr_instr[17:20]

    # B-type
    elif Op == '1100011':
        imm    = f'{curr_instr[0]}' * 20 + curr_instr[24] + curr_instr[1:7] + curr_instr[20:24] + '0'
        rs2    = int(curr_instr[7:12], 2)
        rs1    = int(curr_instr[12:17], 2)
        funct3 = curr_instr[17:20]
    
    # J-type
    elif Op == '1101111':
        imm    = f'{curr_instr[0]}' * 12 + curr_instr[12:20] + curr_instr[11] + curr_instr[1:7] + curr_instr[7:11] + '0'
        rd     = int(curr_instr[20:25], 2)
    
    else:
        print("Not defined")

    return Op, rs1, rs2, rd, funct3, funct7, BitStr(bit_str=imm)


def exec_instr(instr_list, curr_idx, registers):
    # get instruction
    curr_instr = instr_list[curr_idx]
    # decode instruction
    Op, funct, rs, rt, rd, sa, j_addr, imm = instr_decode(curr_instr)
    
    print(f'addr:{hex(curr_idx * 4)}, instr:{hex(int(curr_instr, 2))}')

    # execute instruction
    if int(curr_instr, 2) == 13: print('nop')
    # R-type
    elif Op == '0110011':
        if funct3 == '000':
            if funct7 == '0000000':
                print(f'add r{rd} r{rs} r{rt}')
                registers[rd] = registers[rs] + registers[rt]
            elif funct7 == ''
                print(f'sub r{rd} r{rs} r{rt}')
                registers[rd] = registers[rs] - registers[rt]
        
        elif funct3 == '111':
            print(f'and r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] & registers[rt]

        elif funct3 == '110':
            print(f'or r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] | registers[rt]

        elif funct3 == '100':
            print(f'xor r{rd} r{rs} r{rt}')
            registers[rd] = registers[rs] ^ registers[rt]
        
        elif funct3 == '001':
            print(f'sll r{rd} r{rt} {sa}')
            registers[rd] = registers[rt] << sa
        
        elif funct3 == '101':
            if funct7 == '0000000'
                print(f'srl r{rd} r{rt} {sa}')
                registers[rd] = registers[rt] >> sa
            
            elif funct7 == '0100000':
                print(f'sra r{rd} r{rt} {sa}')
                registers[rd] = registers[rt].sra(sa)   
        
        elif funct3 == '010':
            print(f'slt r{rd} r{rs} r{rt}')
            if registers[rs] < registers[rt]: registers[rd] = BitStr(value=1)
            else: registers[rd] = BitStr(value=0)
           
        else:
            print('unk')
    
    # jalr
    elif Op == '1100111':
        print(f'jalr r{rd} r{rs}')
            registers[rd] = BitStr(value=(curr_idx + 1) * 4)
            curr_idx = registers[rs].dec() // 4 - 1 # -1: idx + 1 in the end

    # J-type
    elif Op == '1101111':
        print(f'jal {hex(int(j_addr, 2))}')
        registers[31] = BitStr((curr_idx + 1) * 4)
        curr_idx = int(j_addr, 2) - 1 # -1: idx + 1 in the end
    
    # B-type
    elif Op == '1100011':
        if funct3 == '000':
            print(f'beq r{rs} r{rt} {hex(imm)}')
            if registers[rs] == registers[rt]:
                # TODO
                # curr_idx = int((curr_idx + imm) % math.pow(2, 14))

        elif funct3 == '001':
            print(f'bne r{rs} r{rt} {hex(imm)}')
            if registers[rs] != registers[rt]:
                # TODO
                # curr_idx = int((curr_idx + imm) % math.pow(2, 14))
  
    # I-type
    elif Op == '0010011':
        if funct3 == '000':
            print(f'addi r{rt} r{rs} {imm}')
            # TODO
            registers[rt] = registers[rs] + imm
    
        elif funct3 == '010':
            print(f'slti r{rt} r{rs} {imm}')
            # TODO
            if registers[rs] < imm: registers[rt] = BitStr(value=1)
            else: registers[rt] = BitStr(value=0)
    
        elif funct3 == '111':
            print(f'andi r{rt} r{rs} {imm}')
            # TODO
            registers[rt] = registers[rs] & imm
    
        elif funct3 == '110':
            print(f'ori r{rt} r{rs} {imm}')
            # TODO
            registers[rt] = registers[rs] | imm
    
        elif funct3 == '100':
            print(f'xori r{rt} r{rs} {imm}')
            # TODO
            registers[rt] = registers[rs] ^ imm
    
    # Load
    elif Op == '0000011':
        print(f'lw r{rt} r{rs} {imm}')
        # TODO
        mem_idx = (registers[rs] + imm).dec() // 4
        registers[rt] = D_mem[mem_idx]
        print(f"load D_mem[{mem_idx}]={D_mem[mem_idx].dec()} to r{rt}")
    
    # Store
    elif Op == '0100011':
        print(f'sw r{rt} r{rs} {imm}')
        # TODO
        mem_idx = (registers[rs] + imm).dec() // 4
        D_mem[mem_idx] = registers[rt]
        print(f"store r{rt}={registers[rt].dec()} to D_mem[{mem_idx}]")
    
    else:
        print('unk')

    # update curr_idx
    return curr_idx + 1


def print_reg(registers):
    # for i in range(len(registers)):
    for i in range(32):
        print(f'[{i}]\t{registers[i].dec()}', end='\t')
        if (i + 1) % 4 == 0:
            print()


"""Main"""
# define
fname     = sys.argv[1]
registers = [BitStr(value=0)] * 32
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
    # print_reg(registers)
    index += 1