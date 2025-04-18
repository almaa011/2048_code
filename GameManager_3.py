from Grid_3       import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer
from random       import randint
import time

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05

class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
        else:
            while time.perf_counter() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.perf_counter()



    # def start(self):
    #     for i in range(self.initTiles):
    #         self.insertRandonTile()

    #     self.displayer.display(self.grid)

    #     # Player AI Goes First
    #     turn = PLAYER_TURN
    #     maxTile = 0

    #     self.prevTime = time.perf_counter()

    #     while not self.isGameOver() and not self.over:
    #         # Copy to Ensure AI Cannot Change the Real Grid to Cheat
    #         gridCopy = self.grid.clone()

    #         move = None

    #         if turn == PLAYER_TURN:
    #             print("Player's Turn:", end="")
    #             move = self.playerAI.getMove(gridCopy)
    #             print(actionDic[move])

    #             # Validate Move
    #             if move != None and move >= 0 and move < 4:
    #                 if self.grid.canMove([move]):
    #                     self.grid.move(move)

    #                     # Update maxTile
    #                     maxTile = self.grid.getMaxTile()
    #                 else:
    #                     print("Invalid PlayerAI Move")
    #                     self.over = True
    #             else:
    #                 print("Invalid PlayerAI Move - 1")
    #                 self.over = True
    #         else:
    #             print("Computer's turn:")
    #             move = self.computerAI.getMove(gridCopy)

    #             # Validate Move
    #             if move and self.grid.canInsert(move):
    #                 self.grid.setCellValue(move, self.getNewTileValue())
    #             else:
    #                 print("Invalid Computer AI Move")
    #                 self.over = True

    #         if not self.over:
    #             self.displayer.display(self.grid)

    #         # Exceeding the Time Allotted for Any Turn Terminates the Game
    #         self.updateAlarm(time.perf_counter())


    #         turn = 1 - turn
    #     print(maxTile)



    def start(self):
        # Record the overall start time
        start_time = time.perf_counter()

        # Insert initial tiles and display the grid.
        for i in range(self.initTiles):
            self.insertRandonTile()
        self.displayer.display(self.grid)

        maxTile = 0

        # Main game loop without enforcing a per-turn time limit.
        while not self.isGameOver() and not self.over:
            gridCopy = self.grid.clone()
            print("Player's Turn:", end="")

            move = self.playerAI.getMove(gridCopy)
            print(actionDic[move])

            if move is not None and move >= 0 and move < 4:
                if self.grid.canMove([move]):
                    self.grid.move(move)
                    maxTile = self.grid.getMaxTile()
                else:
                    print("Invalid Move")
                    self.over = True
            else:
                print("Invalid Move")
                self.over = True

            if not self.over:
                self.insertRandonTile()
                self.displayer.display(self.grid)

        print("Max tile reached:", maxTile)
        
        # Compute and print total time played.
        total_time = time.perf_counter() - start_time
        print("Total time played: {:.2f} seconds".format(total_time))



    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    computerAI  = ComputerAI()
    displayer 	= Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    gameManager.start()

if __name__ == '__main__':
    main()
