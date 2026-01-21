-- ============================================================================
-- HUNTER SYSTEM - AGGIORNAMENTO TIPS 2026 (VERSIONE CORRETTA)
-- ============================================================================
-- Tips aggiornati e accurati basati sul sistema reale
-- Rimuove informazioni obsolete e aggiunge consigli utili
-- CORRETTI: Streak bonus, Party mechanics, Speed Kill, Karma
-- ============================================================================

USE `srv1_hunabku`;

-- Svuota tabella tips vecchi
TRUNCATE TABLE `hunter_quest_tips`;

-- ============================================================================
-- TIPS CATEGORIA: SISTEMA BASE & RANK
-- ============================================================================

INSERT INTO `hunter_quest_tips` (tip_text) VALUES
('Il Sistema Hunter ha 7 ranghi: E, D, C, B, A, S e il leggendario N (Monarca Nazionale).'),
('Ogni rango ti garantisce un bonus Gloria permanente: D=+1%, C=+3%, B=+5%, A=+7%, S=+10%, N=+12%!'),
('Per avanzare da E→D e D→C serve solo gloria. Da C in poi devi completare le Trial (Prove).'),
('Le Trial richiedono Boss, Metin, Fratture e Bauli. Ogni rank ha requisiti diversi. Controlla il tab Trial!'),
('Le Trial B→A, A→S e S→N hanno TEMPO LIMITE! Non far scadere la prova o perdi i progressi.'),

-- ============================================================================
-- TIPS CATEGORIA: MISSIONI GIORNALIERE & RESET
-- ============================================================================

('Ogni giorno alle 05:00 ricevi 3 Missioni Giornaliere. Completale TUTTE per un bonus Gloria x1.5!'),
('Il bonus x1.5 vale FINO AL RESET! Se fai solo 2 missioni su 3, NON ricevi il bonus.'),
('Le missioni NON completate ti danno penalità! Perdi gloria totale e karma. Completa sempre tutte e 3!'),
('I reset sono alle 05:00: Missioni Giornaliere, Classifica Daily, Penalità. Settimanale ogni Lunedì.'),
('Se fallisci troppe missioni consecutive, il Sistema ti marca come "penalty_active" e riduci la gloria.'),

-- ============================================================================
-- TIPS CATEGORIA: PARTY PLAY & COOPERAZIONE
-- ============================================================================

('In party, le FRATTURE condividono progresso! Se un membro sigilla, TUTTI ricevono gloria e missione.'),
('Boss, Metin e Bauli sono INDIVIDUALI! Solo chi uccide/apre riceve il progresso missione.'),
('Questo design premia il gioco di squadra (fratture) ma mantiene la meritocrazia (boss/metin).'),
('Se apri una frattura in party, TUTTI devono stare entro 20m. Se un membro si allontana, difesa fallisce!'),
('La gloria base viene data a TUTTI i membri del party, ma il progresso missioni dipende dal tipo.'),

-- ============================================================================
-- TIPS CATEGORIA: STREAK & KARMA
-- ============================================================================

('Accedi ogni giorno per la Serie Consecutiva! 3 giorni=+5%, 7 giorni=+10%, 30 giorni=+20% Gloria!'),
('Se salti UN SOLO giorno perdi la serie e torni a 0%. La costanza è la chiave del potere!'),
('Bonus Rank + Streak si SOMMANO! Rank N (+12%) + Streak 30d (+20%) = +32% Gloria totale!'),
('Il Sistema Hunter è integrato con il Karma! 1 gloria guadagnata = 0.1 karma. 100 gloria = 1 alignment.'),
('Se fallisci missioni giornaliere perdi gloria E karma. Il Sistema punisce i cacciatori pigri!'),

-- ============================================================================
-- TIPS CATEGORIA: FRATTURE & DEFENSE
-- ============================================================================

('Le Fratture hanno 7 gradi: E(Verde), D(Blu), C(Arancio), B(Rosso), A(Oro), S(Viola), N(Bianco).'),
('Quando clicchi una frattura inizia la DIFESA! Devi eliminare tutte le ondate entro il tempo.'),
('Se vinci, apri la frattura e prendi il tesoro. Se perdi, Fratture B+ vengono DISTRUTTE!'),
('Fratture E, D, C restano anche se perdi. Puoi ritentare. Ma B+ spariscono per sempre!'),
('Tempo difesa: E/D/C=60s, B=90s, A=120s, S=150s, N=180s. Più alto il rank, più tempo hai.'),

