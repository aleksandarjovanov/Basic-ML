'''Да се промени функцијата за предвидување, така што таа ќе ја печати само класата која ја предвидува (а не речник како сега).
Притоа да се проверува дали во листот има повеќе од една класа. Ако има само една класа тогаш се предвидува истата, но ако има повеќе
од една треба да се испечати таа со најголем број на инстанци. Ако во листот има неколку класи со ист број на инстанци да се предвиде првата класа по азбучен ред.'''
trainingData=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['google','France','yes',23,'Basic'],
        ['google','France','yes',23,'Basic'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode(object):
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, l = -1):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb
        self.l = l


def sporedi_broj(value1, value2):
    return value1 >= value2


def sporedi_string(value1, value2):
    return value1 == value2


# In[43]:


def get_compare_func(value):
    if isinstance(value, int) or isinstance(value, float):
        comparer = sporedi_broj
    else:
        comparer = sporedi_string
    return comparer

def compare_values(v1, v2):
    sporedi = get_compare_func(v1)
    return sporedi(v1, v2)

def divideset(rows, column, value):
    sporedi = get_compare_func(value)
#     print(split_function)
    # Divide the rows into two sets and return them
    set_false = []
    set_true = []
    for row in rows:
        uslov=sporedi(row[column], value)
#         print(column, value, row[column], uslov, row)
        if uslov:
            set_true.append(row)
        else:
            set_false.append(row)
#     print(len(set_true), len(set_false))
#     set_true = [row for row in rows if
#             split_function(row, column, value)]  # za sekoj row od rows za koj split_function vrakja true
#     set_false = [row for row in rows if
#             not split_function(row, column, value)]  # za sekoj row od rows za koj split_function vrakja false
    return (set_true, set_false)

def uniquecounts(rows):
    d={}
    for r in rows:
#         print(r[-1])
        d.setdefault(r[-1], 0)
        d[r[-1]]+=1
    return d

from math import log
log2 = lambda x: log(x)/log(2)

def entropy(rows):
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    n = len(rows)
    for label, cnt in results.items():
#         print(r)
        p = float(cnt) / n
#         print(label, cnt, p)
        ent -= p * log2(p)
    return ent

def info_gain(current_score, sets, scoref=entropy):
    m = sum([len(s) for s in sets])
    gain = current_score
    for s in sets:
        n=len(s)
        p=1.*n/m
        gain -= p*scoref(s)
    return gain


def buildtree(rows, scoref=entropy, level = -1):
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)

    # Set up some variables to track the best criteria
    best_gain = 0.0
    best_column = -1
    best_value = None
    best_subsetf = None
    best_subsett = None

    column_count = len(rows[0]) - 1
    for col in range(column_count):
        # Generate the list of different values in
        # this column
        #         column_values = set()
        #         for row in rows:
        #             column_values.add(row[col])
        #         print(column_values)
        column_values = set([row[col] for row in rows])
        #         print('Zemame vo predvid podelba po:', col, len(column_values), column_values)
        #         continue
        # Now try dividing the rows up for each value
        # in this column
        for value in column_values:
            sets = divideset(rows, col, value)

            # Information gain
            #             p = float(len(set1)) / len(rows)
            #             gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            gain = info_gain(current_score, sets, scoref)
            if gain > best_gain and len(sets) > 0 and len(sets[0]) > 0 and len(sets[1]) > 0:
                best_gain = gain
                best_column = col
                best_value = value
                best_subsett = sets[0]
                best_subsetf = sets[1]
                # best_criteria = (col, value)
                # best_sets = (set1, set2)
    #             print('Dividing dataset', col, value, gain, sets)
    # pronajden e korenot
    #     return
    # Create the subbranches
    if best_gain > 0:
        #         print(best_subsett)
        #         print(best_subsetf)
        level +=1
        trueBranch = buildtree(best_subsett, scoref, level)
        falseBranch = buildtree(best_subsetf, scoref, level)

        return decisionnode(col=best_column, value=best_value,
                            tb=trueBranch, fb=falseBranch, l = level)

    else:
        return decisionnode(results=uniquecounts(rows), l = level)

def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results != None:
        print(str(tree.results))
    else:
        # Print the criteria
        print(str(tree.col) + ':' + str(tree.value) + '? ' + 'Level=' + str(tree.l))
        # Print the branches
        print(indent + 'T->'),
        printtree(tree.tb, indent + '  ')
        print(indent + 'F->'),
        printtree(tree.fb, indent + '  ')

'''def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results != None:
        print(str(tree.results))
    else:
        # Print the criteria
        print(str(tree.col) + ':' + str(tree.value) + '? ' + 'Level=' + str(tree.l))
        # Print the branches
        print(indent + 'T->')
        printtree(tree.tb, indent + '  ')
        print(indent + 'F->')
        printtree(tree.fb, indent + '  ')'''                        #EDNATA PRINT NE RABOTE SO ENTER TOCNO NEMAM POIMA ZASO, na code ama

