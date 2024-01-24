import random

LAST_MONTH_L=[]


rota1= ["00A1_","01B2_","02B3_","03A4_","04C5_","05C6_","06C7_","07D8_","08D9_","09D10_","10A11_","11A12_","12A13_","13E14_","14B15_","15F16_","16G17_","17G18_","18G19_","19H20_","20H21_","21G22_","22H23_","23H24_","24E25_","49I50x"]
rota2= ["25G26_","26B27_","27I28_","28C29_","29B30x","30D31x","31A32x","32A33x","33H34x","34J35_","35J36_","36E37_","37H38x","38F39_","39G40_","40F41x","41G42_","42F43_","43F44_","44D45_","45D46_","46D47_","47A48x","48H49x","50I51x"]
orota1, orota2 = [],[]
max_len = max(len(rota1), len(rota2))
l1,l2 = "", ""
last_offset = 1


import csv
import functions

people_dict ={}


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

group_id = 0
for i in range(len(mlb_devs)):
    group_code ="G_{:02d}".format(group_id)
    mlb_devs_groups[mlb_devs[i]] = group_code

    if mlb_group_lead.get(group_code) == None:
        mlb_group_lead[group_code] = [get_boss(mlb_devs[i])]
    else:
        if get_boss(mlb_devs[i]) not in mlb_group_lead[group_code]:
            mlb_group_lead[group_code].append(get_boss(mlb_devs[i]))

    if i % MAX_MLB_DEVS % 7 == 0:
        group_id += 1




print(">>> MLB Blocks")
print(mlb_devs_groups)
print(">>> MLB Group Leaders")
print(mlb_group_lead )

# delete all mlb devs from devs
for mlb_dev in mlb_devs:
    devs.remove(mlb_dev)

# add all keys from mlb_group_lead to devs at the end
devs.extend(list(mlb_group_lead.keys()))


# delete repeated from devs
devs = list(dict.fromkeys(devs))

print(">>> After turning mlb_devs into single blocks")
print(devs)

#exit(0)

original_devs_arrange = "-".join(devs)
half_point = int(len(devs)/2)

for lm in last_month:
    LAST_MONTH_L.append(dev_by_name[lm["name"]])

print(LAST_MONTH_L)
rota1, rota2 = devs[:half_point],devs[half_point:]
orota1, orota2 = rota1+[], rota2+[]
max_len = max(len(rota1), len(rota2))

# rota2 is the only one that can have mlb devs

max_repeat = 100000
for j in range(max_repeat):
    print("iter",j, "rate", get_success_fitness(),"adhoc_distance" ,adhoc_distance(rota1+rota2))    
    for i in range(max_len):
        r2pos = i % len(rota2)
        r1pos = i % len(rota1)

        """
            Check if it is mlb dev,
            for mlb dev, the same_boss has to check with 2 sets of leaders
            for mlb dev, it's treated as a single block that can be adjacent to other mlb dev. Consider this in same_boss
        """
        if is_same_boss(rota1[r1pos], rota2[r2pos]):
            l1,l2= replace_better_pos(rota1, rota2, i)
            continue
        if is_adjacent(rota1, rota2, i, i):
            l1,l2= replace_better_pos(rota1, rota2, i)
            continue
        if are_both_new(rota1[r1pos], rota2[r2pos]):
            l1,l2= replace_better_pos(rota1, rota2, i)
            continue
        if i <= max_len/2 and is_in_last_month(rota1[r1pos]):
            l1,l2 = replace_better_pos(rota1, rota2, i)
            continue
        if i <= max_len/2 and is_in_last_month(rota2[r2pos]):
            l1,l2 = replace_better_pos(rota1, rota2, i)
            continue
    if get_success_fitness() == 0:
        break

#write_solution_to_excel(orota1, orota2,rota1, rota2, people_dict)
    
def get_name(dev):
    if is_MLB_group(dev):
        return dev
    return people_dict[dev]["name"]

def get_leader_by_code(code):
    # iterate leader_codes and find the code by value
    for k,v in leader_codes.items():
        if v == code:
            return k

def get_lead(dev):
    ret = ""
    if is_MLB_group(dev):
        for l in mlb_group_lead[dev]:
            ret += get_leader_by_code(l) + ", " # doesnt work, have to get list of leads of mlb_group_lead and then from
        return ret
    return people_dict[dev]["leader"]


print(">>> Leader codes")
print(leader_codes)

for i in range(max_len):
    r2pos = i % len(rota2)    
    r1pos = i % len(rota1)
    dev1 = rota1[r1pos]
    dev2 = rota2[r2pos]
    print("{} ({}) [{}]\t{} ({}) [{}]\t{}\t{}\t{}==\t{}\t\t{}{}\t{}\t{}{}\t{}".format(
        dev1, get_boss(dev1), dev1[-1],
        dev2, get_boss(dev2), dev2[-1],
        is_adjacent(rota1,rota2,i,i),
        is_same_boss(rota1[r1pos], rota2[r2pos]),
        are_both_new(rota1[r1pos], rota2[r2pos]),
        (
            is_adjacent(rota1,rota2,i,i) or
            is_same_boss(rota1[r1pos], rota2[r2pos]) or
            are_both_new(rota1[r1pos], rota2[r2pos])
        ),
        get_name(dev1),"(.)" if is_in_last_month(dev1) else "",get_lead(dev1),
        get_name(dev2),"(.)" if is_in_last_month(dev2) else "",get_lead(dev2),
        
        ))




