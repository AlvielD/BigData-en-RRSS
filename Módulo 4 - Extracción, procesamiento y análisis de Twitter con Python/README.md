# Module 4 - Extraction, processing and analysis of Twitter with Python

**Teacher of the module:**
- Jacinto Mata

**Contents:**
- Extraction of data through the Python Twitter's API ([Tweepy](https://www.tweepy.org/)).
- Text processing: Tokenizatio, normalization and management of the data.
- Clasification of documents: Sentiment analysis.

**Developed project:**

The script developed on the jupyter notebook works as follows:

Downloads using api.search() function, the last 500 last tweets, exclusing RTs and saves the result on a dataframe containing the following information:

- Date of the tweet
- User's name
- Text of the tweet
- Number of RTs

 The criteria used for the search are:

 - Contains "ONG" or "Inmigrante" 
 - Date of the tweet must be 28/01/2021
 - Written in Spanish

Then a plot is generated showing the 5 users that has tweeted the most in the downloaded dataset.

*Please, notice the functions and methods used in the notebook are already out-dated. The notebook is most likely to not work anymore.*
