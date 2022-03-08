#!/usr/bin/env python3.9
# coding=utf-8
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import pickle
import gzip

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

""" Ukol 1:
načíst soubor nehod, který byl vytvořen z vašich dat. Neznámé integerové hodnoty byly mapovány na -1.

Úkoly:
- vytvořte sloupec date, který bude ve formátu data (berte v potaz pouze datum, tj sloupec p2a)
- vhodné sloupce zmenšete pomocí kategorických datových typů. Měli byste se dostat po 0.5 GB. Neměňte však na kategorický typ region (špatně by se vám pracovalo s figure-level funkcemi)
- implementujte funkci, která vypíše kompletní (hlubkou) velikost všech sloupců v DataFrame v paměti:
orig_size=X MB
new_size=X MB

Poznámka: zobrazujte na 1 desetinné místo (.1f) a počítejte, že 1 MB = 1e6 B. 
"""

def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:

    # File exists - check
    if( not os.path.isfile(filename) ):
        return 1

    # pickle load to data / making dataframe
    with gzip.open(filename) as f:
        data = pickle.load(f)
        data = pd.DataFrame(data)

        # counts original size of data
        if (verbose):
            print("origin_size={:.1f} MB".format(data.memory_usage(index=False, deep=True).sum() / 1048576))

        # data template
        #["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
        #       "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
        #       "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
        #       "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a","region" ]

        # convert objects to different datatypes
        data['p2a'] = pd.to_datetime(data['p2a'], format='%Y-%m-%d')
        data['date'] = data['p2a']
        data['p1'] = pd.to_numeric(data['p1'])
        data['p36'] = pd.to_numeric(data['p36'])
        data['p37'] = pd.to_numeric(data['p37'])
        data['weekday(p2a)'] = data['weekday(p2a)'].astype('category')
        data['p2b'] = pd.to_numeric(data['p2b'])
        data['p6'] = pd.to_numeric(data['p6'])
        data['p7'] = pd.to_numeric(data['p7'])
        data['p8'] = pd.to_numeric(data['p8'])

        data['p9'] = data['p9'].astype('category')

        data['p10'] = pd.to_numeric(data['p10'])
        data['p11'] = pd.to_numeric(data['p11'])
        data['p12'] = pd.to_numeric(data['p12'])
        data['p13a'] = pd.to_numeric(data['p13a'])
        data['p13b'] = pd.to_numeric(data['p13b'])
        data['p13c'] = pd.to_numeric(data['p13c'])
        data['p14'] = pd.to_numeric(data['p14'])
        data['p15'] = pd.to_numeric(data['p15'])
        data['p16'] = pd.to_numeric(data['p16'])
        data['p17'] = pd.to_numeric(data['p17'])
        data['p18'] = pd.to_numeric(data['p18'])
        data['p19'] = pd.to_numeric(data['p19'])
        data['p20'] = pd.to_numeric(data['p20'])
        data['p21'] = pd.to_numeric(data['p21'])
        data['p22'] = pd.to_numeric(data['p22'])
        data['p23'] = pd.to_numeric(data['p23'])
        data['p24'] = pd.to_numeric(data['p24'])
        data['p27'] = pd.to_numeric(data['p27'])
        data['p28'] = pd.to_numeric(data['p28'])
        data['p34'] = pd.to_numeric(data['p34'])
        data['p35'] = pd.to_numeric(data['p35'])
        data['p39'] = pd.to_numeric(data['p39'])
        data['p44'] = pd.to_numeric(data['p44'])
        data['p45a'] = pd.to_numeric(data['p45a'])
        data['p47'] = pd.to_numeric(data['p47'])
        data['p48a'] = pd.to_numeric(data['p48a'])
        data['p49'] = pd.to_numeric(data['p49'])
        data['p50a'] = pd.to_numeric(data['p50a'])
        data['p50b'] = pd.to_numeric(data['p50b'])
        data['p51'] = pd.to_numeric(data['p51'])
        data['p52'] = pd.to_numeric(data['p52'])
        data['p53'] = pd.to_numeric(data['p53'])
        data['p55a'] = pd.to_numeric(data['p55a'])
        data['p57'] = pd.to_numeric(data['p57'])
        data['p58'] = pd.to_numeric(data['p58'])
        data['a'] = pd.to_numeric(data['a'])
        data['b'] = pd.to_numeric(data['b'])
        data['d'] = pd.to_numeric(data['d'])
        data['e'] = pd.to_numeric(data['e'])
        data['f'] = pd.to_numeric(data['f'])
        data['g'] = pd.to_numeric(data['g'])

        data['h'] = data['h'].astype('category')
        data['i'] = data['i'].astype('category')
        data['j'] = data['j'].astype('category')
        data['k'] = data['k'].astype('category')
        data['l'] = data['l'].astype('category')
        data['n'] = data['n'].astype('category')
        data['o'] = data['o'].astype('category')
        data['p'] = data['p'].astype('category')
        data['q'] = data['q'].astype('category')
        data['r'] = data['r'].astype('category')
        data['s'] = data['s'].astype('category')
        data['t'] = data['t'].astype('category')

        data['p5a'] = pd.to_numeric(data['p5a'])

        # counts new size of data
        if (verbose):
            print("new_size={:.1f} MB".format(data.memory_usage(index=False, deep=True).sum() / 1048576))

    return data

