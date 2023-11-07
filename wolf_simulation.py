import random
import time
import collections
import statistics
import re

##############      CONFIG      #############
## All ##
#一日目の昼のターン有効
daytime1 = "true"
#試行回数
playtime = 10000
#ゲーム内メッセージを非表示
hide_gameMsg = "true"       #"true"でメッセージ非表示

## Role ##
#人狼の数
number_of_wolf = 2
#市民の数
number_of_villager =  12
#占い師の数
number_of_fortune_teller = 1

## fortune_teller Config ##
# ft_act_pattern の詳細
# 1: 白潜伏　占い先（白）が吊られそうだったらかばう
# 2: 白潜伏　かばわない
ft_act_pattern = 1


## Color ##
class color:
    important = "\033[93m" #YELLOW
    fortune_teller = "\033[36m" #CYAN
    bold = "\033[1m"
    underline = "\033[4m"
    reset = "\033[0m"

##############      DEF      #############
def voting():
    if hide_gameMsg != "true":
        print("投票開始")
    global can_vote
    global wolf_count
    global ft_CO
    global ft_guess
    global CO_player
    voter = []
    vote_counter = 1

    while True:
        vote_wolf_count = 0
        k = 0
        for i in range(len(can_vote)):#投票先の中での人狼の数
            if playerrole[can_vote[i]] == "人狼":
                vote_wolf_count = vote_wolf_count + 1 
        
        
        for i in range(len(survivor)):#全生存者で同じ処理やってる
            voting_now = survivor[i]
            
            if ft_CO == "success": #予言COが成功したら
                if ft_guess == "success":#黒だし成功
                    if divination_result[1] == voting_now:
                        voter.append(divination_result[0])  #占い結果:divination_result, 狼の味方は身内切りをする、黒出しされた狼は占いに投票
                    else:
                        voter.append(divination_result[1])
                else:
                    if playerrole[voting_now] == "市民" or playerrole[voting_now] == "占い師":
                        while True:
                            executioner = random.randint(0,member-1)
                            if executioner != player[voting_now] and executioner in can_vote and executioner not in white_list:
                                voter.append(executioner)
                                break
                    elif playerrole[voting_now] == "人狼":
                        while True:
                            executioner = random.randint(0,member-1)
                            if playerrole[executioner] != "人狼" and executioner != player[voting_now] and executioner in can_vote and executioner not in white_list:
                                voter.append(executioner)
                                break
                            elif len(can_vote) == vote_wolf_count:
                                while True:
                                    n = random.randint(0,vote_wolf_count-1)
                                    executioner = can_vote[n]
                                    if executioner != player[voting_now]:
                                        voter.append(executioner)
                                        break
                                break

            elif playerrole[voting_now] == "市民":
                while True:
                    executioner = random.randint(0,member-1)
                    if executioner != player[voting_now] and executioner in can_vote and executioner not in white_list:
                        voter.append(executioner)
                        break
            elif playerrole[voting_now] == "占い師":
                while True:
                    if divination_result[2] == "白":
                        executioner = random.randint(0,member-1)
                        if executioner != player[voting_now] and executioner in can_vote and executioner not in white_list and executioner != divination_result[1]:
                            voter.append(executioner)
                            break
                    elif divination_result[2] == "黒":
                        voter.append(divination_result[1])
                    else:
                        executioner = random.randint(0,member-1)
                        if executioner != player[voting_now] and executioner in can_vote and executioner not in white_list:
                            voter.append(executioner)
                            break

            elif playerrole[voting_now] == "人狼":
                while True:
                    executioner = random.randint(0,member-1)
                    if playerrole[executioner] != "人狼" and executioner != player[voting_now] and executioner in can_vote:
                        voter.append(executioner)
                        break
                    elif len(can_vote) == vote_wolf_count:
                        while True:
                            n = random.randint(0,vote_wolf_count-1)
                            executioner = can_vote[n]
                            if executioner != player[voting_now]:
                                voter.append(executioner)
                                break
                        break



        last_executioner = statistics.multimode(voter)
        if hide_gameMsg != "true":
            print("投票数:",collections.Counter(voter))
        if len(last_executioner) == 1:
            voter = []
            if playerrole[last_executioner[0]] == "占い師":
                voter = []
                if hide_gameMsg != "true":
                    print(color.fortune_teller + "",last_executioner[0],": CO 占い師" + color.reset)
                if last_executioner[0] not in wolf_kill_later:
                    wolf_kill_later.append(last_executioner[0])
                ft_CO = "success"
                if last_executioner[0] not in white_list:
                    white_list.append(last_executioner[0])
                CO_player = last_executioner[0]
                vote_counter = 0
                for i in range(member):
                    if player_status[i] == 1:
                        can_vote.append(i)
            elif ft_act_pattern == 1 and player_status[divination_result[0]] == 1 and last_executioner[0] == divination_result[1] and divination_result[2] == "白":
                voter = []
                if hide_gameMsg != "true":
                    print(color.fortune_teller + "",divination_result[0],": CO 占い師",divination_result[1],"→",divination_result[2],"" + color.reset)
                if last_executioner[0] not in wolf_kill_later:
                    wolf_kill_later.append(divination_result[1])
                if divination_result[0] not in wolf_kill_later:
                    wolf_kill_later.append(divination_result[0])
                ft_CO = "success"
                if last_executioner[0] not in white_list:
                    white_list.append(divination_result[1])
                if divination_result[0] not in white_list:
                    white_list.append(divination_result[0])
                CO_player = last_executioner[0]
                vote_counter = 0
                for i in range(member):
                    if player_status[i] == 1:
                        can_vote.append(i)
            else:

                break
        elif len(last_executioner) == 2 and divination_result[0] in last_executioner and divination_result[1] in last_executioner and divination_result[2] == "白":
            voter = []
            if hide_gameMsg != "true":
                print(color.fortune_teller + "",divination_result[0],": CO 占い師",divination_result[1],"→",divination_result[2],"" + color.reset)
            if last_executioner[0] not in wolf_kill_later:
                wolf_kill_later.append(last_executioner[0])
            if divination_result[0] not in wolf_kill_later:
                wolf_kill_later.append(divination_result[0])
            ft_CO = "success"
            if last_executioner[0] not in white_list:
                white_list.append(last_executioner[0])
            if divination_result[0] not in white_list:
                white_list.append(divination_result[0])
            CO_player = last_executioner[0]
            vote_counter = 0
            for i in range(member):
                if player_status[i] == 1:
                    can_vote.append(i)
        elif vote_counter >= 3:
            voter = []
            break
        else:
            if hide_gameMsg != "true":
                print(last_executioner)
            can_vote=[]
            for ii in range(len(last_executioner)):
                can_vote.append(last_executioner[ii])            #投票可能リストを決選投票の対象に入れ替える
            if hide_gameMsg != "true":
                print("決選投票")
            voter = []
            vote_counter = vote_counter + 1

    for i in range(len(last_executioner)):
        if hide_gameMsg != "true":
            print(player[last_executioner[i]],"が処刑された。")
        player_status[last_executioner[i]] = 0
        survivor.remove(last_executioner[i])
        if last_executioner[i] in can_divine:
            can_divine.remove(last_executioner[i])
    for i in range(member):
        if player_status[i] == 1:
            can_vote.append(i)

    victory_dic()
    ft_CO = ""
    ft_guess = ""
    can_vote=[]
    if hide_gameMsg != "true":
        print()


