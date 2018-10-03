# utah-concert-review
Django crud app using scrapy

An effort to scrape concert data from multiple concert venue websites and input them into a database as an aggregate for users to utilize.

#Dependencies
Django
Scrapy

#Description
Web application where client side features input text boxes that make ajax calls to the views.py that filter the database and retrieve records based off user input in order of current date.

A form to create new concerts in the database.

A button that when clicked, runs scrapy from a script, which scrapes concert information from 11 different websites each having their own parse function to extract the required data since every venue website is different.

Scrapy runs from concerts_spider.py which immediately runs the start_requests() function that makes Http requests using scrapy to the venue websites.  The data is returned and parsed by the associated parsing function.  Not all of the data is given in the same format.  I.e. months are sometimes 'September' or 'Sept' or '9'.  In order to retrieve records in the proper order, the models.py has IntegerField() for the columns of 'month', 'day', and 'year', thus the returned data which is all in string format must be converted to Int.  

The parsing function organizes the data into a dictionary that gets its format from the items.py (file that is created when a new scrapy project is created).  It then 'yield's that data or passes it to the pipelines.py which is where I placed my logic to save it to the database.

This application will be used as an aggregate for concerts in the state of Utah and might possibly be turned into an API in json format for other applications to use.
