:- include(mapa).

:- dynamic([
	visitado/1,
	livre/1,
	
	brisa/1,
	pburaco/1,
	nburaco/1,
	buraco/1,
	
	passos/1,
	pinimigo/1,
	ninimigo/1,
	inimigo/1,
	tiro/1,
	
	flash/1,
	pteleport/1,
	nteleport/1,
	teleport/1,
	
	ouro/1,
	o_coletados/1,
	powerup/1,
	p_coletados/1,
	
	posicao/1,
	vida/1,
	pontos/1,
	balas/1,
	direcao/1
]).

/*posicoes, direcoes, etc*/
/* p(X, Y) = point(X,Y) */
norte(p(X, Y), C) :-
  Y2 is Y + 1, C = p(X, Y2), not(parede(C)).

sul(p(X, Y), C) :-
  Y2 is Y - 1, C = p(X, Y2), not(parede(C)).

leste(p(X, Y), C) :-
  X2 is X + 1, C = p(X2, Y), not(parede(C)).

oeste(p(X, Y), C) :-
  X2 is X - 1, C = p(X2, Y), not(parede(C)).

nordeste(p(X,Y), C) :-
  norte(p(X,Y), C2), leste(C2, C).

noroeste(p(X,Y), C) :-
  norte(p(X,Y), C2), oeste(C2, C).

sudeste(p(X,Y), C) :-
  sul(p(X,Y), C2), leste(C2, C).

sudoeste(p(X,Y), C) :-
  sul(p(X,Y), C2), oeste(C2, C).

adjacente(p(X,Y), C) :-
	norte(p(X,Y), C);
	sul(p(X,Y), C);
	leste(p(X,Y), C);
	oeste(p(X,Y), C).

diagonal(p(X,Y), C) :-
	noroeste(p(X,Y), C);
	nordeste(p(X,Y), C);
	sudoeste(p(X,Y), C);
	sudeste(p(X,Y), C).

/*parede*/
parede(p(X,Y)) :- X < 1; Y < 1; X > 12; Y > 12.

/*estado*/
reset :- 
	retractall(visitado(_)),
	retractall(livre(_)),
	retractall(brisa(_)),
	retractall(pburaco(_)),
	retractall(nburaco(_)),
	retractall(buraco(_)),
	retractall(passos(_)),
	retractall(pinimigo(_)),
	retractall(ninimigo(_)),
	retractall(inimigo(_)),
	retractall(tiro(_)),
	retractall(flash(_)),
	retractall(pteleport(_)),
	retractall(nteleport(_)),
	retractall(teleport(_)),
	retractall(ouro(_)),
	retractall(o_coletados(_)),
	retractall(powerup(_)),
	retractall(p_coletados(_)),
	retractall(posicao(_)),
	retractall(vida(_)),
	retractall(pontos(_)),
	retractall(balas(_)),
	retractall(direcao(_)),
	assert(o_coletados(0)),
	assert(p_coletados(0)),
	assert(posicao(p(1,1))),
	assert(vida(100)),
	assert(pontos(0)),
	assert(balas(5)),
	assert(direcao('U')),
	observar.

assertThis(Fact):-
    \+( Fact ),!,         % \+ is a NOT operator.
    assert(Fact).
	assertThis(_).

retractThis(Fact):-
    ( Fact ),!,
    retract(Fact).
	retractThis(_).
	
/*implicacoes do mapa*/
m_brisa(p(X,Y)) :- m_buraco(p(W,Z)), adjacente(p(X,Y),p(W,Z)).

m_flash(p(X,Y)) :- m_teleport(p(W,Z)), adjacente(p(X,Y),p(W,Z)).

m_passos(p(X,Y)) :- m_inimigoD(p(W,Z),_), adjacente(p(X,Y),p(W,Z)); m_inimigod(p(W,Z),_), adjacente(p(X,Y),p(W,Z)).

