
"""This is an example of of how I am constructing my ORMS from various Financial Data Sources
"""
import json
import enum


import sys

from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, DateTime, Boolean, ARRAY, DATE, FLOAT, Enum, TIME
from sqlalchemy import select, insert, within_group
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()
Base = declarative_base()

class Denominations(enum.Enum):
    k = 1
    m = 2
    b = 3


class ReportingTypes(enum.Enum):
    quarterlyReports = 1
    annualReports = 2

class RealGDP(Base):
    """Grabbed from FRED and from ALPHA_VANTAGE"""
    __tablename__ = "real_gdp"
    id = Column(Integer, primary_key=True)
    date = Column(DATE)
    currency = Column(String(3))
    value = Column(FLOAT)
    unit = Column(Enum(Denominations))
    interval = Column(String(1))

class Treasury_Yield(Base):
    __tablename__ = "sov_yc"
    id = Column(Integer, primary_key=True)
    maturity = Column(String(10))
    date = Column(DATE)
    rate = Column(FLOAT)
    currency = Column(String(3))

class Income_Statement(Base):
    __tablename__ = "income_statements"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(35), ForeignKey('stock_symbol_mapping.symbol'))
    reporting_type = Column(Enum(ReportingTypes))
    reporting_denominations = Column(Enum(Denominations))
    fiscalDateEnding = Column(DATE) 
    reportedCurrency = Column(String(3))
    grossProfit = Column(FLOAT) 
    totalRevenue = Column(FLOAT)
    costOfRevenue = Column(FLOAT)
    costofGoodsAndServicesSold = Column(FLOAT)
    operatingIncome = Column(FLOAT) 
    sellingGeneralAndAdministrative = Column(FLOAT)
    researchAndDevelopment = Column(FLOAT)
    operatingExpenses = Column(FLOAT)
    investmentIncomeNet = Column(FLOAT)
    netInterestIncome = Column(FLOAT)
    interestIncome = Column(FLOAT)
    interestExpense = Column(FLOAT)
    nonInterestIncome = Column(FLOAT)
    otherNonOperatingIncome = Column(FLOAT)
    depreciation = Column(FLOAT)
    depreciationAndAmortization = Column(FLOAT)
    incomeBeforeTax = Column(FLOAT)
    incomeTaxExpense = Column(FLOAT)
    interestAndDebtExpense = Column(FLOAT)
    netIncomeFromContinuingOperations = Column(FLOAT)
    comprehensiveIncomeNetOfTax = Column(FLOAT)
    ebit = Column(FLOAT)
    ebitda = Column(FLOAT)
    netIncome = Column(FLOAT)

class Balance_Sheet(Base):
    __tablename__ = "balance_sheet"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(35), ForeignKey('stock_symbol_mapping.symbol'))
    reporting_type = Column(Enum(ReportingTypes))
    reporting_denominations = Column(Enum(Denominations))
    fiscalDateEnding = Column(DATE)
    totalAssets = Column(FLOAT) 
    totalCurrentAssets =  Column(FLOAT)
    cashAndCashEquivalentsAtCarryingValue = Column(FLOAT)
    cashAndShortTermInvestments = Column(FLOAT)
    inventory = Column(FLOAT)
    currentNetReceivables = Column(FLOAT) 
    totalNonCurrentAssets = Column(FLOAT)
    propertyPlantEquipment = Column(FLOAT) 
    accumulatedDepreciationAmortizationPPE = Column(FLOAT) 
    intangibleAssets = Column(FLOAT) 
    intangibleAssetsExcludingGoodwill = Column(FLOAT) 
    goodwill = Column(FLOAT) 
    investments = Column(FLOAT) 
    longTermInvestments = Column(FLOAT) 
    shortTermInvestments = Column(FLOAT) 
    otherCurrentAssets = Column(FLOAT)
    otherNonCurrrentAssets = Column(FLOAT) 
    totalLiabilities = Column(FLOAT) 
    totalCurrentLiabilities = Column(FLOAT) 
    currentAccountsPayable = Column(FLOAT) 
    deferredRevenue = Column(FLOAT) 
    currentDebt = Column(FLOAT) 
    shortTermDebt = Column(FLOAT) 
    totalNonCurrentLiabilities = Column(FLOAT) 
    capitalLeaseObligations = Column(FLOAT) 
    longTermDebt = Column(FLOAT) 
    currentLongTermDebt = Column(FLOAT) 
    longTermDebtNoncurrent = Column(FLOAT) 
    shortLongTermDebtTotal = Column(FLOAT) 
    otherCurrentLiabilities = Column(FLOAT) 
    otherNonCurrentLiabilities = Column(FLOAT) 
    totalShareholderEquity = Column(FLOAT) 
    treasuryStock = Column(FLOAT) 
    retainedEarnings = Column(FLOAT) 
    commonStock = Column(FLOAT) 
    commonStockSharesOutstanding = Column(FLOAT) 

