# **COVID Statistics 2020-2021**

![COVID Infection Forecasting](https://raw.githubusercontent.com/JoaquinGF74/Portfolio/main/assets/covid_dashboard_img.png)

### **Project Overview**

This Project focuses on the analysis and visualization of infection and death cases throughout all 7 contients using **SQL** and **Tableau**. The goal was to clean, process, and analyze when, and how many deaths were relative to the infected ratio by country.

## **Objectives**

- **Data Cleaning & Processing:** Handle missing values, rename columns, and correct inconsistencies in data.
- **Country-Based Segmentation:** Split the dataset based on countries with highest infection rates and deaths.
- **Data Aggregation:** Summarize key metrics such as population vs vaccination, and Death per infection %.
- **Interactive Dashboard:** Develop a Tableau dashboard to visualize forecasting, and key data.
  
## **Methodology**

### 1. Creation of source tables

- **SQL** was key to perform the analysis and understanding of the data, allowing the representation of multiple measures.

### 2. Data Processing with SQL

- Dropped unnecesary columns to reduce redudancy and optimize processing.
- Standardized date format for better consistency.
- Made sure to assign countries with their respective country code accordingly.
- Handled missing values, since the original file had discrepancies in the showcase of the data.
- Renamed columns for a better comprehensionn of each field. 

### 3. Tableau Dashboard:
- Visualized Global Infected/Death %, Deaths per Continent, % of Population infected by country, and Avegare infected rate.
- Created scalar graphs, alongside a map visualization tool, and a forecasting line graph. 

## Key Insights
- The United States of America led the average population infected rate, having and average of 9% of their population infected by the begining of 2021, which forecasted to achieve a total of a 19% by the end of that year with similar numbers.
- The total of Europe led the death count, this can be interpreted as the % of old population in the continent adn the geopolitical locations.
- Countries in Asia --China, Korea, Japan-- and Oceania --New Zealand, Australia--, showcased a very low number of infected/deaths by the beginning of 2021.

### Technologies Used

- `SQL`: Data processing, data cleaning, and data interpretation.
- `Tableau`: Data visualization and dashboard creation.

## Conclusion

## SQL Code:
```SQL
-- Global Numbers
SELECT 
  SUM(new_cases) AS TotalCases, 
  SUM(CAST(new_deaths AS bigint)) AS TotalDeaths, 
  SUM(CAST(new_deaths AS bigint)) * 100.0 / NULLIF(SUM(new_cases), 0) AS DeathPercentage
FROM PortfolioProject..CovidDeaths
WHERE continent IS NOT NULL;

-- Countries with the highest death count per population
SELECT location, MAX(cast(total_deaths as bigint)) AS TotalDeathCount
FROM PortfolioProject..CovidDeaths
WHERE continent IS NULL AND location NOT IN ('World', 'European Union', 'International')
BROUP BY location
ORDER BY TotalDeathCount desc

-- Looking at countries with highest infection rate compared to population
SELECT location, population, date, MAX(total_cases) AS HighestInfectedCount, MAX((total_cases/population))*100 AS PercentPopulationInfected
FROM PortfolioProject..CovidDeaths
WHERE population IS NOT NULL
GROUP BY location, population, date
ORDER BY PercentPopulationInfected desc
```

## Tableau Public link: 
[COVID Dashboard 2020-2021](https://public.tableau.com/views/CovidDashboard2020-2021_17513011312390/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

### [Back](https://joaquingf74.github.io/Portfolio/Projects.html)
