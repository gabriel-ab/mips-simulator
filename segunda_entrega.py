from mips_simulator import simulator, constants
import json
import os

files = os.listdir('input')
for file in files:
    sim = simulator.MipsSimulator()

    with open(os.path.join('input', file)) as f:
        input = json.load(f)
    output = sim(input, debug=True)

    with open(os.path.join('output', file.replace('input', 'grupoG.output')), 'w') as f:
        json.dump(output, f, indent=2)
