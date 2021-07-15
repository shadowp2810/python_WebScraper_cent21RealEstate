#!/usr/bin/env python
# coding: utf-8

# In[121]:


import requests
from bs4 import BeautifulSoup

r = requests.get( 
        "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/" , 
         headers = {
             'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0' } )
c = r.content

soup = BeautifulSoup( c , "html.parser" )
# print( soup.prettify() )

all = soup.find_all( 
        "div" , 
        { "class" : "propertyRow" } )

# all   # len( all )   # all[ 0 ]

all[ 0 ].find( 
    "h4" , 
    { "class" : "propPrice" } ).text.replace( 
        "\n" , "" ).replace( " " , "" )


# In[122]:


l = [] #list to store dictionaries of items

for item in all:
    d = {} #dictionary to store all items
    
    d[ "Price" ] = item.find( "h4" , 
        { "class" , "propPrice" } ).text.replace( 
            "\n" , "" ).replace( " " , "" ) 
    
    d[ "Address" ] = item.find_all( "span" , 
        { "class" , "propAddressCollapse" } )[0].text 
          
    d[ "Locality" ] = item.find_all( "span" , 
        { "class" , "propAddressCollapse" } )[1].text 
    
    try:
        d[ "Beds" ] = item.find( "span" , 
        { "class" , "infoBed"} ).find( "b" ).text 
    except:
        d[ "Beds" ] = None
    
    try:
        d[ "Area" ] = item.find( "span" , 
        { "class" : "infoSqFt"} ).find( "b" ).text 
    except:
        d[ "Area" ] = None 
    
    try:
        d[ "Full Bath" ] = item.find( "span" , 
        { "class" : "infoValueFullBath"} ).find( "b" ).text 
    except:
        d[ "Full Bath" ] = None 
    
    try:
        d[ "Half Bath" ] = item.find( "span" , 
        { "class" : "infoValueHalfBath"} ).find( "b" ).text 
    except:
        d[ "Half Bath" ] = None 

    for column_group in item.find_all( 
            "div" , { "class" , "columnGroup" } ) :
        # print( column_group )
        for feature_group , feature_name in zip( 
                column_group.find_all( "span" , 
                    { "class" , "featureGroup" } ) ,
                column_group.find_all( "span" , 
                    { "class" , "featureName" } ) ) :
            if "Lot Size" in feature_group.text :
                d[ "Lot Size" ] = feature_name.text 

                
    l.append( d )

l


# In[123]:


import pandas
df = pandas.DataFrame( l ) 
df


# In[124]:


df.to_csv( "Output.csv" )


# In[130]:


l_allPages = [] #list to store dictionaries of items

final_page_nbr = soup.find_all( 
    "a" , 
    { "class" : "Page" } )[-1].text

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range( 0 , int( final_page_nbr ) * 10 , 10 ) :
    print( base_url + str( page ) + ".html" )

    r = requests.get( 
        ( base_url + str( page ) + ".html" ) , 
         headers = {
             'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0' } )
    c = r.content

    soup = BeautifulSoup( c , "html.parser" )
    
    # print( soup.prettify() )
    
    all = soup.find_all( 
        "div" , 
        { "class" : "propertyRow" } )
    
    
    for item in all:
        d = {} #dictionary to store all items

        d[ "Price" ] = item.find( "h4" , 
            { "class" , "propPrice" } ).text.replace( 
                "\n" , "" ).replace( " " , "" ) 

        d[ "Address" ] = item.find_all( "span" , 
            { "class" , "propAddressCollapse" } )[0].text 
        
        try:
            d[ "Locality" ] = item.find_all( "span" , 
                { "class" , "propAddressCollapse" } )[1].text 
        except:
            d[ "Locality" ] = None

        try:
            d[ "Beds" ] = item.find( "span" , 
            { "class" , "infoBed"} ).find( "b" ).text 
        except:
            d[ "Beds" ] = None

        try:
            d[ "Area" ] = item.find( "span" , 
            { "class" : "infoSqFt"} ).find( "b" ).text 
        except:
            d[ "Area" ] = None 

        try:
            d[ "Full Bath" ] = item.find( "span" , 
            { "class" : "infoValueFullBath"} ).find( "b" ).text 
        except:
            d[ "Full Bath" ] = None 

        try:
            d[ "Half Bath" ] = item.find( "span" , 
            { "class" : "infoValueHalfBath"} ).find( "b" ).text 
        except:
            d[ "Half Bath" ] = None 

        for column_group in item.find_all( 
                "div" , { "class" , "columnGroup" } ) :
            # print( column_group )
            for feature_group , feature_name in zip( 
                    column_group.find_all( "span" , 
                        { "class" , "featureGroup" } ) ,
                    column_group.find_all( "span" , 
                        { "class" , "featureName" } ) ) :
                if "Lot Size" in feature_group.text :
                    d[ "Lot Size" ] = feature_name.text 

        l_allPages.append( d )

l_allPages


# In[131]:


import pandas
df = pandas.DataFrame( l_allPages ) 
df


# In[132]:


df.to_csv( "Output_allPages.csv" )

