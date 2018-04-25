import sys
import utils.io as io
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


def get_tallies(mcnpoutputlist):
    # Locate the start of all tallies (indicated by "Energy Distribution...")
    tally_nums = []
    tally_start_linenums = []
    for linenum in range(len(mcnpoutputlist)):
        if mcnpoutputlist[linenum]:
            if mcnpoutputlist[linenum][0] == 'cell':
                try:
                    tally_nums.append(int(mcnpoutputlist[linenum][1]))
                    tally_start_linenums.append(linenum)
                except:
                    pass
    # Locate the end of each tally
    tally_end_linenums = []
    for linenum in tally_start_linenums:
        while mcnpoutputlist[linenum]:
            linenum += 1
        tally_end_linenums.append(linenum+1)
    # Turn each tally output into a numpy array
    tallies = []
    tally_bounds = list(zip(tally_nums,tally_start_linenums,tally_end_linenums))
    for bounds in tally_bounds:
        start,stop = bounds[1],bounds[2]
        tally_energies = np.array(mcnpoutputlist[start+2:stop-2],dtype=float)
        tallies.append([bounds[0],tally_energies])
    return tallies

if __name__ == '__main__':
    mcnpoutput = sys.argv[1]
    # Find all tallies in the output
    mcnpoutputlist = io.read_mcnp_output(mcnpoutput)
    tallies = get_tallies(mcnpoutputlist)
    fig, ax = plt.subplots(figsize=(10,8))
    for tally in tallies:
        ax.plot(tally[1][1:-1,0],tally[1][1:-1,1],label='Cell {}'.format(tally[0]))
    ax.legend()
    ax.set_xlim(2.001,2.780)
    plt.show()
