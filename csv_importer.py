import csv
from rotation_schedule import PeopleDict
from itertools import combinations

def get_boss(code):
    return code[2]
def has_same_boss(pair):
    return get_boss(pair[0]) == get_boss(pair[1])

def arrange(devs):
    all_pairs = list(combinations(devs, 2))

    print(f"All Pairs {len(all_pairs)}")

    disjointed_pairs = []
    for pair in all_pairs:
        if not any(set(pair) & set(disjointed_pair) for disjointed_pair in disjointed_pairs):
            disjointed_pairs.append(pair)

    print(f"Disjointed {len(disjointed_pairs)}")
    
    valid_pairs = [pair for pair in disjointed_pairs if not has_same_boss(pair)]

    print(f"Valid Pairs {len(valid_pairs)}")

    left_over_devs = devs.copy()
    for pair in valid_pairs:
        left_over_devs.remove(pair[0])
        left_over_devs.remove(pair[1])
    
    print(f"Left Over Devs {len(left_over_devs)}\n{left_over_devs}")

    should_insert = False
    temp_pair = []
    for dev in left_over_devs:
        temp_pair.append(dev)
        if should_insert:            
            valid_pairs.append(temp_pair)
            temp_pair = []
        
        should_insert = not should_insert
    

    for idx, pair in enumerate(valid_pairs):
        print(f"Pair: {idx}: {pair}")

    
    return disjointed_pairs

def create_people_db(people_file, last_month_file):
    people_dict ={}
    devs = []



    leader_codes = {}  # Replace with the leader names and their codes

    # Load the CSV file into a list of dictionaries
    with open(people_file, "r") as file:
        reader = csv.DictReader(file)
        people_list = list(reader)

    # Convert the list of people into a dictionary with codes as keys

    # Load the CSV file into a list of dictionaries
    with open(last_month_file, "r") as file:
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

    mlb_devs_arranged_blocks = arrange(mlb_devs)

    mlb_devs_groups ={} # dev code -> group code
    mlb_group_lead ={} # group code -> leader code
    #FIXME should arrange mlb blocks always with 2 leaders, if possible

    for i in range(len(mlb_devs_arranged_blocks)):
        pair = mlb_devs_arranged_blocks[i]
        group_id = i + 1
        group_code ="G_{:02d}".format(group_id)
        mlb_devs_groups[pair[0]] = group_code
        mlb_devs_groups[pair[1]] = group_code

        mlb_group_lead[group_code] = list(set([get_boss(pair[0]),get_boss(pair[1])]))
        
        
        




    print(">>> MLB Blocks")
    print(mlb_devs_groups)
    print(">>> MLB Group Leaders")
    print(mlb_group_lead )


    # delete repeated from devs
    devs = list(dict.fromkeys(devs))

    # add all keys from mlb_group_lead to devs at the end
    for mlb_group_dev in list(mlb_group_lead.keys()):
        devs.append(mlb_group_dev)
        devs.append(mlb_group_dev) # add twice to make rotation blocks of two weeks
    

    return PeopleDict(
        devs,
        dev_by_name,
        people_dict,
        mlb_devs_groups,
        mlb_group_lead,
        leader_codes,
        last_month,
    )

if __name__ == "__main__":
    create_people_db("people.csv", "last_month.csv")