$ cat Cargo.toml                           [package]
name = "rust"
version = "0.1.0"
edition = "2024"



[dependencies]
chrono = "0.4"
colored = "2.1"
rand = "0.8"
sysinfo = "0.30"
$
$ cat src/main.rs
use chrono::Local;
use colored::*;
use sysinfo::System;

fn main() {
    let mut system = System::new_all();
    system.refresh_all();

    println!("{}", "=== System Report ===".green());

    println!("Time: {}", Local::now().format("%Y-%m-%d %H:%M:%S"));

    println!("OS: {}", System::name().unwrap_or("Unknown".to_string()));

    println!("Kernel: {}", System::kernel_version().unwrap_or("Unknown".to_string()));

    println!("Host: {}", System::host_name().unwrap_or("Unknown".to_string()));

    println!("CPU Cores: {}", system.cpus().len());

    println!("Total Memory: {} MB", system.total_memory() / 1024 / 1024);

    println!("Used Memory: {} MB", system.used_memory() / 1024 / 1024);

    println!("System Uptime: {} seconds", System::uptime());

    println!("Processes Running: {}", system.processes().len());
}


Example

$
$ cargo run --bin rust
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.54s
     Running `target/debug/rust`

=== System Report ===
Time: 2026-06-30 12:44:31
OS: C5L Max
Kernel: 5.4.286
Host: localhost
CPU Cores: 0
Total Memory: 1911 MB
Used Memory: 923 MB
System Uptime: 0 seconds
Processes Running: 14

