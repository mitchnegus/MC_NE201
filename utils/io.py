'''Utilities for python scripts'''

def read_mcnp_input(filename):
    '''Read MCNP input and return a list of lines, separated by item'''
    with open(filename,'r') as infile:
        linelist = [line.rstrip('\n& ').split() for line in infile.readlines()]
    return linelist

def read_mcnp_output(filename):
    '''Read MCNP output and return a list of lines, separated by item'''
    with open(filename,'r') as infile:
        linelist = [line.rstrip('\n ').split() for line in infile.readlines()]
    return linelist
