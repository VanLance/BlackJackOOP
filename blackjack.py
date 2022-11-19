import random


class GameTable():
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.pot = 0

    def first_deal(self):
        setattr(self.player, 'hand', self.dealer.deal())
        print(f'{self.player.hand}, Player Hand\n')
        print(self.dealer.hand)
        print(f'{[self.dealer.hand[0],"FaceDown"]}, Dealer Hand\n')
        self.driver(False)

    def driver(self, first=True):
        while True:
            bet = input('Would you like to bet? [Y/N] ')
            if 'y' == bet.lower() or bet.lower() == 'yes':
                bet = self.player.bet()
                self.pot = bet * 2
                if first:
                    self.first_deal()
                    break
            if self.pot:
                while True:
                    self.player.hand.append(self.dealer.addCards())
                    print(self.player.hand, '\n')
            
            else:
                leave = input('Would you like to leave? [Y/N]').lower()
                if leave == 'y' or leave == 'yes':
                    break
            
            


class Dealer():
    def __init__(self, name, deck):
        self.name = name
        self.deck = list(deck.deck)
        self.hand = []

    def deal(self):
        random.shuffle(self.deck)
        if not self.hand:
            playerCards = [self.deck.pop()]
            self.hand.append(self.deck.pop())
            playerCards.append(self.deck.pop())
            self.hand.append(self.deck.pop())
            return playerCards

    def addCards(self):
        return self.deck.pop()


class Player():
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash

    def addCash(self):
        try:
            self.cash += int(input("How much money are you adding? "))
        except:
            while True:
                add = input("Please input number amount you're adding to your pot or type Nevermind: ")
                if add.lower() == 'nevermind':
                    break
                if add.isdigit():
                    self.cash += int(add)
                    break

    def bet(self):
        try:
            bet = int(input("How much money are you betting? "))
            self.cash -= bet
            return bet
        except:
            while True:
                bet = input(
                    "Please input number amount you're adding betting or type Nevermind: ")
                if bet.lower() == 'nevermind':
                    break
                if bet.isdigit():
                    self.cash -= int(bet)
                    return bet
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


newDeck = Deck()


gamblinMan = Player('Clint', 100)
shuffler = Dealer('Joe', newDeck)
hotSpot = GameTable(gamblinMan, shuffler)
hotSpot.driver()
# shuffler.deal()
# print(shuffler.hand)
