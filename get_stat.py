#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import argparse

from numpy.core.defchararray import array, rfind
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse
from download import DataDownloader


def plot_stat(data_source, fig_location=None, show_figure=False):
    # status check
    print("Preparing data for graph")

    # initialization of graph all values
    names = ["Přerušovaná žlutá","Semofor mimo provoz","Dopravními značkami","Přenosné dopravní značky","Nevyznačena","Žádná úprava"]
    regions = []
    arrays = []
    values = []
    
    # getting region names
    for region in set(data_source['region']):
        regions.append(region)

    # taking and merging two arrays, so we dont have to work with the entire thing
    arr = np.stack([data_source['p24'],data_source['region']],axis=0)
    
    # splitting by regions
    for region in regions:
        i = 0
        tmp = []
        for key in arr[1]:
            if(arr[1][i] == region):
                tmp.append(arr[0][i])
            i += 1
        arrays.append(tmp)
        
    # getting characteristic values of accidents
    for array in arrays:     
        array = np.array(array)
        var_p24_0 = np.count_nonzero(array == '0')
        var_p24_1 = np.count_nonzero(array == '1')
        var_p24_2 = np.count_nonzero(array == '2')
        var_p24_3 = np.count_nonzero(array == '3')
        var_p24_4 = np.count_nonzero(array == '4')
        var_p24_5 = np.count_nonzero(array == '5')
        values.append([var_p24_1,var_p24_2,var_p24_3,var_p24_4,var_p24_5,var_p24_0])
    values = np.array(values)
    values = np.transpose(values)

    # showing graph
    fig, ax1 = plt.subplots()
    im = ax1.imshow(values)
    ax1.set_xticks(np.arange(len(regions)))
    ax1.set_yticks(np.arange(len(names)))
    ax1.set_xticklabels(regions)
    ax1.set_yticklabels(names)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
    ax1.set_title("Absolutně")
    fig.tight_layout()

    # second graph to be continued
    #plt.legend()
    #im2 = ax1.imshow(values)
    #ax2.set_xticks(np.arange(len(regions)))
    #ax2.set_yticks(np.arange(len(names)))
    #ax2.set_xticklabels(regions)
    #ax2.set_yticklabels(names)
    #plt.setp(ax2.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
    #ax2.set_title("Relative")
    #fig.tight_layout()

    # status check
    print("Showing graph")
    if show_figure is True:
        plt.show()

    if not fig_location is None:
        # status check
        print("Saving graph")
        if not os.path.exists(fig_location):
            os.makedirs(fig_location)
        plt.savefig(fig_location + '/Statistiky_nehodovosti.png')

  
if __name__ == '__main__':
    # init
    fig_location = None
    show_figure = False

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig_location', help='Path to the picture', required=False)
    parser.add_argument('--show_figure', help= 'Show Graph True/False',required=False, action='store_true')
    args = parser.parse_args()
    
    if args.fig_location:
        fig_location = args.fig_location
    if args.show_figure:
        show_figure = True

    data_source = DataDownloader().get_dict()
    plot_stat(data_source,fig_location,show_figure)