-- ============================================================================
-- TIPS CATEGORIA: GLORIA, SHOP & ACHIEVEMENTS
-- ============================================================================

('Ottieni Gloria da: Boss Elite, Metin, Fratture, Bauli, Missioni, Eventi, Emergency Quest.'),
('Gloria Totale conta per il rank. Gloria Spendibile la usi nello shop. Spendi saggiamente!'),
('Ci sono 12 Achievement: 7 basati su kill, 5 basati su Gloria. Rewards: Buoni e Item Unici!'),
('Achievement #11 (100k gloria) e #12 (500k gloria) danno item UNICI. Valgono tantissimo!'),
('Tutte le transazioni shop sono loggate. Il Sistema traccia TUTTO. No exploit, no cheat!'),

-- ============================================================================
-- TIPS CATEGORIA: SPEED KILL & EMERGENCY QUEST
-- ============================================================================

('Speed Kill Emergency: Uccidi boss in <60s = +300 gloria! Uccidi metin in <300s = +150 gloria!'),
('Le Emergency Quest sono sfide improvvise! Appaiono random, completale in tempo per bonus enormi.'),
('Durante Emergency Quest vedi un TIMER in alto. Se fallisci puoi perdere gloria. Attento!'),
('In party, il timer Speed Kill appare per TUTTI i membri. Collabora per completarlo velocemente!'),
('Usa item shop "Segnale d''Emergenza" (10k gloria) per forzare uno Speed Kill challenge su un mob!'),

-- ============================================================================
-- TIPS CATEGORIA: EVENTI SCHEDULATI
-- ============================================================================

('Ci sono 29 Eventi Schedulati ogni giorno! Controlla il tab Eventi per orari e premi.'),
('Eventi "Alba del Cacciatore" (05:00) e "Glory Rush Notturno" (01:30) danno gloria x2 e x4!'),
('Eventi "Prima Frattura" e "Risveglio dei Boss" premiano il PRIMO player che completa. No sorteggio!'),
('Partecipare a un evento ti registra automaticamente. Il vincitore sorteggiato riceve premi extra!'),
('L''evento migliore è "Glory Rush Notturno" (01:30, 30 min): gloria x4! Perfetto per farming.'),

-- ============================================================================
-- TIPS CATEGORIA: STATISTICHE & RECORD
-- ============================================================================

('Il Sistema traccia TUTTO: Bauli per grado, Boss per difficoltà, Metin, Defense Win Rate, Elite.'),
('Il tab Stats mostra statistiche dettagliate. Puoi vedere quanti bauli N-Rank hai aperto!'),
('Boss sono classificati in 4 categorie: Facili (<500pts), Medi (500-1500), Difficili (1500-5000), Elite (>5000).'),
('Il tuo Win Rate delle difese è visibile nelle stats. Cerca di mantenere almeno 70% per essere rispettato!'),
('Ogni kill, baule, frattura viene salvata nel database. Il Sistema non dimentica MAI.'),

-- ============================================================================
-- TIPS CATEGORIA: CLASSIFICA & COMPETIZIONE
-- ============================================================================

('La classifica si divide in: Giornaliera, Settimanale e Totale (Overall).'),
('Classifica Giornaliera resetta alle 05:00. Settimanale ogni Lunedì. Overall MAI.'),
('Essere TOP 3 in Daily/Weekly ti da premi automatici! Controlla il pending reward nel tuo profilo.'),
('Vuoi salire in classifica? Non spendere gloria nello shop! Ogni punto conta per la posizione.'),
('Il #1 Overall è il vero Monarca. Il suo nome appare nella Sala delle Leggende del server!'),

-- ============================================================================
-- TIPS CATEGORIA: CONSIGLI EARLY GAME (Lv 1-50, Rank E-D)
-- ============================================================================

('EARLY GAME: Fai TUTTE le missioni giornaliere! Il bonus x1.5 è FONDAMENTALE all''inizio.'),
('Partecipa a TUTTI gli eventi possibili. Gloria gratuita senza sforzo!'),
('Compra "Scanner di Fratture" (1k gloria) per spawnare fratture quando vuoi. Utile per farm!'),
('Mantieni lo streak! +5% al 3° giorno, +10% al 7° giorno. Vale tantissimo early game.'),
('Le fratture E-D sono facili. Puoi farle da solo. Non aver paura di clickarle!'),

