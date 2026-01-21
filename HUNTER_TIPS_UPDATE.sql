-- ============================================================================
-- HUNTER SYSTEM - AGGIORNAMENTO TIPS 2026
-- ============================================================================
-- Tips aggiornati e accurati basati sul sistema reale
-- Rimuove informazioni obsolete e aggiunge consigli utili
-- ============================================================================

USE `srv1_hunabku`;

-- Svuota tabella tips vecchi
TRUNCATE TABLE `hunter_quest_tips`;

-- ============================================================================
-- TIPS CATEGORIA: SISTEMA BASE & RANK
-- ============================================================================

INSERT INTO `hunter_quest_tips` (tip_text) VALUES
('Il Sistema Hunter ha 7 ranghi: E, D, C, B, A, S e il leggendario N (Monarca Nazionale).'),
('Ogni rango ti garantisce un bonus Gloria permanente: Rank D = +1%, C = +3%, B = +5%, A = +7%, S = +10%, N = +12%!'),
('Per avanzare di rango devi completare le Trial (Prove). Aprile dal tab Trial nel terminale Hunter.'),
('Le Trial richiedono: Boss uccisi, Metin distrutti, Fratture sigillate e Bauli aperti. Varia per ogni rango.'),
('Se fallisci una Trial puoi riprovare! Non perdi progressi, devi solo riattivare la prova.'),

-- ============================================================================
-- TIPS CATEGORIA: MISSIONI GIORNALIERE & EVENTI
-- ============================================================================

('Ogni giorno ricevi 3 Missioni Giornaliere alle 05:00. Completale TUTTE per un bonus Gloria x1.5!'),
('Le missioni possono richiedere: uccisioni specifiche, apertura bauli, sigillo fratture o distruzione metin.'),
('Ci sono 27 Eventi Schedulati ogni giorno! Controlla il tab Eventi per vedere orari e premi.'),
('Gli eventi hanno 3 tipi: Gloria Boost (punti extra), Drop Boost (item migliori), Speed Kill (sfide veloci).'),
('Partecipare agli eventi ti registra automaticamente per i sorteggi. Il vincitore riceve premi extra!'),

-- ============================================================================
-- TIPS CATEGORIA: STREAK & BONUS
-- ============================================================================

('Accedi ogni giorno per la Serie Consecutiva! 3 giorni = +3%, 7 giorni = +7%, 30 giorni = +12% Gloria!'),
('Se salti anche UN SOLO giorno perdi la serie e torni a 0%. La costanza è la chiave!'),
('Il bonus Serie + Rango si sommano! Rank N + 30 giorni = +12% + +12% = +24% Gloria totale!'),
('Il tuo bonus giornaliero totale è visibile nel tab Stats sotto "Bonus Giornaliero Totale".'),

-- ============================================================================
-- TIPS CATEGORIA: FRATTURE & DEFENSE
-- ============================================================================

('Le Fratture hanno 7 gradi di difficoltà: E (Verde), D (Blu), C (Arancio), B (Rosso), A (Oro), S (Viola), N (Bianco).'),
('Aprire una Frattura ti mette in modalità Difesa: devi eliminare tutte le ondate di nemici!'),
('Se vinci la difesa, puoi aprire la Frattura e ottenere il tesoro. Se perdi, le Fratture B+ vengono distrutte!'),
('Le Fratture E, D, C rimangono anche se fallisci la difesa. Puoi riprovarci!'),
('In party, TUTTI i membri ottengono credit per le Fratture sigillate. Gioca in gruppo per progredire velocemente!'),

-- ============================================================================
-- TIPS CATEGORIA: GLORIA & SHOP
-- ============================================================================

('Ottieni Gloria uccidendo Elite Mob, Metin e Boss. I punti variano in base alla difficoltà del nemico.'),
('La Gloria si divide in 2 tipi: Totale (per il rank) e Spendibile (per lo shop). Spendi saggiamente!'),
('Lo Shop Hunter ha 12 item esclusivi. Controlla il tab Shop per vedere cosa puoi comprare.'),
('Le transazioni dello shop sono loggate. Gli admin possono vedere tutti gli acquisti, quindi no exploit!'),
('Vuoi salire in classifica? Non spendere Gloria nello shop! Ogni punto conta per la tua posizione.'),

-- ============================================================================
-- TIPS CATEGORIA: ACHIEVEMENTS & RECORD
-- ============================================================================

