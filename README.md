# Einführung und Anwendung der Künstlichen Intelligenz

In dieser B-Aufgabe implementieren Sie ein kleines Logistik-Simulationsspiel mit Agenten:
Mehrere Lieferroboter (Agenten) bewegen sich auf einer diskreten Karte, verteilen Lieferaufträge
untereinander und planen ihre Wege mit A*.

Sofern nicht anders angegeben, können Sie die Programmiersprache für die Lösung frei wählen.
Achten Sie aber darauf, eine betriebssystemunabhängige Lösung zu wählen. Bei der Wahl der
Darstellung sind Sie ebenfalls frei, d. h., Sie können eine einfache Text-Ausgabe auf der Konsole
genauso wie eine grafische Oberfläche wählen.

## Karte

Diese Karte enthält mehrere Engstellen, Sackgassen und alternative Verbindungswege zwischen den beiden Depots und den Lieferzielen. Dadurch entstehen Situationen, in denen Agenten konkurrierende Routen wählen und sich gegenseitig blockieren können. Die Karte eignet sich daher gut zur Untersuchung der Wegplanung mit A*, der späteren Kollisionsvermeidung sowie der Auftragsvergabe zwischen mehreren Agenten.

####################
#D....#.......Z....#
#.###.#.#####.###..#
#.....#.....#......#
#.#####.###.#.###..#
#.......#...#......#
#.#####.#.#####.##.#
#..Z....#.....#....#
#.###.#####.#.###..#
#....#.....#....D..#
#.##.#.###.#####...#
#......Z...........#
####################


