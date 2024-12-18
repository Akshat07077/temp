import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def find_duplicates_and_non_sequential(data, pk_column):
    # Find duplicate IDs
    duplicate_ids = data[data[pk_column].duplicated(keep=False)]

    # Find non-sequential IDs
    data = data.sort_values(by=pk_column).reset_index(drop=True)
    data['Expected_Next_ID'] = data[pk_column].shift(-1)  # Expected next PK
    data['Is_Sequential'] = (data['Expected_Next_ID'] == data[pk_column] + 1)
    non_sequential_ids = data[data['Is_Sequential'] == False].dropna()

    return {
        "Duplicates": duplicate_ids,
        "Non_Sequential": non_sequential_ids,
        "Sorted_Data": data
    }

def plot_anomalies(data, anomalies, pk_column):
    """
    Plot graphical anomalies including duplicates and non-sequential IDs.

    Parameters:
    - data (pd.DataFrame): The full dataset.
    - anomalies (dict): Anomalies detected in the dataset.
    - pk_column (str): The primary key column.
    """
    sorted_data = anomalies["Sorted_Data"]

    # Plot the full dataset
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=sorted_data.index, y=sorted_data[pk_column], label="Data")

    # Highlight duplicates
    if not anomalies["Duplicates"].empty:
        duplicate_indices = anomalies["Duplicates"].index
        plt.scatter(duplicate_indices, 
                    anomalies["Duplicates"][pk_column], 
                    color="red", label="Duplicates", s=100, zorder=5)
    
    # Highlight non-sequential points
    if not anomalies["Non_Sequential"].empty:
        non_sequential_indices = anomalies["Non_Sequential"].index
        plt.scatter(non_sequential_indices, 
                    anomalies["Non_Sequential"][pk_column], 
                    color="orange", label="Non-Sequential", s=100, zorder=5)

    # Add labels and legend
    plt.title("Anomalies in Primary Key (Duplicates and Non-Sequential IDs)", fontsize=14)
    plt.xlabel("Index in DataFrame", fontsize=12)
    plt.ylabel(pk_column, fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Simulated dataset
    sample_data = {
        "ID": [1, 2, 2, 3, 5, 6, 6, 8],  # ID column with duplicates and gaps
        "Column1": ["A", "B", "C", "D", "E", "F", "G", "H"],
        "Column2": [10, 20, 30, 40, 50, 60, 70, 80]
    }
    df = pd.DataFrame(sample_data)

    # Detect anomalies
    anomalies = find_duplicates_and_non_sequential(df, pk_column="ID")

    # Print anomalies
    print("Duplicate Records:")
    print(anomalies["Duplicates"])

    print("\nNon-Sequential Records:")
    print(anomalies["Non_Sequential"])

    # Plot the anomalies
    plot_anomalies(df, anomalies, pk_column="ID")

