class State_s:
    def __init__(self,n_odd,n_2,n_4,b,p,level):
        self.bank = b
        self.p = p
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
            return State_s(self.n_odd - 1, self.n_2, self.n_4,self.bank,self.p+1,self.level+1)
        return None
    
    """def rm_3(self):
        if self.n_odd > 0:
            return State_s(self.n_odd - 1, self.n_2, self.n_4,self.bank,self.p+3,self.level+1)
        return None"""
    
    def rm_2(self):
        if self.n_2 > 0:
            return State_s(self.n_odd, self.n_2 - 1, self.n_4,self.bank,self.p+2,self.level+1)
        return None
    
    def rm_4(self):
        if self.n_4 > 0:
            return State_s(self.n_odd, self.n_2, self.n_4 - 1,self.bank,self.p+4,self.level+1)
        return None
    
    def split_2(self):
        if self.n_2 > 0:
            return State_s(self.n_odd + 2, self.n_2 - 1, self.n_4, self.bank + 1, self.p,self.level+1)
        return None
    
    def split_4(self):
        if self.n_4 > 0:
            return State_s(self.n_odd, self.n_2 + 2, self.n_4 - 1, self.bank,self.p+2,self.level+1)
        return None
    
    def pri(self):
        print("--"*self.level + str(self.n_odd) +"-"+ str(self.n_2) +"-"+ str(self.n_4) + "-" + str(self.bank))
        for i in self.next:
            i.pri()
            
            
    def Minimax(self):
        #Maximizer goes first
        if self.n_2 + self.n_4 == 0:
            return 1-(self.bank%2 + (self.p+self.n_odd)%2)
        if self.level%2 == 0:
            #Maximizer turn
            res = -1
            for i in self.next:
                temp = i.Minimax()
                #if temp == 1:
                #    return 1
                if temp > res:
                    res = temp
            return res
        else:
            #Minimizer
            res = 1
            for i in self.next:
                temp = i.Minimax()
                #if temp == -1:
                #    return -1
                if temp < res:
                    res = temp
            return res
        
    def AlphaBeta(self,alpha = -2,beta = 2):
        if self.n_2 + self.n_4 == 0:
            return 1-(self.bank%2 + (self.p+self.n_odd)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in self.next:
                temp = i.AlphaBeta(alpha,beta)
                val = max(val,temp)
                alpha = max(alpha,val)
                if alpha >= beta:
                    break
            return val    
        else:
            #Maximizer turn
            val = 2
            for i in self.next:
                temp = i.AlphaBeta(alpha,beta)
                val = min(val,temp)
                alpha = min(beta,val)
                if alpha >= beta:
                    break
            return val    
            
            
    
                
            

A = State_s(0,2,2,1,0,0)
#A.pri()
#print(A.Minimax())
print(A.AlphaBeta())
# Ma