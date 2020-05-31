# First thoughts
The VM is provided with a file `code.bin` this file has a lot of emojis. My first thought was that every emoji stands for an instruction.

# Reversing
The following will exploin every emoji and what instruction it executes. I reversed everything with ghidras decompiler.
## 💀-Instruction
This instruction is very easyas it just calls `exit(-1)` so the program terminates when reached.

## 💪-Instruction
When looking at this instruction inside the file it is clear that this instruction is followed by six number emojis.
Inside the vm it is clear that the six number emojis get read and the value they correspong to gets used as pairs.

First the first 2 numbers get read and then the first number is set as the exponent and the second as the base. The result gets added to the output variable and the wohole thing gets repeated for the other 2 pairs.

For example `💪1️⃣0️⃣2️⃣4️⃣7️⃣2️⃣` gets translated to pow(0,1)+pow(4,2)+pow(2,7)=0x90.

The result gets saved into a vm stack.

## ✏️-Instruction
Like the symbol implies this instruction writes, it writes to the console from the input file. It pops the first 2 values from the vm stack and uses the second value as the offset from the file beginning and the first value as the size. This Text gets then written to the console.

## 📖-Instruction
This instruction is like the ✏️-Instruction very obvious it waits for user input. It pops 2 values from the vm stack. The first value is the size of the expected user input and the second value is the file descriptor.

The input gets saved to a variable.

## 🦾-Instruction
Similar to the 💪-Instruction six numbers get read and get calculated together. The result gets used as an index. From the previous saved variable (a string) the index's char gets added to the top of the vm stack.

## 🔀-Instruction
This instrcution pops 2 values from the vm stack and then xors them together and writes the result back into the vm stack.

## ✅-Instruction
This instrcution pops 2 values from the vm stack and then ors them together and writes the result back into the vm stack.

## 🤔-Instruction
This instruction is a conditional jump. It first reads similar to the 💪-Instruction it's values and then pop a value from the vm stack. This value gets checkked if it is 0. If that is the case then the vm jumpsthe number of calculated bytes. If it isn't true nothing happens.

## 🌠-Instruction
Similar to the 💪-Instruction six numbers get read and get calculated together. The result gets used as an index. From the previous saved variable (a string) the index's char and the 4 next get added to the top of the vm stack as one value.

## ‼️-Instruction
This instruction pops a value from the vm stack and pushes it 2 times onto it. So bascically it copies the value from the top of the stack.

## ➕-Instruction
This instruction pops a value from the vm stack and does an bitwise and operation with 0x1 on it. The result gets pushed back onto the stack.

## ➡️-Instruction
This instruction reads the six numbers similar to the 💪-Instruction and does a bitwise and with the value and 0x1f. Then it pops a value from the vm stack and shifts it the calculate value times to the right, This value gets pushed to the vm stack.

# Solve
After I understood what each instruction does I could read the `code.bin` file.

```
💪1️⃣0️⃣2️⃣4️⃣7️⃣2️⃣💪0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣✏️
```
This will output data from the file at offset 0x90. The size of the outputed data is 0x17. Which corresonds to `Welcome to eVMoji 😎`.

```
💪1️⃣3️⃣2️⃣6️⃣7️⃣2️⃣💪0️⃣0️⃣1️⃣3️⃣2️⃣4️⃣✏️
```

This will output data from the file at offset 0xa7. The size of the outputed data is 0x14. Which corresonds to `🤝 me the 🏳️`.

```
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣💪0️⃣0️⃣0️⃣0️⃣2️⃣5️⃣📖
```

This will read 0x1b charchetrs from the concole input.

