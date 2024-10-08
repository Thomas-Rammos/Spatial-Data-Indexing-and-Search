# Spatial-Data-Indexing-and-Search
This project implements spatial data indexing and search techniques using R-trees for a dataset of restaurant locations in Beijing. The project is divided into two parts: constructing an R-tree using the Sort-Tile-Recursive (STR) method and performing a best-first nearest neighbor search on the tree.
# Part 1: Constructing an R-tree
The first part involves building an R-tree to index spatial data from a dataset containing the coordinates of 51,970 restaurants in Beijing. The STR technique is used to recursively divide the data into tiles and sort them to build the tree. Each leaf node stores entries of the form <record-id, point>, while non-leaf nodes store entries of the form <node-id, MBR>.
- Code file: part1.py
- Input: The file Beijing_restaurants.txt containing restaurant coordinates​(Beijing_restaurants).
- Output: The R-tree structure is written to an output file. The root node ID is saved on the first line, followed by lines representing each node with the format:
  - node-id, n, f, (ptr1, geo1), (ptr2, geo2), …, (ptrn, geon)
    
  where n is the number of records in the node, f is 0 or 1 depending on whether the node is a leaf or not, and each entry consists of a pointer (node ID or record ID) and geometric            information (coordinates or MBR). The program also prints statistics about the tree, including height, the number of nodes at each level, and the average area of MBRs at each level.


# Part 2: Best-First Nearest Neighbor Search
In the second part, the program performs a best-first nearest neighbor (BFNN) search on the R-tree created in Part 1. The search finds the k nearest neighbors, k+1 nearest neighbors, and k+2 nearest neighbors for a given query point, printing the ID, coordinates, and distance of each neighbor.

- Code file: part2.py
- Input: The R-tree output file from Part 1, the query point coordinates, and the number of nearest neighbors (k)​(part2).
- Output: The program outputs the k, k+1, and k+2 nearest neighbors, as well as the state of the priority queue at the time of finding each neighbor.
# Instructions
  1. Part 1: Run part1.py to build the R-tree. Example: python part1.py output_tree.txt

  2. Part 2: Run part2.py to perform the nearest neighbor search. Example: python part2.py output_tree.txt 39.9 116.4 5 (Finds the 5 nearest neighbors to the point (39.9, 116.4)).

# Notes
- The program assumes that the input file Beijing_restaurants.txt is formatted with one restaurant’s coordinates per line, following an initial line specifying the number of records.
- The R-tree is built entirely in memory, and no external sorting is required.
