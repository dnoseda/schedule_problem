import logging


class RotationSchedule:
    def __init__(self):
        self.debug = False
        self.rota = []

    def use_dict(self, peopleDict):
        Person.init_dict(peopleDict)       
   
    def rule_only_mlb_in_rota2(self):
        ret = 0
        for i in range(self.get_half_point()):
            if Person(self.get_rota1_pos(i)).is_mlb_block():
                ret += 1
        return ret
    
    def rule_adjacent_bosses(self):
        ret = 0
        for i in range(self.get_half_point()-1):
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
        return ret
    
    def rule_same_overlaping_bosses(self):
        ret = 0
        for i in range(self.get_half_point()-1):
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
    
    def fitness(self):
        fns ={
            "check_mlb_groups_rota2": {
                "desc":"Only mlb groups can be in rota2",
                "weight": 5,
                "func": lambda: self.rule_only_mlb_in_rota2()
            },
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

    def move_block2(self, from_,to):
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
            is_rota2_from = from_  >= self.get_half_point()
            if not is_rota2_from:
                logging.error(f"Err from MLB block in rota1, from_ {from_}, rota {self.rota}")
                return False
            dev_from_size = 2
            from_=MLBBlock(from_, self.rota).get_first_cell_pos()

        if dev_to.is_mlb_block():            
            is_rota2_to = to >= self.get_half_point()
            if not is_rota2_to:
                logging.error(f"Err to MLB block in rota1, to {to}, rota {self.rota}")
                return False
            
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

        adjusted_to = to - dev_from_size + dev_to_size
        for i in range(dev_to_size):
            self.remove_cell(adjusted_to)

        for i in range(dev_from_size):
            self.insert_cell(adjusted_to, dev_from.code)

        if len(set(self.rota)) != len(set(original_rota)) or len(self.rota) != len(original_rota):
            logging.error(f"Err len changed {len(set(self.rota))} {len(set(original_rota))} {len(self.rota)} {len(original_rota)}")
            self.debug=True
            logging.error("Rota After:")
            
            self.print_rota_with_pos(from_, to)
            
            self.rota = original_rota

            logging.error("Rota Before:")
            self.print_rota_with_pos(from_,to)
            
            raise Exception(f"Err len changed {from_} {to} {dev_from.code} {dev_to.code}") #FIXME just report this with all parameters and rota state for new test cases, then perform rollback and return False 

        
        
        return True
    
    def move_block(self, from_, to):
        return self.move_block2(from_, to)
        
        """
        Move the whole location. from_ and to are indexes of the rota
        Also use module to get positions
        TODO
        use this 


To add a second length parameter for how many cells should be moved back from the destination position to the origin, we can modify the function accordingly. Here's the updated implementation:


        """
        #print("called with ", from_, to)
        from_ = from_% len(self.rota)
        to = to % len(self.rota)
        if from_ == to:
            #print("Err nop same pos")
            return False    
        is_rota2_from = from_  >= self.get_half_point()
        is_rota2_to = to >= self.get_half_point()


        dev = Person(self.get_code_pos(from_))

        original_rota = self.rota.copy()

        # mlb block should only move in rota2
        if dev.is_mlb_block():
            if not(is_rota2_from and is_rota2_to):
                #print("Err nop mlb and not rota2")
                return False # NOOP
            
            # get first and second pos of the block
            first_cell_pos = from_
            second_cell_pos = from_+1
            
            if self.get_code_pos(second_cell_pos) != dev.code:
                #print("Err NOOP can't move block if second cell is not the same as the first")
                return False # NOOP can't move block if second cell is not the same as the first
            
            dev_to = Person(self.get_code_pos(to))
            if dev_to.is_mlb_block():
                #print("this should be 2 removes and identify first and second pos")
                # detect first and second block of pos to
                to_second_cell_pos = to+1
                if self.get_code_pos(to_second_cell_pos) != dev_to.code:
                    logging.info("Err can't move block if second cell is not the same as the first")
                    return False
                self.remove_cell(first_cell_pos)
                self.remove_cell(first_cell_pos)
                
                adjusted_to = to - 2 # FIXME this is is true onli if to > from_
                
                # FIXME corner cases with adjusted < 0
                
                self.remove_cell(adjusted_to)
                self.remove_cell(adjusted_to)

                self.insert_cell(first_cell_pos, dev_to.code)
                self.insert_cell(first_cell_pos, dev_to.code) # insert second block
                adjusted_to = adjusted_to + 2
                self.insert_cell(adjusted_to, dev.code)
                self.insert_cell(adjusted_to, dev.code) # insert second block
                return True

            ## TODO moind moving block that not turn into rota1
            ## have to do all with shift TODO mind no go more than half point
            # shift should do first remove, then insert

            #print("first_cell_pos")
            #self.print_rota_with_pos(first_cell_pos)
            #print("second_cell_pos")
            #self.print_rota_with_pos(second_cell_pos)

            # 1. remove first block
            self.remove_cell(first_cell_pos)
            #print("removed first cell >>>")
            #self.print_rota_with_pos(first_cell_pos)

            self.remove_cell(first_cell_pos)
            #print("removed second cell >>>")
            #self.print_rota_with_pos(first_cell_pos)
            adjusted_to = to - 2
            #print("adjusted", adjusted_to)
            #self.print_rota_with_pos(adjusted_to)
            
            # 2. insert first block the same place
            self.insert_cell(first_cell_pos, dev_to.code)
            #print("inserted first cell >>>")
            #self.print_rota_with_pos(adjusted_to)
            adjusted_to = adjusted_to + 1
            #print("after adjust")
            #self.print_rota_with_pos(adjusted_to)

            


            # 3. remove second block
            self.remove_cell(adjusted_to ) # TODO what if the removes change positions of to
            #print("removed second cell >>>")
            #self.print_rota_with_pos(adjusted_to)

            # 4. insert second block the same place
            # in reverse order given that insert is before index
            self.insert_cell(adjusted_to, dev.code)
            #print("inserted first cell >>>")
            #self.print_rota_with_pos(adjusted_to)
            
            self.insert_cell(adjusted_to, dev.code)
            #print("inserted second cell >>>")
            self.print_rota_with_pos(adjusted_to)
            
                      
        else:
            dev_to = Person(self.get_code_pos(to))
            if dev_to.is_mlb_block(): # dev
                # detect first cell of the dev_to block
                dev_to_first_cel = to
                if self.get_code_pos(dev_to_first_cel+1) != dev_to.code:
                    if self.get_code_pos(dev_to_first_cel-1) != dev_to.code:
                        raise Exception("Err can't move block if second cell is not the same as the first")
                    dev_to_first_cel = to-1 #FIXME to can be <0
                
                return self.move_block(dev_to_first_cel, from_)
            
                
            
            else: # simpliest scenario
                logging.debug("swapping")
                self.rota[to ], self.rota[from_] = self.rota[from_], self.rota[to] # swap

        if len(set(self.rota)) != len(set(original_rota)):
                logging.error(f"Err nop mlb and not rota2, rollback")
                self.debug=True
                logging.error("Rota After:")
                
                self.print_rota_with_pos(from_, to)
                
                self.rota = original_rota

                logging.error("Rota Before:")
                self.print_rota_with_pos(from_,to)
                
                raise Exception(f"Err nop mlb and not rota2, rollback {from_} {to} {dev.code} {dev_to.code}") 
        

        # if mlb group can only move within rota2
        # mind the size of the block
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



class MLBBlock:
    def __init__(self, mlb_cell,rota):
        self.first_cell_pos = mlb_cell
        self.second_cell_pos = mlb_cell+1
        if self.second_cell_pos >= len(rota) or rota[self.first_cell_pos] != rota[self.second_cell_pos]:
            self.first_cell_pos = mlb_cell-1
            self.second_cell_pos = mlb_cell            
        

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
        return not self.code.endswith("x")
    
    def get_boss_code(self):
        return self.code[2]
    
    def is_same_boss(self, other):
        return self.get_boss_code() == other.get_boss_code() # TODO consider same boss as mlb block
         

class PeopleDict:
    def __init__(self, devs, dev_by_name, people_dict, mlb_devs_groups, mlb_group_lead):         
        self.devs= devs
        self.dev_by_name= dev_by_name
        self.people_dict= people_dict
        self.mlb_devs_groups= mlb_devs_groups
        self.mlb_group_lead= mlb_group_lead
    
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