```
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x0
💪0️⃣0️⃣2️⃣5️⃣3️⃣6️⃣    0xf2    🦾1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    offset=0x0  🔀
💪0️⃣0️⃣3️⃣3️⃣7️⃣2️⃣    0x9c    🔀✅
💪1️⃣2️⃣2️⃣4️⃣3️⃣6️⃣    0xea    🦾0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    offset=0x1  🔀
💪0️⃣0️⃣1️⃣0️⃣3️⃣6️⃣    0xd9    🔀✅
💪0️⃣0️⃣0️⃣0️⃣7️⃣2️⃣    0x82    🦾0️⃣0️⃣0️⃣0️⃣1️⃣0️⃣    offset=0x2  🔀
💪0️⃣0️⃣0️⃣0️⃣5️⃣3️⃣    0xf5    🔀✅
💪0️⃣0️⃣1️⃣4️⃣2️⃣7️⃣    0x36    🦾0️⃣0️⃣0️⃣0️⃣0️⃣0️⃣    offset=0x3  🔀
💪1️⃣5️⃣2️⃣6️⃣2️⃣8️⃣    0x69    🔀✅
💪0️⃣0️⃣2️⃣4️⃣3️⃣5️⃣    0x8e    🦾0️⃣0️⃣0️⃣0️⃣1️⃣2️⃣    offset=0x4  🔀
💪1️⃣7️⃣2️⃣4️⃣3️⃣6️⃣    0xef    🔀✅
💪0️⃣0️⃣0️⃣0️⃣2️⃣4️⃣    0x12    🦾0️⃣0️⃣0️⃣0️⃣1️⃣3️⃣    offset=0x5  🔀
💪1️⃣0️⃣2️⃣6️⃣2️⃣9️⃣    0x75    🔀✅
💪0️⃣0️⃣1️⃣7️⃣2️⃣4️⃣    0x18    🦾0️⃣0️⃣0️⃣0️⃣1️⃣4️⃣    offset=0x6  🔀
💪0️⃣0️⃣1️⃣6️⃣2️⃣6️⃣    0x2b    🔀✅
💪1️⃣2️⃣2️⃣7️⃣2️⃣8️⃣    0x73    🦾0️⃣0️⃣0️⃣0️⃣1️⃣5️⃣    offset=0x7  🔀
💪0️⃣0️⃣1️⃣7️⃣2️⃣6️⃣    0x2c    🔀✅
💪1️⃣6️⃣2️⃣6️⃣2️⃣9️⃣    0x7b    🦾0️⃣0️⃣0️⃣0️⃣1️⃣6️⃣    offset=0x8  🔀
💪0️⃣0️⃣1️⃣3️⃣1️⃣9️⃣    0xd     🔀✅
💪0️⃣0️⃣1️⃣0️⃣2️⃣4️⃣    0x11    🦾0️⃣0️⃣0️⃣0️⃣1️⃣7️⃣    offset=0x9  🔀
💪0️⃣0️⃣1️⃣4️⃣3️⃣3️⃣    0x20    🔀✅
💪0️⃣0️⃣1️⃣9️⃣2️⃣9️⃣    0x5b    🦾0️⃣0️⃣0️⃣0️⃣1️⃣8️⃣    offset=0xa  🔀
💪0️⃣0️⃣1️⃣4️⃣2️⃣6️⃣    0x29    🔀✅
💪1️⃣5️⃣2️⃣6️⃣2️⃣8️⃣    0x69    🦾0️⃣0️⃣0️⃣0️⃣1️⃣9️⃣    offset=0xb  🔀
💪0️⃣0️⃣0️⃣0️⃣3️⃣3️⃣    0x1d    🔀✅
💪0️⃣0️⃣1️⃣6️⃣2️⃣7️⃣    0x38    🦾0️⃣0️⃣1️⃣2️⃣1️⃣9️⃣    offset=0xc  🔀
💪0️⃣0️⃣2️⃣7️⃣3️⃣3️⃣    0x4d    🔀✅
💪0️⃣0️⃣1️⃣9️⃣7️⃣2️⃣    0x8a    🦾0️⃣0️⃣1️⃣3️⃣1️⃣9️⃣    offset=0xd  🔀
💪0️⃣0️⃣2️⃣8️⃣3️⃣5️⃣    0xbe    🔀✅
💪1️⃣2️⃣2️⃣7️⃣3️⃣5️⃣    0xb0    🦾0️⃣0️⃣1️⃣4️⃣1️⃣9️⃣    offset=0xe  🔀
💪0️⃣0️⃣1️⃣3️⃣3️⃣6️⃣    0xdc    🔀✅
💪1️⃣2️⃣1️⃣9️⃣7️⃣2️⃣    0x8b    🦾0️⃣0️⃣1️⃣5️⃣1️⃣9️⃣    offset=0xf  🔀
💪0️⃣0️⃣1️⃣9️⃣3️⃣6️⃣    0xe2    🔀✅
💪0️⃣0️⃣2️⃣4️⃣3️⃣5️⃣    0x8e    🦾0️⃣0️⃣1️⃣6️⃣1️⃣9️⃣    offset=0x10 🔀
💪0️⃣0️⃣1️⃣0️⃣5️⃣3️⃣    0xf4    🔀✅
💪0️⃣0️⃣1️⃣2️⃣7️⃣2️⃣    0x83    🦾0️⃣0️⃣1️⃣0️⃣2️⃣4️⃣    offset=0x11 🔀
💪1️⃣6️⃣2️⃣7️⃣7️⃣2️⃣    0xb7    🔀✅
💪0️⃣0️⃣1️⃣2️⃣5️⃣3️⃣    0xf6    🦾0️⃣0️⃣0️⃣0️⃣2️⃣4️⃣    offset=0x12 🔀
💪0️⃣0️⃣0️⃣0️⃣7️⃣2️⃣    0x82    🔀✅
💪1️⃣4️⃣2️⃣8️⃣7️⃣2️⃣    0xc4    🦾0️⃣0️⃣1️⃣2️⃣2️⃣4️⃣    offset=0x13 🔀
💪0️⃣0️⃣0️⃣0️⃣5️⃣3️⃣    0xf5    🔀✅
💪0️⃣0️⃣1️⃣7️⃣2️⃣7️⃣    0x39    🦾0️⃣0️⃣1️⃣3️⃣2️⃣4️⃣    offset=0x14 🔀
💪0️⃣0️⃣1️⃣4️⃣2️⃣9️⃣    0x56    🔀✅
💪0️⃣0️⃣0️⃣0️⃣5️⃣3️⃣    0xf5    🦾0️⃣0️⃣1️⃣4️⃣2️⃣4️⃣    offset=0x15 🔀
💪1️⃣0️⃣3️⃣3️⃣7️⃣2️⃣    0x9b    🔀✅
💪0️⃣0️⃣2️⃣6️⃣3️⃣5️⃣    0xa2    🦾0️⃣0️⃣1️⃣5️⃣2️⃣4️⃣    offset=0x16 🔀
💪0️⃣0️⃣1️⃣9️⃣5️⃣3️⃣    0xfd    🔀✅
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x0 🤔1️⃣2️⃣2️⃣6️⃣2️⃣8️⃣    jump=0x66
💪2️⃣5️⃣2️⃣9️⃣2️⃣9️⃣    offset=0xbb
💪0️⃣0️⃣1️⃣8️⃣2️⃣4️⃣    size=0x19   ✏️💀
```

