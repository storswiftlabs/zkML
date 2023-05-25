def generate_input_file(tree_dict, dataset, label, path):
    # generate tree
    # Tree instance by dict {'haveHouse': {0: {'haveJob': {0: 'no', 1: 'yes'}}, 1: 'yes'}}
    str_list_inputs = []
    str_list_inputs.append("[main]\n")
    # generate_tree_struct(tree_dict, str_list_inputs, label)
    generate_dataset_struct(dataset, str_list_inputs)
    
    with open(path, "w+") as file:
        for line in str_list_inputs:
            file.write(line+"\n")

def generate_tree_struct(tree_dict, str_list_inputs, label: list):
    tree_type = get_tree_type(tree)
    str_list_inputs.append("public tree: "+tree_type+" = "+tree_type+" {")
    dict_to_input(tree_dict, str_list_inputs, label)
    str_list_inputs.append("};")

def dict_to_input(tree_dict, str_list_inputs, label: list):
    node_name = "node_name"
    left_str = "left"
    right_str = "right"
    for k, v in tree_dict.items():
        if k == 'label':
            head_node_name = str(label.index(v))  # is index
            str_list_inputs.append("    "+node_name+": "+head_node_name+"u8,")
        if k == 1:
            if type(v) is dict:
                tree_type = get_tree_type(v)
                str_list_inputs.append("    "+left_str+": "+tree_type+"{")
                dict_to_input(v, str_list_inputs, label)
                str_list_inputs.append("},")
            else:
                if v == 0:
                    v= "false"
                else:
                    v= "true"
                str_list_inputs.append("    "+left_str+": "+v+",")
        elif k == 0 :
            if type(v) is dict:
                tree_type = get_tree_type(v)
                str_list_inputs.append("    "+right_str+": "+tree_type+"{")
                dict_to_input(v, str_list_inputs, label)
                str_list_inputs.append("},")
            else:
                if v == 0:
                    v= "false"
                else:
                    v= "true"
                str_list_inputs.append("    "+right_str+": "+v+",") 

def generate_dataset_struct(dataset, str_list_inputs):
    str_list_inputs.append("public dataset: Dataset = Dataset {")
    for index,ele in enumerate(dataset):
        str_list_inputs.append("    e"+str(index)+": "+str(ele)+"u32,")
    str_list_inputs.append("};")

# ==================inputs file generate ↑===============  
# ==================  main file generate ↓===============   

def generate_main_file(tree: dict, dataset, label, path) :
    str_list_inputs = []
    str_list_inputs.append("program classify.aleo {" )
    generate_struct_by_tree(tree, str_list_inputs, dataset)
    generate_transition(tree, str_list_inputs, label)
    str_list_inputs.append("}")
    with open(path, "w+") as file:
        for line in str_list_inputs:
            file.write(line+"\n")

def generate_struct_by_tree(tree: dict, str_list_inputs, dataset):
    diff_node_list: list = []
    get_diff_node(tree, diff_node_list)
    print("debug:get_diff_node list is", diff_node_list)
    for index, ele in enumerate(diff_node_list):
        if ele in diff_node_list[:index]:
            continue;
        if ele == 0:
            generate_endless_node(str_list_inputs)
        elif ele == 1:
            generate_one_son_node(str_list_inputs, diff_node_list[index-1])
        elif ele >= 2:
            generate_n_son_node(str_list_inputs, diff_node_list[index-2], diff_node_list[index-1], n=2)

    generate_dataset_static_struct(str_list_inputs, dataset)

def get_tree_type(tree: dict):
    tree_type = 0
    for _, value in tree.items():
        if type(value) is dict:
            tree_type+=1
    if tree_type >= 2:
        tree_type = "SonNode2"
    elif tree_type == 1:
        tree_type = "OneSonNode"
    elif tree_type == 0:
        tree_type = "EndlessNode"
    return tree_type

def generate_transition(tree: dict, str_list_inputs, label: list):
    tree_type = get_tree_type(tree)
    str_list_inputs.append("    transition main(public dataset: Dataset) -> bool {")
    flat_dict_tree(tree,str_list_inputs,label)

