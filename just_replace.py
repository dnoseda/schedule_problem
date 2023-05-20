import random

LAST_MONTH_L=[]

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

def write_solution_to_excel(rota1, rota2, nrota1, nrota2, people_dict):
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment
    from openpyxl.utils import get_column_letter
    
    # Create a new workbook
    workbook = Workbook()
    sheet = workbook.active
    
    sheet['A1'] = "New rotation"    

    sheet['A2'] = "Original:"
    sheet.merge_cells('A2:D2')

    sheet["F2"] = "New:"
    sheet.merge_cells('F2:I2')

    sheet['A3'], sheet['C3'], sheet['F3'], sheet['H3'] = "Rota1", "Rota2", "Rota1", "Rota2"
    sheet.merge_cells('A3:B3')
    sheet.merge_cells('C3:D3')
    sheet.merge_cells('F3:G3')
    sheet.merge_cells('H3:I3')

    for i in ["A","C", "F", "H"]:
        sheet[i+"4"] = "Name"
    for i in ["B","D", "G", "I"]:
        sheet[i+"4"] = "Leader"

    sheet["E4"] = "Is Adjacent?"
    sheet["J4"] = "Is Adjacent?"

    titles=  ["A1","A2", "F2","A3", "C3", "F3","H3","A4","C4", "F4", "H4", "B4","D4", "G4", "I4", "E4", "J4"]       

    offset = 5

    for i in range(max(len(rota1), len(rota2))):
        pos = i + offset
        odevr1, odevr2, ndevr1, ndevr2 = rota1[(i % len(rota1))], rota2[(i % len(rota2))], nrota1[(i % len(nrota1))], nrota2[(i % len(nrota2))]

        sheet["A"+str(pos)] = people_dict[odevr1]["name"]
        if people_dict[odevr1]["has_experience"] == "FALSE":
            sheet["A"+str(pos)].fill = PatternFill(start_color="FFFF00",end_color="FFFF00", fill_type="solid") # yellow
        elif is_in_last_month(odevr1):
            sheet["A"+str(pos)].fill = PatternFill(start_color="CCFFFF",end_color="CCFFFF", fill_type="solid") # light blue

        
        sheet["B"+str(pos)] = people_dict[odevr1]["leader"]

        sheet["C"+str(pos)] = people_dict[odevr2]["name"]
        if people_dict[odevr2]["has_experience"] == "FALSE":
            sheet["C"+str(pos)].fill = PatternFill(start_color="FFFF00",end_color="FFFF00", fill_type="solid") # yellow
        elif is_in_last_month(odevr2):
            sheet["C"+str(pos)].fill = PatternFill(start_color="CCFFFF",end_color="CCFFFF", fill_type="solid") # light blue

        sheet["D"+str(pos)] = people_dict[odevr2]["leader"]
        
        sheet["E"+str(pos)] = "=OR(D{pos}=D{npos},D{pos}=B{npos},B{pos}=B{npos},B{pos}=D{npos})".format(pos=pos,npos=(pos+1))

        ### New:
        sheet["F"+str(pos)] = people_dict[ndevr1]["name"]
        if people_dict[ndevr1]["has_experience"] == "FALSE":
            sheet["F"+str(pos)].fill = PatternFill(start_color="FFFF00",end_color="FFFF00", fill_type="solid") # yellow
        elif is_in_last_month(ndevr1):
            sheet["F"+str(pos)].fill = PatternFill(start_color="CCFFFF",end_color="CCFFFF", fill_type="solid") # light blue

        sheet["G"+str(pos)] = people_dict[ndevr1]["leader"]
    
        sheet["H"+str(pos)] = people_dict[ndevr2]["name"]
        if people_dict[ndevr2]["has_experience"] == "FALSE":
            sheet["H"+str(pos)].fill = PatternFill(start_color="FFFF00",end_color="FFFF00", fill_type="solid") # yellow
        elif is_in_last_month(ndevr2):
            sheet["H"+str(pos)].fill = PatternFill(start_color="CCFFFF",end_color="CCFFFF", fill_type="solid") # light blue

        sheet["I"+str(pos)] = people_dict[ndevr2]["leader"]

        sheet["J"+str(pos)]="=OR(I{pos}=I{npos},I{pos}=G{npos},G{pos}=G{npos},G{pos}=I{npos})".format(pos=pos,npos=(pos+1))
    
    offset += max(len(rota1), len(rota2) )+ 2
    sheet["A"+str(offset)] = "Code list"
    titles.append("A"+str(offset))
    offset +=1    

    for index, key in enumerate(people_dict):  
        pos = index + offset
        sheet["A"+str(pos)] = key
        sheet["B"+str(pos)] = people_dict[key]['name']
        sheet["C"+str(pos)] = people_dict[key]['leader']
    
    offset += len(people_dict) + 2

    sheet["A"+str(offset)] = "Last month"
    titles.append("A"+str(offset))
    offset +=1
    for index, key in enumerate(LAST_MONTH_L):
        pos = index + offset
        sheet["A"+str(pos)] = key
        sheet["B"+str(pos)] = people_dict[key]['name']

    
    for cell in titles:
        sheet[cell].alignment = Alignment(horizontal='center')
        sheet[cell].font = Font(bold=True)
    
    workbook.save("report.xlsx")
    print("Excel file created successfully.")
        


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

