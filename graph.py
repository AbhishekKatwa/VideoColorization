#!/usr/bin/env python

class Edge:
    def __init__(self, v1, v2, dist):
        self.v1 = v1
        self.v2 = v2
        self.dist = dist
        #print('(%d, %d) = %lf' % (self.v1,self.v2,self.dist))

class Graph:
    def __init__(self, w, h, pix):
        self.w = w
        self.h = h
        self.E = []
        for j in range(h):
            for i in range(w):
                cur = j*w + i
                #print(pix[i,j])
                #for making edge with node below it,[0,0] with [1,0]
                if i < w-1:
                  self.E.append(Edge(cur, j*w + (i+1), self.dist(pix[i,j], pix[i+1,j])))
                #for making edge with node next to it, [0,0] with [0,1[
                if j < h-1:
                  self.E.append(Edge(cur, (j+1)*w + i, self.dist(pix[i,j], pix[i,j+1])))
                #for diagonal right egde  
                if i < w-1 and j < h-1:
                  self.E.append(Edge(cur, (j+1)*w + (i+1), self.dist(pix[i,j], pix[i+1,j+1])))
                #for diagonal left egde
                if i < w-1 and j > 0:
                  self.E.append(Edge(cur, (j-1)*w + (i+1), self.dist(pix[i,j], pix[i+1,j-1])))
        self.E.sort(key = lambda a: a.dist)
        

    def dist(self, v1, v2):
        #return sum(map(lambda a,b: (a-b)*(a-b), v1, v2))**.5
        return abs(v1-v2)

