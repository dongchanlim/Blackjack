import random
import pandas as pd
import numpy as np

# Initial entire Card Deck (블랙잭 카드 구성하기)
symbols = [i for i in range(2,11)] * 4 + ['A','J','Q','K'] * 4
numbers = [i for i in range(2,11)] * 4 + [11, 10, 10, 10] * 4
deck = list(map(list, zip(symbols, numbers)))

# Card Pack that player or dealer has in hand (플레이어 & 딜러에 있는 카드 덱 구성하기)
class Pack:
    
    def __init__(self):
        # 덱에서 랜덤으로 두장 뽑기 (팩)
        self.pack = random.choices(deck, k = 2)
        # 카드 그림 
        self.symbol = [i[0] for i in self.pack]
        # 카드 합계
        self.sum = sum([i[1] for i in self.pack])
        # 블랙잭인지 체크
        self.blackjack = False
        # 21인지 체크
        self.twentyone = False
        # 카드 합계가 21이 넘는지 체크
        self.over_21 = False
        # 추가한 카드숫자
        self.adding_card = 0
        
class Player:
    
    def __init__(self, name):
        self.pack = Pack()
        # 승/패 체크
        self.lose = False
        # 플레이어 이름 정하기
        self.name = name
        
        
        
class Dealer:
    
    def __init__(self):
        self.pack = Pack()
        self.lose = False
        self.name = 'Dealer'
        
