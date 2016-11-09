:- dynamic brisa/2.
:- dynamic nbrisa/2.
:- dynamic buraco/1.

:- dynamic passos/2.
:- dynamic npassos/2.
:- dynamic inimigo/1.

:- dynamic flash/2.
:- dynamic nflash/2.
:- dynamic teleport/1.

:- dynamic livre/2.
:- dynamic ouro/2.
:- dynamic powerup/2.
:- dynamic balas/1.
:- dynamic vida/1.

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


parede(p(X,Y)) :- parede(X,Y).
parede(0,_).
parede(_,0).
parede(13,_).
parede(_,13).

livre(p(X,Y)) :- livre(X,Y).
livre(1,1).
livre(2,1).
livre(1,2).

/* Sabidamente nao tem brisa */
nbrisa(p(X,Y)) :- nbrisa(X,Y).
nbrisa(1,1).

brisa(p(X,Y)) :- brisa(X,Y).

/* Teste ----- */
brisa(1,2).
brisa(2,1).
brisa(3,2).
brisa(2,3).
/* ----------- */

/* Sabidamente nao eh buraco */
nburaco(P) :- livre(P); parede(P). /* Adicionar outros inimigos aqui */
nburaco(P) :- norte(P, N), nbrisa(N).
nburaco(P) :- sul(P, S),   nbrisa(S).
nburaco(P) :- leste(P, L), nbrisa(L).
nburaco(P) :- oeste(P, O), nbrisa(O).

/* Possivel buraco */
pburaco(P) :- (\+ nburaco(P)), norte(P, N), brisa(N).
pburaco(P) :- (\+ nburaco(P)), sul(P, S),   brisa(S).
pburaco(P) :- (\+ nburaco(P)), leste(P, L), brisa(L).
pburaco(P) :- (\+ nburaco(P)), oeste(P, O), brisa(O).

flash(p(X,Y)) :- flash(X,Y).

/* Sabidamente nao eh teleport */
nteleport(P) :- livre(P); parede(P). /* Adicionar outros inimigos aqui */
nteleport(P) :- norte(P, N), nflash(N).
nteleport(P) :- sul(P, S),   nflash(S).
nteleport(P) :- leste(P, L), nflash(L).
nteleport(P) :- oeste(P, O), nflash(O).

/* Possivel teleport */
pteleport(P) :- (\+ nteleport(P)), norte(P, N), flash(N).
pteleport(P) :- (\+ nteleport(P)), sul(P, S),   flash(S).
pteleport(P) :- (\+ nteleport(P)), leste(P, L), flash(L).
pteleport(P) :- (\+ nteleport(P)), oeste(P, O), flash(O).

passos(p(X,Y)) :- passos(X,Y).

/* Sabidamente nao eh inimigo */
ninimigo(P) :- livre(P); parede(P). /* Adicionar outros inimigos aqui */
ninimigo(P) :- norte(P, N), npassos(N).
ninimigo(P) :- sul(P, S),   npassos(S).
ninimigo(P) :- leste(P, L), npassos(L).
ninimigo(P) :- oeste(P, O), npassos(O).

/* Possivel inimigo */
pinimigo(P) :- (\+ ninimigo(P)), norte(P, N), passos(N).
pinimigo(P) :- (\+ ninimigo(P)), sul(P, S),   passos(S).
pinimigo(P) :- (\+ ninimigo(P)), leste(P, L), passos(L).
pinimigo(P) :- (\+ ninimigo(P)), oeste(P, O), passos(O).

/* Posicao possivelmente problematica */
pproblema(P) :- pburaco(P); pteleport(P); pinimigo(P); parede(P).

/* Infere posicoes sem inimigo baseado nos inimigos encontrados
 * e sabendo que nao ha 2 do mesmo tipo promixos */
infere(P) :- infere_brisa(P), infere_flash(P), infere_passos(P).

