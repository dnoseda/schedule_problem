import random
import logging
import sys

class RotationSchedule:
    def __init__(self):
        self.debug = False
        self.rota = []    
   
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
    
    def fitness(self):
        fns ={
            "check_mlb_groups_rota2": {
                "desc":"Only mlb groups can be in rota2",
                "weight": 1,
                "func": lambda: self.rule_only_mlb_in_rota2()
            },
            "check_same_adjacent_bosses":{
                "desc":"check if there are no two people with the same boss in the same rota",
                "weight": 1,
                "func": lambda: self.rule_adjacent_bosses()
            },
            "check_same_overlaping_bosses":{
                "desc":"check if there are no two people with the same boss in the same rota",
                "weight": 1,
                "func": lambda: self.rule_same_overlaping_bosses()
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
        return len(self.rota)//2
    
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
                rota2_person = Person(self.get_rota2_pos(self.get_half_point()+i))

                logging.info(f"{rota1_person.code}\t{rota1_person.name}\t{rota2_person.code}\t{rota2_person.name}")

    
    def get_code_pos(self, pos):
        return self.rota[pos%len(self.rota)]
    
    def insert_cell(self, pos, code):
        self.rota.insert(pos, code)

    def remove_cell(self, pos):
        self.rota.pop(pos)

    def print_rota_with_pos(self,pos):
        for i in range(len(self.rota)):
            pos_marker = "*" if i == pos else ""
            print(f"{i}\t{self.rota[i]}", pos_marker )
    
    def move_block(self, from_, to):
        """
        Move the whole location. from_ and to are indexes of the rota
        Also use module to get positions
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
                return False #TODO FIXME this should be 2 removes and identify first and second pos

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
                logging.error("Err nop mlb and not rota2")
                return False # TODO consider limits and scenarios
            
            else: # simpliest scenario
                logging.debug("swapping")
                self.rota[to ], self.rota[from_] = self.rota[from_], self.rota[to] # swap
            
        

        # if mlb group can only move within rota2
        # mind the size of the block
        return True
    def stash(self):
        self.stash_copy = self.rota.copy()
    def restore(self):
        self.rota = self.stash_copy.copy()
        self.stash_copy = None
    def commit(self):
        self.stash_copy = None

class Person:
    def __init__(self, code):
        self.name = "WIP" # TODO get from dict
        self.code = code
    def is_mlb_block(self):
        return self.code.startswith("G")
    
    def has_experience(self):
        #ends with x
        return self.code.endswith("x")
    
    def get_boss_code(self):
        return self.code[2]
    
    def is_same_boss(self, other):
        return self.get_boss_code() == other.get_boss_code() # TODO consider same boss as mlb block
         

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

    s = RotationSchedule()

    #          0 , 1 , 2 , 3 , 4  , 5  , 6 , 7
    # s.rota = ["G_00", "64K65_", "50E51_", "67B68_", "58K59x", "55F56_", "66H67_", "30D31_", "33E34_", "36F37x", "38G39x", "48B49_", "60I61_", "41E42x", "46H47_", "56F57x", "53G54_", "37D38x", "49E50_", "52C53x", "59D60_", "65F66_", "54C55_", "57A58x", "32I33_", "23H24x", "43F44x", "68B69_", "34I35_", "47D48_", "13B14_", "12G13_", "29F30x", "04E5_", "03D4_", "G_01", "06C7_", "08F9_", "28E29_", "02C3_", "35G36_", "19D20_", "11A12x", "09C10_", "10D11_", "18H19_", "21F22_", "14A15_", "16G17_", "01B2_", "17F18_", "05E6_", "00A1_", "G_00", "20B21_", "08F9_", "18H19_", "05E6_", "37D38x", "17F18_"]
    s.rota = ["01A", "02A","03A", "01B","02B", "01C", "02C", "03C", "01D", "02D", "03D", "01E", "02E", "03E","G1A","G2A","G1B","G2B"]

   

    ## repeating N same operation
    ## get random position to start and another random position to move
    ## move block and check if fitness improves

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