import time
import pandas as pd
import numpy as np


def greeting() :
    print ( " welcome to bikeshare system ")

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_input(input_str, input_type):
    """
    check the validity of user input .
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month , 3 = day
    """

    while True:
        input_read = input(input_str).casefold()
        try:

            if input_read in ['chicago', 'new york city', 'washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_read in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                                'all'] and input_type == 3:
                break
            else:

                if input_type == 1:
                    print("sorry, your input should be : chicago new york city or washington")
                if input_type == 2:
                    print("sorry,your input should be :january, february, march,april,may,june or all")
                if input_type == 3:
                    print("sorry, your input should be :sunday,... friday,saturday or all")
        except ValueError:
            print("Sorry,your input is wrong")
    return input_read


def get_filters():
    """
     Asks user to specify a city ,month, and day to analyze .

     Returns:
     (str) city - name of the city to analyze
     (str) month - name of the month filter by , or ''all'' to apply no month filter
     (str) day - name of the day of week to filter by , or ''all'' to apply no day filter

     """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (Chicago,new york city,   washington) .HINT: Use a while loop to handle invalid inputs city
    city = check_input("would you like to see data for Chicago,new york or washington?", 1)

    # TO DO: get user input for month (all, january, february, ... , june)

    month = check_input(" which month (all,january,...june)?", 2)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = check_input(" which day? (all,monday,tuesday,...sunday) ", 3)

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week ,hour from start time to create new columns

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #  filter by month if applicable
    if month != 'all':
        # use the index of the months list to get  the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Day Of Week:', popular_day_of_week)

    # TO DO: display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]
    print('Moat Common Start Hour:', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('user types in Data are :', df['User Type'].value_counts())
    # because columns Gender and Birth Year aren't in washington data , we have ensure that the city is not    washington
    if city != 'washington':

        # TO DO: Display counts of gender
        try:
            gender_types = df['Gender'].value_counts()
            print('\nGender Types:\n', gender_types)
        except KeyError:
            print("\nGender Types :\nNo data available for this month.")

        # TO DO: Display earliest, most recent, and most common year of birth

        try:
            most_common_year = df['Birth Year'].value_counts()
            print('\nMost Common Year:', most_common_year)
        except KeyError:
            print("\nMost Common Year:\nNo data available for this month")

        try:
            Most_recent_year = df['Birth Year'].max()
            print('\nMost Recent Year:', Most_recent_year)
        except KeyError:
            print("nMost Recent Year:\nNo data available for this month")

        try:
            Earliest_Year = df['Birth Year'].min()
            print('\nEarliest Year:', Earliest_Year)
        except KeyError:
            print("\nEarliest Year :\nNo data available for this month")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Asking if the user want to show more data
def ask_for_more_data(df):
    view_more_data = input("would you like to view 5 rows of data ? enter yes or no?").lower()
    start_loc = 0
    while view_more_data == 'yes':
        print(df.iloc[0:5])
        start_loc += 5
        view_more_data = input("would you like to view 5 rows of data ? enter yes or no?").lower()

    return df


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        return ask_for_more_data(df)


if __name__ == "__main__":
    main()