('Ci sono 12 Achievement totali: 7 basati su kill e 5 basati su Gloria accumulata.'),
('Gli achievement danno ricompense uniche! Controlla il tab Achievements per vederli tutti.'),
('Ogni baule, boss e metin che apri/uccidi viene tracciato per GRADO. Vedi le stats dettagliate nel tab Stats!'),
('Il tuo Win Rate delle difese fratture è visibile nelle statistiche. Cerca di mantenere almeno il 70%!'),
('I bauli N-Rank sono i più rari! Se ne hai aperti molti, sei tra i top player del server.'),

-- ============================================================================
-- TIPS CATEGORIA: PARTY & COMPETIZIONE
-- ============================================================================

('In party, la Gloria viene distribuita in base al "livello di potenza" (Power Rank). I rank alti prendono più punti.'),
('Anche se sei in party, le missioni giornaliere si completano individualmente. Ognuno progredisce le proprie.'),
('La classifica si divide in: Giornaliera, Settimanale e Totale. Controlla il tab Ranking per vedere la tua posizione.'),
('Essere #1 in classifica giornaliera ti da prestigio! Il tuo nome appare in cima alla Sala delle Leggende.'),
('Le classifiche si resettano: Giornaliera alle 05:00, Settimanale ogni Lunedì. La Totale non si resetta mai.'),

-- ============================================================================
-- TIPS CATEGORIA: STRATEGIA AVANZATA
-- ============================================================================

('I Boss Elite (>5000 Gloria) sono difficili ma danno punti enormi. Affrontali in gruppo se possibile!'),
('I Metin Speciali (>1000 Gloria) appaiono durante eventi. Sono più forti ma valgono il doppio!'),
('Vuoi maximizzare la Gloria? Completa le 3 missioni giornaliere, mantieni la serie 30 giorni e sali di rank!'),
('Le Trial hanno un timer! Non lasciare scadere la prova o dovrai ripartire da zero con i requisiti.'),
('Il Sistema traccia TUTTO: kill, defense, bauli per grado, boss per difficoltà. Ogni azione conta!'),

-- ============================================================================
-- TIPS CATEGORIA: MECCANICHE SPECIALI
-- ============================================================================

('I bauli hanno rank proprio come le fratture. Più alto il rank, migliore il loot e la Gloria!'),
('Esistono bauli Jackpot rari che danno Gloria extra o item leggendari. Quando ne trovi uno, sei fortunato!'),
('Le Emergency Quest sono sfide improvvise! Completale in tempo per bonus enormi, ma se fallisci perdi Gloria.'),
('Il terminale Hunter si apre con F10 (default). Usalo spesso per controllare progressi e missioni!'),
('Ogni kill, ogni baule, ogni frattura viene salvata nel database. Il Sistema non dimentica mai.'),

-- ============================================================================
-- TIPS CATEGORIA: CONSIGLI PRATICI
-- ============================================================================

('Non aprire fratture da solo se sei basso livello! Le difese possono essere difficili, cerca un party.'),
('Prima di aprire una frattura, attiva buff e consumabili. La difesa inizia SUBITO dopo l''apertura!'),
('Se vedi una Emergency Quest attiva, fermati e leggila! Ignorarla può farti perdere punti.'),
('Il tab Stats mostra il tuo "Livello di Potere" in stile Solo Leveling. Cerca di raggiungere rank SSS!'),
('Le notifiche Hunter appaiono in alto a destra. Se ne vedi troppe, controlla le impostazioni UI.'),

-- ============================================================================
-- TIPS CATEGORIA: SISTEMA & PERFORMANCE
-- ============================================================================

('Il sistema Hunter usa un sistema di flush: i dati vengono salvati ogni 30 secondi o al logout.'),
('Le statistiche dettagliate sono ottimizzate. Con 500+ player online, il database regge perfettamente!'),
('Le notifiche di traguardo e rank appaiono solo quando hai completato i requisiti reali. Non è un bug!'),
('Se vedi "Trial completata" durante attività normali, hai completato i requisiti senza saperlo. Congratulazioni!'),
('Il Sistema è sicuro contro exploit. Ogni transazione è loggata e monitorata dagli admin. Gioca pulito!');

-- ============================================================================
-- VERIFICA
-- ============================================================================

SELECT COUNT(*) as 'Totale Tips Inseriti' FROM hunter_quest_tips;

-- ============================================================================
-- FINE AGGIORNAMENTO
-- ============================================================================
