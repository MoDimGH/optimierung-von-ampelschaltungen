  ____       __  _       _                         
 / __ \___  / /_(_)_ _  (_)__ ______ _____  ___ _ 
/ /_/ / _ \/ __/ /  ' \/ / -_) __/ // / _ \/ _ `/ 
\____/ .__/\__/_/_/_/_/_/\__/_/  \_,_/_//_/\_, /  
    /_/                                   /___/                 
 _  _____  ___  
| |/ / _ \/ _ \ 
|___/\___/_//_/ 
   ___                  __        __        ____                        
  / _ | __ _  ___  ___ / /__ ____/ /  ___ _/ / /___ _____  ___ ____ ___ 
 / __ |/  ' \/ _ \/ -_) (_-</ __/ _ \/ _ `/ / __/ // / _ \/ _ `/ -_) _ \
/_/ |_/_/_/_/ .__/\__/_/___/\__/_//_/\_,_/_/\__/\_,_/_//_/\_, /\__/_//_/
           /_/                                           /___/          

Dieses Programm ist mit eventuell leichten Modifikationen an die meisten konventionellen Kreuzungssysteme anpassbar.
Alle Benutzerdefinierten Einstellungen sind in "in.json" einzutragen. Die Ids der jeweiligen JSON Elemente sind dessen GPIO-Eingänge.
Die Sensoren-Elemente bestehen unter anderem aus Angaben der anliegenden Lichtzeichenanlage und ihrer Mitgliedsfunktion. Diese wird später
das Umwandeln der Sensordaten in eine verrechenbare Zeit erleichtern. Die Mitgliedsfunktionen sind durch die Kenntnis der 
durchschnittlichen Schlange/besten zu addierenden Zeit zu erstellen. Sie bestehen jeweils aus weiteren Trapezförmigen oder 
am Rande vertikal abgehackten Trapezförmigen Attributen, wie "viel", "mittel", "wenig", nach dessen Extrema die Mitgliedsfunktionen aufgebaut werden.
Die Phasenevents können relativ zu anderen Events sein, d. h. wenn ein Event endet, wessen Zeit noch nicht bekannt ist, schliesst sich ein anderes Event an 
dieses an. "Triggertime" beschreibt die Zeit, nach der bei Beendigung des relativen Events das jetzige gestartet wird, wobei es so lange andauert und
die Ampel auf 'Grün' geschaltet ist, bis die Zeit "duration" vorbei ist. 'extended' gibt an, ob das event durch die 
mithilfe der Sensorik ermittelten zusätzlichen Zeit verlängert werden soll. Die Regeln zur Ermittlung der zusatzlichen Zeit sind in seperaten
dateien zu speichern, die Mitgliedsfunktion hier beschreibt die Dauer der zusätzlichen Zeit und die 'safetysens' sind die sensoren and den
Sicherheitsampeln, bei deren Aktivierung die Verlängerung der Events abgebrochen wird. 
Zusätzliche Kreuzungsbedingte Maßnahmen sind in der Phasenschleife sowie der 'update_events'-Funktion etc. zu verbauen.

Zum Ausführen 'Controller.py' starten.
