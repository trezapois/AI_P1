class State:
    def __init__(self,s):
        self.points = 0
        self.s = s
        self.len = len(s)
        self.bank = 0
        
    def Revert(self,points,s,bank):
        self.points = points
        self.s = s
        self.len = len(s)
        self.bank = bank
        
    def Progress(self,index,take):
        if index >= self.len:
            return False
        if take:
            self.points += int(self.s[index])
            self.s = self.s[:index] + self.s[index + 1:]            
            self.len -=1
            return True
        elif self.s[index] == '2':
            """self.s = self.s[:index] + "11" + self.s[index + 1:]
            self.len += 1"""
            self.s = self.s[:index] + self.s[index + 1:]
            self.len -= 1;         
            self.points += 2
            self.bank += 1
            return True
        elif self.s[index] == '4':
            self.s = self.s[:index] + "22" + self.s[index + 1:]
            self.bank += 2
            self.len += 1
            return True
        else:
            return False
        
    def Next_states(self):
        p = self.points
        b = self.bank
        s0 = self.s
        for i in range(self.len):
            if self.Progress(i,True):
                print(str(self.points) + "  " + self.s + "  " + str(self.bank))
                if self.len != 0:
                    self.Next_states()
                self.Revert(p,s0,b)         
            if self.Progress(i,False):
                print(str(self.points) + "  " + self.s + "  " + str(self.bank))
                self.Next_states()
                self.Revert(p,s0,b)  
        return     
         
#3, 1 change nature(even/odd) of the score

A = State(4,"24",0)
A.Next_states()