class Blackjack:
    
    def __init__(self, who_play, play_money):
        # 덱에서 카드 추가 뽑기위해 필요함
        self.cards = deck
        # 플레이어 이름 정하기
        self.player_name = who_play
        # 플레이 머니 정하기
        self.play_money = play_money
        # 플레이어와 딜러 오브젝트 만들기
        self.player = Player(self.player_name)
        self.dealer = Dealer() 
        # 히트할지 스탑할지 정하기
        self.hit_stop = False
        # 게임을 멈출지 안멈출지 정하기
        self.game_stop = False
    
    # 플레이어의 현재 플레이 머니를 보여준다
    def display_current_play_money(self):
        print("Play Money : ${}".format(self.play_money))
        
    # 플레이어 또는 딜러 (target) 의 현재 카드 상황을 보여준다
    def display_current_card(self, target):
        if target == self.player:
            print("{}: {}, sum: {}".format(target.name, target.pack.symbol, target.pack.sum))
        # 딜러의 카드 하나는 뒤집은 상태에서 나머지 카드들만 보여준다
        elif target == self.dealer:
            print("Dealer: {}, sum: ?".format(target.pack.symbol[:-1] + ["?"]))

    # check whether target (Player or Dealer)'s card is bust (over 21) or 21 (blackjack)
    def check_bust_21(self, target):
        # 카드 합계가 21일때 블랙잭인지 21인지 정한다
        self.choose_blackjack_21(target)
        # ACE 숫자 정하기
        self.choose_a_number(target)
        if target.pack.sum >= 21:
            if target.pack.sum > 21:
                target.pack.over_21 = True
            # self.game_stop 과 연결되어 게임을 계속 할지 중단할지를 결정한다
            return True
        else:
            return False
        
    # 합계가 21일때 블랙잭인지 21인지를 구별한다   
    def choose_blackjack_21(self, target):
        if target.pack.sum == 21:
            if target.pack.adding_card == 0:
                target.pack.blackjack = True
            else:
                target.pack.twentyone = True
                
    def choose_a_number(self, target):
        if target.pack.blackjack or target.pack.twentyone:
            pass
        elif target.pack.adding_card == 0:
            self.first_choose_a_number(target)
        else:
            self.adding_card_choose_a_number(target)
        
    def adding_card_choose_a_number(self, target):
        for i in target.pack.symbol[1 + target.pack.adding_card: 2 + target.pack.adding_card]:
            if i == 'A':
                # 'Ace'의 값이 11일때 21이 넘으면 자동으로 값을 1로 바꾼다
                if target.pack.sum > 21:
                    target.pack.sum -= 10
                elif target == self.player:
                    loop = True
                    while loop:
                        number_a = input("Choose A Number - 1 or 11?: ")
                        if int(number_a) == 1:
                            target.pack.sum -= 10   
                            loop = False
                        elif int(number_a) == 11:
                            loop = False
                elif target == self.dealer:
                        if target.pack.sum < 17:
                            target.pack.sum -= 10
        # Choose the number for 'Ace' card - 1 or 11
    def first_choose_a_number(self, target):
        for i in target.pack.symbol:
            if i == 'A':
                if target.pack.sum > 21:
                    target.pack.sum -= 10
                # 플레이어의 경우 'Ace' 일때 1 일지 11 일지 정할수 있다
                elif target == self.player:
                    loop = True
                    while loop:
                        number_a = int(input("Choose A Number - 1 or 11?: "))
                        if number_a == 1:
                            target.pack.sum -= 10
                            print()
                            self.display_current_card(target)
                            loop = False
                        elif number_a == 11:
                            print()
                            self.display_current_card(target)
                            loop = False
                # 딜러의 경우 'Ace' 일때 합이 17보다 작으면 무조건 1 로 계산한다
                elif target == self.dealer:
                    if target.pack.sum < 17:
                        target.pack.sum -= 10

    # hit 또는 stop을 결정한다 (다른 명령어 입력시 다시 입력한다)
    def choose_hit_stay(self, choice):
        if choice.upper() == 'H':
        # When player hit, add addtional card
            print("\nAdding one more card for player")
            self.adding_card(self.player)
            # 히트한 후의 플레이어의 카드가 버스트 이거나 21일때 게임을 종료한다 
            self.game_stop = self.check_bust_21(self.player)
            # 히트한 후의 플레이어/ 딜러의  현재 카드 상황을 보여준다
            for i in [self.player, self.dealer]:
                self.display_current_card(i)
            if self.game_stop:
                self.hit_stop = True
        # 다른 명령어 입력시 다시 입력한다
        elif choice.upper() == 'S':
            self.hit_stop = True
        
        else:
            print("Incorrect Input. Please type correctly.")
            
    # Giving one more card to target (player or dealer)
    def adding_card(self, target):
        new_pack = random.choice(deck)
        target.pack.symbol.append(new_pack[0])
        target.pack.sum += new_pack[1]
        # 추가 카드 숫자 증가
        target.pack.adding_card += 1
    
    # Choose whether to split or not (only for player)
    def choose_split(self):
        pass

    
    # 플레이어와 딜러 (target) 의 최종 카드 상황을 보여준다
    def display_final_card(self):
        for i in [self.player, self.dealer]:
            print("{}: {}, sum: {}".format(i.name, i.pack.symbol, i.pack.sum))
        
    def play_game(self):
        print("-Table-")
        # 처음 카드 상황을 보여준다
        for i in [self.player, self.dealer]:
            self.display_current_card(i)
        # 한 세트가 끝날때 까지 (게임이 중단되기 까지) 모든 과정을 반복한다
        while not self.game_stop:
            for i in [self.player, self.dealer]:
                # 플레이어와 딜러의 처음 카드가 버스트이거나 블랙잭인지 확인한다. 맞다면 게임을 중단한다
                self.game_stop = self.check_bust_21(i)
                if self.game_stop:
                    break
            # 플레이어 hit / stop 선택하기
            choice = ''
            # 플레이어가 스탑을 선택하기 전까지 카드를 추가하기 (다른 명령어 입력시 다시 입력할수 있게 하기)
            while not self.game_stop and not self.hit_stop:
                choice = input("\nPlayer Hit or Stay? (H/S): ")
                self.choose_hit_stay(choice)
            if self.game_stop:
                break
            # 플레이어가 스탑을 선택하고 딜러의 카드의 합계가 17 이상이 될때까지 카드를 추가하기
            while self.hit_stop and self.dealer.pack.sum < 17:
                print("\nAdding one more card for dealer")
                self.adding_card(self.dealer)
                self.game_stop = self.check_bust_21(self.dealer)
                for i in [self.player, self.dealer]:
                    self.display_current_card(i)
                if self.game_stop:
                    break
            self.game_stop = True
        # 최종결과 보여주기 (승/패 결정하기)
        self.display_final_result()
    
    # Show the final card pack and sum for both and who wins the game
    def display_final_result(self):
        # 게임이 끝나면 결과에 따라 결과 보여주기
        print("\n-Final Result-")
        # 플레이어 / 딜러 최종 카드 결과 보여주기
        self.display_final_card()
        print()
        # 카드 결과에 따라 플레이어 / 딜러 승패 정하기
        # 블랙잭이거나 버스트이거나 21일때 승패 정하기
        if self.dealer.pack.blackjack:
            print("Blackjack\nDealer win!")
            self.player.lose = True
        elif self.player.pack.blackjack:
            print("Blackjack\nPlayer win! ")
            self.dealer.lose = True
        elif self.player.pack.twentyone:
            print("21!\nPlayer win!")
            self.dealer.lose = True
        elif self.dealer.pack.twentyone:
            print("21!\nDealer win!")
            self.player.lose = True
        elif self.player.pack.blackjack and self.dealer.pack.blackjack:
            print("Push! Draw!")
        elif self.dealer.pack.over_21:
            print("Since number is over 21\nPlayer win!")
            self.dealer.lose = True
        elif self.player.pack.over_21:
            print("Since number is over 21\nDealer win!")
            self.player.lose = True
        # 21 / 블랙잭 / 버스트 가 아닐때 카드 합계를 비교하여 승패 정하기
        elif not self.dealer.lose and not self.player.lose:
            if self.dealer.pack.sum > self.player.pack.sum:
                print("Dealer win!")
                self.player.lose = True
            elif self.dealer.pack.sum < self.player.pack.sum  :
                print("Player win!")
                self.dealer.lose = True
            else:
                print("Draw!")
        self.display_current_play_money()
                

