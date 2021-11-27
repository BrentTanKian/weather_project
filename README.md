# Weather_project
Scrapes the government weather api and provides detailed, granular forecasts/graphs down to a specific area and for up to 4 days ahead.
Running the main.py script will generate a csv file with all the forecast data, and a png file with a graph that shows average temperature
and humidity over the next 4 days. 

To generate a .exe file from the code so that you can simply run the script by double-clicking the exe, follow these steps.

1. Clone the project down into a folder.
2. Via the terminal, cd into the folder and do pipenv install to install required packages
3. Do pipenv shell to get into the environment which you previously installed the packages
4. Do pipenv install pyinstaller
5. Do pyinstaller --onefile main.py
6. And once the previous command runs successfully, you should have a .exe file in the dist folder
