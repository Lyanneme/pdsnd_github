import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        cities= ['chicago','new york city','washington']
        city= input("\n Which city do you want to explore data from?\n(Chicago, New york city, Washington) \n").lower()
        #error handling
        if city in cities:
            break
        else:
            print("\n Ups there has been an error. Please enter one of the valid city names")    

    # get user input for month (january, february, ... , june or none)
    while True:
        months= ['January','February','March','April','June','May','None']
        month = input("\n Which month do you want to explore data from?\n(January, February, March, April, May, June)? Type 'None' for no specific month\n").title()
       # error handling
        if month in months:
            break
        else:
            print("\n Ups there has been an error. Please enter one of the valid month names")    

    # get user input for day of week (monday, tuesday, ... sunday or none)
    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','None']
        day = input("\n Which day of the week do you want to explore data for? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' for no specific day \n").title()         
        #error handling
        if day in days:
            break
        else:
            print("\n Ups there has been an error. Please enter one of the valid day names")    
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #1  read data from the selected city with panda 
    df = pd.read_csv(CITY_DATA[city])

    #2 convert the Start Time to datetime onject in order to be able to make an extraction for month weekday, hour,
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #3 extract month and day from week 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #4 Filtering if possible based on user selection
    if month != 'None':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
    
        # Establishement of the new dataframe
        df = df[df['month']==month] 

    # Filtering if possible based on user selection
    if day != 'None':
        # Establishment of the new dataframe
        df = df[df['day_of_week']==day]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month =='None':
        pop_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        pop_month= months[pop_month-1]
        print("The most Popular month is",pop_month)

    # display the most common day of week
    if day =='None':
        popular_day= df['day_of_week'].mode()[0]
        print("The popular day is",popular_day)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour=df['Start Hour'].mode()[0]
    print("The popular start hour is {}:00 hrs".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print("The popular start station is {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print("The popular end station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"-"+" "+ df['End Station']
    popular_combination= df['combination'].mode()[0]
    print("The popular combination of start - end station is {} ".format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration=df['Trip Duration'].sum()
    minute,second=divmod(total_duration,60)
    hour,minute=divmod(minute,60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))
    
    # display mean travel time
    mean_duration=round(df['Trip Duration'].mean())
    m,sec=divmod(mean_duration,60)
    if m>60:
        h,m=divmod(m,60)
        print("The duration of the trip is: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
        print("The duration of the trip is: {} minute(s) {} second(s)".format(m,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertype_counts= df['User Type'].value_counts()
    print("\nThe count of types of users are:\n",usertype_counts)


    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gendertype_counts= df['Gender'].value_counts()
        print("\nThe count of types of gender are:\n",gendertype_counts)
    
    # Display earliest, most recent, and most common year of birth
        early_yearofbirth= int(df['Birth Year'].min())
        print("\nThe earliest year of birth is\n",early_yearofbirth)
        recent_yearofbirth= int(df['Birth Year'].max())
        print("\nThe recent year of birth is\n",recent_yearofbirth)
        common_yearofbirth= int(df['Birth Year'].mode()[0])
        print("\nMost common year of birth is\n",common_yearofbirth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    while True:
        response=['yes','no']
        choice= input("Do you want to explore trip data (each 5 data rows)? Use 'yes' or 'no'\n").lower()
        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break     
        else:
            print("Ups there has been an error. Please enter one of the valid response names")
    if  choice=='yes':       
            while True:
                choice_2= input("Do you want to explore 5 more rows of data? Use 'yes' or 'no'\n").lower()
                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:    
                        break  
                else:
                    print("Ups there has been an error. Please enter one of the valid response names")              


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

