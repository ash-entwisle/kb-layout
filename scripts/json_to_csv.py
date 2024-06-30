import csv
import json

# Function to write a dictionary to a CSV file
def write_dict_to_csv(table_name, table_data):
    csv_file = f"../data/{table_name}.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["key", "value"])
        for key, value in table_data.items():
            writer.writerow([key, value])
    print(f"CSV file '{csv_file}' has been created.")


if __name__ == "__main__":
    # Load JSON data
    with open("../data/data.json") as f:
        repos = json.load(f)

    # Write JSON data to CSV
    for table_name, table_data in repos.items():
        write_dict_to_csv(table_name, table_data)
        