# Ukol 2: počty nehod v jednotlivých regionech podle druhu silnic

 
def plot_roadtype(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):

    # dropping unnecessary columns
    data = df
    data = data.drop(columns=["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p22", "p23", "p24", "p27", "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a", "date"])

    # extracting 4 regions
    data = data.loc[df['region'].isin(["ZLK", "OLK", "LBK", "KVK"])]
    # replacing numbers with identical strings
    data['p21'].replace({0: "Jiná koumunikace", 1: "Dvoupruhová komunikace", 2: "Třípruhová komunikace", 3: "Čtyřpruhová komunikace",
                         4: "Čtyřpruhová komunikace", 5: "Vícepruhová komunikace", 6: "Rychlostní komunikace"}, inplace=True)

    # grouping data into 4 groups
    grouped_data = data[["region", "p21"]].groupby(["region"], as_index=False).sum()


    # extracting data from first region
    region1 = grouped_data.loc[grouped_data['region'].isin(["ZLK"])]
    region1_6 = region1['p21'].str.count("Rychlostní komunikace")
    region1_5 = region1['p21'].str.count("Vícepruhová komunikace")
    region1_4 = region1['p21'].str.count("Čtyřpruhová komunikace")
    region1_3 = region1['p21'].str.count("Třípruhová komunikace")
    region1_2 = region1['p21'].str.count("Dvoupruhová komunikace")
    region1_1 = region1['p21'].str.count("Jiná koumunikace")

    # extracting data from second region
    region2 = grouped_data.loc[grouped_data['region'].isin(["OLK"])]
    region2_6 = region2['p21'].str.count("Rychlostní komunikace")
    region2_5 = region2['p21'].str.count("Vícepruhová komunikace")
    region2_4 = region2['p21'].str.count("Čtyřpruhová komunikace")
    region2_3 = region2['p21'].str.count("Třípruhová komunikace")
    region2_2 = region2['p21'].str.count("Dvoupruhová komunikace")
    region2_1 = region2['p21'].str.count("Jiná koumunikace")

    # extracting data from third region
    region3 = grouped_data.loc[grouped_data['region'].isin(["LBK"])]
    region3_6 = region3['p21'].str.count("Rychlostní komunikace")
    region3_5 = region3['p21'].str.count("Vícepruhová komunikace")
    region3_4 = region3['p21'].str.count("Čtyřpruhová komunikace")
    region3_3 = region3['p21'].str.count("Třípruhová komunikace")
    region3_2 = region3['p21'].str.count("Dvoupruhová komunikace")
    region3_1 = region3['p21'].str.count("Jiná koumunikace")

    # extracting data from fourth region
    region4 = grouped_data.loc[grouped_data['region'].isin(["KVK"])]
    region4_6 = region4['p21'].str.count("Rychlostní komunikace")
    region4_5 = region4['p21'].str.count("Vícepruhová komunikace")
    region4_4 = region4['p21'].str.count("Čtyřpruhová komunikace")
    region4_3 = region4['p21'].str.count("Třípruhová komunikace")
    region4_2 = region4['p21'].str.count("Dvoupruhová komunikace")
    region4_1 = region4['p21'].str.count("Jiná koumunikace")

    # initializing x axis for graphs
    x=["ZLK","OLK","LBK","KVK"]

    # creating figure
    fig,axes = plt.subplots(2,3, figsize=(10,7))
    ax = axes.flatten()

    # graph name
    fig.suptitle("Druhy Silnic",fontsize=20)

    # creating 6 graphs
    sns.barplot(x,y=[region1_2[3],region2_2[2],region3_2[1],region4_2[0]],ax=ax[0])
    ax[0].title.set_text("Dvoupruhová komunikace")
    ax[0].set(ylabel="Počet nehod")
    ax[0].get_xaxis().set_visible(False)
    ax[0].set_facecolor('#EFEFEF')

    sns.barplot(x,y=[region1_1[3],region2_1[2],region3_1[1],region4_1[0]],ax=ax[1])
    ax[1].title.set_text("Jiná koumunikace")
    ax[1].get_xaxis().set_visible(False)
    ax[1].set_facecolor('#EFEFEF')

    sns.barplot(x,y=[region1_3[3],region2_3[2],region3_3[1],region4_3[0]],ax=ax[2])
    ax[2].title.set_text("Třípruhová komunikace")
    ax[2].get_xaxis().set_visible(False)
    ax[2].set_facecolor('#EFEFEF')

    sns.barplot(x,y=[region1_4[3],region2_4[2],region3_4[1],region4_4[0]],ax=ax[3])
    ax[3].set(ylabel="Počet nehod")
    ax[3].title.set_text("Čtyřpruhová komunikace")
    ax[3].set(xlabel="Kraje")
    ax[3].set_facecolor('#EFEFEF')

    sns.barplot(x,y=[region1_5[3],region2_5[2],region3_5[1],region4_5[0]],ax=ax[4])
    ax[4].title.set_text("Vícepruhová komunikace")
    ax[4].set(xlabel="Kraje")
    ax[4].set_facecolor('#EFEFEF')

    sns.barplot(x,y=[region1_6[3],region2_6[2],region3_6[1],region4_6[0]],ax=ax[5])
    ax[5].title.set_text("Rychlostní komunikace")
    ax[5].set(xlabel="Kraje")
    ax[5].set_facecolor('#EFEFEF')

    # graph save to file
    if fig_location is not None:
        directory = os.path.dirname(fig_location)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        plt.savefig(fig_location)

    # show graph
    if show_figure:
        plt.show()

