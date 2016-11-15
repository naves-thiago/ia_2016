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
	inimigo/2,
	
	flash/1,
	pteleport/1,
	nteleport/1,
	teleport/1,
	
	ouro/1,
	powerup/1,
	
	posicao/1,
	vida/1,
	pontos/1,
	balas/1,
	direcao/1
]).

/*posicoes, direcoes, etc*/
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

adjacente(p(X,Y), C) :-
	(Y < 12, norte(p(X,Y), C));
	(Y > 1, sul(p(X,Y), C));
	(X < 12, leste(p(X,Y), C));
	(X > 1, oeste(p(X,Y), C)).

diagonal(p(X,Y), C) :-
	noroeste(p(X,Y), C);
	nordeste(p(X,Y), C);
	sudoeste(p(X,Y), C);
	sudeste(p(X,Y), C).

/*parede*/
parede(p(X,Y)) :- parede(X,Y).
parede(0,_).
parede(_,0).
parede(13,_).
parede(_,13).

/*conhecimento inicial*/
/*livre(p(X,Y)) :- livre(X,Y).
livre(1,1).
livre(2,1).
livre(1,2).*/

/*estado*/
reset :- 
	retractall(posicao(_)),
	retractall(vida(_)),
	retractall(pontos(_)),
	retractall(balas(_)),
	retractall(direcao(_)),
	assert(posicao(p(1,1))),
	assert(vida(100)),
	assert(pontos(0)),
	assert(balas(5)),
	assert(direcao('U')),
	observar.

/*implicacoes do mapa*/
brisa(p(X,Y)) :- brisa(X,Y).
m_brisa(p(X,Y)) :- m_buraco(p(W,Z)), adjacente(p(X,Y),p(W,Z)).

flash(p(X,Y)) :- flash(X,Y).
m_flash(p(X,Y)) :- m_teleport(p(W,Z)), adjacente(p(X,Y),p(W,Z)).

passos(p(X,Y)) :- passos(X,Y).
m_passos(p(X,Y)) :- m_inimigoD(p(W,Z),_), adjacente(p(X,Y),p(W,Z)); m_inimigod(p(W,Z),_), adjacente(p(X,Y),p(W,Z)).

/*%Perceber_Sofrer
perceber_sofrer :- estado(casa(Lin,Col),_,_,Vida,_,_), assert(percorrido(casa(Lin,Col))), 
(
	(brilho(casa(Lin,Col)), assert(tem_brilho(casa(Lin,Col))),false);
	SOBREVIVE DANO FRACO
	(inimigoD(casa(Lin,Col),_), NovaVida is Vida - 20, NovaVida > 0, retract(estado(casa(Lin, Col),Orientacao,Pontos,Vida,Ouros,vivo)), assert(estado(casa(Lin,Col),Orientacao,Pontos,NovaVida,Ouros,vivo)), false); 
	MORRE DANO FRACO
	(inimigoD(casa(Lin,Col),_), NovaVida is Vida - 20, NovaVida =< 0, retract(estado(casa(Lin, Col),Orientacao,Pontos,Vida,Ouros,_)), assert(estado(casa(Lin,Col),Orientacao,Pontos,NovaVida,Ouros,morto)), false);   
	SOBREVIVE DANO FORTE
	(inimigoW(casa(Lin,Col),_), NovaVida is Vida - 50, NovaVida > 0, retract(estado(casa(Lin, Col),Orientacao,Pontos,Vida,Ouros,vivo)), assert(estado(casa(Lin,Col),Orientacao,Pontos,NovaVida,Ouros,vivo)), false); 
	MORRE DANO FORTE
	(inimigoW(casa(Lin,Col),_), NovaVida is Vida - 50, NovaVida =< 0, retract(estado(casa(Lin, Col),Orientacao,Pontos,Vida,Ouros,_)), assert(estado(casa(Lin,Col),Orientacao,Pontos,NovaVida,Ouros,morto)), false); 
	MORRE NO BURACO
	(poco(casa(Lin,Col)), retract(estado(casa(Linha, Coluna),Orientacao,Pontos,Vida,Ouros,_)), NovoPontos is Pontos - 1000, NovaVida is 0, assert(estado(casa(Lin,Col),Orientacao,NovoPontos,NovaVida,Ouros,morto)), false);
	CAI NO TELEPORTE
	(teletransporter(casa(Lin,Col)), teleporte);
	true
).*/

/*observar*/
observar :- posicao(p(X,Y)), assert(visitado(p(X,Y))),
	(
		/*se nao ha perigo, a posicao eh livre e nao tem perigos*/
		(not(m_inimigoD(p(X,Y),_)), not(m_inimigod(p(X,Y),_)), not(m_teleport(p(X,Y))), not(m_buraco(p(X,Y))), assert(livre(p(X,Y))), retract(pinimigo(p(X,Y))), retract(pteleport(p(X,Y))), retract(pburaco(p(X,Y))), false);
		
		/*se tem brisa, infere possiveis buracos*/
		(m_brisa(p(X,Y)), adjacente(p(X,Y), p(W,Z)), not(livre(p(W,Z))), assert(pburaco(p(W,Z))), assert(brisa(p(X,Y))), false);
		
		/*se tem passos, infere possiveis inimigos*/
		(m_passos(p(X,Y)), adjacente(p(X,Y), p(W,Z)), not(livre(p(W,Z))), assert(pinimigo(p(W,Z))), assert(passos(p(X,Y))), false);
		
		/*se tem flash, infere possiveis teleports*/
		(m_flash(p(X,Y)), adjacente(p(X,Y), p(W,Z)), not(livre(p(W,Z))), assert(pteleport(p(W,Z))), assert(flash(p(X,Y))), false);
		
		/*se nao tem nenhum, infere que a posicao e os adjacentes estao livres*/
		
		/*se dois adjacentes tem brisa, infere buraco na diagonal correspondente e tira pburaco e poe nburaco em volta*/
		
		/*se dois adjacentes tem passos, infere inimigo na diagonal correspondente e tira pinimigo e poe ninimigo em volta*/
		
		/*se dois adjacentes tem flash, infere teleport na diagonal correspondente e tira pteleport e poe nteleport em volta*/
		
		/*se p eh nburaco, ninimigo e nteleport tira nCoisa e poe livre(p)*/
		
		true
	).