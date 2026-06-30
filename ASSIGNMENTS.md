# Assignments

## 1. Karten- und Agentenmodell

a)Implementieren Sie eine diskrete 2D-Karte (mind. 10 × 10 Zellen) mit befahrbaren Zellen,
Hindernissen (Wänden), mindestens zwei Depots und mindestens drei Lieferzielen. Imple-
mentieren Sie auf jeden Fall eine eigene Karte, selbst dann, wenn Sie die Beispiele unten
zum Testen nutzen. Argumentieren Sie: Was ist das Besondere an Ihrer Karte? (5 Punkte)

b) Implementieren Sie ein Agentenmodell mit Position (𝑥, 𝑦), Geschwindigkeit in Zellen pro
Simulationsschritt, Kapazität (in Paketeinheiten) und Batteriestand. Erzeugen Sie mindes-
tens zwei Agententypen, Standard und Express. (5 Punkte)

c) Implementieren Sie die Initialisierung und Hauptschleife der Simulation. Pro Schritt kön-
nen Agenten Nachrichten empfangen/lesen, Handlungen planen und eine Handlung aus-
führen (Bewegung, Paket aufnehmen, Paket abliefern, Nachricht senden). Für die Bewe-
gungslogik können Sie zunächst zum Testen eine zufällige Richtungswahl implementieren;
die eigentliche Wegplanung ist Gegenstand von Aufgabe 3. (10 Punkte)

Die Codierung der Karte und deren Gestalt können Sie frei wählen; hier sind zwei Beispiele,
die Sie als Grundlage für eigene Karten nutzen oder direkt übernehmen können:

[ ][ ][ ][#][#][#][ ][ ][Z][ ]
[D][ ][ ][#][Z][#][ ][#][#][ ]
[ ][#][ ][#][ ][#][ ][ ][ ][ ]
[ ][#][ ][ ][ ][ ][#][#][ ][ ]
[ ][#][#][#][#][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][#][ ][#][#][ ][ ]
[ ][#][#][ ][#][ ][ ][ ][ ][Z]
[ ][#][ ][ ][ ][#][ ][#][#][ ]
[ ][ ][ ][#][ ][#][ ][ ][ ][ ]
[ ][Z][ ][#][ ][ ][ ][#][D][ ]

Listing 1: Stadt mit Flaschenhals in der Mitte

Karte 1 hat zwei Depots an den Positionen (0, 1) und (9, 8) sowie Ziele an den Positionen
(0, 8), (1, 4), (6, 9) und (9, 1). Hindernisse sind durch das Raute-Symbol # codiert. Die Klam-
mern [ und ] dienen der besseren Darstellung der einzelnen Felder und müssen nicht Teil der
Kartencodierung sein.

Auf der Karte sind keine Agenten dargestellt. Agenten entstehen am Anfang der Simulation
an zufälligen freien Stellen.

Ein weiteres Beispiel stellt eine Stadt mit zwei Vierteln dar:

[ ][Z][ ][#][#][#][ ][ ][ ][ ]
[D][ ][ ][#][ ][#][ ][#][Z][ ]
[ ][#][ ][#][ ][#][ ][#][ ][ ]
[ ][#][ ][ ][ ][ ][ ][#][ ][ ]
[ ][#][#][#][#][#][ ][#][ ][ ]
[ ][ ][ ][ ][ ][#][ ][#][ ][ ]
[ ][#][#][#][ ][#][ ][ ][ ][ ]
[ ][#][Z][#][ ][#][#][#][ ][ ]
[ ][ ][ ][#][ ][ ][ ][ ][ ][D]
[ ][ ][ ][#][Z][ ][#][#][ ][ ]

Listing 2: Stadt mit zwei Vierteln, verbunden über eine Brücke

Diese Karte enthält zwei Depots (D) im linken Virtel bei (1, 0) und im rechten Viertel bei
(8, 9). Ziele (Z) befinden sich an den Positionen (0, 1), (1, 8), (7, 2) und (9, 4). Es existiert eine
„Brücke“ als Durchgang bei Spalte 4/5 rund um Zeilen 3 und 6, die die beiden Seiten verbindet.
Agenten können Sie zur Laufzeit mit Zahlen codieren/darstellen. Da die Agenten in dieser
Aufgabe noch keine echte Strategie besitzen, können Sie einfach zufällig in eine mögliche
Richtung laufen. Zwei Agenten können sich nicht gleichzeitig auf einem Feld befinden.
Ergebnisnachweis: Geben Sie zusammen mit dem Quelltext eine Darstellung der Karte
unmittelbar nach Erzeugung und Platzierung der Agenten sowie nach fünf Simulationsschritten
mit ab.
