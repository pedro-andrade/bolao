BEGIN;

INSERT INTO worldcup2014_matchstriker VALUES (1, 1, 111);
UPDATE worldcup2014_match SET winner_id = 5 WHERE id = 1;
UPDATE worldcup2014_match SET score = '2-0' WHERE id = 1;

INSERT INTO worldcup2014_matchstriker VALUES (2, 2, 582);
UPDATE worldcup2014_match SET winner_id = 26 WHERE id = 2;
UPDATE worldcup2014_match SET score = '1-1' WHERE id = 2;

COMMIT;