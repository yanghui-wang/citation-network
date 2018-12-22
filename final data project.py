#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:42:27 2018

@author: yanghuiwang
"""

#%%
"""
• Clean the data
"""

import matplotlib.pyplot as plt
import networkx as nx
import re

with open("outputacm.txt","r") as f:
    data = f.read().split('\n\n')
n = len(data)-1

citation= [map(int,re.findall(r'(?:#%)(\d+)',data[i])) for i in range(n)] # find all citation of each node and turn them into integers

#%%
"""
• Create nodes, edges, and bigragh G
"""

edgewhole=[(i,j) for i in range(n) for j in citation[i]]
node=range(n)
G=nx.DiGraph()
G.add_nodes_from(node)
G.add_edges_from(edgewhole)

#%%
"""
• Use PageRank on the discovered network to rank the papers by importance.
"""

# pagerank 

pr=nx.pagerank(G,alpha=0.99)
mydic=dict(zip(node,citation))

# sort pagerank

from operator import itemgetter

sorted_pr = sorted(pr.items(), key=itemgetter(1)) # all nodes with weight
impnodes=sorted_pr[::-1] # all nodes with weight arranged descendingly 
print impnodes[0] # (453387, 0.0002667540311108015) the most important node and its weight
#%%

"""
• Display the ranking.
"""
 
# for distribution image

from nltk import FreqDist
fdist=FreqDist(citation[i][j] for i in range(n) for j in range(len(citation[i])))
fdist.plot(10, cumulative=False,title='The first 10 most cited books')
#%%

# for table ranking

m=20 # first 20 
implist = [impnodes[i][0] for i in range(m)] # the first 20 most important nodes
print implist,len(implist) # [453387, 246511, 586607, 81323, 79620, 214951, 326368, 162585, 311413, 517247, 455254, 178287, 327827, 231782, 151297, 144427, 319217, 616075, 250081, 162995] 20

list=[]
for i in range(m):
    list.append ([j for j in range(n) if implist[i] in citation[j]]) # find who cited the first 20 node and put in to a list of lists
print len(list[1]) # 442 is the number of times the second most important node being cited

from prettytable import PrettyTable
title= [re.findall(r'(?:#\*)(.+)',data[implist[i]])[0] for i in range(m)]
author=[re.findall(r'(?:#@)(.+)',data[implist[i]])[0] for i in range(m)]
year=[int(re.findall(r'(?:#t)(.+)',data[implist[i]])[0]) for i in range(m)]
cite=[len(citation[implist[i]]) for i in range(20)]
cited=[len(list[i]) for i in range(20)]

x = PrettyTable()
x.add_column('Rank',range(1,21))
x.add_column('ID',implist)
x.add_column('Title',title)
x.add_column('Author',author)
x.add_column('Year',year)
x.add_column('Cite',cite)
x.add_column('Cited',cited)
x.align["Rank"]="l"
x.align["ID"]="l"
x.align["Title"]="l"
x.align["Author"]="l"
x.align["Year"]="l"
x.align["Cite"]="l"
x.align["Cited"]="l"
lines = x.get_string()
print(x)


with open('output.txt','w') as file:
    file.write(lines)

#%%
"""
• Graph drawing algorithm to create a visually pleasing picture of the most important papers/authors in your network, and come up with a nice way to display the ranking.
"""

def findnds(m):
    ndslist = []
    impndlist = [impnodes[0][0]]
    impnd=impnodes[0][0] #453387
    for i in range(m):
        nds=[j for j in range(n) if impnd in citation[j]] # find all nodes which cited the impnd
        ndslist.append(nds) # append the nodes
        print len(nds) # 816; 33; 37; 8 
        dic={} 
        for k in range(len(nds)):
            dic[nds[k]]=pr[nds[k]] # project the whole dataset into a smaller one with nodes which cited the impnd
        sorted_pr=sorted(dic.items(),key=itemgetter(1)) # rank them 
        if sorted_pr:
            std=sorted_pr[-1] # find the most important within the dict and its weight
            impnd = std[0]
            impndlist.append(impnd)
        else:
            print 'no cited after the %d\'th node'%m
    return ndslist,impndlist

findnds(6)

#Visulization

nds_l, impnd_l = findnds(6)
ndshow = [0]*6
ndrank = [0]*6
for i in range(6):
    #if len(nds_l[i]) > 20: # if more than 20 nodes cited the node
    d1 = {}
    for k in range(len(nds_l[i])):
        d1[nds_l[i][k]]=pr[nds_l[i][k]] # project node and weight
    pr_s = sorted(d1.items(),key=itemgetter(1)) # sorted by weight
    pr_s = pr_s[:-21:-1] # return the first most important node to virtualize
    ndshow[i] = [pr_s[j][0] for j in range(len(pr_s))]
    ndrank[i] = [pr_s[j][1] for j in range(len(pr_s))]
 
center= impnd_l[0]
egshow =[0]*6

for i,v in enumerate(impnd_l): # connect in between clusters
    egshow[i] = [(j, v) for j in ndshow[i]]
print egshow


nodelist=[i for j in range(6) for i in ndshow[j]] # 20+20+20+8+8

#%%

Graph=nx.DiGraph()
Graph.add_nodes_from(nodelist)
for i in range(6):
    Graph.add_edges_from(egshow[i]) 


rank_dict = {ndshow[i][j]:ndrank[i][j]*(10**8) for i in range(len(ndshow)) for j in range(len(ndshow[i]))}
rank_dict[center] = impnodes[0][1]*(10**8/4)

cluster_dict = {ndshow[i][j]:i for i in range(len(ndshow)) for j in range(len(ndshow[i]))}

for i,v in enumerate(impnd_l):
    cluster_dict[v] = 5 

#print cluster_dict

#set node attributes
nx.set_node_attributes(Graph,rank_dict,'rank')
nx.set_node_attributes(Graph,cluster_dict,'cluster')
print Graph.nodes()


node_num = len(Graph.nodes())
colors = [0]*node_num
size = [0]*node_num
for i,n in enumerate(Graph.nodes()):
    if Graph.node[n]['cluster'] == 0:
        colors[i] = 'pink'
    elif Graph.node[n]['cluster'] == 1:
        colors[i] = 'orange'
    elif Graph.node[n]['cluster'] == 2:
        colors[i] = 'yellow'
    elif Graph.node[n]['cluster'] == 3:
        colors[i]='green'
    elif Graph.node[n]['cluster'] == 4:
        colors[i] ='blue'
    else:
        colors[i] ='red'

#print len(colors)

for i,n in enumerate(Graph.nodes()):
    size[i] = Graph.node[n]['rank']

nx.draw(Graph,node_color = colors, node_size = size, font_size = 5, with_labels = True)

plt.show()


#%%
"""
@INPROCEEDINGS{Tang:08KDD,
    AUTHOR = "Jie Tang and Jing Zhang and Limin Yao and Juanzi Li and Li Zhang and Zhong Su",
    TITLE = "ArnetMiner: Extraction and Mining of Academic Social Networks",
    pages = "990-998",
    YEAR = {2008},
    BOOKTITLE = "KDD'08",
}
 
