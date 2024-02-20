import logging
import json



class RotationSchedule:
    def __init__(self):
        self.debug = False
        self.rota = []
        self.peopleDict = None

    def use_dict(self, peopleDict):
        self.peopleDict = peopleDict
        Person.init_dict(peopleDict)
        

    def save_state(self, filename):
        state = {
            "rota": self.rota,
            "peopleDict": self.peopleDict
        }
        with open(filename, 'w') as f:
            f.write(json.dumps(state, cls=PersonEncoder, indent=4))
    
    def load_state(self, filename):
        with open(filename, 'r') as f:
            state = json.loads(f.read())
            
            self.rota = state["rota"]
            
            self.peopleDict = PeopleDict.from_dict(state["peopleDict"])
            print(f"State: {self.peopleDict}")
            Person.init_dict(self.peopleDict)
    
    
    def rule_adjacent_bosses(self):
        #TODO check same bosses in mlb block
        ret = 0
        for i in range(self.get_half_point()):
            #print(f"Checking {i} R1 {self.get_rota1_pos(i)} Next R1 {self.get_rota1_pos(i+1)} R2 {self.get_rota2_pos(i)} Next R2 {self.get_rota2_pos(i+1)}")

            dev_rota1 = Person(self.get_rota1_pos(i))
            next_dev_rota1 = Person(self.get_rota1_pos(i+1))
            dev_rota2 = Person(self.get_rota2_pos(i))
            next_dev_rota2 = Person(self.get_rota2_pos(i+1))

            
            if dev_rota1.is_same_boss(
                next_dev_rota1):
                ret += 1

            if dev_rota2.is_same_boss(
                next_dev_rota2):
                ret += 1

            if dev_rota1.is_same_boss(
                next_dev_rota2):
                ret += 1

            if dev_rota2.is_same_boss(
                next_dev_rota1):
                ret += 1
            
            
        return ret
    
    def rule_same_overlaping_bosses(self):
        ret = 0
        for i in range(self.get_half_point()):
            #print(f"Checking {i} {self.get_rota1_pos(i)} {self.get_rota2_pos(i)}")
            if Person(self.get_rota1_pos(i)).is_same_boss(
                Person(self.get_rota2_pos(i))):
                ret += 1
        return ret

    def rule_experience(self):
        ret = 0
        for i in range(self.get_half_point()-1):
            if not Person(self.get_rota1_pos(i)).has_experience() and not Person(self.get_rota2_pos(i)).has_experience():
                ret += 1

        return ret
    
    def rule_dev_last_month(self):
        #iterate from half of half point to half point
        ret = 0
        from_pos = 0
        to_pos = self.get_half_point()//2
        #print(f"Checking from {from_pos} to {to_pos}")
        for i in range(from_pos, to_pos):
            #print(f"Checking {i} {self.get_rota1_pos(i)} {self.get_rota2_pos(i)}")
            if Person(self.get_rota1_pos(i)).is_in_last_month():
                ret += 1
            if Person(self.get_rota2_pos(i)).is_in_last_month():
                ret += 1
        return ret
    
    def fitness(self):
        fns ={           
            "check_same_adjacent_bosses":{
                "desc":"check if there are no two people with the same boss in the same rota",
                "weight": 4,
                "func": lambda: self.rule_adjacent_bosses()
            },
            "check_same_overlaping_bosses":{
                "desc":"check if there are no two people with the same boss in the same rota",
                "weight": 4,
                "func": lambda: self.rule_same_overlaping_bosses()
            },
            "check_experience":{
                "desc":"check if there are no two people without experience in the same rota",
                "weight": 6,
                "func": lambda: self.rule_experience()            
            },
            "check_last_month":{
                "desc":"check if there are no two people without experience in the same rota",
                "weight": 10,
                "func": lambda: self.rule_dev_last_month()              
            }            
        }
        f = 0
        for k,v in fns.items():
            ret = v["func"]()
            logging.debug(f"Running {k} {v['desc']}, ret {ret}")
            if ret > 0:
                f += v["weight"]*ret
        return f
    
    def get_half_point(self):
        return max(len(self.get_rota1()), len(self.get_rota2()))
    
    def get_rota1(self):
        return self.rota[:len(self.rota)//2]
    
    def get_rota2(self):
        return self.rota[len(self.rota)//2:]
    
   
    def __str__(self) -> str:
        return str(self.rota)
    
    def get_rota2_pos(self, pos):
        return self.get_rota2()[pos % len(self.get_rota2())]
    
    def get_rota1_pos(self, pos):
        return self.get_rota1()[pos % len(self.get_rota1())]
    
    def pretty_print(self):
        if self.debug:
            logging.info("Rota 1\t\tRota 2")
            logging.info("-------\t\t-------")
            for i in range(self.get_half_point()): # TODO: half point should consider max
                
                rota1_person = Person(self.get_rota1_pos(i))
                rota2_person = Person(self.get_rota2_pos(i))

                logging.info(f"{rota1_person.code}\t{rota1_person.name}\t{rota2_person.code}\t{rota2_person.name}")

    def get_code_pos(self, pos):
        return self.rota[pos%len(self.rota)]
    
    def insert_cell(self, pos, code):
        self.rota.insert(pos, code)

    def remove_cell(self, pos):
        self.rota.pop(pos)

    def print_rota_with_pos(self,*args):
        if not self.debug:
            return

        for i in range(len(self.rota)):
            pos_marker = ""
            
            for idx,j in enumerate(args):
                if i == j:
                    pos_marker = "<"*(idx+1)
                    break
            
            logging.info(f"{i}\t{self.rota[i]} {pos_marker}")

    def move_block(self, from_,to):
        """
        but with this consideration:
        - detect if from or to are mlb blocks
        - then detect first cell of the blocks
        - then run if need 2 to 1 or 1 to 2 or 2 to 2 or 1 to 1 alwyas detecting first cell of the blocks
        """

        from_ = from_% len(self.rota)
        to = to % len(self.rota)

        
        
        dev_from = Person(self.get_code_pos(from_))
        dev_to = Person(self.get_code_pos(to))

        dev_from_size = 1
        dev_to_size = 1

        if dev_from.is_mlb_block():
            dev_from_size = 2
            from_=MLBBlock(from_, self.rota).get_first_cell_pos()

        if dev_to.is_mlb_block():            
            dev_to_size = 2
            to=MLBBlock(to, self.rota).get_first_cell_pos()

        
        if from_ == to:
            #print("Err nop same pos")
            return False
    
        original_rota = self.rota.copy()

        # Extract the cell blocks to swap
        for i in range(dev_from_size):
            self.remove_cell(from_)
        for i in range(dev_to_size):
            self.insert_cell(from_, dev_to.code)

        adjusted_to = to
        if to >from_:
            adjusted_to = to - dev_from_size + dev_to_size

        for i in range(dev_to_size):
            self.remove_cell(adjusted_to)

        for i in range(dev_from_size):
            self.insert_cell(adjusted_to, dev_from.code)

        if len(set(self.rota)) != len(set(original_rota)) or len(self.rota) != len(original_rota):
            
            self.rota = original_rota
            logging.error("Len changed!!! To check in a test {} and {} from: {} to: {} ".format(
                ",".join(self.get_rota1()),
                ",".join(self.get_rota2()),
                from_,
                to ))

            return False

        for idx, dev in enumerate(self.rota):
            if Person(dev).is_mlb_block():
                if not MLBBlock(idx, self.rota).is_valid():
                    self.rota = original_rota
                    logging.error("MLB block not valid!!! To check in a test {} and {} from: {} to: {} ".format(
                        ",".join(self.get_rota1()),
                        ",".join(self.get_rota2()),
                        from_,
                        to ))
                    return False

        
        
        return True
    

       
    
    def stash(self):
        self.stash_copy = self.rota.copy()
    def restore(self):
        if self.stash_copy is None:
            raise Exception("No stash to restore")
        self.rota = self.stash_copy.copy()
        self.stash_copy = None
    def commit(self):
        self.stash_copy = None

    def print_schedule(self):
        data = []
        data.append([""    , ""   , "Rota1", ""     ,"",""    ,"Rota2"])
        data.append(["Week","Code","Dev"   ,"leader","","Code","Dev","leader"])
        for i in range(self.get_half_point()):
            dev1,dev2 = Person(self.get_rota1_pos(i)), Person(self.get_rota2_pos(i))
            if dev1.is_mlb_block():
                dev1,dev2=dev2,dev1
            data.append([
                str(i+1),
                dev1.code,
                dev1.name + (" (LM)" if dev1.is_in_last_month() else "") + (" (X)" if not dev1.has_experience() else ""),
                dev1.get_bosses_name(),
                "",
                dev2.code,
                dev2.name + (" (LM)" if dev2.is_in_last_month() else "") + (" (X)" if not dev2.has_experience() else ""),
                dev2.get_bosses_name()
            ])
        
        for i in range(len(data)):
            print("\t".join(data[i]))
            



class MLBBlock:    
    def __init__(self, mlb_cell,rota):
        self.first_cell_pos = mlb_cell
        self.second_cell_pos = mlb_cell+1
        self.rota = rota
        if self.second_cell_pos >= len(rota) or rota[self.first_cell_pos] != rota[self.second_cell_pos]:
            self.first_cell_pos = mlb_cell-1
            self.second_cell_pos = mlb_cell            
        
    def is_valid(self):
        widhin_range = self.first_cell_pos < len(self.rota) and self.second_cell_pos < len(self.rota)
        if not widhin_range:
            return False
        
        not_negative = self.first_cell_pos >= 0 and self.second_cell_pos >= 0
        if not not_negative:
            return False
        
        return self.rota[self.first_cell_pos] == self.rota[self.second_cell_pos]
        

    def get_first_cell_pos(self):
        return self.first_cell_pos

    def get_second_cell_pos(self):
        return self.second_cell_pos
        

class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PeopleDict):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

class Person:
    people_dict = None
    @classmethod
    def init_dict(cls, people_dict):
        cls.people_dict = people_dict

    def __init__(self, code):
        # exit if no dict
        if not self.__class__.people_dict:
            raise Exception("People dict not initialized")
        
        # check if self.__class__.people_dict is a PeopleDict instance, if not convert it
        if not isinstance(self.__class__.people_dict, PeopleDict):
            raise Exception(f"People dict is wrong type {type(self.__class__.people_dict)}")
        
        self.name = self.__class__.people_dict.get_dev_name(code)
        self.code = code

    def is_mlb_block(self):
        return self.code.startswith("G")
    
    def has_experience(self):
        if self.is_in_last_month():
            return True
        if self.is_mlb_block():
            return False
        return self.code.endswith("x")
    
    def get_boss_code(self):
        return self.code[2]
    
    def get_bosses(self):
        if not self.is_mlb_block():
            return [self.get_boss_code()]
        
        return self.__class__.people_dict.mlb_group_lead[self.code]
    def get_leader_by_code(self, code):
        # iterate leader_codes and find the code by value
        for k,v in self.__class__.people_dict.leader_codes.items():
            if v == code:
                return k
    
    def get_bosses_name(self):
        return ", ".join([self.get_leader_by_code(boss) for boss in self.get_bosses()])
    
    def is_same_boss(self, other):
        # if is same mlb block return false
        if self.is_mlb_block() and self.code == other.code:
            return False
        
        my_boss = self.get_bosses()
        others_boss = other.get_bosses()
        # return true if any of my bosses is in others bosses
        return any(boss in others_boss for boss in my_boss)
    
    def is_in_last_month(self):
        for i in range(len(self.__class__.people_dict.last_month)):
            if self.name == self.__class__.people_dict.last_month[i]["name"]:
                return True
        return False
         

class PeopleDict:
    def __init__(self, devs, dev_by_name, people_dict, mlb_devs_groups, mlb_group_lead,leader_codes,last_month):         
        self.devs= devs
        self.dev_by_name= dev_by_name
        self.people_dict= people_dict
        self.mlb_devs_groups= mlb_devs_groups
        self.mlb_group_lead= mlb_group_lead
        self.leader_codes=leader_codes
        self.last_month=last_month

    @classmethod
    def from_dict(cls, d):
        return PeopleDict(
                d["devs"],
                d["dev_by_name"],
                d["people_dict"],
                d["mlb_devs_groups"],
                d["mlb_group_lead"],
                d["leader_codes"],
                d["last_month"],
            )
    
    def to_json(self):
        obj = {
            "devs": self.devs,
            "dev_by_name": self.dev_by_name,
            "people_dict": self.people_dict,
            "mlb_devs_groups": self.mlb_devs_groups,
            "mlb_group_lead": self.mlb_group_lead,
            "leader_codes": self.leader_codes,
            "last_month": self.last_month
        }
        return json.dumps(obj)
    
    def is_mlb_block(self, code):
        return code.startswith("G")
    
    def get_dev_name(self, code):
        if self.is_mlb_block(code):         
            
            if not code in self.mlb_devs_groups.values():
                raise Exception(f"MLB group {code} not found")
            
            ret = f"{code}: "
            names = []
            for k,v in self.mlb_devs_groups.items():
                if v == code:
                    names.append(self.people_dict[k]["name"])
            ret += ", ".join(names)
            return ret
        else:
            return self.people_dict[code]["name"]
    
    def pretty_print(self):
        logging.info("Code\tName")
        logging.info("-------\t-------")
        for k, v in self.people_dict.items():
            logging.info(f"{k}\t{v}")
        
        logging.info("MLB Groups")
        logging.info("-------")
        for k, v in self.mlb_devs_groups.items():
            logging.info(f"{k}\t{v}")

        logging.info("MLB Group Lead")
        logging.info("-------")
        for k, v in self.mlb_group_lead.items():
            logging.info(f"{k}\t{v}")
        
        logging.info("People by name")
        logging.info("-------")
        for k, v in self.dev_by_name.items():
            logging.info(f"{k}\t{v}")

        logging.info("Last Month")
        logging.info("-------")
        for k in self.last_month:
            logging.info(f"{k}")

import unittest
from unittest.mock import Mock

class TestRotationSchedule(unittest.TestCase):
    
    
    def _run_test(self, rota1, rota2, from_, to, expected_rota):
        rs = RotationSchedule()
        rs.rota = rota1 +rota2
        
        mock_people_dict = Mock(spec=PeopleDict)
        # Mock the get_dev_name method
        mock_people_dict.get_dev_name.return_value = "wip"

        rs.use_dict(mock_people_dict)
        rs.debug = True
        rs.print_rota_with_pos(from_,to)
        print("Before move block")
        rs.pretty_print()
        self.assertTrue(rs.move_block(from_, to))
        print("After move block")
        rs.pretty_print()
        self.assertEqual(rs.rota, expected_rota)
    
    def test_move_single_to_single(self):
        self._run_test(
            ['01A','02A','03A'],
            ['G_01A','G_01A','01B'],
            0,2,
            ['03A','02A','01A','G_01A','G_01A','01B'])
    
    def test_move_single_to_block_first_cell(self):
        self._run_test(
            ['01A','02A','03A'],
            ['01B','G_01A','G_01A'],
            3,4,
            ['01A','02A','03A'] +
            ['G_01A','G_01A','01B']
        )
    
    def test_move_single_to_block_second_cell(self):
        self._run_test(
            ['01A','02A','03A'],
            ['01B','G_01A','G_01A'],
            3,5,
            ['01A','02A','03A'] +
            ['G_01A','G_01A','01B']
        )

    
    def test_move_block_to_single(self):        
        self._run_test(
            ['01A','02A','03A'],
            ['G_01A','G_01A','01B'],
            3,5,
            ['01A','02A','03A','01B','G_01A','G_01A'])        
    
    def test_move_block_to_block(self):
        self._run_test(
            ['01A','02A','03A','04A','05A','06A'],
            ['G_01A','G_01A','01B','G_02A','G_02A','02B'],
            6,9,
            ['01A','02A','03A','04A','05A','06A','G_02A','G_02A','01B','G_01A','G_01A','02B'],
        )
    
    def test_move_upper_single_to_lower_block(self):
        self._run_test(
            ["49F50_","36D37_","40F41_","41I42x","14B15x","06F7x","09A10x","34I35_","13A14_","G_06","G_06","04D5_","02C3x","39G40_","53B54_","15E16x","50A51x","25G26_","17H18_","07G8_","32F33_","31B32_","19A20_","51H52_","45E46_","18D19_","24J25x","11G12_","33J34_","22E23_","42G43_","29A30_","26E27_","30G31_"],
            ["12I13_","00A1x","01B2_","48H49_","05E6_","44J45_","10C11_","35H36_","37B38_","38H39_","27A28_","28G29x","43E44_","08H9_","23D24x","47G48_","16B17_","20F21_","G_01","G_01","46H47_","G_03","G_03","21J22x","G_02","G_02","52A53_","G_04","G_04","03A4x","G_05","G_05","G_07","G_07"],
            21,
            9,
            ["49F50_","36D37_","40F41_","41I42x","14B15x","06F7x","09A10x","34I35_","13A14_","31B32_","04D5_","02C3x","39G40_","53B54_","15E16x","50A51x","25G26_","17H18_","07G8_","32F33_","G_06","G_06","19A20_","51H52_","45E46_","18D19_","24J25x","11G12_","33J34_","22E23_","42G43_","29A30_","26E27_","30G31_","12I13_","00A1x","01B2_","48H49_","05E6_","44J45_","10C11_","35H36_","37B38_","38H39_","27A28_","28G29x","43E44_","08H9_","23D24x","47G48_","16B17_","20F21_","G_01","G_01","46H47_","G_03","G_03","21J22x","G_02","G_02","52A53_","G_04","G_04","03A4x","G_05","G_05","G_07","G_07"]
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()