import random
import sys
import logging
from rotation_schedule import RotationSchedule
from csv_importer import create_people_db
import time

def get_random_pos():
    current_time_ms = int(time.time()*1000)
    random.seed(current_time_ms)
    return random.randint(0, 1000)

def execute_algorithm(s, max_iterations):
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"max_iterations: {max_iterations}")

    for i in range(max_iterations):
        random_position = get_random_pos() % len(s.rota)

        logging.info(random_position)
        if s.fitness() == 0:
            print("Fitness 0 exit")
            break
        for from_pos in range(len(s.rota)):
            if s.fitness() == 0:
                print("Fitness 0 exit")
                break
            for to_pos in range(len(s.rota)):
                if s.fitness() == 0:
                    print("Fitness 0 exit")
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

    peopleDict = create_people_db("people.csv", "last_month.csv","mlb_groups.csv")

    s = RotationSchedule()
    s.rota = peopleDict.devs
    s.use_dict(peopleDict)
    

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

    s.print_schedule()
    print(f"Fitness {s.fitness()}")
    print(",".join(s.rota))

if __name__ == "__main__":
    #catch program interruption
    
    print(f"Called with ${sys.argv}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        
        peopleDict = create_people_db("people.csv", "last_month.csv", "mlb_groups.csv")

        s = RotationSchedule()
        s.rota = peopleDict.devs
        s.use_dict(peopleDict)

        # get rota from argument -R:"
        if len(sys.argv) > 2 and sys.argv[2].startswith("-R:"):
           s.rota = sys.argv[2][3:].split(",")
           
        s.debug=True
        
        s.pretty_print()
        s.print_schedule()
        logging.debug(f"Fitness {s.fitness()}")
        logging.debug(f"Rule Last Month {s.rule_dev_last_month()}")
    else:
        main()