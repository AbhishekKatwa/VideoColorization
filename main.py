#!/usr/bin/env python

import sys
import time
from random import randrange
from PIL import Image
from PIL import ImageFilter
from filterfft import *
from disjointset import DisjointSet
from graph import Graph


#Default Values
K = 300
MinCC = 20
Sigma = 0.5

#Runtime scale of observation
#Larger K larger components
def tau(C):
    return K/float(C)

#width,height, disjoint set, graph
def segment(w, h, ds, g):
	# K*w*h
    dist = [tau(1.0)]*(w*h)
    #merges
    me = 0
    for e in g.E:
        #print('Edge %d and %d = %f' % (e.v1, e.v2, e.dist))
        p1 = ds.find(e.v1)
        p2 = ds.find(e.v2)
        if p1 != p2:
            if e.dist <= min(dist[p1.key], dist[p2.key]):
                pn = ds.unionNode(p1, p2)
                dist[pn.key] = e.dist + tau(pn.size)
                #print('Merging %d and %d, sz = %d, tau = %lf, dist = %lf, tot = %lf' % (p1.key, p2.key, pn.size, tau(pn.size), e.dist, dist[pn.key]))
                me = me + 1
    #for i in range(w*h):
    #    print (dist[i])
    print('Total merges: ',me)

def postprocess(ds, g):
    for e in g.E:
        p1 = ds.find(e.v1)
        p2 = ds.find(e.v2)
        if p1 != p2:
            if p1.size < MinCC or p2.size < MinCC:
                ds.unionNode(p1, p2)

def randomColour(w, pix, ds, image):
    orig_img = Image.open("beach1.jpg")
    #orig_img.show()
    orig_pix = orig_img.load()
    col = list()
    cols = list()
    i=0
    for (pp, node) in ds.dataSet.items():
    	#Parent returned, COlor is assigned to parent and then applied to all childrens O(n logn)
        rep = ds.findNode(node)
        if rep not in col:
        	col.append(rep)
        	cols.append((randrange(0, 255),randrange(0, 255),randrange(0, 255)))
        	(j,i) = (pp/w, pp%w)
        	orig_pix[i,j] = (255,255,255)
        	i = i+1
        else:
        	ind = col.index(rep)
        	(j,i) = (pp/w, pp%w)
        	orig_pix[i,j] = cols[ind]
    orig_img.show()
    return len(col)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: main.py image [K min sigma]")
        sys.exit()

    if len(sys.argv) > 2:
        K = int(sys.argv[2])
    if len(sys.argv) > 3:
        MinCC = int(sys.argv[3])
    if len(sys.argv) > 4:
        Sigma = float(sys.argv[4])

    print('Processing image %s, K = %d', sys.argv[1], K)
    start = time.time()

# Apply gaussian filter to all color channels separately
    im = Image.open(sys.argv[1])
    im = im.convert('1')
    #im.show()
    (width, height) = im.size
    #print('Image width = %d, height = %d' % (width, height))

	#Smoothning
    print('Blurring with Sigma = %f' , Sigma)
    
    #Split this image into individual bands. 
    #This method returns a tuple of individual image bands from an image. 
    #For example, splitting an “RGB” image creates three new images each containing a copy of one of the original bands (red, green, blue).
    #Returns:	A tuple containing bands.
    source = im.split()
    
    '''blurred = []
    for c in range(len(source)):
        I = numpy.asarray(source[c])
        I = filter(I, gaussian(Sigma))
        blurred.append(Image.fromarray(numpy.uint8(I)))'''
    
    #Merging the image with blurred Image    
    #im = Image.merge(im.mode, tuple(blurred))
    #im.show()

	
    pix = im.load()
    ds = DisjointSet(width*height)
    for j in range(height):
        for i in range(width):
            ds.makeSet(j*width + i, pix[i,j])
            #print( pix[i,j])

    print('Number of pixels: %d' % len(ds.dataSet))
    g = Graph(width, height, pix)
    print(g)
    #print(pix)
    print('Number of edges in the graph: %d' % len(g.E))
    print('Time: %lf' % (time.time() - start))

    segstart = time.time()
    segment(width, height, ds, g)
    print('Segmentation done in %lf, found %d segments' % (time.time() - segstart, ds.num))

    print('Postprocessing small components, min = %d' % MinCC)
    postproc = time.time()
    postprocess(ds, g)
    print('Postprocessing done in %lf' % (time.time() - postproc))

    l = randomColour(width, pix, ds , sys.argv[1])
    #print('Regions produced: %d' % l)
	
    print
    print('Time total: %lf' % (time.time() - start))

    im.show()