def wolf_act():
    global wolf_kill
    global survivor
    global wolf_alive
    global wolf_kill_dicide
    for i in range(wolf_alive):
        if len(wolf_kill_later) >= 1:
            for ii in range(len(wolf_kill_later)):
                if wolf_kill_dicide == 0:
                    if playerrole[wolf_kill_later[ii]] == "占い師" and wolf_kill_dicide == 0:
                        wolf_kill = wolf_kill_later[ii]
                        wolf_kill_later.remove(wolf_kill_later[ii])
                        wolf_kill_dicide = 1
            for ii in range(len(wolf_kill_later)):
                if wolf_kill_dicide == 0:
                    if playerrole[wolf_kill_later[ii]] == "霊媒師" and wolf_kill_dicide == 0:
                        wolf_kill = wolf_kill_later[ii]
                        wolf_kill_later.remove(wolf_kill_later[ii])
                        wolf_kill_dicide = 1
            for ii in range(len(wolf_kill_later)):
                if wolf_kill_dicide == 0:
                    if playerrole[wolf_kill_later[ii]] == "狩人":
                        wolf_kill = wolf_kill_later[ii]
                        wolf_kill_later.remove(wolf_kill_later[ii])
                        wolf_kill_dicide = 1
            for ii in range(len(wolf_kill_later)):
                if wolf_kill_dicide == 0:
                    if playerrole[wolf_kill_later[ii]] == "市民":
                        wolf_kill = wolf_kill_later[ii]
                        wolf_kill_later.remove(wolf_kill_later[ii])
                        wolf_kill_dicide = 1

            player_status[wolf_kill] = 0
            survivor.remove(wolf_kill)
            killed_player_by_wolf.append(wolf_kill)
            wolf_kill_dicide = 0
            if wolf_kill in can_divine:
                can_divine.remove(wolf_kill)
        else:
            while True:
                wolf_kill = random.randint(0,member-1)
                if playerrole[wolf_kill] != "人狼" and player_status[wolf_kill] == 1:
                    player_status[wolf_kill] = 0
                    survivor.remove(wolf_kill)
                    killed_player_by_wolf.append(wolf_kill)
                    if wolf_kill in can_divine:
                        can_divine.remove(wolf_kill)
                    break
    for i in range(member):
        if player_status[i] == 1:
            can_vote.append(player[i])
    if hide_gameMsg != "true":
        print()


