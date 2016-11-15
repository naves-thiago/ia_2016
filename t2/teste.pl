:- dynamic m_buraco/1.
:- dynamic m_teleport/1.
:- dynamic m_inimigoD/2.
:- dynamic m_inimigod/2.
:- dynamic m_powerup/1.
:- dynamic m_ouro/1.
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

m_buraco(p(10, 11)).
m_teleport(p(3, 3)).
m_inimigoD(p(4, 4), 50).
m_inimigod(p(5, 5), 100).
m_powerup(p(3, 1)).
m_ouro(p(4, 1)).

posicao(p(1, 1)).
pontos(50).
vida(70).
direcao('R').
