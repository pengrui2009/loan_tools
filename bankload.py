#!/usr/bin/env python3
# import os
# import sys

# def CommonFound(money, year, method_enum) :
#     print('')
#     year_rate = 3.10
#     #等额本息
#     if method_enum == 1:
#         print('')
#     elif method_enum == 2:#等额本金
#         print('')

# def Bussiness(money, year, method_enum):
#     print('')
#     year_rate = 3.80 * 0.01
#     #等额本息
#     if method_enum == 1:
#         month_rate = year_rate / 12
#         month_pay = money * month_rate * (1+month_rate)^year*12
#         print('')
#     elif method_enum == 2:#等额本金
#         print('')

# def main(argv):
#     # os.makedirs('src',exist_ok=True)
#     # os.makedirs('src/codec',exist_ok=True)

#     # with open('src/codec/data_element.c', 'w+') as f:
#     #     f.write('hello world')
#     #     f.write('hello world0000')
#     #     f.close()
#     # asn_handle = ASNCodec('CSAE-157-2020.asn')
#     # asn_handle.handle()
#     print('')

#     commonfund_money = 90
#     bussiness_money = 190


# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from decimal import *


def benqidate(date, k):
    """
    算每一期时间
    :param date: 贷款时间，字符串类型
    :param k: 第几期
    :return: 返回本期的还款日期
    """
    date_daikuan = datetime.strptime(date,'%Y-%m-%d')
    if 1 <= k + date_daikuan.month <= 12:
        date_benqi = date_daikuan + relativedelta(month=k + date_daikuan.month)
    elif 13 <= k + date_daikuan.month <= 24:
        date_benqi = date_daikuan + relativedelta(year=date_daikuan.year + 1, month=k + date_daikuan.month - 12)
    elif 25 <= k + date_daikuan.month <= 36:
        date_benqi = date_daikuan + relativedelta(year=date_daikuan.year + 2, month=k + date_daikuan.month - 24)
    else:
        date_benqi = date_daikuan + relativedelta(year=date_daikuan.year + 4, month=k + date_daikuan.month - 48)
    return date_benqi


def calD(date, n=36):
    """
    算本期的天数，用列表表示出来，精确到天
    :param date: 贷款日期
    :param n: 期数
    :return: 每期天数的列表
    """
    result_D = []
    for i in range(1, n+1):
        date_daikuan = datetime.strptime(date, '%Y-%m-%d')
        if i == 1:
            benqitianshu = (benqidate(date, i) - date_daikuan).days
            result_D.append(benqitianshu)
        else:
            benqitianshu = (benqidate(date, i) - benqidate(date, i - 1)).days
            result_D.append(benqitianshu)
    return result_D



def calmonthpay(date, rent_sum, n=36, r=0.153/360):
    """
    计算每期的租金总额
    :param date: 贷款时间
    :param rent_sum: 贷款总额
    :param n: 期数
    :param r: 日利率
    :return: 每期的租金总额
    """
    D = calD(date)
    M = np.eye(n)
    for i in np.arange(1, n):
        for j in range(i):
            M[i, j] = -r * D[i]
    c1 = np.ones(n) * -1
    c1.shape = (n, 1)
    r1 = np.ones(n + 1).T
    r1[0] = 0
    r1.shape = (1, n + 1)
    M = np.hstack((c1, M))
    M = np.vstack((M, r1))
    B = -r * rent_sum * np.array(D)
    B = np.append(B, [rent_sum])
    X = np.mat(M).I * np.mat(B).T
    return X[0, 0]


