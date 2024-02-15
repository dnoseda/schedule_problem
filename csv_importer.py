import csv
from rotation_schedule import PeopleDict
from itertools import combinations

def get_boss(code):
    return code[2]

def create_rota_from_file(rota_file):
    rota = []
    with open(rota_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rota.append(row["code"])
    return rota

def create_people_db(people_file, last_month_file, mlb_groups_file):
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
    
    with open(mlb_groups_file, "r") as file:
        reader = csv.DictReader(file)
        mlb_groups = list(reader)

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

    mlb_devs_arranged_blocks = []

    mlb_devs_groups ={} # dev code -> group code
    mlb_group_lead ={} # group code -> leader code

    for i in range(len(mlb_groups)):
        pair = [dev_by_name[mlb_groups[i]["dev1"]], dev_by_name[mlb_groups[i]["dev2"]]]
        group_id = mlb_groups[i]["group"]

        group_code ="G_{:02d}".format(int(group_id))
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
    create_people_db("people.csv", "last_month.csv","mlb_groups.csv")