"""
2024-01-29 13:30:40
Created by FV + ChatGPT

This script is useful to color branches in a phylogeny based on text files (one file per group)
In the working folder, one must place the script, the tree in newick format and a list of files (.txt extension is mandatory).
The files should contain endline separated lists of the entries in the tree.
The functions that perform the task (phylogeny_tree and paint_tree) were based on HMMERCTTER's functions.
The function to sort and read the .txt files was created with ChatGPT's assistance.
The outputs will be the colored tree in nexml and svg formats.
Dendroscope (install and put in PATH) and xvfb (Synaptic) are required. 
Python modules natsort, Biopython and numpy are also required.

"""

from __future__ import division
from __future__ import print_function
from Bio import SeqIO
from Bio import Phylo
import os
import random
import numpy as np
import argparse
from natsort import natsorted

parser = argparse.ArgumentParser()
parser.add_argument("-t", default="training.tree", help="Specify the training tree (default 1_target.tree)")
args = vars(parser.parse_args())

input_tree = str(args['t'])
family_name = input_tree.split(".")[0]
folder_path = "./"

# Paint tree
main_colors = ["255 0 0", "0 255 0", "0 0 255", "255 255 0", "0 255 255",
     "255 0 255", "128 128 128", "128 0 0", "128 128 0", "0 128 0",
     "128 0 128", "0 128 128", "0 0 128"]
secondary_colors = ["139 0 0", "178 34 34", "220 20 60", "255 99 71",
     "255 127 80", "205 92 92", "233 150 122", "250 128 114", "255 69 0",
      "255 140 0", "184 134 11", "218 165 32", "189 183 107", "154 205 50",
       "85 107 47", "107 142 35", "173 255 47", "0 100 0", "34 139 34",
        "50 205 50", "144 238 144", "143 188 143", "0 250 154", "0 255 127",
         "46 139 87", "102 205 170", "60 179 113", "32 178 170", "47 79 79",
          "64 224 208", "72 209 204", "127 255 212", "95 158 160",
           "70 130 180", "100 149 237", "30 144 255", "135 206 235",
            "25 25 112", "138 43 226", "75 0 130", "72 61 139",
             "106 90 205", "123 104 238", "147 112 219", "139 0 139",
              "148 0 211", "153 50 204", "186 85 211", "221 160 221",
               "238 130 238", "218 112 214", "199 21 133", "219 112 147",
                "255 20 147", "255 105 180", "139 69 19", "160 82 45",
                 "210 105 30", "205 133 63", "244 164 96", "210 180 140",
                  "188 143 143", "255 222 173", "255 218 185", "112 128 144",
                   "119 136 153", "176 196 222"]
all_colors = list(main_colors + secondary_colors)

def read_and_sort_txt_files(folder_path):
    """
    Reads all .txt files in a folder, sorts them alphanumerically, 
    and creates a list of lists. Each sublist corresponds to the lines 
    of the respective file.

    Parameters:
    - folder_path (str): The path to the folder containing .txt files.

    Returns:
    - list of lists: Each sublist contains the lines from a corresponding .txt file.
    """
    result = []

    # List all files in the folder and sort them alphanumerically
    files = natsorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
            result.append(lines)

    return result

def phylogeny_tree(train_tree, path):
    """
    Converts input tree into a Midpoint Root tree
    """
    cf = open('com_file.txt', 'w')
    cf.write('open file=\'' + str(train_tree) +
    '\';midpointroot;save format=newick file=\'Training_MidPoint.tree\';quit;')
    cf.close()

    os.system('xvfb-run --auto-servernum --server-num=1 Dendroscope -g -E -c ' +
    str(path) + '/' + 'com_file.txt')

    os.system('rm com_file.txt')
    #print(("Mid-Point Root Tree created: " + str((datetime.now() - startTime))))

    training_tree = next(Phylo.parse('Training_MidPoint.tree', 'newick'))

