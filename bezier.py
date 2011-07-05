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

"""
    Principe :
    Dans toutes les fonctions
    courbe est une liste de tuple par lesquels passent la courbe
"""


def pdt_tuple(tup, k):
    return (k * tup[0], k * tup[1])

def somme_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])
  
def binom(k,n):
    """
        renvoi le coefficient
        binomial: k parmi n
    """
    if k > n or k < 0:
        return 0
    elif k == n or k == 0:
        return 1
    else:
        return binom(k-1,n-1) + binom(k, n-1)
        
def bezier(courbe,t):
    """
        bezier(courbe, t):
        Renvoi les coordonnées d'un point sur une courbe de bézier
        en fonction du paramètre t.
    """
    point = (0,0)
    n = len(courbe)-1
    for i,pt in enumerate(courbe):
        point = somme_tuple(point, pdt_tuple(pt, binom(i,n) * t**i * (1 - t)**(n-i)))
    
    return (int(point[0]), int(point[1]))

def f_bezier(courbe):
    """
        Renvoi un tableau d'une courbe de bézier.
    """
    
    # Précision
    prec = 1000.
    table = [0 for _ in range(256)]
    avg = [0 for _ in range(256)]
    
    for v in range(int(prec)+1):
        i, val = (bezier(courbe, v/prec))
        table[i] += val
        avg[i] += 1
        
    return [ table[i] / avg[i] for i in range(256) ]
    
def draw_bezier(courbe, filename):
    """
        dessine la courbe sur un fichier
    """
    im = Image.new('L', (255,255))
    draw = ImageDraw.Draw(im)
    
    points = [ ( bezier(courbe, t / 255.)[0], 255 - bezier(courbe, t / 255.)[1] ) for t in range(256) ]
    draw.point(points, fill=200)
    del draw 

    # write to stdout
    im.save(filename+'.png', "PNG")

