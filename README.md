# adBot
This bot receives as input a list of domains and keywords for each one of them and runs infinitely until the ad budget for the selected keywords has been depleted.

It uses selenium webdriver (regular browser) to scrape ad URLs for each keyword-domain combination and saves them in an array.
Then TOR browser is used to simulate a real visit to the URL, using a different IP address each time. Every time, after executing all visits
a new search is performed for each domain stacking the array with URLs and requests are done to every URL in the array including the old ones.
That happens because they don't expire (meaning they still charge the victim, so damage is done in less time). The script runs in a loop and each time 
a certain domain is not found using the selected keywords, it gets removed from the array. Once the array has been emptied, the script is run 4 additional 
times to ensure that the ad budget for each domain-keyword combo has been indeed depleted.

**Python Dependencies:**

- selenium
- tbselenium
- torrequest


**Linux packages:**

- chromium-chromedriver (for selenium)
- geckodriver v 0.17 (for tbselenium)
- torbrowser binary

**Environment Setup:**
In order to run the script you need to install some Python and system dependencies, as well as do an essential configuration. For a complete environment setup, please feel free to contact me. I can provive a Linux Virtual Machine with everything pre-installed and ready to use.


**_Disclaimer:  This bot was made solely for educational purposes, aiming to expose security flaws on Google's Adwords platform. Please test this bot on your own funded account. I am not responsible for any misuse of this script._**
