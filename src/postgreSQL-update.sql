-- Update name for Jim Beam
UPDATE employees
SET first_name = 'Juan',  -- Replace 'NewFirstName' with the desired new first name
    last_name = 'Pérez'     -- Replace 'NewLastName' with the desired new last name
WHERE employee_id = 5;

-- Update name for Jane Doe
UPDATE employees
SET first_name = 'Eva',  -- Replace 'AnotherNewFirstName' with the new first name
    last_name = 'Smith'     -- Replace 'AnotherNewLastName' with the new last name
WHERE employee_id = 4;

-- Update name for Jhon Doe
UPDATE employees
SET first_name = 'Phill',  -- Replace 'AnotherNewFirstName' with the new first name
    last_name = 'Spencer'     -- Replace 'AnotherNewLastName' with the new last name
WHERE employee_id = 2;