def fortune_teller_act():
    global can_divine
    global fortune_teller_alive
    global be_divined
    for i in range(len(survivor)):
        if playerrole[survivor[i]] == "占い師":
            divination_result[0] = survivor[i]
            n = random.randint(0,len(can_divine)-1)   #占い先をリスト[can_divine]からランダムに決定
            be_divined = can_divine[n]
            divination_result[1] = be_divined
            if playerrole[be_divined] == "人狼":
                divination_result[2] = "黒"
            else:
                divination_result[2] = "白"
            if be_divined in can_divine:
                can_divine.remove(be_divined)     #今回の占い先をリストから削除（重複回避）
            if hide_gameMsg != "true":
                print("(",divination_result[0],"占い先:",divination_result[1],"→",divination_result[2],")")



def victory_dic():
    global wolf_alive
    global innocent_alive
    global game_condition
    global wolf_win
    global innocent_win
    global villager_alive
    global fortune_teller_alive
    wolf_alive = 0
    innocent_alive = 0
    villager_alive = 0
    fortune_teller_alive = 0
    for i in range(member):
        if playerrole[i] == "人狼":
            if player_status[i] == 1:
                wolf_alive = wolf_alive + 1
        elif playerrole[i] == "市民":
            if player_status[i] == 1:
                innocent_alive = innocent_alive + 1
                villager_alive = villager_alive + 1
        elif playerrole[i] == "占い師":
            if player_status[i] == 1:
                innocent_alive = innocent_alive + 1
                fortune_teller_alive = fortune_teller_alive + 1

    if hide_gameMsg != "true":
        print("生存:",survivor)
    if wolf_alive == 0:
        if hide_gameMsg != "true":
            print("市民陣営の勝利")
            print("------------------------------------------------")
        innocent_win = innocent_win + 1
        game_condition = 0
    elif wolf_alive >= innocent_alive:
        if hide_gameMsg != "true":
            print("人狼陣営の勝利")
            print("------------------------------------------------")
        wolf_win = wolf_win + 1
        game_condition = 0


