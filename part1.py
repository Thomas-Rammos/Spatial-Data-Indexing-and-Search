#RAMMOS THOMAS
#AM : 4583

import math
import sys

def read_data(filepath):
    # Ανοίγει το αρχείο για ανάγνωση
    with open(filepath, 'r') as file:
        # Διαβάζει τον αριθμό των σημείων από την πρώτη γραμμή
        num_points = int(file.readline().strip())
        coordinates = []
        # Διαβάζει κάθε γραμμή, εξάγει τις συντεταγμένες και αποθηκεύει τον αριθμό εγγραφής και τις συντεταγμένες
        for i, line in enumerate(file):
            x, y = map(float, line.strip().split())
            coordinates.append((i+1, (x, y)))  # Περιλαμβάνει το record-id αρχίζοντας από το 1
   
    
    return coordinates

def sort_data(coordinates):
    # Ταξινομεί τις συντεταγμένες βάσει του x
    return sorted(coordinates, key=lambda coord: coord[1][0])
    

def slice_data(sorted_coordinates):
    slices = []
    length_coord = len(sorted_coordinates)
    n = math.floor(1024/20)
    P = math.ceil(length_coord/n)
    S = math.ceil(math.sqrt(P))
    layer_size =  S * n
    # Διαχωρίζει τα δεδομένα σε τμήματα, καθένα με μέγεθος όσο το όριο των φύλλων
    for i in range(0, len(sorted_coordinates), layer_size):
        slices.append(sorted_coordinates[i:i + layer_size])
    return slices

def sort_slices_by_y(slices):
    # Ταξινομεί κάθε τμήμα βάσει του y
    for slice in slices:
        slice.sort(key=lambda coord: coord[1][1])
    return slices

def pack_nodes(slices, leaf=True):
    nodes = []
    node_id = 0
    n = math.floor(1024/20)
    
    # Δημιουργεί κόμβους από κάθε τμήμα
    for slice in slices:
        # Προσθέτει κάθε σημείο στον κόμβο
        for k in range(0, len(slice), n):
            node = {'id': node_id, 'records': [], 'leaf': leaf}
            temp_slices = slice[k:k+n]
            for i in range(len(temp_slices)):
                node['records'].append({'ptr': temp_slices[i][0], 'geo': temp_slices[i][1]})
            nodes.append(node)
            node_id += 1  # Αυξάνει το ID του κόμβου
    
    return nodes, node_id

def build_tree(node_id,levels,points_per_node):
    while len(levels[-1]) > 1:
        new_level = []
        current_nodes = levels[-1]
        #print(len(current_nodes))
        for i in range(0, len(current_nodes), points_per_node):
            children = current_nodes[i:i+points_per_node]
            geometries = [calculate_mbr([rec['geo'] for rec in child['records']])
                          for child in children]
           
            new_node = {
                'id': node_id,
                'records': [{'ptr': children[i]['id'], 'geo': geo} for (i, geo) in enumerate (geometries)],
                'leaf': False,
            }
                
            new_level.append(new_node)
            node_id += 1
        levels.append(new_level)

    return levels

def calculate_mbr(geometries):
    if(len(geometries[0]) == 2):
        # Υπολογίζει το Minimum Bounding Rectangle (MBR)
        min_x = min(geo[0] for geo in geometries)
        max_x = max(geo[0] for geo in geometries)
        min_y = min(geo[1] for geo in geometries)
        max_y = max(geo[1] for geo in geometries)
    else:
        min_x = min(geo[0] for geo in geometries)
        min_y = min(geo[1] for geo in geometries)
        max_x = max(geo[2] for geo in geometries)
        max_y = max(geo[3] for geo in geometries)
    return [min_x, min_y, max_x, max_y]

def write_output(levels,output_file):
    # Γράφει την έξοδο σε αρχείο
    with open(output_file, 'w') as file:
        root = levels[-1][0]['id']
        file.write(f"{root}\n")
        for level in levels:
            for node in level:
                node_info = ""
                if(len(node['records']) == 51):
                    node_info = f"{node['id']} , {len(node['records'])} , {0 if node['leaf'] else 1} , " + " , ".join([f"({rec['ptr']},{rec['geo']})" for rec in node['records']])
                else:
                    node_info = f"{node['id']} , {len(node['records'])} , {0 if node['leaf'] else 1} , " + " , ".join([f"({rec['ptr']},{rec['geo']})" for rec in node['records']])
                file.write(f"{node_info}\n")

def print_statistics(levels):
    print(f"Height of the tree: {len(levels)}")
    total_nodes = 0
    for i, level in enumerate(levels):
        node_count = len(level)
        total_nodes += node_count
        if level[0]['leaf']:  # Check if the level contains leaf nodes
            average_mbr_area = 0
        else:
            total_area = sum(
                (rec['geo'][2] - rec['geo'][0]) * (rec['geo'][3] - rec['geo'][1])  # Calculate area of each MBR
                for node in level for rec in node['records']
            )
            average_mbr_area = total_area / node_count  # Calculate average area of MBRs
        print(f"Level {i+1} - Number of Nodes: {node_count}, Average MBR Area: {average_mbr_area}")
    print(f"Total number of nodes: {total_nodes}")


def main():
    filepath = "Beijing_restaurants.txt" 
    output_file = sys.argv[1]

    points_per_leaf = 1024 // 20  # Κάθε σημείο χρησιμοποιεί 20 bytes
    points_per_node = 1024 // 36  # Κάθε MBR με node-id χρησιμοποιεί 36 bytes
    
    coordinates = read_data(filepath)
    sorted_coordinates = sort_data(coordinates)
    
    slices = slice_data(sorted_coordinates)
    
    sorted_slices = sort_slices_by_y(slices)
    
    leaf_nodes,current_node_id = pack_nodes(sorted_slices, leaf=True)
    all_levels = [leaf_nodes]
    complete_tree = build_tree(current_node_id,all_levels, points_per_node)
    write_output(complete_tree, output_file)
    print_statistics(complete_tree)

if __name__ == '__main__':
    main()
