INSERT INTO task (name, description, expire)
VALUES ('poin', 'ppoin poin', '2025-11-08 10:20:30');


INSERT INTO task (name, description)
VALUES ('poin', 'ppoin poin')

-- Com o campo tipo datetime
INSERT INTO task (name, description, expire)
VALUES ('poin', 'ppoin poin', variável);

-- Com o campo tipo number
INSERT INTO task (name, description, expire)
VALUES ('poin', 'ppoin poin', DATE_ADD(NOW(), INTERVAL variável DAY));


SELECT 
    id,
    date,
    name,
    description,
    expire,
    TIMESTAMPDIFF(DAY, date, NOW()) AS dias_passados,
    TIMESTAMPDIFF(DAY, NOW(), expire) AS dias_restantes
FROM 
    task
WHERE 
    status = 'pen';  -- opcional, se você quiser filtrar apenas tarefas pendentes