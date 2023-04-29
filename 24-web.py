
from flask import Flask, request, send_file
from urllib.request import urlopen
import json

app = Flask(__name__)

#
# FRONTEND
#

@app.route('/')
def index():
    return '''
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta id="viewport" name="viewport" content ="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
<meta name="theme-color" content="#ffffff">
<title>The Game of 24</title>
<style>
textarea,input, button{
    margin:6px 0px !important;
    display:block;
    width:100%;
    padding:10px;
    font-size:24px!important;
    text-align: center;
}
textarea{
    font-size:12px;
    resize:none!important;
    height: calc(100% - 230px);
    overflow-y: auto !important;
    background-color: lightgreen;
}
#tbl-numbers{
    width:100%;
}
#tbl-numbers td{
    width:25%;
}
#inp-numbers{
    display:none;
}
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/css/bootstrap.min.css" integrity="sha512-SbiR/eusphKoMVVXysTKG/7VseWii+Y3FdHrt0EpKgpToZeemhqHeZeLWLhJutz/2ut2Vw1uQEj2MbRF+TVBUA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.4/jquery.min.js" integrity="sha512-pumBsjNRGGqkPzKHndZMaAG+bir374sORyzM3uulLV14lN5LyykqNk8eEeUlUkB3U0M4FApyaHraT65ihJhDpQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>
function generate_nos(){
    $('input[type=number]').each(function(){
        $(this).val(parseInt(Math.random()*10)+1);
    });
    $('#ta-results').text('');     
}
async function submit_nos(){
    var numbers = [];
    $('input[type=number]').each(function(){
        var n = $(this).val().trim();
        if (n && !isNaN(n)){
            numbers.push(parseInt(n));
        }
    });
    $('#inp-numbers').val(numbers.join(' '));
    var inp_numbers = $('#inp-numbers').val();
    if (!inp_numbers || inp_numbers.split(' ').length != 4){
        $('#ta-results').text(inp_numbers + ' does not conform the format: 1 2 3 4');
        return;
    }

    fetch('/generate?inp_numbers=' + inp_numbers)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        var output = '';
        if (data.error){
            output = data.error;
        } else {
            var sols = data.solutions;
            if (sols.length){
                output = sols.join("\\n");
            } else {
                output = inp_numbers + " has no solutions.";
            }
        }
        $('#div-possible-permutations').text(data.solutions.length + '/' + data.possible_permutations);
        $('#ta-results').text(output);        
        $('input[type=number]').focus(function(){
            $(this).select();
        });
        $('input[type=number]').eq(0).focus();
    });
}    

$(document).ready(function(){
    $('#btn-generate').click(generate_nos);
    $('#btn-submit').click(submit_nos);
    $('input')
        .keyup(function(e){
            if (e.which === 13)
                submit_nos();
        })
        .focus();
});
</script>
</head>
<body>
<table id="tbl-numbers">
<tr>
    <td>
        <input type="number" id="card1" name="card1" min="1" max="10">
    </td>
    <td>
        <input type="number" id="card2" name="card2" min="1" max="10">
    </td>
    <td>
        <input type="number" id="card3" name="card3" min="1" max="10">
    </td>
    <td>
        <input type="number" id="card4" name="card4" min="1" max="10">
    </td>
</tr>
</table>
<input id="inp-numbers" type="text" placeholder="4 nos. for 24 (separated by spaces)" value="">
<button id="btn-generate" class="btn btn-primary">Generate</button>
<button id="btn-submit" class="btn btn-warning">Show solutions</button>
<div style="display:flex; width:100%">
    <div style="text-align:left; width:50%">Solutions</div>
    <div style="text-align:right; width:50%" id="div-possible-permutations"></div>
</div>
<textarea id="ta-results"></textarea>
</body>
</html>
'''

@app.route('/generate')
def generate():
    inp_numbers = request.args.get('inp_numbers')
    numbers = [int(x) for x in inp_numbers.split()]
    error = ''
    solutions = []
    global possible_permutations
    possible_permutations = 0

    if len(numbers) != 4:
        error = inp_numbers + ' has a wrong format: 1 2 3 4'
    else:
        solutions = list(generate_expressions(numbers))

    return {
        'error': error,
        'inp_numbers': inp_numbers,
        'solutions': solutions,
        'possible_permutations': possible_permutations,  
    }

#
# BACKEND
#

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
possible_permutations = 0
def generate_expressions(numbers):
    global possible_permutations
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
                possible_permutations += 1
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

# while True:
#    play_game()