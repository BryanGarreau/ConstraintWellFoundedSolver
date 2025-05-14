% example 6

a :- not b, not c.
b :- not a, not c.
c :- not a, not b.
