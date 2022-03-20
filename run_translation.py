from mips_simulator import interpreter
import os

files = os.listdir('input')
for file in files:
    with open(os.path.join('input', file)) as f:
        input = f.read()
    output = interpreter.translate(input)
    with open(os.path.join('output', file), 'w') as f:
        f.write(output)
