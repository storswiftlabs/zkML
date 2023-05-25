// The 'decTreeGini' program.
import operators.leo;
program decTreeGini.aleo {
    // Save the one with the lowest Gini coefficient for each layer
    struct Candidate{
        gini: u32;
        label: u32;
    }
    struct Dataset {
        feature1: u32;
        feature2: u32;
    }
    struct TreeNode {
        node: u32;
        son_node_nums: u8;
        level: u8;
        weight: u16;
    }
    // key：Previous node; value: list. For example, [x,y], x number of people with jobs，y number of people are without jobs. 
    mapping gini_compute_input: u32 => Dataset;
    // key：Previous node; value：Candidate nodes and their Gini coefficients
    mapping gini_compute_output: u32 => Candidate;

    
    // Calculate Gini coefficients of two elements
    transition com_gini (public x: u32, public y: u32, public s: u32, preNode: u32, nowLabel: u32) -> u32 {
        let gini: u32 = 1u32 * s - operators.leo/my_square(operators.leo/my_divide(x, x+y, s), s) - operators.leo/my_square(operators.leo/my_divide(y, x+y, s), s);
        return gini then finalize(x, y, gini, preNode, nowLabel);
    }
    finalize com_gini(x: u32, y: u32, gini: u32, preNode: u32, nowLabel: u32) {
        // Publicly increment the number of agree votes.
        let candidate_init: Candidate = Candidate{gini: 0u32, label: 0u32};
        let candidate_map: Candidate = Mapping::get_or_init(gini_compute_output, preNode, candidate_init);
        // Find the smallest Gini coefficient as the node
        if (gini<candidate_map.gini){
            let next_node: Candidate = Candidate{gini: gini, label: nowLabel};
            Mapping::set(gini_compute_output, preNode, next_node);
        }
    }
}
