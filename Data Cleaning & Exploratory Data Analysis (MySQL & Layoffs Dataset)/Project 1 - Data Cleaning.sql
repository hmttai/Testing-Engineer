-- DATA CLEANING

SELECT *
FROM layoffs;

-- create a staging table. This is the one we will work in and clean the data. We want a table with the raw data in case something happens
CREATE TABLE layoffs_staging
LIKE layoffs;

INSERT layoffs_staging
SELECT *
FROM layoffs;

SELECT *
FROM layoffs_staging;

-- follow a few steps:
-- 1. check for duplicates and remove any
-- 2. standardize data and fix errors
-- 3. Look at null values and see what 
-- 4. remove any columns and rows that are not necessary - few ways


-- -------------------------
-- 1. Remove Duplicates

# First let's check for duplicates
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 'date', stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
;

WITH duplicate_cte AS
(
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 'date', stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
SELECT *
FROM duplicate_cte
WHERE row_num > 1
;

-- look at oda to confirm
SELECT *
FROM layoffs_staging
WHERE company = 'Oda';

-- create a new table with a new column and add those row numbers in. Then delete where row numbers are over 2, then delete that column
-- these are the ones we want to delete where the row number is > 1 or 2 or greater essentially
CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;

INSERT INTO layoffs_staging2
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 'date', stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
;

DELETE
FROM layoffs_staging2
WHERE row_num > 1;

SELECT *
FROM layoffs_staging2;


-- -------------------
-- 2. Standardize Data

-- handle multiple names come from 1 company
UPDATE layoffs_staging2
SET company = TRIM(company)
;

-- noticing that the Crypto has multiple different variations. We need to standardize that - let's say all to Crypto
UPDATE layoffs_staging2
SET industry = 'Crypto'
WHERE industry LIKE 'Crypto%'
;

-- we have some "United States" and some "United States." with a period at the end.
SELECT distinct industry
FROM layoffs_staging2
ORDER BY industry ASC;

SELECT DISTINCT country
FROM layoffs_staging2
ORDER BY 1;

UPDATE layoffs_staging2
SET country = TRIM(TRAILING '.' FROM country);

-- fix date column
SELECT `date`, STR_TO_DATE(`date`, '%m/%d/%Y')
FROM layoffs_staging2
;

UPDATE layoffs_staging2
SET `date` = STR_TO_DATE(`date`, '%m/%d/%Y')
;

-- convert the data type properly
ALTER TABLE layoffs_staging2
MODIFY COLUMN `date` DATE
;

select * from layoffs_staging2
where industry is null;

-- handle industry column
-- the blanks to nulls since those are typically easier to work with
update layoffs_staging2
set industry = null 
where industry = ''
;

-- now we need to populate those nulls if possible
select s1.company, s1.industry, s2.company, s2.industry
from layoffs_staging2 s1 join layoffs_staging2 s2 on s1.company = s2.company
	and s1.industry is null and s2.industry is not null
;

update layoffs_staging2 s1 join layoffs_staging2 s2 on s1.company = s2.company
set s1.industry = s2.industry where s1.industry is null and s2.industry is not null
;

select *
from layoffs_staging2
where company is null
;


-- ------------------------------------------
-- 3. Look at Null Values
-- the null values in total_laid_off, percentage_laid_off, and funds_raised_millions all look normal. So there isn't anything I want to change with the null values


-- ------------------------------------------
-- 4. remove any columns and rows which are useless

delete
from layoffs_staging2
where total_laid_off is null
and percentage_laid_off is null
;

alter table layoffs_staging2
drop column row_num;

select *
from layoffs_staging2
;


