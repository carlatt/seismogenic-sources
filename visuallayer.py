# -*- coding: utf-8 -*-
"""
Created on Fri May  4 22:20:24 2018

@author: cleme
"""

from osgeo import ogr                    #import ogr
import matplotlib.pyplot as plt
import random
def get_random_color(pastel_factor = 0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def plot_linestring(geom,color="black",linewidth=0.1,linestyle='-'):
    #it visualizes a linestring
    points = geom.GetPoints()
    ptsx = [p[0] for p in points]
    ptsy = [p[1] for p in points]
    #args=(ptsx,ptsy)
    plt.plot(ptsx,ptsy,color=color,linewidth=linewidth,linestyle=linestyle)

def plot_rings(geom,edgecolor="black",fillcolor="grey",
                  holeedgecolor='red',holefillcolor='white',
                  alpha=0.5,linewidth=0.1,fill=True):
    #it visualizes a polygon with its outer ring and inner rings
    ring=geom.GetGeometryRef(0)
    points = ring.GetPoints()
    ptsx = [p[0] for p in points]
    ptsy = [p[1] for p in points]
    args=(ptsx,ptsy)
    plt.fill(*args,closed=True,fill=fill,   #outer ring
                 facecolor=fillcolor,
                 linewidth=linewidth,
                 edgecolor=edgecolor,alpha=alpha)
    n=geom.GetGeometryCount()
    args=()
    for i in range(1,n):                #inner rings
        ring=geom.GetGeometryRef(i)
        points=ring.GetPoints()        
        ptsx=[p[0] for p in points]
        ptsy=[p[1] for p in points]
        args=args+(ptsx,ptsy)
    plt.fill(*args, closed=True, fill=fill,
             facecolor=holefillcolor,
             linewidth=0.1,
             edgecolor=holeedgecolor, alpha=alpha)

def plot_geometry(geom,color='grey',edgecolor="black",fillcolor="grey",
                  holeedgecolor='red',holefillcolor='white',
                  alpha=0.5,linewidth=0.1,linestyle='-',symbol='r.',fill=True):
    geomtype = geom.GetGeometryName()
    if geomtype == "MULTIPOLYGON":
        for i in range(geom.GetGeometryCount()): #in the number of components
            geom1=geom.GetGeometryRef(i)
            plot_rings(geom1, edgecolor,fillcolor,holeedgecolor,holefillcolor,alpha,linewidth,fill)
    elif geomtype == "POLYGON":
        plot_rings(geom, edgecolor,fillcolor,holeedgecolor,holefillcolor,alpha,linewidth,fill)
    elif geomtype == "LINESTRING":
        linewidth=0.8
        plot_linestring(geom, color, linewidth, linestyle)
    elif geomtype == "MULTILINESTRING":
        linewidth = 0.8
        for i in range(geom.GetGeometryCount()):  # in the number of linestrings
            geom1 = geom.GetGeometryRef(i)
            plot_linestring(geom1, color, linewidth, linestyle)
    elif geomtype == "POINT":
        plt.plot(geom.GetX(),geom.GetY(),symbol)
    else:
        pass
    plt.axis('scaled')

class VisualLayer:
    def __init__(self,layer,fill=True):
        self.layer=layer
        self.fill=fill
    def plot(self):
        self.layer.ResetReading()
        for i in range(self.layer.GetFeatureCount()):
            f = self.layer.GetNextFeature()
            geom = f.GetGeometryRef()
            color = get_random_color()
            plot_geometry(geom, edgecolor="grey", fillcolor=color, color=color,
                          holeedgecolor='grey', holefillcolor='white',fill=self.fill)



if __name__ == '__main__':
    drvName = "ESRI Shapefile"
    driver = ogr.GetDriverByName(drvName)
    fname='data/countries_rectangle'
    shapefile=fname+'.shp'
    vector = driver.Open(shapefile, 0)
    layer = vector.GetLayer(0)
    vl=VisualLayer(layer,True)
    vl.plot()
    vector.Destroy()
    pdf_file=fname+'.pdf'
    plt.savefig(pdf_file,bbox_inches='tight',pad_inches=0)
    plt.show()
