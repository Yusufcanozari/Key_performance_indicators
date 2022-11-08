import pandas as pd
import datetime as dt
df_ = pd.read_excel(r"C:\Users\Sony\PycharmProjects\pythonProject1\Datasets\online_retail_II.xlsx",sheet_name="Year 2009-2010")
pd.set_option("display.max_columns",None)
pd.set_option("display.float_format",lambda x: "%.3f" % x)
df = df_.copy()
df.head()
df.isnull().sum()
df.dropna(inplace=True)
df["total_price"] = df["Price"] * df["Quantity"]
df = df[df["Quantity"]>0]
df = df[~df["Invoice"].str.contains("C",na=False)]

cltv_c = df.groupby("Customer ID").agg({"Invoice":lambda x:x.nunique(),
                                        "Quantity":lambda x:x.sum(),
                                        "total_price":lambda x:x.sum()})
cltv_c.columns = ["Transaction","total_unit","total_price"]

#average order value
cltv_c["Average_order_value"] = cltv_c["total_price"] / cltv_c["Transaction"]

#Purchase frequency
cltv_c["Purchase_Frequency"] = cltv_c["Transaction"] / cltv_c.shape[0]

#Repeat,Churn rate
repeat = cltv_c[cltv_c["Transaction"]>1].shape[0] / cltv_c.shape[0]
churn_Rate = 1-repeat

#Proftit Margin
cltv_c["Profit_Margin"] = cltv_c["total_price"] * 0.10

#customers value
cltv_c["cust_val"] = cltv_c["Average_order_value"] * cltv_c["Purchase_Frequency"]

#Customer Lifetime Value
cltv_c["cltv"] = (cltv_c["cust_val"] /churn_Rate) * cltv_c["Profit_Margin"]

cltv_c.sort_values(by="cltv",ascending=False)

cltv_c["segment"] =pd.qcut(cltv_c["cltv"],4,labels=["D","C","B","A"])

cltv_c.groupby("segment").agg(["mean","count","sum"])

df = df[~df["Invoice"].str.contains("C",na=False)]
df =df[df["Quantity"]>0]
df.dropna(inplace =True)
df.describe().T

df["totalprice"] = df["Price"] * df["Quantity"]

cltv= df.groupby('Customer ID').agg({'Invoice': lambda x:x.nunique(),#kaç kere almış
                                        'Quantity': lambda x: x.sum(),#kaç birim almış
                                        'totalprice': lambda x: x.sum()})#ne kadar ödemiş

cltv.columns = ["Total_transaction","total_unit","total_price"]