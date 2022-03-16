

fn calculate_legendre(p: u64, n: u64) -> i32 {

    let legendre ;

    // in test p==23, n==17 I got an overflow when vars were u32. IDE suggested this cast.
    // not convinced that is the right thing to do
    let residue = n.pow(((p - 1) / 2) as u32) % p;

    if residue == 1 {
        legendre = 1;
    } else if residue == 0 {
        legendre = 0;
    } else {
        legendre = -1
    }

    return legendre
}


fn tonelli_shanks(p: u64, n: u64) -> u64 {

    assert_eq!(calculate_legendre(p, n), 1, "Legendre value not equal to 1");

    let mut q = p -1;
    let mut z:u64 = 0;
    let mut s = 0;

    while q % 2 == 0 {
        q = q / 2;
        s = s + 1;
    }
    if s == 1 {
        return n.pow(((p + 1) / 4) as u32) % p;
    }
    for zed in 2..p+1 {
        if p - 1 == n.pow(((p - 1) / 2) as u32) % p {
            z = zed;
            break
        }
    }

    let mut c = z.pow(q as u32) % p;
    let mut r = n.pow(((q+1)/2) as u32) % p;
    let mut t = n.pow(q as u32) % p;

    let mut m = s;
    let mut t2 = 0;
    let mut b = 0;
    let mut k = 0;

    while t > 1 && (t - 1) % p != 0 {
        t2 = (t * t) % p;
        for i in 1..m+1 {
            if (t2 - 1) % p == 0 {
                k = i;
                break;
            }
            t2 = (t2 * t2) % p;
        }

        println!("m {} k {}", m, k);
        b = c.pow( 2u32.pow(m-k-1 as u32) as u32) % p;
        r = (r * b) % p;
        c = (b * b) % p;
        t = (t * c) % p;
        println!("T AGAIN {}", t);
        m = k;
    }

    return r;
}

fn main() {
    println!("{}", tonelli_shanks(101, 56));
}
