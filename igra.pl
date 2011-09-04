%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% rijesi(+Pozicija1, -Duljina)
%% Pronalazi rjesenje Pozicija-e i broj koraka
%% pri tom rjesenju unificira s Duljina
rijesi(P,Duljina):-
  time(
    depth_first_search(arc,P,pobjeda,R)
%    breadth_first_search_slow(arc,P,pobjeda,R)
%    best_first_search_st_ad(arc,P,vrijednost,pobjeda,R)
  ),
  length(R,Duljina).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% arc(+Pozicija1, -Pozicija2)
%% Opisuje moguce prijelaze izmedu pozicija igre
arc(G1,G2):-
  potez(G1,_,_,_,G2).
%  print_array(G1),
%  print_array(G2),
%  read(Answer),nl,
%  Answer \= !.
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% pobjeda(+Pozicija)
%% (izvedba nedostaje)
%% 
%% Ispituje da li je Pozicija konacna,
%% tj. da li je igra rijesena

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% closing(+Val,+Node)
%
%% omogucava dijagnosticki ispis svakog posjecenog
%% cvora u kojem je vrijednost heuristicke funkcije Val
%% veci od 4.
%
%% poziv ugradenog predikata read omogucava prekidanje
%% pretrazivanja (upisati !.<CR>), odnosno rjesava problem 
%% prebrzog skroliranja ekrana (nakon analize stanja igre
%% unijeti <bilo-sto>.<CR>)

closing(_,_).
%closing(Val,Node):-
%  write(Val),nl,
%  ( Val<4, closing(Node),!;
%    true).

closing(_).
%closing(Node):-
%  print_array(Node),
%  read(Answer),nl,
%  Answer \= !.


%rjesiva
igra40([
  [x,3],
  [2,1]
]).
%nerjesiva
igra41([
  [1,3],
  [x,2]
]).


%nerjesiva
igra60([
  [2,3,x],
  [5,4,1]
]).
%rjesiva
igra61([
  [2,3,x],
  [4,5,1]
]).
%rjesiva
igra62([
  [2,3,x],
  [4,5,1]
]).

%nerjesiva
igra80([
  [2,3,x,6],
  [5,4,1,7]
]).
%rjesiva
igra81([
  [3,2,x,6],
  [5,4,1,7]
]).
%rjesiva
igra82([
  [3,2,x,6],
  [5,4,1,7]
]).



%rjesiva
igra90([
  [x,3,4],
  [5,1,6],
  [2,8,7]
]).
%rjesiva
igra91([
  [8,3,4],
  [5,x,6],
  [2,1,7]
]).
%rjesiva
igra92([
  [x,8,7],
  [6,5,4],
  [3,2,1]
]).

gamef0([
  [ 5, 6,10, 7],
  [15,12, x, 3],
  [13, 8, 1, 4],
  [ 9,14,11, 2]
]).

