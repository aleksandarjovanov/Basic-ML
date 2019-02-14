'''Да испрограмира функција за косинусна сличност која е дефинирана со следнава формула, каде A е листа со
оцените на едниот корисник или филм, а B е листа со оцените на другиот корисник или филм:

http://code.finki.ukim.mk/public/uploads/1453390764510.png

Притоа треба да се избегне делење со нула и во тој случај да се смета дека сличноста е -1.
Речник со оцени на корисници по филмови треба е веќе даден. Од стандардниот влез се вчитува име на еден
филм. Да се испечати сличноста на прочитаниот филм со секој друг филм (освен самиот со себе) така што ќе
се печати:

Филм 2

Косинусна сличност, Пеарсонова сличност, Евклидова сличност

Празна линија

При печатењето филмовите треба да бидат подредени по азбучен редослед. Сите сличности треба да бидат
заокружени на 2 децимали.

Vlez:
'Catch Me If You Can'
IZlez:Just My Luck
1.0 0 0.4

Lady in the Water
0.98 0.89 0.39

Snakes on a Plane
0.99 0.96 0.54

Snitch
1.0 0.99 0.67

Superman Returns
1.0 0.96 0.45

The Night Listener
0.92 -0.73 0.26

You, Me and Dupree
0.97 0.69 0.39'''


oceniPoKorisnici={
    'Lisa Rose': {'Catch Me If You Can': 3.0 , 'Snakes on a Plane': 3.5, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0, 'Snitch': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,  'The Night Listener': 3.0,'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Catch Me If You Can': 2.5, 'Lady in the Water': 2.5,'Superman Returns': 3.5, 'The Night Listener': 4.0, 'Snitch': 2.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,'The Night Listener': 4.5, 'Superman Returns': 4.0,'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'Just My Luck': 2.0, 'Superman Returns': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Catch Me If You Can': 4.5, 'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'Snitch': 4.5},
    'Toby': {'Snakes on a Plane':4.5, 'Snitch': 5.0},
    'Michelle Nichols': {'Just My Luck' : 1.0, 'The Night Listener': 4.5, 'You, Me and Dupree': 3.5, 'Catch Me If You Can': 2.5, 'Snakes on a Plane': 3.0},
    'Gary Coleman': {'Lady in the Water': 1.0, 'Catch Me If You Can': 1.5, 'Superman Returns': 1.5, 'You, Me and Dupree': 2.0},
    'Larry': {'Lady in the Water': 3.0, 'Just My Luck': 3.5, 'Snitch': 1.5, 'The Night Listener': 3.5}
    }

def sim_distance(oceni, person1, person2):
    # Se pravi lista na zaednicki predmeti (filmovi)
    from math import sqrt

    filmovi1=set(oceni[person1].keys())
    filmovi2=set(oceni[person2].keys())
    zaednicki = filmovi1.intersection(filmovi2)
#     print(filmovi1)
#     print(filmovi2)
#     print(zaednicki)
#     for item in oceni[person1].keys():
#         if item in oceni[person2]:
#             zaednicki.add(item)
#     # ako nemaat zaednicki rejtinzi, vrati 0
    if len(zaednicki) == 0: return 0
#     # Soberi gi kvadratite na zaednickite razliki
    suma = 0.0
    for item in zaednicki:
        ocena1 = oceni[person1][item]
        ocena2 = oceni[person2][item]
        suma += (ocena1 - ocena2) ** 2
#         print(item, person1, ocena1, person2, ocena2)

    return round(1 / (1 + sqrt(suma)),2)

def sim_pearson(oceni, p1, p2):
    from math import sqrt
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
    r = round(num / den,2)
    return r

def getRecommendations(oceni, person, similarity=sim_pearson, min_zaednicki=None):
    totals = {}
    simSums = {}
    for person2 in oceni.keys():
        # Za da ne se sporeduva so samiot sebe
        if person2 == person: continue
        filmovi1=set(oceni[person].keys())
        filmovi2=set(oceni[person2].keys())
        zaednicki = filmovi1.intersection(filmovi2)
        # ova e ako se bara minimum zaednicki filmovi
        # za da se zemat vo predvid ocenite na drugiot korisnik
        if min_zaednicki and len(zaednicki)<min_zaednicki:
            print('So korisnikot', person2, 'imame samo',len(zaednicki),'filmovi, pa go preskoknuvame')
            continue
        sim = similarity(oceni, person, person2)
#         print(person,person2,sim)
        # ne se zemaat vo predvid rezultati <= 0
        if sim <= 0: continue
        print(person,person2,sim)
        for item in oceni[person2].keys():
#             print(item, oceni[person].get(item, None), oceni[person2].get(item, None))
            # za tekovniot korisnik gi zemame samo filmovite sto gi nemame veke gledano
            if item not in oceni[person]: # or oceni[person][item] == 0:
                # similarity * Score   (Slicnost * Ocena)
                print(item, sim, oceni[person2][item], sim* oceni[person2][item])
                totals.setdefault(item, 0)
                totals[item] += oceni[person2][item] * sim

                # Sumuma na slicnosti
                simSums.setdefault(item, 0)
                simSums[item] += sim
        print()
#     return
    print()
    # Kreiranje na normalizirana lista so rejtinzi
    # rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings = []
    for item, weighted_score in totals.items():
        sim_total = simSums[item]
        my_score = round(weighted_score / sim_total, 1)
        print(item, weighted_score, sim_total, my_score)
        rankings.append((my_score, item))

    # Sortiranje na listata vo rastecki redosled
    rankings.sort(reverse=True)
    # Prevrtuvanje na lista za najgolemite vrednosti da bidat napred
#     rankings.reverse()
    return rankings

def topMatches_inline(oceni, person, n=5, similarity=sim_pearson):
    scores = [(similarity(oceni, person, other), other)
              for other in oceni if other != person]
    # Se sortira listata vo rastecki redosled
    scores.sort()
    # Se prevrtuva za najslicnite (so najgolema vrednost) da bidat prvi
    scores.reverse()
    return scores[0:n]

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
        similar_items = topMatches_inline(oceni_po_film, item, n=None)
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

def sim_kosinus(oceni,f1,f2):

    korisnici1 = set((oceni[f1].keys()))
    korisnici2 = set((oceni[f2].keys()))
    zaednicki = korisnici1.intersection(korisnici2)

    if len(zaednicki) == 0: return 0

    sumaAB = 0
    sumaSqa = 0
    sumaSqb = 0

    for item in zaednicki:
        ocenka1 = oceni[f1][item]
        ocenka2 = oceni[f2][item]

        sumaAB += ocenka1 * ocenka2
        sumaSqa += ocenka1 ** 2
        sumaSqb += ocenka2 ** 2

    from math import sqrt
    delitel = sqrt(sumaSqa) * sqrt(sumaSqb)

    if delitel == 0: return -1

    rez = round(sumaAB / delitel,2)

    return rez

if __name__ == '__main__':

    film = 'Catch Me If You Can'

    oceniPoFilm = transformoceni(oceniPoKorisnici)

    for item in oceniPoFilm:

        if item != film:
            print(item)
            print(sim_kosinus(oceniPoFilm,film,item),
                  sim_pearson(oceniPoFilm,film,item),
                  sim_distance(oceniPoFilm,film,item))
            print()