##############      MAIN      #############
wolf_win = 0
innocent_win = 0
C1 = []
for i in range(3):
    C1.append(1)
print("実行中...")
for z in range(playtime):
    if round(z/playtime*100) == 20 and C1[0] == 1:
        print("25%完了")
        C1[0] = 0
    if round(z/playtime*100) == 50 and C1[1] == 1:
        print("50%完了")
        C1[1] = 0
    if round(z/playtime*100) == 75 and C1[2] == 1:
        print("75%完了")
        C1[2] = 0

    role = []
    for i in range(number_of_wolf):
        role.append("人狼")
    for i in range(number_of_villager):
        role.append("市民")
    for i in range(number_of_fortune_teller):
        role.append("占い師")
    member = len(role)
    lst = list(range(0,member))
    random.shuffle(lst)
    ft_CO = ""
    ft_guess = ""
    CO_player = 0
    player = []
    survivor = []
    day = 1
    player_status = []
    playerrole = []
    white_list = []
    wolf_count = 0
    killed_player_by_wolf = []
    wolf_alive = 0
    innocent_alive = 0
    villager_alive = 0
    fortune_teller_alive = 0
    wolf_kill_later = []
    wolf_kill_dicide = 0
    can_vote = []
    can_divine = []
    be_divined = 0
    game_condition = 1
    divination_result = [-1,-1,""]  #[占い師のプレイヤー(member)番号,占い先のプレイヤー番号,判定]
    for i in range(member):
        player.append(i)
        player_status.append(1)
        playerrole.append(1)
        can_vote.append(i)
        survivor.append(i)


    for i in range(member):
        playerrole[i] = role[lst[i]] #役職配布
        if playerrole[i] == "人狼":
            wolf_count = wolf_count + 1
        if playerrole[i] != "占い師":
            can_divine.append(player[i])
        if hide_gameMsg != "true":
            print(player[i],":",playerrole[i],end=" ")
    if hide_gameMsg != "true":
        print()
        print("----------------------------------------")


    if daytime1 == "true":
        if hide_gameMsg != "true":
            print(day,"日目昼")
        voting()


    while game_condition == 1:
        if hide_gameMsg != "true":
            print(day,"日目夜")
        if number_of_fortune_teller >= 1:
            fortune_teller_act()
        wolf_act()
        day = day + 1
        if hide_gameMsg != "true":
            print(day,"日目昼")
        for i in range(len(killed_player_by_wolf)):
            if hide_gameMsg != "true":
                print(player[killed_player_by_wolf[i]],"が人狼の襲撃に逢いました。")
        killed_player_by_wolf = []
        victory_dic()
        if game_condition == 0:
            break
        if divination_result[2] == "黒" and player_status[divination_result[0]] == 1:
            if hide_gameMsg != "true":
                print(color.fortune_teller + "",divination_result[0],": CO 占い師 「",divination_result[1],"→",divination_result[2],"」" + color.reset)

            ft_CO = "success"
            ft_guess = "success"
            if divination_result[0] not in wolf_kill_later:
                wolf_kill_later.append(divination_result[0])
            if divination_result[0] not in white_list:
                white_list.append(divination_result[0])
        voting()




print("100%完了")
print("-------------------------------------------------------------------------------")
print(color.important + color.bold + "試行回数:",playtime)
print("人狼の勝率:",round(wolf_win/playtime*100,1),"%")
print("市民の勝率:",round(innocent_win/playtime*100,1),"%" + color.reset)



#Comprete
#10/27 14:25 占い師　かばう機能　デバッグ中
#ToDO

#狼2市民11 試行10000　:　78.2 78.9 77.7 78.0 79.1
#(白占い無潜伏パターン)
#(狼対抗COパターン)

#人狼2市民12
#試行回数: 1000000
#人狼の勝率: 78.2 %
#市民の勝率: 21.8 %






