import time
import pandas as pd

# Dictionaries and variables to be used in various functions

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}

date_month = ("January", "February", "March", "April", "May", "June")
date_day = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# function to be called upon in time_stats function

def standard_time(num):
    """
    Converts an integer 0 - 23 into standard time

    Returns:
        (int) hours - hour of the day from 1 - 12
        (str) period - "AM" or "PM"
    """

    if num == 0:
        hours = 12
        period = "AM"
    elif num < 12:
        hours = num
        period = "AM"
    elif num == 12:
        hours = num
        period = "PM"
    elif 12 < num <= 23:
        hours = num - 12
        period = "PM"

    return hours, period

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    invalid = True
    while invalid:

        city = input("Select 'Chicago', 'New York City', or 'Washington': ").title().strip()

        if city in ("Chicago", "New York City", "Washington"):
            invalid = False
        else:
            print("not a valid city, please try again")

    # get user input for month (or all)
    invalid = True
    while invalid:

        month = input("Select a month from January to June to filter by. Type All to select all: ").title().strip()

        if month in date_month or month == "All":
            invalid = False
        else:
            print("not a valid month, please try again")

    # get user input for day of week (or all)
    invalid = True
    while invalid:

        day = int(input("Select a day to filter by (pick an integer from 1 to 7, or 8 for 'all days'): ").strip())

        if day in range(1, 9):
            invalid = False
        else:
            print("not a valid day, please try again")

    print(f"\nYou have selected the city: {city}, month: {month}, day of week number: {day}")

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
    # load csv based on city selected
    df = pd.read_csv(CITY_DATA[city])

    # convert start date column in csv to Pandas Datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create a month and day column
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek

    # change 'days' in 'Day' column from 0 to 6 to 1 - 7:
    df['Day'] = df['Day'] + 1

    # filter dataframe by month (if required)
    if month != 'All':
        selected_month = date_month.index(month) + 1

        df = df[df['Month'] == selected_month]

    # filter dataframe by day (if required)
    if day != 8:
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['Month'].mode()[0]
    print(f"the most common month is {date_month[common_month - 1]}")

    # display the most common day of week

    common_day = df['Day'].mode()[0]
    print(f"the most common day of the week is {date_day[common_day - 1]}")

    # create a new column for start hours

    df['Hour'] = df['Start Time'].dt.hour

    # display the most common start hour

    common_hour = df['Hour'].mode()[0]
    hours, period = standard_time(common_hour)
    print(f"the most common start hour is {hours} {period}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is {common_start_station}")

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print(f"the most commonly used end station is {common_end_station}")

    # produce a dataframe which counts the number of unique combinations of Start Station and End Station.

    grouping_and_count = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')

    # display most frequent combination of start station and end station trip

    max_comb = grouping_and_count.sort_values(by='Count', ascending=False).head(1)

    print(f"the most frequent combination of stations is {max_comb.iloc[0,0]} and {max_comb.iloc[0,1]}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_time = df['Trip Duration'].sum()
    print(f"The total travel time is {total_time}")

    # display mean travel time

    mean_time = df['Trip Duration'].mean()
    print(f"the mean travel time is {mean_time}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display count of user types

    usertype_count = df['User Type'].value_counts()

    subscribers = usertype_count.get('Subscriber')
    customers = usertype_count.get('Customer')

    print(f"number of Subscribers: {subscribers}\nnumber of Customers: {customers}\n")

    if city != 'Washington':

        # Display counts of gender

        gender_type = df['Gender'].value_counts()

        Male_count = gender_type.get('Male')
        Female_count = gender_type.get('Female')
        NaN_count = df['Gender'].isnull().sum()

        print(f"number of men: {Male_count}\nnumber of women: {Female_count}\nnumber of unknown: {NaN_count}\n")

        # Convert column from float to integer while preserving NaN values

        df['Birth Year'] = df['Birth Year'].astype('Int64')

        # Display earliest, most recent, and most common year of birth

        earliest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print(f"earliest birth year: {earliest_year}\nlatest birth year: {latest_year}\nmost common birth year: {common_year}\n")

        # Display number of unknown birth years

        unknown_birth_count = df['Birth Year'].isnull().sum()

        print(f"number of unknown birth years: {unknown_birth_count}")

    else:
        print("Washington.csv does not have any information regarding user gender or birth year")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)


def display_data(df):
    """
    used to print five rows of raw data. Uses 3 while loops to repeat until 'no' is inserted into input
    Returns:
        Nothing (return is used to end function)
     """

    # Check if input is valid

    invalid = True
    while invalid:
        view_data = input('\nWould you like to view the first 5 rows of the selected dataframe? Enter yes or no\n').lower().strip()
        if view_data not in ('yes', 'no'):
            print("invalid input, please try again")
        else:
            invalid = False

    # prints five rows of dataframe if input is 'yes'

    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

        # check if following inputs are valid or end function

        while True:
            view_data = input("Do you wish to continue? Enter yes or no: ").lower().strip()
            if view_data == 'no':
                return
            elif view_data == 'yes':
                print("Displaying the next five rows...\n")
                break
            else:
                print("Invalid input, please try again.")

        # End function if all rows in dataframe have been printed

        if start_loc >= len(df):
            print("You've reached the end of the dataframe.")
            return

def main():
    while True:
        city, month, day = get_filters()
        end_script = input("\nAre you happy with your selection? Enter 'yes' to continue.\n")
        print('-' * 40)
        if end_script.lower().strip() != 'yes':
            print("script ending, please run again to change filters")
            break
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' to restart.\n")
        if restart.lower().strip() != 'yes':
            print("ending script")
            break


if __name__ == "__main__":
	main()
