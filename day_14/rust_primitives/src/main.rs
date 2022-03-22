fn main() {
    let logical: bool = true;

    let a_float: f64 = 1.0;
    let an_integer = 5i32;

    let default_float = 3.0;
    let default_integer = 7;

    let mut inferred_type = 12;
    inferred_type = 4294967296i64;

    let mut mutable = 12;
    mutable = 21;

    // intentional error to show types cant be changed without 'shadowing'
    //mutable = true;

    // Shadowing. More on this in chapter 4
    // https://doc.rust-lang.org/rust-by-example/variable_bindings/scope.html
    let mutable = true;

    println!("1 + 2 = {}", 1u32 + 2);

    // Unsigned integer so this will overflow
    //println!("1 - 2 = {}", 1u32 - 2);

    println!("1 - 2 = {}", 1i32 - 2);

    println!("ture and false is {}", true && false);
    println!("true or false is {}", true || false);
    println!("NOT true is {}", !true);

    println!("0011 AND 0101 is {:04b}", 0b0011u32 & 0b0101);
    println!("0011 OR 0101 is {:04b}", 0b0011u32 | 0b0101);
    println!("0011 XOR 0101 is {:04b}", 0b0011u32 ^ 0b0101);
    println!("1 << 5 is {}", 1u32 << 5);
    println!("0x80 >> 2 is 0x{:x}", 0x80u32 >> 2);

    println!("One million is written as {}", 1_000_000u32);



}