def paint_tree(groups_list, family_name):
    """
    Colors groups in the Midpoint Root tree
    """
    if len(groups_list) <= len(main_colors):
        # If they are <= 13 groups, just use the main colors
        painted_groups = []

        for g_names, lg in zip(groups_list, range(0, len(groups_list))):
            find_labels = []
            for on in g_names:
                f_label = 'find searchtext=' + str(on) + ' target=Nodes'
                find_labels.append(f_label)

            group_painted = str(';'.join(map(str, find_labels))) + ';select inducedNetwork;set color=' + str(main_colors[lg]) + ';deselect all;'
            painted_groups.append(group_painted)

        cf = open('com_file_group.txt', 'w')
        cf.write('open file=\'Training_MidPoint.tree\';show nodelabels=false' +
        ';show edgelabels=false;show edgeweights=false;set edgewidth=2;' +
        str(';'.join(map(str, painted_groups))) +
        ' select all; set drawer=RadialPhylogram;' +
        'show scalebar=false;deselect all;' +
        'save format=nexml file=\'' + str(family_name) + '_tree.nexml\';' +
        'exportimage file=\'' + str(family_name) + '_tree.svg\' format=SVG REPLACE=true;' +
        #'exportimage file=\'RESULT_tree.png\' format=PNG REPLACE=true;' +
        ';quit;END')
        cf.close()

        # Plot it in Dendroscope
        os.system('xvfb-run --auto-servernum --server-num=1 Dendroscope' +
        ' -g -E -c ' + str(folder_path) + '/' + 'com_file_group.txt')

    else:

        if len(groups_list) <= len(all_colors):
            # If they are >13 groups but less than 80, use main colors first
            # and then use secondary colors in order
            painted_groups = []
            painted_lg = []

            for g_names, lg in zip(groups_list, range(0, len(groups_list))):
                find_labels = []

                for on in g_names:
                    f_label = 'find searchtext=' + str(on) + ' target=Nodes'
                    find_labels.append(f_label)
                group_painted = str(';'.join(map(str, find_labels))) + ';select inducedNetwork;set color=' + str(main_colors[lg]) + ';deselect all;'
                painted_groups.append(group_painted)
                painted_lg.append(lg)

                if len(painted_groups) == len(main_colors):
                    break

            rest_of_groups = []

            for group, lg in zip(groups_list, range(0, len(groups_list))):
                if lg not in painted_lg:
                    rest_of_groups.append(group)

            used_colors = random.sample(secondary_colors, len(rest_of_groups))

            for r_names, rlg in zip(rest_of_groups, range(0, len(rest_of_groups))):
                find_labels = []

                for on in r_names:
                    f_label = 'find searchtext=' + str(on) + ' target=Nodes'
                    find_labels.append(f_label)
                group_painted = str(';'.join(map(str, find_labels))) + ';select inducedNetwork;set color=' + str(used_colors[rlg]) + ';deselect all;'
                painted_groups.append(group_painted)

            cf = open('com_file_group.txt', 'w')
            cf.write('open file=\'Training_MidPoint.tree\';show nodelabels=false' +
            ';show edgelabels=false;show edgeweights=false;set edgewidth=2;' +
            str(';'.join(map(str, painted_groups))) +
            ' select all; set drawer=RadialPhylogram;' +
            'show scalebar=false;deselect all;' +
            'save format=nexml file=\'' + str(family_name) + '_tree.nexml\';' +
            'exportimage file=\'' + str(family_name) + '_tree.svg\' format=SVG REPLACE=true;' +
            #'exportimage file=\'RESULT_tree.png\' format=PNG REPLACE=true;' +
            ';quit;END')
            cf.close()
            # Plot it in Dendroscope
            os.system('xvfb-run --auto-servernum --server-num=1 Dendroscope' +
            ' -g -E -c ' + str(folder_path) + '/' + 'com_file_group.txt')

        else:
            # If they are > 80 groups, use all colors in order, and then use
            # them again random with repetitions
            painted_groups = []
            painted_lg = []

            for g_names, lg in zip(groups_list, range(0, len(groups_list))):
                find_labels = []
                for on in g_names:
                    f_label = 'find searchtext=' + str(on) + ' target=Nodes'
                    find_labels.append(f_label)
                group_painted = str(';'.join(map(str, find_labels))) + ';select inducedNetwork;set color=' + str(main_colors[lg]) + ';deselect all;'
                painted_groups.append(group_painted)
                painted_lg.append(lg)
                if len(painted_groups) == len(main_colors):
                    break

            rest_of_groups = []

            for group, lg in zip(groups_list, range(0, len(groups_list))):
                if lg not in painted_lg:
                    rest_of_groups.append(group)

            try:
                used_colors = random.sample(all_colors, len(rest_of_groups))
            except ValueError:
                used_colors = np.random.choice(all_colors, len(rest_of_groups))

            for r_names, rlg in zip(rest_of_groups, range(0, len(rest_of_groups))):
                find_labels = []

                for on in r_names:
                    f_label = 'find searchtext=' + str(on) + ' target=Nodes'
                    find_labels.append(f_label)
                group_painted = str(';'.join(map(str, find_labels))) + ';select inducedNetwork;set color=' + str(used_colors[rlg]) + ';deselect all;'
                painted_groups.append(group_painted)

            cf = open('com_file_group.txt', 'w')
            cf.write('open file=\'Training_MidPoint.tree\';show nodelabels=false' +
            ';show edgelabels=false;show edgeweights=false;set edgewidth=2;' +
            str(';'.join(map(str, painted_groups))) +
            ' select all; set drawer=RadialPhylogram;' +
            'show scalebar=false;deselect all;' +
            'save format=nexml file=\'' + str(family_name) + '_tree.nexml\';' +
            'exportimage file=\'' + str(family_name) + '_tree.svg\' format=SVG REPLACE=true;' +
            #'exportimage file=\'RESULT_tree.png\' format=PNG REPLACE=true;' +
            ';quit;END')
            cf.close()
            # Plot it in Dendroscope
            os.system('xvfb-run --auto-servernum --server-num=1 Dendroscope' +
            ' -g -E -c ' + str(folder_path) + '/' + 'com_file_group.txt')

    return()

final_clustering = read_and_sort_txt_files(folder_path)

phylogeny_tree(input_tree, folder_path)

paint_tree(final_clustering, family_name)

os.system('rm Training_MidPoint.tree')
os.system('rm com_file_group.txt')