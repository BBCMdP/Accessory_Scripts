from Bio import SeqIO
from Bio import AlignIO
import A3MIO


input_handle = open("/home/fer/Dropbox/BBC/Transferase_superfamily/D22_001/2-tree_post_classification/1805_BAHD.faa", "rU")
output_handle = open("/home/fer/Dropbox/BBC/Transferase_superfamily/D22_001/2-tree_post_classification/1805_BAHD.a3m", "w")

alignments = AlignIO.parse(input_handle, "fasta")
AlignIO.write(alignments, output_handle, "a3m")

output_handle.close()
input_handle.close()
