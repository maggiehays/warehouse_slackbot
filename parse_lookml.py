import lkml

with open('sample_lookml.lkml', 'r') as file:
    parsed = lkml.load(file)