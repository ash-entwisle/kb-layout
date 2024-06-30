use clap::Command;

mod handlers;
mod data;
mod filter;

#[tokio::main]
async fn main() {
    let matches = Command::new("My CLI Tool")
        .version("1.0")
        .author("Your Name")
        .about("A CLI tool for scraping and analyzing data")
        .subcommand(
            Command::new("scrape")
                .about("Scrape data")
        )
        .subcommand(
            Command::new("analyze")
                .about("Analyze data")
        )
        .get_matches();

    
    match matches.subcommand() {
        Some(("scrape", scrape_matches)) => {
            handlers::scrape::scrape().await;
            }
        Some(("analyze", analyze_matches)) => {
            handlers::analyze::analyze().await;
        }
        _ => {
            println!("No subcommand specified, see the readme for usage instructions")
        }
    };
}