# Ukol3: zavinění zvěří
 
def plot_animals(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):
    data = df

    data = data.drop(columns=["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a"])

    data = data.loc[df['region'].isin(["ZLK", "OLK", "LBK", "KVK"])]
    data['p10'].replace({0: "jiné", 1: "řidičem", 2: "řidičem", 3: "jiné", 4: "zvěří", 5: "jiné", 6: "jiné", 7: "jiné"}, inplace=True)

    # vybrat rok < 2021
    data = data.where(lambda x:x['date'].dt.year < 2021)
    # p58 == 5
    data = data.where(lambda x:x['p58'] == 5)
    # dropping p58, cause we dont need it
    data = data.drop(columns=["p58"])

    # parsing data
    data1 = data.loc[data['region'].isin(["ZLK"])]
    data2 = data.loc[data['region'].isin(["OLK"])]
    data3 = data.loc[data['region'].isin(["LBK"])]
    data4 = data.loc[data['region'].isin(["KVK"])]

    data1 = data1.drop(columns=["region"])
    data2 = data2.drop(columns=["region"])
    data3 = data3.drop(columns=["region"])
    data4 = data4.drop(columns=["region"])

    data1['date'] = data1['date'].dt.month
    data2['date'] = data2['date'].dt.month
    data3['date'] = data3['date'].dt.month
    data4['date'] = data4['date'].dt.month

    data1 = data1[["date", "p10"]].groupby(["date"], as_index=False).sum()
    data2 = data2[["date", "p10"]].groupby(["date"], as_index=False).sum()
    data3 = data3[["date", "p10"]].groupby(["date"], as_index=False).sum()
    data4 = data4[["date", "p10"]].groupby(["date"], as_index=False).sum()

    data1_1 = data1['p10'].str.count("řidičem")
    data1_2 = data1['p10'].str.count("zvěří")
    data1_3 = data1['p10'].str.count("jiné")

    data2_1 = data2['p10'].str.count("řidičem")
    data2_2 = data2['p10'].str.count("zvěří")
    data2_3 = data2['p10'].str.count("jiné")

    data3_1 = data3['p10'].str.count("řidičem")
    data3_2 = data3['p10'].str.count("zvěří")
    data3_3 = data3['p10'].str.count("jiné")

    data4_1 = data4['p10'].str.count("řidičem")
    data4_2 = data4['p10'].str.count("zvěří")
    data4_3 = data4['p10'].str.count("jiné")


    # plotting graph
    ind = np.arange(12)
    ind = ind+1
    width = 0.25

    fig,ax = plt.subplots(2,2,figsize=(10,8))

    ax[0,0].bar(ind,data1_1.values,width,color='r')
    ax[0,0].bar(ind+width,data1_2.values,width,color='g')
    ax[0,0].bar(ind+width+width,data1_3.values,width,color='b')

    ax[0,1].bar(ind,data2_1.values,width,color='r')
    ax[0,1].bar(ind+width,data2_2.values,width,color='g')
    ax[0,1].bar(ind+width+width,data2_3.values,width,color='b')

    ax[1,0].bar(ind,data3_1.values,width,color='r')
    ax[1,0].bar(ind+width,data3_2.values,width,color='g')
    ax[1,0].bar(ind+width+width,data3_3.values,width,color='b')

    ax[1,1].bar(ind,data4_1.values,width,color='r')
    ax[1,1].bar(ind+width,data4_2.values,width,color='g')
    ax[1,1].bar(ind+width+width,data4_3.values,width,color='b')

    ax[0,0].set(ylabel="Počet nehod")
    ax[0,1].set(ylabel="Počet nehod")
    ax[1,0].set(ylabel="Počet nehod")
    ax[1,1].set(ylabel="Počet nehod")

    ax[0,0].set(xlabel="Měsíc")
    ax[0,1].set(xlabel="Měsíc")
    ax[1,0].set(xlabel="Měsíc")
    ax[1,1].set(xlabel="Měsíc")

    ax[0,0].title.set_text("Kraj: ZLK")
    ax[0,1].title.set_text("Kraj: OLK")
    ax[1,0].title.set_text("Kraj: LBK")
    ax[1,1].title.set_text("Kraj: KVK")

    ax[0,0].set_facecolor('#EFEFEF')
    ax[0,1].set_facecolor('#EFEFEF')
    ax[1,0].set_facecolor('#EFEFEF')
    ax[1,1].set_facecolor('#EFEFEF')

    fig.legend(("řidičem","zvěří","jiné"))
    fig.tight_layout()

    #graph save to file
    if fig_location is not None:
        directory = os.path.dirname(fig_location)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    plt.savefig(fig_location)

    #show graph
    if show_figure:
        plt.show()

