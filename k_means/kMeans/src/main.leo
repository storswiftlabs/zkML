program kMeans.aleo {
    struct Axis{
        x: i32;
        y: i32;
    }
    struct KMeansCenters {
        e0: Axis;
        e1: Axis;
    }
    transition main(public dataset: Axis, centers: KMeansCenters) -> u32 {
        let e0: i32 = (centers.e0.x-dataset.x)**2u32 + (centers.e0.y-dataset.y)**2u32;
        let e1: i32 = (centers.e1.x-dataset.x)**2u32 + (centers.e1.y-dataset.y)**2u32;
        let min_ele_index:u32 = 0u32;
        if (e0 > e1){
            min_ele_index = 1u32;
        }else{
            min_ele_index = 0u32;
        }
        return min_ele_index;
    }
}
