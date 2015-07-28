import random
randint = random.randint


def shuffle():

    """This function produces a random arrangement of the numbers 0 through 51.
    """
    deckorder = []
    while len(deckorder) < 6 * 52:
        card = randint(0, 51)
        if deckorder.count(card) < 6:
            deckorder.append(card)

    return deckorder


def deckread(deckorder):

    """This function interprets numbers 1 through 52 as cards and prints the result.
    """

    # Define a deck
    basedeck = ['cA', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'cJ', 'cQ', 'cK',
                'sA', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 'sJ', 'sQ', 'sK',
                'hA', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'hJ', 'hQ', 'hK',
                'dA', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'dJ', 'dQ', 'dK']

    deck = []
    for i in range(312):
        deck.append(basedeck[deckorder[i]])
    return deck


def initial_deal(deck, place, money, bet, rm, dm):
    playercards = [deck[place], deck[2 + place]]
    dealercards = [deck[1 + place], deck[3 + place]]
    chosen = False
    place += 4
    print('\n\n**', dealercards[1])
    print('Bet: $', bet)
    if rm > 0:
        if (playercards[0][0] == playercards[1][0] and (playercards[0][1] == 'K' or playercards[0][1] == 'Q')
           and playercards[1][1] == 'K' or playercards[1][1] == 'Q'):
            money += 25 * rm
            print('You have Royal Match!')
        elif playercards[0][0] == playercards[1][0]:
            money += 2.5 * rm
            print('You have Easy Match!')
    if dm > 0:
        for i in range(2):
            if playercards[i][1] == dealercards[1][1] and playercards[i][0] == dealercards[1][0]:
                money += 11 * dm
                print('You have a suited dealer match!')
            elif playercards[i][1] == dealercards[1][1]:
                money += 4 * dm
                print('You have a dealer match!')
    if (cardvalue(playercards[0]) + cardvalue(playercards[1]) == 21 and
       cardvalue(dealercards[0]) + cardvalue(dealercards[1]) == 21):
        print('\nYou both have blackjack!')
        print('\n$', money)
        print(playercards)
        chosen = True
    elif cardvalue(playercards[0]) + cardvalue(playercards[1]) == 21:
        print('You have blackjack!')
        money += 3 * bet
        print('\n$', money)
        print(playercards)
        chosen = True
    elif cardvalue(dealercards[1]) == 11:
        print('\nBuy insurance? (Y/N)')
        print('\n$', money)
        print(playercards)
        choice = input()
        choice = choice.casefold()
        if choice == 'y' and cardvalue(dealercards[0]) == 10:
            print('Dealer has blackjack.')
            money += bet
            chosen = True
        elif choice != 'y' and cardvalue(dealercards[0]) == 10:
            print('Dealer has blackjack.')
            chosen = True
        elif cardvalue(dealercards[0]) != 10:
            print('Dealer does not have blackjack.')
            if choice == 'Y':
                money -= bet
            print('\n\n**', dealercards[1])
            print('Bet: $', bet)
            print('\nWhat would you like to do?')
            print('d. Double down')
            print('h. Hit')
            print('s. Stand')
            if cardvalue(playercards[0]) == cardvalue(playercards[1]):
                print('u. Split')
            print('t. Surrender')
            print('x. Run for it')
            print('\n$', money)
            print(playercards)
    elif cardvalue(dealercards[0]) + cardvalue(dealercards[1]) == 21:
        print('Dealer has Blackjack.')
        chosen = True
    else:
        print('\nWhat would you like to do?')
        print('d. Double down')
        print('h. Hit')
        print('s. Stand')
        if cardvalue(playercards[0]) == cardvalue(playercards[1]):
            print('u. Split')
        print('t. Surrender')
        print('x. Run for it')
        print('\n$', money)
        print(playercards)
    return money, place, playercards, dealercards, chosen


def cardvalue(card):
    if card[1] != 'A' and card[1] != 'J' and card[1] != 'Q' and card[1] != 'K' and card[1] != '1':
        value = int(card[1])
    elif card[1] == 'A':
        value = 11
    else:
        value = 10
    return value


