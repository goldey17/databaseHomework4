# Turn the nodes into xml
def make_nodes_into_xml(node, level):
    # If there is no node
    if node is None:
        return ""
    # If there are no children
    xml = ""
    if node.left_nodes is None and node.right_nodes is None:
        for x in range(0, level):
            xml += "\t"
        # set name
        xml += "<" + node.name + ' path = "' + node.path + '" row = "' + node.row + '"> \n'
        # set blank left and right nodes
        for x in range(0, level + 1):
            xml += "\t"
        xml += "<leftNodes>\n"
        for x in range(0, level + 1):
            xml += "\t"
        xml += "</leftNodes>\n"
        for x in range(0, level + 1):
            xml += "\t"
        xml += "<rightNodes>\n"
        for x in range(0, level + 1):
            xml += "\t"
        xml += "</rightNodes>\n"
        # set end of the name
        for x in range(0, level):
            xml += "\t"
        xml += "</" + node.name + ">\n"
    # If there are children
    else:
        # set name
        for x in range(0, level):
            xml += "\t"
        xml += "<" + node.name + ' path = "' + node.path + '" row = "' + node.row + '"> \n'
        # set blank left and right nodes
        for x in range(0, level + 1):
            xml += "\t"
        xml += "<leftNodes>\n"
        xml += make_nodes_into_xml(node.left_nodes, level + 1)
        for x in range(0, level + 1):
            xml += "\t"
        xml += "</leftNodes>\n"
        for x in range(0, level + 1):
            xml += "\t"
        xml += "<rightNodes>\n"
        xml += make_nodes_into_xml(node.right_nodes, level + 1)
        for x in range(0, level + 1):
            xml += "\t"
        xml += "</rightNodes>\n"
        # set end of the name
        for x in range(0, level):
            xml += "\t"
        xml += "</" + node.name + ">\n"
    return xml


# Turn the xml into nodes
def make_xml_into_nodes(file_to_read, node, side):
    # If this is the first time reading the file
    if node is None:
        # Read the first line and make sure its an xml file
        line = file_to_read.readline()
        try:
            line.index("xml")
        except ValueError:
            print "Not a valid xml file"
    # Get a line to find the data of the node
    line = file_to_read.readline()
    # Get the name, path, and row
    try:
        line.index("<")
        name = line[line.index("<") + 1:line.index("path")].strip()
    except ValueError:
        name = line[:line.index("path")].strip()
    path = line[line.index('path = "') + 8:line.index('" row')].strip()
    row = line[line.index('row = "') + 7:line.index('">')].strip()
    # Set the node to the corresponding part of the tree
    if node is None:
        node = BTreeNode(name, path, row)
    elif side == "Left":
        node.left_nodes = BTreeNode(name, path, row)
    elif side == "Right":
        node.right_nodes = BTreeNode(name, path, row)
    # Get the next line and make sure its a left node
    line = file_to_read.readline()
    try:
        line.index("<leftNodes>")
    except ValueError:
        print "Not a valid xml file"
    # See if there is a leftNode
    line = file_to_read.readline()
    try:
        line.index("</leftNodes>")
        # No left node
    except ValueError:
        file_to_read.seek(-len(line), 1)
        # If there is a left node recall the function on the corresponding node
        if side == "":
            make_xml_into_nodes(file_to_read, node, "Left")
        elif side == "Left":
            make_xml_into_nodes(file_to_read, node.left_nodes, "Left")
        elif side == "Right":
            make_xml_into_nodes(file_to_read, node.right_nodes, "Left")
        line = file_to_read.readline()
        line = file_to_read.readline()
    # Get the next line and make sure its a right node
    line = file_to_read.readline()
    try:
        line.index("<rightNodes>")
    except ValueError:
        print "Not a valid xml file"
    # See if there is a rightNode
    line = file_to_read.readline()
    try:
        line.index("</rightNodes>")
        # No right node
    except ValueError:
        file_to_read.seek(-len(line), 1)
        # If there is a right node recall the function on the corresponding node
        if side == "":
            make_xml_into_nodes(file_to_read, node, "Right")
        elif side == "Left":
            make_xml_into_nodes(file_to_read, node.left_nodes, "Right")
        elif side == "Right":
            make_xml_into_nodes(file_to_read, node.right_nodes, "Right")
        line = file_to_read.readline()
        line = file_to_read.readline()
    return node


