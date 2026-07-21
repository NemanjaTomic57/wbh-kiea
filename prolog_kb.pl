% Statisches Kartenwissen wird automatisch aus constants.MAP erzeugt und
% in generated_map.pl abgelegt.  Die Fakten agent/6 und task/6 werden von
% der Python-Simulation je Abfrage in einer temporären Datei bereitgestellt.
:- dynamic agent/6.
:- dynamic task/6.

% Eine Kante besteht nur zwischen zwei befahrbaren, orthogonal benachbarten
% Feldern. Cost ist die Kosten einer Bewegung in der Gitterkarte.
vertex((X1,Y1), (X2,Y2), 1) :-
    road(X1,Y1),
    road(X2,Y2),
    adjacent(X1,Y1,X2,Y2).

adjacent(X,Y,X2,Y) :- X2 is X + 1.
adjacent(X,Y,X2,Y) :- X2 is X - 1.
adjacent(X,Y,X,Y2) :- Y2 is Y + 1.
adjacent(X,Y,X,Y2) :- Y2 is Y - 1.

% Tiefensuche mit besuchten Knoten verhindert Zyklen.
reachable(From, To) :- reachable_(From, To, [From]).
reachable_(To, To, _).
reachable_(From, To, Visited) :-
    vertex(From, Next, _),
    \+ member(Next, Visited),
    reachable_(Next, To, [Next|Visited]).

% Breitensuche liefert die minimale Anzahl Gitterkanten.
distance(From, To, Distance) :- bfs([[From,0]], To, [From], Distance).
bfs([[To,Distance]|_], To, _, Distance).
bfs([[Current,Distance]|Queue], To, Seen, Result) :-
    findall([Next,NextDistance],
        (vertex(Current, Next, _),
         \+ member(Next, Seen),
         NextDistance is Distance + 1),
        New),
    pairs_keys(New, NewVertices),
    append(Seen, NewVertices, Seen1),
    append(Queue, New, Queue1),
    bfs(Queue1, To, Seen1, Result).

pairs_keys([], []).
pairs_keys([[Key,_]|Rest], [Key|Keys]) :- pairs_keys(Rest, Keys).

% task(Id, DepotX, DepotY, ZielX, ZielY, Paketgewicht).
% agent(Id, X, Y, Kapazitaet, Batteriestand, Status).
% Die Batterie muss beide Strecken abdecken. Unter allen zulaessigen, freien
% Agenten wird der mit der kleinsten Gesamtstrecke bestimmt.
candidate_agent(task(TaskId), AgentId) :-
    setof(Total-Agent,
        X^Y^Capacity^Battery^DepotX^DepotY^DestX^DestY^Weight^ToDepot^ToDestination^
        (task(TaskId, DepotX, DepotY, DestX, DestY, Weight),
         agent(Agent, X, Y, Capacity, Battery, idle),
         Capacity >= Weight,
         distance((X,Y), (DepotX,DepotY), ToDepot),
         distance((DepotX,DepotY), (DestX,DestY), ToDestination),
         Total is ToDepot + ToDestination,
         Battery >= Total),
        [_-AgentId|_]).
