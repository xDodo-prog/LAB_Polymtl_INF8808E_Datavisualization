'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''

    dataframe = dataframe.copy()
    
    # Convert the "Date_Plantation" column to datetime format, coercing errors
    dataframe["Date_Plantation"] = pd.to_datetime(dataframe["Date_Plantation"], errors="coerce")
    
    return dataframe


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    
    dataframe = dataframe.copy()
    
    # Extract year from the date and store in a new column
    dataframe["Year"] = dataframe["Date_Plantation"].dt.year
    
    # Filter rows where year is within the given range
    return dataframe[(dataframe["Year"] >= start) & (dataframe["Year"] <= end)]


def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    
    dataframe = dataframe.copy()
    
    # Extract the year from the planting date
    dataframe["Year"] = dataframe["Date_Plantation"].dt.year
    
    # Group by neighborhood and year, then count the number of entries
    grouped = dataframe.groupby(["Arrond_Nom", "Year"]).size().reset_index(name="Counts")
    
    return grouped


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    # Pivot the table to make neighborhoods the index and years the columns
    heatmap_df = yearly_df.pivot(index="Arrond_Nom", columns="Year", values="Counts")
    
    # Replace missing values with 0 and ensure data is integer type
    heatmap_df = heatmap_df.fillna(0).astype(int)
    
    return heatmap_df


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
   
    dataframe = dataframe.copy()
    
    # Extract year from the planting date
    dataframe["Year"] = dataframe["Date_Plantation"].dt.year

    # Filter by the selected neighborhood and year
    filtered_df = dataframe[
        (dataframe["Arrond_Nom"] == arrond) &
        (dataframe["Year"] == year)
    ]

    # Return empty result if no data found
    if filtered_df.empty:
        return pd.DataFrame(columns=["Date_Plantation", "Counts"])

    # Get the full date range between min and max planting date
    min_date = filtered_df["Date_Plantation"].min()
    max_date = filtered_df["Date_Plantation"].max()
    full_range = pd.date_range(start=min_date, end=max_date)
    full_df = pd.DataFrame({"Date_Plantation": full_range})

    # Count the number of trees planted per day
    daily_counts = (
        filtered_df
        .groupby("Date_Plantation")
        .size()
        .reset_index(name="Counts")
    )

    # Merge full date range with the actual daily counts
    merged_df = pd.merge(full_df, daily_counts, on="Date_Plantation", how="left")
    
    # Fill missing counts with 0 and convert to integer
    merged_df["Counts"] = merged_df["Counts"].fillna(0).astype(int)

    return merged_df


# === Test Calls ===
df = pd.read_csv("./assets/data/arbres.csv")  # Load data from CSV
df = convert_dates(df)                        # Convert date columns to datetime
df = filter_years(df, 2010, 2020)             # Filter rows between 2010 and 2020
summary = summarize_yearly_counts(df)         # Summarize by year and neighborhood
heatmap_df = restructure_df(summary)          # Restructure to heatmap format
print(heatmap_df.head())                      # Print preview of heatmap data
daily = get_daily_info(df, "Le Sud-Ouest", 2017)  # Get daily counts for one area and year
print(daily.head())                           # Print preview of daily data
