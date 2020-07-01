# 1.
rule1 = [
    [['a', 'b'], "sk", "k", "m", "g"],
    ['sk',       'z',  'z', 'z', 'z'],
    ['k',        'z',  'z', 'z', 'z'],
    ['m',        'k',  'k', 'z', 'z'],
    ['g',        'm',  'm', 'k', 'k']
]

rule2 = [
    [['a', 'd'], "sk", "k", "m", "g"],
    ['sk',       'z',  'z', 'z', 'z'],
    ['k',        'z',  'z', 'z', 'z'],
    ['m',        'k',  'k', 'z', 'z'],
    ['g',        'm',  'm', 'k', 'k']
]

rule3 = [
    [['c', 'b', 'i'],   "sk", "k", "m", "g"],
    [['sw', 'sk'], 'z',  'z', 'z', 'z'],
    [['sw', 'k'],  'z',  'z', 'z', 'z'],
    [['sw', 'm'],  'k',  'k', 'z', 'z'],
    [['sw', 'g'],  'm',  'm', 'k', 'k'],
    [['w',  'sk'], 'z',  'z', 'z', 'z'],
    [['w',  'k'],  'z',  'z', 'z', 'z'],
    [['w',  'm'],  'k',  'k', 'z', 'z'],
    [['w',  'g'],  'm',  'm', 'k', 'k'],
    [['m',  'sk'], 'z',  'z', 'z', 'z'],
    [['m',  'k'],  'z',  'z', 'z', 'z'],
    [['m',  'm'],  'm',  'm', 'z', 'z'],
    [['m',  'g'],  'g',  'g', 'm', 'z'],
    [['n',  'sk'], 'z',  'z', 'z', 'z'],
    [['n',  'k'],  'k',  'k', 'z', 'z'],
    [['n',  'm'],  'm',  'm', 'k', 'z'],
    [['n',  'g'],  'g',  'g', 'm', 'k']
]

rule4 = [
    [['c', 'd', 'i'],   "sk", "k", "m", "g"],
    [['sw', 'sk'], 'z',  'z', 'z', 'z'],
    [['sw', 'k'],  'z',  'z', 'z', 'z'],
    [['sw', 'm'],  'k',  'k', 'z', 'z'],
    [['sw', 'g'],  'm',  'm', 'k', 'k'],
    [['w',  'sk'], 'z',  'z', 'z', 'z'],
    [['w',  'k'],  'z',  'z', 'z', 'z'],
    [['w',  'm'],  'k',  'k', 'z', 'z'],
    [['w',  'g'],  'm',  'm', 'k', 'k'],
    [['m',  'sk'], 'z',  'z', 'z', 'z'],
    [['m',  'k'],  'z',  'z', 'z', 'z'],
    [['m',  'm'],  'm',  'm', 'z', 'z'],
    [['m',  'g'],  'g',  'g', 'm', 'z'],
    [['n',  'sk'], 'z',  'z', 'z', 'z'],
    [['n',  'k'],  'k',  'k', 'z', 'z'],
    [['n',  'm'],  'm',  'm', 'k', 'z'],
    [['n',  'g'],  'g',  'g', 'm', 'k']
]

rule5 = [
    [['b', 'a'], "sk", "k", "m", "g"],
    ['sk',       'z',  'z', 'z', 'z'],
    ['k',        'z',  'z', 'z', 'z'],
    ['m',        'k',  'z', 'z', 'z'],
    ['g',        'm',  'm', 'k', 'z']
]

rule6 = [
    [['d', 'a'], "sk", "k", "m", "g"],
    ['sk',       'z',  'z', 'z', 'z'],
    ['k',        'z',  'z', 'z', 'z'],
    ['m',        'k',  'z', 'z', 'z'],
    ['g',        'm',  'm', 'k', 'z']
]

