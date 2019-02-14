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

def sim_distance(oceni,person1,person2):

    filmovi1 = set((oceni[person1].keys()))
    filmovi2 = set((oceni[person2].keys()))
    zaednicki = filmovi1.intersection(filmovi2)

    #print(filmovi1)
    #print(filmovi2)
    #print(zaednicki)

    if len(zaednicki) == 0: return 0

    suma = 0.0
    for item in zaednicki:
        ocena1 = oceni[person1][item]
        ocena2 = oceni[person2][item]
        suma += (ocena1 - ocena2) ** 2

    from math import sqrt

    sim = round(1 / (1 + sqrt(suma)),3)
    torka = (sim, len(zaednicki))

    return (torka)

def sim_pearson(oceni,person1,person2):

    filmovi1 = set((oceni[person1].keys()))
    filmovi2 = set((oceni[person2].keys()))
    zaednicki = filmovi1.intersection(filmovi2)

    n = len(zaednicki)
    if n == 0: return 0

    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    pSum = 0

    for item in zaednicki:
        sum1 += oceni[person1][item]
        sum2 += oceni[person2][item]

        sum1Sq += oceni[person1][item] ** 2
        sum2Sq += oceni[person2][item] ** 2

        pSum += oceni[person1][item] * oceni[person2][item]

    from math import sqrt

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2,2) / n))

    if den == 0: return 0

    r = round(num / den,3)


    return (r,n)

if __name__ == "__main__":

    korisnik1=input()
    korisnik2=input()
    # korisnik1='Mick LaSalle'
    # korisnik2='Lisa Rose'
    print (sim_pearson(oceniPoKorisnici, korisnik1, korisnik2))
    print (sim_distance(oceniPoKorisnici, korisnik1, korisnik2))