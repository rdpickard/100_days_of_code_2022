use num_bigint::{BigInt, ToBigInt};
use modpow::*;
use num_traits::{Zero, One, one};

fn calculate_residue(n: &BigInt, p: &BigInt) -> num_bigint::BigInt {
    return n.modpow(&((p-1.to_bigint().unwrap())/2.to_bigint().unwrap()), &p)
}


fn calculate_legendre(n: &BigInt, p: &BigInt) -> i32 {
    let residue = calculate_residue(n,p);

    return if residue == BigInt::one() {
        1
    } else if residue == BigInt::zero() {
        0
    } else {
        -1
    }
}

fn tonelli_shanks(n: &BigInt, p: &BigInt) -> num_bigint::BigInt {

    assert_eq!(calculate_legendre(n, p), BigInt::one(), "Legendre value not equal to 1");

    let mut q = p - BigInt::one();
    let mut s = BigInt::zero();

    while q.modpow(&BigInt::one(), &2.to_bigint().unwrap()) == BigInt::zero() {
        q = q / &2.to_bigint().unwrap();
        s = s + BigInt::one();
    }

    if s == BigInt::one() {
        return n.modpow(&((p + BigInt::one()) / 4.to_bigint().unwrap()), &p)
    }

    let mut z = 2.to_bigint().unwrap();

    while calculate_residue(&z, p) != p - BigInt::one() {
        z = z + BigInt::one();
    }

    let mut c = z.modpow(&q, p);
    let mut r = n.modpow(&((q + BigInt::one()) / 2.to_bigint().unwrap()), p);
    let mut t = n.modpow(&q, p);

    let mut m = s.clone();
    let mut t2 = BigInt::zero().clone();

    while (t-BigInt::one()).modpow(&BigInt::one(), p) != BigInt::zero() {
        t2 = (t * t).modpow(&BigInt::one(), p);
        
    }

    return BigInt::one();



}

fn main() {

    for p in vec![3,5,7,11] {
        for n in 0..11 {
            if n >= p {
                break;
            }
            let bign = n.to_bigint().unwrap();
            println!("({}|{}) -> {}", n, p, calculate_legendre(&n.to_bigint().unwrap(),
                                                               &p.to_bigint().unwrap()));
        }
    }
}