# CB_Lab_Mapping_Economic_Migration
Mapping the economic migration of mini-grid communities 


Environment
A reasonably up-to-date Python environment is required to run this code. Perhaps the easiest way to satisfy all dependencies is to use the provided environment.yml file by running the command

conda env create -f environment.yml

and by activating the environment in all subsequent sessions with:

conda activate CB_Lab_Mapping_Economic_Migration-env

A quick description of the main dependencies is:

python: This has been tested on Python 3.9, though it's expected that anything released after 3.6 or so ought to work.
pip: For package management.
numpy: For array manipulation.
pandas: For loading and handling the alternative CSV files for this data.
plotly: For interactive visualizations.
pyyaml: For parsing config files, etc.
dash: Interactive dashboard library
sklearn: Clustering algorithms used within dash.
Config files
You will need to create and update your user-specific configuration details. Make a copy of user_config_sample.yml and rename it user_config.yml. Use any text editor to edit user_config, in particular, the location in your computer where the main CrossBoundary Dropbox folder resides. This generally varies from user to user, and this code will rely on that folder location to find the raw data, create outputs and find reference material.