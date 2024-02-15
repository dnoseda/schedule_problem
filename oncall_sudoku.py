import random
import sys
import logging
from rotation_schedule import RotationSchedule, Person
from csv_importer import create_people_db,create_rota_from_file
import time
import argparse

def get_random_pos():
    current_time_ms = int(time.time()*1000)
    random.seed(current_time_ms)
    return random.randint(0, 1000)

def execute_algorithm(s, max_iterations, start_position):
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"max_iterations: {max_iterations}")

    for i in range(max_iterations):
        random_position = get_random_pos() % len(s.rota)

        logging.info(random_position)
        for from_pos in range(len(s.rota)):
            from_pos_with_offset = from_pos + start_position
            for to_pos in range(len(s.rota)):
                if s.fitness() == 0:
                    print("Fitness 0 exit")
                    return
                print(f"[{i:02d}] {from_pos_with_offset:02d} -> {to_pos:02d}: current fitness {s.fitness():03d}")
                to_pos_with_offset = to_pos + random_position
                before_fitness = s.fitness()
                s.stash()
                if s.move_block(from_pos_with_offset, to_pos_with_offset):
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
            if start_position > 0:
                logging.info(f"after replaced: {start_position}")
                break
        if start_position > 0:
                logging.info(f"after replaced: {start_position}")
                break
        

def generate_schedule(args):
    s = RotationSchedule()
    if args.current_rota_file != None:
        print(f"State loaded from {args.current_rota_file}")
        s.load_state(args.current_rota_file)
    else:
        #TODO: Consider current rotation
        peopleDict = create_people_db(args.people_file, args.last_month_file, args.mlb_groups_file)
        
        s.use_dict(peopleDict)
        s.rota = peopleDict.devs
    return s

def main():

    """
        Iterate max times
            Start randon position
            Move block to other position
            MLB blocks can only be moved within rota2
    """

    parser = argparse.ArgumentParser(description='Rearrange on call schedule.')
    parser.add_argument('-f', '--fitness',action="store_true",help='Execute fitness',default=False, required=False)
    parser.add_argument('-R', '--rota', help='Schedule to test in the format {:02d}[A-Z] comma separated', required=False)
    parser.add_argument('-i', '--iterations',type=int, help='Number of iterations', default=1000, required=False)
    parser.add_argument('-p', '--people_file', help='People File', default="people.csv", required=False)
    parser.add_argument('-l', '--last_month_file', help='Last Month File', default="last_month.csv", required=False)
    parser.add_argument('-g', '--mlb_groups_file', help='MLB Groups File', default="mlb_groups.csv", required=False)
    
    # add parameter for the position on where to start the algorithm
    parser.add_argument('-s', '--start_position',type=int, help='Start position', default=0, required=False)

    # add parameter for file to get current rota for minimal adjustment
    parser.add_argument('-r', '--current_rota_file', help='Current Rota File', required=False)
    
    args = parser.parse_args()

    if args.fitness:
        if not args.rota:
            logging.error("Rota is required when using fitness")
            return
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        
        #TODO: Consider current rotation
        peopleDict = create_people_db(args.people_file, args.last_month_file, args.mlb_groups_file,args.current_rota_file)

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
    
    s = generate_schedule(args)

    print(f"generated {s}")
    
    print(f"Rota fitness {s.fitness()} from file: {s.rota}")
        
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        #print(f"\n\nstart_position: {args.start_position} {Person(s.rota[args.start_position]).name}\n\n")
        execute_algorithm(s, args.iterations,args.start_position)
        
    except KeyboardInterrupt:
        print("Program interrupted")    
    
    s.save_state("state.json")
    s.debug=True
    s.pretty_print()
    print("rota {}".format(",".join(s.rota)))
    
    s.peopleDict.pretty_print()
    
    print(f"original devs: {s.peopleDict.devs}")

    print(f"original len devs: {len(s.peopleDict.devs)} len rota: {len(s.rota)} len rota1 {len(s.get_rota1())} len rota2 {len(s.get_rota2())} half point {s.get_half_point()}")
    print(f"len unique devs: {len(set(s.peopleDict.devs))} len unique rota: {len(set(s.rota))}")

    s.print_schedule()
    print(f"Fitness {s.fitness()}")
    print(",".join(s.rota))

if __name__ == "__main__":
    #catch program interruption
    
    print(f"Called with ${sys.argv}")
    
    main()