# Place a new node into the tree in the right spot
def place_new_node(node, new):
    # Find the name of the node and see if my node is greater than, less than, or equal
    if len(node.name) > len(new.name):
        max_value = len(new.name)
    else:
        max_value = len(node.name)
    for x in range(0, max_value - 1):
        # Node should go left
        if node.name[x] > new.name[x]:
            # If empty place the node
            if node.left_nodes is None:
                node.left_nodes = new
                break
            else:
                node.left_nodes = place_new_node(node.left_nodes, new)
                break
        # Node should go right
        elif node.name[x] < new.name[x]:
            # If empty place the node
            if node.right_nodes is None:
                node.right_nodes = new
                break
            else:
                node.right_nodes = place_new_node(node.right_nodes, new)
                break
        # Else look at next letter
    return node


class BTreeNode(object):
    left_nodes = None
    right_nodes = None
    name = ""
    path = ""
    row = -1

    def __init__(self, name, path, row):
        self.name = name
        self.path = path
        self.row = row

# Ask user if command line or csv file
user_input = raw_input("Are you using a file or command line: ")
try:
    user_input.index("file")
    user_input = raw_input("Please enter file name: ")
    f = open(user_input, "r")
    content = f.readlines()
    for item in content:
        # Get user input via command line
        field = item[:item.index(",")].strip()
        item = item[item.index(",") + 1:]
        value = item[:item.index(",")].strip()
        item = item[item.index(",") + 1:]
        storage_path = item[:item.index(",")].strip()
        item = item[item.index(",") + 1:]
        line_number = item.strip()
        # See if field has a corresponding XML file if not create it
        f = open(field + ".xml", "a")
        f.close()
        # Read from the file to see if the file is empty
        file_empty = False
        f = open(field + ".xml", "r")
        contents = f.read()
        f.close()
        try:
            contents.index("xml")
            file_empty = False
        except ValueError:
            file_empty = True
        # If the file is empty start the tree
        if file_empty:
            f = open(field + ".xml", "w")
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
            f.write("\n")
            nodes = BTreeNode(value, storage_path, line_number)
            result = make_nodes_into_xml(nodes, 0)
            f.write(result)
            f.close()
        # If the file is not empty read the file and make it into nodes
        else:
            f = open(field + ".xml", "r")
            nodes = make_xml_into_nodes(f, None, "")
            f.close()
            # Add the node to the tree
            new_node = BTreeNode(value, storage_path, line_number)
            nodes = place_new_node(nodes, new_node)
            # Save the tree in xml
            f = open(field + ".xml", "w")
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
            f.write("\n")
            result = make_nodes_into_xml(nodes, 0)
            f.write(result)
            f.close()
except ValueError:
    # Get user input via command line
    user_input = raw_input("Please enter input: ")
    field = user_input[:user_input.index(",")].strip()
    user_input = user_input[user_input.index(",") + 1:]
    value = user_input[:user_input.index(",")].strip()
    user_input = user_input[user_input.index(",") + 1:]
    storage_path = user_input[:user_input.index(",")].strip()
    user_input = user_input[user_input.index(",") + 1:]
    line_number = user_input.strip()
    # See if field has a corresponding XML file if not create it
    f = open(field + ".xml", "a")
    f.close()
    # Read from the file to see if the file is empty
    file_empty = False
    f = open(field + ".xml", "r")
    contents = f.read()
    f.close()
    try:
        contents.index("xml")
        file_empty = False
    except ValueError:
        file_empty = True
    # If the file is empty start the tree
    if file_empty:
        f = open(field + ".xml", "w")
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write("\n")
        nodes = BTreeNode(value, storage_path, line_number)
        result = make_nodes_into_xml(nodes, 0)
        f.write(result)
        f.close()
    # If the file is not empty read the file and make it into nodes
    else:
        f = open(field + ".xml", "r")
        nodes = make_xml_into_nodes(f, None, "")
        f.close()
        # Add the node to the tree
        new_node = BTreeNode(value, storage_path, line_number)
        nodes = place_new_node(nodes, new_node)
        # Save the tree in xml
        f = open(field + ".xml", "w")
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write("\n")
        result = make_nodes_into_xml(nodes, 0)
        f.write(result)
        f.close()
