'''
Created on 2019年5月16日

@author: Charl Ep
'''
from referee.game import Chexers
from SandSculpture.player import Player as player
import time
import sys
def main():
    game=Chexers()
    player1=player('r')
    player2=player('g')
    player3=player('b')
    players=(player1, player2, player3)
    curr_p,next_p,prev_p=player1,player2,player3
    
    while not game.over():
        action = curr_p.action()
        
        # Validate this action (or pass) and apply it to the game if it is 
        # allowed. Display the resulting game state.
        game.update(curr_p.colour, action)
        print(game.__str__())
        # Notify all three players (including the current player) of the action
        # (or pass) (using their .update() methods).
        for i in players:
            i.update(curr_p.colour, action)
    
        # Next player's turn!
        curr_p,next_p,prev_p=next_p,prev_p,curr_p
        
if __name__ == '__main__':
    main()