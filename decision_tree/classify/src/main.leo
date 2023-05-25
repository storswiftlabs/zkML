program classify.aleo {
    struct EndlessNode {
        node_name: u8;
        right: bool;
        left: bool;
    }
    struct OneSonNode {
        node_name: u8;
        right: EndlessNode;
        left: bool;
    }
    struct Dataset {
        e0: u32,
        e1: u32,
    }
    transition main(public dataset: Dataset) -> bool {
    if (dataset.e0 == 0u32) {
    if (dataset.e1 == 0u32) {
            return false;
    }
    return true;
    }
    return true;
    }
}
