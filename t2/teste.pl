:- dynamic buraco/1.
:- dynamic teleport/1.
:- dynamic inimigoD/2.
:- dynamic inimigod/2.
:- dynamic powerup/1.
:- dynamic ouro/1.
:- dynamic livre/2.
:- dynamic posicao/1.
:- dynamic pontos/1.
:- dynamic vida/1.
:- dynamic direcao/1.

livre(1, 1).
livre(2, 1).
livre(1, 2).

livre(12, 12).
livre(1, 12).
livre(12, 1).

buraco(p(10, 11)).
teleport(p(3, 3)).
inimigoD(p(4, 4), 50).
inimigod(p(5, 5), 100).
powerup(p(3, 1)).
ouro(p(4, 1)).

posicao(p(1, 1)).
pontos(50).
vida(70).
direcao('R').
