class State_s:
    def __init__(self,n_1,n_3,n_2,n_4,b,p,level):
        self.bank = b
        self.p = p
        self.n_1 = n_1
        self.n_3 = n_3
        self.n_2 = n_2
        self.n_4 = n_4
        self.level = level
        self.next = []
        self.hVal = None
        

    def rm_1(self):
        if self.n_1 > 0:
            return State_s(self.n_1 - 1,self.n_3, self.n_2, self.n_4,self.bank,self.p+1,self.level+1)
        return None
    
    def rm_3(self):
        if self.n_3 > 0:
            return State_s(self.n_1,self.n_3 - 1, self.n_2, self.n_4,self.bank,self.p+3,self.level+1)
        return None
    
    def rm_2(self):
        if self.n_2 > 0:
            return State_s(self.n_1, self.n_3, self.n_2 - 1, self.n_4,self.bank,self.p+2,self.level+1)
        return None
    
    def rm_4(self):
        if self.n_4 > 0:
            return State_s(self.n_1, self.n_3, self.n_2, self.n_4 - 1,self.bank,self.p+4,self.level+1)
        return None
    
    def split_2(self):
        if self.n_2 > 0:
            return State_s(self.n_1+2, self.n_3, self.n_2 - 1, self.n_4, self.bank + 1, self.p,self.level+1)
        return None
    
    def split_4(self):
        if self.n_4 > 0:
            return State_s(self.n_1, self.n_3, self.n_2 + 2, self.n_4 - 1, self.bank,self.p+2,self.level+1)
        return None 
    
    def generate_next_states(self,stop = -1):
        if self.n_2 + self.n_1 + self.n_3 + self.n_4 > 0 and stop != 0:
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
            return self.rm_1()
        if n == 1:
            return self.rm_3()
        if n == 2:
            return self.rm_2()
        if n == 3:
            return self.rm_4()
        if n == 4:
            return self.split_2()
        if n == 5:
            return self.split_4()
        

    
    def Minimax(self,n_ply = 1):
        if self.n_2 + self.n_4 + self.n_1 + self.n_3 == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(6):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.Minimax(n_ply - 1)
                    else:
                        temp = next.heuristic()
                    val = max(val,temp)
                    #if val == 1:
                    #    return 1
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(6):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.Minimax(n_ply - 1)
                    else:
                        temp = next.heuristic()
                    val = min(val,temp)
                    #if val == -1:
                    #    return -1
            return val        
    
        
    def AlphaBetaNply(self,n_ply = 1,alpha = -2,beta = 2):
        if self.n_2 + self.n_4 + self.n_1 + self.n_3 == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(6):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.AlphaBetaNply(n_ply - 1)
                    else:
                        temp = next.heuristic()
                        #print("1"*next.n_1 + "2"*next.n_2 +"4"*next.n_4 + " b: "+str(next.bank) + " p: " +str(self.p)+": " + str(temp) + "|"+ str(next.AlphaBeta()))
                    val = max(val,temp)
                    #if val == 1:
                    #    return 1
                    alpha = max(alpha,val)
                    if alpha >= beta:
                        break
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(6):
                next = self.advance(i)
                if next is not None:
                    if n_ply > 0:
                        temp = next.AlphaBetaNply(n_ply-1)
                    else:
                        
                        temp = next.heuristic()
                        #print("1"*next.n_1 + "2"*next.n_2 +"4"*next.n_4 + " b: "+str(next.bank) + " p: " +str(next.p)+": " + str(temp) + "|"+ str(next.AlphaBeta()))
                    val = min(val,temp)
                    #if val == -1:
                    #    return -1
                    beta = min(beta,val)
                    if alpha >= beta:
                        break
            return val    
    
    def AlphaBeta(self,alpha = -2,beta = 2):
        if self.n_2 + self.n_4 + self.n_1 + self.n_3 == 0:
            return 1-(self.bank%2 + (self.p)%2)
        if self.level%2 == 0:
            #Maximizer turn
            val = -2
            for i in range(6):
                next = self.advance(i)
                if next != None:
                    #if n_ply > 0:
                    temp = next.AlphaBeta()

                    #else:
                    #    temp = next.heuristic()
                    #if temp == -2:
                    #    print("----")                    
                    val = max(val,temp)
                    if val == 1:
                        return 1
                    alpha = max(alpha,val)
                    if alpha >= beta:
                        break
            if val == -2:
                print("1"*self.n_1 + "2"*self.n_2 +"4"*self.n_4 + " b: "+str(self.bank) + " p: " +str(self.p))
            return val    
        else:
            #Minimizer turn
            val = 2
            for i in range(6):
                next = self.advance(i)
                if next is not None:
                    print("---")
                    #if n_ply > 0:
                    temp = next.AlphaBeta()
                    #else:
                    #    temp = next.heuristic()
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
            if(self.n_1 + self.n_3)%2 == 0 and (self.n_2 + self.n_4) >= 2:
                x += 1
            return 1-((self.bank+self.n_2+self.n_4 + x)%2 + (self.p+self.n_1 + self.n_3)%2)
        else:
            if(self.n_1 + self.n_3)%2 == 1 and (self.n_2 + self.n_4) >= 2:
                x += 1
            if(self.n_4 == 1 and self.n_2 == 0 and (self.n_1 + self.n_3)%2 == 1):
                x+=1
            return 1-((self.bank+self.n_2+self.n_4 + x)%2 + (self.p+self.n_1 + self.n_3)%2)
            

for i in range(2):
    for j in range(3):
        for k in range(3):
            A = State_s(i,0,j,k,2,0,0)
            #A.generate_next_states()
            print("1"*i + "2"*j +"4"*k + " : " + str(A.AlphaBetaNply()) + " | " + str(A.heuristic()))
            
            

"""A = State_s(2,0,0,0,1,2,0)
print(A.AlphaBeta())
print(A.AlphaBetaNply())
print(A.Minimax())
print(A.heuristic())"""