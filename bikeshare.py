import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city_list = ['washington', 'new york city', 'chicago']
    while city.lower().strip() not in city_list:
        print()
        city = input("Enter city name to be analysed. Valid names are 'chicago', 'new york city', 'washington'. - ")
        city = city.lower()


    # get user input for month (all, january, february, ... , june)
    month = ''
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month.lower().strip() not in month_list:
        print()
        month = input("Enter month to be analysed. Valid names are 'all', 'january', 'february', 'march', 'april', 'may', 'june'. - ")
        month = month.lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    dow_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while day.lower().strip() not in dow_list:
        print()
        day = input("Enter day of week to be analysed. Valid names are 'all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'. - ")
        day = day.lower()


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
    try:
        
        df = pd.read_csv(f'{CITY_DATA[city]}', parse_dates=['Start Time', 'End Time'])

        # Drop first column
        df = df.iloc[:,1:]

        # Create month column
        months_dict = {'01': 'january', '02': 'february', '03': 'march', '04':'april', '05': 'may', '06': 'june'}

        df['month'] = df['Start Time'].dt.strftime('%m')
        df['month'] = df['month'].map(months_dict)

        # Create day of week (dow) column
        dow_dict ={0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}

        df['dow'] = df['Start Time'].dt.dayofweek
        df['dow'] = df['dow'].map(dow_dict)

         # Create an hour column
        df['hour'] = df['Start Time'].dt.hour
        df['hour'] = df['hour'].apply(lambda x: str(x) + ':00')  


        # Filter data
        if month != 'all':
            df = df[df['month'] == month]

        if day != 'all':
            df = df[df['dow'] == day]

        count = 0

        while True:
            view_data = input('Do you want to view 5 lines of raw data? Enter yes or no. - ')

            if view_data != 'yes':
                break
            else: 
                count +=1
                print(df.iloc[(count-1)*5:(count*5)])

        

        return df
    
    except KeyError as e:
        print('An error occured {}'.format(e))



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_lines()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    month = df['month'].value_counts().index[0]
    
    print()
    print('----- Most Common Month -----')
    print(month)


    # display the most common day of week
    dow = df['dow'].value_counts().index[0]

    print()
    print('----- Most Common Day of the Week -----')
    print(dow)


    # display the most common start hour
    hour = df['hour'].value_counts().index[0]

    print()
    print('----- Most Common Start Hour -----')
    print(hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_lines()
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_lines()
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print()
    print('----- Most used Start Station -----')
    print(f'\'{df["Start Station"].value_counts().index[0]}\'')

    # display most commonly used end station
    print()
    print('----- Most used End Station -----')
    print(f'\'{df["End Station"].value_counts().index[0]}\'')

    # display most frequent combination of start station and end station trip
    print()
    print('----- Most Frequent Route -----')

    df['Routes'] = df['Start Station'] + ' - ' + df['End Station']
    most_freq_route = df['Routes'].value_counts().index[0]

    print(f'Start station: {most_freq_route.split("-")[0].strip()}')
    print()
    print(f'End station: {most_freq_route.split("-")[1].strip()}')
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_lines()
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_lines()
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('----- Total travel time -----')
    print(f'{np.sum(df["Trip Duration"])}')

    # display mean travel time
    print()
    print('----- Mean Travel Time -----')
    print(f'{np.mean(df["Trip Duration"])}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_lines()
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_lines()
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        print('----- User types -----')
        for index, val in zip(df['User Type'].value_counts().index, df['User Type'].value_counts()):
                print(index +  ": " + str(val))
        print()
        # Display counts of gender
        print("----- Gender count -----")
        for index, val in zip(df['Gender'].value_counts().index, df['Gender'].value_counts()):
                print(index +  ": " + str(val))
        print()
        
        # Display earliest, most recent, and most common year of birth

        year_list = df['Birth Year'].value_counts().index
        year_list = list(year_list)
        year_list = sorted(year_list)

        print('----- Most common year of birth -----')
        print(int(df["Birth Year"].value_counts().index[0]))
        print()
        print('----- Earliest year of birth -----')
        print(int(year_list[0]))

        print()
        print('----- Most recent year of birth -----')
        print(int(year_list[-1]))

        print("\nThis took %s seconds." % (time.time() - start_time))

        print_lines()
        print('-'*40)

    except Exception as e:
        print('An error occurred. %s column doesn\'t exist for this dataset' % (e))

def print_lines():
    """ Print two empty lines """
    print()
    print()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
