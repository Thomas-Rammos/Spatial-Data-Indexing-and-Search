# Spatial-Data-Indexing-and-Search
This project implements spatial data indexing and search techniques using R-trees for a dataset of restaurant locations in Beijing. The project is divided into two parts: constructing an R-tree using the Sort-Tile-Recursive (STR) method and performing a best-first nearest neighbor search on the tree.
# Part 1: Constructing an R-tree
The first part involves building an R-tree to index spatial data from a dataset containing the coordinates of 51,970 restaurants in Beijing. The STR technique is used to recursively divide the data into tiles and sort them to build the tree. Each leaf node stores entries of the form <record-id, point>, while non-leaf nodes store entries of the form <node-id, MBR>.
- Code file: part1.py
- Input: The file Beijing_restaurants.txt containing restaurant coordinates​(Beijing_restaurants).
- Output: The R-tree structure is written to an output file. The root node ID is saved on the first line, followed by lines representing each node with the format:
  - node-id, n, f, (ptr1, geo1), (ptr2, geo2), …, (ptrn, geon)
  where n is the number of records in the node, f is 0 or 1 depending on whether the node is a leaf or not, and each entry consists of a pointer (node ID or record ID) and geometric            information (coordinates or MBR)​(Assignment2). The program also prints statistics about the tree, including height, the number of nodes at each level, and the average area of MBRs at each level.
