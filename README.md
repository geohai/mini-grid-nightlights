# Mini-Grid Nightlights

Code for **“A Light in the Dark: Detectability of Mini-Grid Electrification with Remote Sensing in Sub-Saharan Africa.”**  
This repository contains the Python and R code used to extract geospatial time series, run staggered Difference-in-Differences (DiD) analyses, and generate figures for the paper and supplementary material.

## Repository Structure (in numerical order)

### Python / Jupyter Notebooks
- **01_GetCBILSites.ipynb** – Clean and compile CBIL mini-grid site information.  
- **02_GetNightlightValues.ipynb** – Extract VIIRS DNB nighttime lights for CBIL sites.  
- **03_InitialNightlightsAnalysis.ipynb** – Exploratory analysis of brightness patterns.  
- **06_GetCLUBNightlightValues.ipynb** – Nightlights extraction for CLUB-ER sites.  
- **09_SLGetDarkAreas.ipynb** – Sample dark comparison sites for Sierra Leone.  
- **11_AfricaGetDarkAreas.ipynb** – Sample dark comparison sites across Africa.  
- **13_GetSLPopulationValues.ipynb** – Extract gridded population for Sierra Leone sites.  
- **15_GetCLUBERPopulationValues.ipynb** – Population extraction for CLUB-ER sites.  
- **17_GetCBILPopulationValues.ipynb** – Population extraction for CBIL sites.  
- **19_OEMapsValidation.ipynb** – Validate remote-sensing electricity access maps.  
- **20_MGDistance.ipynb** – Compute site distances and spatial metrics.  
- **21_GetUsageInfo.ipynb** – Usage and revenue data compilation.  
- **22_UsageCorrelations.ipynb** – Correlations between nightlights and usage.  
- **23_MinusOceanDiD.ipynb** – Background-ocean-adjusted DiD prep.  
- **24_MovingAvgDiD.ipynb** – Moving-average preprocessing for robustness checks.  
- **25_GetBackgroundNightlights.ipynb** – Global ocean background signal extraction.

### R / R Markdown (DiD and Statistical Analysis)
- **05_StaggeredDinDSL.Rmd** – Staggered DiD for Sierra Leone.  
- **07_StaggeredDinDcluber.Rmd** – Staggered DiD for CLUB-ER sites.  
- **08_StaggeredDinDSLv2.Rmd** – Revised Sierra Leone DiD model.  
- **10_SLDarkAreaDinD.Rmd** – Sierra Leone DiD using dark-area controls.  
- **12_AfricaDarkAreaDinD.Rmd** – Africa-wide dark-area DiD.  
- **14_PopulationSLDinD.Rmd** – DiD on population for Sierra Leone.  
- **16_PopulationCLUBERDinD.Rmd** – Population DiD for CLUB-ER sites.  
- **18_PopulationCBILDinD.Rmd** – Population DiD for CBIL sites.  
- **26_BackgroundNightlightsAnalysis.Rmd** – Analysis of global background signal.  
- **27_ParallelTrendsTesting.Rmd** – Parallel trends assumption tests.  
- **28_HREAValidation.Rmd** – Validation using external energy access products.


## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/geohai/mini-grid-nightlights.git
cd mini-grid-nightlights
```

### 2. Python environment

Create the Conda environment:

```bash
conda env create -f environment.yml
conda activate CB_Lab_Mapping_Economic_Migration-env
```

### 3. R environment

Install required R packages (see headers of each `.Rmd`):

```r
install.packages(c("tidyverse", "sf", "did", "ggplot2", "rmarkdown"))
```


## Configuration

Copy and edit the sample configs:

```bash
cp user_config_sample.yml user_config.yml
cp .env.example .env
```

Add your local paths and any credentials required for data access.


## Data Availability

* **Public datasets** (VIIRS, population grids, CLUB-ER) can be downloaded via the provided notebooks.
* **Operational mini-grid data** (PowerGen, CBIL) **cannot** be redistributed due to confidentiality.
* Scripts are provided so that users with legitimate access can reproduce the analysis.
