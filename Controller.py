from Fuzzylogic import Membership_Func, Rule, defuzzify
from json import load
import time
## import Jetson.GPIO as GPIO


class Trafficlight:
    list_ = []  # Liste mit allen Ampeln
    def __init__(self, name, ids):
        self.name = name
        self.ids = ids
        self.state = False
        ## GPIO.setup(outputIDs, GPIO.OUT)
    
    @classmethod
    def get_dict(cls):
        return {tl.name: tl.ids for tl in cls.list_}
    
    @classmethod
    def get_states(cls):
        return {tl.name: tl.state for tl in cls.list_}


class Sensor:
    class Schleife:  # Induktionsschleifen
        def __init__(self, id_):
            self.id = id_
            self.state0 = False
            self.state0_time = 0
            self.state1 = False
            self.state1_time = 0
            self.log = []
            self.activation_time = None
            ##  GPIO.setup(id_, GPIO.IN)

        def __repr__(self):
            return f'Schleife({self.id})'


    list_ = []  # Liste mit allen vorhandenen Sensoren
    log_in = []
    log_out = []
    def __init__(self, name, ids, memb_func=None, trafficlight=None, maxqueue=None):
        self.name = name
        self.memb_func = Membership_Func(**memb_func) if memb_func is not None else None
        self.schleifen = tuple(self.Schleife(id_) for id_ in ids)
        self.trafficlight = trafficlight
        self.value = 0
        self.maxqueue = maxqueue
        self.queue = False

    def __repr__(self):
        return f'{self.schleifen} -- {self.memb_func}'
    
    @classmethod
    def get_states(cls):  # liste mit allen staten
        return {s.name: s.value for s in cls.list_}
    
    @classmethod
    def get_dict(cls):
        return {s.name: s for s in cls.list_}
    
    # Sensoreninput einlesen
    def get_value(self):
        self.value = int(input(f"Wert für Sensorengruppe {self.name}: "))  # -------------------------------------------------------------------------------------------
        return self.value
        if self.memb_func is None:  # bei Nebensensoren
            return any(list(map(GPIO.IN, [s.id for s in self.schleifen])))
        else:  # bei Hauptsensoren mit allen drei Schleifen durch den Schleifenlog gehen und Autos erkennen und zählen
            self.value += (str([x.values() for x in self.log_in]).count(str([
                [False, True],
                [False, False],
                [True, False]
            ])[9:-9]) + 
            str([x.values() for x in self.log_in]).count(str([
                [False, True],
                [True, True],
                [True, False]
            ])[9:-9])*2 -
            str(self.log_out).count("True, False"))
        
        # wenn alle Schleifen länger als 3 sek an, Schlange maximal setzen
        if (self.schleifen[1].activation_time is not None and 
            time.time()-self.schleifen[1].activation_time > 3):
            self.value = self.maxqueue
        elif self.value < 0:
            self.value = 0
        
        # logs zurücksetzen
        self.log_in = []
        self.log_out = [] if len(self.log_out) % 2 == 0 else self.log_out[-1:]

        return self.value  # lkws werden beim abfahren als 1 auto gezählt, dafür wird eventlog entleert ohne auf halbe events zu achten

    # Sensoren updaten
    def update(self):  # updates states
        # schleifenupdates
        for i, schleife in enumerate(self.schleifen):
            schleife.state0 = schleife.state1
            schleife.state1 = GPIO.IN(schleife.id)
            if schleife.state1 != schleife.state0:
                print(f"Sensor {schleife.id_} ist {schleife.state1}")  # ----------------------------------------------
                if i == 0:
                    self.log_out.append(schleife.state1)
                else:
                    if schleife.state1:
                        schleife.activation_time = time.time()
                    else:
                        schleife.activation_time = None

                    if i == 1:
                        self.log_in.append(dict(
                            schleife1=schleife.state1,
                            schleife2=self.schleifen[2]
                        ))
                    else:
                        self.log_in.append(dict(
                            schleife1=self.schleifen[1],
                            schleife2=schleife.state1
                        ))

    @classmethod
    def update_all(cls):
        for s in Sensor.list_:
            s.update()

            
