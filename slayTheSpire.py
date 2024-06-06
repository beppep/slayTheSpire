#what would be a good name for a card with this efect: "Attack 23. lose 1 strength." its important that your answer is well formatted and between 5 and 15 characters long since i will use it for a game. your answer cannot contain any other text than those characters. dont write any other sentences. give exactly one answer

import random



class Effect():

    def __init__(self):
        self.effectType = "None"
        self.value = 0
        #self.target = target
        self.estimatedCost = 0

    def activate(self, encounter):
        if self.effectType == "Attack":
            encounter.enemies[0].hurt(self.value, encounter)
        elif self.effectType == "Block":
            encounter.player.block += self.value
        elif self.effectType == "Draw":
            for i in range(self.value):
                encounter.player.drawCard()

    def generate(self):
        if random.random()<0.5:
            self.effectType = "Attack"
            self.value = random.randint(1,random.randint(1,30))
            self.estimatedCost = self.value/8
        elif random.random()<0.5:
            self.effectType = "Block"
            self.value = random.randint(1,random.randint(1,20))
            self.estimatedCost = self.value/6
        else:
            self.effectType = "Draw"
            self.value = random.randint(1,random.randint(1,5))
            self.estimatedCost = self.value/2

    def print(self):
        print(self.effectType, self.value)

    def text(self):
        return self.effectType + " " + str(self.value)


class Card():

    def __init__(self):

        self.name = "None"
        self.cost = 0
        self.effects = []

    def play(self, encounter):
        encounter.player.hand.remove(self)
        encounter.player.discard.append(self)
        encounter.player.mana -= self.cost
        for effect in self.effects:
            effect.activate(encounter)

    def generate(self):

        estimatedCost = 999
        while not (0 < estimatedCost < 4):
            self.effects = []

            estimatedCost = -0.5
            for i in range(random.randint(1,3)):
                effect = Effect()
                effect.generate()
                self.effects.append(effect)
                estimatedCost += effect.estimatedCost

        self.cost = int(estimatedCost+0.5)
        self.truCost = estimatedCost

        self.name = self.effects[0].effectType + " Card yo"

    def print(self):

        print(self.name)
        print("<"+str(self.cost)+">", "("+str(self.truCost)+")")
        for effect in self.effects:
            effect.print()


    def generateStrike(self):
        self.name = "Strike!"
        self.cost = 1
        self.truCost = 1
        effect = Effect()
        effect.effectType = "Attack"
        effect.value = 6
        self.effects = [effect]

    def generateDefend(self):
        self.name = "Defend!"
        self.cost = 1
        self.truCost = 1
        effect = Effect()
        effect.effectType = "Block"
        effect.value = 5
        self.effects = [effect]

class Character():

    def __init__(self, hp, maxhp):
        self.hp = hp
        self.maxhp = maxhp
        self.block = 0

    def hurt(self, value, encounter):
        value = max(0, value - self.block)
        self.hp -= value
        if(self.hp <= 0):
            self.die(encounter)
        return value


class Player(Character):

    def __init__(self, deck, hp, maxhp):
        super().__init__(hp, maxhp)

        self.deck = deck.copy()
        self.hand = []
        self.discard = []
        self.maxmana = 3
        self.mana = self.maxmana

    def drawCard(self):
        self.hand.append(self.deck.pop())
        if len(self.deck) == 0:
            self.deck = self.discard.copy()
            random.shuffle(self.deck)
            self.discard = []

    def playCard(self, i, encounter):
        self.hand[i].play(encounter)

    def discardHand(self):
        self.discard += self.hand
        self.hand = []

    def printHand(self):
        padding = 20
        line = ""
        for i in range(len(self.hand)):
            card = self.hand[i]
            text = card.name + " ("+str(i+1)+")"
            line += text
            line += " "*(padding - len(text))
        print(line)
        line = ""
        for card in self.hand:
            text = "<"+str(card.cost)+">   ("+str(round(card.truCost,2))+")" 
            line += text
            line += " "*(padding - len(text))
        print(line)
        for i in range(max([len(card.effects) for card in self.hand])):
            line = ""
            for card in self.hand:
                if len(card.effects)>=i+1:
                    text = card.effects[i].text()
                else:
                    text = ""
                line += text
                line += " "*(padding - len(text))
            print(line)

class Enemy(Character):
    def __init__(self):
        maxhp = random.randint(10,40)
        super().__init__(maxhp, maxhp)

        self.name = "Generic Enemy"
        self.action = None

    def randomizeAction(self):
        if random.random()<1:
            self.action = "Attack"
            self.actionValue = random.randint(1,20)

    def act(self, encounter):
        if self.action == "Attack":
            thruDmg = encounter.player.hurt(self.actionValue, encounter)
            print(self.name, "attacks for", self.actionValue, "("+str(thruDmg)+")")

    def die(self, encounter):
        print(self.name, "was killed.")
        encounter.enemies.remove(self)

class Encounter():
        
    def __init__(self, playerDeck, playerhp, playermaxhp):

        self.player = Player(playerDeck, playerhp, playermaxhp)

        self.enemies = []
        for i in range(1):
            self.enemies.append(Enemy())

    def printStatus(self):

        print("PLAYER:","("+str(self.player.hp)+"/"+str(self.player.maxhp)+")", "<"+str(self.player.mana)+"/"+str(self.player.maxmana)+">", "["+str(self.player.block)+"]")
        for enemy in self.enemies:
            print(enemy.name.upper()+":","("+str(enemy.hp)+"/"+str(enemy.maxhp)+") with intention: ["+enemy.action+" "+str(enemy.actionValue)+"]")
        print()
        self.player.printHand()
        #print("You have", len(self.player.hand), "cards:", cardstring)

    def enemyRandomizeAction(self):
        for enemy in self.enemies:
            enemy.randomizeAction()

    def playerTurn(self):

        self.player.mana = self.player.maxmana
        self.player.block = 0
        for i in range(5):
            self.player.drawCard()

        choice = ""
        while not (choice == "end"):
            self.printStatus()
            choice = input('Choose a card: ')

            if choice.isdigit() and (0 < int(choice) <= len(self.player.hand)):
                chosenCard = self.player.hand[int(choice)-1]
                #chosenCard.print()

                if self.player.mana>=chosenCard.cost:
                    #if input("Do you want to play this card? (y to play): ")=="y":
                    print("You played", chosenCard.name)
                    chosenCard.play(self)
                else:
                    print("...not enough mana...")

        self.player.discardHand()

    def enemyTurn(self):

        for enemy in self.enemies:
            enemy.act(self)

class Run():

    def __init__(self):

        self.playermaxhp = 50
        self.playerhp = self.playermaxhp

        self.playerDeck = []
        for i in range(10):
            card = Card()
            if i<4:
                card.generateStrike()
            elif i<8:
                card.generateDefend()
            else:
                card.generate()
            self.playerDeck.append(card)

        for i in range(10):
            encounter = Encounter(self.playerDeck, self.playerhp, self.playermaxhp)
            while encounter.enemies:
                encounter.enemyRandomizeAction()
                encounter.playerTurn()
                encounter.enemyTurn()
        print("you win")



run = Run()