import requests, json
import time
from datetime import datetime
from statistics import mean
home_points, away_points, overall_points, positions, performance_home, performance_home_, performance_away = [], [], [], [], [], [], []
ids, names, bets, kendi_aralarinda, kendi_aralarinda_odds, kendi_aralarinda_ort, home_scors, away_scors, alt_ust, home_odds, away_odds, temp_pid, pid= [], [], [], [], [], [], [], [], [], [], [], [], []
vals = {}
comp_date = datetime(2020, 12, 1)
txt = "NBA-" + str(round(time.time() * 1000)) + ".txt"
url = "https://apivx.misli.com/api/web/v1/sportsbook/event/0?sportType=BASKETBALL&betType=PRE_EVENT"
response = requests.get(url)
json_value = response.json()

#JSON data okuma
for i in range(len(json_value['data']['e']) - 1):
    temp_a = []
    if json_value['data']['e'][i]['cp'] == 138:
        temp_a.append(json_value['data']['e'][i]['p'][0]['n'])
        temp_a.append(json_value['data']['e'][i]['p'][1]['n'])
        names.append(temp_a)
        ids.append(json_value['data']['e'][i]['i'])
#JSON performans kısmını okuma
for i in range(len(ids)):
    url = "https://apivx.misli.com/api/web/v1/statistics/match/" + str(ids[i]) + "/performance"
    response = requests.get(url)
    json_value = response.json()
    performance_home.append(json_value['data']['homeTeam'])
    performance_away.append(json_value['data']['awayTeam'])
#Ev sahibi ev sahibi iken performans istatistik hesaplama
for i in range(performance_home.__len__()):
    temp_array = []
    for j in range(performance_home[i].__len__()):
        performance_home_ = json.dumps(performance_home[i][j])
        home_final = json.loads(performance_home_)
        mili_date = home_final['d']
        conv_date = datetime \
            .strptime((datetime
                       .fromtimestamp(int(mili_date) / 1000.0)
                       .strftime('%Y-%m-%d')), '%Y-%m-%d')
        if conv_date > comp_date:
            temp_scor_home = home_final['ht']['s']['r']
            temp_scor_away = home_final['at']['s']['r']
            total = temp_scor_away + temp_scor_home
            temp_array.append(total)
    home_scors.append(temp_array)
#Deplasman deplasman iken sahibi performans istatistik hesaplama
for i in range(performance_away.__len__()):
    temp_array = []
    for j in range(performance_away[i].__len__()):
        performance_home_ = json.dumps(performance_away[i][j])
        home_final = json.loads(performance_home_)
        mili_date = home_final['d']
        conv_date = datetime \
            .strptime((datetime
                       .fromtimestamp(int(mili_date) / 1000.0)
                       .strftime('%Y-%m-%d')), '%Y-%m-%d')
        if conv_date > comp_date:
            temp_scor_home = home_final['ht']['s']['r']
            temp_scor_away = home_final['at']['s']['r']
            total = temp_scor_away + temp_scor_home
            temp_array.append(total)
    away_scors.append(temp_array)
#Takım ID lerini ayıklama
for i in range(len(ids)):
    temp_pid = []
    url = "https://apivx.misli.com/api/web/v1/sportsbook/event/" + str(ids[i]) + "/single"
    response = requests.get(url)
    json_value = response.json()
    bets.append(json_value['data'])
    temp_pid.append(json_value['data']['phid'])
    temp_pid.append(json_value['data']['paid'])
    pid.append(temp_pid)
bets = json.dumps(bets)
bets = json.loads(bets)
# IDlernden NBA olanları ayıklama 114 = NBA-ID
for i in range(bets.__len__()):
    temp_array = []
    for j in range(len(bets[i]['m'])):
        if bets[i]['m'][j]['st'] == 114:
            temp_array.append(bets[i]['m'][j]['ov'])
    temp_array.sort()
    alt_ust.append(temp_array)
