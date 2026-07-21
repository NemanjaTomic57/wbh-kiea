# Einführung und Anwendung der Künstlichen Intelligenz

## Aufgabe 4: PROLOG-Wissensbasis

Die Datei [prolog_kb.pl](prolog_kb.pl) enthält die Wissensbasis. Die Python-Brücke
[prolog_bridge.py](prolog_bridge.py) schreibt für jede Abfrage die aktuelle Karte und
die aktuellen Agenten-/Auftragsfakten in eine temporäre PROLOG-Datei und ruft
SWI-Prolog auf. Damit bleiben Karte und Simulation in Python die einzige Quelle der
Wahrheit; `road/2`, `wall/2`, `depot/3` und `goal/3` werden daraus erzeugt.

`vertex/3` bildet orthogonale Nachbarn mit Kosten 1. `reachable/2` verwendet eine
Tiefensuche mit Besuchsliste. `candidate_agent/2` verwendet Breitensuche fuer die
Distanz und waehlt unter freien Agenten den Kandidaten mit minimaler Gesamtstrecke,
ausreichender Kapazitaet und Batterie fuer Anfahrt plus Lieferung.

Voraussetzung ist SWI-Prolog (Befehl `swipl`; alternativ den Pfad mit der Variablen
`SWIPL` setzen). Start der Simulation:

```bash
python main.py
```

Vor jeder A*-Planung fragt `main.py` PROLOG, ob Depot und Ziel erreichbar sind.
Danach wird `candidate_agent/2` als Vorfilter der Bieterauswahl verwendet. Nur der
von PROLOG zugelassene, beste freie Agent wird an die vorhandene Bieterauswahl
weitergegeben; erst dann berechnet A* den konkreten Weg.

### Ergebnisnachweis: konkrete verwendete Abfragen

Der Nachweis ist mit der aktuellen Karte reproduzierbar. Das Skript
[`prolog_evidence.py`](prolog_evidence.py) erzeugt normale `Task`- und
`Agent`-Objekte und ruft ausschliesslich die beiden Methoden auf, die auch
`determine_winner` in `main.py` verwendet:

```bash
python prolog_evidence.py
```

Die dabei ausgefuehrten PROLOG-Abfragen und erwarteten Antworten sind:

```prolog
?- reachable((21,3),(8,2)).
true.

?- task(7,21,3,8,2,1), agent(0,2,2,5,100,idle),
   agent(1,20,3,3,80,idle), candidate_agent(task(7), Agent).
Agent = 1.
```

Die erste Abfrage ist die Erreichbarkeitspruefung zwischen Depot und Ziel,
unmittelbar bevor A* einen Weg plant. Die zweite Abfrage waehlt Agent 1: Er
steht einen Schritt vom Depot entfernt, ist frei, besitzt Kapazitaet 3 fuer das
Paketgewicht 1 und hat mit Batterie 80 genug Energie fuer Anfahrt und Lieferung.
Damit ist der Ergebnisnachweis nicht nur ein isoliertes REPL-Beispiel, sondern
ein reproduzierbarer Ablauf der tatsächlich eingebundenen Simulation.

In dieser B-Aufgabe implementieren Sie ein kleines Logistik-Simulationsspiel mit Agenten:
Mehrere Lieferroboter (Agenten) bewegen sich auf einer diskreten Karte, verteilen Lieferaufträge
untereinander und planen ihre Wege mit A*.

Sofern nicht anders angegeben, können Sie die Programmiersprache für die Lösung frei wählen.
Achten Sie aber darauf, eine betriebssystemunabhängige Lösung zu wählen. Bei der Wahl der
Darstellung sind Sie ebenfalls frei, d. h., Sie können eine einfache Text-Ausgabe auf der Konsole
genauso wie eine grafische Oberfläche wählen.

## Karte

###############################################
#.............#######.........................#
#....#.....Z..............D.....####..........#
#....#........#######.....#........#.....Z....#
#....##########...........#........#..........#
#.........................#..Z.....#.....#....#
#.#.....#.....#######.....#######..#.....#....#
#########........#.................#######....#
#.Z.....#..#.....#..............#.............#
#................########.......##########....#
#................#.....Z#................#....#
#...#####........#......########D........#....#
#....#........####......#......#......#########
######...........#......#......#.........Z....#
#......D####.....#.............#####..........#
#................#...######...................#
###############################################

Besonderheiten der Karte:

Die Karte wurde auf 15 × 15 Felder erweitert und enthält mehrere Besonderheiten, die die Routenplanung anspruchsvoller machen. Die zahlreichen Wände bilden Engstellen, Sackgassen und voneinander getrennte Bereiche, sodass Agenten häufig Umwege fahren müssen und nicht immer den direkten Weg zum Ziel wählen können.

Insgesamt sind drei Depots (D) und fünf Lieferziele (Z) auf der Karte verteilt. Diese befinden sich in unterschiedlichen Bereichen der Karte, wodurch längere Transportwege entstehen und eine sinnvolle Auswahl des nächstgelegenen Depots sowie eine effiziente Reihenfolge der Lieferungen erforderlich wird.

Zusätzlich gibt es sowohl große freie Flächen als auch stark blockierte Bereiche. Dadurch existieren mehrere mögliche Routen zwischen Start- und Zielpunkten, deren Länge und Aufwand sich deutlich unterscheiden. Die Karte eignet sich daher gut, um Pfadfindungsalgorithmen hinsichtlich ihrer Effizienz und ihrer Fähigkeit zu testen, Hindernisse zu umgehen und geeignete Alternativrouten zu finden.
