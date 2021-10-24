# write your code here
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('--type')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--payment')
parser.add_argument('--interest')
'--type=diff --principal=500000 --periods=8 --interest=7.8'
args = parser.parse_args()

counter = 0

if args.type:
    the_type = args.type
    counter += 1
if args.principal:
    principal = float(args.principal)
    counter += 1
else:
    principal = None
if args.periods:
    periods = float(args.periods)
    counter += 1
else:
    periods = None
if args.interest:
    interest = float(args.interest) / (12. * 100)
    counter += 1
else:
    interest = None
if args.payment:
    payment = float(args.payment)
    counter += 1
else:
    payment = None

if counter < 4 or interest is None:
    print('Incorrect parameters')
elif the_type == 'annuity':
    if payment is None:
        loan_interest = interest
        power_calculus = math.pow(1. + loan_interest, periods)
        payment = principal * loan_interest * power_calculus / (power_calculus - 1.)
        payment = math.ceil(payment)
        result = f"Your annuity payment = {payment}!"
        over = f"Overpayment = {periods * payment - principal}"
        print(result)
        print(over)
    elif principal is None:
        annuity = float(payment)
        loan_interest = interest
        power_calculus = math.pow(1. + loan_interest, periods)
        principal = annuity * (power_calculus - 1.) / (loan_interest * power_calculus)
        result = f"Your loan principal = {principal}!"
        over = f"Overpayment = {periods * annuity - principal}"
        print(result)
        print(over)
    elif periods is None:
        monthly = int(payment)
        loan_interest = interest
        n = math.log(monthly / (monthly - loan_interest * principal)) / math.log(1 + loan_interest)
        n = math.ceil(n)
        years = n // 12
        months = n % 12
        result = f"It will take {years} years"
        if months > 0:
            result += f" and {months} months"
        result += " to repay this loan!"
        print(result)
        months += years * 12
        over = f"Overpayment = {months * monthly - principal}"
        print(over)
elif the_type == 'diff':
    monthly_payments = []
    summer = 0
    for i in range(1, int(periods) + 1):
        d = principal / periods
        product = principal * (i - 1) / periods
        product = principal - product
        product *= interest
        d += product
        d = math.ceil(d)
        monthly_payments.append(d)
        print(f'Month {i}: payment is {d}')
        summer += d

    over = summer - principal
    print(f'Overpayment = {over}')

