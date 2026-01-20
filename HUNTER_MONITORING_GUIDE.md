# Hunter System - Guida Monitoraggio e Anti-Exploit

## 🔒 SISTEMI DI SICUREZZA IMPLEMENTATI

### 1. **Anti-Exploit Locks**
Ogni azione critica ha un lock temporaneo (2-3 secondi) per prevenire:
- ❌ Double-click exploit
- ❌ Acquisti multipli simultanei
- ❌ Claim multipli di achievement

**Lock implementati:**
- `hq_shop_lock` - Acquisti shop (2 sec)
- `hq_ach_lock` - Claim achievement singolo (2 sec)
- `hq_smart_claim_lock` - Claim achievement multipli (3 sec)

### 2. **Transazioni Atomiche**
**PRIMA (VULNERABILE):**
```lua
UPDATE points SET points = points - 100  -- Sottrae punti
give_item(item)                          -- Se fallisce, punti persi!
```

**DOPO (SICURO):**
```lua
give_item(item)                          -- Da item PRIMA
if success then
    UPDATE points SET points = points - 100  -- Solo se successo
end
```

### 3. **Logging Completo**

Tutte le transazioni sono registrate in tabelle di log:

#### **Tabella: `hunter_shop_purchases`**
Log di TUTTI gli acquisti shop.

**Campi:**
- `purchase_id` - ID univoco transazione
- `player_id` + `player_name` - Chi ha acquistato
- `item_id` - ID item nello shop
- `item_vnum` - Vnum item effettivo
- `item_count` - Quantità acquistata
- `price_paid` - Gloria spesa
- `purchased_at` - Timestamp acquisto

#### **Tabella: `hunter_achievements_claimed`**
Log di achievement riscossi.

**Campi:**
- `id` - ID univoco
- `player_id` - Chi ha riscosso
- `achievement_id` - Quale achievement
- `claimed_at` - Quando riscosso

#### **Tabella: `hunter_security_logs`**
Log di errori e eventi di sicurezza.

---

## 📊 QUERY DI MONITORAGGIO

### 🔍 **Trova Acquisti Sospetti (Possibili Exploit)**

```sql
-- Acquisti multipli dello stesso item in meno di 60 secondi
SELECT
    player_id,
    player_name,
    item_id,
    COUNT(*) as acquisti,
    MIN(purchased_at) as primo_acquisto,
    MAX(purchased_at) as ultimo_acquisto,
    TIMESTAMPDIFF(SECOND, MIN(purchased_at), MAX(purchased_at)) as secondi_totali
FROM srv1_hunabku.hunter_shop_purchases
WHERE purchased_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY player_id, item_id
HAVING acquisti > 3 AND secondi_totali < 60
ORDER BY acquisti DESC;
```

**Cosa cercare:**
- ✅ **Normale:** 1-2 acquisti dello stesso item in 1 ora
- ⚠️ **Sospetto:** 3+ acquisti in < 60 secondi
- 🚨 **EXPLOIT:** 5+ acquisti in < 10 secondi

---

### 💰 **Classifica Spese (Top Spender)**

```sql
-- Top 50 player per gloria spesa
SELECT
    player_id,
    player_name,
    SUM(price_paid) as gloria_totale_spesa,
    COUNT(*) as numero_acquisti,
    ROUND(SUM(price_paid) / COUNT(*), 2) as media_per_acquisto
FROM srv1_hunabku.hunter_shop_purchases
GROUP BY player_id, player_name
ORDER BY gloria_totale_spesa DESC
LIMIT 50;
```

**Come usarlo:**
- Verifica che i top spender non abbiano gloria impossibile
- Controlla che la gloria spesa corrisponda alla gloria guadagnata

---

### 🎯 **Item Più Acquistati**

```sql
-- Scopri quali item sono più popolari
SELECT
    s.id as item_id,
    s.description as nome_item,
    s.price_points as prezzo,
    COUNT(p.purchase_id) as volte_acquistato,
    SUM(p.price_paid) as gloria_totale_incassata
FROM srv1_hunabku.hunter_shop_purchases p
JOIN srv1_hunabku.hunter_quest_shop s ON p.item_id = s.id
GROUP BY s.id, s.description, s.price_points
ORDER BY volte_acquistato DESC
LIMIT 20;
```

**Utilità:**
- Identifica item troppo convenienti
- Bilancia economia in-game

---

### ⏰ **Acquisti Recenti (Ultime 24 ore)**

```sql
-- Vedi tutti gli acquisti delle ultime 24 ore
SELECT
    purchased_at,
    player_name,
    item_id,
    item_vnum,
    item_count,
    price_paid
FROM srv1_hunabku.hunter_shop_purchases
WHERE purchased_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY purchased_at DESC;
```

---

### 👤 **Storico Acquisti di un Player**

```sql
-- Sostituisci PLAYER_ID con l'ID del player da controllare
SELECT
    purchased_at,
    s.description as item_acquistato,
    p.item_count as quantita,
    p.price_paid as gloria_spesa
FROM srv1_hunabku.hunter_shop_purchases p
LEFT JOIN srv1_hunabku.hunter_quest_shop s ON p.item_id = s.id
WHERE p.player_id = PLAYER_ID
ORDER BY p.purchased_at DESC;
```

