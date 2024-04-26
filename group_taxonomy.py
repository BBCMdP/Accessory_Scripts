from ete3 import NCBITaxa
from ete3 import Tree
from io import StringIO
import argparse
import glob
import os
import pandas as pd
import plotly as plt
import plotly.express as px
import re
import requests

# Class to read inputs by extension and sort them alphanumerically
class FileSorter:
    def __init__(self, pattern):
        self.pattern = pattern

    def _numerical_sort(self, value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def sort_files(self):
        list_of_files = sorted(glob.glob(self.pattern), key=self._numerical_sort)
        return list_of_files

def get_unique_taxids(tsv_file):
    # Read the TSV file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep='\t')

    # Extract unique taxids from the 'taxid' column
    all_seqs = df['seq'].tolist()
    all_taxids = df['taxid'].tolist()
    unique_taxids = df['taxid'].unique().tolist()


    return all_seqs, all_taxids, unique_taxids

def read_sequences_from_file(file_path):
    with open(file_path, 'r') as file:
        sequences = file.readlines()
    return [seq.strip() for seq in sequences]

def assign_taxonomic_info(file,group_seqs, all_seqs, all_taxids, taxonomic_dict):
        """Get taxonomic rank information for each sequence in group
        Limited to ranks: species, genus, subfamily, family, order, subclass, class_, phylum, kingdom
        """
        group = file.split('.')[0]
        table_data = []

        for seq in group_seqs:
            # Find the index of the sequence in 'all_seqs'
            index = all_seqs.index(seq)
            # Get the taxid corresponding to the sequence
            taxid = all_taxids[index]    
            # Access the taxonomic information for the taxid
            tax_info = taxonomic_dict.get(taxid, {})    

            #Retrieve desired info from the dictionary
            species = tax_info.get('species', '')
            genus = tax_info.get('genus', '')
            subfamily = tax_info.get('subfamily', '')
            family = tax_info.get('family', '')
            order = tax_info.get('order', '')
            superorder =  tax_info.get('superorder', '')
            subclass = tax_info.get('subclass', '')
            class_ = tax_info.get('class', '')
            phylum = tax_info.get('phylum', '')
            kingdom = tax_info.get('kingdom', '')
                        
            table_data.append([group, seq, str(taxid), species, genus, subfamily, family, order, superorder, subclass, class_, phylum, kingdom])
        
        return table_data

def write_tabular_output(table_data, output_file):
        # Write the table data to the output file
        #check if file is empty
        try:
            is_empty = os.stat(output_file).st_size == 0
        except FileNotFoundError:
        # If the file doesn't exist, assume it's empty
            is_empty = True
        with open(output_file, 'a' if not is_empty else 'w') as file:
            # Write the header only if the file is empty
            if is_empty:
                header = ['group','sequence', 'taxid', 'species', 'genus', 'subfamily', 'family', 'order', 'superorder', 'subclass', 'class', 'phylum', 'kingdom']
                file.write('\t'.join(header) + '\n')
        
            # Write the data
            for row in table_data:
                file.write('\t'.join(row) + '\n')
    
def taxid2dict(in_seq_tax,taxid_list):
    # The function builds a table with taxonomic ranks for all the taxids in the input file (.tsv)
    # This input file must have the following columns: 'seq', 'taxid', representing each sequence in the dataset with the corresponding taxid (at species level) 
    filename = in_seq_tax.split('.')[0]
    # Construct the txid part of the URL
    txid_param = ','.join(map(str, taxid_list))

    # URL template with the txid parameter, using the API provided  @taxallnomy
    url_template = "http://bioinfo.icb.ufmg.br/cgi-bin/taxallnomy/taxallnomy_multi.pl?txid={}&rank=common"

    # Construct the complete URL
    url = url_template.format(txid_param)
    # Fetch the content from the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Split the content into lines
        lines = response.text.strip().split('\n')
        
        # Skip the first line
        lines = lines[1:]
        # Remove the '#' symbol before 'taxid'
        lines = [line.replace('#taxid', 'taxid') for line in lines]
        # Join the lines into a single string
        data = '\n'.join(lines)
        # Read the data into a pandas DataFrame
        df = pd.read_csv(StringIO(data), sep='\t')
        del df['subgenus']
        del df['subspecies']
            
        for col in df.columns:
            # Iterate over each row in the column
            for i in range(len(df)):
                # Check if the value is a string before splitting
                if isinstance(df[col][i], str):
                    # Split the item by underscore and retrieve the last portion
                    df.iloc[i, df.columns.get_loc(col)] = df[col][i].split('_')[-1]
        
        df.to_csv(filename + '_taxonomy.tsv', sep='\t')

    else:
        print("Failed to fetch data from the URL")

    # Initialize an empty dictionary to store taxonomic information
    taxonomic_dict = {}

    # Iterate over the DataFrame rows
    for index, row in df.iterrows():
        # Extract taxonomic information for the current row
        taxid = row['taxid']
        kingdom = row['kingdom']
        phylum = row['phylum']
        class_ = row['class']
        subclass = row['subclass']
        superorder = row['superorder']
        order = row['order']
        family = row['family']
        subfamily = row['subfamily']
        genus = row['genus']
        species = row['species']
        
        # Build a dictionary with taxonomic information for the current taxid
        taxonomic_info = {
            'kingdom': kingdom,
            'phylum': phylum,
            'class': class_,
            'subclass': subclass,
            'superorder': superorder,
            'order': order,
            'family': family,
            'subfamily': subfamily,
            'genus': genus,
            'species': species
        }

        # Add the taxonomic information to the taxonomic dictionary
        taxonomic_dict[taxid] = taxonomic_info
    return taxonomic_dict

def tree_by_taxa(rank_level, taxid_list): 
    """
    Required for heatmap.
    Generate a taxonomic tree at indicated taxonomic level (based on NCBI Taxonomy).
    Accepted levels are species, genus, subfamily, family, order, superorder, subclass, class, phylum, kingdom
    Uses also taxallnomy to retrieve full taxonomic data.
    The taxid_list correspond to the list of taxids associated to the sequences in the set (taxid @ species level). Calculated by get_unique_taxids
    """

    ncbi = NCBITaxa()
    # Get complete tree at rank_level
    tree = ncbi.get_topology(taxid_list, intermediate_nodes=True, rank_limit=rank_level) 
    tree.ladderize()
    outtree = 'tree_by_' + rank_level + '_taxid.tree'
    tree.write(format=1, outfile=outtree)

    leaves = []
    ranks = []   #once is populated, it will have the scientific names at rank indicated, sorted as in the tree

    #We need to match the taxids in the rank indicated with the corresponding scientific name.
    for leaf in tree:
        # URL template with the txid parameter, using the API provided  @taxallnomy
        url_template = "http://bioinfo.icb.ufmg.br/cgi-bin/taxallnomy/taxallnomy_multi.pl?txid={}&rank=common"
        # Construct the complete URL
        url = url_template.format(leaf.name.split("-")[-1])
        # Fetch the content from the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Split the content into lines
            lines = response.text.strip().split('\n')
            # Skip the first line
            lines = lines[1:]
            data = '\n'.join(lines)
            df = pd.read_csv(StringIO(data), sep='\t')
            tax_info = df.to_dict(orient='list')
            rank_value = tax_info[rank_level][0]
            if rank_value:
                rank_value = rank_value.split('_')[-1]
            ranks.append(rank_value) # contains all sci_names for the taxids in leaves (at the taxonomic rank indicated)
            leaves.append(leaf.name.split('-')[-1])
        else:
            print("Failed to fetch data from the URL")

    with open(outtree, 'r') as file:
        line = file.readline()

    # Replace the target value in the line
    for i, leaf in enumerate(leaves):
        # Replace the target leaf value with the corresponding rank
        line = line.replace(leaf, ranks[i])

    # Write the modified line back to the file
    with open(outtree, 'w') as file:
        file.write(line)
        
    return ranks

def tree_by_group(tree,group_refs,group_names):
    #read in Phylogenetic Tree
    tree_group_in = Tree(tree)
    #with this we make a pruned tree with only the reference per group. To be used as column sorter in heatmap
    tree_group_in.prune(group_refs)
    tree_group_in.ladderize()
    tree_group_in.write(format=5, outfile="groupref_tree.tree")

    with open('groupref_tree.tree', 'r') as file:
        content = file.read()

    # Replace items from ref_by_group with corresponding items from name_group
    for ref, name in zip(group_refs, group_names):
        content = content.replace(ref, name)

    # Write the modified contents back to the file
    with open('groupref_tree.tree', 'w') as file:
        file.write(content)
        
    tree_group_out = Tree('groupref_tree.tree')
    tree_group_leaves = tree_group_out.get_leaves()
    tree_group_leaves_sort = [node.name for node in tree_group_leaves]

    return tree_group_leaves_sort

def heatmap_v1(tax_level,tsv_file,group_leaf,tax_leaf):
    # Read the TSV file into a Pandas DataFrame
    group_leaf.append('Total')
    tax_leaf.append('Total')
    
    df = pd.read_csv(tsv_file, sep='\t')

    # Group by "group" and "order", and count occurrences
    grouped = df.groupby(['group', tax_level]).size().unstack(fill_value=0)

    # Ensure all taxa are included, even if they have zero occurrences
    all_taxa = df[tax_level].unique()
    grouped = grouped.reindex(columns=all_taxa, fill_value=0)

    # Add row and column totals
    grouped['Total'] = grouped.sum(axis=1)
    grouped.loc['Total'] = grouped.sum()
    grouped.sort_values(by='group', key=lambda column: column.map(lambda e: group_leaf.index(e)), inplace=True)
    grouped_T = grouped.T
    grouped_T.sort_values(by=tax_level, key=lambda column: column.map(lambda e: tax_leaf.index(e)), inplace=True)

    # Print or save the resulting DataFrame
    # If you want to save it to a new TSV file
    grouped_T.to_csv('count_seqs_per_' + tax_level +'_and_group.tsv', sep='\t')

    fig = px.imshow(grouped_T,
                    text_auto=True,
                    color_continuous_scale=[[0, 'white'], [0.05, 'yellow'], [0.25, 'purple'], [1, 'black']]
                )

    plt.offline.plot(fig, filename = in_filename + '_heatmap_' + tax_level + '.html', auto_open=False)

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Input file containing sequences and taxids (tab separated values). Must have columns 'seq' and 'taxids'", required=True)
parser.add_argument("--ext", default='*.txt', help="Extension of files containing groups sequences. All files with the extension will be processed", required=False)
parser.add_argument("--treemap", default='n', help="Plot the taxonomic tree map for each group (use y or n)", required=False)
parser.add_argument("--rank_color", default='order', help="Rank to color the tree map: Use group, class, superorder, order (default), family, subfamily or species", required=False)
parser.add_argument("--heatmap", default='n', help="Plot the heatmap for incidences by group and taxonomic rank", required=False)
parser.add_argument("--hmap_tree", default='training.tree', help="Phylogenetic tree of sequences in complete dataset (newick format required)", required=False)
parser.add_argument("--hmap_rank", default='species', help="Taxonomic level to show the results in the heatmap: Use group, class, superorder, order, family, subfamily or species (default)", required=False)

args = vars(parser.parse_args())
in_table = str(args["i"])
ext = str(args["ext"])
treemap = str(args["treemap"])
rank_color = str(args["rank_color"])
heatmap = str(args["heatmap"])
hmap_tree = str(args["hmap_tree"])
hmap_rank = str(args["hmap_rank"])


in_filename = in_table.split('.')[0]
output_file = in_filename + '_fulltax.tsv'

# To avoid overwriting the output file, remove it if it exists
if os.path.exists(output_file):
    os.remove(output_file)

# Generate the list of group files to read as input
if __name__ == "__main__":
    ext = '*.txt'  # Example file extension pattern
    file_sorter = FileSorter(ext)
    list_of_files = file_sorter.sort_files()

# Get complete taxonomy from taxids associated to each sequence in input tsv file
all_seqs, all_taxids, unique_taxids = get_unique_taxids(in_table)

# Build the dictionary with taxonomic rank information for each taxid
taxonomic_dict = taxid2dict(in_table,unique_taxids)
group_ref = []
group_name = []
for file in list_of_files:
    group_seqs = read_sequences_from_file(file)
    group_ref.append(group_seqs[0])
    group_name.append(file.split('.')[0])
    table_data = assign_taxonomic_info(file,group_seqs, all_seqs, all_taxids, taxonomic_dict)
    write_tabular_output(table_data, output_file)  


if treemap == 'y':
    df = pd.read_csv(output_file, sep='\t')
    fig_treemap = px.treemap(df, path=['group', 'class', 'subclass', 'superorder', 'order', 'family', 'subfamily','species'], 
                    color=rank_color,
                    color_discrete_map={'group':'darkgray',
                                        '(?)':'lightgray'})
    fig_treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    #fig_treemap.update_traces(marker=dict(cornerradius=2))

    plt.offline.plot(fig_treemap, filename = in_filename + '_treemap.html', auto_open=False)

if heatmap == 'y':
    taxon_leaf_name = tree_by_taxa(hmap_rank, unique_taxids)
    group_leaf_name = tree_by_group(hmap_tree, group_ref, group_name)
    heatmap_v1(hmap_rank,output_file,group_leaf_name,taxon_leaf_name)




