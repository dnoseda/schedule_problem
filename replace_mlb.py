import random
import sys
import logging
from rotation_schedule import RotationSchedule, Person



def execute_algorithm(s, max_iterations):
    max_repeat = 100
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"max_repeat: {max_repeat}")

    for i in range(max_repeat):
        random_position = random.randint(0, len(s.rota) - 1)
        logging.info(random_position)
        for from_pos in range(len(s.rota)):
            for to_pos in range(len(s.rota)):
                logging.info("{} -> {}: current fitness {}".format(from_pos, to_pos, s.fitness()))
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
    
    s.debug=True
    s.pretty_print()
    print("rota {}".format(",".join(s.rota)))



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

    #people_db = create_people_db("people.csv", "last_month.csv")

    s = RotationSchedule()

    #          0 , 1 , 2 , 3 , 4  , 5  , 6 , 7
    # s.rota = ["G_00", "64K65_", "50E51_", "67B68_", "58K59x", "55F56_", "66H67_", "30D31_", "33E34_", "36F37x", "38G39x", "48B49_", "60I61_", "41E42x", "46H47_", "56F57x", "53G54_", "37D38x", "49E50_", "52C53x", "59D60_", "65F66_", "54C55_", "57A58x", "32I33_", "23H24x", "43F44x", "68B69_", "34I35_", "47D48_", "13B14_", "12G13_", "29F30x", "04E5_", "03D4_", "G_01", "06C7_", "08F9_", "28E29_", "02C3_", "35G36_", "19D20_", "11A12x", "09C10_", "10D11_", "18H19_", "21F22_", "14A15_", "16G17_", "01B2_", "17F18_", "05E6_", "00A1_", "G_00", "20B21_", "08F9_", "18H19_", "05E6_", "37D38x", "17F18_"]
    s.rota = ["01A", "02A","03A", "01B","02B", "01C", "02C", "03C", "01D", "02D", "03D", "01E", "02E", "03E","G1A","G2A","G1B","G2B"]

    

    ## repeating N same operation
    ## get random position to start and another random position to move
    ## move block and check if fitness improves

    execute_algorithm(s, 1000)

if __name__ == "__main__":
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