def flat_dict_tree(tree,str_list_inputs,label):
    for key, value in tree.items():
        if key == 'label':
            label_index = label.index(value)
            str_list_inputs.append("    if (dataset.e"+str(label_index)+" == 0u32) {")
            if type(tree.get(0)) is dict:
                flat_dict_tree(tree.get(0),str_list_inputs,label)
            else:
                # str_list_inputs.append("    }else{")
                if tree.get(0) is 0:
                    str_list_inputs.append("            return false;")
                else:
                    str_list_inputs.append("            return true;")
                str_list_inputs.append("    }")

            if type(tree.get(1)) is dict:
                flat_dict_tree(tree.get(1),str_list_inputs,label)
            else:
                # str_list_inputs.append("    }else{")
                if tree.get(1) is 0:
                    str_list_inputs.append("    return false;")
                else:
                    str_list_inputs.append("    return true;")
                str_list_inputs.append("    }")

def generate_dataset_static_struct(str_list_inputs, dataset):
    str_list_inputs.append("    struct Dataset {")
    for index,_ in enumerate(dataset):
        str_list_inputs.append("        e"+str(index)+": "+"u32,")
    str_list_inputs.append("    }")

def get_diff_node(tree, diff_node_list):
    node2_num = 0
    for k, v in tree.items():
        if type(v) is dict:
            node2_num+=1
            get_diff_node(v, diff_node_list)
    diff_node_list.append(node2_num) 

def generate_endless_node(str_list_inputs):
    str_list_inputs.append("    struct EndlessNode {")
    str_list_inputs.append("        node_name: "+"u8;")
    str_list_inputs.append("        right: "+"bool;")
    str_list_inputs.append("        left: "+"bool;")
    str_list_inputs.append("    }")
    
def generate_one_son_node(str_list_inputs, right_type):
    if right_type == 0:
        right_type = "EndlessNode"
    elif right_type == 1:
        right_type = "OneSonNode"
    elif right_type >= 2:
        right_type = "SonNode"+str(right_type)
    str_list_inputs.append("    struct OneSonNode {")
    str_list_inputs.append("        node_name: "+"u8;")
    str_list_inputs.append("        right: "+right_type+";")
    str_list_inputs.append("        left: "+"bool;")
    str_list_inputs.append("    }")

# TODO As the number of child nodes increases, new nodes need to be generated
def generate_n_son_node(str_list_inputs, left_type, right_type, n):
    print("debug", left_type, right_type, n)
    if left_type == 0:
        left_type = "EndlessNode"
    elif left_type == 1:
        left_type = "OneSonNode"
    elif left_type >= 2:
        left_type = "SonNode"+str(left_type)
    if right_type == 0:
        right_type = "EndlessNode"
    elif right_type == 1:
        right_type = "OneSonNode"
    elif right_type >= 2:
        right_type = "SonNode"+str(right_type)
    str_list_inputs.append("    struct SonNode"+str(n)+" {")
    str_list_inputs.append("        node_name: "+"u8;")
    str_list_inputs.append("        right: "+right_type+";")
    str_list_inputs.append("        left: "+left_type+";")
    str_list_inputs.append("    }")


# output leo file path
input_path = "./classify/inputs/classify.in"
main_path = "./classify/src/main.leo"

# Normal test case from dt.py 
# dataset and label corresponded one by one, 0 was false, 1 was true,  and the decision tree was represented by dict
dataset = [0, 0]
tree: dict = {'label': 'haveHouse',0: {'label': 'haveJob', 0: 0, 1: 1}, 1: 1}
label = ['haveHouse', 'haveJob']

# Complex test case
# tree: dict = {'label': 'haveHouse', 0: {'label': 'haveJob',0: {'label': 'isLegalPerson', 0:{'label': ' isAssetBalanceSatisfied', 0:0, 1:1},1:{'label': 'isEgisteredCapitaSatisfied', 0:0, 1:1}}, 1: 1}, 1:  {'label':'isHousesSatisfied',0: 0, 1: 1}}
# dataset = [0, 0, 1, 1, 1, 1]
# label = ['haveHouse', 'haveJob', 'isHousesSatisfied', 'isLegalPerson', ' isAssetBalanceSatisfied', 'isEgisteredCapitaSatisfied']

# Generate leo code
generate_input_file(tree, dataset, label, input_path)
generate_main_file(tree, dataset, label, main_path)

# import subprocess
# p1 = subprocess.run("cd classify/")
# p2 = subprocess.run("leo run main")
# print(p2)