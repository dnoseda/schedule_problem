import random
import sys
import logging
from rotation_schedule import RotationSchedule
from csv_importer import create_people_db



def execute_algorithm(s, max_iterations):
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"max_iterations: {max_iterations}")

    for i in range(max_iterations):
        random_position = random.randint(0, len(s.rota) - 1)
        logging.info(random_position)
        if s.fitness() == 0:
            break
        for from_pos in range(len(s.rota)):
            if s.fitness() == 0:
                break
            for to_pos in range(len(s.rota)):
                if s.fitness() == 0:
                    break
                logging.info(f"[{i:02d}] {from_pos:02d} -> {to_pos:02d}: current fitness {s.fitness():03d}")
                to_pos_with_offset = to_pos + random_position
                before_fitness = s.fitness()
                s.stash()
                if s.move_block(from_pos, to_pos_with_offset):
                    logging.debug("after move in r2")
                    s.pretty_print()
                    if  before_fitness < s.fitness():
                        s.restore()
                    else:
                        s.commit()
                    logging.debug(s.fitness())
                else:
                    logging.debug("invalid move NOOP")
                    continue

def main():
    # read file of people from csv
    # read file of last month from csv

    # create mlb groups from people file

    # iterate several times to get the best arrangement according to the fitness function
    # each iteration replace blocks and check if fitness improves, rollback if not

    """
        Iterate max times
            Start randon position
            Move block to other position
            MLB blocks can only be moved within rota2
    """

    peopleDict = create_people_db("people.csv", "last_month.csv")

    s = RotationSchedule()
    s.rota = peopleDict.devs
    s.use_dict(peopleDict)
    # TODO set people_db to RotationSchedule

    #          0 , 1 , 2 , 3 , 4  , 5  , 6 , 7
    # s.rota = ["G_00", "64K65_", "50E51_", "67B68_", "58K59x", "55F56_", "66H67_", "30D31_", "33E34_", "36F37x", "38G39x", "48B49_", "60I61_", "41E42x", "46H47_", "56F57x", "53G54_", "37D38x", "49E50_", "52C53x", "59D60_", "65F66_", "54C55_", "57A58x", "32I33_", "23H24x", "43F44x", "68B69_", "34I35_", "47D48_", "13B14_", "12G13_", "29F30x", "04E5_", "03D4_", "G_01", "06C7_", "08F9_", "28E29_", "02C3_", "35G36_", "19D20_", "11A12x", "09C10_", "10D11_", "18H19_", "21F22_", "14A15_", "16G17_", "01B2_", "17F18_", "05E6_", "00A1_", "G_00", "20B21_", "08F9_", "18H19_", "05E6_", "37D38x", "17F18_"]
    #s.rota = ["01A", "02A","03A", "01B","02B", "01C", "02C", "03C", "01D", "02D", "03D", "01E", "02E", "03E","G1A","G2A","G1B","G2B"]

    

    ## repeating N same operation
    ## get random position to start and another random position to move
    ## move block and check if fitness improves
    try:
        execute_algorithm(s, 10000)
    except KeyboardInterrupt:
        print("Program interrupted")    

    s.debug=True
    s.pretty_print()
    print("rota {}".format(",".join(s.rota)))
    # TODO print rota with proper format
    peopleDict.pretty_print()
    
    print(f"original devs: {peopleDict.devs}")

    print(f"original len devs: {len(peopleDict.devs)} len rota: {len(s.rota)} len rota1 {len(s.get_rota1())} len rota2 {len(s.get_rota2())} half point {s.get_half_point()}")
    print(f"len unique devs: {len(set(peopleDict.devs))} len unique rota: {len(set(s.rota))}")

if __name__ == "__main__":
    #catch program interruption
    
    print(f"Called with ${sys.argv}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        s = RotationSchedule()
        # get rota from argument -R:"
        if len(sys.argv) > 2 and sys.argv[2].startswith("-R:"):
           s.rota = sys.argv[2][3:].split(",")
           
        s.debug=True
        s.pretty_print()
        logging.debug(f"Fitness {s.fitness()}")
    else:
        main()