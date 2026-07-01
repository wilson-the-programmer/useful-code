

fn is_prime(n: u32) -> bool {
    if n < 2 {
        return false;
    }

    let mut i = 2;
    while i * i <= n {
        if n % i == 0 {
            return false;
        }
        i += 1;
    }

    true
}

fn main() {
    let min = 0;
    let max = 100;
    let range_size = 10;

    println!("{:<15}{:>18}", "Numbers", "Prime Count");
    println!("{:-<33}", "");

    let mut start = min;

    while start < max {
        let end = (start + range_size).min(max);
        let mut count = 0;

        for n in start..end {
            if is_prime(n) {
                count += 1;
            }
        }

        println!("{:>3} - {:<3}{:>20}", start, end, count);

        start += range_size;
    }
}
