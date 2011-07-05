#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image, ImageDraw
import sys


def pdt_tuple(tup, k):
    return (k * tup[0], k * tup[1])

def somme_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

"""
    binom(k,n):
    renvoir le coefficient
    binomial k parmi n
"""
  
def binom(k,n):
    if k > n or k < 0:
        return 0
    elif k == n or k == 0:
        return 1
    else:
        return binom(k-1,n-1) + binom(k, n-1)
"""
    bezier(courbe, t):
    Renvoi les coordonnées d'un point sur une courbe de bézier
    en fonction du paramètre t.
"""
        
def bezier(courbe,t):
    point = (0,0)
    n = len(courbe)-1
    for i,pt in enumerate(courbe):
        point = somme_tuple(point, pdt_tuple(pt, binom(i,n) * t**i * (1 - t)**(n-i)))
    
    return (int(point[0]), int(point[1]))

"""
    Renvoi un tableau d'une courbe de bézier.
"""

def f_bezier(courbe):
    prec = 1000.
    table = [0 for _ in range(256)]
    avg = [0 for _ in range(256)]
    
    for v in range(int(prec)+1):
        i, val = (bezier(courbe, v/prec))
        table[i] += val
        avg[i] += 1
        
    return [ table[i] / avg[i] for i in range(256) ]


"""
    draw_bezier(courbe, filename):
    dessine la courbe sur un fichier
"""
    
def draw_bezier(courbe, filename):
    im = Image.new('L', (255,255))
    draw = ImageDraw.Draw(im)
    
    points = [ ( bezier(courbe, t / 255.)[0], 255 - bezier(courbe, t / 255.)[1] ) for t in range(256) ]
    draw.point(points, fill=200)
    del draw 

    # write to stdout
    im.save(filename+'.png', "PNG")

