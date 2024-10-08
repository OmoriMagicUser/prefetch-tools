import pandas as pd

def find_duplicate_hashes_in_csv(file_path):
    try:
        data = pd.read_csv(file_path)

        duplicate_hashes = data[data.duplicated('Hash', keep=False)]

        if not duplicate_hashes.empty:
            print("\nDuplicate file hashes found:")
            for hash_value in duplicate_hashes['Hash'].unique():
                print(f"\nHash: {hash_value}")
                matching_files = duplicate_hashes[duplicate_hashes['Hash'] == hash_value]
                for _, row in matching_files.iterrows():
                    print(f"  - File: {row['SourceFilename']}")
        else:
            print("\nNo duplicate file hashes found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    file_path = input("Please enter the path to the CSV file: ").strip()

    find_duplicate_hashes_in_csv(file_path)

if __name__ == "__main__":
    main()