#Ev sahibi sezonun tüm maçlarının skor istatistiği
for i in range(home_scors.__len__()):
    temp_odds = []
    temp_odds.clear()
    for j in range(alt_ust[i].__len__()):
        temp_odds.append(0)
    for l in range(home_scors[i].__len__()):
        for k in range(alt_ust[i].__len__()):
            if home_scors[i][l] >= alt_ust[i][k]:
                 temp_odds[k] += 1
    for t in range(temp_odds.__len__()):
        temp_odds[t] = int((temp_odds[t] / home_scors[i].__len__()) * 100)
    home_odds.append(temp_odds)
#Deplasman sezonun tüm maçları skor istatistiği
for i in range(away_scors.__len__()):
    temp_odds = []
    temp_odds.clear()
    for j in range(alt_ust[i].__len__()):
        temp_odds.append(0)
    for l in range(away_scors[i].__len__()):
        for k in range(alt_ust[i].__len__()):
            if away_scors[i][l] >= alt_ust[i][k]:
                 temp_odds[k] += 1
    for t in range(temp_odds.__len__()):
        temp_odds[t] = int((temp_odds[t] / away_scors[i].__len__()) * 100)
    away_odds.append(temp_odds)
#Kazanma yüzdesihesaplama
for k in range(ids.__len__()):
    url = "https://apivx.misli.com/api/web/v1/statistics/match/" + str(ids[k]) + "/standing"
    response = requests.get(url)
    json_value = response.json()
    temp_position = []
    null = ["null", "null"]
    if json_value['data'] is not None:
        for l in range(pid[k].__len__()):
            for h in range(len(json_value['data']['standings']['OVERALL'])):
                if pid[k][l] == json_value['data']['standings']['OVERALL'][h]['team']['id']:
                    a = json_value['data']['standings']['OVERALL'][h]['won']
                    b = json_value['data']['standings']['OVERALL'][h]['played']
                    temp = int((a / b) * 100)
                    temp_position.append(temp)
        positions.append(temp_position)
    else:
        positions.append(null)
    try:
        for i in range(len(json_value['data']['standings']['HOME'])):
            for j in range(pid.__len__()):
                if json_value['data']['standings']['HOME'][i]['team']['id'] == pid[j][0]:
                    home_points.append(int(int(json_value['data']['standings']['HOME'][i]['scored'])
                                           / int(json_value['data']['standings']['HOME'][i]['played'])))
        for i in range(len(json_value['data']['standings']['AWAY'])):
            for j in range(pid.__len__()):
                if json_value['data']['standings']['AWAY'][i]['team']['id'] == pid[j][1]:
                    away_points.append(int(int(json_value['data']['standings']['AWAY'][i]['scored'])
                                           / int(json_value['data']['standings']['AWAY'][i]['played'])))
    except:
        home_points.append("null")
        away_points.append("null")
#Kendi aralarında sezonda oynanan maçların ortalama sayılarını hesaplama
for i in range(len(ids)):
    temp_kendi_aralarinda = []
    temp_kendi_aralarinda_ort = [0, 0]

    away, home , calc = 0, 0, 0
    url = "https://apivx.misli.com/api/web/v1/statistics/match/" + str(ids[i]) + "/head-to-head"
    response = requests.get(url)
    json_value = response.json()
    for j in range(len(json_value['data'])):
        mili_date = json_value['data'][j]['date']
        conv_date = datetime \
            .strptime((datetime
                       .fromtimestamp(int(mili_date) / 1000.0)
                       .strftime('%Y-%m-%d')), '%Y-%m-%d')
        if conv_date > comp_date:
            calc += 1
            temp_kendi_aralarinda.append(int(json_value['data'][j]['homeTeamFullTimeScore']
                                         + json_value['data'][j]['awayTeamFullTimeScore']))
            if json_value['data'][j]['homeTeamCurrentSide'] == "AWAY":
                temp_kendi_aralarinda_ort[0] += int(json_value['data'][j]['awayTeamFullTimeScore'])
                temp_kendi_aralarinda_ort[1] += int(json_value['data'][j]['homeTeamFullTimeScore'])
            else:
                temp_kendi_aralarinda_ort[0] += int(json_value['data'][j]['homeTeamFullTimeScore'])
                temp_kendi_aralarinda_ort[1] += int(json_value['data'][j]['awayTeamFullTimeScore'])
    if calc != 0:
        temp_kendi_aralarinda_ort[0] /= calc
        temp_kendi_aralarinda_ort[1] /= calc
    kendi_aralarinda_ort.append(temp_kendi_aralarinda_ort)
    if not temp_kendi_aralarinda:
        temp_kendi_aralarinda.append(0)
    kendi_aralarinda.append(temp_kendi_aralarinda)