rule7 = [
    [['b', 'c', 'i'], ['sw', 'sk'], ['sw', 'k'], ['sw', 'm'], ['sw', 'g'], ['w', 'sk'], ['w', 'k'], ['w', 'm'], ['w', 'g'], ['m', 'sk'], ['m', 'k'], ['m', 'm'], ['m', 'g'], ['n', 'sk'], ['n', 'k'], ['n', 'm'], ['n', 'g']],
    ['sk',       'z',          'z',         'z',         'z',         'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['k',        'z',          'z',         'z',         'z',         'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['m',        'k',          'z',         'z',         'z',         'k',         'z',        'z',        'z',        'k',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['g',        'm',          'm',         'k',         'z',         'm',         'm',        'k',        'z',        'm',         'k',        'k',        'z',        'm',         'k',        'z',        'z',      ]

]

rule8 = [
    [['d', 'c', 'i'], ['sw', 'sk'], ['sw', 'k'], ['sw', 'm'], ['sw', 'g'], ['w', 'sk'], ['w', 'k'], ['w', 'm'], ['w', 'g'], ['m', 'sk'], ['m', 'k'], ['m', 'm'], ['m', 'g'], ['n', 'sk'], ['n', 'k'], ['n', 'm'], ['n', 'g']],
    ['sk',       'z',          'z',         'z',         'z',         'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['k',        'z',          'z',         'z',         'z',         'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['m',        'k',          'z',         'z',         'z',         'k',         'z',        'z',        'z',        'k',         'z',        'z',        'z',        'z',         'z',        'z',        'z',      ],
    ['g',        'm',          'm',         'k',         'z',         'm',         'm',        'k',        'z',        'm',         'k',        'k',        'z',        'm',         'k',        'z',        'z',      ]

]

# regeln in strings umwandeln
rule1_list = []

for row in rule1[1:]:
    for ic, column in enumerate(rule1[0][1:]):
        rule1_list.append(f"IF {rule1[0][0][0]} IS {row[0]} AND {rule1[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

for row in rule2[1:]:
    for ic, column in enumerate(rule2[0][1:]):
        rule1_list.append(f"IF {rule2[0][0][0]} IS {row[0]} AND {rule2[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

for row in rule3[1:]:
    for ic, column in enumerate(rule3[0][1:]):
        rule1_list.append(f"IF {rule3[0][0][2]} IS {row[0][0]} AND {rule3[0][0][0]} IS {row[0][1]} AND {rule3[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

for row in rule4[1:]:
    for ic, column in enumerate(rule4[0][1:]):
        rule1_list.append(f"IF {rule4[0][0][2]} IS {row[0][0]} AND {rule3[0][0][0]} IS {row[0][1]} AND {rule4[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

print(*rule1_list, sep='\n')

print("\n_------------_\n")

rule2_list = []

for row in rule5[1:]:
    for ic, column in enumerate(rule5[0][1:]):
        rule2_list.append(f"IF {rule5[0][0][0]} IS {row[0]} AND {rule5[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

for row in rule6[1:]:
    for ic, column in enumerate(rule6[0][1:]):
        rule2_list.append(f"IF {rule6[0][0][0]} IS {row[0]} AND {rule6[0][0][1]} IS {column} THEN xt IS {row[ic+1]}")

for row in rule7[1:]:
    for ic, column in enumerate(rule7[0][1:]):
        rule2_list.append(f"IF {rule7[0][0][0]} IS {row[0]} AND {rule7[0][0][1]} IS {column[1]} AND {rule7[0][0][2]} IS {column[0]} THEN xt IS {row[ic+1]}")

for row in rule8[1:]:
    for ic, column in enumerate(rule8[0][1:]):
        rule2_list.append(f"IF {rule8[0][0][0]} IS {row[0]} AND {rule8[0][0][1]} IS {column[1]} AND {rule8[0][0][2]} IS {column[0]} THEN xt IS {row[ic+1]}")

print(*rule2_list, sep='\n')

# regeln in dateien speicher
with open("phase1rules.csv", 'w') as file:
    file.write("\n".join(rule1_list))

with open("phase2rules.csv", 'w') as file:
    file.write("\n".join(rule2_list))
