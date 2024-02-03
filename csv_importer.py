import csv

def get_boss(code):
    return code[2]

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


    # delete repeated from devs
    devs = list(dict.fromkeys(devs))

    # add all keys from mlb_group_lead to devs at the end
    for mlb_group_dev in list(mlb_group_lead.keys()):
        devs.append(mlb_group_dev)
        devs.append(mlb_group_dev) # add twice to make rotation blocks of two weeks
    

    return {
        "devs": devs,
        "dev_by_name": dev_by_name,
        "people_dict": people_dict,
        "mlb_devs_groups": mlb_devs_groups,
        "mlb_group_lead": mlb_group_lead,
    }

if __name__ == "__main__":
    create_people_db("people.csv", "last_month.csv")