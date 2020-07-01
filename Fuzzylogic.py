from Centroid import get_centroid


"""Ermittlung der zusätlichen Zeit mithilfe 
der festgelegten Regeln für die Phase und 
der festgelegten Mitgliedsfunktionen der Sensoren und 
der zusätzlichen Zeit der Phase"""
class Membership_Func:  # Membership-Funktion Objekt bestehend aus mehreren Attribut-Funktionen
    class Attribute:  # Attribut-Funktion Objekt bestehend aus mehreren Unterfunktionen
        # Initialisierung des Attribut Objektes
        def __init__(self, *extrema, max_DOM):
            self.Inf = 9999999999
            
            # Extrema der Attribut-Funktion aufnehmen
            self.extrema = dict(
                min1=extrema[0], 
                max1=extrema[1] if extrema[1] is not None else -self.Inf, 
                max2=extrema[2] if extrema[2] is not None else self.Inf, 
                min2=extrema[3]
            )
            self.max_DOM = max_DOM

            # bestimmen des Grundrisses der gesamten Attribut-Funktion
            self.layout = list(map(
                lambda x: False if x is None or x in (self.Inf, -self.Inf) else True, 
                self.extrema.values()
            ))
            
            # lineare Funktionen für x und y
            self.linear_y = lambda x1, y1, x2, y2: lambda x: (x-x2)*(y2-y1)/(x2-x1)+y2
            self.linear_x = lambda x1, y1, x2, y2: lambda y: (y-y2)*(x2-x1)/(y2-y1)+x2

            # Unterteilung der Attribut-Funktion in mehrere einzelne Funktionen zwischen Extrema
            sections = [
                [
                    (-self.Inf, 0, self.extrema['min1'], 0), 
                    (-self.Inf, self.extrema['min1'])
                ],
                [
                    (self.extrema['min1'], 0, self.extrema['max1'], self.max_DOM), 
                    (self.extrema['min1'], self.extrema['max1'])
                ],
                [
                    (self.extrema['max1'], self.max_DOM, self.extrema['max2'], self.max_DOM), 
                    (self.extrema['max1'], self.extrema['max2'])
                ],
                [
                    (self.extrema['max2'], self.max_DOM, self.extrema['min2'], 0), 
                    (self.extrema['max2'], self.extrema['min2'])
                ],
                [
                    (self.extrema['min2'], 0, self.Inf, 0), 
                    (self.extrema['min2'], self.Inf)
                ]
            ]
            # Bestimmen der Abschnitte für Funktionslayout /¯\
            if self.layout == [True]*4:
                self.sections = sections
            # Bestimmen der Abschnitte für Funktionslayout ¯\
            elif self.layout == [False]*2 + [True]*2:
                self.sections = sections[-3:]
            # Bestimmen der Abschnitte für Funktionslayout /¯
            elif self.layout == [True]*2 + [False]*2:
                self.sections = sections[:3]
            else:
                raise AttributeError("Ungültige Extrema angegeben!")
            
        
        # Umwandeln eines klaren Inputs in Fuzzy-Werte
        def __call__(self, crisp_input):
            fuzzy_value = 0
            # Input Wert in passende Funktion der verschiedenen Abschnitte eingeben
            for section in self.sections:
                if section[1][0] <= crisp_input <= section[1][1]:
                    fuzzy_value = self.linear_y(*section[0])(crisp_input)
                    break
            else:
                raise ValueError("Input ungültig!")
            return fuzzy_value
        
        # alle entsprechenden x-Werte eines y-Wertes der Attribut-Funktion liefern
        def get_x_values_of(self, y):
            # je nach Funktionsgrundriss y-Wert in Abschnitt-Gegenfunktion eingeben
            if self.layout == [True]*4:
                return [
                    self.linear_x(*self.sections[1][0])(y), 
                    self.linear_x(*self.sections[-2][0])(y)
                ]
            elif self.layout == [False]*2 + [True]*2:
                return [None, self.linear_x(*self.sections[-2][0])(y)]
            elif self.layout == [True]*2 + [False]*2:
                return [self.linear_x(*self.sections[1][0])(y), None]
            else:
                raise AttributeError("Invalid Extrema!")


    # Initialisieren des Membership_Func Objektes bestehend aus mehreren einzelnen Attribut-Funktionen
    def __init__(self, max_DOMs=None, scale=None, **attrs):
        self.scale = scale
        self.attributes = {
            attr_name: self.Attribute(*extrema, max_DOM=1 
            if max_DOMs is None 
            else max_DOMs[attr_name]) 
            for attr_name, extrema in attrs.items()
        }

    # klarer Input zu Fuzzy-Wert durch eingeben des Inputs in die Attrubut-Funktionen 
    def __call__(self, crisp_input):
        return {
            attr_name: attr_obj(crisp_input) 
            for attr_name, attr_obj in self.attributes.items()
        }
    
    def __repr__(self):
        return f'Membership_Function({list(self.attributes.keys())})'
    
    def __iter__(self):
        return iter(self.attributes.items())


