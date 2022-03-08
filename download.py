#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as plt
import os
import sys
import re
from numpy.core.fromnumeric import var
import requests
import gzip
from io import TextIOWrapper
import pickle
from zipfile import ZipFile
import csv
from bs4 import BeautifulSoup
from requests.api import head

# Kromě vestavěných knihoven (os, sys, re, requests …) byste si měli vystačit s: gzip, pickle, csv, zipfile, numpy, matplotlib, BeautifulSoup.
# Další knihovny je možné použít po schválení opravujícím (např ve fóru WIS).


class DataDownloader:
    """ TODO: dokumentacni retezce 

    Attributes:
        headers    Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!  
        regions     Dictionary s nazvy kraju : nazev csv souboru
    """

    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a","region"]

    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename
        
    def download_data(self):
        # status check
        print("Downloads data")
        req = requests.get("https://ehw.fit.vutbr.cz/izv/", headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},allow_redirects=True)
        
        # gets the html of the page
        result_html = BeautifulSoup(req.text, "html.parser")
        
        # gets the html of all download buttons
        buttons_html = result_html.findAll(class_='btn btn-sm btn-primary')
        
        
        # creates a new folder if folder does not exist
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        # parses for each button, downloads zip file from url and saves it    
        for item in buttons_html:
            url = item.get('onclick')
            url = url[10:][:-2]
            link_to_download = 'https://ehw.fit.vutbr.cz/izv/' + url
            just_zip_name = url.split("/")
            download_request = requests.get(link_to_download, stream=True)
            with open(self.folder + '/' + just_zip_name[1], 'wb') as fd:
                fd.write(download_request.content)

    def parse_region_data(self, region):
        # status check
        print("parsing data " + region)

        # downloads data if not existing
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            self.download_data()

        # checks for wrong region types
        if (region not in self.regions):
            print("REGION DOES NOT EXISTS")
            exit(10)
        
        # gets list of files
        # unzips each file
        # search for region csv file
        # read encoded csv file
        # change of datatypes from str to int if needed
        # adds region type at the end of arr
        result_array = []
        for file in os.listdir(self.folder):
            # excludes any other type then .zip
            if(".pkl.gz" in file):
                continue

            with ZipFile(self.folder + '/' + file,'r') as zipObject:
                with zipObject.open(self.regions[region] + ".csv") as csvFile:
                    dataFile = csv.reader(TextIOWrapper(csvFile,"cp1250"), delimiter = ';')
                    for row in dataFile:
                        text = [None]*65
                        i = 0
                        for data in row:
                            try:
                                #text[i] = int(data) #looses data somehow :]
                                text[i] = data
                            except ValueError:
                                text[i] = data
                            i += 1
                        text[64] = region
                        result_array.append(text)
        
        # transpose arr to have better access to dict keys
        result = np.transpose(result_array)
        i = 0
        var = {}
        # adds to each column ndarray its key from headers
        for row in result:
            var[self.headers[i]] = row
            i += 1
        
        return var

    def get_dict(self, regions=None):
        # status check
        print("Get dictionary")

        # checks for regions
        if(regions is None or regions == []):
            regions = list(self.regions.keys())

        #return dictionary initialization
        self.finish = {}
        for header in self.headers:
            self.finish[header] = np.array([])
        
        # checks for file
        # if file not found throws exception and creates file with data
        # if file exists copies data, appends, returns
        for region in regions:
            # REMAKE TRY CATCH STATEMENT TO OS.PATH.EXIST if I will have enough time...
            # status check
            print(region + " is being processed")

            try:
                with gzip.GzipFile(self.folder + '/' + self.cache_filename.replace("{}", region),'rb') as cache:
                    data = pickle.load(cache)
                    for header in self.headers:
                        self.finish[header] = np.append(self.finish[header], data[header])
                    
                    
            except FileNotFoundError:
                data = self.parse_region_data(region)
                with gzip.GzipFile(self.folder + '/' + self.cache_filename.replace("{}", region),'wb') as cache:
                    pickle.dump(data,cache)
                    for header in self.headers:
                        self.finish[header] = np.append(self.finish[header], data[header])
        return self.finish

if __name__ == '__main__':
    #  základní informace o stažených datech
    data = DataDownloader().get_dict(["KVK", "LBK", "PAK"])
    print("Sloupce:", data.keys())
    i = 0
    for header in data.keys():
        for arr in data[header]: i += len(arr)
    print("Počet záznamů: ", i)
    print("Kraje: KVK, LBK, PAK")
