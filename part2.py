#RAMMOS THOMAS
#AM : 4583

import math
import heapq
import re
import argparse

def parse_lines(filepath):
    data_tree = []
    with open(filepath, 'r') as file:
        root_id = int(next(file).strip())  # The first line contains the root node ID
        
        for line in file:
            # First split the line into node attributes and records
            parts = line.split(', ', 3)
            node_id = int(parts[0])
            num_records = int(parts[1])
            is_leaf = int(parts[2])
            records_str = parts[3]
            
            # Regular expression to match both points and MBRs
            pattern = r'\((\d+),\s*(\[[^\]]+\]|\([^\)]+\))\)'
            records = re.findall(pattern, records_str)
            
            parsed_records = []
            for record in records:
                record_id, coord_str = record
                record_id = int(record_id)
                              
                # Determine if it's a point or MBR by checking for brackets
                if coord_str.startswith('['):
                    coords = tuple(map(float, re.findall(r'\d+\.\d+', coord_str.strip('[]'))))
                else:
                    coords = tuple(map(float, re.findall(r'\d+\.\d+', coord_str.strip('()'))))
                
                parsed_records.append({'record_id': record_id, 'coords': coords})
            
            data_tree.append({
                'node_id': node_id,
                'num_records': num_records,
                'is_leaf': is_leaf,
                'records': parsed_records
            })
    
    return data_tree, root_id


def mindist(q, mbr):
    # Calculate the mindist from the query point q to the MBR.
    # q is a tuple (qx, qy)
    # mbr is a tuple (min_x, min_y, max_x, max_y)
    qx, qy = q
    min_x, min_y, max_x, max_y = mbr
    dx = max(min_x - qx, 0, qx - max_x)
    dy = max(min_y - qy, 0, qy - max_y)
    return math.sqrt(dx**2 + dy**2)

def euclidean_distance(q, p):
    # Calculate the Euclidean distance between two points q and p.
    qx, qy = q
    px, py = p
    return math.sqrt((qx - px)**2 + (qy - py)**2)

def bfnn(heap, nearest_neighbors,query_point, r_tree, root_id, k):
    
    
    #if the heap is empty this is the start of the algorithm
    if (len(heap)==0):
        # Add all the root node entries to the heap
        root_node = r_tree[root_id]  # assuming root_id is 1-indexed
        
        for entry in root_node['records']:
            # Use mindist for non-leaf nodes
            dist = mindist(query_point, entry['coords'])
            heapq.heappush(heap, (dist, entry['record_id'], entry['coords'], 1))
        
    # Continue the search until we've found k nearest neighbors
    while heap and len(nearest_neighbors)<k:
        dist, node_id, coords, node_type = heapq.heappop(heap)
 
        if node_type == 0:
            nearest_neighbors.append((node_id, coords ,dist))
            print(f"Heap status: {[heap_item[:3] for heap_item in heap]}")
        else:
            node = r_tree[node_id]  # Node IDs are assumed to be 1-indexed
            # If it's not a leaf node, we enqueue its children
            for child in node['records']:
                if len(child["coords"]) == 2:
                    child_dist = euclidean_distance(query_point, child['coords'])
                    heapq.heappush(heap, (child_dist, child['record_id'], child["coords"],0))
                else:
                    child_dist = mindist(query_point, child['coords'])
                    heapq.heappush(heap, (child_dist, child['record_id'], child["coords"],1))
                    
    return heap,nearest_neighbors



def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='BFNN search on an R-tree')
    parser.add_argument('tree_file', type=str, help='Path to the file containing the R-tree')
    parser.add_argument('query_x', type=float, help='X coordinate of the query point')
    parser.add_argument('query_y', type=float, help='Y coordinate of the query point')
    parser.add_argument('k', type=int, help='Number of nearest neighbors to find')

    # Parse the command line arguments
    args = parser.parse_args()

    # Load the R-tree from the specified file
    tree, root_id = parse_lines(args.tree_file)  # Ensure parse_lines is defined to read the tree file
    query_point = (args.query_x, args.query_y)  # The query point from command line
    k = args.k  # The number of nearest neighbors to find from command line
    
    heap = []
    nearest_neighbors = []
    # Run the BFNN search
    heap,nearest_neighbors = bfnn(heap,nearest_neighbors,query_point, tree, root_id, k)
    #k+1
    heap,nearest_neighbors = bfnn(heap,nearest_neighbors,query_point, tree, root_id, k+1)
    #k+2
    heap,nearest_neighbors = bfnn(heap,nearest_neighbors,query_point, tree, root_id, k+2)
    # Print the k nearest neighbors
    print("\nK-Nearest neighbors:")
    for i,neighbor in enumerate (nearest_neighbors):
        print(f"ID: {neighbor[0]}, Distance: {neighbor[2]}, Coordinates: {neighbor[1]}")
        if(i==k-1):
            print("K+1-Nearest neighbor:")
        if(i==k):
            print("K+2-Nearest neighbor:")

if __name__ == '__main__':
    main()