infere_brisa_ne(P) :- norte(P, N), leste(P, L), nordeste(P, NE),
                      %nbrisa(P), brisa(N), brisa(L),
                      nburaco(P), assert(buraco(NE)),
                      nordeste(NE, NE_NE), assert(nburaco(NE_NE)),
                      leste(L, L_L), assert(nburaco(L_L)),
                      norte(N, N_N), assert(nburaco(N_N)),
                      oeste(N, N_O), assert(nburaco(N_O)),
                      nordeste(N_N, N_N_NE), assert(nburaco(N_N_NE)),
                      sul(L, L_S), assert(nburaco(L_S)),
                      leste(NE, NE_L), assert(nburaco(NE_L)).

infere_brisa_se(P) :- sul(P, S), sul(S, S_S), infere_brisa_ne(S_S).

/* P = Posicao atual
 * D = Direcao atual ('n', 's', 'l', 'o')
 * P2 = Proxima posicao
 */
prox_mesma_dir(P, D, P2) :- (D = 'n'), norte(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 's'), sul(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 'l'), leste(P, P2).
prox_mesma_dir(P, D, P2) :- (D = 'o'), oeste(P, P2).

/* P = Posicao atual
 * D = Direcao atual ('n', 's', 'l', 'o')
 * P2 = Proxima posicao
 */
prox_1_giro(P, D, P2) :- (D = 'n'), leste(P, P2).
prox_1_giro(P, D, P2) :- (D = 's'), oeste(P, P2).
prox_1_giro(P, D, P2) :- (D = 'l'), sul(P, P2).
prox_1_giro(P, D, P2) :- (D = 'o'), norteP, P2).

/* P = Posicao atual
 * D = Direcao atual ('n', 's', 'l', 'o')
 * A = Acao:
 * A = 'a' -> andar pra frente
 * A = 'g' -> girar pra direita
 * A = 'p' -> pegar ouro / power up
 * A = 't' -> atirar
*/
prox(P, _, A) :- ouro(P), A = 'p'. /* Se estiver junto do ouro, pega */

/* Continua na mesma direcao, a nao ser que ja tenha visitado ou seja problema */
prox(P, D, A) :- prox_mesma_dir(P, D, P2), (\+ pproblema(P2)), (\+ livre(P2)), A = 'a'.

/* Tenta girando 1 vez */
prox(P, D, A) :- prox_1_giro(P, D, P2), (\+ pproblema(P2)), (\+ livre(P2)), A = 'g'.

/* Tenta girando 2 vezes */
prox(P, D, A) :-
  prox_1_giro(P, D, P2),
  prox_1_giro(P2, D, P3),
  (\+ pproblema(P3)), (\+ livre(P3)), A = 'g'.

/* Tenta girando 3 vezes */
prox(P, D, A) :-
  prox_1_giro(P, D, P2),
  prox_1_giro(P2, D, P3),
  prox_1_giro(P3, D, P4),
  (\+ pproblema(P4)), (\+ livre(P4)), A = 'g'.

/* todas as opcoes sao ja visitadas ou problematicas, tenta fugir de problema */

/* Continua na mesma direcao, a nao ser que seja problema */
prox(P, D, A) :- prox_mesma_dir(P, D, P2), (\+ pproblema(P2)), A = 'a'.

/* Tenta girando 1 vez */
prox(P, D, A) :- prox_1_giro(P, D, P2), (\+ pproblema(P2)), A = 'g'.

/* Tenta girando 3 vezes */
prox(P, D, A) :-
  prox_1_giro(P, D, P2),
  prox_1_giro(P2, D, P3),
  prox_1_giro(P3, D, P4),
  (\+ pproblema(P4)), A = 'g'.

/* So volta se nao tiver opcao */
prox(P, D, A) :-
  prox_1_giro(P, D, P2),
  prox_1_giro(P2, D, P3),
  (\+ pproblema(P3)), A = 'g'.

