oceniPoKorisnici = {
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


# Vrakja merka za slicnost bazirana na rastojanieto za person1 i person2
def sim_distance(oceni, person1, person2):
    # Se pravi lista na zaednicki predmeti (filmovi)

    filmovi1 = set(oceni[person1].keys())
    filmovi2 = set(oceni[person2].keys())
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

    from math import  sqrt
    return round(1 / (1 + sqrt(suma)),3)


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

    from math import sqrt
    # Presmetaj go koeficientot na korelacija
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = round(num / den,3)

    return r


def TabelaNaSlicniKorisnici(oceni):
    slicnosti = {}

    for item1 in oceni:
        slicnosti.setdefault(item1, {})
        for item2 in oceni:

            if item1 != item2:
                torka = tuple((sim_distance(oceni,item1,item2), sim_pearson(oceni,item1,item2), zaednicki(oceni,item1,item2)))
                slicnosti[item1][item2] = torka


    return slicnosti

def zaednicki(oceni,p1,p2):

    filmovi1 = set((oceni[p1].keys()))
    filmovi2 = set((oceni[p2].keys()))
    mvo = filmovi1.intersection(filmovi2)

    return len(mvo)

if __name__ == "__main__":
    korisnik1 = input()
    korisnik2 = input()
    # korisnik1='Mick LaSalle'
    # korisnik2='Lisa Rose'
    # print oceniPoKorisnici
    tabela = TabelaNaSlicniKorisnici(oceniPoKorisnici)
    print(tabela)
    #print(tabela[korisnik1][korisnik2])
