class Rule:  # Regel Objekt um Fuzzy-Output-Sets aus Fuzzy-Input-Sets zu bestimmen
    # Initialisierung des Regel Objekts
    def __init__(self, rule):
        self.string = rule

        # Nur entweder UND oder ODER Regeln zulassen
        assert not (rule.count('AND') > 0 and rule.count('OR') > 0), "UND und ODER beides in Regel vorhanden"
        rule = rule[3:]  # 'IF' entfernen

        # Regel-String zu Array formatieren
        self.op = 'AND' if 'AND' in rule else 'OR'
        self.rule = [
            y.split(' IS ') 
            for x in rule.split(f' {self.op} ') 
            for y in x.split(' THEN ')
        ]
        # print(self.rule)


    # Regel anwenden und modifiziertes Fuzzy-Output-Set zurückgeben
    def apply(self, inputsets, outputset):
        # Input-Sets für Regelanwendung filtern
        comp_list = [inputsets[name][attr] for name, attr in self.rule[:-1]]
        # nach Regel Attribut-Wert des Output-Sets updaten
        outputset[self.rule[-1][-1]] = max(
            outputset[self.rule[-1][-1]], 
            min(comp_list) if self.op == 'AND' else max(comp_list)
        )
        return outputset
    

    def __repr__(self):
        return f'Rule({self.string})'


# Ermitteln der echten Zeit aus Fuzzy-Output-Set und Membership-Funktion
def defuzzify(output_set, memb_func):
    # x-Wert an dem sich zwei lineare Funktionen kreuzen
    linear_junc = lambda x1a, y1a, x2a, y2a, x1b, y1b, x2b, y2b: (
        ((x1a-x2a)*(y1b*x2b-y2b*x1b)+(x1a*y2a-y1a*x2a)*(x1b-x2b))/
        ((y1b-y2b)*(x1a-x2a)+(x2b-x1b)*(y1a-y2a))
    )

    # Erstellen einer neuen Membership-Funktion mit duch Output-Set neu gesetzte Extrema
    newattr_list = {
        attr_name: [
            attr.extrema['min1'], 
            attr.get_x_values_of(output_set[attr_name])[0], 
            attr.get_x_values_of(output_set[attr_name])[1], 
            attr.extrema['min2']
        ] 
        for attr_name, attr in memb_func
    }
    func = Membership_Func(
        **newattr_list, 
        max_DOMs=output_set, 
        scale=memb_func.scale
    )

    # Polygon aus Graphen der neuen Membership-Funktion erstellen
    polygon = []
    # für jedes Attribut in Membership-Funktion
    for attr_name, attr in func:
        # für jedes Extrema in Attribut-Funktion
        for _, extrema in attr.extrema.items():
            if extrema is not None:
                # + höchster Punkt bei x=0 wenn Extrema niedriger als 0
                if extrema < 0:
                    polygon.append([0, max(func(0).values())])
                # + höchster Punkt bei x=Scalaende wenn Extrema höher alse Scalaende
                elif extrema > func.scale:
                    polygon.append([func.scale, max(func(func.scale).values())])
                # sonst + Extrema Punkt wenn Punkt höchster von allen Attribut-Funktionen insgesamt
                else:
                    if max(func(extrema).values()) == attr(extrema):
                        polygon.append([extrema, attr(extrema)])
        
        # für jeden Funktions-Abschnitt
        for section in attr.sections:
            # für jedes andere Attribut
            for attr2_name, attr2 in func:
                if attr2_name != attr_name:
                    # für jeden Abschnitt im anderen Attribut
                    for section2 in attr2.sections:
                        try:
                            # + schnittpunkt beider Abschnitts-Funktionen wenn Schnittpunkt in Reichweite des ersten Abschnitts und höchster von allen Attribut-Funktionen insgesamt
                            temp = linear_junc(*section[0], *section2[0])
                            if (section[1][0] <= temp <= section[1][1] and 
                                max(func(temp).values()) == attr(temp)):
                                polygon.append([temp, attr(temp)])
                        except ZeroDivisionError:
                            pass
    
    # doppelte Werte entfernen und sortieren
    polygon = [list(p2) for p2 in set([tuple(p) for p in polygon])]
    polygon.sort(key=lambda x: x[0])
    # Eckpunkte einfügen
    if float(polygon[0][1]) != 0.0:
        polygon.insert(0, [0, 0])
    if float(polygon[-1][-1]) != 0.0:
        polygon.append([func.scale, 0])


    # links und rechts nicht verbundene Koordinaten entfernen
    remove_list = []

    lstrip = []
    done = False
    i = 0
    while not done:
        if polygon[i][1] != 0:
            done = True
        else:
            lstrip.append(polygon[i])
        i += 1

    remove_list += lstrip[:-1]

    rstrip = []
    done = False
    i = len(polygon)-1
    while not done:
        if polygon[i][1] != 0:
            done = True
        else:
            rstrip.append(polygon[i])
        i -= 1
    
    remove_list += rstrip[:-1]

    for x in remove_list:
        polygon.remove(x)
    
    # Mittelpunkt des Polygons zurückgeben
    return get_centroid(polygon)[0]

