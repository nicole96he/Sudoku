import random

class SAT:
    '''
    Purpose: Here, I initial all need information from .cnf file, such as the threshold h,
             all the variables, transfer 111 to number 1.
    Args:
        filename
    Returns:

    '''
    def __init__(self, filename):
        self.h = 0.7   # For me, I set the threshold as 0.8
        self.vars = {}  # I created a dictionary to store variables and their values
        self.key_111 = {}  # This dictionary is used to transfer 111 to 1
        self.key_1 = {}  # This dictionary is used to transfer 1 to 111
        self.model = [] # I created a list called model to store all clauses in number version.

        f = open(filename, "r")  # open file
        var = 0  # This variable is used to represent variables of cnf.
        for line in f:  # loop lines
            change_line = []
            for ele in line.split():
                if ele.startswith('-'):
                    ele = ele.replace('-','')
                    #if ele in self.key_111:
                    change_line.append('-'+str(self.key_111[ele])) # store every component of this line

                else:
                    if ele not in self.key_111:
                        var += 1
                        self.vars[var] = random.getrandbits(1) # choose random value for every variable
                        self.key_111[ele] = var
                        self.key_1[var] = ele

                    #if ele in self.key_111:
                    change_line.append(str(self.key_111[ele]))
            self.model.append(change_line)


    def gsat(self):
        '''
        Purpose: GAST algorithm
        Args:
        Returns: If there is result, return true and change vars dictionary.

        '''
        flip_time = 0
        while not self.stop() and flip_time < 100000: # If the assignment satisfies all the clauses, stop
            flip_time += 1
            pick = random.uniform(0,1) # pick a number between 0 and 1
            if pick > self.h:  # If the number is greater than threshold h
                ran_var = random.choice(list(self.vars.keys()))
                # choose a variable uniformly at random.
                self.vars[ran_var] = not self.vars[ran_var] # flip the variable
                # then go to next loop
            else:  # If the number is smaller than or equal to threshold h
                max_score = 0
                score_var = [] # create a list to store variables with highest score
                for var in self.vars:
                    self.vars[var] = not self.vars[var] # flip the variable

                    cur_score = self.get_score()  # get score
                    if cur_score > max_score:
                        score_var.clear() # clear the list
                        max_score = cur_score
                        score_var.append(var)
                    elif cur_score == max_score:
                        score_var.append(var)
                        # score how many clauses are satisfied when current var is flipped

                    self.vars[var] = not self.vars[var] # flip back the variable

                highest_var = random.choice(score_var)
                # uniformly at random choose one of the variables with highest score
                self.vars[highest_var] = not self.vars[highest_var] # flip back the variable
            print (flip_time)
        return True


    def walksat(self):
        '''
        WALKSAT algorithm
        '''
        flip_time = 0
        while not self.stop() and flip_time < 100000: # most of this is same as gsat algorithm
            flip_time += 1
            pick = random.uniform(0,1)
            if pick > self.h:
                candidate = self.unsatisfied_clauses() #
                ran_line = random.choice(candidate) # randomly choose a clause form candidate
                ran_var = random.choice(ran_line) # randomly choose a variable from line
                if ran_var.startswith('-'):
                    ran_var = int(ran_var.replace('-',''))
                self.vars[int(ran_var)] = not self.vars[int(ran_var)] # flip it
            else:
                max_score = 0
                score_var = []
                candidate = self.unsatisfied_clauses() # store all unsatisfied clauses in this list
                print (len(candidate))
                line = random.choice(candidate)
                for var in line:
                    if var.startswith('-'):
                        var = int(var.replace('-', ''))
                    self.vars[int(var)] = not self.vars[int(var)]
                    cur_score = self.get_score()
                    if cur_score > max_score:
                        score_var.clear()
                        max_score = cur_score
                        score_var.append(var)
                    elif cur_score == max_score:
                        score_var.append(var)
                        # score how many clauses are satisfied when current var is flipped

                    self.vars[int(var)] = not self.vars[int(var)] # flip back the variable

                highest_var = random.choice(score_var)
                self.vars[int(highest_var)] = not self.vars[int(highest_var)]

        return True



    def stop(self):# This is used to check if the assignment satisfies all the clauses
        result = True
        for line in self.model:
            line_result = False
            for var in line:
                if var.startswith('-'):
                    var = var.replace('-','')
                    line_result = (line_result or (not self.vars[int(var)]))
                else:
                    line_result = (line_result or self.vars[int(var)])
            if line_result == False:
                return False
            result = (result and line_result)
            if result == False:
                return False

        return  True

    def get_score(self): # get how many clauses would be satisfied.
        count = 0
        for line in self.model:
            line_result = False
            for var in line:
                if var.startswith('-'):
                    var = var.replace('-','')
                    line_result = (line_result or (not self.vars[int(var)]))
                else:
                    line_result = line_result or self.vars[int(var)]
            if line_result:
                count += 1
        return count

    def write_solution(self,filename): # write the solution into a file

        f = open(filename, "w")
        for var in self.vars:
            if self.vars[var]:
                s = self.key_1[var]
            else:
                s = '-' + self.key_1[var]
            f.writelines(s+"\n")
        f.close()

    def unsatisfied_clauses(self): # get unsatisfied clauses
        candidate = [] # create a list to store candidates
        for line in self.model:
            line_result = False
            for var in line:
                if var.startswith('-'):
                    var = var.replace('-','')
                    line_result = (line_result or (not self.vars[int(var)]))
                else:
                    line_result = line_result or self.vars[int(var)]
            if not line_result:
                candidate.append(line)
        return candidate










