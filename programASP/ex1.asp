%example 1 
a.
b :- not a.
c :- a, not d.
d :- not c, not e.
e :- b, not f.
e :- e. 