#Kendi aralarında hesaplanan sayıların oynanacak maçtaki bahislere göre kazanma yüzdesi (ALt-Üst)
for i in range(kendi_aralarinda.__len__()):
    temp_odds = []
    temp_odds.clear()

    for j in range(alt_ust[i].__len__()):
        temp_odds.append(0)

    for l in range(kendi_aralarinda[i].__len__()):
        for k in range(alt_ust[i].__len__()):
            if kendi_aralarinda[i][l] >= alt_ust[i][k]:
                temp_odds[k] += 1

    for t in range(temp_odds.__len__()):
        try:
            temp_odds[t] = int((temp_odds[t] / kendi_aralarinda[i].__len__()) * 100)
        except:
            temp_odds[t] = 0
    kendi_aralarinda_odds.append(temp_odds)
#txt dosyasına yazdırma
def txt_write():
    f = open(txt, "w")
    f.write(str(datetime.now()) + "\n")
    for i in range(names.__len__()):
        f.write("---------------------------------------\n")
        f.write(names[i][0] + " - " + names[i][1] +"\n")
        f.write("---------------------------------------\n")
        for j in range(names[i].__len__()):
            f.write(str(names[i][j]) + "\nGenel kazanma orani= %" + str(positions[i][j]) + "\n")
            for gggg in alt_ust[i]:
                f.write(str(gggg) + " - ")
            f.write(" => Baremler\n")
            if j == 0:
                for gg in home_odds[i]:
                    f.write("  %" + str(gg) + " - ")
                f.write(" => Ust olma olasiligi")
                f.write("\nEvinde attigi ortalama sayi = " + str(home_points[i]))
                if kendi_aralarinda_ort[i][j] != 0:
                    f.write("\nRakip takima attigi ortalama sayi = " + str(kendi_aralarinda_ort[i][j]))
                else:
                    f.write("\nRakip takima attigi ortalama sayi = Aralarindaki ilk mac")
                f.write("\n\n")
            else:
                for ggg in away_odds[i]:
                    f.write("  %" + str(ggg) + " - ")
                f.write(" => Ust olma olasiligi\n")
                f.write("Deplasmanda attigi ortalama sayi = " + str(away_points[i]))
                if kendi_aralarinda_ort[i][j] != 0:
                    f.write("\nRakip takima attigi ortalama sayi = " + str(kendi_aralarinda_ort[i][j]))
                else:
                    f.write("\nRakip takima attigi ortalama sayi = Aralarindaki ilk mac\n")
        if kendi_aralarinda[i][0] != 0:
            f.write("\n\nKendi aralarinda attiklari toplam sayilar\n")
        for g2 in kendi_aralarinda[i]:
            if kendi_aralarinda[i][0] != 0:
                f.write(str(g2) + " - ")
            else:
                break
        if kendi_aralarinda_ort[i][0] != 0:
            temp = mean(kendi_aralarinda[i])
            f.write("\nKendi aralarinda atilan ortalama sayi = " + str(temp))
            f.write("\n\nKendi aralarinda oynanan maclara gore olasiliklar\n")
            for gggg in alt_ust[i]:
                f.write(str(gggg) + " - ")
            f.write(" => Baremler\n")
            for g3 in kendi_aralarinda_odds[i]:
                f.write("  %" + str(g3) + " - ")
            f.write(" => Ust olma olasiligi\n")
            f.write("\n\n")
    f.close()
txt_write()
print("Finish...")
