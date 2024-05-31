% example program for ICLP

a.
b :- not a.
g :- a, not d, #(nequal(x,y)).
d :- not g, not e.
e :- b, not f, not h.
f :- #(equal(x,5)), #(equal(y,5)).
#(leq(x,y,3)).
:- #(greater(x,y)).
#(dom(x,[1,2,3,4,5])).
#(dom(y,[1,2,3,4,5])).
