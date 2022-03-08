from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import os
import pickle
import gzip

def get_dataframe(filename: str):

    if( not os.path.isfile(filename) ):
        exit(-1)
        
    with gzip.open(filename) as f:
        data = pickle.load(f)
        data = pd.DataFrame(data)

    return data


def generate_graph(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):

    # alternating data
    dff = df[['p1', 'p55a', 'p57', 'region']].copy()

    dff['p57'] = dff['p57'].replace(
        {-1: 'záznam neexistuje',
         0: 'jiný nepříznivý stav',
         1: 'dobrý',
         2: 'unaven, usnul',
         3: 'pod vlivem narkotik',
         4: 'vliv alkoholu do 1‰',
         5: 'vliv alkoholu od 1‰',
         6: 'nemoc, úraz',
         7: 'invalida',
         8: 'řidič zemřel při jízdě',
         9: 'sebevražda'})

    # only truck drivers
    region_ZLK = dff[(dff["region"] == "ZLK") & (dff["p55a"] == 3)]
    region_JHM = dff[(dff["region"] == "JHM") & (dff["p55a"] == 3)]
    dff = dff[(dff["p55a"] == 3)]

    data_ALL = (dff.groupby(['region']).agg({'p57': 'count'}).reset_index())
    data_ZLK = (region_ZLK.groupby(['p57']).agg({'region': 'count'}).reset_index())
    data_JHM = (region_JHM.groupby(['p57']).agg({'region': 'count'}).reset_index())

    data = [data_ALL, data_JHM, data_ZLK]
    titles = ["Celkový počet nehod řidičů kamionů v ČR", "Stav řidičů kamionů v JHM", "Stav řidičů kamionů v ZLK"]
    ylabels = ["Kraje", "", ""]
    xscales = ["linear", "log", "log"]
    xxes = ['p57','region','region']
    yyes = ['region','p57','p57']

    # plot graph
    sns.set_theme(style="darkgrid")
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 8.27))
    for i in range(3):
        axes[i].set(xscale=xscales[i])
        axes[i].set_title(titles[i])
        sns.barplot(ax=axes[i],
                        data=data[i],
                        x=xxes[i],
                        y=yyes[i],
                        saturation=1)
        axes[i].set(ylabel=ylabels[i], xlabel='Počet nehod')
        axes[i].spines['bottom'].set_color('black')
        axes[i].spines['left'].set_color('black')
    plt.tight_layout()

    # save | show fig
    if fig_location:
        (dirname, filename) = os.path.split(fig_location)
        # create folder if doesnt exist
        if dirname:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

def generate_table(df: pd.DataFrame):
    dff = df[['p1', 'p55a', 'p57', 'region']].copy()

    dff['p57'] = dff['p57'].replace(
        {-1: 'záznam neexistuje',
         0: 'jiný nepříznivý stav',
         1: 'dobrý',
         2: 'unaven, usnul',
         3: 'pod vlivem narkotik',
         4: 'vliv alkoholu do 1‰',
         5: 'vliv alkoholu od 1‰',
         6: 'nemoc, úraz',
         7: 'invalida',
         8: 'řidič zemřel při jízdě',
         9: 'sebevražda'})

    # only truck drivers
    region_ZLK = dff[(dff["region"] == "ZLK") & (dff["p55a"] == 3)]
    region_JHM = dff[(dff["region"] == "JHM") & (dff["p55a"] == 3)]
    dff = dff[(dff["p55a"] == 3)]

    data_ALL = (dff.groupby('region').agg({'p57': 'count'}).reset_index())
    data_ZLK = (region_ZLK.groupby('p57').agg({'region': 'count'}).reset_index())
    data_JHM = (region_JHM.groupby('p57').agg({'region': 'count'}).reset_index())

    data = [data_ALL, data_ZLK, data_JHM]
    title = ["Tabulka celá ČR", "Tabulka ZLK", "Tabulka JHM"]
    names = ["region\tcount","state\tcount","state\tcount"]

    # print table
    for i in range(3):
        print(title[i])
        print(names[i])
        for row in data[i].values:
            for item in row:
                print(item, end="\t")
            print()
        print()

def generate_values():
    print("Usnutí za volantem ZLK vs JHM: JHM 2x častěji")
    print("Jízda pod vlivem alkoholu ZLK vs JHM: JHM 1.6x častěji")
    print("Počet srážek neovlivněných stavem řidiče v ZLK: 4293")
    print("Počet srážek neovlivněných stavem řidiče v JHM 6171")
    print("Počet srážek neovlivněných stavem řidiče celkově: 97952")


if __name__ == "__main__":
    df = get_dataframe("accidents.pkl.gz")
    generate_graph(df,"fig.png",False)
    generate_table(df)
    generate_values()
