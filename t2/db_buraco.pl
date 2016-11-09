:- dynamic brisa/2.
:- dynamic nbrisa/2.
:- dynamic livre/2.

/* p(X, Y) = point(X,Y) */

norte(p(X, Y), C) :-
  Y2 is Y + 1,
  C = p(X, Y2).

sul(p(X, Y), C) :-
  Y2 is Y - 1,
  C = p(X, Y2).

leste(p(X, Y), C) :-
  X2 is X + 1,
  C = p(X2, Y).

oeste(p(X, Y), C) :-
  X2 is X - 1,
  C = p(X2, Y).

nordeste(p(X,Y), C) :-
  norte(p(X,Y), C2),
  leste(C2, C).

noroeste(p(X,Y), C) :-
  norte(p(X,Y), C2),
  oeste(C2, C).

sudeste(p(X,Y), C) :-
  sul(p(X,Y), C2),
  leste(C2, C).

sudoeste(p(X,Y), C) :-
  sul(p(X,Y), C2),
  oeste(C2, C).


fora_do_mapa(p(X,Y)) :-
  (X > 13) ; ( X < 0 ) ;
  (Y > 13) ; ( Y < 0 ).

parede(p(X,Y)) :- parede(X,Y).
parede(0,_).
parede(_,0).
parede(13,_).
parede(_,13).

livre(p(X,Y)) :- livre(X,Y).
livre(1,1).
livre(2,1).
livre(1,2).

nbrisa(p(X,Y)) :- nbrisa(X,Y).
nbrisa(1,1).

brisa(p(X,Y)) :- brisa(X,Y).
brisa(1,2).
brisa(2,1).
brisa(3,2).
brisa(2,3).

/* buraco(p(X,Y)) :- buraco(X,Y). */
buraco(P) :-
  \+ fora_do_mapa(P),
  \+ livre(P),       /* Se ta livre nao tem buraco */
  \+ parede(P),      /* Parede nao eh buraco */
  norte(P, N),
  sul(P, S),
  leste(P, L),
  oeste(P, O),
  \+ nbrisa(N),      /* Se sabemos que um dos lados nao tem brisa, */
  \+ nbrisa(S),      /* nao eh buraco                              */
  \+ nbrisa(L),
  \+ nbrisa(O),
  nordeste(P, NE),
  noroeste(P, NO),
  sudeste(P, SE),
  sudoeste(P, SO),
  /* (brisa(N); brisa(S); brisa(L); brisa(O)), */
  ((brisa(N), norte(N, N2), \+ buraco(N2), \+ buraco(NE), \+ buraco(NO));
  ( brisa(S), sul(S, S2),   \+ buraco(S2), \+ buraco(SE), \+ buraco(SO));
  ( brisa(L), leste(L, L2), \+ buraco(L2), \+ buraco(NE), \+ buraco(SE));
  ( brisa(O), oeste(O, O2), \+ buraco(O2), \+ buraco(NO), \+ buraco(SO))).
