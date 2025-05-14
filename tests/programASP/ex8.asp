% example 8

#(dom(x,[1,2])).
#(dom(y,[1,2])).

a :- not b.
b :- not a.

#(nequal(x,y)) :- a.
#(equal(x,y)).
