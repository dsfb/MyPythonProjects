Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> list(map(str, input("Digite alguns números:")))
Digite alguns números:45 86 92 12 34 58
['4', '5', ' ', '8', '6', ' ', '9', '2', ' ', '1', '2', ' ', '3', '4', ' ', '5', '8']
>>> list(map(str, input("Digite alguns números: ").split(" ")))
Digite alguns números: 45 78 12 74 89 82 92 512
['45', '78', '12', '74', '89', '82', '92', '512']
>>> list(map(int, input("Digite alguns números: ").split(" ")))
Digite alguns números: 45 98 123 87 423 843
[45, 98, 123, 87, 423, 843]
>>> tuple(map(int, input("Digite alguns números: ").split(" ")))
Digite alguns números: 142 134 984 238 653 123
(142, 134, 984, 238, 653, 123)
>>> x = lambda: yield map(int, input("Digite alguns números: ").split(" "))
SyntaxError: invalid syntax
>>> 