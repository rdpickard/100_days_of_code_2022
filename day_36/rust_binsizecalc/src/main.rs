#![feature(int_log)]

extern crate num;
use chrono::Utc;


fn main() {
    let mut v: i128 = 618970019642690137449562111;

    let mut previous_v: i128 = 0;
    let mut i = 0;

    let start_time = Utc::now().time();

    while v != previous_v {
        previous_v = v;
        v |= v >> 1;
        i += 1;
    }

    v = v + 1;
    let end_time = Utc::now().time();
    let diff = end_time - start_time;

    println!("{}", v);
    println!("{}", v.log2());
    println!("{}", diff);

}
