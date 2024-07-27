-- Exploratory Data Analysis project



-- 1)Basic Statistics and Data Quality Checks
-- Calculate summary statistics (mean, median, mode, etc.) for numeric columns.
SELECT MAX(total_laid_off) AS max_total_laid_off,MIN(total_laid_off) AS min_total_laid_off,AVG(total_laid_off) AS avg_total_laid_off,
MAX(percentage_laid_off) AS max_percentage_laid_off,MIN(percentage_laid_off) AS min_percentage_laid_off,AVG(percentage_laid_off) AS avg_percentage_laid_off,
MAX(funds_raised_millions) AS max_funds_raised,MIN(funds_raised_millions) AS min_funds_raised,AVG(funds_raised_millions) AS avg_funds_raised
FROM layoffs_clean;
--  Check for Missing Values
SELECT
    COUNT(*) - COUNT(company) AS missing_company,
    COUNT(*) - COUNT(location) AS missing_location,
    COUNT(*) - COUNT(industry) AS missing_industry,
    COUNT(*) - COUNT(total_laid_off) AS missing_total_laid_off,
    COUNT(*) - COUNT(percentage_laid_off) AS missing_percentage_laid_off,
    COUNT(*) - COUNT(date) AS missing_date,
    COUNT(*) - COUNT(stage) AS missing_stage,
    COUNT(*) - COUNT(country) AS missing_country,
    COUNT(*) - COUNT(funds_raised_millions) AS missing_funds_raised
FROM layoffs_clean;
--  Distribution Analysis
-- total laid off by each company
SELECT company,SUM(total_laid_off) AS total
FROM layoffs_clean
GROUP BY company
ORDER BY total DESC;
-- total funds raised by each company
SELECT DISTINCT	company , funds_raised_millions
FROM layoffs_clean ;
-- number of companies in each industry
SELECT industry,COUNT(*) AS nb_companies
FROM layoffs_clean
GROUP BY industry
ORDER BY nb_companies DESC;
-- number of companies in each country
SELECT country,COUNT(*) AS nb_companies
FROM layoffs_clean
GROUP BY country
ORDER BY nb_companies DESC;
-- number of companies by stage
SELECT stage,COUNT(*) AS nb_companies
FROM layoffs_clean
GROUP BY stage
ORDER BY nb_companies DESC;
-- total of laid offs for each country
SELECT country,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY country
ORDER BY total_laid_offs DESC;
-- total of laid offs for each industry
SELECT industry,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY industry
ORDER BY total_laid_offs DESC;
-- total of laid offs for each stage
SELECT stage,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY stage
ORDER BY total_laid_offs DESC;
-- Layoffs by location
SELECT location, SUM(total_laid_off) AS total_laid_off
FROM layoffs_clean
GROUP BY location
ORDER BY total_laid_off DESC;
-- total laid offs per month
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month_date, 
    COUNT(*) AS layoffs_count,
    SUM(total_laid_off) AS total_laid_off
FROM layoffs_clean
GROUP BY month_date
ORDER BY month_date;
-- total laid offs per year
SELECT 
    DATE_FORMAT(date, '%Y') AS year_of, 
    COUNT(*) AS layoffs_count,
    SUM(total_laid_off) AS total_laid_off
FROM layoffs_clean
GROUP BY year_of
ORDER BY year_of;
-- top three industries that laid off people
SELECT industry,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY industry
ORDER BY total_laid_offs DESC LIMIT 3;
-- top three countries that laid off people
SELECT country,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY country
ORDER BY total_laid_offs DESC LIMIT 3;
-- top three stages that laid off people
SELECT stage,SUM(total_laid_off) AS total_laid_offs
FROM layoffs_clean
GROUP BY stage
ORDER BY total_laid_offs DESC LIMIT 3;
-- top three richest countries by funds raised
SELECT country,SUM(funds_raised_millions) AS total_funds_millions
FROM layoffs_clean
GROUP BY country
ORDER BY total_funds_millions DESC LIMIT 3;
-- top five richest companies by funds raised
SELECT DISTINCT company,funds_raised_millions
FROM layoffs_clean
ORDER BY funds_raised_millions DESC LIMIT 5;

-- Companies with highest percentage laid off
SELECT company, percentage_laid_off
FROM layoffs_clean
ORDER BY percentage_laid_off DESC
LIMIT 10;
-- Companies with lowest percentage laid off
SELECT company, percentage_laid_off
FROM layoffs_clean
WHERE percentage_laid_off IS NOT NULL
ORDER BY percentage_laid_off ASC
LIMIT 10;
-- Relationship between funds_raised_millions and total_laid_off
SELECT funds_raised_millions,total_laid_off,industry
FROM layoffs_clean
WHERE funds_raised_millions IS NOT NULL AND total_laid_off IS NOT NULL
ORDER BY funds_raised_millions;