This is the next code section I commented it a bit with the values. I could see that the conditional jump at the end should jump so the program doesn't exit.
The first 0x17 charachters get xored with a number and the result gets xored with a diffrent number (x^i)^y. Then the result gets ored with the result from the previous charachter or 0 at the beginning. Basically I want the result of the xors to always be 0. Luckily (x^i)^y con be transposed to be x^y=i. I wrote a little python script which would do this for me.
```python
compBytes1 = bytearray(b'\xf2\xea\x82\x36\x8e\x12\x18\x73\x7b\x11\x5b\x69\x38\x8a\xb0\x8b\x8e\x83\xf6\xc4\x39\xf5\xa2')
compBytes2 = bytearray(b'\x9c\xd9\xf5\x69\xef\x75\x2b\x2c\x0d\x20\x29\x1d\x4d\xbe\xdc\xe2\xf4\xb7\x82\xf5\x56\x9b\xfd')

for i in range(0,len(compBytes1)):
    print(chr(compBytes1[i]^compBytes2[i]), end='')
```

The result is `n3w_ag3_v1rtu4liz4t1on_` that's the first part of the flag. Now for the second part

```
🌠1️⃣3️⃣1️⃣9️⃣7️⃣2️⃣    0x8c    ‼️   ➕  🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣    0x17    ➡️1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    shift=0x0   ➕  🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣    jump=0xec   ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x1 🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣    0x80    🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x0
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x0 🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣    0x30    ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    shift=0x1   ‼️   ➕  🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣    0x17    ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    shift=0x1   ➕  🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣    jump=0xec   ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    shift=0x1   ‼️   ➕  🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣    0x17    ➡️0️⃣0️⃣0️⃣0️⃣1️⃣0️⃣    shift=0x2   ➕  🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣    jump=0xec   ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    shift=0x1   ‼️   ➕  🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣    0x17    ➡️0️⃣0️⃣0️⃣0️⃣0️⃣0️⃣    shift=0x3   ➕  🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣    jump=0xec   ➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣2️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣3️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣5️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣6️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣7️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣8️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣2️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣3️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣4️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣5️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣6️⃣1️⃣9️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣0️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣2️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣3️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣4️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣5️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣7️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣8️⃣2️⃣4️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣0️⃣2️⃣5️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣2️⃣5️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣0️⃣3️⃣3️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣0️⃣0️⃣3️⃣3️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣2️⃣3️⃣3️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣‼️➕🌠0️⃣0️⃣1️⃣6️⃣2️⃣4️⃣➡️0️⃣0️⃣1️⃣3️⃣3️⃣3️⃣➕🤔1️⃣4️⃣2️⃣4️⃣3️⃣6️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣2️⃣3️⃣5️⃣🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🤔1️⃣0️⃣2️⃣4️⃣5️⃣2️⃣➡️0️⃣0️⃣1️⃣0️⃣1️⃣0️⃣🌠0️⃣0️⃣1️⃣7️⃣7️⃣2️⃣    0x88    🔀
💪1️⃣0️⃣1️⃣0️⃣1️⃣0️⃣    0x0 🤔1️⃣2️⃣2️⃣6️⃣2️⃣8️⃣    0x66
```

