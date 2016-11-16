:- dynamic buraco/1.
:- dynamic teleport/1.
:- dynamic inimigoD/2.
:- dynamic inimigod/2.
:- dynamic powerup/1.
:- dynamic ouro/1.
:- dynamic o_coletados/1.
:- dynamic livre/2.
:- dynamic posicao/1.
:- dynamic pontos/1.
:- dynamic vida/1.
:- dynamic direcao/1.

o_coletados(3).
balas(4).

livre(1, 1).
livre(2, 1).
livre(1, 2).

pinimigo(X) :- inimigoD(X, _); inimigod(X, _).
pburaco(X) :- buraco(X).
pteleport(X) :- teleport(X).

/*
livre(1, 3).
livre(1, 4).
livre(2, 4).
livre(3, 4).
livre(4, 4).
livre(5, 4).
livre(6, 4).
livre(7, 4).
livre(7, 5).
livre(7, 6).
livre(7, 7).
*/


livre(1, 3).
livre(1, 4).
livre(1, 5).
livre(1, 6).
livre(1, 7).
livre(2, 7).
livre(3, 7).
livre(4, 7).
livre(5, 7).
livre(6, 7).

livre(12, 12).
livre(1, 12).
livre(12, 1).

buraco(p(10, 11)).
teleport(p(3, 3)).
inimigoD(p(4, 4), 50).
inimigod(p(5, 5), 100).
powerup(p(3, 1)).
ouro(p(4, 1)).

posicao(p(2, 1)).
pontos(50).
vida(70).
direcao('U').
