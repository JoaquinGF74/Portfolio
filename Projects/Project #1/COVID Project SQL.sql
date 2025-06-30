
select *
from PortfolioProject..CovidDeaths
Where continent is not null

--select *
--from PortfolioProject..CovidVaccinations
--order by 3, 4

--Likelihood of dying from covid in your country
Select location, date, population,total_cases, round((total_cases/population)*100, 2) as PercentPopulationInfected
From PortfolioProject..CovidDeaths
where population IS NOT NULL
order by 1, 2

-- Looking at countries with highest infection rate compared to population
Select location, population, MAX(total_cases) as HighestInfectedCount, MAX((total_cases/population))*100 as PercentPopulationInfected
From PortfolioProject..CovidDeaths
where population IS NOT NULL
group by location, population
order by PercentPopulationInfected desc

-- Countries with the highest death count per population
Select location, MAX(cast(total_deaths as bigint)) as TotalDeathCount
From PortfolioProject..CovidDeaths
--where population IS NOT NULL
Where continent is null
group by location
order by TotalDeathCount desc

-- Showing continents with the highest death counts
Select continent, MAX(cast(total_deaths as bigint)) as TotalDeathCount
From PortfolioProject..CovidDeaths
--where population IS NOT NULL
Where continent is not null
group by continent
order by TotalDeathCount desc

-- Global Numbers
Select date, SUM(new_cases) as TotalCases, SUM(cast(new_deaths as bigint)) as TotalDeaths, SUM(cast(new_deaths as bigint))/SUM(new_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
where population IS NOT NULL and continent is not null
group by date
order by 1, 2


-- Looking at toal population vs vaccination
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as bigint)) OVER 
(Partition by dea.location order by dea.location, dea.date) as RollingPeopleVacc
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.location = vac.location
and dea.date = vac.date
where dea.continent is not null and population is not null
order by 2, 3

-- Use of CTE
With PopVsVacc(continent, location, date, population, new_vaccinations, RollingPeopleVacc)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as bigint)) OVER 
(Partition by dea.location order by dea.location, dea.date) as RollingPeopleVacc
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.location = vac.location
and dea.date = vac.date
where dea.continent is not null and population is not null
)
select *, round((RollingPeopleVacc/population)*100, 2)
from PopVsVacc

-- Temp table
DROP table if exists #PercentPopulationVaccinated 
create table #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccination numeric,
RollingPeopleVacc numeric
)
insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as bigint)) OVER 
(Partition by dea.location order by dea.location, dea.date) as RollingPeopleVacc
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.location = vac.location
and dea.date = vac.date
where dea.continent is not null and population is not null
select *, round((RollingPeopleVacc/population)*100, 2)
from #PercentPopulationVaccinated

--create view to store data for later use

USE PortfolioProject
GO
create view PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as bigint)) OVER 
(Partition by dea.location order by dea.location, dea.date) as RollingPeopleVacc
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.location = vac.location
and dea.date = vac.date
where dea.continent is not null and population is not null

select *
from PercentPopulationVaccinated
