import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

VALID_CITY_NAMES = ['chicago', 'new york city', 'washington']
VALID_MONTH_NAMES = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAY_OF_WEEK = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    month = ''
    day = ''

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in VALID_CITY_NAMES:
        city = input("Please enter city name ('chicago', 'new york city', 'washington'):\n").lower().strip()
        if city not in VALID_CITY_NAMES:
            print('Please enter valid city name')

    # get user input for month (all, january, february, ... , june)
    while month not in VALID_MONTH_NAMES:
        month = input("Please enter month name (all, january, february, ... , june)").lower()
        if month not in VALID_MONTH_NAMES:
            print('Please enter valid month name')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in VALID_DAY_OF_WEEK:
        day = input("Please enter day of week (all, monday, tuesday, ... sunday)").lower()
        if month not in VALID_MONTH_NAMES:
            print('Please enter valid day of week')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == VALID_MONTH_NAMES.index(month)]
    if day != 'all':
        df = df[df['day_of_week'] == VALID_DAY_OF_WEEK.index(day) - 1]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("Most common month is :", VALID_MONTH_NAMES[most_common_month])

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("Most common day of week is :", VALID_DAY_OF_WEEK[most_common_day_of_week+1])

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("Most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].value_counts().idxmax()
    print("Most commonly used Start Station is:", most_commonly_used_start_station)

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].value_counts().idxmax()
    print("Most commonly used End station is :", most_commonly_used_end_station)

    # display most frequent combination of start station and end station trip
    most_common_combination_of_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print(f"Most commonly used Start station & End station are : {most_common_combination_of_start_end_station[0]},"
          f" {most_common_combination_of_start_end_station[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is :", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is :", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:\n")
    user_type_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_type_counts):
        print(f"{user_type_counts.index[index]}: {user_count}")
    try:
        # Display counts of gender
        print("Counts of Gender:\n")
        gender_counts = df['Gender'].value_counts()

        for index, gender_count in enumerate(gender_counts):
            print(f"{gender_counts.index[index]}: {gender_count}")
    except KeyError:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
    # Display earliest, most recent, and most common year of birth
    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print("The most common Birth Year is:", most_common_year)

        most_recent_birth_year = df['Birth Year'].max()
        print("The most recent Birth Year is:", most_recent_birth_year)

        earliest_birth_year = df['Birth Year'].min()
        print("The most earliest Birth Year is:", earliest_birth_year)
    except KeyError:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    start_loc = 0
    while start_loc + 5 <= len(df.index):
        print(df.iloc[start_loc: start_loc + 5])
        start_loc += 5
        view_display = input("Do you wish to continue?: Enter Yes or No").lower()
        if view_display.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
        if view_data.lower() == 'yes':
            display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