def hit(deck, place, playercards, dealercards, money, bet):
    print('\n\n**', dealercards[1])
    print('Bet: $', bet)
    playercards.append(deck[place])
    place += 1
    playerhandvalue = 0
    for i in range(len(playercards)):
        playerhandvalue += cardvalue(playercards[i])
    playeraces = playercards.count('cA') + playercards.count('dA') \
        + playercards.count('hA') + playercards.count('sA')
    while playerhandvalue > 21 and playeraces > 0:
        playerhandvalue -= 10
        playeraces -= 1
    if playerhandvalue < 21:
        print('\nWhat would you like to do?')
        print('d. Double down')
        print('h. Hit')
        print('s. Stand')
        print('x. Run for it')
        print('\n$', money)
        print(playercards)
    elif playerhandvalue == 21:
        place, money = stand(deck, place, playercards, dealercards, money, bet)
    else:
        print('Player busts.')
        print('\n$', money)
        print(playercards)
    choice = input()
    choice = choice.casefold()
    if choice == 'h':
        place, money, playercards = hit(deck, place, playercards, dealercards, money, bet)
        playerhandvalue = 0
        for i in range(len(playercards)):
            playerhandvalue += cardvalue(playercards[i])
    elif choice == 's':
        place, money = stand(deck, place, playercards, dealercards, money, bet)
    elif choice == 'd':
        place, money, = double_down(deck, place, playercards, dealercards, money, bet)
    return place, money, playercards


def stand(deck, place, playercards, dealercards, money, bet):
    dealerhandvalue = cardvalue(dealercards[0]) + cardvalue(dealercards[1])
    while dealerhandvalue < 17:
        dealercards.append(deck[place])
        place += 1
        dealerhandvalue = 0
        for i in range(len(dealercards)):
            dealerhandvalue += cardvalue(dealercards[i])
        dealeraces = dealercards.count('cA') + dealercards.count('dA') + \
            dealercards.count('hA') + dealercards.count('sA')
        while dealerhandvalue > 21 and dealeraces > 0:
            dealerhandvalue -= 10
            dealeraces -= 1
    print('\n\n', dealercards)
    playerhandvalue = 0
    for i in range(len(playercards)):
        playerhandvalue += cardvalue(playercards[i])
    playeraces = playercards.count('cA') + playercards.count('dA') + \
        playercards.count('hA') + playercards.count('sA')
    while playerhandvalue > 21 and playeraces > 0:
        playerhandvalue -= 10
        playeraces -= 1
    print('Bet: $', bet)
    if (dealerhandvalue > playerhandvalue) and (dealerhandvalue < 22):
        print('Dealer wins.')
    elif (dealerhandvalue < playerhandvalue) or (dealerhandvalue > 21):
        print('Player wins!')
        money += 2 * bet
    elif (dealerhandvalue == playerhandvalue) and (len(dealercards) > len(playercards)):
        print('Dealer wins.')
    elif (dealerhandvalue == playerhandvalue) and (len(dealercards) < len(playercards)):
        print('Player wins!')
        money += 2 * bet
    else:
        print("It's a tie!")
        money += bet
    print('\n$', money)
    print(playercards)
    return place, money


def double_down(deck, place, playercards, dealercards, money, bet):
    money -= bet
    bet += bet
    print('\n\n**', dealercards[1])
    print('Bet: $', bet)
    playercards.append(deck[place])
    place += 1
    playerhandvalue = 0
    for i in range(len(playercards)):
        playerhandvalue += cardvalue(playercards[i])
    playeraces = playercards.count('cA') + playercards.count('dA') + \
        playercards.count('hA') + playercards.count('sA')
    while playerhandvalue > 21 and playeraces > 0:
        playerhandvalue -= 10
        playeraces -= 1
    if playerhandvalue < 21:
        place, money = stand(deck, place, playercards, dealercards, money, bet)
    elif playerhandvalue == 21:
        place, money = stand(deck, place, playercards, dealercards, money, bet)
    else:
        print('Player busts.')
        print('\n$', money)
        print(playercards)
    return place, money


