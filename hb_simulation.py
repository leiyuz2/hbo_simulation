# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:49:55 2019

@author: szhou
"""

import numpy as np

def Yearly_pmt(principal, annual_r, years):

    n = years   # number of  payments
    r = annual_r
    YearlyPayment = (r * principal * ((1+r) ** n)) / (((1+r) ** n) - 1)
    return YearlyPayment

# Generate performance statistics
def performance_measurement(unison_program,proceeds_w_unison,proceeds_n_unison,\
                            number_of_simulation,unison_invmt_prct,home_value):
    if unison_program=="HomeBuyer":
        make_money_w=round(len([i for i in proceeds_w_unison if i>(0.2-unison_invmt_prct)*home_value])/number_of_simulation*100)
        make_money_n=round(len([i for i in proceeds_n_unison if i>(0.2-unison_invmt_prct)*home_value])/number_of_simulation*100)
    else:    
        make_money_w=round(len([i for i in proceeds_w_unison if i>0.2*home_value])/number_of_simulation*100)
        make_money_n=round(len([i for i in proceeds_n_unison if i>0.2*home_value])/number_of_simulation*100)
    
    median_rtn_w=round(np.median(proceeds_w_unison))
    median_rtn_n=round(np.median(proceeds_n_unison))

    lose_all_w=round(len([i for i in proceeds_w_unison if i<0])/number_of_simulation*100)
    lose_all_n=round(len([i for i in proceeds_n_unison if i<0])/number_of_simulation*100)
    
    lose_part_w=100-lose_all_w-make_money_w
    lose_part_n=100-lose_all_n-make_money_n
    return(median_rtn_w,median_rtn_n,make_money_w,make_money_n,lose_all_w,lose_all_n,lose_part_w,lose_part_n)
    
def wrapper_hb(unison_gives,home_value):
    expected_return=0.035 #per year housing price return
    volatility=0.15 #per year housing price vol

    re_invt_r=0.07 #per year reinvestment return
    re_invt_std=0.14 #per year reinvestment vol
   
    transaction_cost=0.06 #transaction fee to sell house
    tax_rate=0.28 

    #home buyer simulation fixed constants
    pmi_reset=0.8
    unison_mtgg_r=0.0375
    non_unison_mtgg_r=0.0375
    pmi_rate=0.005

    holding_period=7 #years
    hb_pricing_ratio=3.5 #times
    
    np.random.seed(0)
    part1=hb_simulation(unison_gives,home_value,expected_return,volatility,re_invt_r,\
                      re_invt_std,transaction_cost,tax_rate,pmi_reset,unison_mtgg_r,non_unison_mtgg_r,\
                      pmi_rate,holding_period,hb_pricing_ratio)
    
    return(part1)

def hb_simulation(unison_invmt_prct,home_value,expected_return,volatility,re_invt_r,\
                  re_invt_std,transaction_cost,tax_rate,pmi_reset,unison_mtgg_r,non_unison_mtgg_r,\
                  pmi_rate,holding_period,hb_pricing_ratio):
    unison_program="HomeBuyer"
    u_principal=home_value*0.8  #mortgage principal with unison
    share_in_appr=hb_pricing_ratio*unison_invmt_prct
    down_pmt = home_value - u_principal - unison_invmt_prct * home_value
    non_u_principal = home_value - down_pmt
    scope=holding_period+1 #years
    #non-unison mortgage principal, payment and tax break
    non_u_principal_T=np.zeros(scope)
    non_u_mtgg_pmt=Yearly_pmt(non_u_principal,non_unison_mtgg_r,30)
    non_u_tax_break_T=np.zeros(scope)
    #unison mortgage principal, payment and tax break
    u_principal_T=np.zeros(scope)
    u_mtgg_pmt=Yearly_pmt(u_principal,unison_mtgg_r,30)
    u_tax_break_T=np.zeros(scope)
    #pmi 
    pmi_T=np.zeros(scope)
    #generate result within the scope
    # first calculate mortgage related numbers
    residual_cash_no_T=np.zeros(scope)
    for year in range(scope):
        if year==0:
            non_u_principal_T[year]=non_u_principal
            u_principal_T[year]=u_principal
    
        else:
            non_u_principal_T[year]=non_u_principal_T[year-1]*(1+non_unison_mtgg_r)-non_u_mtgg_pmt
            u_principal_T[year]=u_principal_T[year-1]*(1+unison_mtgg_r)-u_mtgg_pmt
    
        non_u_tax_break_T[year]=non_u_principal_T[year]*non_unison_mtgg_r*tax_rate
        u_tax_break_T[year]=u_principal_T[year]*unison_mtgg_r*tax_rate
        if (non_u_principal_T[year]/home_value)>pmi_reset:
            pmi_T[year]=non_u_principal_T[year]*pmi_rate
        else:
            pmi_T[year]=0
        residual_cash_no_T[year]=pmi_T[year]+non_u_mtgg_pmt-u_mtgg_pmt-non_u_tax_break_T[year]+u_tax_break_T[year]

    # monte carlo simulation
    
    number_of_simulation=5000
    oip=home_value*unison_invmt_prct 
    
    mu_term_r=re_invt_r-0.5*re_invt_std**2
    mu_term_hp=expected_return-0.5*volatility**2
    
    #initialize
    hp_random=np.random.normal(0,re_invt_std,number_of_simulation*scope).reshape(scope,number_of_simulation)
    r_random=np.random.normal(0,volatility,number_of_simulation*scope).reshape(scope,number_of_simulation)   
    home_price_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    unison_position_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    reinvt_r_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    residual_cash_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    equity_w_unison_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    equity_n_unison_year=np.zeros(number_of_simulation*scope).reshape(scope,number_of_simulation)
    
    for i in range(scope):
        reinvt_r_year[i]=np.exp(mu_term_r+r_random[i])-1
        if i==0:
            home_price_year[i]=np.ones(number_of_simulation)*home_value
            unison_position_year[i]=np.ones(number_of_simulation)*oip
            residual_cash_year[i]=pmi_T[i]+non_u_mtgg_pmt-u_mtgg_pmt-non_u_tax_break_T[i]+u_tax_break_T[i]
        else:
            home_price_year[i]=np.multiply(home_price_year[i-1],np.exp(mu_term_hp+hp_random[i]))
            unison_position_year[i] = np.maximum(oip+(home_price_year[i]-home_value)*share_in_appr,0)
            residual_cash_year[i] = residual_cash_year[i-1]*(1+reinvt_r_year[i-1])+pmi_T[i]+\
                                      non_u_mtgg_pmt-u_mtgg_pmt-non_u_tax_break_T[i]+u_tax_break_T[i]
        if i==holding_period:
            transaction_shock=transaction_cost*home_price_year[i]
        else:
            transaction_shock=0
            
        equity_w_unison_year[i]=home_price_year[i]-unison_position_year[i]-\
                                        u_principal_T[i]+residual_cash_year[i]-transaction_shock
        equity_n_unison_year[i]=home_price_year[i]-non_u_principal_T[i]-transaction_shock

    proceeds_w_unison = equity_w_unison_year[holding_period]
    proceeds_n_unison = equity_n_unison_year[holding_period]
    [median_rtn_w,median_rtn_n,make_money_w,make_money_n,lose_all_w,lose_all_n,lose_part_w,lose_part_n]=performance_measurement(\
                            unison_program,proceeds_w_unison,proceeds_n_unison,\
                            number_of_simulation,unison_invmt_prct,home_value)
    
    monthly_savings= int(np.median(residual_cash_no_T[:scope])/12)
    part1={'Unison_rtn':int(median_rtn_w),'None_Unison_rtn':int(median_rtn_n),\
          'Unison_win':make_money_w,'None_Unison_win':make_money_n,\
          'Unison_lose_part':lose_part_w,'None_Unison_lose_part':lose_part_n,\
          'Unison_lose_all':lose_all_w,'None_Unison_lose_all':lose_all_n,\
          'Monthly_Savings':monthly_savings,'None_Unison_Mortgage_Principal':int(non_u_principal),\
           'Unison_Mortgage_Principal': int(u_principal)}
  
    
    return(part1)
    
    

def lambda_handler(event, context):
    #event: {"home_value","investment_percentage"}
    try:
       
        return wrapper_hb(unison_gives=float(event["investment_percentage"]),\
                            home_value=float(event["home_value"]))
        
    except Exception as e:
        return dict(meta=dict(
            result='failed',
            error=repr(e),
            message=
            'expecting a dictionary of deal parameters, in JSON key-value formats'
        ))