This code cycles through multiple xors with the rest of the input (4 bytes). I bruteforced this part but I later found out that this is just crc32 and could be reversed within seconds. The result is `l0l?`. But nevertheless here is my bruteforce code.

```c
#include <stdio.h>
#include <stdbool.h>
#include <pthread.h>

bool result = false;
long x = 0xffffffff;
pthread_mutex_t lock;

long test2 = 0xedb88320;
long test3 = 0xf40e845e;

bool func(long input){
	long test = 0xffffffff;

    long inp = input;

    int i;

    for (i = 0; i < 32; ++i)
    {
        if((inp & 0x1) == (test & 0x1)){
            //printf("%i\n", i);
            test = test >> 0x1;
        }
        else
        {
            test = (test >> 0x1) ^ test2;
        }    

        inp = inp >> 1; 
    }

    if (test == test3)
    {
        return true;
    }else
    {
        return false;
    }
    
}

void *mainFunc(void *vargp)
{
    while (!result)
    {
        pthread_mutex_lock(&lock);
        long input = x;
        x=x-1;
        pthread_mutex_unlock(&lock);

        printf("0x%08x\n", input);
        if (func(input))
        {
            printf("0x%08x\n HUUUUURAAAA\n", input);
            result = true;
        }
    }
}

int main()
{
    if (pthread_mutex_init(&lock, NULL) != 0)
    {
        printf("\n mutex init failed\n");
        return 1;
    }

    pthread_t tid; 
    int i;
    for (i = 0; i < 24; i++) 
    {
        pthread_create(&tid, NULL, mainFunc, NULL); 
    }
    

    pthread_exit(NULL);
    pthread_mutex_destroy(&lock);

    return 0;
}

```

# Prevention
The problem here isn't that the vm could be reversed. The problem is the password comparision it would be much safer if the password would be stored as a cryptographic hash and the input would be hashed the same way. The two hashed strings can now be compared and it wouldn't be possible (in a stort time) to get the password from the hash.