class CashFlow(Base):
    __tablename__ = "cashflow"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(35), ForeignKey('stock_symbol_mapping.symbol'))
    reporting_type = Column(Enum(ReportingTypes))
    reporting_denominations = Column(Enum(Denominations))
    fiscalDateEnding = Column(DATE)
    operatingCashflow = Column(FLOAT) 
    paymentsForOperatingActivities = Column(FLOAT) 
    proceedsFromOperatingActivities = Column(FLOAT) 
    changeInOperatingLiabilities = Column(FLOAT) 
    changeInOperatingAssets = Column(FLOAT) 
    depreciationDepletionAndAmortization = Column(FLOAT) 
    capitalExpenditures = Column(FLOAT) 
    changeInReceivables = Column(FLOAT) 
    changeInInventory = Column(FLOAT) 
    profitLoss = Column(FLOAT) 
    cashflowFromInvestment = Column(FLOAT) 
    cashflowFromFinancing = Column(FLOAT) 
    proceedsFromRepaymentsOfShortTermDebt = Column(FLOAT) 
    paymentsForRepurchaseOfCommonStock = Column(FLOAT) 
    paymentsForRepurchaseOfEquity = Column(FLOAT) 
    paymentsForRepurchaseOfPreferredStock = Column(FLOAT) 
    dividendPayout = Column(FLOAT) 
    dividendPayoutCommonStock = Column(FLOAT) 
    dividendPayoutPreferredStock = Column(FLOAT) 
    proceedsFromIssuanceOfCommonStock = Column(FLOAT) 
    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = Column(FLOAT) 
    proceedsFromIssuanceOfPreferredStock = Column(FLOAT) 
    proceedsFromRepurchaseOfEquity = Column(FLOAT) 
    proceedsFromSaleOfTreasuryStock = Column(FLOAT) 
    changeInCashAndCashEquivalents = Column(FLOAT) 
    changeInExchangeRate = Column(FLOAT) 
    netIncome = Column(FLOAT) 


class Stock_Meta(Base):
    __tablename__ = "stock_meta"
    symbol = Column(String(35), primary_key=True)
    assetSubType = Column(String(50))
    companyFullName = Column(String(255))
    cik = Column(Integer)
    exchange = Column(String(30))
    currency = Column(String(3))
    country = Column(String(3))
    sector = Column(String(50))
    industry = Column(String(150))
    address = Column(String(150))
    fiscalYearEnd = Column(String(30))

class Earnings(Base):
    __tablename__ = "earnings"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(35), ForeignKey('stock_symbol_mapping.symbol'))
    reporting_type = Column(Enum(ReportingTypes))
    reporting_denominations = Column(Enum(Denominations))
    fiscalDateEnding = Column(DATE)
    reportedDate = Column(FLOAT)
    reportedEPS = Column(FLOAT)
    estimatedEPS = Column(FLOAT) 
    annualEPS = Column(FLOAT)
    surprise = Column(FLOAT)
    surprisePercentage = Column(FLOAT)  

class Stock_Mapper(Base):
    __tablename__ = "stock_symbol_mapping"
    symbol = Column(String(35), primary_key=True)
    company_name = Column(String(100))
    region = Column(String(30))
    currency = Column(String(3))
    asset_type = Column(String(25))
    marketOpen = Column(TIME)
    marketClose = Column(TIME)
    timezone = Column(String(10))