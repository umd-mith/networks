#!/usr/bin/env python

import codecs
import igraph
import urllib
import csv

csv_url = 'https://docs.google.com/spreadsheets/d/1tmzoUWrVTGjzhetWyexDTi9dJpAwXhqUUiUreYPioGc/export?format=csv'

http_stream = urllib.urlopen(csv_url)
csv_reader = csv.reader(http_stream)
csv_writer = csv.writer(codecs.open("people-interests.csv", "wb"))

# skip header
next(csv_reader)

for row in csv_reader:
    if not row[0]:
        continue
    name = row[1]
    for col in row[2:]:
        csv_writer.writerow([name, col])

# read back in data and write out graphs
data = csv.reader(open("people-interests.csv"))
g = igraph.Graph()

for row in data:
    g.add_vertex(row[0], type=True)
    g.add_vertex(row[1], type=False)
    g.add_edge(row[0], row[1])

g1, g2 = g.bipartite_projection(types="type")

def output(graph, filename):
    out = csv.writer(open(filename, "w"))
    for edge in graph.es():
        out.writerow([
            graph.vs(edge.source)['name'][0],
            graph.vs(edge.target)['name'][0], 
            edge['weight']
        ])

output(g1, "interests.csv")
output(g2, "people.csv")
