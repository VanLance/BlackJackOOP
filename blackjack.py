import random

class GameTable():
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.pot = 0
        self.cardValues = self.dealer.deck
        
    def first_deal(self):
        setattr(self.player, 'hand', self.dealer.deal())
        print(f'{self.player.hand}, {self.player.name.capitalize()}\'s hand\n')
        print(self.dealer.hand)
        print(f'{[self.dealer.hand[0],"FaceDown"]}, Dealer Hand\n')

    def playerTurn(self):
        while True:
            self.evaluate(self.player)
            if 0 < self.value < 21 and True if input('Do you want to hit or Stay ? [H/S]:').lower() == 'h' else False:
                self.player.hand.append(self.dealer.addCards())
                self.evaluate(self.player)        
            else:
                break

    def evaluate(self,who):
        # change setattr
        try:
            who.value += self.cardValues[who.hand[-1]]
        except:
            setattr(who, 'value', sum(self.cardValues[card] for card in who.hand))
        print(f'{who.hand}\n{who.name} current value {who.value}\n')
        if who.value > 21:
            if 'ace' in who.hand:
                who.value -= 10
            else:
                print(f'{who.name} Busts')
                who.value=0
            
    def dealerTurn(self):
        while True:
            self.evaluate(self.dealer)
            if 0 < self.dealer.value < 17:
                self.dealer.hand.append(self.dealer.addCards())
                self.dealer.value += self.cardValues[self.dealer.hand[-1]]
            else:
                break
    
    def winner(self):
        if self.player.value > self.dealer.value:
            self.player.cash += self.pot
            print(f'{self.player.name} wins\n\nNew Wallet: {self.player.cash}')
        else:
            print("Dealer Wins")
        self.pot= 0
        self.player.value,self.dealer.value,self.dealer.hand,self.player.hand = 0,0,[],[]

    def continuePlaying(self):
        continuePlaying = input('Would you Like to Play a Hand Of BlackJack? [Y/N]: ').lower()
        print(continuePlaying)
        if continuePlaying == 'n' or continuePlaying == 'no':
            print(f'{self.player.name} thank you for playing\nYou currently have ${self.player.cash}')
        else:
            return True 
        
    def driver(self, first=True):
        while self.continuePlaying():
            self.pot = self.player.bet() * 2
            print(f'Current Pot: {self.pot}\n')
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
                    print(f'{self.name}\'s wallet: ${self.cash}\n')
                    return bet
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

