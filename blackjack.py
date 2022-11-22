import random

class GameTable():
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.pot = 0
        self.cardValues = self.dealer.deck
        self.handValue = {}
        
    def first_deal(self):
        self.player.hand = self.dealer.deal()
        print(f'{[self.dealer.hand[0],"FaceDown"]}, Dealer Hand\n')

    def playerTurn(self):
        while True:
            self.evaluate(self.player)
            if 0 < self.handValue[self.player] < 21:
                if input('Hit or Stay? [H/S]:').lower()=='h':
                    self.player.hand.append(self.dealer.addCards())
                else:
                    break        
            else:
                break
            
    def evaluate(self,who):
        self.handValue[who]= self.handValue.get(who, self.cardValues[who.hand[0]]) + self.cardValues[who.hand[-1]]
        if self.handValue[who] > 21 and 'ace' in who.hand:
            self.handValue[who] = sum(self.cardValues[card] for card in who.hand) - (10 * who.hand.count('ace'))
        print(f'{who.name}\'s hand value {self.handValue[who]}\n{who.hand}\n')
        if self.handValue[who] > 21:
            print(f'{who.name} Busts')
            self.handValue[who]=0
            print(self.handValue[who])
    
    def dealerTurn(self):
        while True:
            self.evaluate(self.dealer)
            if 0 < self.handValue[self.dealer] < 17:
                self.dealer.hand.append(self.dealer.addCards())
            else:
                break
    
    def winner(self):
        if self.handValue[self.player] > self.handValue[self.dealer]:
            self.player.cash += self.pot
            print(f'{self.player.name} wins\n\nNew Wallet: {self.player.cash}')
        elif self.handValue[self.player] < self.handValue[self.dealer]:
            print(f"{self.dealer.name} Wins")
        else:
            print('Push you Get your Bet back')
            self.player.cash += self.pot  // 2
        self.player.pot= 0
        del self.handValue[self.player]
        del self.handValue[self.dealer]
        self.dealer.hand,self.player.hand = [],[]

    def continuePlaying(self):
        continuePlaying = input('Would you Like to Play a Hand Of BlackJack? [Y/N]: ').lower()
        self.player.bet()
        if continuePlaying == 'n' or continuePlaying == 'no':
            print(f'{self.player.name} thank you for playing\nYou currently have ${self.player.cash}')
        else:
            return True 
        
    def driver(self):
        while self.continuePlaying():
            self.first_deal()
            self.playerTurn()
            self.dealerTurn()
            self.winner()
            
class Dealer():
    def __init__(self, name, deck):
        self.name = name
        self.deckCards = list(deck.deck)
        self.deck = deck.deck
        self.hand = []

    def deal(self):
        random.shuffle(self.deckCards)
        if not self.hand:
            playerCards = [self.deckCards.pop()]
            self.hand.append(self.deckCards.pop())
            playerCards.append(self.deckCards.pop())
            self.hand.append(self.deckCards.pop())
            return playerCards

    def addCards(self):
        return self.deckCards.pop()

class Player():
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash

    def addCash(self):
        try:
            self.cash += int(input("How much money are you adding? "))
            print(f'{self.name}"s wallet: ${self.cash}\n')
        except:
            while True:
                add = input("Please input number amount you're adding to your wallet or type Nevermind: ")
                if add.lower() == 'nevermind':
                    break
                if add.isdigit():
                    self.cash += int(add)
                    break

    def bet(self):
        bet = input('\nWould you like to bet? [Y/N]\n')
        if bet.lower()=='y' or bet.lower() == 'yes':
            while True:
                bet = input(f"Current Wallet: {self.cash}\nHow much money are you betting? \n")
                if bet.isdigit():
                    bet = int(bet)
                    while bet > self.cash:
                        self.addCash()
                    self.cash -= bet
                    self.pot = bet * 2
                    print(f'{self.name}\'s wallet: ${self.cash}\nCurrent Pot: {self.pot}\n')
                    return
                else:
                    print('Please enter number amount\n')
        return False
class Deck():
    def __init__(self):
        self.deck = {i: i for i in range(1, 11)}
        self.addFaceCards()
        
    def addFaceCards(self):
        self.deck['jack'] = 10
        self.deck['queen'] = 10
        self.deck['king'] = 10
        self.deck['ace'] = 11

hotSpot = GameTable(Player('Clint', 100), Dealer('dealerJoe', Deck()))
hotSpot.driver()

