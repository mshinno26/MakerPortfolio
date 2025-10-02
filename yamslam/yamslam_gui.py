"""
cumulative gui for Yamslam
yamslam_gui.py
Max Shinno
"""

import pygame
from yamslam import Yamslam
from dice import DiceManager
from button import Button
from chip import ChipManager
from playerScore import PlayerScore

class YamslamGUI():

    def __init__(self):
        pygame.init()
        self._CLOCK = pygame.time.Clock()
        self._FPS = 30
        self._WHITE = (255, 255, 255)
        self._YELLOW = (234, 170, 0)
        self._WIDTH = 1000
        self._HEIGHT = 600
        pygame.display.set_caption("YAMSLAM")
        self._screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        self._screen.fill(self._YELLOW)

    def start(self):
        # (splash screen), get num players
        numPlayers = self.splash()
        if numPlayers < 0:
            return
        players = []
        for i in range(numPlayers):
            players.append("Player " + str(i+1))
        yamslam = Yamslam(players)

        # initiate objects
        dswidth = 290
        dsheight = 50
        diceManager = DiceManager(self._screen.subsurface(((self._WIDTH - dswidth)/2, (self._HEIGHT - dsheight)/2, dswidth, dsheight)), "diceImages")

        # first roll, get patterns, check for yamslam (if so, run=false)
        roll = yamslam.roll([0]*5, [0, 1, 2, 3, 4])
        diceManager.createDice(roll, 60)

        bx = 711
        bry = 233
        bsy = 313
        bny = 393
        btnRoll = self.createBtn(False, "roll", bx, bry)
        btnScore = self.createBtn(False, "score", bx, bry)
        btnNext = self.createBtn(True, "next", bx, bny)
        btnHelp = self.createBtn(True, "btnHelp", 945, 545)

        cswidth = 210
        csheight = 580
        csx = 73
        csy = 20
        chipManager = ChipManager(self._screen.subsurface((csx, csy, cswidth, csheight)))
        chipx = 0
        chipy = 490
        chipxincrement = 100
        chipyincrement = -100
        chipManager.loadChips(yamslam.pattern(roll), "chipImages", 1.0, chipx, chipxincrement, chipy, chipyincrement)

        # scoreboard
        psw = 206
        psh = 56
        sbw = psw*numPlayers
        sbx = (self._WIDTH - sbw)/2
        sby = 30
        scoreboard = self._screen.subsurface((sbx, sby, sbw, psh))
        psgroup = self.makePSGroup(players, yamslam.getScores(), 0)

        rolledYamslam = False
        nextTurn = False
        run = True
        help = False
        while run:
            if not help:
                self._screen.fill(self._YELLOW)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # selection for roll & score
                        if btnRoll.isClicked() and diceManager.isDiceSelected() and yamslam.rollsLeft():
                            # reroll: get numbers AND patterns, create dice, check for yamslam (if so, run=false)
                            roll = yamslam.roll(diceManager.getDice(), diceManager.getDiceSelections())
                            diceManager.createDice(roll, 60)
                            btnRoll = self.createBtn(False, "roll", bx, bry)
                            patterns = yamslam.pattern(roll)
                            chipManager.loadChips(patterns, "chipImages", 1.0, chipx, chipxincrement, chipy, chipyincrement)
                            nextTurn = not yamslam.rollsLeft() and not chipManager.isChipsAvail()    # if no rolls left and no chips selectable, next turn
                        elif btnScore.isClicked() and chipManager.getChipSelected() > 0:
                            # score: pass selected chip, get scoreboard, next turn*
                            rolledYamslam = yamslam.score(chipManager.getChipSelected())
                            # override all chips to depleted or unavailable
                            chipsTemp = {50:1, 40:1, 30:1, 25:1, 20:1, 10:1, 5:1}
                            chips = yamslam.getChips()
                            for chip in chips:
                                if chips[chip] == 0:
                                    chipsTemp.update({chip:0})
                            chipManager.loadChips(chipsTemp, "chipImages", 1.0, chipx, chipxincrement, chipy, chipyincrement)
                            scores = yamslam.getScores()
                            psgroup.empty()
                            for i in range(numPlayers):
                                psgroup.add(PlayerScore(f"{players[i]}: {scores[players[i]]}", psw*i, 0, i == yamslam.getCurrPlayerNum()))
                            if yamslam.end():
                                run = False
                                break
                            nextTurn = True if not rolledYamslam else False    # if scored, next turn unless Yamslam
                        if rolledYamslam:
                            roll = yamslam.roll([0]*5, [0, 1, 2, 3, 4])
                            diceManager.createDice(roll, 60)
                            chipManager.loadChips(yamslam.pattern(roll), "chipImages", 1.0, chipx, chipxincrement, chipy, chipyincrement)
                            rolledYamslam = False
                        elif nextTurn:
                            btnNext = self.createBtn(True, "next", bx, bny)
                            if btnNext.draw(self._screen):
                                yamslam.nextTurn()
                                btnRoll = self.createBtn(False, "roll", bx, bry)
                                btnScore = self.createBtn(False, "score", bx, bsy)
                                roll = yamslam.roll([0]*5, [0, 1, 2, 3, 4])
                                diceManager.createDice(roll, 60)
                                chipManager.loadChips(yamslam.pattern(roll), "chipImages", 1.0, chipx, chipxincrement, chipy, chipyincrement)
                                nextTurn = False
                                psgroup.empty()
                                scores = yamslam.getScores()
                                for i in range(numPlayers):
                                    psgroup.add(PlayerScore(f"{players[i]}: {scores[players[i]]}", psw*i, 0, i == yamslam.getCurrPlayerNum()))
                            # *next turn: check if out of chips (if so, run=false), first roll
                
                # draw dice
                if diceManager.drawDice():
                    # if any dice were changed, check if dice are selected; if so, activate roll button; otherwise, deactivate
                    if diceManager.isDiceSelected() and yamslam.rollsLeft():
                        btnRoll = self.createBtn(True, "roll", bx, bry)
                    else:
                        btnRoll = self.createBtn(False, "roll", bx, bry)
                        
                # draw chips
                chipManager.drawChips()
                # check if chips are selected; if so, activate score button
                if chipManager.getChipSelected() > 0:
                    btnScore = self.createBtn(True, "score", bx, bsy)
                else:
                    btnScore = self.createBtn(False, "score", bx, bsy)

                # draw roll button
                btnRoll.draw(self._screen)

                # draw score button
                btnScore.draw(self._screen)
                
                # draw score button
                if nextTurn:
                    btnNext.draw(self._screen)

                if btnHelp.draw(self._screen):
                    help = True

                # draw scoreboard
                for ps in psgroup:
                    ps.draw(scoreboard)
                    
                # blit rolls left
                self.rollsLeft(3-yamslam.getNumRolls())

                #pygame.display.update()
                pygame.display.flip()
                self._CLOCK.tick(self._FPS)
            else:
                if self.helpScreen():
                    help = False
                else:
                    pygame.quit()
                    return
        # display winner
        self.endScreen(players, yamslam.getScores(), yamslam.getWinner().getIndex())
        pygame.quit()
    
    def splash(self):
        numPlayers = 1
        font = pygame.font.Font("fonts/NovaMono.ttf", 60)
        textSurface = font.render("Welcome to Yamslam!", True, self._WHITE)
        self._screen.blit(textSurface, ((self._WIDTH-textSurface.get_width())/2, 25, 500, 100))
        bsSide = 425
        btnSurface = self._screen.subsurface(((self._WIDTH-bsSide)/2, 125, bsSide, bsSide))
        btn1 = self.createBtn(True, "players1", 0, 0)
        btn2 = self.createBtn(True, "players2", 225, 0)
        btn3 = self.createBtn(True, "players3", 0, 225)
        btn4 = self.createBtn(True, "players4", 225, 225)
        run = True
        while run:
            # get events so that pygame doesn't break in the inifinite run loop
            for event in pygame.event.get():
                # TODO event.quit
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    return -1
            # draw each button & check if has been clicked
            if btn1.draw(btnSurface):
                numPlayers = 1
                run = False
            elif btn2.draw(btnSurface):
                numPlayers = 2
                run = False
            elif btn3.draw(btnSurface):
                numPlayers = 3
                run = False
            elif btn4.draw(btnSurface):
                numPlayers = 4
                run = False
            pygame.display.update()
            self._CLOCK.tick(self._FPS)
        return numPlayers

    def endScreen(self, players, scores, winner):
        numPlayers = len(players)
        psw = 206
        psh = 56
        sbw = psw*numPlayers
        sbx = (self._WIDTH - sbw)/2
        sby = 130
        scoreboard = self._screen.subsurface((sbx, sby, sbw, psh))
        psgroup = self.makePSGroup(players, scores, winner)
        font = pygame.font.Font("fonts/NovaMono.ttf", 60)
        textSurface = font.render(f"WINNER: Player {winner+1}", True, self._WHITE)
        run = True
        while run:
            self._screen.fill(self._YELLOW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            for ps in psgroup:
                ps.draw(scoreboard)
            self._screen.blit(textSurface, ((self._WIDTH-textSurface.get_width())/2, (self._HEIGHT-textSurface.get_height())/2, 500, 100))
            pygame.display.update()
            self._CLOCK.tick(self._FPS)

    def makePSGroup(self, players, scores, currPlayerNum):
        numPlayers = len(players)
        psw = 206
        psgroup = pygame.sprite.Group()
        for i in range(numPlayers):
            psgroup.add(PlayerScore(f"{players[i]}: {scores[players[i]]}", psw*i, 0, i==currPlayerNum))
        return psgroup

    def createBtn(self, active, type, x, y):
        return Button(active, "buttonImages", type, x, y, 1.0)
    
    def rollsLeft(self, numLeft):
        font = pygame.font.Font("fonts/NovaMono.ttf", 38)
        textSurface = font.render(f"Rolls Left: {numLeft}", True, self._WHITE)
        self._screen.blit(textSurface, (645+(355-textSurface.get_width())/2, 155, 500, 100))

    def helpScreen(self):
        btnReturn = self.createBtn(True, "return", 772, 5)
        imageFilename = "miscImages/help.png"
        image = pygame.image.load(imageFilename).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * 1.0), int(height * 1.0)))
        run = True
        while run:
            self._screen.fill(self._YELLOW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return False
            if btnReturn.draw(self._screen):
                run = False
            self._screen.blit(image, (0, 0))                
            pygame.display.update()
            self._CLOCK.tick(self._FPS)
        return True