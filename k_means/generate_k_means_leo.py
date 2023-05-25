def generate_input_file(centers, dataset, path):
    str_list_inputs = []
    str_list_inputs.append("[main]")
    generate_dataset_struct(dataset, str_list_inputs)
    generate_centers_struct(centers, str_list_inputs)
    with open(path, "w+") as file:
        for line in str_list_inputs:
            file.write(line+"\n")
def generate_dataset_struct(dataset, str_list_inputs):
    str_list_inputs.append("public dataset: Axis =  Axis{")
    str_list_inputs.append("    x: "+str(int(dataset[0]*1000))+"i32,")
    str_list_inputs.append("    y: "+str(int(dataset[1]*1000))+"i32,")
    str_list_inputs.append("};")

def generate_centers_struct(centers, str_list_inputs):
    str_list_inputs.append("public centers: KMeansCenters = KMeansCenters {")
    for index, point in enumerate(centers):
        str_list_inputs.append("    e"+str(index)+":  Axis{")
        str_list_inputs.append("        x: "+str(int(point[0]*1000))+"i32,")
        str_list_inputs.append("        y: "+str(int(point[1]*1000))+"i32,")
        str_list_inputs.append("    },")
    str_list_inputs.append("};")


# ==================inputs file generate ↑===============  
# ====================main file generate ↓===============   
def generate_main_file(centers, dataset, path):
    str_list_inputs = []
    str_list_inputs.append("program kMeans.aleo {" )
    generate_struct(centers, dataset, str_list_inputs)
    generate_transition(centers, str_list_inputs)
    str_list_inputs.append("}")
    with open(path, "w+") as file:
        for line in str_list_inputs:
            file.write(line+"\n")

def generate_struct(centers, dataset, str_list_inputs):
    str_list_inputs.append("    struct Axis{" )
    str_list_inputs.append("        x: i32;" )
    str_list_inputs.append("        y: i32;" )
    str_list_inputs.append("    }" )
    str_list_inputs.append("    struct KMeansCenters {" )
    for index, _ in enumerate(centers):
        str_list_inputs.append("        e"+str(index)+": Axis;" )
    str_list_inputs.append("    }" )
    
def generate_transition(centers, str_list_inputs):
    str_list_inputs.append("    transition main(public dataset: Axis, centers: KMeansCenters) -> u32 {" )
    for index in range(len(centers)):
        str_list_inputs.append("        let e"+str(index)+": i32 = (centers.e"+str(index)+".x-dataset.x)**2u32 + (centers.e"+str(index)+".y-dataset.y)**2u32;" )
    str_list_inputs.append("        let min_ele_index:u32 = 0u32;")
    for index in range(len(centers)-1):
        str_list_inputs.append("        if (e"+str(index)+" > e"+str(index+1)+"){")
        str_list_inputs.append("            min_ele_index = "+str(index+1)+"u32;")
        str_list_inputs.append("        }else{")
        str_list_inputs.append("            min_ele_index = "+str(index)+"u32;")
        str_list_inputs.append("        }")
    str_list_inputs.append("        return min_ele_index;")

    str_list_inputs.append("    }" )
    

# output leo file path
input_path = "./kMeans/inputs/kMeans.in"
main_path = "./kMeans/src/main.leo"

# Normal test case from k_means.py
dataset = [2,6] # New point to be predicted
centers = [[1.167,1.467], [7.333, 9]] # Each central point cluster

# Generate leo code
generate_input_file(centers, dataset, input_path)
generate_main_file(centers, dataset, main_path)