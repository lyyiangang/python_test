import math

def test_round(a, b):
    print('-------------------------------------')
    print(f'{a}/{b}=', a/b)
    print(f'{a}//{b}=', a//b)
    print(f'round({a}/{b})=', round(a/b))
    print(f'int({a}/{b})=', int(a/b))
    print(f'ceil({a}/{b})=', math.ceil(a/b))
    print(f'floor({a}/{b})=', math.floor(a/b))

test_round(3, 2)
test_round(-3, 2)

test_round(3.3, 2)