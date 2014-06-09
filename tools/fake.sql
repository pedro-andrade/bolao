BEGIN;

INSERT INTO worldcup2014_matchstriker VALUES (1, 1, 111);
UPDATE worldcup2014_match SET winner_id = 5 WHERE id = 1;
UPDATE worldcup2014_match SET score = '2-0' WHERE id = 1;

INSERT INTO worldcup2014_matchstriker VALUES (2, 2, 651);
UPDATE worldcup2014_match SET winner_id = 26 WHERE id = 2;
UPDATE worldcup2014_match SET score = '1-1' WHERE id = 2;

INSERT INTO worldcup2014_vote VALUES (1, 1, 'pedro', 1, 5, '2-0');
INSERT INTO worldcup2014_vote VALUES (2, 2, 'pedro', 10, 10, '10-10');
INSERT INTO worldcup2014_vote VALUES (3, 1, 'teresa', 10, 10, '10-10');
INSERT INTO worldcup2014_vote VALUES (4, 2, 'teresa', 3, 26, '1-1');

COMMIT;