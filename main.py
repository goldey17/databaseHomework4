#Get user input via command line
user_input = raw_input("Please enter input: ")
field = user_input[:user_input.index(",")].strip()
user_input = user_input[user_input.index(",") + 1:]
value = user_input[:user_input.index(",")].strip()
user_input = user_input[user_input.index(",") + 1:]
storage_path = user_input[:user_input.index(",")].strip()
user_input = user_input[user_input.index(",") + 1:]
line_number = user_input.strip()
print(field)
print(value)
print(storage_path)
print(line_number)

#See if field has a corresponding XML file if not create it
f = open(field + ".xml","r+")
#Read from the file to see if the file is empty
if f.mode == 'r':
    contents = f.read()
    try:
        contents.index("xml")
        file_empty = False
    except:
        file_empty = True

#If the file is empty start the tree
f = open(field + ".xml", "w")
f.write('<?xml version="1.0" encoding="UTF-8"?>')
f.write("/n")

#Make a B+ tree


#If the file is not empty read the file and put it into a List


def make_nodes_into_xml(node):
    #If there are no children
    if(node.left_nodes is None and node.right_nodes is None):
        #set name
        xml = "<" + node.name + 'path = "' + node.path + '" row = "' + node.row + '"> /n'
        #set blank left and right nodes
        xml += "<leftNodes>/n"
        xml += "</leftNodes>/n"
        xml += "<rightNodes>/n"
        xml += "</rightNodes>/n"
        #set end of the name
        xml += "</" + node.name + ">/n"
    #If there are children
    else:
        # set name
        xml = "<" + node.name + 'path = "' + node.path + '" row = "' + node.row + '"> /n'
        # set blank left and right nodes
        xml += "<leftNodes>/n"
        xml += make_nodes_into_xml(node.left_nodes)
        xml += "</leftNodes>/n"
        xml += "<rightNodes>/n"
        xml += make_nodes_into_xml(node.right_nodes)
        xml += "</rightNodes>/n"
        # set end of the name
        xml += "</" + node.name + ">/n"
    return xml

class B_Tree_Node(object):
    left_nodes = []
    right_nodes = []
    name = ""
    path = ""
    row = -1

    def __init__(self, name, path, row):
        self.name = name
        self.path = path
        self.row = row

