'''3. За корисникот внесен на влез да се препорача филм. Да се користи Пирсонов коефициент на корелација
како мерка. Ако корисникот го нема во базата да се препорача најгледаниот филм. Доколку корисникот има
гледано повеќе од 5 филмови, да се препорача според филмовите, во спротивно да се препорача според
корисниците кои се слични со него'''
from __future__ import print_function
import json
from math import sqrt

# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {'Catch Me If You Can': 3.0, 'Snakes on a Plane': 3.5, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0, 'Snitch': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'The Night Listener': 3.0,
                     'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Catch Me If You Can': 2.5, 'Lady in the Water': 2.5, 'Superman Returns': 3.5,
                         'The Night Listener': 4.0, 'Snitch': 2.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Catch Me If You Can': 4.5, 'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'Snitch': 4.5},
    'Toby': {'Snakes on a Plane': 4.5, 'Snitch': 5.0},
    'Michelle Nichols': {'Just My Luck': 1.0, 'The Night Listener': 4.5, 'You, Me and Dupree': 3.5,
                         'Catch Me If You Can': 2.5, 'Snakes on a Plane': 3.0},
    'Gary Coleman': {'Lady in the Water': 1.0, 'Catch Me If You Can': 1.5, 'Superman Returns': 1.5,
                     'You, Me and Dupree': 2.0},
    'Larry': {'Lady in the Water': 3.0, 'Just My Luck': 3.5, 'Snitch': 1.5, 'The Night Listener': 3.5}
}


def sim_pearson(oceni, p1, p2):
    # Se kreira recnik vo koj ke se cuvaat predmetite (filmovi) koi se oceneti od dvajcata
    # Vo recnikot ni se vazni samo klucevite za da gi cuvame iminjata na filmovite koi se zaednicki, a vrednostite ne ni se vazni
    zaednicki = set()
    for item in oceni[p1]:
        if item in oceni[p2]:
            zaednicki.add(item)

    # Se presmetuva brojot na predmeti oceneti od dvajcata
    n = len(zaednicki)

    # Ako nemaat zaednicki predmeti vrati korelacija 0
    if n == 0: return 0

    # Soberi gi zaednickite oceni (rejtinzi) za  sekoja licnost posebno
    sum1 = 0
    sum2 = 0

    # Soberi gi kvadratite od zaednickite oceni (rejtinzi) za  sekoja licnost posebno
    sum1Sq = 0
    sum2Sq = 0

    # Soberi gi proizvodite od ocenite na dvete licnosti
    pSum = 0
    for item in zaednicki:
        ocena1 = oceni[p1][item]
        ocena2 = oceni[p2][item]
        sum1 += ocena1
        sum1Sq += ocena1 ** 2
        sum2 += ocena2
        sum2Sq += ocena2 ** 2
        pSum += ocena1 * ocena2

    # Presmetaj go koeficientot na korelacija
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r
def topMatches(oceni, person, n=5, similarity=sim_pearson):
    scores = []
    for person2 in oceni.keys():
        if person != person2:
            s = similarity(oceni, person, person2)
            scores.append((s, person2))
    # Se sortira listata vo rastecki redosled
    scores.sort()
    # Se prevrtuva za najslicnite (so najgolema vrednost) da bidat prvi
    scores.reverse()
    if n is None:
        return scores
    else:
        return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}

    for other in prefs.keys():

        if other == person: continue

        sim = similarity(prefs, person, other)

        if sim <= 0: continue

        for item in prefs[other]:
            if item not in prefs[person]:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = []
    for item, total in totals.items():
        sim_total = simSums[item]

        my_score = round(total / sim_total, 1)

        rankings.append((my_score, item))

    rankings.sort(reverse=True)
    return rankings

def transformoceni(oceni):
    result = {}
    for person in oceni.keys():
        for item in oceni[person]:
            result.setdefault(item, {})
            # Zameni gi mestata na licnosta i predmetot
            result[item][person] = oceni[person][item]
    return result

def item_based(critics, person1, n=3):
    oceni_po_film = transformoceni(critics)
    similarity_per_item = {}
    for item in critics[person1].keys():
        similar_items = topMatches(oceni_po_film, item, n=None)
        my_rating = critics[person1][item]

        for similarity, item2 in similar_items:
            if item2 in critics[person1] or similarity <= 0:
#                 print('Slicnost', similarity, 'na', item,'so', item2)
                continue
            weight= similarity * my_rating
#             print('Slicnost', similarity, 'na', item,'so', item2, weight)
            similarity_per_item.setdefault(item2, [])
            similarity_per_item[item2].append(weight)
#         print(item, my_rating, list(similarity_per_item.items()))
    similarity_per_item_avg = []
    import numpy as np
    for item in similarity_per_item:

        avg_sim = np.mean(similarity_per_item[item])
        similarity_per_item_avg.append((avg_sim, item))
    similarity_per_item_avg.sort(reverse=True)
    return similarity_per_item_avg[:n]

def najgledanFIlm(oceni):

    inverse = transformoceni(oceni)

    tmpList = []
    for key, value in inverse.items():
        torka = (len(value),key)
        tmpList.append(torka)

    tmpList.sort(reverse=True)

    return tmpList

if __name__ == "__main__":

    korisnik = input()

    #print(getRecommendations(critics,korisnik,sim_pearson))

    if korisnik not in critics:
        print(najgledanFIlm(critics)[0][1])
    else:
        if len(critics[korisnik]) > 5:
            print(item_based(critics,korisnik))                 # VO ZAVISNOST OD TOA KOLKU FILMOVI SE BARAT MOZE DA SE STAVA [0][1] VAKA GI VRAKA SITE KAKO STO E VO KODOT
        else:
            print(getRecommendations(critics,korisnik,sim_pearson))


























