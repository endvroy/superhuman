# SuperHuman
SuperHuman is a enumerative superoptimizer for the game Human Resource Machine

Superoptimization is the process of automatically finding the optimal code sequence for one, loop-free sequence of instructions. While most standard compiler optimizations only improve code partly, a superoptimizer's goal is to find the optimal sequence.

Human Resource Machine is a game where players are asked to write assembly code to complete a given task. The architecture is unconventional, with the following elements:

- one-address code
- only 1 register
- one input stream 
- one output stream
- limited memory
- the instruction set has limited functionality

The game features an optional 'size challenge' and an optional 'speed challenge'. This superoptimizer aims to synthesize program that is correct and beats the size challenge.

"py-version" has the working build. Other failed approaches are in other branches.
