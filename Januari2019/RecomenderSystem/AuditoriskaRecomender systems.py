from math import sqrt

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


###########################################################################################
def sim_distance(prefs, person1, person2):  # -------EVKLIDOVO RASTOJANIE--------
    si = {}
    sum_of_squares = 0

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: return 0

    # sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)    '''ovaa e resenie od courses za Soberi gi kvadratite na site razliki, mojto e dolu '''

    #            for item in prefs[person1] if item in prefs[person2]

    #           ])

    # Soberi gi kvadratite na site razliki
    for item in prefs[person1]:
        if item in prefs[person2]:
            sum_of_squares += pow(prefs[person1][item] - prefs[person2][item], 2)

    return 1 / (1 + sqrt(sum_of_squares))


############################################################################################
def sim_pearson(pref, p1, p2):  # --------PEARSONOVA KORELACIJA---------

    si = {}
    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    pSum = 0

    for item in pref[p1]:
        if item in pref[p2]:
            si[item] = 1

    n = len(si)

    if n == 0: return 0

    for it in si:
        ocena1 = pref[p1][it]  # so ovaa
        ocena2 = pref[p2][it]

        sum1 += ocena1
        sum2 += ocena2

        sum1Sq += ocena1 ** 2
        sum2Sq += ocena2 ** 2

        pSum += ocena1 * ocena2

    '''for it in si:  # soberi gi ocenite za person1               #ovaa e istoto resenie 
        sum1 += pref[p1][it]
    for it in si:  # soberi gi ocenite za person2
        sum2 += pref[p2][it]

    for it in si:  # soberi gi kvadratite na ocenite za person1
        sum1Sq += pow(pref[p1][it], 2)
    for it in si:  # soberi gi kvadratite na ocenite za person2
        sum2Sq += pow(pref[p2][it], 2)

    for it in si:  # soberi gi proizvodite od ocenite na dvete licnosti
        pSum += pref[p1][it] * pref[p2][it]'''

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0: return 0

    r = num / den
    return r


###################################################################################################
def topMatches(pref, person, n=5, similarity=sim_pearson):
    scoreList = []

    for otherPerson in pref:
        if otherPerson != person:
            tmp = similarity(pref, person, otherPerson)
            scoreList.append((tmp, otherPerson))

    scoreList.sort()
    scoreList.reverse()

    return scoreList


########################################################################################################

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


######################################################################################################
def transformoceni(oceni):
    result = {}
    for person in oceni.keys():
        for item in oceni[person]:
            result.setdefault(item, {})
            # Zameni gi mestata na licnosta i predmetot
            result[item][person] = oceni[person][item]
    return result


#####################################################################################################

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
    import numpy as np ##################################################################################### nemozam da instaliram numpy
    for item in similarity_per_item:
        print(item, similarity_per_item[item])
        avg_sim = np.mean(similarity_per_item[item])
        similarity_per_item_avg.append((avg_sim, item))
    similarity_per_item_avg.sort(reverse=True)
    return similarity_per_item_avg[:n]

'''for critic in critics.keys():                           #-------------------- MAIN -------------------------

    tmp1 = sim_distance(critics,'Lisa Rose', critic)
    tmp2 = sim_pearson(critics, 'Lisa Rose', critic)

    print("Lisa Rose and", critic, "\t\t\t Euc. dist", tmp1, "\t\t\t Pearson C.C", tmp2)




slicni = topMatches(critics, 'Michael Phillips', 100)    #---testiranje na TopMatches
for critic in slicni:
    print(critic[1], "\t", critic[0])'''



print(getRecommendations(critics, 'Toby', sim_distance))    #---testiranje na getRecommendations

