-- ============================================================================
-- TIPS CATEGORIA: CONSIGLI MID GAME (Lv 50-100, Rank C-B)
-- ============================================================================

('MID GAME: Completa le Trial per salire rank velocemente. Ogni rank = bonus permanente!'),
('Compra "Focus del Cacciatore" (2.5k gloria) prima di farm session. +20% gloria per 1 ora!'),
('Fai fratture Rank C-B per gloria migliore. In party sono più facili e tutti prendono credit!'),
('Partecipa all''evento "Prima Frattura" (06:00). Se sei il primo a sigillare = +300 gloria!'),
('A questo livello, mantieni streak 7 giorni (+10%) + Rank C (+3%) = +13% totale. Vale oro!'),

-- ============================================================================
-- TIPS CATEGORIA: CONSIGLI LATE GAME (Lv 100+, Rank A-S)
-- ============================================================================

('LATE GAME: Mantieni streak 30 giorni! +20% gloria è ENORME a livelli alti.'),
('Fai Emergency Quest di rank alto. Boss Elite danno 150-1200 gloria + Speed Kill bonus!'),
('Risparmia per "Frammento di Monarca" (50k gloria). Item finale, solo per Rank S+.'),
('Obiettivo finale: National Rank N (1.5M gloria + Trial completata). Diventa il Monarca!'),
('Rank S (+10%) + Streak 30d (+20%) + Missioni x1.5 = MASSIMA gloria possibile. Sei un dio!'),

-- ============================================================================
-- TIPS CATEGORIA: STRATEGIA AVANZATA
-- ============================================================================

('Boss Elite (>5000 pts) sono difficili ma danno gloria enorme. Affrontali in party forte!'),
('I bauli hanno Jackpot casuali! Se vedi gloria extra o item leggendari, hai vinto il jackpot!'),
('Le Chiavi Dimensionali rivelano tesori nascosti nei bauli. Non sprecarle su bauli E-D!'),
('Vuoi maximizzare gloria? Formula: Rank alto + Streak 30d + Missioni complete + Eventi.'),
('Il Sistema usa "pending/flush": dati salvati ogni 30s o al logout. Non crashare o perdi progresso!'),

-- ============================================================================
-- TIPS CATEGORIA: PARTY & TEAM STRATEGY
-- ============================================================================

('Prima di aprire frattura B+, controlla che TUTTO il party sia pronto. Buff, HP, distanza!'),
('Se un membro del party muore durante difesa, la frattura può fallire. Proteggi i deboli!'),
('In party, il leader può usare "Risonatore di Gruppo" (15k gloria) per +30% gloria a tutti!'),
('Comunicazione è chiave! Se apri frattura S/N avvisa il party. Servono strategie coordinate.'),
('Party bilanciato: 1 Tank, 2-3 DPS, 1 Support. Fratture N richiedono composizione perfetta!'),

-- ============================================================================
-- TIPS CATEGORIA: SHOP & ITEM STRATEGICI
-- ============================================================================

('EARLY: Scanner (1k). MID: Focus +20% (2.5k). LATE: Frammento Monarca (50k).'),
('Item più forte: "Sigillo di Conquista" (12.5k) = Salta difesa frattura! Instant clear.'),
('"Calibratore" (4k) forza prossima frattura a essere grado C+. Usa prima di Scanner!'),
('"Stabilizzatore di Rango" (7.5k) ti fa SCEGLIERE il rank frattura. Meglio del Calibratore!'),
('Non comprare Buoni Punti (500/2.5k/5k gloria). Sono conversioni yang. Non valgono per rank push!'),

-- ============================================================================
-- TIPS CATEGORIA: MECCANICHE SPECIALI
-- ============================================================================

('Ogni baule ha grado come fratture. Più alto il grado, migliore il loot e la gloria!'),
('Defense Record Win Rate: Verde (≥70%), Arancione (≥50%), Rosso (<50%). Colore = skill level!'),
('Il terminale Hunter si apre con F10 (default). Usalo SPESSO per controllare progressi!'),
('Le notifiche appaiono in alto a sinistra. Se ne vedi troppe, è perché stai facendo progressi!'),
('Il Sistema ha anti-spam: Lock shop 2s, Lock achievement 2s, Lock smart claim 3s. No double-click!'),

