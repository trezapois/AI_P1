import random
import time
import tkinter as tk
from tkinter import messagebox

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
        return "1"*self.n_1 + "2"*self.n_2 + "3"*self.n_3 +"4"*self.n_4 + " bank: " + str(self.bank) + " points: " + str(self.p)
    
    
def game():
    len = int(input("What length for the string ?"))
    AI_first = input("Put 0 if you want the AI to start") == "0"
    Minimax = input("Put 0 if you want to use Minimax else it will use Alphabeta") == "0"
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0
    for i in range(len):
        x = random.randint(0,3)
        if x == 0:
            x1 +=1
        if x == 1:
            x2 += 1
        if x == 2:
            x3 +=1
        if x == 3:
            x4 += 1
    state = State_s(x1,x3,x2,x4,0,0,0)
    state.print()
    if AI_first:
        if Minimax:
            state.Minimax()
        else:
            state.AlphaBetaNply()
        #print(state.chosen)
        state = state.advance(0)
        state.print()
    while state.n_1 + state.n_2 + state.n_3 + state.n_4 > 0:
        #print(state.heuristic())
        c = int(input("what action : \n 0 to remove a 1, 1 to remove a 3 ,2 to remove a 2\n 3 to remove a 4, 4 to split a 2 and 5 to split a 4"))
        while c == None or c < 0 or c > 5 or state.advance(c) == None:
            c = int(input("what action : \n 0 to remove a 1, 1 to remove a 3 ,2 to remove a 2\n 3 to remove a 4, 4 to split a 2 and 5 to split a 4"))
        state = state.advance(c)
        state.print()
        if state.n_1 + state.n_2 + state.n_3 + state.n_4 == 0:
            break
        if Minimax:
            state.Minimax()
        else:
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
            

#A = State_s(1,1,2,2,0,0,0)
#print(A.AlphaBeta())
#print(A.AlphaBetaNply())
#print(A.Minimax())
#print(A.heuristic())
#game()

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
    
class GameGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game")
        self.geometry("600x400")

        self.len_label = tk.Label(self, text="Enter length of the string:")
        self.len_label.pack()

        self.len_entry = tk.Entry(self)
        self.len_entry.pack()

        self.ai_label = tk.Label(self, text="AI starts? (0 for Yes, 1 for No):")
        self.ai_label.pack()

        self.ai_entry = tk.Entry(self)
        self.ai_entry.pack()

        self.algo_label = tk.Label(self, text="Choose algorithm (0 for Minimax, 1 for AlphaBeta):")
        self.algo_label.pack()

        self.algo_entry = tk.Entry(self)
        self.algo_entry.pack()

        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.action_frame = tk.Frame(self)
        self.action_label = tk.Label(self.action_frame, text="Choose an action:")
        self.action_label.pack()

        self.action_buttons = []
        self.create_action_buttons()

        self.state_label = tk.Label(self, text="")
        self.state_label.pack()

        self.current_state = None
        self.ai_first = False
        self.use_minimax = False
        self.node_visited = 0
        self.time = 0
        

    def create_action_buttons(self):
         actions = [
            "Remove a 1", "Remove a 3", "Remove a 2",
            "Remove a 4", "Split a 2", "Split a 4"
        ]
         for i, action in enumerate(actions):
            btn = tk.Button(self.action_frame, text=action, command=lambda idx=i: self.player_move(idx))
            btn.pack(side=tk.LEFT)
            self.action_buttons.append(btn)

    def start_game(self):
        try:
            length = int(self.len_entry.get())
            self.ai_first = self.ai_entry.get() == "0"
            self.use_minimax = self.algo_entry.get() == "0"
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return
        if(length < 15 or length > 20):
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return
        x1, x2, x3, x4 = 0, 0, 0, 0
        for _ in range(length):
            x = random.randint(0, 3)
            if x == 0:
                x1 += 1
            elif x == 1:
                x2 += 1
            elif x == 2:
                x3 += 1
            elif x == 3:
                x4 += 1

        self.current_state = State_s(x1, x3, x2, x4, 0, 0, 0)
        self.update_state_label()

        if self.ai_first:
            self.ai_turn()
        else:
            self.action_frame.pack()

    def ai_turn(self):
        self.update_state_label()
        if self.current_state.n_1 + self.current_state.n_2 + self.current_state.n_3 + self.current_state.n_4 == 0:
            self.end_game()
            return
        begin = time.time() 
        if self.use_minimax:
            self.current_state.Minimax()
        else:
            self.current_state.AlphaBetaNply()

        self.current_state = self.current_state.advance(self.current_state.chosen)
        end = time.time()
        self.time = end - begin
        #self.node_visited 
        self.update_state_label()

        if self.current_state.n_1 + self.current_state.n_2 + self.current_state.n_3 + self.current_state.n_4 == 0:
            self.end_game()
        else:
            self.action_frame.pack()

    def player_move(self, action):
        next_state = self.current_state.advance(action)
        if next_state is None:
            messagebox.showerror("Error", "Invalid move.")
            return

        self.current_state = next_state
        self.node_visited += 1
        self.update_state_label()
        self.action_frame.pack_forget()

        if self.current_state.n_1 + self.current_state.n_2 + self.current_state.n_3 + self.current_state.n_4 == 0:
            self.end_game()
        else:
            self.ai_turn()

    def update_state_label(self):
         self.state_label.config(text=str(self.current_state.print()+ "\n time to find the move : " + str(self.time)))

    def end_game(self):
        self.action_frame.pack_forget()
        p1 = "You"
        p2 = "The AI"
        if self.ai_first:
            p1, p2 = p2, p1

        winner = ""
        if (self.current_state.bank % 2 == 0):
            if self.current_state.p % 2 == 0:
                winner = p1 + " won"
            else:
                winner = "It's a tie"
        else:
            if self.current_state.p % 2 == 0:
                winner = "It's a tie"
            else:
                winner = p2 + " won"
        self.result_label.config(text=winner)

if __name__ == "__main__":
    game_window = GameGUI()
    game_window.mainloop()