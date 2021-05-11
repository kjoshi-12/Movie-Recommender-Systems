% predictes for knowledge_base.pl
% a menu with multiple options to filter movies based
% on certain content such as genre, authors,rating, or combination of
% options.

%imports the user data as facts in the form likes(UserNumber, Genre, Actor)
import:-
    csv_read_file('userData.csv', Data, [functor(likes), separator(0',)]),
    maplist(assert, Data).

%Takes a list of lists and turns it into just one list
makeOneDArray(X,[X]) :- \+ is_list(X).
makeOneDArray([],[]).
makeOneDArray([X|Xs],Zs) :- makeOneDArray(X,Y), makeOneDArray(Xs,Ys), append(Y,Ys,Zs).

%Source code for the mode of the list:https://stackoverflow.com/questions/50437617/prolog-function-that-returns-the-most-frequent-element-in-a-list
count_repeated([Elem|Xs], Elem, Count, Ys) :-
    count_repeated(Xs, Elem, Count1, Ys), Count is Count1+1.
count_repeated([AnotherElem|Ys], Elem, 0, [AnotherElem|Ys]) :-
    Elem \= AnotherElem.
count_repeated([], _, 0, []).

rle([X|Xs], [[C,X]|Ys]) :-
    count_repeated([X|Xs], X, C, Zs),
    rle(Zs, Ys).
rle([], []).


rle([X|Xs], [[C,X]|Ys]) :-
    count_repeated([X|Xs], X, C, Zs),
    rle(Zs, Ys).
rle([], []).
%End borrowed code

%Deletes the last element of the list
deleteLast([_], []).

deleteLast([H|T], [H|T1]) :- 
    deleteLast(T, T1).

%gets the two most common elements of a list, this is where the borrowed code is used
twoMostCommon(L,M1,M2):- msort(L, SList),rle(SList, RLE),
		           sort(RLE, SRLE),last(SRLE, [_, M1]),deleteLast(SRLE,SRLE1),
			   last(SRLE1,[_, M2]). 


start:- write('*Welcome To Our Movie Recommender*'),nl,nl,
write('Select 1 to view all movies related by genre'),nl,
write('Select 2 to view all movies that are similar based on a rating'),nl,
write('Select 3 to view all movies that are similar based on a actor/actress'),nl,
write('Select 4 to view all movies that the contain the same Actor/Actress & Rating'),nl,
write('Select 5 to view all movies that contain the same Actor/Actress & Genre'),nl,
write('Select 6 to view all movies that contain the same Genre & Rating'),nl,
write('Select 7 to view all movies based on user\'s favorite genre'),nl,
write('Select 8 to view all movies based on user\'s favorite actor'),nl,
write('Select 9 to view all movies based on previously watched movies and only one genre'),nl,
write('Select 10 to view all movies based on previously watched movies and two genres'),nl,
write('Select 11 to view all movies that contain two specific genres'),nl,
write('Select 12 to view all movies that contain two specific Actors/Actress'),nl,
write(' '), read(X), option(X).

% print movies with same genre based on user choice

option(1):-write('Select from the following Genres (\'Family\', \'Crime\', \'Comedy\', \'Drama\',ETC)'),nl,
read(X),forall(film(Y,X,_,_,_,_,_,_,_);
               film(Y,_,X,_,_,_,_,_,_),
               writeln(Y)),again.


% print movies based on ratings

option(2):- write('Enter a Rating from 4.0 - 10.0 '),
nl,nl, read(X),forall(film(Y,_,_,_,_,_,_,_,X),writeln(Y)),again.

% print movies based on a single actor or actress
% order of the actors does not matter

option(3) :-write('Enter a Actor/Actress Name'),nl,nl,read(X),
    forall(film(Y,_,_,X,_,_,_,_,_);film(Y,_,_,_,X,_,_,_,_)
           ;film(Y,_,_,_,_,X,_,_,_);film(Y,_,_,_,_,_,X,_,_)
           ;film(Y,_,_,_,_,_,_,X,_),writeln(Y)),again.

% print movies based on actors/actress & rating

option(4) :-write('Enter the Actor/Actress followed by a Rating'),nl,nl,
    read(X),read(Z),forall(film(Y,_,_,X,_,_,_,_,Z);film(Y,_,_,_,X,_,_,_,Z)
           ;film(Y,_,_,_,_,X,_,_,Z);film(Y,_,_,_,_,_,X,_,Z)
           ;film(Y,_,_,_,_,_,_,X,Z),writeln(Y)),again.

% print movies based on actors/actress & genre

option(5):-write('Enter the Actor/Actress followed by a Genre'),nl,nl,
    read(X),read(Y),forall(film(Z,Y,_,X,_,_,_,_,_);film(Z,_,Y,X,_,_,_,_,_)
                           ;film(Z,_,Y,_,X,_,_,_,_);film(Z,Y,_,_,X,_,_,_,_)
                           ;film(Z,Y,_,_,_,X,_,_,_);film(Z,_,Y,_,_,X,_,_,Z)
                           ;film(Z,Y,_,_,_,_,X,_,Z);film(Z,_,Y,_,_,_,X,_,Z);
                           film(Z,Y,_,_,_,_,_,X,Z);film(Z,_,Y,_,_,_,_,X,Z),writeln(Z)),again.

% print movies based on genre & rating

option(6):-write('Enter the genre followed by a Rating'),nl,nl,
   read(X),read(Y),nl,forall(film(Z,X,_,_,_,_,_,_,Y)
                           ;film(Z,_,X,_,_,_,_,_,Y),writeln(Z)),again.

option(7):-write('Enter your user number'),nl,nl,
    read(X),likes(X,G,_),write('Your favorite genre is: '),write(G),nl,forall(film(M,G,_,_,_,_,_,_,_);
	film(M,_,G,_,_,_,_,_,_),writeln(M)),again.

option(8):-write('Enter your user number'),nl,nl,
    read(X),likes(X,_,A),write('Your favorite actor is: '),write(A),nl,forall(film(M,_,_,A,_,_,_,_,_);
	film(M,_,_,_,A,_,_,_,_);film(M,_,_,_,_,A,_,_,_);film(M,_,_,_,_,_,A,_,_);film(M,_,_,_,_,_,_,A,_),
	writeln(M)),again.

option(9):- csv_read_file('movie.csv', Data, [functor(fact), separator(0',)]),maplist(assert, Data), 
    setof([W, X, Y], fact(W,X,Y), Z), makeOneDArray(Z,L),twoMostCommon(L,G,_),forall(film(M,G,_,_,_,_,_,_,_);
	film(M,_,G,_,_,_,_,_,_),writeln(M)),again.

option(10):- csv_read_file('movie.csv', Data, [functor(fact), separator(0',)]),maplist(assert, Data), 
    setof([W, X, Y], fact(W,X,Y), Z), makeOneDArray(Z,L),twoMostCommon(L,G1,G2),forall(film(M,G1,G2,_,_,_,_,_,_);
	film(M,G2,G1,_,_,_,_,_,_),writeln(M)),again.

% print movies based on two specfic genres of movies
option(11):-write('Select from the following Genres (\'Family\', \'Crime\', \'Comedy\', \'Drama\',ETC)'),nl,
read(X),read(Y),forall(film(Z,X,Y,_,_,_,_,_,_);
               film(Z,Y,X,_,_,_,_,_,_),
               writeln(Z)),again.

% print movies based on two specfic Actors/Actress

option(12):-write('Enter two Actors/Actress'),nl,
read(X),read(Y),forall(film(Z,_,_,X,Y,_,_,_,_);film(Z,_,_,Y,X,_,_,_,_)
                           ;film(Z,_,_,_,X,Y,_,_,_);film(Z,_,_,_,Y,X,_,_,_)
                           ;film(Z,_,_,_,_,X,Y,_,_);film(Z,_,_,_,_,Y,X,_,Z)
                           ;film(Z,_,_,_,_,_,X,Y,Z);film(Z,_,_,_,_,_,Y,X,Z),
                           writeln(Z)),again.





% give the user the choice to make another selection
% based on a genre,rating,actor/actress,or combination.
%
again:- write('Would You Like To Search Again?'),nl,nl,
    write('Select 1 to view all movies related by genre'),nl,
    write('Select 2 to view all movies that are similar based on a rating'),nl,
    write('Select 3 to view all movies that are similar based on a actor/actress'),nl,
    write('Select 4 to view all movies that the contain the same Actor/Actress & Rating'),nl,
    write('Select 5 to view all movies that the contain the same Actor/Actress & Genre'),nl,
    write('Select 6 to view all movies that the contain the same Genre & Rating'),nl,
    write('Select 7 to view all movies based on user\'s favorite genre'),nl,
    write('Select 10 to view all movies that contain two specific genres'),nl,
    write('Select 11 to view all movies that contain two specific Actors/Actress'),nl,
    write('Select 0 to exit.'),nl,
    read(X),option(X);false.
