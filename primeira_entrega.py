from mips_simulator import interpreter
import json
import os

files = os.listdir('input')
for file in files:
    with open(os.path.join('input', file)) as f:
        input = json.load(f)

    translated = list(map(str, interpreter.decode(input['text'])))
    hex_lines = input['text']

    output = [
        {
            'hex': h_line, 
            'text': t_line,
            'mem': {},
            'regs': {},
            'stdout': ''
        }
        for h_line, t_line in zip(hex_lines, translated)
    ]

    with open(os.path.join('output', file.replace('input', 'grupoG.output')), 'w') as f:
        json.dump(output, f, indent=True)
