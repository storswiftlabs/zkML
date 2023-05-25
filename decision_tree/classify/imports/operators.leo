// The 'operators' program.
program operators.aleo {
    transition main(public a: u32, b: u32) -> u32 {
        let c: u32 = a + b;
        return c;
    }
    transition my_add(a: u32, b: u32) -> u32 {
        let result: u32 = a + b;
        return result;
    }

    transition my_multiply(a: u32, b: u32, s: u32) -> u32 {
        let result: u32 = a * b / s;
        return result;
    }

    transition my_divide(a: u32, b: u32, s: u32) -> u32 {
        let result: u32 = s * a / b;
        return result;
    }

    transition my_square(a: u32, s: u32) -> u32 {
        let result: u32 = a * a / s;
        return result;
    }
}
