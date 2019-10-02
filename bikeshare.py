import time
import pandas as pd
import numpy as np
import statistics as st


CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
         or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input("\nWould you like to see data for Chicago, New York City, or Washington.\n").lower()

    while True:
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            city = input('Enter the correct city name: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nWhich month? January, February, March, April, May, June, or All?\n").lower()

    while True:
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            month = input('Enter a valid month: ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhich day ? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?\n').lower()

    while True:
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            day = input('Enter a correct day of the week: ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
         or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
         or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    print ("Accessing data from: " + file_name)
    df = pd.read_csv(file_name)

    df['Start Time']=pd.to_datetime(arg=df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    #filter by month
    if month != 'all':
        df['month'] = df['Start Time'].dt.month

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df.loc[df['month'] == month]
    #filter by day
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    month = df['Start Time'].dt.month
    weekday_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour

    # TO DO: display the most common month
    most_common_month = month.mode()[0]
    print('Displaying the most common month:', most_common_month)

    # TO DO: display the most common day of week
    most_common_day = weekday_name.mode()[0]
    print('Displaying the most common day:', most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = hour.mode()[0]
    print('Displaying the most common hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is:', df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('The most commonly used end station is:', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    combine_stations = df['Start Station'] + "*" + df['End Station']
    common_station = combine_stations.value_counts().idxmax()
    print('Most frequent used combinations are:\n{} \nto\n{}'.format(common_station.split('*')[0],         common_station.split('*')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Readable time format
    def readable_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        print('Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}'.format(y,d,h,m,s))

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Displaying the total travel time:\n')
    readable_time(total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nDisplaying the mean travel time: {} seconds'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:', user_types)

    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('Gender Types: ', gender_types)
    except KeyError:
        print("There is not data available this month for Gender Types:\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('Display the earliest birth year:', earliest_year)
    except KeyError:
        print("There is no data available for this month for displaying earliest:\n")

    try:
        most_recent_year = df['Birth Year'].max()
        print('Display the most recent year', most_recent_year)
    except KeyError:
        print("There is no data available for this month for displaying max:\n")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('Display the most common year', most_common_year)
    except KeyError:
        print("There is no data available for the displaying the most common:\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Raw data is displayed upon request by the user in this manner:
    Script should prompt the user if they want to see 5 lines of raw data,
    display that data if the answer is 'yes', and continue these prompts
    and displays until the user says 'no'.
    """

    user_input = input('Do you want to see raw data? Enter yes or no.\n')
    line_number = 0

    while 1 == 1 :
        if user_input.lower() == 'yes':
            print(df.iloc[line_number : line_number + 5])
            line_number += 5
            user_input = input('\nDo you want to see more raw data? Enter yes or no .\n')
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
