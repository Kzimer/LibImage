"""
    Copyright (c) Fabre Arnaud 2011
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


#!/usr/bin/python
# -*- coding: utf-8 -*-


import Image, ImageDraw
import sys
import bezier

def fromdata(data, mode, size):
    im = Image.new(mode, size)
    im.putdata(data)
    return im

def xy2pos(x, y, size):
    return y * size[0] + x
    
def pos2xy(pos, size):
    return (pos % size[0], pos // size[0])

def dist(pos1, pos2, size):
    p1 = pos2xy(pos1, size)
    p2 = pos2xy(pos2, size)
    return ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )**(1./2.)
    

def rgb2hsl(r, g, b):
    var_R = (r / 255.)
    var_G = (g / 255.)
    var_B = (b / 255.)
    
    var_Min = min(var_R, var_G, var_B)
    var_Max = max(var_R, var_G, var_B)
    del_Max = var_Max - var_Min 

    L = (var_Max + var_Min) / 2.
    if del_Max == 0:
        return 0,0,int(L * 100.)

    if L < 0.5:
        S = del_Max / (var_Max + var_Min)
    else:
        S = del_Max / (2. - var_Max - var_Min)
            
    del_R = (((var_Max - var_R) / 6.) + (del_Max / 2.)) / del_Max
    del_G = (((var_Max - var_G) / 6.) + (del_Max / 2.)) / del_Max
    del_B = (((var_Max - var_B) / 6.) + (del_Max / 2.)) / del_Max

    if var_R == var_Max:
        H = del_B - del_G
    elif var_G == var_Max:
        H = (1. / 3.) + del_R - del_B
    elif var_B == var_Max:
        H = (2. / 3.) + del_G - del_R

    if H < 0.:
        H = H + 1
    if H > 1.:
        H = H - 1
        
    return int(H * 360.),int(S * 100.),int(L * 100.)



def hsl2rgb(t, s, l):
    """
    TODO
    """
    return 0,0,0

def get_pix_lumi(pixel):
    return (pixel[0] + pixel[1] + pixel[2]) / 3

def pix_lumi(pixel, value):
    return (pixel[0] + value, pixel[1] + value, pixel[2] + value)

def lumi(im, value):
    data = im.getdata()
    imNew = Image.new(im.mode ,im.size)
    imNew.putdata( [pix_lumi(pixel, value) for pixel in data] )
    return imNew

def vignetage(im, value, intensity):
    data = im.getdata()
    centre = xy2pos(size[0]/2,size[1]/2, size)
    maximum = dist(0, centre, size)
    return fromdata([pix_lumi(pixel, int(value * ((dist(pos, centre, im.size)) / maximum)**intensity) ) for (pos, pixel) in enumerate(data)], im.mode, im.size) 
    
def saturation(im, value):
    data = im.getdata()

def appli_bezier(im, courbe):
    """
        Fonction sur l'histogramme
        retourne une courbe de bezier traitement 3 composantes identique
        ou 3 (une par composante r,v,b)
    """
    im.getdata()
    if isinstance(courbe, list):
        comp = [ fromdata([courbe[v] for v in c.getdata()], 'L', im.size) for c in im.split() ]
        return Image.merge('RGB', comp)
    elif isinstance(courbe, tuple):
        comp = [ fromdata([courbe[i][v] for v in c.getdata()], 'L', im.size) for i,c in enumerate(im.split()) ]
        return Image.merge('RGB', comp)
            
        
def contraste(im,c):
    if c < 128:
        table = bezier.f_bezier( [(0,0), (128,128-c), (128,128), (128,128+c), (255,255)] )
    else:
        table = bezier.f_bezier( [(0,0), (c,0), (255-c,255), (255,255)] )
    
    return appli_bezier(im, table)


def draw_histogramme(data, filename, hauteur = 200):
    histo = histogramme(data)
    
    im = Image.new('L', (255,hauteur))
    draw = ImageDraw.Draw(im)
    
    maximum = max(histo)
    for i,value in enumerate(histo):
        longueur = int((float(value) / float(maximum)) * float(hauteur))
        draw.line((i,hauteur)+(i,hauteur-longueur), fill=200)
    del draw 

    # write to stdout
    im.save(filename+'.png', "PNG")

def histogramme(data):
    histo = [0 for i in range(256)]
        
    for pixel in data:
        histo[get_pix_lumi(pixel)] += 1
    
    return histo
        

def main():
    """
        Example 
        increase the contrast
    """
    filename = sys.argv[1]
    im = Image.open(filename)
    new = contraste(im, 50)
    new.save(filename+'2.png','PNG')
        
if __name__ == '__main__':
    main()

