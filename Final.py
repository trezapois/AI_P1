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
        self.chosen = None
        

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
        return None
        

    
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
                    if temp > val:
                        val = temp
                        self.chosen = i
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
                    if temp < val:
                        val = temp
                        self.chosen = i
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
                    if temp > val:
                        val = temp
                        self.chosen = i
                        
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
                    if temp < val:
                        val = temp
                        self.chosen = i
                    #if val == -1:
                    #    return -1
                    beta = min(beta,val)
                    if alpha >= beta:
                        break
            #print(self.chosen)
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
                    if temp > val:
                        val = temp
                        self.chosen = next
                    if val == 1:
                        return 1
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
                    #print("---")
                    #if n_ply > 0:
                    temp = next.AlphaBeta()
                    #else:
                    #    temp = next.heuristic()
                    if temp < val:
                        val = temp
                        self.chosen = next
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
    
    def print(self):
        print("1"*self.n_1 + "2"*self.n_2 + "3"*self.n_3 +"4"*self.n_4 + " bank: " + str(self.bank) + " points: " + str(self.p))
    
    
def game(state, AI_first):
    state.print()
    if AI_first:
        state.AlphaBetaNply()
        print(state.chosen)
        state = state.advance(0)
        state.print()
    while state.n_1 + state.n_2 + state.n_3 + state.n_4 > 0:
        print(state.heuristic())
        c = int(input("what action : "))
        while c == None or c < 0 or c > 5 or state.advance(c) == None:
            c = int(input("what action : "))
        state = state.advance(c)
        state.print()
        if state.n_1 + state.n_2 + state.n_3 + state.n_4 == 0:
            break
        state.AlphaBetaNply()
        state = state.advance(state.chosen)
        state.print()
    p1 = "You"
    p2 = "The AI"
    if AI_first:
        (p1,p2) = (p2,p1)
    if(state.bank%2 == 0):
        if state.p % 2 == 0:
            print(p1 + " won")
        else:
            print("It's a tie")
    else:
        if state.p % 2 == 0:
            print("It's a tie")
        else:
            print(p2 + " won")
        

"""for i in range(2):
    for j in range(3):
        for k in range(3):
            A = State_s(i,0,j,k,2,0,0)
            #A.generate_next_states()
            print("1"*i + "2"*j +"4"*k + " : " + str(A.AlphaBetaNply()) + " | " + str(A.heuristic()))
    """        
            

A = State_s(1,1,2,2,0,0,0)
print(A.AlphaBeta())
#print(A.AlphaBetaNply())
#print(A.Minimax())
print(A.heuristic())
game(A,True)

"""while A.n_1 + A.n_2 + A.n_3 + A.n_4 > 0:
    A = A.advance(A.chosen)
    print("1"*A.n_1 + "2"*A.n_2 + "3"*A.n_3 +"4"*A.n_4 + " bank: " + str(A.bank) + " points: " + str(A.p))
    c = int(input("what action"))
    while c == None or c < 0 or c > 5 or A.advance(c) == None:
        c = int(input("what action"))
    A = A.advance(c)
    if A.n_1 + A.n_2 + A.n_3 + A.n_4 == 0:
        break
    print("1"*A.n_1 + "2"*A.n_2 + "3"*A.n_3 +"4"*A.n_4 + " bank: " + str(A.bank) + " points: " + str(A.p))
    A.AlphaBetaNply()"""