# CPU Instruction Traverse
2020 Spring Digital System Design, NTUEE

Debugging tool for CPU instructions.

## Input and Output
### Input instruction pattern
32 bits instructions are the only thing needed.
```
000000_00000_00000_00000_00000_000000 //0x00//
000010_00000000000000000000101110     //0x04//
101011_00000_01000_0000001111111100   //0x08//
000000_11111_00000_00000_00000_001000 //0x0C//
001000_00000_01011_0000000000010000   //0x10//
001000_00000_01001_0000000000000000   //0x14//
001000_00000_01010_0000000000000001   //0x18//
001000_00000_01111_0000000000000000   //0x1C//
101011_01111_01001_0000000000000000   //0x20//
001000_01111_01111_0000000000000100   //0x24//
101011_01111_01010_0000000000000000   //0x28//
001000_01001_01000_0000000000000000   //0x2C//
000011_00000000000000000000000010     //0x30//
001000_01010_01000_0000000000000000   //0x34//
000011_00000000000000000000000010     //0x38//
```
### Output form
Print out index, I_mem address, instruction, instruction description, and register values.
```
[1210] addr:0xc, instr:0x3e00008
jr r31
[0]     0       [1]     0       [2]     0       [3]     0
[4]     0       [5]     0       [6]     0       [7]     0
[8]     144     [9]     64      [10]    12      [11]    4
[12]    4       [13]    377     [14]    610     [15]    1
[16]    16      [17]    100     [18]    0       [19]    0
[20]    0       [21]    0       [22]    0       [23]    0
[24]    0       [25]    0       [26]    0       [27]    0
[28]    0       [29]    0       [30]    208     [31]    172

[1211] addr:0xac, instr:0x214a0004
addi r10 r10 4
[0]     0       [1]     0       [2]     0       [3]     0
[4]     0       [5]     0       [6]     0       [7]     0
[8]     144     [9]     64      [10]    16      [11]    4
[12]    4       [13]    377     [14]    610     [15]    1
[16]    16      [17]    100     [18]    0       [19]    0
[20]    0       [21]    0       [22]    0       [23]    0
[24]    0       [25]    0       [26]    0       [27]    0
[28]    0       [29]    0       [30]    208     [31]    172

[1212] addr:0xb0, instr:0x1549fffc
bne r10 r9 0xfffc
[0]     0       [1]     0       [2]     0       [3]     0
[4]     0       [5]     0       [6]     0       [7]     0
[8]     144     [9]     64      [10]    16      [11]    4
[12]    4       [13]    377     [14]    610     [15]    1
[16]    16      [17]    100     [18]    0       [19]    0
[20]    0       [21]    0       [22]    0       [23]    0
[24]    0       [25]    0       [26]    0       [27]    0
[28]    0       [29]    0       [30]    208     [31]    172

[1213] addr:0xa4, instr:0x8d480000
lw r8 r10 0
load D_mem[4]=89 to r8
[0]     0       [1]     0       [2]     0       [3]     0
[4]     0       [5]     0       [6]     0       [7]     0
[8]     89      [9]     64      [10]    16      [11]    4
[12]    4       [13]    377     [14]    610     [15]    1
[16]    16      [17]    100     [18]    0       [19]    0
[20]    0       [21]    0       [22]    0       [23]    0
[24]    0       [25]    0       [26]    0       [27]    0
[28]    0       [29]    0       [30]    208     [31]    172
```

## Usage
```bash
python3 src/MIPS_instr_traverse.py [pattern file] [mode]
```
`pattern file` is the path of the pattern file

`mode` **0** : print all; **1** : print 1 at a time when press enter