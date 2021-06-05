# SQL Alchemy Challenge

## Task

Using Python and SQLAlchemy to do basic climate analysis and data exploration by connecting to a sqlite database, reflecting the tables into classes and creating a session from Python to the database. 

###Python and SQLAlchemy: Jupyter Notebook

**Precipitation Analysis**
Designed a query to retrieve precipitation data for the last 12 months of data, loading into a Pandas DataFrame and plotting the results and outputting summary statistics. 

**Station Analysis**
Designed a query to calculate most active stations, retrieve the last 12 months of temperature obsveration data (TOBS), filtering by station with the highest number of observations and plotting the results as a histogram with `bins=12`

###Flask App Routes
Using Python library Flask, routes created to retrieve data from the sqlite database as a JSON call. Routes include:
  * `/api/v1.0/precipitation`
  * `/api/v1.0/stations`
  * `/api/v1.0/tobs`
  * `/api/v1.0/temp/<start>`
  * `/api/v1.0/temp/<start>/<end>`

--- 

## Technologies

Python Libraries:
* Pandas
* Numpy
* Datetime
* SQL Alchemy
 * automap_base, Session, create_engine, func
* Flask
  * Flask, jsonify

Jupyter Notebook