infere_buraco_adjacente(P,D) :-
	sudeste(P, D), sul(P,S), livre(S), leste(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	sudeste(P, D), leste(P,L), livre(L), sul(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	sudoeste(P, D), sul(P,S), livre(S), oeste(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	sudoeste(P, D), oeste(P,O), livre(O), sul(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	nordeste(P, D), norte(P,N), livre(N), leste(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	nordeste(P, D), leste(P,L), livre(L), norte(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	noroeste(P, D), norte(P,N), livre(N), oeste(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B);
	noroeste(P, D), oeste(P,O), livre(O), norte(P, B), assertThis(buraco(B)), limpa_regiao_buraco(B).

limpa_regiao_buraco(B) :-
	(
		(adjacente(B, A), retractThis(pburaco(A)), assertThis(nburaco(A)), (ninimigo(A)), (nteleport(A)), assertThis(livre(A)), false);
		(diagonal(B, D), retractThis(pburaco(D)), assertThis(nburaco(D)), (ninimigo(D)), (nteleport(D)), assertThis(livre(D)), false);
		(norte(B,N), norte(N,N_N), not(parede(N_N)), retractThis(pburaco(N_N)), assertThis(nburaco(N_N)), (ninimigo(N_N)), (nteleport(N_N)), assertThis(livre(N_N)), false);
		(sul(B,S), sul(S,S_S), not(parede(S_S)), retractThis(pburaco(S_S)), assertThis(nburaco(S_S)), (ninimigo(S_S)), (nteleport(S_S)), assertThis(livre(S_S)), false);
		(leste(B,L), leste(L,L_L), not(parede(L_L)), retractThis(pburaco(L_L)), assertThis(nburaco(L_L)), (ninimigo(L_L)), (nteleport(L_L)), assertThis(livre(L_L)), false);
		(oeste(B,O), oeste(O,O_O), not(parede(O_O)), retractThis(pburaco(O_O)), assertThis(nburaco(O_O)), (ninimigo(O_O)), (nteleport(O_O)), assertThis(livre(O_O)), false);
		true
	).
	
infere_teleport_adjacente(P,D) :-
	sudeste(P, D),  sul(P,S),   livre(S), leste(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T);
	sudeste(P, D),  leste(P,L), livre(L), sul(P, T),   assertThis(teleport(T)), limpa_regiao_teleport(T);
	sudoeste(P, D), sul(P,S),   livre(S), oeste(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T);
	sudoeste(P, D), oeste(P,O), livre(O), sul(P, T),   assertThis(teleport(T)), limpa_regiao_teleport(T);
	nordeste(P, D), norte(P,N), livre(N), leste(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T);
	nordeste(P, D), leste(P,L), livre(L), norte(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T);
	noroeste(P, D), norte(P,N), livre(N), oeste(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T);
	noroeste(P, D), oeste(P,O), livre(O), norte(P, T), assertThis(teleport(T)), limpa_regiao_teleport(T).

limpa_regiao_teleport(T) :-
	(
		(adjacente(T, A), retractThis(pteleport(A)), assertThis(nteleport(A)), (ninimigo(A)), (nburaco(A)), assertThis(livre(A)), false);
		(diagonal(T, D), retractThis(pteleport(D)), assertThis(nteleport(D)), (ninimigo(D)), (nburaco(D)), assertThis(livre(D)), false);
		(norte(T,N), norte(N,N_N), not(parede(N_N)), retractThis(pteleport(N_N)), assertThis(nteleport(N_N)), (ninimigo(N_N)), (nburaco(N_N)), assertThis(livre(N_N)), false);
		(sul(T,S), sul(S,S_S), not(parede(S_S)), retractThis(pteleport(S_S)), assertThis(nteleport(S_S)), (ninimigo(S_S)), (nburaco(S_S)), assertThis(livre(S_S)), false);
		(leste(T,L), leste(L,L_L), not(parede(L_L)), retractThis(pteleport(L_L)), assertThis(nteleport(L_L)), (ninimigo(L_L)), (nburaco(L_L)), assertThis(livre(L_L)), false);
		(oeste(T,O), oeste(O,O_O), not(parede(O_O)), retractThis(pteleport(O_O)), assertThis(nteleport(O_O)), (ninimigo(O_O)), (nburaco(O_O)), assertThis(livre(O_O)), false);
		true
	).
	
infere_inimigo_adjacente(P,D) :-
	sudeste(P, D),  sul(P,S),   livre(S), leste(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	sudeste(P, D),  leste(P,L), livre(L), sul(P, I),   assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	sudoeste(P, D), sul(P,S),   livre(S), oeste(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	sudoeste(P, D), oeste(P,O), livre(O), sul(P, I),   assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	nordeste(P, D), norte(P,N), livre(N), leste(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	nordeste(P, D), leste(P,L), livre(L), norte(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	noroeste(P, D), norte(P,N), livre(N), oeste(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I);
	noroeste(P, D), oeste(P,O), livre(O), norte(P, I), assertThis(inimigo(I)), limpa_regiao_inimigo(I).

limpa_regiao_inimigo(I) :-
	(
		(adjacente(I, A), retractThis(pinimigo(A)), assertThis(ninimigo(A)), (nteleport(A)), (nburaco(A)), assertThis(livre(A)), false);
		(diagonal(I, D), retractThis(pinimigo(D)), assertThis(ninimigo(D)), (nteleport(D)), (nburaco(D)), assertThis(livre(D)), false);
		(norte(I,N), norte(N,N_N), not(parede(N_N)), retractThis(pinimigo(N_N)), assertThis(ninimigo(N_N)), (nteleport(N_N)), (nburaco(N_N)), assertThis(livre(N_N)), false);
		(sul(I,S), sul(S,S_S), not(parede(S_S)), retractThis(pinimigo(S_S)), assertThis(ninimigo(S_S)), (nteleport(S_S)), (nburaco(S_S)), assertThis(livre(S_S)), false);
		(leste(I,L), leste(L,L_L), not(parede(L_L)), retractThis(pinimigo(L_L)), assertThis(ninimigo(L_L)), (nteleport(L_L)), (nburaco(L_L)), assertThis(livre(L_L)), false);
		(oeste(I,O), oeste(O,O_O), not(parede(O_O)), retractThis(pinimigo(O_O)), assertThis(ninimigo(O_O)), (nteleport(O_O)), (nburaco(O_O)), assertThis(livre(O_O)), false);
		true
	).

/*observar*/
observar :- posicao(P), assertThis(visitado(P)),
	(
		/*se nao ha perigo, a posicao eh livre e nao tem perigos*/
		(not(m_inimigoD(P,_)), not(m_inimigod(P,_)), not(m_teleport(P)), not(m_buraco(P)), assertThis(livre(P)), retractThis(pinimigo(P)), retractThis(pteleport(P)), retractThis(pburaco(P)), false);
		
		/*se tem brisa, infere possiveis buracos*/
		(m_brisa(P), adjacente(P, Q), not(livre(Q)), assertThis(pburaco(Q)), assertThis(brisa(P)), false);
		
		/*se tem passos, infere possiveis inimigos*/
		(m_passos(P), adjacente(P, Q), not(livre(Q)), assertThis(pinimigo(Q)), assertThis(passos(P)), false);
		
		/*se tem flash, infere possiveis teleports*/
		(m_flash(P), adjacente(P, Q), not(livre(Q)), assertThis(pteleport(Q)), assertThis(flash(P)), false);
		
		/*se nao tem nenhum, infere que a posicao e os adjacentes estao livres*/
		(not(m_flash(P)), not(m_passos(P)), not(m_brisa(P)), adjacente(P, Q), assertThis(livre(P)), retractThis(pburaco(Q)), retractThis(pinimigo(Q)), retractThis(pteleport(Q)), assertThis(livre(Q)), false);
		
		/*se tem brisa e em alguma diagonal tambem, infere buraco na adjacencia correspondente e tira pburaco e poe nburaco em volta*/
		(brisa(P), diagonal(P, D), brisa(D), infere_buraco_adjacente(P, D), false);
		
		/*se tem brisa e no lado oposto tb, infere buraco no meio*/
		(brisa(P), norte(P,N), norte(N, N_N), brisa(N_N), assertThis(buraco(N)), limpa_regiao_buraco(N), false);
		(brisa(P), leste(P,L), leste(L, L_L), brisa(L_L), assertThis(buraco(L)), limpa_regiao_buraco(L), false);
		(brisa(P), oeste(P,O), oeste(O, O_O), brisa(O_O), assertThis(buraco(O)), limpa_regiao_buraco(O), false);
		(brisa(P), sul(P,S), sul(S, S_S), brisa(S_S), assertThis(buraco(S)), limpa_regiao_buraco(S), false);
		
		/*se dois adjacentes tem passos, infere inimigo na diagonal correspondente e tira pinimigo e poe ninimigo em volta*/
		(passos(P), diagonal(P, D), passos(D), infere_inimigo_adjacente(P, D), false);
		
		/*se tem passos e no lado oposto tb, infere inimigo no meio*/
		(passos(P), norte(P,N), norte(N, N_N), passos(N_N), assertThis(inimigo(N)), limpa_regiao_inimigo(N), false);
		(passos(P), leste(P,L), leste(L, L_L), passos(L_L), assertThis(inimigo(L)), limpa_regiao_inimigo(L), false);
		(passos(P), oeste(P,O), oeste(O, O_O), passos(O_O), assertThis(inimigo(O)), limpa_regiao_inimigo(O), false);
		(passos(P), sul(P,S), sul(S, S_S), passos(S_S), assertThis(inimigo(S)), limpa_regiao_inimigo(S), false);
		
		/*se dois adjacentes tem flash, infere teleport na diagonal correspondente e tira pteleport e poe nteleport em volta*/
		(flash(P), diagonal(P, D), flash(D), infere_teleport_adjacente(P, D), false);
		
		/*se tem flash e no lado oposto tb, infere teleporte no meio*/
		(flash(P), norte(P,N), norte(N, N_N), flash(N_N), assertThis(teleport(N)), limpa_regiao_teleport(N), false);
		(flash(P), leste(P,L), leste(L, L_L), flash(L_L), assertThis(teleport(L)), limpa_regiao_teleport(L), false);
		(flash(P), oeste(P,O), oeste(O, O_O), flash(O_O), assertThis(teleport(O)), limpa_regiao_teleport(O), false);
		(flash(P), sul(P,S), sul(S, S_S), flash(S_S), assertThis(teleport(S)), limpa_regiao_teleport(S), false);
		
		/*se A eh nburaco, ninimigo e nteleport tira nCoisa e poe livre(A)*/
		(nburaco(A), ninimigo(A), nteleport(A), retractThis(nburaco(A)), retractThis(ninimigo(A)), retractThis(nteleport(A)), assertThis(livre(A)), false);
		
		/*se tem powerup em P, guarda powerup(A)*/
		(m_powerup(P), assertThis(powerup(P)), false);
		
		/*se tem ouro em P, guarda ouro(A)*/
		(m_ouro(P), assertThis(ouro(P)), false);
		
		sofrer;
		true
	).

sofrer :- posicao(P),
(
	/*se tem inimigo50, perde 50 pontos e toma 50 de dano*/
	(m_inimigoD(P,_), pontos(Q), R is Q - 50, vida(V), U is V - 50, retractall(pontos(_)), assertThis(pontos(R)), retractall(vida(_)), assert(vida(U)), assertThis(inimigo(P)), limpa_regiao_inimigo(P), vida(V), V < 1, pontos(Q), R is Q - 1000, retractall(pontos(_)), assertThis(pontos(R)), false);

	/*se tem inimigo20, perde 20 pontos e toma 20 de dano*/
	(m_inimigod(P,_), pontos(Q), R is Q - 20, vida(V), U is V - 20, retractall(pontos(_)), assertThis(pontos(R)), retractall(vida(_)), assert(vida(U)), assertThis(inimigo(P)), limpa_regiao_inimigo(P), vida(V), V < 1, pontos(Q), R is Q - 1000, retractall(pontos(_)), assertThis(pontos(R)), false);
	
	/*se tem buraco, morre e perde 1000 pontos*/
	(m_buraco(P), retractall(vida(_)), assert(vida(0)), assertThis(buraco(P)), limpa_regiao_buraco(P), pontos(Q), R is Q - 1000, retractall(pontos(_)), assertThis(pontos(R)), false);
	
	/*se tem teleporte, eh teleportado, observa e sofre*/
	(m_teleport(P), random_between(1, 12, X), random_between(1, 12, Y), retractall(posicao(_)), assert(posicao(p(X,Y))), observar);
	
	true
).

mata_inimigoD(T) :- write("grito"), retractall(m_inimigoD(T,_)), limpa_regiao_inimigo(T), retractThis(pinimigo(T)), assertThis(livre(T)),
(
	(adjacente(T,A), retractThis(passos(A)), false);
	true
).

mata_inimigod(T) :- write("grito"), retractall(m_inimigod(T,_)), limpa_regiao_inimigo(T), retractThis(pinimigo(T)), assertThis(livre(T)),
(
	(adjacente(T,A), retractThis(passos(A)), false);
	true
).

atirar :- posicao(P), direcao(D), balas(M), M > 0, N is M - 1, retractall(balas(_)), assertThis(balas(N)), pontos(Q), R is Q - 10, retractall(pontos(_)), assertThis(pontos(R)),
	(
		(D = 'U', norte(P, T), assertThis(tiro(T)));
		(D = 'R', leste(P, T), assertThis(tiro(T)));
		(D = 'D', sul(P, T), assertThis(tiro(T)));
		(D = 'L', oeste(P, T), assertThis(tiro(T)))
	),
	(
		m_inimigoD(T, V), random_between(20, 50, Dano), NV is V - Dano, retractThis(m_inimigoD(T,V)), assertThis(m_inimigoD(T,NV)), NV < 1, mata_inimigoD(T);
		m_inimigod(T, V), random_between(20, 50, Dano), NV is V - Dano, retractThis(m_inimigod(T,V)), assertThis(m_inimigod(T,NV)), NV < 1, mata_inimigod(T)
	),
	retractThis(tiro(T)).
	
pegar_ouro :- posicao(P), ouro(P), o_coletados(O), retract(ouro(P)), retract(m_ouro(P)), retract(o_coletados(O)), O1 is O + 1, assert(o_coletados(O1)), pontos(Q), R is Q + 1000, retract(pontos(Q)), assert(pontos(R)).

pegar_powerup :- posicao(P), powerup(P), p_coletados(O), retract(powerup(P)), retract(m_powerup(P)), retract(p_coletados(O)), O1 is O + 1, assert(p_coletados(O1)), vida(Q), R is Q + 20, retract(vida(Q)), assert(vida(R)), R > 100, S is 100, retract(vida(R)), assert(vida(S)).

sair :- posicao(p(1,1)), pontos(Q), R is Q - 1, retractall(pontos(_)), assert(pontos(R)).

virar :- direcao(D),
	(
		(D = 'U', retractall(direcao(_)), assert(direcao('R')));
		(D = 'R', retractall(direcao(_)), assert(direcao('D')));
		(D = 'D', retractall(direcao(_)), assert(direcao('L')));
		(D = 'L', retractall(direcao(_)), assert(direcao('U')))
	),
	pontos(P), Q is P - 1, retractall(pontos(_)), assert(pontos(Q)).
	
andar :- posicao(P), direcao(D),
	(
		(D = 'U', norte(P, P1), retractall(posicao(_)), assert(posicao(P1)));
		(D = 'R', leste(P, P1), retractall(posicao(_)), assert(posicao(P1)));
		(D = 'D', sul(P, P1), retractall(posicao(_)), assert(posicao(P1)));
		(D = 'L', oeste(P, P1), retractall(posicao(_)), assert(posicao(P1)))
	),
	pontos(Q), R is Q - 1, retractall(pontos(_)), assert(pontos(R)).

/*SOMENTE PARA TESTE! APAGAR DEPOIS!!!*/
andar_cima :- posicao(p(X,Y)), retractThis(posicao(p(X,Y))), NY is Y + 1, assertThis(posicao(p(X,NY))), observar.
andar_baixo :- posicao(p(X,Y)), retractThis(posicao(p(X,Y))), NY is Y - 1, assertThis(posicao(p(X,NY))), observar.
andar_direita :- posicao(p(X,Y)), retractThis(posicao(p(X,Y))), NX is X + 1, assertThis(posicao(p(NX,Y))), observar.
andar_esquerda :- posicao(p(X,Y)), retractThis(posicao(p(X,Y))), NX is X - 1, assertThis(posicao(p(NX,Y))), observar.
virar_cima :- retractall(direcao(_)), assert(direcao('U')).
virar_baixo :- retractall(direcao(_)), assert(direcao('D')).
virar_direita :- retractall(direcao(_)), assert(direcao('R')).
virar_esquerda :- retractall(direcao(_)), assert(direcao('L')).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Possivel problema
pproblema(P) :- pburaco(P); pinimigo(P); pteleport(P); parede(P).

/* P = Posicao atual
 * D = Direcao atual ('U', 'D', 'R', 'L')
 * P2 = Proxima posicao
 */
prox_mesma_dir(P, D, P2) :- (D = 'U'), norte(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 'D'), sul(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 'R'), leste(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 'L'), oeste(P, P2).

/* P = Posicao atual
 * D = Direcao atual ('U', 'D', 'R', 'L')
 * P2 = Proxima posicao
 */
prox_1_giro(P, D, P2) :- (D = 'U'), leste(P, P2).
prox_1_giro(P, D, P2) :- (D = 'D'), oeste(P, P2).
prox_1_giro(P, D, P2) :- (D = 'R'), sul(P, P2).
prox_1_giro(P, D, P2) :- (D = 'L'), norte(P, P2).

% D - direcao atual
% D2 - direcao depois de girar 1 vez
dir_1_giro(D) :- D = 'U', D2 = 'R'.
dir_1_giro(D) :- D = 'R', D2 = 'D'.
dir_1_giro(D) :- D = 'D', D2 = 'L'.
dir_1_giro(D) :- D = 'L', D2 = 'U'.

/* P = Posicao atual
 * D = Direcao atual ('U', 'D', 'R', 'L')
 * A = Acao:
 * A = 'T' -> atirar
 * A = 'R' -> rodar pra direita
 * A = 'A' -> andar pra frente
 * A = 'P' -> pegar ouro / power up
 * A = 'S' -> ir para a saida e sair
 * A = 'D' -> ir para uma posicao desconhecida
 * A = 'I' -> subir
*/
prox(A) :- posicao(P), ouro(P), A = 'P'. /* Se estiver junto do ouro, pega */

% Se ja tiver todos os o_coletados, e esta na saida, sobe
prox(A) :- o_coletados(3), posicao(p(1,1), A = 'I'.

% Se ja tiver todos os o_coletados, vai pra saida
prox(A) :- o_coletados(3), A = 'S'.

/* Continua na mesma direcao, a nao ser que ja tenha visitado ou seja problema */
prox(A) :- posicao(P), direcao(D), prox_mesma_dir(P, D, P2), (\+ pproblema(P2)), (\+ visitado(P2)), A = 'A'.

/* Tenta girando vezes */
prox(A) :-
  posicao(P), direcao(D),
  prox_1_giro(P, D, P2),
  dir_1_giro(D, D2),
  prox_1_giro(P2, D2, P3),
  dir_1_giro(D2, D3)
  prox_1_giro(P3, D2, P4),
  (
    ((\+ pproblema(P2)), (\+ visitado(P2)), A = 'R');
    ((\+ pproblema(P3)), (\+ visitado(P3)), A = 'R');
    ((\+ pproblema(P4)), (\+ visitado(P4)), A = 'R')
  ).

% todas as opcoes sao ja visitadas ou problematicas, tenta fugir de problema
% roda um A* para o nao visitado mais proximo
prox(A) :- A = 'D'.