def split(deck, place, playercards, dealercards, money, bet):
    playercards1 = [playercards[0], deck[place]]
    playercards2 = [playercards[1], deck[1 + place]]
    place += 2
    money -= bet
    dealerhandvalue = cardvalue(dealercards[0]) + cardvalue(dealercards[1])
    while dealerhandvalue < 17:
        dealercards.append(deck[place])
        place += 1
        dealerhandvalue = 0
        for i in range(len(dealercards)):
            dealerhandvalue += cardvalue(dealercards[i])
        dealeraces = dealercards.count('cA') + dealercards.count('dA') + \
            dealercards.count('hA') + dealercards.count('sA')
        while dealerhandvalue > 21 and dealeraces > 0:
            dealerhandvalue -= 10
            dealeraces -= 1
    print('\n\n', dealercards)
    playerhandvalue1 = 0
    for i in range(len(playercards)):
        playerhandvalue1 += cardvalue(playercards1[i])
    playeraces1 = playercards1.count('cA') + playercards1.count('dA') + \
        playercards1.count('hA') + playercards1.count('sA')
    while playerhandvalue1 > 21 and playeraces1 > 0:
        playerhandvalue1 -= 10
        playeraces1 -= 1
    print('Bet: $', bet)
    if (dealerhandvalue > playerhandvalue1) and (dealerhandvalue < 22):
        print('Dealer wins.')
    elif (dealerhandvalue < playerhandvalue1) or (dealerhandvalue > 21):
        print('Player wins!')
        money += 2 * bet
    elif (dealerhandvalue == playerhandvalue1) and (len(dealercards) > len(playercards1)):
        print('Dealer wins.')
    elif (dealerhandvalue == playerhandvalue1) and (len(dealercards) < len(playercards1)):
        print('Player wins!')
        money += 2 * bet
    else:
        print("It's a tie!")
        money += bet
    print('\n$', money)
    print(playercards1)
    playerhandvalue2 = 0
    for i in range(len(playercards2)):
        playerhandvalue2 += cardvalue(playercards2[i])
    playeraces2 = playercards2.count('cA') + playercards2.count('dA') + \
        playercards2.count('hA') + playercards2.count('sA')
    while playerhandvalue2 > 21 and playeraces2 > 0:
        playerhandvalue2 -= 10
        playeraces2 -= 1
    print('Bet: $', bet)
    if (dealerhandvalue > playerhandvalue2) and (dealerhandvalue < 22):
        print('Dealer wins.')
    elif (dealerhandvalue < playerhandvalue2) or (dealerhandvalue > 21):
        print('Player wins!')
        money += 2 * bet
    elif (dealerhandvalue == playerhandvalue2) and (len(dealercards) > len(playercards2)):
        print('Dealer wins.')
    elif (dealerhandvalue == playerhandvalue2) and (len(dealercards) < len(playercards2)):
        print('Player wins!')
        money += 2 * bet
    else:
        print("It's a tie!")
        money += bet
    print('\n$', money)
    print(playercards2)
    return place, money


def play(deck, place, money):
    choice = 'p'
    bet = 1
    while choice != 'x' and money > 2 and bet != 0:
        if place > 206:
            deck = deckread(shuffle())
            place = 0
            print('The deck has been shuffled.')
        bet = 1
        error = 0
        while (bet != 0 and bet < 3) or bet > money:
            if error == 1:
                print('I\'m sorry; I couldn\'t understand that input.\nPlease provide an integer.')
            if error == 2:
                print('Are you alright? Your input still makes no sense. I need an integer.')
            if error > 2:
                print('I don\'t know how I can make myself more clear.\nProvide an integer amount to bet.')
            bet = input('\n\nHow much would you like to bet? ($) ')
            try:
                bet = int(bet)
            except:
                error += 1
                bet = 1
        if bet != 0:
            money -= bet
            rm = input('Royal Match? ')
            try:
                rm = int(rm)
            except:
                print('No wager identified, interpreting as 0.')
                rm = 0
            money -= rm
            dm = input('Dealer Match? ')
            try:
                dm = int(dm)
                money -= dm
            except:
                print('No wager identified, interpreting as 0.')
                dm = 0
            money, place, playercards, dealercards, chosen = initial_deal(deck, place, money, bet, rm, dm)
            playerhandvalue = cardvalue(playercards[0]) + cardvalue(playercards[1])
            playeraces = playercards.count('cA') + playercards.count('dA') + \
                playercards.count('hA') + playercards.count('sA')
            while playerhandvalue > 21 and playeraces > 0:
                playerhandvalue -= 10
                playeraces -= 1
            while (not chosen) and (playerhandvalue < 21):
                choice = input()
                choice = choice.casefold()
                if choice == 'h':
                    place, money, playercards = hit(deck, place, playercards, dealercards, money, bet)
                    chosen = True
                elif choice == 's':
                    chosen = True
                    place, money = stand(deck, place, playercards, dealercards, money, bet)
                elif choice == 'u':
                    chosen = True
                    place, money = split(deck, place, playercards, dealercards, money, bet)
                elif choice == 't':
                    chosen = True
                    money += bet / 2
                elif choice == 'd':
                    chosen = True
                    place, money = double_down(deck, place, playercards, dealercards, money, bet)
                elif choice == 'x':
                    chosen = True
                else:
                    print('Invalid Input: Please try again.')
    return


if __name__ == "__main__":
    play([], 311, 100)
    print('Goodbye')
    input()