#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 17:59:08 2017

@author: Floreana
"""

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()

def movie_list():
    ''' Function to pull top 5,000 movies from website, then save to a 
    pickle file '''

    # Pulls the first 100 movies on page 1
    movies = pd.read_html(
            'https://www.the-numbers.com/box-office-records/international/' + 
            'all-movies/cumulative/all-time')
    movies_df = movies[0][0:]
    
    # Gets movies 101-5,000 from subsequent pages
    for i in range(1,50):
        next_movies = pd.read_html(
            'https://www.the-numbers.com/box-office-records/international/' + 
            'all-movies/cumulative/all-time/' + str(i*100+1))
        
        movies_df=movies_df.append(next_movies[0][0:])

    # International = Worldwide - Domestic        
    movies_df.rename(columns={'InternationalBox Office':'IntBoxOff', 
                             'Released':'Year', 
                             'DomesticBox Office':'DomBoxOff',
                             'WorldwideBox Office':'WorldBoxOff'
                             }, inplace=True)
    
  
    cols=['IntBoxOff','DomBoxOff','WorldBoxOff']
    movies_df[cols] = movies_df[cols].replace( '[\$,]', '', 
             regex=True ).astype(int)
    
    movies_df.set_index('Rank', inplace=True)
    
    pickle_out = open('movies.pickle', 'wb')
    pickle.dump(movies_df, pickle_out)
    pickle_out.close()

    
def inflation_rates():
    ''' 
    NOT USING FUNCTION ANYMORE, USING CPI_VALUES INSTEAD
    Pull inflation rates from website 
    '''
    
    # Gives inflation rates in percentages
    inflate = pd.read_html('http://www.usinflationcalculator.com/inflation/' +
            'historical-inflation-rates/')[0][0:]

    # Change column names to months and average, which was the first row, then
    #   remove this row
    inflate.columns = inflate.iloc[0]
    inflate.drop(inflate.index[0], inplace=True)

    inflate.set_index('Year', inplace=True)
    inflate = inflate.astype(float)
    
    plt.figure()
    inflate.Ave.plot()
#    for column in inflate:
#        inflate[column].plot(legend=True)
    plt.xlabel('Year')
    plt.ylabel('Average Annual Inflation Rate')
    plt.show
    
    for (idx, row) in inflate.iterrows():
    #    row.plot(legend=True)   # plots inflation rates for all months, with 
    #                            # each line representing a year
        print(idx)  # The years (index)
        print(row)  # The months and inflation rates for each year

    return inflate

def cpi_values():
    
    cpi_u = pd.read_html('http://www.usinflationcalculator.com/inflation/' + 
                         'consumer-price-index-and-annual-percent-changes-' + 
                         'from-1913-to-2008/')[0][0:]
    cpi_u.columns = cpi_u.iloc[1]
    cpi_u.drop(cpi_u.index[0:2], inplace=True)
    cpi_u.set_index('Year', inplace=True)

    # Need an average for 2018 which isn't complete  
    avgs_2018 = cpi_u.iloc[-1].astype(float)
    ave2018 = np.nanmean(avgs_2018)
    ave_cpi = cpi_u.Avg.astype(float)
    ave_cpi.set_value('2018', ave2018)
    
    return ave_cpi

def ticket_prices():
    
    # Gives annual U.S. ticket prices (from:
    #   http://www.boxofficemojo.com/about/adjuster.htm)
    tix = pd.read_html('movie_ticket_prices.html')[-1][1:]
    tix.columns = ['Year', 'Prices']
    
    tix.Prices = tix.Prices.str.strip('Est.')
    tix.Prices = tix.Prices.replace( '[\$]', '', regex=True).astype(float)
    tix.set_index('Year', inplace=True)

    return tix

def movie_inflate():
    
    mov_adjust = []
    
    movies_df = pd.read_pickle('movies.pickle')   
    ave_cpi = cpi_values()
    
    cpi_2018 = ave_cpi['2018']
    
    for (idx, row) in movies_df.iterrows():

        year_cpi = ave_cpi[str(movies_df.Year.iloc[idx-1])]
        year_adjust = (movies_df.DomBoxOff.iloc[idx-1] * cpi_2018) / year_cpi
        mov_adjust.append(year_adjust)

    movies_df['Adjust_DomBO'] = pd.Series(mov_adjust, index=movies_df.index)

    return movies_df

def movie_inflate_plots():
    
    movies_df = movie_inflate()
    
    # Scatterplot of all movies' Domestic Box Office value plotted through time
    plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot(movies_df['Year'], movies_df['DomBoxOff'], marker='.', 
            linestyle='none')
    ax1.set_ylim(10**2, 10**10)
    ax1.set_yscale('log')
    plt.xlabel('Year')
    plt.ylabel('Domestic Box Office')
    plt.title("All Movies' Domestic Box Office Values")
    
    # Scatterplot of all movies' Adjusted Domestic Box Office value plotted 
    # through time
    plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot(movies_df['Year'], movies_df['Adjust_DomBO'], marker='.', 
            linestyle='none')
    ax1.set_ylim(10**2, 10**10)
    ax1.set_yscale('log')
    plt.xlabel('Year')
    plt.ylabel('Adjusted Domestic Box Office')
    plt.title("All Movies' Adjusted Domestic Box Office Values")
    
    bins = np.arange(min(movies_df['Year']), max(movies_df['Year'])+1)
    plt.figure()
    plt.subplot2grid((1, 1), (0, 0))
    plt.hist(movies_df['Year'], bins=bins)
    plt.xlabel('Year')
    plt.ylabel('Total Movies')
    
#movie_inflate_plots()

def tix_inflate():
    
    tix_adjust = []
    tix_df = ticket_prices()
    ave_cpi = cpi_values()
    cpi_2018 = ave_cpi['2018']
    

    while min(tix_df.index) < min(ave_cpi.index):
        minimum = min(tix_df.index)
        tix_df = tix_df.drop([minimum])
       
    for (idx, row) in tix_df.iterrows():
        
        year_cpi = ave_cpi[idx]
        year_adjust = (tix_df.Prices[idx] * cpi_2018) / year_cpi
        tix_adjust.append(year_adjust)
        
    tix_df['Adjust_tix'] = pd.Series(tix_adjust, index=tix_df.index)
    
    return tix_df

def cpi_tix_inflate_plots():
    
    ave_cpi = cpi_values()
    years = ave_cpi.index.values.astype(int)
    year_average_cpi = np.array(ave_cpi)
    tix_df = tix_inflate()

    # Plot average annual CPI through time
    plt.figure()
    plt.plot(years, year_average_cpi, marker='*', linestyle='none')
    plt.xticks(np.arange(1910, 2020+1, 10))
    plt.xlabel('Year')
    plt.ylabel('Average CPI')
    plt.title('Average CPI through time')
    plt.show()
    
    years = tix_df.index.values.astype(int)
    fig, ax1 = plt.subplots()
    plt.plot(years, tix_df.Prices, label='Ticket Prices')
    plt.plot(years, tix_df.Adjust_tix, label='Adjusted Ticket Prices')
#   plt.legend(loc=4)
    plt.legend()
    plt.xticks(np.arange(1920, 2020+1, 10))
    plt.ylim([0, 11])
    plt.xlabel('Year')
    plt.ylabel('Average Ticket Prices ($)')

#cpi_tix_inflate_plots()

def movies_by_year():
    
    df = movie_inflate()
    
    groupby_movies = df['Adjust_DomBO'].groupby(df['Year'])
    year_sum = groupby_movies.sum()
    year_mean = groupby_movies.mean()
    year_max = groupby_movies.max()
    year_median = groupby_movies.median()

    # Plot of mean, max, & median movies' adjusted domestic box office by year
    fig, ax = plt.subplots()
    plt.scatter(year_mean.index, year_mean, marker='*', s=30, color='b', 
                label='Mean')
    plt.scatter(year_max.index, year_max, marker='^', s=30, color='k', 
                label='Max')
    plt.scatter(year_median.index, year_median, marker='p', s=30, color='m', 
                label='Median')
    plt.legend(loc=3)
    plt.xlabel('Year')
    plt.ylabel('Adjusted Domestic Box Office')
    plt.xlim([min(year_mean.index)-2, max(year_mean.index)+2])
    ax.set_yscale('log')
    plt.ylim([10**5, 10**10])

    # Boxplot of adjusted domestic box office by year
    plt.figure()
    ax1 = sns.boxplot(x='Year', y='Adjust_DomBO', data=df, fliersize=5)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(90)
    ax1.set_yscale('log')
    plt.xlabel('Year')
    plt.ylabel('Adjusted Domestic Box Office')
    plt.title('Adjusted Domestic Box Office By Year')
    
    # Scatterplot of adjusted domestic box office by year
    plt.figure()
    ax1 = sns.stripplot(x='Year', y='Adjust_DomBO', data=df)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(90)
    ax1.set_yscale('log')
    plt.xlabel('Year')
    plt.ylabel('Adjusted Domestic Box Office')
    plt.title('Adjusted Domestic Box Office By Year')
    
    return groupby_movies

def ticket_sales():
    
    movies_df = movie_inflate()
    tix_df = tix_inflate()
    tix_sold = []
    
    for index, row in movies_df.iterrows():

        movie_year = str(movies_df.Year[index])
        
        if movie_year in tix_df.index:            
            year_tix = tix_df.Adjust_tix[movie_year]
            tix = movies_df.Adjust_DomBO[index] / year_tix
            tix_sold.append(tix)
        else:
            movies_df.drop(index, inplace=True)
            
    movies_df['Tix_sold'] = pd.Series(tix_sold, index=movies_df.index)
    
    return(movies_df)
    
# Only uncomment if re-running the website scraping to update the movie file
#movie_list()

# Calling other functions individually
#movies_df = movie_inflate()
#tix_df = tix_inflate()  
#inflation = inflation_rates()   # Not using this function anymore
#cpi = cpi_values()
#tix = ticket_prices()
grouped = movies_by_year()
#movies_df = ticket_sales()

#top_100 = movies_df.nlargest(100, 'Tix_sold')
#
#fig, ax = plt.subplots()
#plt.scatter(top_100.Year, top_100.Tix_sold)
#ax.set_yscale('log')
#plt.xlabel('Year')
#plt.ylabel('Tickets Sold')
#
#'''
#Divide by the number of movies each year?
#
#'''

#grouped.describe()

## A way to pull out all the movies from 1988
#print(movies_df[movies_df.Year.isin([1988])])
#
## Cool ways to get top grossing film, and top 10 grossing films
#print(movies_df.loc[movies_df['Adjust_DomBO'].idxmax()])
#print(movies_df.nlargest(10, 'Adjust_DomBO'))