def classify(observation, tree):
    if tree.results != None:
         br = len(tree.results)

         if br == 1:
            lista = list(tree.results.keys())
            return lista[0]
         else:
             maxInstanci = 0
             klasa = None

             for v in tree.results.values():
                 if v > maxInstanci:
                     maxInstanci = v

             for k, v in tree.results.items():
                 if v == maxInstanci:
                     klasa = k

             return klasa
#         return tree.results
    else:
        vrednost = observation[tree.col]
        if compare_values(vrednost, tree.value):
           branch = tree.tb
        else:
           branch = tree.fb
        return classify(observation, branch)


if __name__ == "__main__":

    referrer='google'
    location='Macedonia'
    readFAQ='yes'
    pagesVisited=23
    serviceChosen='Unknown'

    #referrer=input()
    #location=input()
    #readFAQ=input()
    #pagesVisited=input()
    #serviceChosen=input()

    testCase=[referrer, location, readFAQ, pagesVisited, serviceChosen]

    t=buildtree(trainingData)
    print(classify(testCase,t))



























'''trainingData = [['slashdot', 'USA', 'yes', 18, 'None'],
                ['google', 'France', 'yes', 23, 'Premium'],
                ['google', 'France', 'yes', 23, 'Basic'],
                ['google', 'France', 'yes', 23, 'Basic'],
                ['digg', 'USA', 'yes', 24, 'Basic'],
                ['kiwitobes', 'France', 'yes', 23, 'Basic'],
                ['google', 'UK', 'no', 21, 'Premium'],
                ['(direct)', 'New Zealand', 'no', 12, 'None'],
                ['(direct)', 'UK', 'no', 21, 'Basic'],
                ['google', 'USA', 'no', 24, 'Premium'],
                ['slashdot', 'France', 'yes', 19, 'None'],
                ['digg', 'USA', 'no', 18, 'None'],
                ['google', 'UK', 'no', 18, 'None'],
                ['kiwitobes', 'UK', 'no', 19, 'None'],
                ['digg', 'New Zealand', 'yes', 12, 'Basic'],
                ['slashdot', 'UK', 'no', 21, 'None'],
                ['google', 'UK', 'yes', 18, 'Basic'],
                ['kiwitobes', 'France', 'yes', 19, 'Basic']]


class decisionnode:
    # lel init konstruktor?
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


def sporedi_broj(row, column, value):
    return row[column] >= value


def sporedi_string(row, column, value):
    return row[column] == value


# Divides a set on a specific column. Can handle numeric
# or nominal values
def divideset(rows, column, value):
    # Make a function that tells us if a row is in
    # the first group (true) or the second group (false)
    split_function = None  # Flag za proverka
    if isinstance(value, int) or isinstance(value, float):
        # ako vrednosta so koja sporeduvame e od tip int ili float
        split_function = sporedi_broj
    else:
        # ako vrednosta so koja sporeduvame e od drug tip (string)
        split_function = sporedi_string

    # Divide the rows into two sets and return them
    set1 = [row for row in rows if
            split_function(row, column, value)]  # za sekoj row od rows za koj split_function vrakja true
    set2 = [row for row in rows if
            not split_function(row, column, value)]  # za sekoj row od rows za koj split_function vrakja false
    return (set1, set2)


# Create counts of possible results
# (the last column (vertical result) of each row is the result)

def uniquecounts(rows):
    results = {}
    for row in rows:
        # The result is the last column
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


# Entropy is the sum of p(x)log(p(x)) across all
# the different possible results
def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent


def buildtree(rows, scoref=entropy):
    if len(rows) == 0: return decisionnode()
    current_score = scoref(rows)

    # Set up some variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        # Generate the list of different values in
        # this column
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1

        # Now try dividing the rows up for each value
        # in this column
        for value in column_values.keys():
            (set1, set2) = divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the subbranches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1], tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))


def classify(observation, tree):
    if tree.results != None:
        recnik = tree.results;
        lista = []
        for k in recnik.keys():
            torka = (k, recnik[k])
            lista.append(torka)
        brKlasi = len(torka)
        if brKlasi == 1:
            return lista[0][0]
        lista.sort()
        return lista[0][0]
    else:
        vrednost = observation[tree.col]
        branch = None

        if isinstance(vrednost, int) or isinstance(vrednost, float):
            if vrednost >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if vrednost == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb

    return classify(observation, branch)


if __name__ == "__main__":
    # referrer='slashdot'
    # location='UK'
    # readFAQ='no'
    # pagesVisited=21
    # serviceChosen='Unknown'

    referrer = input()
    location = input()
    readFAQ = input()
    pagesVisited = input()
    serviceChosen = input()

    testCase = [referrer, location, readFAQ, pagesVisited, serviceChosen]
    t = buildtree(trainingData)
    print
    classify(testCase, t)'''