@article{Tang:10TKDD,
     author = {Jie Tang and Limin Yao and Duo Zhang and Jing Zhang},
     title = {A Combination Approach to Web User Profiling},
     journal = {ACM TKDD},
     year = {2010},
     volume = {5},
     number = {1},
    pages = {1--44},
 }
 
@article{Tang:11ML,
     author = {Jie Tang and Jing Zhang and Ruoming Jin and Zi Yang and Keke Cai and Li Zhang and Zhong Su},
     title = {Topic Level Expertise Search over Heterogeneous Networks},
     year = {2011},
     volume = {82},
     number = {2},
     pages = {211--237},
     journal = {Machine Learning Journal},
}
 
@article{Tang:12TKDE,
    author = {Jie Tang and Alvis C.M. Fong and Bo Wang and Jing Zhang},
    title = {A Unified Probabilistic Framework for Name Disambiguation in Digital Library},
    journal ={IEEE Transactions on Knowledge and Data Engineering},
    volume = {24},
    number = {6},
    year = {2012},
    pages = {975-987},
}
 
@INPROCEEDINGS{Tang:07ICDM,

    AUTHOR = "Jie Tang and Duo Zhang and Limin Yao",
    TITLE = "Social Network Extraction of Academic Researchers",
    PAGES = "292-301",
    YEAR = {2007},
    BOOKTITLE = "ICDM'07",
}
 
@inproceedings{sinha2015overview,
  title={An overview of microsoft academic service (mas) and applications},
  author={Sinha, Arnab and Shen, Zhihong and Song, Yang and Ma, Hao and Eide, Darrin and Hsu, Bo-june Paul and Wang, Kuansan},
  booktitle={Proceedings of the 24th international conference on world wide web},
  pages={243--246},
  year={2015},
  organization={ACM}
}
"""