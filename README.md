# Scraping Restaurants

This project aims at extracting a list of restaurants from a places API (TripAdvisor) in given polygon (input .kml format). 

## Getting Started

### Prerequisites

Make sure you have Python 3.6 installed or higher. Also make sure that you have api_keys granting access to the TripAdvisor API and store the credentials in the .env file as environment variables.

### Installing

Open your terminal/command line in the relevant directory which will be the root directory for you project.

Run the following command in the terminal and the code will be copied to your machine in the directory.

```
git clone https://github.com/adrienlin/scraping_restaurants
```

Make sure pip is up to date

```
python -m pip install --upgrade pip
```

Install all the requirements necessary to run the script

```
pip install -r requirements.txt
```

## Execute the script

Drop the .kml that contains your polygon dara in your root directory. Open the scaping_restaurants.py script, change the strings where the comments say INPUT REQUIRED for the script to read the correct .kml file. It should drop the results file in your root directory as a .csv.

### Results explanation

The results breaks down all the details of every restaurant in the area(s) searched.

## Authors

* **Adrien Lin**