class LastGreen:  # Grünsignal anliegender Kreuzungen
    list_ = []
    def __init__(self, name, memb_func, id_, maxtime):
        self.name = name
        self.memb_func = Membership_Func(**memb_func)
        self.id = id_
        self.last_signal = 0
        self.value = time.time()
        self.maxtime = maxtime
        # GPIO.setup(id_, GPIO.IN)

    @classmethod
    def get_states(cls):
        return {lg.name: lg.value for lg in cls.list_}

    # Grünsignal updaten
    def update(self):
        if GPIO.IN(self.id):
            self.last_signal = time.time()
        
        ctime = time.time()-self.last_signal
        if ctime > self.maxtime:
            self.value = 0
        else:
            self.value = time.time()

    def get_value(self):
        return self.value
        
    @classmethod
    def update_all(cls):
        for lg in cls.list_:
            lg.update()



class Phase:
    class Event:
        active_list = []
        def __init__(self, dict_, creation_time, trigger_time, state):
            self.dict = dict_
            self.state = state
            self.creation_time = creation_time
            self.trigger_time = trigger_time
        

    list_ = []
    # Initialisierung der Phase
    def __init__(self, events, rules, memb_func, safetysens):
        self.events = events  # [self.Event(**e) for e in events]
        self.rules = list(map(Rule, rules))
        self.memb_func = Membership_Func(
            **{
                attr: extr 
                for attr, extr in memb_func.items() 
                if attr != "scale"
            }, 
            scale=memb_func["scale"]
        )
        self.start_time = None
        self.safetysens = safetysens
    
    # Phasenplan erstellen und durch sensoren extra_zeit hinzufügen
    def setup(self, new=False):
        # eventdauern mit ext_time updaten
        if not new:
            ext_time = self.get_ext_time()
            print(f"Sensoren - a: {Sensor.get_dict()['a'].value}, b: {Sensor.get_dict()['b'].value}, c: {Sensor.get_dict()['c'].value}, d: {Sensor.get_dict()['d'].value}")
            print(f"extra_time: {ext_time}")
            for event in self.events:
                if event["type_"] == "tltoggle":
                    if event["extended"]:
                        event["duration"] += ext_time
        else:
            event_list = []
        
        # events aufrufen
        for event in self.events:
            # event_start_time herausfinden
            total_time = self.start_time+event["triggertime"]
            if event["relative"] is not None:
                stop = False
                cur_event = event
                while not stop:
                    anc = [
                        e for e in self.events 
                        if e["type_"] == "tltoggle" and 
                        e["id_"] == cur_event["relative"]
                    ][0]
                    total_time += anc["duration"]+anc["triggertime"]
                    if anc["relative"] is not None:
                        cur_event = anc
                    else:
                        stop = True
            # events in loop setzen
            if not new:
                if event["type_"] == "tltoggle":
                    self.Event.active_list.append(
                        self.Event(event, time.time(), total_time, True)
                    )
                    self.Event.active_list.append(
                        self.Event(event, time.time(), total_time+event["duration"], False)
                    )
                    
                elif event["type_"] == "exit":
                    self.Event.active_list.append(
                        self.Event(event, time.time(), total_time, True)
                    )            
            else:
                if event["type_"] == "tltoggle":
                    event_list.append(
                        self.Event(event, time.time(), total_time, True)
                    )
                    event_list.append(
                        self.Event(event, time.time(), total_time+event["duration"], False)
                    )
                elif event["type_"] == "exit":
                    event_list.append(
                        self.Event(event, time.time(), total_time, True)
                    )
            
        if new: return event_list

    # events nach abgelaufenen untersuchen und diese auslösen
    def update_events(self, emerg):
        remove_list = []
        exit_ = False
        # wenn keine einsatzwagensperre
        if not emerg:
            for event in self.Event.active_list:
                if time.time() > event.trigger_time:
                    if event.dict["type_"] == "tltoggle": 
                        # GPIO.OUT([id for name in event.dict["trafficlight"] for id in Trafficlight.get_dict()[name]], event.state)
                        for tl in Trafficlight.list_:
                            if tl.name in event.dict["trafficlights"]:
                                tl.state = event.state
                                print(f"set trafficlights {event.dict['trafficlights']} to {event.state}")
                                break
                        else:
                            raise Exception("keine Ampeln gefunden!")
                    else:
                        exit_ = True
                    remove_list.append(event)
            for e in remove_list:
                self.Event.active_list.remove(e)
        return exit_


    # Ermittlung der extra-Zeit aus Sensoreingaben
    def get_ext_time(self):
        # print(Sensor.list_[0].memb_func(2))
        fuzzy_inputs = {
            s.name: s.memb_func(s.get_value()) 
            for s in Sensor.list_ + LastGreen.list_ 
            if s.memb_func}
        fuzzy_output = {attr: 0 for attr in dict(self.memb_func)}
        for rule in self.rules:
            fuzzy_output = rule.apply(fuzzy_inputs, fuzzy_output)
        return defuzzify(fuzzy_output, self.memb_func)


    # liefert unendliche Phasenschleife
    @classmethod
    def phasecycle(cls):
        while True:
            for p in Phase.list_:
                yield p


