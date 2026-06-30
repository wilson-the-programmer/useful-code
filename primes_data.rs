

fn is_prime(n: u64) -> bool {
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

    return true;
}

fn main() {
    let start: u64 = 1;
    let end: u64 = 10000;

    let mut primes = 0;
    let mut last = 0;

    let mut gap_sum = 0;
    let mut gap_count = 0;
    let mut twin = 0;
    let mut max_gap = 0;

    for n in start..=end {
        if is_prime(n) {
            primes += 1;

            if last != 0 {
                let gap = n - last;

                gap_sum += gap;
                gap_count += 1;

                if gap > max_gap {
                    max_gap = gap;
                }

                if gap == 2 {
                    twin += 1;
                }
            }

            last = n;
        }
    }

    let range = (end - start + 1) as f64;

    let density = primes as f64 / range;
    let expected_count = (end as f64) / (end as f64).ln();

    let error = primes as f64 - expected_count;
    let relative_error = error.abs() / expected_count;

    let avg_gap = gap_sum as f64 / gap_count as f64;
    let expected_density = 1.0 / (end as f64).ln();
    let density_error = (density - expected_density).abs();

    println!("=== Prime Interval Summary ===\n");

    println!("Range: ({}, {})", start, end);
    println!("Primes found: {}", primes);
    println!("Expected π(x): {:.2}", expected_count);
    println!("Error: {:.2}", error);
    println!("Relative Error: {:.6}", relative_error);
    println!("Density: {:.6}", density);
    println!("Expected Density: {:.6}", expected_density);
    println!("Density Error: {:.6}", density_error);
    println!("Average Gap: {:.3}", avg_gap);
    println!("Max Gap: {}", max_gap);
    println!("Twin Primes: {}", twin);

    /* ---------------- ADDED RIEMANN VIEW LAYER ---------------- */

    let x = end as f64;

    let pi_over_x = primes as f64 / x;
    let logx = x.ln();

    let log_model = 1.0 / logx;
    let log_model_error = density - log_model;

    let error_per_prime = error / primes as f64;

    let over_under = if error > 0.0 {
        "UNDER-ESTIMATION by model"
    } else {
        "OVER-ESTIMATION by model"
    };

    println!("\n=== Riemann View Layer ===");
    println!("π(x)/x density: {:.6}", pi_over_x);
    println!("1/ln(x) model: {:.6}", log_model);
    println!("Density deviation: {:.6}", log_model_error);
    println!("Error per prime: {:.6}", error_per_prime);
    println!("Model behavior: {}", over_under);
}