def get_success_fitness():
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

        if i <= max_len/2 and (rota1[r1pos] in LAST_MONTH_L or rota2[r2pos] in LAST_MONTH_L):
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
def is_in_last_month(dev):
    return dev in LAST_MONTH_L

def replace_better_pos(rota1, rota2, i):
    offset = random.randint(0, max_len) 
    for j in range(max_len):
        r2pos = (j+i+offset) % len(rota2)
        r1pos = (j+i+offset) % len(rota1)
        if not is_same_boss(rota1[i%len(rota1)], rota2[r2pos]) and not is_adjacent(rota1,rota2,i,j) and not are_both_new(rota1[i%len(rota1)], rota2[r2pos]):
            #replace
            bf = get_success_fitness()
            
            rota1[i%len(rota1)], rota2[r2pos] = rota2[r2pos], rota1[i%len(rota1)]
            af = get_success_fitness()
            if bf >= af:
                #print("Switch : ",rota1[i%len(rota1)], "->", rota2[r2pos], "from", i, "to", r2pos)
                return rota1[i%len(rota1)], rota2[r2pos]
            else: #rollback                
                rota1[i%len(rota1)], rota2[r2pos] = rota2[r2pos], rota1[i%len(rota1)]

        if not is_adjacent(rota1,rota2,i,j) and not are_both_new(rota1[i%len(rota1)], rota2[r2pos]):
            
            bf = get_success_fitness()
            rota1[r1pos], rota1[i%len(rota1)] = rota1[i%len(rota1)], rota1[r1pos]            
            af = get_success_fitness()
            if bf >= af:
                #print("Switch : ",rota1[r1pos], "->", rota1[r1pos], "from", i, "to", r1pos)
                return rota1[i%len(rota1)], rota2[r2pos]
            else: #rollback                
                rota1[r1pos], rota1[i%len(rota1)] = rota1[i%len(rota1)], rota1[r1pos]
        
        
    
    return "",""

import csv

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
    print("iter",j, "rate", get_success_fitness())
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
            continue
        if i <= max_len/2 and is_in_last_month(rota1[r1pos]):
            l1,l2 = replace_better_pos(rota1, rota2, i)
            continue
        if i <= max_len/2 and is_in_last_month(rota2[r2pos]):
            l1,l2 = replace_better_pos(rota1, rota2, i)
            continue
    if get_success_fitness() == 0:
        break

write_solution_to_excel(rota1, rota2,rota1, rota2, people_dict)

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
        people_dict[dev1]["name"],"(.)" if is_in_last_month(dev1) else "",people_dict[dev1]["leader"],
        people_dict[dev2]["name"],"(.)" if is_in_last_month(dev2) else "",people_dict[dev2]["leader"],
        
        ))