def main():
    # laden der preferenzen
    with open("in.json") as file:
        config = load(file)

    # erstellen der Ampel-objekte
    for tl in config["Ampeln"]:
        Trafficlight.list_.append(Trafficlight(**tl))
    
    # erstellen der Sensor-objekte
    for sensor in config["Sensoren"]:
        Sensor.list_.append(Sensor(**sensor))

    # erstellen der lastgreen-objekte
    for lg in config["Grünsignal"]:
        LastGreen.list_.append(LastGreen(**lg))

    # erstellen der Phasen-objekte
    for phase in config["Phasen"]:
        if phase["rules"] is not None:
            with open(phase["rules"]) as file:
                rules = [r for r in file.read().split('\n') if r]
        else:
            rules = None
        Phase.list_.append(Phase(phase["events"], rules, phase["memb_func"], phase["safetysens"]))
    
    
    # Einsatzwagen-Signal
    emerg_id = config["Einsatzwagen"]
    emerg = False
        
    # anwendung der objekte
    phasecycle = Phase.phasecycle()
    for phase in phasecycle:
        print("--Beginning new Phase--")
        phase.start_time = time.time()

        # Phasenplan erstellen und schlusszeit speichern
        phase.setup()

        # warten bis phase vorüber ist
        sec_full = False
        while not phase.update_events(emerg):
            pass
            """alle sonderregelungen hier"""
            """# einsatzwagensperre
            if GPIO.IN(emerg_id) and not emerg:
                emerg_start_time = time.time()
                emerg = True
                # alle tl-states speichern
                tl_states = [tl.state for tl in Trafficlight.list_]

                # alle tl_states zu False setzen
                # GPIO.OUT([y for x in Trafficlight.get_dict().values() for y in x], GPIO.LOW)
                for tl in Trafficlight.list_:
                    tl.state = False
            elif emerg and not GPIO.IN(emerg_id):
                emerg = False
                # alle tl_states wieder instandsetzen
                # GPIO.OUT([y for i, x in enumerate(Trafficlight.list_) for y in x.ids if tl_states[i]], GPIO.HIGH)
                for i, tl in enumerate(Trafficlight.list_):
                    tl.state = tl_states[i]
                
                # alle triggerzeiten der events updaten
                for e in Phase.Event.active_list:
                    e.trigger_time += time.time()-emerg_start_time()"""
            
            """# eine der sec_tls voll: neuer plan ohne ext_time, alle noch vorhandenen events überschreiben
            if any(Sensor.get_dict()[s].get_value() for s in phase.safetysens) and not sec_full:
                sec_full = True # neu berechnen, alle relativen
                new_event_list = phase.setup(new=True)
                for i, event in enumerate(Phase.Event.active_list):
                    for event2 in new_event_list:
                        if event.dict == event2.dict and event.state == event2.state:
                            Phase.Event.active_list[i] = event2"""
            
            # LastGreen.update_all()
            # Sensor.update_all()

            # time.sleep(0.05)  # eventuell programmschleife hierdurch verlangsamen
        print("--End of Phase--")
        print("\n\n------------------------------------------\n\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        # GPIO.cleanup()

# Ein Teil des gerade noch kommentierten Codes funktioniert nur mit dem angeschlossenem Modell.
# Die grundlegende Phasensteuerung funktioniert jedoch auch ohne das Modell.
