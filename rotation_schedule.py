import logging


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
         