---

### 🏆 **Achievement Claims Sospetti**

```sql
-- Trova player che hanno claimato troppi achievement in poco tempo
SELECT
    player_id,
    COUNT(*) as achievement_riscossi,
    MIN(claimed_at) as primo_claim,
    MAX(claimed_at) as ultimo_claim,
    TIMESTAMPDIFF(MINUTE, MIN(claimed_at), MAX(claimed_at)) as minuti_totali
FROM srv1_hunabku.hunter_achievements_claimed
WHERE claimed_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY player_id
HAVING achievement_riscossi > 5 AND minuti_totali < 5
ORDER BY achievement_riscossi DESC;
```

**Cosa cercare:**
- ⚠️ **Sospetto:** 5+ achievement in < 5 minuti (potrebbe essere smart claim legittimo)
- 🚨 **EXPLOIT:** 10+ achievement in < 1 minuto (impossibile senza hack)

---

### 🔒 **Verifica Coerenza Gloria (Anti-Cheat)**

```sql
-- Confronta gloria guadagnata vs spesa
SELECT
    r.player_id,
    r.player_name,
    r.total_points as gloria_guadagnata,
    r.spendable_points as gloria_attuale,
    COALESCE(SUM(p.price_paid), 0) as gloria_spesa,
    (r.total_points - COALESCE(SUM(p.price_paid), 0)) as gloria_teorica_residua,
    (r.spendable_points - (r.total_points - COALESCE(SUM(p.price_paid), 0))) as differenza
FROM srv1_hunabku.hunter_quest_ranking r
LEFT JOIN srv1_hunabku.hunter_shop_purchases p ON r.player_id = p.player_id
GROUP BY r.player_id, r.player_name, r.total_points, r.spendable_points
HAVING ABS(differenza) > 100
ORDER BY ABS(differenza) DESC
LIMIT 50;
```

**Cosa cercare:**
- ✅ **OK:** `differenza` vicina a 0 (±100 margine errore)
- 🚨 **CHEAT:** `differenza` > 1000 (gloria modificata esternamente)

---

## 🚨 GESTIONE EXPLOIT TROVATI

### Se trovi un exploit:

1. **Identifica il player:**
   ```sql
   SELECT player_id, player_name FROM hunter_shop_purchases WHERE ...
   ```

2. **Verifica lo storico completo:**
   ```sql
   SELECT * FROM hunter_shop_purchases WHERE player_id = PLAYER_ID;
   SELECT * FROM hunter_security_logs WHERE player_id = PLAYER_ID;
   ```

3. **Calcola il danno:**
   ```sql
   SELECT SUM(price_paid) as gloria_rubata FROM hunter_shop_purchases
   WHERE player_id = PLAYER_ID AND purchased_at >= 'DATA_EXPLOIT';
   ```

4. **Rollback manuale (se necessario):**
   ```sql
   -- Rimuovi acquisti fraudolenti
   DELETE FROM hunter_shop_purchases WHERE player_id = PLAYER_ID AND purchased_at >= 'DATA_EXPLOIT';

   -- Ripristina gloria
   UPDATE hunter_quest_ranking SET spendable_points = spendable_points + GLORIA_RUBATA WHERE player_id = PLAYER_ID;
   ```

5. **Ban temporaneo:**
   - Usa il sistema di ban del server
   - Documenta l'exploit trovato

---

## ✅ BEST PRACTICES

### Monitoraggio Giornaliero:
```bash
# Ogni giorno controlla:
1. Acquisti sospetti (query exploit)
2. Top 10 spender (verifica coerenza)
3. Achievement claims anomali
4. Verifica coerenza gloria
```

### Monitoraggio Settimanale:
```bash
# Ogni settimana:
1. Analisi item più acquistati
2. Backup tabelle log
3. Pulizia vecchi log (> 90 giorni)
```

### Alert Automatici (Opzionale):
Puoi creare trigger SQL che loggano automaticamente attività sospette.

---

## 📁 FILE DA ESEGUIRE

1. **HUNTER_SHOP_PURCHASES_LOG.sql** - Crea tabella log acquisti
2. Questo file - Guida riferimento

---

## 🛡️ PROTEZIONI IMPLEMENTATE

✅ **Anti Double-Click:** Lock temporanei su tutte le azioni
✅ **Transazioni Atomiche:** Item dato PRIMA di sottrarre risorse
✅ **Logging Completo:** Ogni transazione registrata
✅ **Inventory Check:** Verificato ad ogni iterazione
✅ **Error Handling:** Rollback automatico se give_item fallisce
✅ **SQL Injection:** Tutti i nomi escaped con mysql_escape_string
✅ **Memory Leak:** Queue limit + cleanup automatico

---

## 📞 SUPPORTO

Se trovi nuovi exploit o hai domande:
1. Controlla prima i log con le query sopra
2. Documenta il comportamento sospetto
3. Fai backup dei log prima di modificare
