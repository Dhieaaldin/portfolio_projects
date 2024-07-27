-- 1) remove duplicates
-- 2) standarize data
-- 3) null or blank values?
-- 4) deleting useless data
-- CREATING A COPY OF THE DATA
CREATE TABLE layoffs_copy
LIKE layoffs_raw;
INSERT INTO layoffs_copy
SELECT *
FROM layoffs_raw;
-- adding a unique identifier to layoffs_copy
ALTER TABLE layoffs_copy
ADD COLUMN company_id INT UNIQUE AUTO_INCREMENT;
-- 1) identifiying and deleting duplicate rows
WITH duplicates_count_cte AS (
SELECT  company ,location,industry,total_laid_off,percentage_laid_off,`date`,stage,country,company_id ,ROW_NUMBER() OVER(PARTITION BY company ,location,industry,total_laid_off,percentage_laid_off,`date`,stage,country,funds_raised_millions) num 
FROM layoffs_copy)
DELETE FROM layoffs_copy
WHERE company_id IN (SELECT company_id FROM duplicates_count_cte WHERE num >1) ;

-- 2) standarizing data
-- creating a procedure to select a column from a table
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `show`(IN x VARCHAR(64), IN y VARCHAR(64))
BEGIN
    SET @sql = CONCAT('SELECT DISTINCT ', x, ' FROM ', y,' ORDER BY 1');
    PREPARE qry FROM @sql;
    EXECUTE qry;
    DEALLOCATE PREPARE qry;
END$$
DELIMITER ;
-- selecting company column
CALL `show`("company","layoffs_copy");
CALL `show`("location","layoffs_copy");
CALL `show`("industry","layoffs_copy");
CALL `show`("country","layoffs_copy");
-- i created a saved procedure to trim and remove any comas at the end of a value in the dataset
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `clean`(IN x VARCHAR(64),IN y VARCHAR(64))
BEGIN
    SET @sqlqry = CONCAT('UPDATE ',y,' SET ', x, ' = TRIM(TRAILING ''.'' FROM TRIM(', x, ')) WHERE ', x, ' LIKE ''%.'' OR ', x, ' != TRIM(', x, ');');
    
    PREPARE qry FROM @sqlqry;
    EXECUTE qry;
    DEALLOCATE PREPARE qry;
END$$
DELIMITER ;
CALL clean("company","layoffs_copy");
CALL clean("location","layoffs_copy");
CALL clean("industry","layoffs_copy");
CALL clean("country","layoffs_copy");
-- after runnig the querry above i noticed that the Crypto 
-- industry is named differently with 2 other names so i will update all to Crypto
UPDATE layoffs_copy
SET industry = "Crypto"
WHERE industry LIKE "Crypto%";
-- updating the date column values's format and type from text to date 
UPDATE layoffs_copy
SET `date`=str_to_date(`date`,'%m/%d/%Y');
ALTER TABLE layoffs_copy
MODIFY COLUMN `date` DATE;
-- 3) dealing with null and blank values
-- first i will start by creating a procedure to change any blank value to a null value
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `blankTOnull`(IN x VARCHAR(64),IN y VARCHAR(64))
BEGIN
    SET @sqlqry = CONCAT('UPDATE ', y, ' SET ', x, ' = NULL WHERE ', x, ' = \'\'');
    
    PREPARE qry FROM @sqlqry;
    EXECUTE qry;
    DEALLOCATE PREPARE qry;
END $$
DELIMITER ;
-- i called the procedure on the industry column
CALL blankTOnull("industry","layoffs_copy");
-- next i will be making a self join on the company name to fill the data with the same industry
-- from the same company if existed
UPDATE layoffs_copy l1
JOIN layoffs_copy l2 ON l1.company=l2.company
SET l1.industry=l2.industry
WHERE l1.industry IS NULL AND l2.industry IS NOT NULL;
SELECT * FROM layoffs_copy WHERE industry IS NULL;
-- 4 ) deleting useless data
-- i am cleaning this data for a next project wich will be an exploratory data analysis with MySQL
-- and i came to a conclusion that any rows without a total laid off number 
-- and the percentage laid off won't be useful SO they will be deleted 

DELETE FROM layoffs_copy
WHERE percentage_laid_off IS NULL AND total_laid_off IS NULL;
-- i will also delete the column that i added wich is company_id
ALTER TABLE layoffs_copy
DROP COLUMN company_id; 
-- selecting all rows and columns
SELECT *
FROM layoffs_copy;
-- END OF PROJECT