# Ukol 4: Povětrnostní podmínky
 
def plot_conditions(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):
    # copying and dropping unecessary cols
    data = df
    data = data.drop(columns=["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a"])

    # parsing regions
    data = data.loc[df['region'].isin(["ZLK", "OLK", "LBK", "KVK"])]
    data['p18'].replace({0: 0, 1: "neztížené", 2: "mlha", 3: "počátek", 4: "déšť", 5: "sněžení", 6: "náledí", 7: "vítr"}, inplace=True)

    # vybrat rok < 2021
    data = data.where(lambda x:x['date'].dt.year < 2021)
    # p18 != 0 (jine)
    data = data.where(lambda x:x['p18'] != 0)

    # parsing data
    data1 = data.loc[data['region'].isin(["ZLK"])]
    data2 = data.loc[data['region'].isin(["OLK"])]
    data3 = data.loc[data['region'].isin(["LBK"])]
    data4 = data.loc[data['region'].isin(["KVK"])]

    data1 = data1.drop(columns=["region"])
    data2 = data2.drop(columns=["region"])
    data3 = data3.drop(columns=["region"])
    data4 = data4.drop(columns=["region"])

    data1 = data1[["date", "p18"]].groupby(["date"], as_index=False).sum()
    data2 = data2[["date", "p18"]].groupby(["date"], as_index=False).sum()
    data3 = data3[["date", "p18"]].groupby(["date"], as_index=False).sum()
    data4 = data4[["date", "p18"]].groupby(["date"], as_index=False).sum()

    date1 = data1['date']
    date2 = data2['date']
    date3 = data3['date']
    date4 = data4['date']

    data1_1 = data1['p18'].str.count("neztížené")
    data1_2 = data1['p18'].str.count("mlha")
    data1_3 = data1['p18'].str.count("počátek")
    data1_4 = data1['p18'].str.count("déšť")
    data1_5 = data1['p18'].str.count("sněžení")
    data1_6 = data1['p18'].str.count("náledí")
    data1_7 = data1['p18'].str.count("vítr")

    data2_1 = data2['p18'].str.count("neztížené")
    data2_2 = data2['p18'].str.count("mlha")
    data2_3 = data2['p18'].str.count("počátek")
    data2_4 = data2['p18'].str.count("déšť")
    data2_5 = data2['p18'].str.count("sněžení")
    data2_6 = data2['p18'].str.count("náledí")
    data2_7 = data2['p18'].str.count("vítr")

    data3_1 = data3['p18'].str.count("neztížené")
    data3_2 = data3['p18'].str.count("mlha")
    data3_3 = data3['p18'].str.count("počátek")
    data3_4 = data3['p18'].str.count("déšť")
    data3_5 = data3['p18'].str.count("sněžení")
    data3_6 = data3['p18'].str.count("náledí")
    data3_7 = data3['p18'].str.count("vítr")

    data4_1 = data4['p18'].str.count("neztížené")
    data4_2 = data4['p18'].str.count("mlha")
    data4_3 = data4['p18'].str.count("počátek")
    data4_4 = data4['p18'].str.count("déšť")
    data4_5 = data4['p18'].str.count("sněžení")
    data4_6 = data4['p18'].str.count("náledí")
    data4_7 = data4['p18'].str.count("vítr")


    a = pd.DataFrame({'date': date1, 'neztížené': data1_1, 'mlha': data1_2, 'počátek': data1_3, 'déšť': data1_4, 'sněžení': data1_5, 'náledí': data1_6, 'vítr': data1_7})
    b = pd.DataFrame({'date': date2, 'neztížené': data2_1, 'mlha': data2_2, 'počátek': data2_3, 'déšť': data2_4, 'sněžení': data2_5, 'náledí': data2_6, 'vítr': data2_7})
    c = pd.DataFrame({'date': date3, 'neztížené': data3_1, 'mlha': data3_2, 'počátek': data3_3, 'déšť': data3_4, 'sněžení': data3_5, 'náledí': data3_6, 'vítr': data3_7})
    d = pd.DataFrame({'date': date4, 'neztížené': data4_1, 'mlha': data4_2, 'počátek': data4_3, 'déšť': data4_4, 'sněžení': data4_5, 'náledí': data4_6, 'vítr': data4_7})

    a = a.groupby(pd.PeriodIndex(a['date'], freq="M"))['neztížené','mlha','počátek','déšť','sněžení','náledí','vítr'].mean().reset_index()
    b = b.groupby(pd.PeriodIndex(b['date'], freq="M"))['neztížené','mlha','počátek','déšť','sněžení','náledí','vítr'].mean().reset_index()
    c = c.groupby(pd.PeriodIndex(c['date'], freq="M"))['neztížené','mlha','počátek','déšť','sněžení','náledí','vítr'].mean().reset_index()
    d = d.groupby(pd.PeriodIndex(d['date'], freq="M"))['neztížené','mlha','počátek','déšť','sněžení','náledí','vítr'].mean().reset_index()

    # plotting graph
    fig,axes = plt.subplots(2,2,figsize=(10,8))

    a.plot(x="date",ax=axes[0,0],legend=None,ylabel="Počet nehod",title="Kraj: ZLK").set(xlabel=None)
    b.plot(x="date",ax=axes[0,1],title="Kraj: OLK").set(xlabel=None)
    c.plot(x="date",ax=axes[1,0],legend=None,ylabel="Počet nehod",title="Kraj: LBK").set(xlabel=None)
    d.plot(x="date",ax=axes[1,1],legend=None,title="Kraj: KLK").set(xlabel=None)

    fig.tight_layout()

    #graph save to file
    if fig_location is not None:
        directory = os.path.dirname(fig_location)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    plt.savefig(fig_location)

    #show graph
    if show_figure:
        plt.show()

 
if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz") # tento soubor si stahnete sami, při testování pro hodnocení bude existovat
    plot_roadtype(df, fig_location="01_roadtype.png", show_figure=True)
    plot_animals(df, "02_animals.png", True)
    plot_conditions(df, "03_conditions.png", True)
