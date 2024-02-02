# schedule_problem

2 rotations, several teams with bosses. Each boss can't have adjacent week.

# Next:
- [x] ~~Manhattan difference~~levenshtein distance 
- [x] Init state
- [ ] Dynamic numbers. Set, middle. Randomness
- [ ] Package managment. One file for individual, function to check boss and experience, another file for fitness, another file for evo algorithm, another to feed the inputs
- [ ] Feed configuration from csv or xml right from opsgenie
- [x] Colours
- [ ] Create dict from names and bosess in csv
- [ ] Log to csv every fitness value in order to play around with the values


# Output with 46 devs:

```
473.4961931705475 --> start gen 999
Original: 1e-07
Rota 1 -> ['A1', 'A2', 'A3x', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5x', 'B6', 'C1x', 'C2', 'C3', 'C4', 'C5', 'C6', 'D1', 'D2', 'D3', 'D4x', 'D5', 'D6']
Rota 2 -> ['E1', 'E2', 'E3x', 'E4', 'E5', 'E6', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'G1', 'G2x', 'G3', 'G4', 'G5', 'G6', 'H1', 'H2', 'H3x', 'H4x', 'H5', 'H6']
Solution found with score. 0.011111111111111112
Rota 1 -> ['B5x', 'E5', 'H3x', 'G4', 'C2', 'E6', 'B4', 'F2', 'H1', 'E3x', 'D4x', 'A4', 'B1', 'F3', 'D1', 'B2', 'D6', 'G5', 'H6', 'B3', 'A3x', 'C6', 'G3', 'D5']
Rota 2 -> ['H2', 'D2', 'C5', 'H4x', 'E1', 'A2', 'F6', 'G2x', 'F5', 'G1', 'F1', 'H5', 'G6', 'C4', 'A6', 'E4', 'A5', 'C1x', 'E2', 'C3', 'F4', 'D3', 'B6', 'A1']

```

# Can be called with arguments to check fitness function
```
python3 replace_mlb.py -f -R:01C,03E,02D,02A,01B,02E,01D,03C,03A,03D,01A,02B,01E,02C,G1A,G2A,G1B,G2B
```
