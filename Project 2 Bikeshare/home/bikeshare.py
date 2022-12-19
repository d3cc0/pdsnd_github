import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')

WEEKDAYS = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers."""
    
    while True:
        choice = input(prompt).lower().strip()
        # Terminate the process if the input is end
        if choice == 'end':
            raise SystemExit
        # Take action if the input is more than one name
        elif ',' not in choice:
            if choice in choices:
                break
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        
        
      
        prompt = ('\nPlease make sure to enter a valid format. \ne.g Check CAPITAL letters\n')
    
    return choice
    
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hi! Let\'s explore some US bikeshare data!\n")
    
    print("Type 'end' if you want to cancel.\n")
    
    while True:
        city = choice("\nWhich city you want to get data from?\n"
                      "(Chicago, New York or Washington)\n>", CITY_DATA.keys())
        month = choice("\nWhich month you want to get data from?\n"
                       "(Choose from January to June)\n>", MONTHS)
        day = choice("\nWhich weekday you want get data from?\n>", WEEKDAYS)
        
        confirmation = choice("\nConfirm the information you selected"
                              "\n\nCity: {}\nMonth: {}\nWeekday: {}\n"
                              "\n [y] Yes\n [n] No\n\n".format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("Try again!")

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

    print("\nLoading...")
    start_time = time.time()
    
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort = True)
        
        try:
            df = df.reindex(colums=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    
    if isinstance(month, list):
        df = concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (month.index(month)+1)]
    
    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
        
    else:
        df = df[df['Weekday'] == day.title()]
        
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The most common month is: ' + str(most_common_month-1).title() + '.')

    # TO DO: display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The most common day is: ' + str(most_common_day) + ".")

    # TO DO: display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' + str(most_common_hour) + '.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and travel."""

    print('\nCalculating The Most Popular Stations and Travel...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print('The most commonly used start station is: ' + most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print('The most commonly used end station is: ' + most_common_end_station)

    # TO DO: display most frequent combination of start station and end station travel
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average Trip Duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) + 'd ' + 
                         str(int((total_travel_time % 86400)//3600)) + 'h ' + 
                         str(int(((total_travel_time % 86400) % 3600)//60)) + 'm' + 
                         str(int(((total_travel_time % 86400) % 3600) % 60)) + 's')
    
    print('The total travel time is: ' + total_travel_time + '.')
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm' + str(int(mean_travel_time % 60)) + 's')
    print('The mean travel time is: ' + mean_travel_time + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('Distribution for user types:')
    print(user_types)

    # TO DO: Display counts of gender
    try:
        gender_distrinution = df['Gender'].value_counts().to_string()
        print('\nDistribution for each gender:')
        print(gender_distrinution)
    except KeyError:
        print('Oops! There is no gender information for {}.'.format(city.title()))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print('The last person to ride a bike was born in ' + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print('The youngest person to ride a bike was born in ' + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print('The most common bitrh year amongst the riders is ' + most_common_birth_year)
    
    except:
        print('Oops! There is no bitrth year information for {}.'.format(city.title))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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