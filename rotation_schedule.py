import logging



class RotationSchedule:
    def __init__(self):
        self.debug = False
        self.rota = []

    def use_dict(self, peopleDict):
        Person.init_dict(peopleDict)       
   
    
    
    def rule_adjacent_bosses(self):
        #TODO check same bosses in mlb block
        ret = 0
        for i in range(self.get_half_point()):
            
            if Person(self.get_rota1_pos(i)).is_same_boss(
                Person(self.get_rota1_pos(i+1))):
                ret += 1
            if Person(self.get_rota2_pos(i)).is_same_boss(
                Person(self.get_rota2_pos(i+1))):
                ret += 1
            if Person(self.get_rota1_pos(i)).is_same_boss(
                Person(self.get_rota2_pos(i+1))):
                ret += 1
            if Person(self.get_rota2_pos(i)).is_same_boss(
                Person(self.get_rota1_pos(i+1))):
                ret += 1
            
            #print(f"Checking {i} {self.get_rota1_pos(i)} {self.get_rota2_pos(i)} {ret}")
        return ret
    
    def rule_same_overlaping_bosses(self):
        ret = 0
        for i in range(self.get_half_point()-1):
            if Person(self.get_rota1_pos(i)).is_same_boss(
                Person(self.get_rota2_pos(i))):
                ret += 1#TODO check same bosses in mlb block
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

        # TODO check not spliting mlb blocks between rotas

        

    
        # Extract the cell blocks to swap
        for i in range(dev_from_size):
            self.remove_cell(from_)
        for i in range(dev_to_size):
            self.insert_cell(from_, dev_to.code)

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
        # TODO implement methods to ask stuff about mlb block
    

class Person:
    people_dict = None
    @classmethod
    def init_dict(cls, people_dict):
        cls.people_dict = people_dict

    def __init__(self, code):
        # exit if no dict
        if not self.__class__.people_dict:
            raise Exception("People dict not initialized")
        self.name = self.__class__.people_dict.get_dev_name(code)
        self.code = code

    def is_mlb_block(self):
        return self.code.startswith("G")
    
    def has_experience(self):
        return not self.code.endswith("x") and not self.is_mlb_block()
    
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()