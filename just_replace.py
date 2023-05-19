import random

class Color:
    # Define color codes
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def colorize_string(text, color):
    # Colorize the given string with the specified color
    return color + text + Color.RESET


rota1= ["00A1_","01B2_","02B3_","03A4_","04C5_","05C6_","06C7_","07D8_","08D9_","09D10_","10A11_","11A12_","12A13_","13E14_","14B15_","15F16_","16G17_","17G18_","18G19_","19H20_","20H21_","21G22_","22H23_","23H24_","24E25_","49I50x"]
rota2= ["25G26_","26B27_","27I28_","28C29_","29B30x","30D31x","31A32x","32A33x","33H34x","34J35_","35J36_","36E37_","37H38x","38F39_","39G40_","40F41x","41G42_","42F43_","43F44_","44D45_","45D46_","46D47_","47A48x","48H49x","50I51x"]
max_len = max(len(rota1), len(rota2))
l1,l2 = "", ""

def printstage():
    print("*\nRota1:")
    for dev in rota1:
        s = colorize_string(dev, Color.GREEN) if l1 == dev else (colorize_string(dev, Color.BLUE) if l2 == dev else dev)
        print(s, ",", end="")
    print("\nRota2:")
    for dev in rota2:
        s = colorize_string(dev, Color.GREEN) if l1 == dev else (colorize_string(dev, Color.BLUE) if l2 == dev else dev)
        print(s, ",", end="")
    print("")

def its_all_ok():
    r = 0
    for i in range(max_len):
        r2pos = i % len(rota2)    
        r1pos = i % len(rota1)
        dev1 = rota1[r1pos]
        dev2 = rota2[r2pos]
        if is_adjacent(rota1,rota2,i,i):
            r +=1
        if is_same_boss(rota1[r1pos], rota2[r2pos]):
            r +=1
        if are_both_new(rota1[r1pos], rota2[r2pos]):
            r +=1
    
    return r

def get_boss(cel):
    return cel[2]

def is_new(cel):
    return cel[-1:] == "x"

def is_adjacent(rota1, rota2, i, j):
  
    a1, a2 = get_boss(rota1[i % len(rota1)]), get_boss(rota1[(j+1)%len(rota1)])
    b1, b2 = get_boss(rota2[i % len(rota2)]), get_boss(rota2[(j+1)%len(rota2)])

    if a1 in [a2, b2]:
        return True            
    
    if b1 in [b2, a2]:
        return True

    return False

def is_same_boss(dev1, dev2):
    return get_boss(dev1) == get_boss(dev2)
def are_both_new(dev1,dev2):
    return is_new(dev1) and is_new(dev2)

def replace_better_pos(rota1, rota2, i):
    offset = random.randint(0, max_len) 
    for j in range(max_len):
        r2pos = (j+i+offset) % len(rota2)
        r1pos = (j+i+offset) % len(rota1)
        if not is_same_boss(rota1[i], rota2[r2pos]) and not is_adjacent(rota1,rota2,i,j) and not are_both_new(rota1[i], rota2[r2pos]):
            #replace
            bf = its_all_ok()
            
            rota1[i], rota2[r2pos] = rota2[r2pos], rota1[i]
            af = its_all_ok()
            if bf >= af:
                #print("Switch : ",rota1[i], "->", rota2[r2pos], "from", i, "to", r2pos)
                return rota1[i], rota2[r2pos]
            else: #rollback                
                rota1[i], rota2[r2pos] = rota2[r2pos], rota1[i]

        if not is_adjacent(rota1,rota2,i,j) and not are_both_new(rota1[i], rota2[r2pos]):
            
            bf = its_all_ok()
            rota1[r1pos], rota1[i] = rota1[i], rota1[r1pos]            
            af = its_all_ok()
            if bf >= af:
                #print("Switch : ",rota1[r1pos], "->", rota1[r1pos], "from", i, "to", r1pos)
                return rota1[i], rota2[r2pos]
            else: #rollback                
                rota1[r1pos], rota1[i] = rota1[i], rota1[r1pos]
    
    return "",""

import csv

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
for i, person in enumerate(people_list):
    if not (leader_codes.get(person["leader"]) != None):
        leader_codes[person["leader"]] = chr(len(leader_codes) + 65)
    has_experience = person["has_experience"] == "TRUE" or person["name"] in last_month
    code =  "{:02d}{}{}{}".format(
            i,
            leader_codes[person["leader"]],
            str(i+1),
            ("_" if has_experience else "x")
    )
    people_dict[code] = person
    dev_by_name[person["name"]] = code
    devs.append(code)

print(people_dict)

original_devs_arrange = "-".join(devs)
half_point = int(len(devs)/2)

for lm in last_month:
    LAST_MONTH_L.append(dev_by_name[lm["name"]])

print(LAST_MONTH_L)
rota1, rota2 = devs[:half_point],devs[half_point:]
max_len = max(len(rota1), len(rota2))

max_repeat = 10000
for j in range(max_repeat):
    print("iter",j, "rate", its_all_ok())
    for i in range(max_len):
        #printstage()
        r2pos = i % len(rota2)
        r1pos = i % len(rota1)
        if is_same_boss(rota1[r1pos], rota2[r2pos]):
            l1,l2= replace_better_pos(rota1, rota2, i)
            continue
        if is_adjacent(rota1, rota2, i, i):
            l1,l2= replace_better_pos(rota1, rota2, i)
            continue
        if are_both_new(rota1[r1pos], rota2[r2pos]):
            l1,l2= replace_better_pos(rota1, rota2, i)
    if its_all_ok() == 0:
        break


for i in range(max_len):
    r2pos = i % len(rota2)    
    r1pos = i % len(rota1)
    dev1 = rota1[r1pos]
    dev2 = rota2[r2pos]
    print("{} ({}) [{}]\t{} ({}) [{}]\t{}\t{}\t{}==\t{}\t\t{}\t{}\t{}\t{}".format(
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
        people_dict[dev1]["name"],people_dict[dev1]["leader"],
        people_dict[dev2]["name"],people_dict[dev2]["leader"]
        ))


# TODO: falta levantar la info de un file
# TODO: mandar a excel
# TODO: considerar last_month