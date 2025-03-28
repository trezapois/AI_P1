class State_s:
    def __init__(self,n_odd,n_2,n_4,b,level):
        #self.points = 0
        self.bank = b
        self.n_odd = n_odd
        self.n_2 = n_2
        self.n_4 = n_4
        self.next = []
        self.level = level
        if n_2 + n_odd + n_4 > 0:
            n = self.rm_odd()
            if n != None:
                self.next.append(n)
                
            n = self.rm_2()
            if n != None:
                self.next.append(n)
                
            n = self.rm_4()
            if n != None:
                self.next.append(n)
                
            n = self.split_2()
            if n != None:
                self.next.append(n)
                
            n = self.split_4()
            if n != None:
                self.next.append(n)
                
        
    def rm_odd(self):
        if self.n_odd > 0:
            return State_s(self.n_odd - 1, self.n_2, self.n_4,self.bank,self.level+1)
        return None
    
    def rm_2(self):
        if self.n_2 > 0:
            return State_s(self.n_odd, self.n_2 - 1, self.n_4,self.bank,self.level+1)
        return None
    
    def rm_4(self):
        if self.n_4 > 0:
            return State_s(self.n_odd, self.n_2, self.n_4 - 1,self.bank,self.level+1)
        return None
    
    def split_2(self):
        if self.n_2 > 0:
            return State_s(self.n_odd + 2, self.n_2 - 1, self.n_4, self.bank + 1,self.level+1)
        return None
    
    def split_4(self):
        if self.n_4 > 0:
            return State_s(self.n_odd, self.n_2 + 2, self.n_4 - 1, self.bank,self.level+1)
        return None
    
    def p(self):
        print("--"*self.level + str(self.n_odd) +"-"+ str(self.n_2) +"-"+ str(self.n_4) + "-" + str(self.bank))
        for i in self.next:
            i.p()

A = State_s(0,1,1,0,0)
A.p()
