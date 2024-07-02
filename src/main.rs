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
        .subcommand(
            Command::new("layout_5")
                .about("Layout 5")
        )
        .get_matches();

    
    match matches.subcommand() {
        Some(("scrape", scrape_matches)) => {
            handlers::scrape::scrape().await;
        }
        Some(("analyze", analyze_matches)) => {
            handlers::analyze::analyze().await;
        }
        Some(("layout_5", layout_5_matches)) => {
            handlers::layout_5::layout_5().await;
        }
        _ => {
            println!("No subcommand specified, see the readme for usage instructions")
        }
    };
}