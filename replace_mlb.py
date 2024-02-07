import random
import sys
import logging
from rotation_schedule import RotationSchedule
from csv_importer import create_people_db
import time
import argparse

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

    """
        Iterate max times
            Start randon position
            Move block to other position
            MLB blocks can only be moved within rota2
    """

    parser = argparse.ArgumentParser(description='Rearrange on call schedule.')
    parser.add_argument('-f', '--fitness', action="store_true",help='Execute fitness', required=False)
    parser.add_argument('-R', '--rota', help='Schedule to test in the format {:02d}[A-Z] comma separated', required=False)
    parser.add_argument('-i', '--iterations',type=int, help='Number of iterations', default=1000, required=False)
    parser.add_argument('-p', '--people_file', help='People File', default="people.csv", required=False)
    parser.add_argument('-l', '--last_month_file', help='Last Month File', default="last_month.csv", required=False)
    parser.add_argument('-g', '--mlb_groups_file', help='MLB Groups File', default="mlb_groups.csv", required=False)
    args = parser.parse_args()

    if args.fitness:
        if not args.rota:
            logging.error("Rota is required when using fitness")
            return
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        
        peopleDict = create_people_db(args.people_file, args.last_month_file, args.mlb_groups_file)

        s = RotationSchedule()
        s.rota = peopleDict.devs
        s.use_dict(peopleDict)

        # get rota from argument -R:"
        
        s.rota = args.rota.split(",")
           
        s.debug=True
        
        s.pretty_print()
        s.print_schedule()
        logging.debug(f"Fitness {s.fitness()}")
        logging.debug(f"Rule Last Month {s.rule_dev_last_month()}")
        return
    # read file of people from csv
    # read file of last month from csv

    # create mlb groups from people file

    # iterate several times to get the best arrangement according to the fitness function
    # each iteration replace blocks and check if fitness improves, rollback if not

    

    peopleDict = create_people_db(args.people_file, args.last_month_file, args.mlb_groups_file)

    s = RotationSchedule()
    s.rota = peopleDict.devs
    s.use_dict(peopleDict)
    

    ## repeating N same operation
    ## get random position to start and another random position to move
    ## move block and check if fitness improves

    try:
        execute_algorithm(s, args.iterations)
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
    
    main()