def calzujin(date, rent_sum,  n=36, rate=0.153):
    """
    计算各个所需的参数
    :param rate: 年利率
    :param date: 贷款日期,输入为字符串形式
    :param rent_sum:本金总额
    :param n: 期数
    :return:返回每期的利息，当期本金和期末本金
    """
    month_pay = calmonthpay(date, rent_sum)
    print(month_pay)
    month_pay = Decimal(str(month_pay)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    month_pay = np.float(month_pay)
    result_lixi = []
    result_dangqi = []
    result_qimou = []
    lixi_sum_list = []
    sum = 0
    lixi_sum = 0
    for i in range(1, n+1):
        date_daikuan = datetime.strptime(date, '%Y-%m-%d')
        if i == 1:
            benqitianshu = (benqidate(date, i) - date_daikuan).days
            dangqi_lixi = (rent_sum * rate) / 360 * benqitianshu
            result_lixi.append(dangqi_lixi)
            rent_dangqi = month_pay - dangqi_lixi
            sum += round(rent_dangqi, 2)
            result_dangqi.append(rent_dangqi)
            rent_sum_qimou = rent_sum - rent_dangqi
            result_qimou.append(rent_sum_qimou)
            lixi_sum += dangqi_lixi
            lixi_sum_list.append(lixi_sum)
        elif 2 <= i <= 47:
            benqitianshu = (benqidate(date, i) - benqidate(date, i-1)).days
            rent_sum_qichu = rent_sum_qimou
            dangqi_lixi = (rent_sum_qichu * rate) / 360 * benqitianshu
            result_lixi.append(dangqi_lixi)
            rent_dangqi = month_pay - dangqi_lixi
            sum += round(rent_dangqi, 2)
            result_dangqi.append(rent_dangqi)
            rent_sum_qimou = rent_sum_qichu - rent_dangqi
            result_qimou.append(rent_sum_qimou)
            lixi_sum += dangqi_lixi
            lixi_sum_list.append(lixi_sum)
        else:
            benqitianshu = (benqidate(date, i) - benqidate(date, i - 1)).days
            rent_sum_qichu = rent_sum - sum
            dangqi_lixi = (rent_sum_qichu * rate) / 360 * benqitianshu
            result_lixi.append(dangqi_lixi)
            rent_dangqi = rent_sum - sum
            result_dangqi.append(rent_dangqi)
            rent_sum_qimou = rent_sum_qichu - rent_dangqi
            result_qimou.append(rent_sum_qimou)
            lixi_sum += dangqi_lixi
            lixi_sum_list.append(lixi_sum)
    month_pay = Decimal(str(month_pay)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    lixi_qimou = [lixi_sum-i for i in lixi_sum_list]
    return month_pay, result_lixi, result_dangqi, result_qimou, lixi_qimou


def calrent_sum(month_pay, date, n=36, r=0.153/360):
    D = calD(date=date)
    M = np.eye(n)
    for i in np.arange(1, n):
        for j in range(i):
            M[i, j] = -r * D[i]
    # 然后进行矩阵的拼接
    c1 = np.ones(n)
    for i in range(n):
        c1[i] = r * D[i]
    # 将c1拼接到矩阵中
    c1.shape = (n,1)
    M = np.hstack((c1, M))
    c2 = np.ones(n+1)
    c2[0] = -1
    c2.shape = (1, n+1)
    M = np.vstack((M, c2))
    # 构造月供矩阵
    A = np.ones(n+1).T
    for i in range(n):
        A[i] = month_pay
    A[36] = 0
    A.shape = (n+1, 1)
    X = np.mat(M).I * np.mat(A)
    return X[0,0]


if __name__ == '__main__':
    d, a, b, c, e = calzujin("2018-07-01", 100877)
    sum = 0
    for i in range(36):
        print("第 %d 期利息为:%.2f" % (i+1, round(a[i], 2)))
        sum += round(a[i], 2)
    print(sum)
    print("\n")
    for j in range(36):
        print("第 %d 期本金为:%.2f" % (j+1, round(b[j], 2)))
    print("\n")
    for k in range(36):
        print("第 %d 期末本金为:%.2f" % (k+1,round(c[k], 2)))
    print("每期月供: %s" % (d))
    for m in range(36):
        print("第 %d 期末剩余利息为:%.2f" % ( m+ 1, round(e[m], 2)))


# if __name__ == '__main__':
#     main(sys.argv[1:])