-- ============================================================================
-- TIPS CATEGORIA: TRIAL & AVANZAMENTO RANK
-- ============================================================================

('Trial E→D e D→C sono istantanee (se hai requisiti). Da C in poi hanno TEMPO LIMITE!'),
('Trial B→A: 7 giorni max. A→S: 14 giorni. S→N: 30 giorni. Pianifica bene il farming!'),
('Durante trial attiva, ogni Boss/Metin/Frattura/Baule conta per i requisiti. Grinda duro!'),
('Se trial scade, devi ricominciarla. NON perdi gloria, ma riparti da 0 con i requisiti.'),
('Trial S→N richiede: 50 Boss, 100 Fratture, 50 Metin, 20 Bauli, 30 Missioni Daily. Preparati!'),

-- ============================================================================
-- TIPS CATEGORIA: KARMA & ALIGNMENT SYSTEM
-- ============================================================================

('Il Sistema Hunter influenza il tuo Karma! Ogni 100 gloria = +1 alignment (10 karma display).'),
('Fallire missioni giornaliere sottrae karma proporzionalmente. Penalità = -karma!'),
('Karma alto = rispetto. Karma basso = punizione. Il Sistema ricompensa i cacciatori disciplinati.'),
('Formula Karma: 1 gloria = 0.1 karma display. È automatico, non serve fare nulla!'),
('Se hai karma negativo e fai farming Hunter, puoi riportarlo in positivo guadagnando gloria!'),

-- ============================================================================
-- TIPS CATEGORIA: OTTIMIZZAZIONE & PERFORMANCE
-- ============================================================================

('Il sistema Hunter è ottimizzato per 500+ player online. Zero lag, zero problemi!'),
('Pending/flush system: Dati accumulati in RAM, salvati ogni 30s. Massima performance!'),
('Query database ridotte del 90%! Da ~100 query/sec a ~10 query/sec per player.'),
('Le statistiche dettagliate non rallentano il server. Cache system attivo per fratture/elite.'),
('Se vedi notifiche "Trial completata" random, hai completato requisiti senza saperlo. GG!'),

-- ============================================================================
-- TIPS CATEGORIA: ERRORI COMUNI & TROUBLESHOOTING
-- ============================================================================

('Non clickare fratture se non sei pronto! La difesa inizia SUBITO. Buff prima!'),
('Se difesa fallisce e frattura sparisce (B+), NON è bug. È design! Fratture alte sono rischiose.'),
('Inventario pieno = No reward! Controlla sempre spazio prima di clamare achievement.'),
('Se vedi "Missioni già assegnate", è normale. Le missioni si assegnano UNA volta alle 05:00.'),
('Smart Claim riscuote TUTTI gli achievement sbloccati. Se inventario si riempie, fermati e svuota!'),

-- ============================================================================
-- TIPS CATEGORIA: SICUREZZA & FAIR PLAY
-- ============================================================================

('TUTTE le transazioni sono loggate: Shop, Achievement, Gloria, Missioni, Eventi.'),
('Gli admin possono vedere ogni azione. Il Sistema è protetto contro exploit e cheat.'),
('No macro, no bot, no exploit. Il Sistema ha detection automatico. Ban permanente se scoperto!'),
('Se trovi bug, segnala a GM. Abusare bug = ban. Segnalare bug = reward!'),
('Il rank è basato SOLO su gloria e skill. Zero pay-to-win. La meritocrazia regna suprema!'),

-- ============================================================================
-- TIPS CATEGORIA: MOTIVAZIONE & MINDSET
-- ============================================================================

('Il Sistema ha scelto TE. Sei un Hunter. Ora devi solo diventare più forte!'),
('Ogni giorno è una nuova opportunità. Reset alle 05:00 = nuova corsa al #1 Daily!'),
('La strada per National Rank N è lunga (1.5M gloria). Ma OGNI kill ti avvicina al trono!'),
('"Solo io posso salire di livello" - Tu sei l''unico responsabile del tuo potere.'),
('I Monarchi Nazionali non sono nati forti. Sono diventati forti giorno dopo giorno. Come farai tu!');

-- ============================================================================
-- VERIFICA
-- ============================================================================

SELECT COUNT(*) as 'Totale Tips Inseriti' FROM hunter_quest_tips;

-- ============================================================================
-- FINE AGGIORNAMENTO
-- ============================================================================
