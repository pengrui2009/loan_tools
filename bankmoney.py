#/usr/bin/python3
import os
import sys
import math
import requests

def get_rate():
    url = 'http://api.xxx.com/rate'
    response = requests.get(url)
    rate = float(response.text)
    return rate

# prinicipal:本金
# annual_rate:年利率
# years:还款年限

def calculate_repayment_pri_int(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    months = years * 12
    repayment = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    total_interest = repayment * months - principal
    month_interests = []
    for i in range(months) :
        month_interests.append(10000 * principal * monthly_rate * (((1 + monthly_rate) ** months) - ((1 + monthly_rate) ** (i-1))) / ((1 + monthly_rate) ** months-1))
    return (repayment, total_interest, month_interests)

def calculate_repayment_pri(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    months = years * 12
    repayments = []
    month_interests = []
    repayment_pri = principal / months
    total_interest = 0
    for i in range(months):
        interest = principal * monthly_rate
        total_interest += interest
        principal -= repayment_pri
        repayment = repayment_pri + interest
        repayments.append(repayment)
        month_interests.append((principal - interest * i) * monthly_rate * 10000)
    return (repayments, total_interest, month_interests)

def main(argv):
    # print('{}'.format(argv))
    bussiness_principal = 190
    bussiness_rate = 3.8 * 0.01

    commonfund_principal = 90
    commonfund_rate = 3.1 * 0.01

    print('same load pay:')
    result00 = calculate_repayment_pri_int(bussiness_principal, bussiness_rate, 15)
    # print('{} {}'.format(result00[0] * 10000, result00[1]))
    result01 = calculate_repayment_pri_int(commonfund_principal, commonfund_rate, 15)
    print('{} {} {} '.format((result00[0] * 10000 + result01[0] * 10000), 
        (result00[1] + result01[1]), (result00[2][0] + result01[2][0])))

    total_pay = 0
    left_total_money = (result00[0] * 10000 + result01[0] * 10000) * 15 * 12
    for index in range(15, 0, -1):
        left_total_money 


    print('some money pay:')
    result10 = calculate_repayment_pri(bussiness_principal, bussiness_rate, 20)
    # print('{} {}'.format(result[0][0] * 10000, result[1]))

    result11 = calculate_repayment_pri(commonfund_principal, commonfund_rate, 20)
    print('{} {} {}'.format((result10[0][0] * 10000 + result11[0][0] * 10000), 
        (result10[1]+result11[1]), (result10[2][0] + result11[2][0])))

if __name__ == '__main__':
    main(sys.argv[1:])