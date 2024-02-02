import random
import sys
import logging
from rotation_schedule import RotationSchedule, Person
import csv


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

def create_people_db(people_file, last_month_file):
    people_dict ={}
    devs = []


    filename_input = "people.csv"  # Replace with the name of your CSV file
    leader_codes = {}  # Replace with the leader names and their codes

    # Load the CSV file into a list of dictionaries
    with open(filename_input, "r") as file:
        reader = csv.DictReader(file)
        people_list = list(reader)

    # Convert the list of people into a dictionary with codes as keys

    # Load the CSV file into a list of dictionaries
    with open("last_month.csv", "r") as file:
        reader = csv.DictReader(file)
        last_month = list(reader)

    devs = []
    dev_by_name = {}
    mlb_devs = []
    for i, person in enumerate(people_list):
        if not (leader_codes.get(person["leader"]) != None):
            leader_codes[person["leader"]] = chr(len(leader_codes) + 65) # increment letter from quantity of leaders like autoinc
        
        # if it is  mlb the lead should be the same, another alternative is to do leader as a list of leaders
        has_experience = person["has_experience"] == "TRUE" or person["name"] in last_month
        code =  "{:02d}{}{}{}".format(
                i,
                leader_codes[person["leader"]],
                str(i+1),
                ("_" if has_experience else "x")
        )
        people_dict[code] = person
        dev_by_name[person["name"]] = code
        """
            if it is from mlb:
                add once as a single block
                set leader as all leaders from mlb, this should be setted aside
            else should keep the same logic
            
        """
        if person["mlb"] == "TRUE":
            mlb_devs.append(code)
        else:
            devs.append(code)

    print(">>> Before turning mlb_devs into single blocks")
    print(people_dict)

    MAX_MLB_DEVS = 2



    """
    if len(mlb_devs) % 2 != 0:
        #exit
        print("Error: mlb_devs_total is not even")
        exit(1)
    """


    print(">>> MLB debs")
    print(mlb_devs)

    mlb_devs_groups ={} # dev name -> group code
    mlb_group_lead ={} # group code -> leader code

    group_id = 1
    for i in range(len(mlb_devs)):
        
        group_code ="G_{:02d}".format(group_id)
        mlb_devs_groups[mlb_devs[i]] = group_code

        if mlb_group_lead.get(group_code) == None:
            mlb_group_lead[group_code] = [get_boss(mlb_devs[i])]
        else:
            if get_boss(mlb_devs[i]) not in mlb_group_lead[group_code]:
                mlb_group_lead[group_code].append(get_boss(mlb_devs[i]))

        if (i+1) % MAX_MLB_DEVS == 0:
            group_id += 1
        




    print(">>> MLB Blocks")
    print(mlb_devs_groups)
    print(">>> MLB Group Leaders")
    print(mlb_group_lead )



    # add all keys from mlb_group_lead to devs at the end
    devs.extend(list(mlb_group_lead.keys()))


    # delete repeated from devs
    devs = list(dict.fromkeys(devs))

    # add again groups keys to set groups by pairs
    devs.extend(list(mlb_group_lead.keys()))

    return {
        "devs": devs,
        "dev_by_name": dev_by_name,
        "people_dict": people_dict,
        "mlb_devs_groups": mlb_devs_groups,
        "mlb_group_lead": mlb_group_lead,
    }

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