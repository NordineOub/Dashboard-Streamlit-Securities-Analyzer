import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
import timeit
import sys
import time
import streamlit as st
import streamlit.components.v1 as components
from functools import wraps
import sweetviz as sv
import pydeck as pdk


@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def importData(wt): 
    
    val= pd.read_csv(wt)
    return val.sample(500000)

def selectdate():
    add_selectbox = st.sidebar.radio(
    "Année :",
    ("2020", "2019", "2018","2017","2016")  
)
    if (add_selectbox== "2020"):
        df =importData("https://jtellier.fr/DataViz/full_2020.csv")
    elif(add_selectbox== "2019"):
        df =importData("https://jtellier.fr/DataViz/full_2019.csv")
    elif(add_selectbox== "2018"):
        df =importData("https://jtellier.fr/DataViz/full_2018.csv")
    elif(add_selectbox== "2017"):
        df =importData("https://jtellier.fr/DataViz/full_2017.csv")
    elif(add_selectbox== "2016"):
        df =importData("https://jtellier.fr/DataViz/full_2016.csv")
    return df
def dept_select(df):
    # Get names of indexes for which column Stock has value No
    indexNames = df[~df['code_departement'].isin(['2A','2B'])]
# Delete these row indexes from dataFrame
    dfdept = sorted(indexNames['code_departement'].astype("string"))
    tjr_selectbox = st.sidebar.selectbox("Département", pd.unique(dfdept))
    dfdept = df[df['code_departement'] == int(tjr_selectbox)]
    return int(tjr_selectbox), dfdept


def PlotDataset(rt):
    st.write("Description du dataset :")
    st.write(rt.describe())
    st.write("Taille du dataset :")
    st.write(rt.shape)
    st.write("Nombres de variables :")
    st.write(rt.columns)
    st.write("Présentation de quelques lignes de dataset")
    st.write(rt.head(5))

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def FirstTrans(df):
    df["date_mutation"]= pd.to_datetime(df["date_mutation"])
    df = df.sort_values(by=['nom_commune'])
    return df

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def FiltrateH(fg):
    values = fg['nom_commune'].drop_duplicates()
    return values

def Piechart(fg):


    piechart = plt.pie(fg.value_counts(), labels=fg.drop_duplicates(),autopct='%1.1f%%',
        shadow=True, startangle=180, rotatelabels = True, labeldistance = 1.5)

    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

def Chart(fg):
    st.bar_chart(fg)

def PlotCode(fg,values):
    place_to_filter = st.sidebar.selectbox('Choisir ville', values)
    st.header('Outil de visualisation des transactions en fonction des villes')
    st.subheader(f'Transactions de chaque terrain à {place_to_filter}')
    st.write(fg[fg['nom_commune'] == place_to_filter].loc[:, df.columns.intersection(['nature_mutation','valeur_fonciere','adresse_numero','adresse_nom_voie','type_local'])])
    st.caption("Ci-dessus l'ensemble des transactions dans la ville choisie dans la sidebar")
    return place_to_filter

def Scatter(sd,dr):
    plt.scatter(sd,dr)

    
    plt.title('Prix du terrain en fonction de la surface carré')
    plt.xlabel('Surface carré du premier lot (en m^2')
    plt.ylabel('Prix du terrain (en k€')
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
def SnsPlot(variable):
    plt.figure(figsize=(10,5))
    cmap =sns.color_palette("Paired")

    chart = sns.countplot(variable,x= 'Type de Local', palette =sns.dark_palette("#69d", reverse=True), orient = 'v', dodge =True)
    
    chart.set_xticklabels(    
    chart.get_xticklabels(), 
    rotation=10, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='x-large')
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write(variable.value_counts())

def colorizeScatter(br,bt):   
    plt.hist(br, bins = 100, range = (-74.1, -73.9), color = 'b', alpha = 0.5, label = 'Longitude')
    plt.legend(loc = 'best')
    plt.twiny()
    plt.hist(bt, bins = 100, range = (40.5, 41), color = 'r', label = 'Latitude')
    plt.legend(loc = 'upper left')
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)
def Distplot(fg):
    fig = ff.create_distplot(
    fg, ('lot1_surface_carrez','lot2_surface_carrez','lot3_surface_carrez','lot4_surface_carrez','lot5_surface_carrez'), bin_size=[.1, .25, .5])
    st.plotly_chart(fig, use_container_width=True)

def get_points_by_months(rg,dp):

    points = rg[["valeur_fonciere","latitude","longitude","code_departement"]]#.sample(n=1000, random_state=1)
    points = points.loc[lambda points : points["code_departement"] == dp]
    return points[~(points.latitude.isna() & points.longitude.isna())][["latitude","longitude"]]

def CalculateMean(rg):
    rg['lot_total'] = rg.loc[:, rg.columns.intersection(['lot1_surface_carrez','lot2_surface_carrez','lot3_surface_carrez','lot4_surface_carrez','lot5_surface_carrez'])].astype(int).sum()
    rg['val_total'] = rg['valeur_fonciere'].sum()
    st.write(rg[['lot_total','valeur_fonciere']].mean())

def Showmap(rg,dp):
    st.subheader("Ici vous pouvez voir le nombre de transactions en fonction du département")
    points = get_points_by_months(rg,dp)
    st.write(f"{len(points)} transactions dans le département du {dp}")
    st.map(points)
    st.caption(' Vous pouvez choisir le département via la sidebar ci-contre')


st.title ('Demandes de Valeurs foncières de 2020 à 2016')
st.header ('Dashboard Lab4 par Nour-Eddine OUBENAMI')

df=selectdate()


df1 = FirstTrans(df)
PlotDataset(df1)

departement ,dfdept= dept_select(df1)

Showmap(df1,departement)
values = FiltrateH(df1)
#st.write(df1.isnull())  Permet de voir lequel est nul (ça s'affiche sous forme de booléen)
ville =PlotCode(df1,values)
SnsPlot(dfdept['type_local'])
SnsPlot(dfdept['nature_mutation'])
Piechart(dfdept.nature_mutation)
CalculateMean(df1[df1['nom_commune'] == ville].notnull())



st.subheader('Analyse du Dataset Général')
Piechart(df1.nature_mutation)

Scatter(df1['lot1_surface_carrez'],df1['valeur_fonciere'])
SnsPlot(df1['type_local'])
SnsPlot(df1['nature_mutation'])
Scatter(df1.latitude,df.longitude)
Chart(df1[['lot1_surface_carrez','lot2_surface_carrez','lot3_surface_carrez','lot4_surface_carrez','lot5_surface_carrez']].sample(n=1000, random_state=1))


#plt.hist(df[['valeur_fonciere','surface_terrain']])
#st.pyplot()


#st.map(df.drop(df.columns.difference(['latitude','longitude']), 1, inplace=True), zoom =8,use_container_width=True)




#colorizeScatter(df.latitude,df.longitude)
#distance = df['latitude','longitude']
#st.map(distance)
