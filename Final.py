class State_s:
    def __init__(self,n_odd,n_2,n_4,b,p,level):
        self.bank = b
        self.p = p
        self.n_odd = n_odd
        self.n_2 = n_2
        self.n_4 = n_4
        self.level = level
        self.next = []
        self.hVal = None

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
    
    def generate_next_states(self,stop = -1):
        if self.n_2 + self.n_odd + self.n_4 > 0 and stop != 0:
            n = self.rm_odd()
            if n != None:
                n.generate_next_states(stop - 1)
                self.next.append(n)
                
                
            n = self.rm_2()
            if n != None:
                n.generate_next_states(stop - 1)
                self.next.append(n)
                
            n = self.rm_4()
            if n != None:
                n.generate_next_states(stop - 1)
                self.next.append(n)
                
            n = self.split_2()
            if n != None:
                n.generate_next_states(stop - 1)
                self.next.append(n)
                
            n = self.split_4()
            if n != None:
                n.generate_next_states(stop - 1)
                self.next.append(n)
        else:
            self.hVal = self.heuristic()
    
                
    def advance(self,n):
        if n == 0:
            return self.rm_odd()
        if n == 1:
            return self.rm_2()
        if n == 2:
            return self.rm_4()
        if n == 3:
            return self.split_2()
        if n == 4:
            return self.split_4()
        

    
    def Minimax(self,n_ply = 2):
        if self.n_2 + self.n_4 + self.n_odd == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.Minimax(n_ply - 1)
                    else:
                        temp = next.heuristic()
                    val = max(val,temp)
                    if val == 1:
                        return 1
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.Minimax(n_ply - 1)
                    else:
                        temp = next.heuristic()
                    val = min(val,temp)
                    if val == -1:
                        return -1
            return val        
    
        
    """
    def AlphaBeta(self,alpha = -2,beta = 2):
        if self.n_2 + self.n_4 + self.n_odd == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if len(self.next) == 0:
            return self.hVal
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    temp = next.AlphaBeta(alpha,beta)
                    val = max(val,temp)
                    if val == 1:
                        return 1
                    alpha = max(alpha,val)
                    if alpha >= beta:
                        break
            self.hVal = val
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    temp = next.AlphaBeta(alpha,beta)
                    val = min(val,temp)
                    if val == -1:
                        return -1
                    beta = min(beta,val)
                    if alpha >= beta:
                        break
            self.hVal = val
            return val    
"""
    
    
    def AlphaBeta(self,alpha = -2,beta = 2):
        if self.n_2 + self.n_4 + self.n_odd == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    #if n_ply > 0:
                    temp = next.AlphaBeta()
                    #else:
                    #    temp = next.heuristic()
                    val = max(val,temp)
                    if val == 1:
                        return 1
                    alpha = max(alpha,val)
                    if alpha >= beta:
                        break
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(5):
                next = self.advance(i)
                if next is not None:
                    #if n_ply > 0:
                    temp = next.AlphaBeta()
                    #else:
                        #temp = next.heuristic()
                    val = min(val,temp)
                    if val == -1:
                        return -1
                    beta = min(beta,val)
                    if alpha >= beta:
                        break
            return val       

    def heuristic(self):
        x = 0
        if self.bank%2 == 0:
            if(self.n_2 + self.n_4 + self.bank%2) == 1:
                x += 1
            if(self.n_odd)%2 == 0 and (self.n_2 + self.n_4) >= 2:
                x += 1
            return 1-((self.bank+self.n_2+self.n_4 + x)%2 + (self.p+self.n_odd)%2)
        else:
            if(self.n_odd)%2 == 1 and (self.n_2 + self.n_4) >= 2:
                x += 1
            if(self.n_4 == 1 & self.n_odd%2 == 1):
                x+=1
            return 1-((self.bank+self.n_2+self.n_4 + x)%2 + (self.p+self.n_odd)%2)
            
    
"""for i in range(2):
    for j in range(4):
        for k in range(4):
            A = State_s(i,j,k,1,0,0)
            #A.generate_next_states()
            print("1"*i + "2"*j +"4"*k + " : " + str(A.AlphaBeta()) + " | " + str(A.heuristic()))
            """

A = State_s(1,0,1,1,0,0)
print(A.AlphaBeta())
print(A.heuristic())