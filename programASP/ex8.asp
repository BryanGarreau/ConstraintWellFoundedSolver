% example 8

#(dom(x,[1,2,3,4,5])).
#(dom(y,[1,2,3,4,5])).

a :- not b.
b :- not a.

#(leq3(x,4,y)) :- a.
#(leq3(x,3,y)).
