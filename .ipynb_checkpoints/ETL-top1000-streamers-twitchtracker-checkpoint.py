#!/usr/bin/env python
# coding: utf-8

# Instalacion de librerias
#!pip install BeautifulSoup
get_ipython().system('pip install -U selenium')
get_ipython().system('pip3 install -U webdriver-manager')
get_ipython().system('pip install pandas')

## LIBRERIAS

# Generales
import time
import requests
import urllib.request
import csv
from datetime import datetime

## Gestion de datos
import pandas as pd

## Automatizacion
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium

# Webdriver conf
driver = webdriver.Chrome()
opts = webdriver.ChromeOptions()
opts.add_argument('--headless')
driver = webdriver.Chrome(options=opts)
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)

# Tupla de guardado de datos
data_results=[]

# Funcion extraccion de datos del TOP1000 de Twitchtracker
def extrac_top1000():
    numerador_pagina = 0
    url = 'https://twitchtracker.com/channels/ranking?page='
    #driver.get(url)
    
    #El numero de range(XX) marca el numerador final de la pagina 20 serian el Top1000
    for i in range(20):
        
        numerador_pagina = int(numerador_pagina) + 1
        url_pagina = url + str(numerador_pagina)
        driver.get(url_pagina)
        
        # Numero posicion del Stramer
        #numero = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[1]')
        # URL de imagen circular del Streamer
        #imagen = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[2]')
        # Nombre del Streamer
        nombres_streamer = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[3]')
        # Promedio de viewer
        avg_viewers = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[4]')
        # Tiempo Streameado
        time_streamed = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[5]')
        # Espectadores de todos los tiempos
        all_time_peak_viewers = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[6]')
        # Horas vistas
        hours_watched = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[7]')
        # Posicion en el anking
        rank = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[8]')
        # Seguidores ganados
        followers_gained = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[9]')
        # Total de seguidores
        total_followers = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[10]')
        # Total de viewers
        total_views = driver.find_elements(By.XPATH, '//*[@id="channels"]/tbody/tr/td[11]')
        # Raw information
        #raw_data = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/table/tbody/tr')

        for item in range(len(rank)):
            temporal_data={
                            #'Numero': numero[item].text,
                            #'URL imagen Streamer': imagen[item].get_attribute('innerHTML'),
                            'Nombres Streamers': nombres_streamer[item].text,
                            'AVG viewers': avg_viewers[item].text,
                            'Time Streamed (hours)': time_streamed[item].text,
                            'All time peak viewers': all_time_peak_viewers[item].text,
                            'Hours watched': hours_watched[item].text,
                            'Rank': rank[item].text,
                            'Followers gained': followers_gained[item].text,
                            'Total followers': total_followers[item].text,
                            'Total views': total_views[item].text,
                            #'Raw data': raw_data[item].text,
                            }
            data_results.append(temporal_data)
    
extrac_top1000()

# Mostramos datos del TOP50 de Twitchtracker
df_data = pd.DataFrame(data_results)

## T-ransform

# Eliminar el \nhours
df_data = df_data.replace(to_replace='\nhours', value='', regex=True)

# Trasformar datos de K y M 

# K
df_data['Hours watched'] = df_data['Hours watched'].replace(to_replace='K', value='000', regex=True)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='K', value='000', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace='K', value='000', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace='K', value='000', regex=True)
# M 
#df_data['Hours watched'] = df_data['Followers gained'].replace(to_replace='K', value='000', regex=True)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='M', value='000000', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace='M', value='000000', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace='M', value='000000', regex=True)
df_data['Hours watched'] = df_data['Hours watched'].replace(to_replace='M', value='000000', regex=True)

# . K
#df_data['Hours watched'] = df_data['Followers gained'].replace(to_replace='K', value='000', regex=True)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='\..*K', value='00', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace='\..*K', value='00', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace='\..*K', value='00', regex=True)

# . M 
#df_data['Hours watched'] = df_data['Followers gained'].replace(to_replace='K', value='000', regex=True)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='\..*M', value='00000', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace='\..*M', value='00000', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace='\..*M', value='00000', regex=True)

#Eliminar ,
df_data['AVG viewers'] = df_data['AVG viewers'].replace(to_replace=',', value='', regex=True)
df_data['All time peak viewers'] = df_data['All time peak viewers'].replace(to_replace=',', value='', regex=True)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace=',', value='', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace=',', value='', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace=',', value='', regex=True)
df_data['Rank'] = df_data['Rank'].replace(to_replace=',', value='', regex=True)

# Eliminar .
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='\.', value='', regex=True)
df_data['Total followers'] = df_data['Total followers'].replace(to_replace='\.', value='', regex=True)
df_data['Total views'] = df_data['Total views'].replace(to_replace='\.', value='', regex=True)
df_data['Hours watched'] = df_data['Hours watched'].replace(to_replace='\.', value='', regex=True)

#Eliminar el simbolo Positivo (+)
df_data['Followers gained'] = df_data['Followers gained'].replace(to_replace='\+', value='', regex=True)
df_data['Hours watched'] = df_data['Hours watched'].replace(to_replace='\+', value='', regex=True)

## L-oad

#Exportacion a CSV
now = datetime.now()
datos_top1000_streamers = 'datos_top1000_streamers' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
df_data.to_csv(f'/root/staging_data/{datos_top1000_streamers}.csv', index=False ,encoding='utf-8')