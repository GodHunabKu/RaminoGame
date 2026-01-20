# 🎮 Hunter System - Documento di Design per Progressione Basata su Livello

**Versione:** 1.0
**Data:** 2026-01-20
**Stato:** Proposta - In Revisione

---

## 📋 Indice

1. [Analisi Stato Attuale](#analisi-stato-attuale)
2. [Problemi Identificati](#problemi-identificati)
3. [Sistema di Progressione Proposto](#sistema-di-progressione-proposto)
4. [Dettaglio Fasi di Progressione](#dettaglio-fasi-di-progressione)
5. [Modifiche Tecniche](#modifiche-tecniche)
6. [Bilanciamento Ricompense](#bilanciamento-ricompense)
7. [Migrazione Giocatori Esistenti](#migrazione-giocatori-esistenti)
8. [Timeline Implementazione](#timeline-implementazione)
9. [Domande Aperte](#domande-aperte)

---

## 🔍 Analisi Stato Attuale

### Sistema Esistente

Il sistema Hunter attualmente funziona così:

**Accesso:**
- ✅ Nessun requisito di livello
- ✅ Qualsiasi giocatore può attivare il sistema
- ❌ Nessun tutorial introduttivo

**Fratture:**
- ✅ Spawn basato su chance random (spawn_chance nel DB)
- ✅ Filtro solo per dungeon (max rank C)
- ❌ NO filtro per livello giocatore
- ❌ Un livello 30 può ottenere fratture N-Rank

**Missioni Giornaliere:**
- ✅ Assegnazione basata su **rank Gloria** (total_points)
- ✅ Usa `get_rank_index()` che calcola rank dai punti
- ❌ NO relazione con livello giocatore
- ❌ Un livello 50 con tanti punti può avere missioni S-Rank

**Emergency Quest:**
- ✅ UNICA parte che usa correttamente il livello
- ✅ Usa `get_rank_from_level()` per filtrare missioni
- ✅ Controlla min_level e max_level nel DB

**Rank Calculation:**
```lua
-- Funzione CORRETTA (ma usata solo per Emergency)
get_rank_from_level(level):
  175+ → N
  150+ → S
  125+ → A
  100+ → B
  75+  → C
  50+  → D
  1+   → E

-- Funzione ATTUALE (usata per missioni giornaliere - SBAGLIATA)
get_rank_index(total_points):
  Basato su punti Gloria, non livello
```

---

## ❌ Problemi Identificati

### 1. **Progressione Non Coerente** (CRITICO)
- Il sistema Hunter è completamente scollegato dalla progressione del giocatore
- Un livello 30 può teoricamente fare contenuti endgame (fratture N-Rank)
- Ricompense non bilanciate per livello

### 2. **Nessun Tutorial** (ALTO)
- Sistema complesso senza introduzione graduale
- Giocatori nuovi vengono sommersi da meccaniche complesse
- Nessuna spiegazione delle meccaniche base

### 3. **Level Gate Mancante** (ALTO)
- Chiunque può accedere, anche livello 1
- Non ha senso tematico (perché un principiante può diventare Hunter?)
- Nessun senso di "sbloccaggio" del sistema

### 4. **Ricompense Squilibrate** (MEDIO)
- Un livello 50 che fa una frattura E-Rank riceve le stesse ricompense di un 175
- Nessuna scalatura delle ricompense in base al livello
- Rischio di progression skip (troppo forte troppo presto)

### 5. **Missioni Basate su Gloria** (MEDIO)
- Le missioni giornaliere si basano sui punti Gloria accumulati
- Un giocatore attivo livello 50 può avere missioni impossibili
- Sistema confuso (rank basato su punti, non skill/livello)

---

## ✅ Sistema di Progressione Proposto

### Filosofia di Design

**Principi Fondamentali:**
1. Il sistema Hunter è una **feature endgame** che si sblocca gradualmente
2. Livelli 30-99 sono **TUTORIAL** (apprendimento meccaniche)
3. Livelli 100+ sono **SISTEMA COMPLETO** (contenuto serio)
4. Rank massimo ottenibile è **limitato dal livello del giocatore**
5. Tutorial insegna meccaniche in modo progressivo (E → D → C)

---

## 📊 Dettaglio Fasi di Progressione

### **FASE 0: Bloccato (Livelli 1-29)**

**Stato:** Sistema Hunter **NON DISPONIBILE**

**Comportamento:**
- Nessuna frattura può spawnare
- Nessuna missione giornaliera
- Nessuna Emergency Quest Hunter
- UI Hunter non visibile/attiva

**Messaggi:**
- Se il giocatore prova ad accedere: `"Il sistema Hunter si sblocca al livello 30"`

**Razionale:**
- Livelli 1-29 sono per apprendere Metin2 base
- Il sistema Hunter è complesso e richiede conoscenza del gioco
- Crea senso di progressione ("finalmente livello 30!")

---

### **FASE 1: Introduzione (Livello 30 - Primo Accesso)**

**Trigger:** Giocatore raggiunge livello 30 per la prima volta

**Quest Tutorial:** "Il Risveglio del Hunter"

**Obiettivi:**
1. Visita l'NPC Hunter Guildmaster
2. Ricevi spiegazione del sistema Hunter
3. Completa prima missione tutorial (kill 10 mob facili)
4. Ottieni prima ricompensa Gloria

**Ricompense:**
- 100 Gloria (punti starter)
- 1x Hunter Starter Pack (oggetto tutorial con spiegazione)
- Unlock sistema Hunter

**Dialoghi NPC:**
```
[Hunter Guildmaster]
"Salve, giovane guerriero. Hai raggiunto il livello 30...
Il potere sta crescendo in te. Sei pronto a diventare un Hunter?

Il nostro compito è eliminare minacce dimensionali:
- Fratture spazio-temporali
- Mob Elite pericolosi
- Emergenze che minacciano il regno

Inizierai come E-Rank. Completa missioni, sigilla fratture,
e sali di grado. La tua forza determinerà il tuo Rank.

Rank disponibili in base al tuo livello:
Lv 30-49: E-Rank (Tutorial)
Lv 50-74: D-Rank (Tutorial)
Lv 75-99: C-Rank (Tutorial Avanzato)
Lv 100+: Tutti i Rank (Sistema Completo)

Sei pronto a cominciare?"
```

**Meccaniche Sbloccate:**
- Sistema Gloria (ranking)
- Missioni Giornaliere (solo E-Rank)
- Fratture (solo E-Rank)
- UI Hunter base

---

### **FASE 2: Tutorial E-Rank (Livelli 30-49)**

**Rank Disponibile:** E (verde)

**Fratture:**
- **Spawn:** Solo fratture E-Rank
- **Difesa:** Durata 60 secondi
- **Mob:** 6 mob totali (facili)
- **Messaggi:** `[TUTORIAL E-Rank] Questa è una frattura facile. Uccidi tutti i mob!`

**Missioni Giornaliere:**
- Solo missioni E-Rank
- Target ridotti (50% dei normali)
- Esempi:
  - "Caccia ai Lupi" (kill 5 lupi invece di 10)
  - "Elimina i Cinghiali" (kill 10 cinghiali invece di 20)
  - "Caccia Generale" (kill 12 mob invece di 25)

**Emergency Quest:**
- Solo emergency E-Rank
- Durata più lunga (+30 secondi)
- Target ridotti

**Ricompense:**
- Gloria: **50% delle normali**
- Exp bonus: 100%
- Drop: Item base

**Messaggi Sistema:**
- `[TUTORIAL] Hai completato una missione E-Rank! Continua a salire di livello per sbloccare rank superiori.`
- `[TUTORIAL] Hai sigillato una frattura E-Rank! Al livello 50 potrai affrontare fratture D-Rank.`

**UI Indicators:**
- Badge "TUTORIAL" visibile nelle missioni
- Progress bar "Livello 30/50 - Prossimo Rank: D"

---

### **FASE 3: Tutorial D-Rank (Livelli 50-74)**

**Rank Disponibile:** D (blu)

**Unlock Message:**
```
[HUNTER SYSTEM] Congratulazioni! Hai raggiunto il livello 50!
Ora puoi affrontare fratture e missioni D-Rank.
Il tutorial continua... preparati a sfide più difficili!
```

**Fratture:**
- Spawn: E-Rank (70%), D-Rank (30%)
- Difesa D: 60 secondi, 8 mob
- Cap massimo: **D-Rank** (non può spawnare C+)

**Missioni Giornaliere:**
- E-Rank (40%), D-Rank (60%)
- Target ridotti (60% dei normali)
- Esempi:
  - "Caccia ai Guerrieri Orco" (kill 9 invece di 15)
  - "Stermina gli Scheletri" (kill 12 invece di 20)
  - "Distruggi 1 Metin" (invece di 2)

**Ricompense:**
- Gloria: **60% delle normali**
- Exp bonus: 100%
- Drop: Item intermedi

**Messaggi Sistema:**
- `[TUTORIAL D-Rank] Ben fatto! Al livello 75 sbloccherai il C-Rank.`

---

### **FASE 4: Tutorial C-Rank (Livelli 75-99)**

**Rank Disponibile:** C (arancione)

**Unlock Message:**
```
[HUNTER SYSTEM] Livello 75 raggiunto!
Accesso al C-Rank sbloccato. Questa è l'ultima fase del tutorial.
Al livello 100 accederai al SISTEMA COMPLETO con tutti i rank!
```

**Fratture:**
- Spawn: E (30%), D (40%), C (30%)
- Difesa C: 60 secondi, 10 mob
- Cap massimo: **C-Rank** (non può spawnare B+)

**Missioni Giornaliere:**
- D-Rank (40%), C-Rank (60%)
- Target ridotti (70% dei normali)
- Esempi:
  - "Caccia al Boss Ragno" (1 boss)
  - "Stermina i Guerrieri Elite" (11 invece di 15)
  - "Distruggi 2 Metin" (invece di 3)

**Ricompense:**
- Gloria: **70% delle normali**
- Exp bonus: 100%
- Drop: Item avanzati

**Messaggi Sistema:**
- `[TUTORIAL C-Rank] Fase finale del tutorial! Al livello 100 il sistema completo si sbloccherà.`
- `[AVVISO] Mancano ${100 - level} livelli al sistema completo!`

**UI Indicators:**
- Progress bar "Livello 75/100 - Sistema Completo"
- Tooltip: "Al livello 100 tutti i rank si sbloccheranno"

---

### **FASE 5: Sistema Completo (Livelli 100+)**

**Unlock Message:**
```
[HUNTER SYSTEM] LIVELLO 100 RAGGIUNTO!
Benvenuto nel sistema Hunter completo!

Tutti i rank sono ora disponibili:
- B-Rank (100-124): Difficoltà Alta
- A-Rank (125-149): Difficoltà Estrema
- S-Rank (150-174): Difficoltà Leggendaria
- N-Rank (175-200): Difficoltà Finale

Le ricompense sono ora al 100%.
Il tutorial è completato. Buona fortuna, Hunter!
```

**Rank Disponibili per Livello:**

| Livello | Rank Max | Note |
|---------|----------|------|
| 100-124 | **B** | Fratture max B, missioni max B |
| 125-149 | **A** | Fratture max A, missioni max A |
| 150-174 | **S** | Fratture max S, missioni max S |
| 175-200 | **N** | Tutti i contenuti disponibili |

**Fratture:**
- Spawn filtrato per livello giocatore
- Livello 100: max B-Rank
- Livello 125: max A-Rank
- Livello 150: max S-Rank
- Livello 175: tutti (incluso N-Rank)

**Algoritmo Spawn:**
```lua
-- Esempio per livello 110 (max B-Rank)
Chance spawn:
  E: 15%
  D: 25%
  C: 30%
  B: 30%
  (A, S, N: BLOCCATI)

-- Esempio per livello 180 (max N-Rank)
Chance spawn:
  E: 5%
  D: 10%
  C: 15%
  B: 25%
  A: 20%
  S: 15%
  N: 10%
```

**Missioni Giornaliere:**
- Basate su **livello giocatore**, non Gloria
- Livello 100: mix C/B-Rank
- Livello 125: mix B/A-Rank
- Livello 150: mix A/S-Rank
- Livello 175: tutti i rank possibili

**Ricompense:**
- Gloria: **100% delle normali**
- Exp bonus: 100%
- Drop: Item full

**Messaggi Sistema:**
- Nessun badge "TUTORIAL"
- Messaggi normali senza indicazioni didattiche

---

## 🔧 Modifiche Tecniche

### 1. **Database Changes**

#### A. Aggiungere campi livello alle missioni

**Tabella:** `hunter_mission_definitions`

```sql
ALTER TABLE hunter_mission_definitions
ADD COLUMN is_tutorial TINYINT(1) DEFAULT 0 COMMENT 'Se 1, è una missione tutorial (30-99)';

ALTER TABLE hunter_mission_definitions
ADD COLUMN level_min INT DEFAULT 30 COMMENT 'Livello minimo richiesto';

ALTER TABLE hunter_mission_definitions
ADD COLUMN level_max INT DEFAULT 200 COMMENT 'Livello massimo richiesto';
```

**Esempi di UPDATE:**
```sql
-- Missioni E-Rank tutorial
UPDATE hunter_mission_definitions
SET is_tutorial=1, level_min=30, level_max=49
WHERE min_rank='E';

-- Missioni D-Rank tutorial
UPDATE hunter_mission_definitions
SET is_tutorial=1, level_min=50, level_max=74
WHERE min_rank='D';

-- Missioni C-Rank tutorial
UPDATE hunter_mission_definitions
SET is_tutorial=1, level_min=75, level_max=99
WHERE min_rank='C';

-- Missioni B+ sistema completo
UPDATE hunter_mission_definitions
SET is_tutorial=0, level_min=100, level_max=200
WHERE min_rank IN ('B', 'A', 'S', 'N');
```

#### B. Nuove missioni tutorial specifiche

**Creare missioni tutorial semplificate per rank E, D, C:**

```sql
-- Esempio: Missioni E-Rank tutorial (30-49)
INSERT INTO hunter_mission_definitions VALUES
(50, '[TUTORIAL] Primi Passi', 'kill_mob', 0, 5, 'E', 25, 5, 1440, 1, NOW()),
(51, '[TUTORIAL] Caccia Basilare', 'kill_mob', 101, 5, 'E', 30, 6, 1440, 1, NOW()),
(52, '[TUTORIAL] Metin Tutorial', 'kill_metin', 0, 1, 'E', 40, 8, 1440, 1, NOW());

-- Poi aggiungi campi tutorial
UPDATE hunter_mission_definitions
SET is_tutorial=1, level_min=30, level_max=49
WHERE mission_id IN (50, 51, 52);
```

#### C. Aggiungere quest tutorial iniziale

**Tabella:** `hunter_quest_tutorial` (nuova)

```sql
CREATE TABLE hunter_quest_tutorial (
  player_id INT NOT NULL,
  tutorial_completed TINYINT(1) DEFAULT 0,
  completed_date DATETIME,
  PRIMARY KEY (player_id)
);
```

#### D. Modificare Stored Procedure

**Stored Procedure:** `sp_assign_daily_missions`

**PRIMA (basato su Gloria):**
```sql
-- Usava il rank dai punti Gloria
SET v_player_rank_num = fn_rank_to_num(p_rank);
```

**DOPO (basato su Livello):**
```sql
-- Passa il livello invece del rank Gloria
CREATE PROCEDURE `sp_assign_daily_missions_v2`(
    IN p_player_id INT,
    IN p_player_level INT,  -- NUOVO parametro
    IN p_player_name VARCHAR(64)
)
BEGIN
    DECLARE v_today DATE;
    DECLARE v_max_rank VARCHAR(2);
    DECLARE v_is_tutorial TINYINT(1);

    SET v_today = CURDATE();

    -- Determina rank massimo dal LIVELLO
    SET v_max_rank = fn_get_rank_from_level(p_player_level);

    -- Determina se è tutorial (< 100)
    SET v_is_tutorial = IF(p_player_level < 100, 1, 0);

    -- Cancella missioni vecchie
    DELETE FROM hunter_player_missions
    WHERE player_id = p_player_id AND assigned_date = v_today;

    -- Assegna 3 missioni filtrate per livello
    -- Mission 1
    INSERT INTO hunter_player_missions (...)
    SELECT ...
    FROM hunter_mission_definitions
    WHERE enabled = 1
      AND level_min <= p_player_level
      AND level_max >= p_player_level
      AND is_tutorial = v_is_tutorial
      AND fn_rank_to_num(min_rank) <= fn_rank_to_num(v_max_rank)
    ORDER BY RAND() LIMIT 1;

    -- Mission 2, 3 (stesso filtro)
    ...
END
```

**Nuova funzione SQL:**
```sql
CREATE FUNCTION fn_get_rank_from_level(p_level INT)
RETURNS VARCHAR(2)
DETERMINISTIC
BEGIN
    IF p_level >= 175 THEN RETURN 'N';
    ELSEIF p_level >= 150 THEN RETURN 'S';
    ELSEIF p_level >= 125 THEN RETURN 'A';
    ELSEIF p_level >= 100 THEN RETURN 'B';
    ELSEIF p_level >= 75 THEN RETURN 'C';
    ELSEIF p_level >= 50 THEN RETURN 'D';
    ELSE RETURN 'E';
    END IF;
END
```

---

### 2. **Lua Code Changes**

#### A. Level Gate (hunterlib.lua)

**Funzione:** `hg_lib.check_level_requirement()`

```lua
function hg_lib.check_level_requirement()
    local level = pc.get_level()
    if level < 30 then
        return false
    end
    return true
end

function hg_lib.show_level_gate_message()
    local level = pc.get_level()
    local needed = 30 - level
    syschat(string.format(
        "|cffFF6600[HUNTER SYSTEM]|r Sistema bloccato. Raggiung livello 30 per sbloccare. (Mancano %d livelli)",
        needed
    ))
end
```

**Applicare check in tutte le entry point:**
```lua
-- spawn_fracture()
function hg_lib.spawn_fracture()
    if not hg_lib.check_level_requirement() then
        return  -- Silenzioso, non spawna
    end
    -- ... resto del codice
end

-- assign_daily_missions()
function hg_lib.assign_daily_missions()
    if not hg_lib.check_level_requirement() then
        return false
    end
    -- ... resto del codice
end

-- trigger_random_emergency()
function hg_lib.trigger_random_emergency()
    if not hg_lib.check_level_requirement() then
        return
    end
    -- ... resto del codice
end
```

#### B. Tutorial Quest (hunterlib.lua)

**Funzione:** `hg_lib.check_tutorial_completion()`

```lua
function hg_lib.check_tutorial_completion()
    local level = pc.get_level()
    local tutorial_done = pc.getqf("hq_tutorial_completed") or 0

    -- Se livello 30+ e tutorial non fatto, avvia tutorial
    if level >= 30 and tutorial_done == 0 then
        hg_lib.start_hunter_tutorial()
    end
end

function hg_lib.start_hunter_tutorial()
    -- Mostra finestra tutorial
    cmdchat("HunterTutorialStart")

    -- Messaggio benvenuto
    local msg = [[
|cffFFD700===========================================|r
|cffFFD700   BENVENUTO NEL SISTEMA HUNTER!|r
|cffFFD700===========================================|r

Hai raggiunto il livello 30 e sei pronto a diventare un Hunter.

Il sistema Hunter ti permette di:
- Sigillare Fratture Dimensionali
- Completare Missioni Giornaliere
- Affrontare Emergency Quest
- Salire di Rank e ottenere ricompense

|cffFF6600IMPORTANTE:|r Livelli 30-99 sono TUTORIAL.
Il sistema completo si sblocca al livello 100.

Visita l'NPC Hunter Guildmaster per iniziare!
    ]]

    notice_multiline(msg, 10)

    -- Segna tutorial come visto
    pc.setqf("hq_tutorial_completed", 1)

    -- Registra nel DB
    mysql_direct_query("INSERT INTO srv1_hunabku.hunter_quest_tutorial (player_id, tutorial_completed, completed_date) VALUES (" .. pc.get_player_id() .. ", 1, NOW()) ON DUPLICATE KEY UPDATE tutorial_completed=1, completed_date=NOW()")
end
```

#### C. Filtrare Fratture per Livello (hunterlib.lua)

**Modificare:** `spawn_fracture()`

```lua
function hg_lib.spawn_fracture()
    local pid = pc.get_player_id()
    local level = pc.get_level()

    -- Level gate
    if level < 30 then return end

    local map_index = pc.get_map_index()
    local is_in_dungeon = hg_lib.is_dungeon_map(map_index)

    -- Determina rank massimo dal livello
    local max_rank = hg_lib.get_rank_from_level(level)
    local max_rank_idx = hg_lib.rank_to_index(max_rank)

    -- Calibratore (opzionale, può forzare rank più alto se livello lo permette)
    local calibrator_active = game.get_event_flag("hq_fracture_rank_"..pid) or 0
    local use_calibrator = false
    if calibrator_active == 1 then
        use_calibrator = true
        game.set_event_flag("hq_fracture_rank_"..pid, 0)
    end

    -- Cache fratture
    local cached = hg_lib.get_fractures_cached()
    if not cached then return end
    local c, d = cached.count, cached.data
    if c == 0 then return end

    -- Calcola spawn weighted con filtro livello
    local roll = number(1, 100)
    local evt_name = hg_lib.get_active_event()
    if evt_name == "RED+MOON" then
        roll = number(50, 100)
    end

    local sel_vnum, sel_rank, sel_color = 16060, "E-Rank", "GREEN"
    local cumul = 0
    local found = false

    for i = 1, c do
        local rank_label = d[i].rank_label or ""
        local frac_rank = hg_lib.extract_rank_letter(rank_label)  -- Estrai E, D, C, etc
        local frac_rank_idx = hg_lib.rank_to_index(frac_rank)

        local skip_this = false

        -- FILTRO LIVELLO: salta se rank frattura > rank massimo giocatore
        if frac_rank_idx > max_rank_idx then
            skip_this = true
        end

        -- Calibratore (solo se livello lo permette)
        if use_calibrator then
            if frac_rank_idx < 2 then  -- Skip E, D se calibratore
                skip_this = true
            end
        end

        -- Dungeon restriction
        if is_in_dungeon and not hg_lib.is_rank_allowed_in_dungeon(rank_label) then
            skip_this = true
        end

        if not skip_this then
            cumul = cumul + tonumber(d[i].spawn_chance)
            if roll <= cumul then
                sel_vnum = tonumber(d[i].vnum)
                sel_rank = rank_label
                sel_color = d[i].color_code or "PURPLE"
                found = true
                break
            end
        end
    end

    -- Spawn frattura
    local x, y = pc.get_local_x(), pc.get_local_y()
    mob.spawn(sel_vnum, x + 3, y + 3, 1)

    -- Messaggio tutorial se livello < 100
    local msg
    if level < 100 then
        msg = string.format("|cffFF6600[TUTORIAL %s]|r Frattura %s rilevata.", max_rank, sel_rank)
    else
        msg = hg_lib.get_text("fracture_detected", {RANK = sel_rank}) or ("ATTENZIONE: FRATTURA " .. sel_rank .. " RILEVATA.")
    end
    hg_lib.hunter_speak_color(msg, sel_color)
end
```

**Funzioni helper:**
```lua
function hg_lib.extract_rank_letter(rank_label)
    -- "E-Rank" → "E", "S-Rank" → "S"
    if rank_label:find("N") then return "N"
    elseif rank_label:find("S") then return "S"
    elseif rank_label:find("A") then return "A"
    elseif rank_label:find("B") then return "B"
    elseif rank_label:find("C") then return "C"
    elseif rank_label:find("D") then return "D"
    else return "E"
    end
end

function hg_lib.rank_to_index(rank)
    local map = {E=0, D=1, C=2, B=3, A=4, S=5, N=6}
    return map[rank] or 0
end
```

#### D. Modificare Assegnazione Missioni (hunterlib.lua)

**Modificare:** `assign_daily_missions()`

```lua
function hg_lib.assign_daily_missions()
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local level = pc.get_level()
    local today = hg_lib.get_today_date()

    -- Level gate
    if level < 30 then return false end

    -- Check se già assegnate
    local last_assign_day = pc.getqf("hq_last_assign_day") or 0
    local current_day = tonumber(os.date("%j")) or 0

    if last_assign_day == current_day then
        local c, d = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
        if c > 0 and tonumber(d[1].cnt) >= 3 then
            hg_lib.send_daily_missions()
            return false
        end
    end

    local c, d = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
    if c > 0 and tonumber(d[1].cnt) >= 3 then
        pc.setqf("hq_last_assign_day", current_day)
        hg_lib.send_daily_missions()
        return false
    end

    pc.setqf("hq_last_assign_day", current_day)

    -- CAMBIO: Passa LIVELLO invece di rank Gloria
    -- PRIMA: mysql_direct_query("CALL srv1_hunabku.sp_assign_daily_missions(" .. pid .. ", '" .. rank_letter .. "', '" .. pname .. "')")
    -- DOPO:
    mysql_direct_query("CALL srv1_hunabku.sp_assign_daily_missions_v2(" .. pid .. ", " .. level .. ", '" .. pname .. "')")

    local vc, vd = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "' AND status='active'")
    local inserted_count = 0
    if vc > 0 and vd[1] then inserted_count = tonumber(vd[1].cnt) or 0 end

    -- Messaggio tutorial se livello < 100
    local max_rank = hg_lib.get_rank_from_level(level)
    if level < 100 then
        syschat(string.format("|cffFF6600[TUTORIAL]|r Missioni giornaliere assegnate (Max Rank: %s). Completa 3/3 per bonus!", max_rank))
    else
        syschat("|cff00FF00[HUNTER]|r Nuove missioni giornaliere assegnate!")
    end

    hg_lib.send_daily_missions()
    return true
end
```

#### E. Modificare Ricompense Tutorial (hunterlib.lua)

**Funzione:** `hg_lib.apply_tutorial_penalty(reward, level)`

```lua
function hg_lib.apply_tutorial_penalty(reward, level)
    if level >= 100 then
        return reward  -- Nessuna penalità
    elseif level >= 75 then
        return math.floor(reward * 0.7)  -- 70% per C-Rank tutorial
    elseif level >= 50 then
        return math.floor(reward * 0.6)  -- 60% per D-Rank tutorial
    else
        return math.floor(reward * 0.5)  -- 50% per E-Rank tutorial
    end
end
```

**Applicare in:**
- `complete_mission()` (ricompense missioni giornaliere)
- `on_fracture_seal()` (ricompense fratture - se applicabile)
- Emergency quest completion

**Esempio in complete_mission():**
```lua
function hg_lib.complete_mission(mission_id)
    -- ... codice esistente per recuperare dati missione

    local level = pc.get_level()
    local gloria_reward = tonumber(mission_data.reward_glory) or 0

    -- Applica penalty se tutorial
    gloria_reward = hg_lib.apply_tutorial_penalty(gloria_reward, level)

    -- Aggiungi Gloria
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points=total_points+" .. gloria_reward .. ", spendable_points=spendable_points+" .. gloria_reward .. " WHERE player_id=" .. pid)

    -- Messaggio tutorial
    if level < 100 then
        syschat(string.format("|cffFF6600[TUTORIAL]|r Missione completata! +%d Gloria (ricompensa tutorial ridotta)", gloria_reward))
    else
        syschat(string.format("|cff00FF00[HUNTER]|r Missione completata! +%d Gloria", gloria_reward))
    end

    -- ... resto del codice
end
```

---

### 3. **UI Changes (Python)**

#### A. Tutorial Indicators

**File:** `hunter_missions.py` o `uihunterlevel.py`

**Aggiungere badge TUTORIAL alle missioni:**
```python
def AddMission(self, mission_data):
    # ... codice esistente

    # Check se è tutorial
    is_tutorial = mission_data.get('is_tutorial', 0)
    player_level = player.GetStatus(player.LEVEL)

    if player_level < 100 and is_tutorial:
        # Aggiungi badge TUTORIAL
        tutorial_badge = ui.TextLine()
        tutorial_badge.SetParent(mission_window)
        tutorial_badge.SetText("[TUTORIAL]")
        tutorial_badge.SetPackedFontColor(0xFFFF6600)
        tutorial_badge.Show()
```

#### B. Progress Bar Sistema Completo

**Aggiungere progress bar che mostra avanzamento verso livello 100:**

```python
class HunterProgressBar(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        # ... setup UI

    def UpdateProgress(self):
        level = player.GetStatus(player.LEVEL)

        if level < 30:
            self.SetText("Sistema Hunter bloccato (Lv 30 richiesto)")
            self.progress = 0
        elif level < 100:
            # Tutorial phase
            self.SetText("TUTORIAL - Livello %d/100" % level)
            self.progress = level / 100.0

            # Mostra prossimo unlock
            if level < 50:
                next_unlock = "D-Rank al Lv 50"
            elif level < 75:
                next_unlock = "C-Rank al Lv 75"
            else:
                next_unlock = "Sistema Completo al Lv 100"

            self.nextUnlockText.SetText("Prossimo: " + next_unlock)
        else:
            # Sistema completo
            self.SetText("Sistema Hunter Completo")
            self.progress = 1.0

            # Mostra rank massimo disponibile
            if level < 125:
                max_rank = "B-Rank"
            elif level < 150:
                max_rank = "A-Rank"
            elif level < 175:
                max_rank = "S-Rank"
            else:
                max_rank = "N-Rank (MAX)"

            self.maxRankText.SetText("Rank Massimo: " + max_rank)
```

#### C. Tutorial Popup

**Popup al primo login dopo aver raggiunto livello 30:**

```python
class HunterTutorialPopup(ui.Window):
    def __init__(self):
        # Finestra popup stile "Solo Leveling"
        # Spiega meccaniche base
        # Pulsante "Inizia Tutorial"
        pass
```

---

## 💰 Bilanciamento Ricompense

### Ricompense Gloria per Fase

| Livello | Fase | Gloria Multiplier | Esempio Missione E |
|---------|------|-------------------|-------------------|
| 30-49 | Tutorial E | **50%** | 50 → 25 Gloria |
| 50-74 | Tutorial D | **60%** | 100 → 60 Gloria |
| 75-99 | Tutorial C | **70%** | 200 → 140 Gloria |
| 100+ | Sistema Completo | **100%** | 350 → 350 Gloria |

### Rationale

**Perché ridurre le ricompense nel tutorial?**
1. Previene progression skip (troppo forte troppo presto)
2. Mantiene bilanciamento economico
3. Incentiva a salire di livello per sbloccare ricompense piene
4. Fratture/missioni tutorial sono più facili, quindi meritano meno

**Ricompense EXP:** Sempre 100% (aiuta a livellare, non danneggia economia)

**Drop Item:** Normale (non ridurre, troppo complesso)

---

## 👥 Migrazione Giocatori Esistenti

### Scenario: Giocatori già livello 30+

**Problema:** Giocatori che hanno già livello 30+ ma non hanno fatto il tutorial

**Soluzione:**

**Opzione A: Tutorial Automatico Skip (CONSIGLIATA)**
```lua
function hg_lib.check_tutorial_completion()
    local level = pc.get_level()
    local tutorial_done = pc.getqf("hq_tutorial_completed") or 0

    if level >= 30 and tutorial_done == 0 then
        -- Se livello >= 100, skippa tutorial automaticamente
        if level >= 100 then
            pc.setqf("hq_tutorial_completed", 1)
            mysql_direct_query("INSERT INTO srv1_hunabku.hunter_quest_tutorial (player_id, tutorial_completed, completed_date) VALUES (" .. pc.get_player_id() .. ", 1, NOW()) ON DUPLICATE KEY UPDATE tutorial_completed=1")

            syschat("|cffFFD700[HUNTER SYSTEM]|r Benvenuto! Il tutorial è stato completato automaticamente (livello 100+).")
        else
            -- Livello 30-99: mostra tutorial opzionale
            hg_lib.start_hunter_tutorial()
        end
    end
end
```

**Opzione B: Tutorial Opzionale**
- Aggiungere NPC che permette di vedere il tutorial anche dopo
- Comando `/hunter_tutorial` per riaprire spiegazioni

### Scenario: Giocatori con Gloria già accumulate

**Problema:** Giocatori livello 50 con 10.000 Gloria (rank A nei punti)

**Soluzione:**
- I punti Gloria accumulati **rimangono**
- Il ranking basato su punti **rimane** (classifica)
- Ma le **missioni giornaliere** ora si basano sul **livello**, non Gloria
- Questo è **corretto**: i punti mostrano storia/skill, ma le missioni sono per il livello

**Messaggio ai giocatori:**
```
[HUNTER SYSTEM UPDATE]
Il sistema di assegnazione missioni è cambiato!

PRIMA: Missioni basate su punti Gloria (Rank)
DOPO: Missioni basate su LIVELLO personaggio

I tuoi punti Gloria e posizione in classifica NON cambiano.
Ma ora riceverai missioni adatte al tuo livello.

Questo rende il sistema più bilanciato e graduale.
```

---

## 📅 Timeline Implementazione

### Fase 1: Database & Backend (Priorità ALTA)
**Tempo stimato:** 2-3 giorni

- [ ] Aggiungere campi `is_tutorial`, `level_min`, `level_max` al DB
- [ ] Creare stored procedure `sp_assign_daily_missions_v2`
- [ ] Creare funzione SQL `fn_get_rank_from_level`
- [ ] Aggiungere missioni tutorial specifiche (E, D, C)
- [ ] Creare tabella `hunter_quest_tutorial`
- [ ] Testing database queries

### Fase 2: Lua Core Logic (Priorità ALTA)
**Tempo stimato:** 3-4 giorni

- [ ] Implementare `check_level_requirement()` e level gate
- [ ] Implementare `check_tutorial_completion()` e tutorial flow
- [ ] Modificare `spawn_fracture()` con filtro livello
- [ ] Modificare `assign_daily_missions()` per usare livello
- [ ] Implementare `apply_tutorial_penalty()` per ricompense
- [ ] Aggiungere messaggi tutorial in tutte le funzioni
- [ ] Testing in-game

### Fase 3: UI & UX (Priorità MEDIA)
**Tempo stimato:** 2-3 giorni

- [ ] Creare `HunterTutorialPopup` (popup benvenuto)
- [ ] Aggiungere badge "TUTORIAL" alle missioni
- [ ] Creare `HunterProgressBar` (progress 30-100)
- [ ] Modificare UI missioni per mostrare level requirements
- [ ] Testing UI

### Fase 4: Content (Priorità MEDIA)
**Tempo stimato:** 2-3 giorni

- [ ] Scrivere dialoghi NPC Hunter Guildmaster
- [ ] Creare quest tutorial "Il Risveglio del Hunter"
- [ ] Scrivere tutti i testi tutorial (messaggi, tooltips)
- [ ] Creare Hunter Starter Pack (item tutorial)
- [ ] Testing content

### Fase 5: Migration & Testing (Priorità ALTA)
**Tempo stimato:** 2-3 giorni

- [ ] Script migrazione giocatori esistenti
- [ ] Testing con giocatori livello 30-99
- [ ] Testing con giocatori livello 100+
- [ ] Testing bilanciamento ricompense
- [ ] Bug fixing

### Fase 6: Documentation & Release (Priorità BASSA)
**Tempo stimato:** 1-2 giorni

- [ ] Scrivere changelog
- [ ] Scrivere guida per giocatori
- [ ] Preparare annuncio in-game
- [ ] Release su server live

**TOTALE TEMPO STIMATO:** 12-18 giorni di sviluppo

---

## ❓ Domande Aperte

### 1. **Livello Minimo di Accesso**
**Domanda:** Confermi livello 30 come entry point, o preferisci diverso?

**Opzioni:**
- [ ] Livello 30 (consigliato - mid-game)
- [ ] Livello 50 (late mid-game)
- [ ] Livello 75 (late-game)
- [ ] Livello 1 (ma con tutorial esteso)

**Considerazioni:**
- Livello 30: Giocatore ha già familiarità con meccaniche base Metin2
- Livello 50: Più restrittivo, ma giocatore più esperto
- Livello 75: Molto restrittivo, sistema diventa quasi endgame-only

---

### 2. **Ricompense Tutorial**
**Domanda:** Confermi riduzione ricompense per tutorial (50/60/70%)?

**Opzioni:**
- [ ] Sì, riduzione come proposto (50/60/70%)
- [ ] Riduzione più leggera (70/80/90%)
- [ ] Riduzione più pesante (30/40/50%)
- [ ] No riduzione, ricompense piene anche in tutorial

**Considerazioni:**
- Se ricompense piene: rischio progression skip
- Se riduzione troppo pesante: giocatori potrebbero ignorare sistema fino a lv 100
- 50/60/70% sembra bilanciato (non troppo poco, non troppo tanto)

---

### 3. **Missioni Tutorial**
**Domanda:** Creare nuove missioni specifiche per tutorial o riusare esistenti?

**Opzioni:**
- [ ] Creare nuove missioni tutorial (es. "[TUTORIAL] Primi Passi")
- [ ] Riusare missioni esistenti ma ridurre target (kill 5 invece di 10)
- [ ] Mix: alcune nuove, alcune esistenti modificate

**Considerazioni:**
- Nuove missioni: più lavoro, ma esperienza migliore
- Riusare esistenti: meno lavoro, ma meno impatto didattico
- Mix: bilanciamento tra effort e risultato

---

### 4. **Tutorial Quest Iniziale**
**Domanda:** Quanto elaborato deve essere il tutorial iniziale?

**Opzioni:**
- [ ] Tutorial minimo (solo popup spiegazione + unlock sistema)
- [ ] Tutorial medio (popup + prima quest semplice)
- [ ] Tutorial esteso (popup + catena quest 3-5 step con NPC)

**Considerazioni:**
- Minimo: veloce da implementare, ma meno coinvolgente
- Medio: buon bilanciamento
- Esteso: migliore esperienza, ma richiede più sviluppo

---

### 5. **Fratture in Dungeon**
**Domanda:** Mantenere restrizione "max rank C in dungeon"?

**Opzioni:**
- [ ] Sì, mantieni (max C in dungeon indipendentemente da livello)
- [ ] No, rimuovi (permetti fratture rank alto anche in dungeon)
- [ ] Modifica: max rank = player level cap (se player è 150, max S anche in dungeon)

**Considerazioni:**
- Max C: previene party basso livello da essere sorpresi da fratture impossibili
- Nessuna restrizione: più libertà, ma rischio
- Dinamico: più flessibile, ma complesso

---

### 6. **Calibratore Rank**
**Domanda:** Mantenere item "Calibratore" che forza rank alto?

**Opzioni:**
- [ ] Sì, mantieni ma rispetta level cap (lv 50 non può forzare S-Rank)
- [ ] No, rimuovi completamente (troppo complesso)
- [ ] Modifica: Calibratore aumenta di 1 rank oltre il cap (max +1)

**Considerazioni:**
- Mantenere: dà controllo ai giocatori, ma deve rispettare livello
- Rimuovere: semplifica logica
- Modifica +1: compromesso interessante

---

### 7. **Emergency Quest**
**Domanda:** Le Emergency Quest già usano livello. Modificare qualcosa?

**Opzioni:**
- [ ] Lasciare come sono (già corrette)
- [ ] Aggiungere tutorial emergency (ridotte/facilitate per lv 30-99)
- [ ] Modificare ricompense anche per emergency tutorial

**Considerazioni:**
- Emergency già funzionano bene
- Ma potrebbero beneficiare di versioni tutorial

---

### 8. **Messaggi Tutorial**
**Domanda:** Quanto invasivi devono essere i messaggi tutorial?

**Opzioni:**
- [ ] Molto visibili (notice multiline + syschat + UI badge)
- [ ] Moderati (syschat + UI badge)
- [ ] Minimi (solo UI badge, no spam chat)

**Considerazioni:**
- Troppi messaggi: irritante
- Troppo pochi: giocatori non capiscono
- Moderato: consigliato

---

### 9. **Rank Cap Visualization**
**Domanda:** Come mostrare al giocatore il suo rank cap corrente?

**Opzioni:**
- [ ] Progress bar nella UI Hunter (sempre visibile)
- [ ] Comando `/hunter_info` (mostra info su richiesta)
- [ ] Tooltip quando hover su icona Hunter
- [ ] Tutte le opzioni sopra

---

### 10. **Migrazione Immediata**
**Domanda:** Applicare cambiamenti immediatamente o con preavviso?

**Opzioni:**
- [ ] Immediato: update e deploy subito
- [ ] Preavviso: annuncio 1 settimana prima, poi deploy
- [ ] Graduale: fase 1 (level gate), poi fase 2 (filtri), poi fase 3 (tutorial)

**Considerazioni:**
- Immediato: più veloce
- Preavviso: giocatori apprezzano essere avvisati
- Graduale: riduce impatto ma prolunga development

---

## 📝 Note Finali

Questo documento rappresenta una proposta completa per ristrutturare il sistema Hunter con progressione basata su livello.

**Prossimi Step:**
1. ✅ **Revisione documento** con te
2. ✅ **Rispondere a domande aperte** insieme
3. ✅ **Finalizzare design** in base al feedback
4. ✅ **Iniziare implementazione** con priorità concordate

**Feedback Richiesto:**
- Quali parti del design approvi?
- Quali parti vorresti modificare?
- Risposte alle 10 domande aperte sopra
- Altre idee o suggerimenti?

---

**Fine Documento**
