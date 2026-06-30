# Einführung und Anwendung der Künstlichen Intelligenz

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



