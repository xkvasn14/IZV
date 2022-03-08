#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
import os
# muzete pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    # konvertovani pd.DataFrame do geopandas.GeoDataFrame
    return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514")

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """ Vykresleni grafu s sesti podgrafy podle lokality nehody 
     (dalnice vs prvni trida) pro roky 2018-2020 """
    gdf_new = gdf[gdf["region"] == "JHM"]
    gdf_new = gdf_new.to_crs("EPSG:3857")
    gdf_new['p2a'] = pd.to_datetime(gdf_new['p2a'],yearfirst=True)

    colors = [["red","green"],["red","green"],["red","green"]]
    titles = [["JHM kraj: dálnice 2018","JHM kraj: silnice první třídy 2018"],["JHM kraj: dálnice 2019","JHM kraj: silnice první třídy 2019"],["JHM kraj: dálnice 2020","JHM kraj: silnice první třídy 2020"]]
    years = [[2018,2018],[2019,2019],[2020,2020]]
    roads = [[0,1],[0,1],[0,1]]

    fig, ax = plt.subplots(3,2,figsize=(10,12))
    for i in range(3):
        for j in range(2):
            ax[i][j] = gdf_new[(gdf_new['p2a'].dt.year == years[i][j]) & (gdf_new["p36"] == roads[i][j])].plot(ax=ax[i][j],markersize=3,color=colors[i][j],alpha=0.8)
            ax[i][j].axis("off")
            ax[i][j].set_title(titles[i][j])
            ctx.add_basemap(ax[i][j], crs=gdf_new.crs.to_string(), source=ctx.providers.Stamen.TonerLite)
            ax[i][j].set_aspect("auto")
    plt.tight_layout()

    if fig_location:
        (dirname, filename) = os.path.split(fig_location)
        if dirname:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """

    gdf = gdf[(gdf["region"] == "JHM")]
    gdf["p2a"] = pd.to_datetime(gdf["p2a"],yearfirst=True)
    gdf = gdf[gdf["p36"] == 1]
    gdf = gdf.set_geometry(gdf.centroid).to_crs(epsg=3857)
    gdf = gdf[~gdf.geometry.is_empty]

    coords = np.dstack([gdf.geometry.x,gdf.geometry.y]).reshape(-1,2)

    db = sklearn.cluster.MiniBatchKMeans(n_clusters=30).fit(coords)

    gdf4 = gdf.copy()
    gdf4["cluster"] = db.labels_
    gdf4 = gdf4.dissolve(by="cluster", aggfunc={"p1":"count"})

    gdf_coords = geopandas.GeoDataFrame(geometry=geopandas.points_from_xy(db.cluster_centers_[:, 0], db.cluster_centers_[:, 1]))
    gdf5 = gdf4.merge(gdf_coords, left_on="cluster", right_index=True).set_geometry("geometry_x")


    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    ax.axis("off")
    ax.set_title("JHM kraj: silnice první třídy")


    gdf5.plot(ax=ax, markersize=1 , column="p1", legend=True,legend_kwds={'orientation': "horizontal", 'shrink' : 0.6})
    ctx.add_basemap(ax, crs="epsg:3857", source=ctx.providers.Stamen.TonerLite, zoom=10)


    if fig_location:
        (dirname, filename) = os.path.split(fig_location)
        if dirname:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        plt.savefig(fig_location)
    if show_figure:
        plt.show()

if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", False)
    plot_cluster(gdf, "geo2.png", False)