class B_history:
    # 지금까지의 세트들의 오브젝트를 기록한다
    def __init__(self):
        #기록 번호 
        self.number = 1
        self.history = dict()
        self.array = list()
        self.columns = ['player name', 'player lose', 'dealer lose', 'player sum', 'dealer sum',\
                        'player adding card', 'dealer adding card', 'player blackjack',\
                        'dealer blackjack', 'player 21', 'dealer 21']
        
    def add_new_history(self, blackjack):
        # 기록을 추가한다 
        self.history.update({self.number:blackjack})
        self.number += 1
        
    def make_history_df(self):
        history_num = self.history.keys()
        for j in self.history.values():
            self.array.append([j.player.name, j.player.lose, j.dealer.lose,\
                               j.player.pack.sum, j.dealer.pack.sum, j.player.pack.adding_card,\
                               j.dealer.pack.adding_card, j.player.pack.blackjack, \
                               j.dealer.pack.blackjack, j.player.pack.twentyone, j.dealer.pack.twentyone])
        df = pd.DataFrame(np.array(self.array), columns = self.columns, index = history_num)
        return df
    
    def display_game_history(self):
        print("- Record - ")
        df = self.make_history_df()
        pd.set_option('display.max_columns', 15)
        # csv 파일로 전환하기
        # 1. csv 파일 생성하기
        df.to_csv('C:/Users/dchan/Desktop/blackjack.csv', encoding='utf-8')
        # 2. csv 파일에 행 추가하기
        # df.to_csv('C:/Users/dchan/Desktop/blackjack.csv', mode='a', header=False)
        print(df)
    
def main():
    game_history = B_history()
    player_name = input("Who is going to play?: ")
    player_money = int(input("How much do you want to play($)?: "))
    # 배팅머니를 뺀다
    player_money -= 5
    blackjack = Blackjack(player_name, player_money)
    print("Game Number - game {}".format(game_history.number))
    # 게임(세트)을 시작한다
    blackjack.play_game()
    # 세트가 끝날때마다 기록을 추가한다
    game_history.add_new_history(blackjack)
    play_again = input("\nStill want to play? (Y/N): ")
    print()
    while play_again.upper() != 'N':
        if play_again.upper() == 'Y':
            print("Game Number - game {}".format(game_history.number))
            player_money -= 5
            blackjack = Blackjack(player_name, player_money)
            blackjack.play_game()
            game_history.add_new_history(blackjack)
        else:
            print("Incorrect Input. Please type correctly.")
        play_again = input("\nStill want to play? (Y/N): ")
        print()
    # 전체 세트들의 기록을 보여준다
    game_history.display_game_history()

if __name__ == '__main__':
    main()
        