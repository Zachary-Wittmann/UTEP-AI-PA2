# UTEP-AI-PA2
UTEP AI course programming assignment utilizing Monte Carlo Tree Search for planning/strategic reasoning, utilizing Connect Four as the sample domain.

Usage: python <script> <input_file> <output_mode> <simulations>

Executable: .\main.exe <input_file> <output_mode> <simulations>

UR: .\main.exe test1.txt <Verbose, Brief, None> <int>

PMCGS: .\main.exe test2.txt <Verbose, Brief, None> <int>

UCT: .\main.exe test3.txt <Verbose, Brief, None> <int>

HUMAN V COMPUTER: .\main.exe humantest.txt <None> <int>

TOURNAMENT: .\main.exe test2.txt <None> <0> tournament

HEURISTIC:
If you'd like to run UCT with the priority rollout heuristic, set line 253 to "result = priority_rollout(new_board, player)".