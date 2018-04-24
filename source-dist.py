import sys
import utils.io as io
import numpy as np
from matplotlib import pyplot as plt


def get_mcnp_card_values(cardname,mcnpinputlist):
    '''Get contents of a card from an MCNP input'''
    # Locate the start of the card 
    for linenum in range(len(mcnpinputlist)):
        if mcnpinputlist[linenum]:
            if mcnpinputlist[linenum][0] == cardname:
                card_start_linenum = linenum
    # Collect all lines in the card (cards separated by a blank comment)
    input_linenum = card_start_linenum 
    card = []
    while mcnpinputlist[input_linenum][0].lower() != 'c':
        card.append(mcnpinputlist[input_linenum])
        input_linenum += 1
    # Split the card into individual values (and format as numbers)
    for card_linenum in range(len(card)):
        card[card_linenum] = ' '.join(card[card_linenum])
    card_values = ' '.join(card).split()[1:]
    card_values = np.array(card_values).astype('float')
    return card_values

def plot_energy_vs_angle(ax,angle_card,energy_card):
    '''Plot the source energy as a function of angle'''
    angle_card = np.arccos(angle_card)
    ax.plot(angle_card,energy_card)
    ax.set_xlabel('Angle [rad]')
    ax.set_ylabel('Energy [MeV]')
    return ax

if __name__ == '__main__':
    cards_to_get = ['SI4','DS5']
    mcnpinputs = sys.argv[1:]
    fig,ax = plt.subplots()
    for mcnpinput in mcnpinputs:
        mcnpinputlist = io.read_mcnp_input(mcnpinput);
        cards = {}
        for cardname in cards_to_get:
            card_values = get_mcnp_card_values(cardname,mcnpinputlist)
            cards[cardname] = card_values
        plot_energy_vs_angle(ax,cards['SI4'],cards['DS5'])
    plt.show()


