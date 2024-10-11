from game_Truco import Game as Game

def main():
   
    game = Game()
    s = game.getState()
    r = 0
    t = False

    print("-----------------")
    print("Game Started")
    print("-----------------")
    print("Hand P1:", game.handP1)
    print("Hand P2:", game.handP2)
    print("-----------------")

    while(not game.gameFinished()):
        #print("+++")
        #print("State: ", s)
        if(game.getIsP1Turn()):
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P1 Turn")
            game.printStateP1()

            actionIdx = int(input("Choose action: "))
        else:
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P2 Turn")
            game.printStateP2()

            actionIdx = int(input("Choose action: "))
        
        (s1, r1, t1) = game.step(actionIdx)
        s = s1[:]
        r = r1
        t = t1
        if(game.isP1Turn or game.gameFinished()):
            print("P1 recieved r:", r1)   
        if((not game.isP1Turn) or game.gameFinished()):
            print("P2 recieved r:", r1)        
        
        print("Terminal:", t1)
        
        #print("Whoose turn:", game.getIsP1Turn())
        if(game.gameFinished()):
            print("-------------")
            print("Game Ended")


if __name__ == '__main__':
    main()
