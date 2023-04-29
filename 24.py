import itertools

# define a function to check if a solution is valid
def is_valid_solution(expr):
    try:
        result = eval(expr)
        #print("test: " + expr + '=' + str(result))
        return result == 24
    except:
        return False

# define a function to generate all possible expressions
def generate_expressions(numbers):

    # for different permutation of the numbers
    for perm in itertools.permutations(numbers):

        # for differen permutations of the 4 operations, get 3 out of them
        for op1, op2, op3 in itertools.product(['+', '-', '*', '/'], repeat=3):

            # for different brackets combination
            exprs = [
                f'({perm[0]} {op1} {perm[1]}) {op2} {perm[2]} {op3} {perm[3]}',
                f'{perm[0]} {op1} ({perm[1]} {op2} {perm[2]}) {op3} {perm[3]}',     # 
                f'{perm[0]} {op1} {perm[1]} {op2} ({perm[2]} {op3} {perm[3]})',     # a+b*(c+d)
                f'(({perm[0]} {op1} {perm[1]}) {op2} {perm[2]}) {op3} {perm[3]}',   # (a+b)*(c+d)
                f'({perm[0]} {op1} {perm[1]}) {op2} ({perm[2]} {op3} {perm[3]})',   #
                f'({perm[0]} {op1} {perm[1]} {op2} ({perm[2]}) {op3} {perm[3]}',    #
            ]
            for expr in exprs:
                if is_valid_solution(expr):
                    yield expr
                

# main function to play the game
def play_game(numbers = []):

    # print('Welcome to the 24 game!')
    # print('You are given 4 cards. Use all four numbers on the card, but use each number only once.')
    # print('You can add, subtract, multiply and divide.')

    # input the numbers
    if len(numbers) == 0:
        while True:
            try:
                numbers = [int(x) for x in input('Enter four numbers separated by spaces: ').split()]
                if len(numbers) != 4:
                    raise ValueError
                break
            except ValueError:
                print('Invalid input, please try again.')

    # generate solutions
    solutions = list(generate_expressions(numbers))
    if solutions:
        print('Congratulations, you win!')
        for solution in solutions:
            print(solution)
    else:
        print('Sorry, no solution found.')

    print('')

##

def test1():
    for perm in itertools.permutations([1,2,3,4]):
        print(perm)

##

def test2():
    for op1, op2, op3 in itertools.product(['+', '-', '*', '/'], repeat=3):
        print (f"{op1} {op2} {op3}")
    exit()

##

# test1()
# test2()
# exit()

# play_game([2, 2, 5, 8])
# play_game([6, 7, 7, 10])
# play_game([3, 4, 6, 9])
# play_game([10, 10, 8, 5])
# exit()

while True:
   play_game()