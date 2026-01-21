-- ============================================================
-- HUNTER LEVEL SYSTEM LIB (hg_lib) - STABLE VERSION 2025
-- ============================================================

hg_lib = {}

-- GESTIONE DATI TEMPORANEI SESSIONE
function hg_lib.get_temp_gate_data(pid)
    if not _G.hunter_temp_gate_data then
        _G.hunter_temp_gate_data = {}
    end
    return _G.hunter_temp_gate_data[pid] or {}
end

function hg_lib.set_temp_gate_data(pid, data)
    if not _G.hunter_temp_gate_data then
        _G.hunter_temp_gate_data = {}
    end
    _G.hunter_temp_gate_data[pid] = data
end

-- UTILITY STRINGHE
function hg_lib.clean_str(str)
    if str == nil then return "" end
    -- Sostituisce spazi con + per compatibilit� cmdchat
    local result = string.gsub(tostring(str), " ", "+")
    return result
end

-- SISTEMA NOTIFICHE UI (no spam chat)
function hg_lib.send_notification(player_pid, notif_type, message)
    --[[
        Invia una notifica alla finestra HunterNotification del client
        Args:
            player_pid: PID del giocatore (0 per player corrente)
            notif_type: Tipo notifica ("winner", "achievement", "rank", "system", "event")
            message: Testo del messaggio

        Esempio:
            hg_lib.send_notification(0, "achievement", "Hai completato il traguardo: Cacciatore Esperto!")
            hg_lib.send_notification(pid, "winner", "Hai vinto l'evento Elite Hunt con 150 punti!")
    ]]

    local pid = player_pid or 0
    if pid == 0 then
        pid = pc.get_player_id()
    end

    -- Valida tipo notifica
    local valid_types = {
        ["winner"] = true,
        ["achievement"] = true,
        ["rank"] = true,
        ["system"] = true,
        ["event"] = true
    }

    if not valid_types[notif_type] then
        notif_type = "system"
    end

    -- Pulisci messaggio per cmdchat (spazi -> +)
    local clean_msg = hg_lib.clean_str(message)

    -- Invia comando al client (usa | come separatore, non spazio)
    if pid > 0 then
        local current_pid = pc.get_player_id()
        if pid == current_pid then
            -- Player corrente, non serve begin_other_pc_block
            cmdchat("HunterNotification " .. notif_type .. "|" .. clean_msg)
        else
            -- Altro player, usa begin_other_pc_block
            q.begin_other_pc_block(pid)
            cmdchat("HunterNotification " .. notif_type .. "|" .. clean_msg)
            q.end_other_pc_block()
        end
    end
end

function hg_lib.send_notification_to_party(notif_type, message)
    --[[
        Invia una notifica a tutti i membri del party
        Esempio:
            hg_lib.send_notification_to_party("event", "Il party ha completato la frattura!")
    ]]
    if not party.is_party() then
        -- Solo il player corrente
        hg_lib.send_notification(0, notif_type, message)
        return
    end

    local pids = {party.get_member_pids()}
    for i, member_pid in ipairs(pids) do
        hg_lib.send_notification(member_pid, notif_type, message)
    end
end

-- STORAGE MULTI-VNUM PER EMERGENCY (max 5 vnums come flags separati)
-- pc.setqf accetta SOLO interi, non stringhe!
function hg_lib.set_emerg_vnums(vnum_str)
    -- Reset tutti i flag vnum
    for i = 1, 5 do
        pc.setqf("hq_emerg_vnum" .. i, 0)
    end

    if not vnum_str or vnum_str == "" or vnum_str == "0" then
        return
    end

    -- Parse la stringa e salva ogni vnum come flag separato
    local idx = 1
    for v in string.gfind(tostring(vnum_str), "([^,]+)") do
        v = string.gsub(v, "^%s*(.-)%s*$", "%1")  -- trim
        local vnum = tonumber(v)
        if vnum and vnum > 0 and idx <= 5 then
            pc.setqf("hq_emerg_vnum" .. idx, vnum)
            idx = idx + 1
        end
    end
end

function hg_lib.get_emerg_vnums()
    -- Ricostruisce la stringa dai flags
    local vnums = {}
    for i = 1, 5 do
        local v = pc.getqf("hq_emerg_vnum" .. i) or 0
        if v > 0 then
            table.insert(vnums, tostring(v))
        end
    end
    if table.getn(vnums) == 0 then
        return "0"
    end
    return table.concat(vnums, ",")
end

function hg_lib.clear_emerg_vnums()
    for i = 1, 5 do
        pc.setqf("hq_emerg_vnum" .. i, 0)
    end
end

function hg_lib.is_vnum_in_emerg_list(vnum)
    -- Controlla se un vnum è tra i vnums dell'emergency
    local vnum_n = tonumber(vnum) or 0
    if vnum_n == 0 then return false end

    -- Controlla il vnum singolo principale
    local main_vnum = pc.getqf("hq_emerg_vnum") or 0
    if main_vnum > 0 and main_vnum == vnum_n then
        return true
    end

    -- Controlla i multi-vnums
    local has_any_vnum = false
    for i = 1, 5 do
        local v = pc.getqf("hq_emerg_vnum" .. i) or 0
        if v > 0 then
            has_any_vnum = true
            if v == vnum_n then
                return true
            end
        end
    end

    -- Se non ci sono vnums specificati, qualsiasi mob conta
    if not has_any_vnum and main_vnum == 0 then
        return true
    end

    return false
end

-- VALIDAZIONE RANK
function hg_lib.validate_rank(rank)
    if rank == nil then return "E" end

    -- PRENDE SOLO LA PRIMA LETTERA (es. "N-Rank" diventa "N")
    local clean_rank = string.upper(string.sub(rank, 1, 1))

    local valid_ranks = {E=true, D=true, C=true, B=true, A=true, S=true, N=true}

    if valid_ranks[clean_rank] then
        return clean_rank
    end

    -- Se fallisce, ritorna E come sicurezza
    return "E"
end

-- RANK DAL LIVELLO - Usato per filtrare Emergency Quest
-- Rank E: Level 1-49, Rank D: 50-74, Rank C: 75-99, Rank B: 100-124, Rank A: 125-149, Rank S: 150-174, Rank N: 175+
function hg_lib.get_rank_from_level(level)
    level = level or 1
    if level >= 175 then return "N"
    elseif level >= 150 then return "S"
    elseif level >= 125 then return "A"
    elseif level >= 100 then return "B"
    elseif level >= 75 then return "C"
    elseif level >= 50 then return "D"
    else return "E"
    end
end

-- Range di livello per ogni rank (per filtro Emergency Quest)
function hg_lib.get_level_range_for_rank(rank)
    local ranges = {
        E = {min = 1, max = 49},
        D = {min = 50, max = 74},
        C = {min = 75, max = 99},
        B = {min = 100, max = 124},
        A = {min = 125, max = 149},
        S = {min = 150, max = 174},
        N = {min = 175, max = 200}
    }
    return ranges[rank] or ranges["E"]
end

-- CACHE MOB ELITE (FIX CRASH: Non cancella pi� la tabella globale brutalmente)
function hg_lib.load_elite_cache()
    -- Se la cache esiste ed � recente (< 1 ora), non ricaricare
    local now = get_time()
    if _G.hunter_elite_cache and _G.hunter_cache_loaded and (now - _G.hunter_cache_loaded < 3600) then
        return 
    end

    -- Inizializza solo se necessario
    if not _G.hunter_elite_cache then
        _G.hunter_elite_cache = {}
        _G.hunter_elite_data = {}  
    end

    local c, d = mysql_direct_query("SELECT vnum, name, type_name, base_points, rank_color FROM srv1_hunabku.hunter_quest_spawns WHERE enabled=1")

    if c > 0 then
        -- Ricostruiamo le tabelle interne senza nil-lare l'oggetto principale
        local new_cache = {}
        local new_data = {}

        for i = 1, c do
            local vnum = tonumber(d[i].vnum)
            new_cache[vnum] = true  
            new_data[vnum] = {
                name = d[i].name,
                type_name = d[i].type_name,
                base_points = tonumber(d[i].base_points) or 100,
                rank_color = d[i].rank_color or "BLUE"
            }
        end

        -- Swap sicuro
        _G.hunter_elite_cache = new_cache
        _G.hunter_elite_data = new_data
        _G.hunter_cache_loaded = now
    end
end

-- CACHE ONDATE DIFESA
function hg_lib.load_defense_waves_cache(rank_grade)
    rank_grade = hg_lib.validate_rank(rank_grade)

    if not _G.hunter_defense_waves_cache then
        _G.hunter_defense_waves_cache = {}
    end
    if not _G.hunter_defense_total_mobs then
        _G.hunter_defense_total_mobs = {}
    end

    if _G.hunter_defense_waves_cache[rank_grade] then
        return 
    end

    local q = "SELECT wave_number, spawn_time, mob_vnum, mob_count, spawn_radius FROM srv1_hunabku.hunter_fracture_defense_waves "
    q = q .. "WHERE rank_grade='" .. rank_grade .. "' AND enabled=1 ORDER BY wave_number"
    local c, d = mysql_direct_query(q)

    if c > 0 then
        _G.hunter_defense_waves_cache[rank_grade] = {}
        local total_mobs = 0

        for i = 1, c do
            local wave_num = tonumber(d[i].wave_number)
            local spawn_time = tonumber(d[i].spawn_time)
            local mob_vnum = tonumber(d[i].mob_vnum)
            local mob_count = tonumber(d[i].mob_count)
            local spawn_radius = tonumber(d[i].spawn_radius) or 7

            -- Conta il totale mob per questo rank
            total_mobs = total_mobs + mob_count

            if not _G.hunter_defense_waves_cache[rank_grade][wave_num] then
                _G.hunter_defense_waves_cache[rank_grade][wave_num] = {
                    spawn_time = spawn_time,
                    mobs = {}
                }
            end

            table.insert(_G.hunter_defense_waves_cache[rank_grade][wave_num].mobs, {
                vnum = mob_vnum,
                count = mob_count,
                radius = spawn_radius
            })
        end
        
        -- Salva il totale mob richiesti per questo rank
        _G.hunter_defense_total_mobs[rank_grade] = total_mobs
    end
end

-- Funzione helper per ottenere il totale mob richiesti
function hg_lib.get_defense_total_mobs(rank_grade)
    rank_grade = hg_lib.validate_rank(rank_grade)
    if _G.hunter_defense_total_mobs and _G.hunter_defense_total_mobs[rank_grade] then
        return _G.hunter_defense_total_mobs[rank_grade]
    end
    return 0
end

-- SALVATAGGIO DATI SU DB (FLUSH)
function hg_lib.flush_ranking_updates()
    local pid = pc.get_player_id()

    local pending_total_pts = tonumber(pc.getqf("hq_pending_total_pts")) or 0
    local pending_spendable_pts = tonumber(pc.getqf("hq_pending_spendable_pts")) or 0
    local pending_daily_pts = tonumber(pc.getqf("hq_pending_daily_pts")) or 0
    local pending_weekly_pts = tonumber(pc.getqf("hq_pending_weekly_pts")) or 0
    local pending_total_kills = tonumber(pc.getqf("hq_pending_total_kills")) or 0
    local pending_daily_kills = tonumber(pc.getqf("hq_pending_daily_kills")) or 0
    local pending_weekly_kills = tonumber(pc.getqf("hq_pending_weekly_kills")) or 0
    local pending_metins = tonumber(pc.getqf("hq_pending_metins")) or 0
    local pending_chests = tonumber(pc.getqf("hq_pending_chests")) or 0
    local pending_fractures = tonumber(pc.getqf("hq_pending_fractures")) or 0

    -- DETAILED STATS: Recupera tutti i pending dettagliati
    local pending_chest_e = tonumber(pc.getqf("hq_pending_chest_e")) or 0
    local pending_chest_d = tonumber(pc.getqf("hq_pending_chest_d")) or 0
    local pending_chest_c = tonumber(pc.getqf("hq_pending_chest_c")) or 0
    local pending_chest_b = tonumber(pc.getqf("hq_pending_chest_b")) or 0
    local pending_chest_a = tonumber(pc.getqf("hq_pending_chest_a")) or 0
    local pending_chest_s = tonumber(pc.getqf("hq_pending_chest_s")) or 0
    local pending_chest_n = tonumber(pc.getqf("hq_pending_chest_n")) or 0
    local pending_boss_easy = tonumber(pc.getqf("hq_pending_boss_easy")) or 0
    local pending_boss_medium = tonumber(pc.getqf("hq_pending_boss_medium")) or 0
    local pending_boss_hard = tonumber(pc.getqf("hq_pending_boss_hard")) or 0
    local pending_boss_elite = tonumber(pc.getqf("hq_pending_boss_elite")) or 0
    local pending_metin_normal = tonumber(pc.getqf("hq_pending_metin_normal")) or 0
    local pending_metin_special = tonumber(pc.getqf("hq_pending_metin_special")) or 0
    local pending_defense_wins = tonumber(pc.getqf("hq_pending_defense_wins")) or 0
    local pending_defense_losses = tonumber(pc.getqf("hq_pending_defense_losses")) or 0
    local pending_elite_kills = tonumber(pc.getqf("hq_pending_elite_kills")) or 0

    -- Check se c'è qualcosa da flushare (base o detailed)
    local has_pending = pending_total_pts > 0 or pending_total_kills > 0 or pending_metins > 0 or pending_chests > 0 or pending_fractures > 0
    local has_detailed = pending_chest_e > 0 or pending_chest_d > 0 or pending_chest_c > 0 or pending_chest_b > 0 or pending_chest_a > 0 or
                         pending_chest_s > 0 or pending_chest_n > 0 or pending_boss_easy > 0 or pending_boss_medium > 0 or pending_boss_hard > 0 or
                         pending_boss_elite > 0 or pending_metin_normal > 0 or pending_metin_special > 0 or pending_defense_wins > 0 or
                         pending_defense_losses > 0 or pending_elite_kills > 0

    -- Flush ranking se c'è qualcosa
    if has_pending or has_detailed then
        local q = "UPDATE srv1_hunabku.hunter_quest_ranking SET "
        q = q .. "total_points = total_points + " .. pending_total_pts .. ", "
        q = q .. "spendable_points = spendable_points + " .. pending_spendable_pts .. ", "
        q = q .. "daily_points = daily_points + " .. pending_daily_pts .. ", "
        q = q .. "weekly_points = weekly_points + " .. pending_weekly_pts .. ", "
        q = q .. "total_kills = total_kills + " .. pending_total_kills .. ", "
        q = q .. "daily_kills = daily_kills + " .. pending_daily_kills .. ", "
        q = q .. "weekly_kills = weekly_kills + " .. pending_weekly_kills .. ", "
        q = q .. "total_metins = total_metins + " .. pending_metins .. ", "
        q = q .. "total_chests = total_chests + " .. pending_chests .. ", "
        q = q .. "total_fractures = total_fractures + " .. pending_fractures .. ", "
        -- DETAILED STATS
        q = q .. "chests_e = chests_e + " .. pending_chest_e .. ", "
        q = q .. "chests_d = chests_d + " .. pending_chest_d .. ", "
        q = q .. "chests_c = chests_c + " .. pending_chest_c .. ", "
        q = q .. "chests_b = chests_b + " .. pending_chest_b .. ", "
        q = q .. "chests_a = chests_a + " .. pending_chest_a .. ", "
        q = q .. "chests_s = chests_s + " .. pending_chest_s .. ", "
        q = q .. "chests_n = chests_n + " .. pending_chest_n .. ", "
        q = q .. "boss_kills_easy = boss_kills_easy + " .. pending_boss_easy .. ", "
        q = q .. "boss_kills_medium = boss_kills_medium + " .. pending_boss_medium .. ", "
        q = q .. "boss_kills_hard = boss_kills_hard + " .. pending_boss_hard .. ", "
        q = q .. "boss_kills_elite = boss_kills_elite + " .. pending_boss_elite .. ", "
        q = q .. "metin_kills_normal = metin_kills_normal + " .. pending_metin_normal .. ", "
        q = q .. "metin_kills_special = metin_kills_special + " .. pending_metin_special .. ", "
        q = q .. "defense_wins = defense_wins + " .. pending_defense_wins .. ", "
        q = q .. "defense_losses = defense_losses + " .. pending_defense_losses .. ", "
        q = q .. "elite_kills = elite_kills + " .. pending_elite_kills .. " "
        q = q .. "WHERE player_id = " .. pid

        mysql_direct_query(q)

        -- Reset accumulatori base
        pc.setqf("hq_pending_total_pts", 0)
        pc.setqf("hq_pending_spendable_pts", 0)
        pc.setqf("hq_pending_daily_pts", 0)
        pc.setqf("hq_pending_weekly_pts", 0)
        pc.setqf("hq_pending_total_kills", 0)
        pc.setqf("hq_pending_daily_kills", 0)
        pc.setqf("hq_pending_weekly_kills", 0)
        pc.setqf("hq_pending_metins", 0)
        pc.setqf("hq_pending_chests", 0)
        pc.setqf("hq_pending_fractures", 0)
        -- Reset accumulatori detailed
        pc.setqf("hq_pending_chest_e", 0)
        pc.setqf("hq_pending_chest_d", 0)
        pc.setqf("hq_pending_chest_c", 0)
        pc.setqf("hq_pending_chest_b", 0)
        pc.setqf("hq_pending_chest_a", 0)
        pc.setqf("hq_pending_chest_s", 0)
        pc.setqf("hq_pending_chest_n", 0)
        pc.setqf("hq_pending_boss_easy", 0)
        pc.setqf("hq_pending_boss_medium", 0)
        pc.setqf("hq_pending_boss_hard", 0)
        pc.setqf("hq_pending_boss_elite", 0)
        pc.setqf("hq_pending_metin_normal", 0)
        pc.setqf("hq_pending_metin_special", 0)
        pc.setqf("hq_pending_defense_wins", 0)
        pc.setqf("hq_pending_defense_losses", 0)
        pc.setqf("hq_pending_elite_kills", 0)
    end

    -- SEMPRE flush Trial progress (una sola volta)
    hg_lib.flush_trial_progress()

    -- Security: Save session snapshot for anomaly detection
    hg_lib.save_session_snapshot()
end

-- ============================================================
-- BATCH TRIAL PROGRESS - Accumula e fluscia ogni 5 minuti
-- Invece di chiamare sp_update_trial_progress ad ogni kill
-- ============================================================
function hg_lib.add_trial_progress(progress_type, amount)
    amount = amount or 1
    local key = "hq_trial_" .. progress_type
    pc.setqf(key, (pc.getqf(key) or 0) + amount)
end

function hg_lib.flush_trial_progress()
    local pid = pc.get_player_id()
    
    -- Leggi accumulatori
    local boss_kills = pc.getqf("hq_trial_boss_kill") or 0
    local metin_kills = pc.getqf("hq_trial_metin_kill") or 0
    local chest_opens = pc.getqf("hq_trial_chest_open") or 0
    local fracture_seals = pc.getqf("hq_trial_fracture_seal") or 0
    
    -- Se nulla da flushare, esci
    if boss_kills == 0 and metin_kills == 0 and chest_opens == 0 and fracture_seals == 0 then
        return
    end
    
    -- UNA sola query batch invece di N chiamate SP
    -- Aggiorna direttamente la tabella hunter_player_trials
    local q = string.format([[
        UPDATE srv1_hunabku.hunter_player_trials 
        SET boss_kills = boss_kills + %d,
            metin_kills = metin_kills + %d,
            chest_opens = chest_opens + %d,
            fracture_seals = fracture_seals + %d
        WHERE player_id = %d AND status = 'in_progress'
    ]], boss_kills, metin_kills, chest_opens, fracture_seals, pid)
    
    mysql_direct_query(q)
    
    -- Reset accumulatori
    pc.setqf("hq_trial_boss_kill", 0)
    pc.setqf("hq_trial_metin_kill", 0)
    pc.setqf("hq_trial_chest_open", 0)
    pc.setqf("hq_trial_fracture_seal", 0)
    
    -- NOTA: Non chiamare check_trial_completion_status qui!
    -- Viene chiamata separatamente da on_fracture_seal e altri punti specifici
end

function hg_lib.add_pending_points(total_pts, daily_pts, weekly_pts)
    total_pts = tonumber(total_pts) or 0
    daily_pts = tonumber(daily_pts) or total_pts
    weekly_pts = tonumber(weekly_pts) or total_pts

    pc.setqf("hq_pending_total_pts", (pc.getqf("hq_pending_total_pts") or 0) + total_pts)
    pc.setqf("hq_pending_spendable_pts", (pc.getqf("hq_pending_spendable_pts") or 0) + total_pts)
    pc.setqf("hq_pending_daily_pts", (pc.getqf("hq_pending_daily_pts") or 0) + daily_pts)
    pc.setqf("hq_pending_weekly_pts", (pc.getqf("hq_pending_weekly_pts") or 0) + weekly_pts)
end

function hg_lib.add_pending_kill()
    pc.setqf("hq_pending_total_kills", (pc.getqf("hq_pending_total_kills") or 0) + 1)
    pc.setqf("hq_pending_daily_kills", (pc.getqf("hq_pending_daily_kills") or 0) + 1)
    pc.setqf("hq_pending_weekly_kills", (pc.getqf("hq_pending_weekly_kills") or 0) + 1)
    
    -- Security: Track kill rate
    hg_lib.track_kill()
end

-- UTILITY TEMPO
function hg_lib.format_time(h, m)
    local hh = tostring(h)
    local mm = tostring(m)
    if tonumber(h) < 10 then hh = "0" .. h end
    if tonumber(m) < 10 then mm = "0" .. m end
    return hh .. ":" .. mm
end

function hg_lib.modulo(a, b)
    return a - math.floor(a / b) * b
end

function hg_lib.get_hour_from_ts(ts)
    local t = os.date("*t", ts)
    return t.hour
end

function hg_lib.get_min_from_ts(ts)
    local t = os.date("*t", ts)
    return t.min
end

function hg_lib.get_sec_from_ts(ts)
    local t = os.date("*t", ts)
    return t.sec
end

function hg_lib.get_dow_from_ts(ts)
    local t = os.date("*t", ts)
    local wday = t.wday - 1 -- Lua wday: 1=Sun, Metin2 usually expects 0=Sun or 0=Mon depending on usage
    return wday
end

function hg_lib.get_day_db_from_ts(ts)
    local t = os.date("*t", ts)
    local wday = t.wday - 1
    if wday == 0 then return 7 end -- DB usa 1-7 (Lun-Dom)
    return wday
end

-- FIX: Utilizzo nativo di os.date per la data odierna
function hg_lib.get_today_date()
    return os.date("%Y-%m-%d")
end

-- ============================================================
-- DUNGEON/MAP UTILITY FUNCTIONS
-- ============================================================

-- Lista dei MAP_INDEX che sono dungeon (da dungeon_info.txt)
-- Queste mappe hanno restrizione rank frattura max C
_G.hunter_dungeon_maps = {
    [7] = true,   -- metin2_map_anglar_dungeon_01
    [12] = true,  -- plechito_easter2023_dungeon
    [13] = true,  -- plechito_wukong_dungeon
    [14] = true,  -- plechito_scorpion_dungeon
    [15] = true,  -- plechito_pirate_ship
    [16] = true,  -- metin2_map_whitedragoncave_boss
    [17] = true,  -- plechito_chamber_of_wisdom
    [18] = true,  -- plechito_demon_dungeon
    [19] = true,  -- plechito_ancient
    [20] = true,  -- plechito_lava_map_01
    [21] = true,  -- plechito_jiangshi_temple_1
    [24] = true,  -- plechito_pirate_ship2
    [25] = true,  -- metin2_map_whitedragoncave_boss2
    [26] = true,  -- map_hunter_elite
    [27] = true,  -- map_hunter_nozzera
    [28] = true,  -- hunter_map/plechito_andun_catacombs
    [29] = true,  -- hunter_map/plechito_skeletondragon_dungeon
    [30] = true,  -- hunter_map/plechito_shadow_deviltower
    [200] = true, -- hunter_map/elite/fear_dungeon
    [201] = true, -- hunter_map/elite/mushroom_dungeon
    [202] = true, -- hunter_map/elite/owl_dungeon
    [203] = true, -- hunter_map/elite/slime_cave
    [204] = true, -- hunter_map/elite/underwater_dungeon
    [205] = true, -- hunter_map/elite/crystal_dungeon
    [206] = true, -- hunter_map/elite/plechito_shadow_deviltower_e
}

-- Nomi mappe per il notice
_G.hunter_map_names = {
    [2] = "Capitale",
    [5] = "Zakatki",
    [6] = "Threeway",
    [7] = "Anglar Dungeon",
    [8] = "Mappa EXP",
    [9] = "Deserto",
    [10] = "Neve",
    [11] = "Natural Map",
    [12] = "Easter Dungeon",
    [13] = "Wukong Dungeon",
    [14] = "Scorpion Dungeon",
    [15] = "Nave Pirata",
    [16] = "Drago Bianco",
    [17] = "Camera Saggezza",
    [18] = "Demon Dungeon",
    [19] = "Ancient",
    [20] = "Lava Map",
    [21] = "Tempio Jiangshi",
    [22] = "Sohan",
    [23] = "Foresta",
    [24] = "Nave Pirata 2",
    [25] = "Drago Bianco 2",
    [26] = "Hunter Elite",
    [27] = "Nozzera",
    [28] = "Catacombe",
    [29] = "Skeleton Dragon",
    [30] = "Shadow Tower",
    [200] = "Fear Dungeon",
    [201] = "Mushroom Dungeon",
    [202] = "Owl Dungeon",
    [203] = "Slime Cave",
    [204] = "Underwater Dungeon",
    [205] = "Crystal Dungeon",
    [206] = "Shadow Tower E",
}

function hg_lib.is_dungeon_map(map_index)
    if not map_index then
        map_index = pc.get_map_index()
    end
    -- Normalizza map_index (rimuovi istanza dungeon: 17001 -> 17)
    local base_map = hg_lib.modulo(map_index, 10000)
    return _G.hunter_dungeon_maps[base_map] == true
end

function hg_lib.get_map_name(map_index)
    if not map_index then
        map_index = pc.get_map_index()
    end
    local base_map = hg_lib.modulo(map_index, 10000)
    return _G.hunter_map_names[base_map] or ("Mappa " .. base_map)
end

function hg_lib.get_channel()
    -- Il canale e' dato da: (map_index / 10000) + 1 per istanze
    -- Per mappe normali (map_index < 10000), il canale dipende dal server
    local map_index = pc.get_map_index()
    if map_index >= 10000 then
        -- Istanza dungeon, canale non rilevante
        return 0
    end
    -- Per mappe normali, usa get_server_id() o un altro metodo se disponibile
    -- Fallback: restituisce 1
    return pc.get_channel and pc.get_channel() or 1
end

-- Controlla se il rank e' ammesso nei dungeon (max C)
function hg_lib.is_rank_allowed_in_dungeon(rank_label)
    if not rank_label then return true end
    -- E, D, C sono ammessi nei dungeon
    -- B, A, S, N NON sono ammessi
    local first_char = string.sub(rank_label, 1, 1)
    if first_char == "B" or first_char == "A" or first_char == "S" or first_char == "N" then
        return false
    end
    return true
end

-- ============================================================
-- SECURITY LOG SYSTEM - Anti-Cheat/Exploit Detection
-- ============================================================

-- Severity levels: INFO, WARNING, ALERT, CRITICAL
-- Log types: SPAWN, DEFENSE, REWARD, KILL, FRACTURE, CHEST, GLORY, SUSPICIOUS

function hg_lib.security_log(log_type, severity, action, details)
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local map_idx = pc.get_map_index()
    local px, py = pc.get_x(), pc.get_y()

    -- Escape strings per SQL (SECURITY FIX)
    local safe_pname = mysql_escape_string(pname)
    local safe_action = string.gsub(action or "", "'", "''")
    local safe_details = string.gsub(details or "", "'", "''")

    local q = string.format(
        "CALL srv1_hunabku.sp_hunter_log(%d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d)",
        pid, safe_pname, log_type, severity, safe_action, safe_details, map_idx, px, py
    )
    mysql_direct_query(q)
end

-- Shortcut functions per comodita
function hg_lib.log_info(log_type, action, details)
    hg_lib.security_log(log_type, "INFO", action, details)
end

function hg_lib.log_warning(log_type, action, details)
    hg_lib.security_log(log_type, "WARNING", action, details)
end

function hg_lib.log_alert(log_type, action, details)
    hg_lib.security_log(log_type, "ALERT", action, details)
end

function hg_lib.log_critical(log_type, action, details)
    hg_lib.security_log(log_type, "CRITICAL", action, details)
end

-- ============================================================
-- KILL RATE MONITORING - Rileva bot/speed hack
-- ============================================================

function hg_lib.init_kill_tracking()
    if not _G.hunter_kill_tracking then
        _G.hunter_kill_tracking = {}
    end
end

function hg_lib.track_kill()
    hg_lib.init_kill_tracking()
    local pid = pc.get_player_id()
    local now = get_time()
    
    if not _G.hunter_kill_tracking[pid] then
        _G.hunter_kill_tracking[pid] = {
            kills = {},
            last_check = now,
            warning_count = 0
        }
    end
    
    local tracker = _G.hunter_kill_tracking[pid]
    
    -- Aggiungi timestamp kill
    table.insert(tracker.kills, now)
    
    -- Mantieni solo ultimi 60 secondi di kill
    local cutoff = now - 60
    local new_kills = {}
    for i = 1, table.getn(tracker.kills) do
        if tracker.kills[i] >= cutoff then
            table.insert(new_kills, tracker.kills[i])
        end
    end
    tracker.kills = new_kills
    
    -- Controlla ogni 30 secondi
    if now - tracker.last_check >= 30 then
        tracker.last_check = now
        local kill_count = table.getn(tracker.kills)
        
        -- Soglie di allarme (kill per minuto)
        -- >80 kill/min = WARNING (possibile bot efficiente)
        -- >120 kill/min = ALERT (molto sospetto)
        -- >200 kill/min = CRITICAL (sicuramente cheat)
        
        if kill_count > 2000 then
            hg_lib.log_critical("SUSPICIOUS", "EXTREME_KILL_RATE", 
                string.format("kills_per_min=%d warning_count=%d", kill_count, tracker.warning_count))
            tracker.warning_count = tracker.warning_count + 1
        elseif kill_count > 1200 then
            hg_lib.log_alert("SUSPICIOUS", "HIGH_KILL_RATE", 
                string.format("kills_per_min=%d warning_count=%d", kill_count, tracker.warning_count))
            tracker.warning_count = tracker.warning_count + 1
        elseif kill_count > 800 then
            hg_lib.log_warning("SUSPICIOUS", "ELEVATED_KILL_RATE", 
                string.format("kills_per_min=%d", kill_count))
        end
        
        -- Se troppe warning consecutive, logga critico
        if tracker.warning_count >= 5 then
            hg_lib.log_critical("SUSPICIOUS", "REPEATED_HIGH_KILL_RATE", 
                string.format("consecutive_warnings=%d", tracker.warning_count))
            tracker.warning_count = 0  -- Reset dopo log critico
        end
    end
end

-- ============================================================
-- REWARD VALIDATION - Rileva exploit ricompense
-- ============================================================

function hg_lib.validate_glory_reward(glory_amount, source, mob_vnum)
    local pid = pc.get_player_id()
    mob_vnum = mob_vnum or 0
    
    -- Limite massimo gloria per singola azione
    local max_single_glory = 5000  -- Massimo ragionevole per singolo evento
    
    if glory_amount > max_single_glory then
        hg_lib.log_alert("REWARD", "EXCESSIVE_GLORY", 
            string.format("amount=%d source=%s mob_vnum=%d max_allowed=%d", 
                glory_amount, source, mob_vnum, max_single_glory))
        return false
    end
    
    -- Traccia gloria totale guadagnata nella sessione
    if not _G.hunter_session_glory then
        _G.hunter_session_glory = {}
    end
    if not _G.hunter_session_glory[pid] then
        _G.hunter_session_glory[pid] = {total = 0, start_time = get_time()}
    end
    
    local session = _G.hunter_session_glory[pid]
    session.total = session.total + glory_amount
    
    -- Se guadagna >50000 gloria in meno di 1 ora, sospetto
    local elapsed = get_time() - session.start_time
    if elapsed > 0 and elapsed < 3600 and session.total > 50000 then
        local glory_per_hour = (session.total / elapsed) * 3600
        hg_lib.log_alert("REWARD", "HIGH_GLORY_RATE", 
            string.format("session_glory=%d elapsed_sec=%d projected_hourly=%d", 
                session.total, elapsed, glory_per_hour))
    end
    
    return true
end

-- ============================================================
-- DEFENSE VALIDATION - Rileva exploit difesa fratture
-- ============================================================

function hg_lib.log_defense_start(fracture_id, rank)
    hg_lib.log_info("DEFENSE", "DEFENSE_STARTED", 
        string.format("fracture_id=%d rank=%s", fracture_id or 0, rank or "?"))
end

function hg_lib.log_defense_complete(fracture_id, rank, success, duration, mobs_killed)
    local severity = "INFO"
    local action = success and "DEFENSE_SUCCESS" or "DEFENSE_FAILED"
    
    -- Se difesa completata troppo velocemente, sospetto
    local expected_duration = hg_lib.get_defense_duration(rank)
    if success and duration < (expected_duration * 0.5) then
        severity = "ALERT"
        action = "DEFENSE_TOO_FAST"
    end
    
    hg_lib.security_log("DEFENSE", severity, action, 
        string.format("fracture_id=%d rank=%s duration=%d expected=%d mobs_killed=%d", 
            fracture_id or 0, rank or "?", duration or 0, expected_duration, mobs_killed or 0))
end

function hg_lib.get_defense_duration(rank)
    rank = hg_lib.validate_rank(rank)
    local durations = {E=60, D=60, C=60, B=90, A=120, S=150, N=180}
    return durations[rank] or 60
end

-- ============================================================
-- SPAWN VALIDATION - Rileva exploit spawn
-- ============================================================

function hg_lib.log_spawn_event(spawn_type, mob_vnum, mob_count, source)
    -- Traccia spawn per sessione
    local pid = pc.get_player_id()
    if not _G.hunter_spawn_tracking then
        _G.hunter_spawn_tracking = {}
    end
    if not _G.hunter_spawn_tracking[pid] then
        _G.hunter_spawn_tracking[pid] = {
            total_spawns = 0,
            start_time = get_time(),
            by_type = {}
        }
    end
    
    local tracker = _G.hunter_spawn_tracking[pid]
    tracker.total_spawns = tracker.total_spawns + 1
    tracker.by_type[spawn_type] = (tracker.by_type[spawn_type] or 0) + 1
    
    -- Log normale
    hg_lib.log_info("SPAWN", "MOB_SPAWNED", 
        string.format("type=%s vnum=%d count=%d source=%s", 
            spawn_type, mob_vnum or 0, mob_count or 1, source or "unknown"))
    
    -- Se troppi spawn in poco tempo, sospetto
    local elapsed = get_time() - tracker.start_time
    if elapsed > 60 and tracker.total_spawns > 50 then
        local spawn_rate = tracker.total_spawns / (elapsed / 60)
        if spawn_rate > 30 then  -- >30 spawn/min = sospetto
            hg_lib.log_warning("SPAWN", "HIGH_SPAWN_RATE", 
                string.format("spawns=%d elapsed=%d rate_per_min=%.1f", 
                    tracker.total_spawns, elapsed, spawn_rate))
        end
    end
end

-- ============================================================
-- CHEST VALIDATION - Rileva exploit chest
-- ============================================================

function hg_lib.log_chest_open(chest_type, reward_glory, reward_items)
    local pid = pc.get_player_id()
    
    -- Traccia aperture chest
    if not _G.hunter_chest_tracking then
        _G.hunter_chest_tracking = {}
    end
    if not _G.hunter_chest_tracking[pid] then
        _G.hunter_chest_tracking[pid] = {
            total = 0,
            start_time = get_time(),
            by_type = {}
        }
    end
    
    local tracker = _G.hunter_chest_tracking[pid]
    tracker.total = tracker.total + 1
    tracker.by_type[chest_type] = (tracker.by_type[chest_type] or 0) + 1
    
    hg_lib.log_info("CHEST", "CHEST_OPENED", 
        string.format("type=%s glory=%d items=%s total_session=%d", 
            chest_type, reward_glory or 0, reward_items or "none", tracker.total))
    
    -- Se apre troppi chest in poco tempo
    local elapsed = get_time() - tracker.start_time
    if elapsed > 0 and tracker.total > 20 then
        local rate = (tracker.total / elapsed) * 3600  -- chest/ora
        if rate > 100 then  -- >100 chest/ora = sospetto
            hg_lib.log_alert("CHEST", "HIGH_CHEST_RATE", 
                string.format("total=%d elapsed=%d rate_per_hour=%.1f", 
                    tracker.total, elapsed, rate))
        end
    end
end

-- ============================================================
-- FRACTURE VALIDATION - Rileva exploit fratture
-- ============================================================

function hg_lib.log_fracture_interaction(fracture_id, action_type, rank)
    hg_lib.log_info("FRACTURE", action_type, 
        string.format("fracture_id=%d rank=%s", fracture_id or 0, rank or "?"))
end

function hg_lib.log_fracture_seal(fracture_id, rank, glory_gained)
    local pid = pc.get_player_id()
    
    -- Traccia sigilli per sessione
    if not _G.hunter_fracture_tracking then
        _G.hunter_fracture_tracking = {}
    end
    if not _G.hunter_fracture_tracking[pid] then
        _G.hunter_fracture_tracking[pid] = {
            seals = 0,
            start_time = get_time(),
            glory_total = 0
        }
    end
    
    local tracker = _G.hunter_fracture_tracking[pid]
    tracker.seals = tracker.seals + 1
    tracker.glory_total = tracker.glory_total + (glory_gained or 0)
    
    hg_lib.log_info("FRACTURE", "FRACTURE_SEALED", 
        string.format("fracture_id=%d rank=%s glory=%d total_seals=%d", 
            fracture_id or 0, rank or "?", glory_gained or 0, tracker.seals))
    
    -- Se sigilla troppe fratture in poco tempo
    local elapsed = get_time() - tracker.start_time
    if elapsed > 0 and elapsed < 3600 and tracker.seals > 10 then
        local rate = (tracker.seals / elapsed) * 3600
        if rate > 20 then  -- >20 fratture/ora = molto sospetto
            hg_lib.log_alert("FRACTURE", "HIGH_SEAL_RATE", 
                string.format("seals=%d elapsed=%d rate_per_hour=%.1f glory_total=%d", 
                    tracker.seals, elapsed, rate, tracker.glory_total))
        end
    end
end

-- ============================================================
-- SESSION SNAPSHOT - Salva statistiche periodiche
-- ============================================================

function hg_lib.save_session_snapshot()
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    
    -- Raccogli statistiche sessione
    local kills = 0
    local glory = 0
    local chests = 0
    local fractures = 0
    local avg_kill_interval = 0
    local min_kill_interval = 999999
    local anomaly_score = 0
    
    -- Kill tracking
    if _G.hunter_kill_tracking and _G.hunter_kill_tracking[pid] then
        local kt = _G.hunter_kill_tracking[pid]
        kills = table.getn(kt.kills)
        
        -- Calcola intervalli tra kill
        if kills > 1 then
            local intervals = {}
            for i = 2, kills do
                local interval = (kt.kills[i] - kt.kills[i-1]) * 1000  -- ms
                table.insert(intervals, interval)
                if interval < min_kill_interval then
                    min_kill_interval = interval
                end
            end
            
            -- Media
            local sum = 0
            for i = 1, table.getn(intervals) do
                sum = sum + intervals[i]
            end
            avg_kill_interval = sum / table.getn(intervals)
        end
        
        -- Anomaly: kill troppo veloci
        if min_kill_interval < 200 then  -- <200ms tra kill = impossibile umano
            anomaly_score = anomaly_score + 50
        elseif min_kill_interval < 500 then
            anomaly_score = anomaly_score + 20
        end
        
        -- Anomaly: warning count
        anomaly_score = anomaly_score + (kt.warning_count * 10)
    end
    
    -- Glory tracking
    if _G.hunter_session_glory and _G.hunter_session_glory[pid] then
        glory = _G.hunter_session_glory[pid].total
    end
    
    -- Chest tracking
    if _G.hunter_chest_tracking and _G.hunter_chest_tracking[pid] then
        chests = _G.hunter_chest_tracking[pid].total
    end
    
    -- Fracture tracking
    if _G.hunter_fracture_tracking and _G.hunter_fracture_tracking[pid] then
        fractures = _G.hunter_fracture_tracking[pid].seals
    end
    
    -- Salva snapshot
    if kills > 0 or glory > 0 or chests > 0 or fractures > 0 then
        local q = string.format(
            "INSERT INTO srv1_hunabku.hunter_player_stats_snapshot " ..
            "(player_id, player_name, snapshot_type, kills_count, glory_earned, chests_opened, " ..
            "fractures_completed, avg_kill_interval_ms, min_kill_interval_ms, anomaly_score) " ..
            "VALUES (%d, '%s', 'SESSION', %d, %d, %d, %d, %d, %d, %d)",
            pid, pname, kills, glory, chests, fractures, 
            avg_kill_interval, min_kill_interval == 999999 and 0 or min_kill_interval, anomaly_score
        )
        mysql_direct_query(q)
        
        -- Se anomaly score alto, logga
        if anomaly_score >= 50 then
            hg_lib.log_alert("SUSPICIOUS", "HIGH_ANOMALY_SCORE", 
                string.format("score=%d kills=%d glory=%d min_interval_ms=%d", 
                    anomaly_score, kills, glory, min_kill_interval))
        end
    end
end

-- LOGICA RANKING
function hg_lib.get_rank_letter(rank_num)
    local letters = {"E", "D", "C", "B", "A", "S", "N"}
    return letters[rank_num + 1] or "E"
end

function hg_lib.get_rank_index(points)
    local N = tonumber(hg_lib.get_config("rank_threshold_N")) or 1500000
    local S = tonumber(hg_lib.get_config("rank_threshold_S")) or 500000
    local A = tonumber(hg_lib.get_config("rank_threshold_A")) or 150000
    local B = tonumber(hg_lib.get_config("rank_threshold_B")) or 50000
    local C = tonumber(hg_lib.get_config("rank_threshold_C")) or 10000
    local D = tonumber(hg_lib.get_config("rank_threshold_D")) or 2000

    if points >= N then return 6
    elseif points >= S then return 5
    elseif points >= A then return 4
    elseif points >= B then return 3
    elseif points >= C then return 2
    elseif points >= D then return 1
    else return 0 end
end

function hg_lib.get_rank_index_by_letter(letter)
    -- Supporta sia "S" che "S-Rank"
    local ranks = {
        E = 0, D = 1, C = 2, B = 3, A = 4, S = 5, N = 6,
        ["E-Rank"] = 0, ["D-Rank"] = 1, ["C-Rank"] = 2, ["B-Rank"] = 3, 
        ["A-Rank"] = 4, ["S-Rank"] = 5, ["N-Rank"] = 6
    }
    return ranks[letter] or 0
end

-- COMUNICAZIONE CLIENT
function hg_lib.hunter_speak(msg)
    if msg == nil then return end
    local rank_num = pc.getqf("hq_rank_num")
    if not rank_num or rank_num == 0 then
        -- PERFORMANCE: Usa qf invece di query
        local pts = pc.getqf("hq_total_points") or 0
        rank_num = hg_lib.get_rank_index(pts)
        pc.setqf("hq_rank_num", rank_num)
    end
    local rank_key = hg_lib.get_rank_letter(rank_num)
    cmdchat("HunterSystemSpeak " .. rank_key .. "|" .. hg_lib.clean_str(msg))
end

function hg_lib.hunter_speak_color(msg, color_code)
    if msg == nil then return end
    cmdchat("HunterSystemSpeak " .. (color_code or "BLUE") .. "|" .. hg_lib.clean_str(msg))
end

-- Helper per syschat con colore (usa direttamente il testo italiano)
function hg_lib.syschat_t(key, fallback, replacements, color)
    color = color or "FFFFFF"
    local msg = fallback or key

    -- Applica sostituzioni {PLACEHOLDER}
    if replacements then
        for k, v in pairs(replacements) do
            msg = string.gsub(msg, "{" .. tostring(k) .. "}", tostring(v))
        end
    end

    -- Mostra direttamente con colore
    syschat("|cff" .. color .. msg .. "|r")
end

-- Versione legacy che usa syschat diretto (per messaggi non traducibili)
function hg_lib.syschat_raw(msg, color)
    if msg then
        if color then
            syschat("|cff" .. color .. msg .. "|r")
        else
            syschat(msg)
        end
    end
end

-- Helper per notice_all tradotto
function hg_lib.notice_t(key, fallback, replacements)
    local txt = hg_lib.get_text(key, replacements, fallback)
    if txt then
        notice_all(txt)
    end
end

-- SISTEMA EMERGENZE
-- Parametri opzionali: description, difficulty, penalty_pts, vnums (stringa con più vnum separati da virgola)
function hg_lib.start_emergency(title, seconds, mob_vnum, count, description, difficulty, penalty_pts, vnums)
    -- Non sovrascrivere una Emergency già attiva
    if pc.getqf("hq_emerg_active") == 1 then
        return false
    end

    local expire_time = get_time() + seconds

    -- Supporto multi-vnum: se vnums è fornito, usa quello, altrimenti usa mob_vnum singolo
    local vnum_str = tostring(mob_vnum or 0)
    if vnums and vnums ~= "" then
        vnum_str = vnums  -- Formato: "8052,8053" per esempio
    end

    -- Setta flag su TUTTI i membri del party (o solo player se solo)
    if party.is_party() then
        local leader_pid = party.get_leader_pid()
        -- PERFORMANCE FIX: Setta flag party globale per evitare loop inutili
        game.set_event_flag("hq_party_emergency_" .. leader_pid, 1)

        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_emerg_active", 1)
            pc.setqf("hq_emerg_vnum", mob_vnum or 0)
            hg_lib.set_emerg_vnums(vnum_str)  -- Multi-vnum come flags separati
            pc.setqf("hq_emerg_req", count)
            pc.setqf("hq_emerg_cur", 0)
            pc.setqf("hq_emerg_expire", expire_time)
            pc.setqf("hq_emerg_penalty_pts", penalty_pts or 0)
            q.end_other_pc_block()
        end
    else
        pc.setqf("hq_emerg_active", 1)
        pc.setqf("hq_emerg_vnum", mob_vnum or 0)
        hg_lib.set_emerg_vnums(vnum_str)  -- Multi-vnum come flags separati
        pc.setqf("hq_emerg_req", count)
        pc.setqf("hq_emerg_cur", 0)
        pc.setqf("hq_emerg_expire", expire_time)
        pc.setqf("hq_emerg_penalty_pts", penalty_pts or 0)
    end

    -- Invia UI a TUTTI i membri del party con dati estesi
    -- Formato: title|seconds|vnum|count|description|difficulty|penalty
    local desc_clean = hg_lib.clean_str(description or "Completa la sfida prima che scada il tempo!")
    local diff_clean = difficulty or "NORMAL"
    local penalty_str = tostring(penalty_pts or 0)
    local vnums_clean = hg_lib.clean_str(vnum_str)

    hg_lib.party_cmdchat("HunterEmergency " .. hg_lib.clean_str(title) .. "|" .. seconds .. "|" .. vnums_clean .. "|" .. count .. "|" .. desc_clean .. "|" .. diff_clean .. "|" .. penalty_str)
    cleartimer("hunter_emerg_tmr")
    loop_timer("hunter_emerg_tmr", 1)
end

function hg_lib.update_emergency(current_count)
    hg_lib.party_cmdchat("HunterEmergencyUpdate " .. current_count)
end

function hg_lib.end_emergency(status)
    if pc.getqf("hq_emerg_active") == 0 then return end

    -- IMPORTANTE: Salva i valori reward/penalty PRIMA di resettare i flag
    local bonus_pts = pc.getqf("hq_emerg_reward_pts") or 0
    local penalty_pts = pc.getqf("hq_emerg_penalty_pts") or 0
    local reward_vnum = pc.getqf("hq_emerg_reward_vnum") or 0
    local reward_count = pc.getqf("hq_emerg_reward_count") or 0

    -- Pulisci flag su TUTTI i membri del party
    if party.is_party() then
        local leader_pid = party.get_leader_pid()
        -- PERFORMANCE FIX: Clear flag party globale
        game.set_event_flag("hq_party_emergency_" .. leader_pid, 0)

        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_emerg_active", 0)
            pc.setqf("hq_emerg_vnum", 0)
            hg_lib.clear_emerg_vnums()
            pc.setqf("hq_emerg_req", 0)
            pc.setqf("hq_emerg_cur", 0)
            pc.setqf("hq_emerg_expire", 0)
            pc.setqf("hq_emerg_id", 0)
            pc.setqf("hq_emerg_reward_pts", 0)
            pc.setqf("hq_emerg_penalty_pts", 0)
            pc.setqf("hq_emerg_reward_vnum", 0)
            pc.setqf("hq_emerg_reward_count", 0)
            pc.setqf("hq_speedkill_active", 0)
            pc.setqf("hq_speedkill_vnum", 0)
            q.end_other_pc_block()
        end
    else
        pc.setqf("hq_emerg_active", 0)
        pc.setqf("hq_emerg_vnum", 0)
        hg_lib.clear_emerg_vnums()
        pc.setqf("hq_emerg_req", 0)
        pc.setqf("hq_emerg_cur", 0)
        pc.setqf("hq_emerg_expire", 0)
        pc.setqf("hq_emerg_id", 0)
        pc.setqf("hq_emerg_reward_pts", 0)
        pc.setqf("hq_emerg_penalty_pts", 0)
        pc.setqf("hq_emerg_reward_vnum", 0)
        pc.setqf("hq_emerg_reward_count", 0)
        pc.setqf("hq_speedkill_active", 0)
        pc.setqf("hq_speedkill_vnum", 0)
    end

    cleartimer("hunter_emerg_tmr")
    cleartimer("hq_speedkill_timer")

    local s_str = "FAIL"
    if status == "SUCCESS" then s_str = "SUCCESS" end

    -- Invia chiusura UI a TUTTI i membri del party
    hg_lib.party_cmdchat("HunterEmergencyClose " .. s_str)

    if status == "SUCCESS" then
        if bonus_pts > 0 then
            mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points=total_points+"..bonus_pts..", spendable_points=spendable_points+"..bonus_pts.." WHERE player_id="..pc.get_player_id())

            -- === SYSCHAT DETTAGLIATO EMERGENCY ===
            syschat("|cffFF6600========================================|r")
            hg_lib.syschat_t("EMERG_COMPLETED_TITLE", "[!!!] SFIDA EMERGENZA COMPLETATA [!!!]", nil, "FF6600")
            syschat("|cffFF6600========================================|r")
            syschat("")
            hg_lib.syschat_t("EMERG_REWARD", "Gloria Ricompensa: +{PTS}", {PTS = bonus_pts}, "FFD700")
            syschat("")
            hg_lib.syschat_t("EMERG_TOTAL", ">>> TOTALE: +{PTS} Gloria <<<", {PTS = bonus_pts}, "00FF00")
            syschat("|cffFF6600========================================|r")
            -- ======================================

            local msg = hg_lib.get_text("EMERG_VICTORY_MSG", {PTS = bonus_pts}, "[VITTORIA] SFIDA SUPERATA! +" .. bonus_pts .. " GLORIA EXTRA")
            hg_lib.hunter_speak_color(msg, "GOLD")
        else
            local msg = hg_lib.get_text("EMERG_COMPLETED", nil, "SFIDA COMPLETATA!")
            hg_lib.hunter_speak(msg)
        end

        if reward_vnum > 0 and reward_count > 0 then
            pc.give_item2(reward_vnum, reward_count)
            local msg = "BONUS OGGETTO: " .. hg_lib.item_name(reward_vnum) .. " x" .. reward_count
            hg_lib.hunter_speak(msg)
        end

        hg_lib.send_player_data()
    else
        -- PENALITA' per emergency quest fallita
        if penalty_pts > 0 then
            mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points=GREATEST(0, total_points-"..penalty_pts.."), spendable_points=GREATEST(0, spendable_points-"..penalty_pts..") WHERE player_id="..pc.get_player_id())

            syschat("|cffFF0000========================================|r")
            hg_lib.syschat_t("EMERG_FAILED_TITLE", "[!!!] SFIDA EMERGENZA FALLITA [!!!]", nil, "FF0000")
            syschat("|cffFF0000========================================|r")
            syschat("")
            hg_lib.syschat_t("EMERG_PENALTY", "Penalita' Gloria: -{PTS}", {PTS = penalty_pts}, "FF0000")
            syschat("")
            syschat("|cffFF0000========================================|r")

            local msg = "[FALLIMENTO] SFIDA FALLITA! -" .. penalty_pts .. " GLORIA"
            hg_lib.hunter_speak_color(msg, "RED")

            hg_lib.send_player_data()
        else
            local msg = "[!] TEMPO SCADUTO: Bonus Velocita' perso."
            hg_lib.hunter_speak_color(msg, "ORANGE")
        end
    end
end

-- FIX: Cooldown per notifiche rival (evita spam ogni pochi secondi)
-- Cooldown di 5 minuti (300 secondi) tra una notifica e l'altra per lo stesso tipo
function hg_lib.notify_rival(name, points, label)
    local pid = pc.get_player_id()
    local label_safe = label or "unknown"
    local cooldown_key = "hq_rival_cooldown_" .. string.gsub(label_safe, "%s+", "_")
    local last_notify = pc.getqf(cooldown_key) or 0
    local now = get_time()
    local cooldown_duration = 300  -- 5 minuti
    
    -- Se il cooldown non è scaduto, non inviare notifica
    if now - last_notify < cooldown_duration then
        return
    end
    
    -- Aggiorna timestamp ultimo notify
    pc.setqf(cooldown_key, now)
    
    -- Invia notifica
    cmdchat("HunterRivalAlert " .. hg_lib.clean_str(name) .. "|" .. points .. "|" .. hg_lib.clean_str(label))
end

function hg_lib.ask_choice_color(qid, text, opt1, opt2, opt3, color_code)
    local cmd = "HunterWhatIf " .. qid .. "|" .. hg_lib.clean_str(text) .. "|" .. hg_lib.clean_str(opt1) .. "|" .. hg_lib.clean_str(opt2)
    local o3_str = ""
    if opt3 and opt3 ~= "" then
        o3_str = hg_lib.clean_str(opt3)
    end
    cmd = cmd .. "|" .. o3_str
    cmd = cmd .. "|" .. color_code
    cmdchat(cmd)
end

-- ============================================================
-- CONFIG CACHE SYSTEM - Evita query ripetute per configurazioni statiche
-- Cache caricata una volta al login, valida per tutta la sessione
-- ============================================================
_G.hunter_config_cache = nil
_G.hunter_config_cache_time = 0
_G.hunter_rank_bonus_cache = nil

function hg_lib.load_config_cache()
    -- Ricarica solo se la cache è vuota o più vecchia di 10 minuti
    local now = get_time()
    if _G.hunter_config_cache and (now - _G.hunter_config_cache_time < 600) then
        return
    end
    
    _G.hunter_config_cache = {}
    _G.hunter_config_cache_time = now
    
    local c, d = mysql_direct_query("SELECT config_key, config_value FROM srv1_hunabku.hunter_quest_config")
    if c > 0 then
        for i = 1, c do
            local key = d[i].config_key
            local val = tonumber(d[i].config_value) or 0
            _G.hunter_config_cache[key] = val
        end
    end
    
    -- Carica anche i bonus rank in cache
    _G.hunter_rank_bonus_cache = {}
    local rc, rd = mysql_direct_query("SELECT min_points, bonus_gloria FROM srv1_hunabku.hunter_ranks ORDER BY min_points DESC")
    if rc > 0 then
        for i = 1, rc do
            table.insert(_G.hunter_rank_bonus_cache, {
                min_points = tonumber(rd[i].min_points) or 0,
                bonus = tonumber(rd[i].bonus_gloria) or 0
            })
        end
    end
end

-- CONFIG & DB HELPERS (OTTIMIZZATO CON CACHE)
function hg_lib.get_config(key)
    -- Prima controlla la cache
    if _G.hunter_config_cache and _G.hunter_config_cache[key] then
        return _G.hunter_config_cache[key]
    end
    
    -- Fallback a query diretta (solo se cache non disponibile)
    local q = "SELECT config_value FROM srv1_hunabku.hunter_quest_config WHERE config_key='" .. key .. "' LIMIT 1"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then 
        local val = tonumber(d[1].config_value) or 0
        -- Salva in cache per prossime chiamate
        if not _G.hunter_config_cache then _G.hunter_config_cache = {} end
        _G.hunter_config_cache[key] = val
        return val
    end
    return 0
end

function hg_lib.get_rank_bonus(points)
    -- Usa cache se disponibile
    if _G.hunter_rank_bonus_cache then
        for i, rank in ipairs(_G.hunter_rank_bonus_cache) do
            if points >= rank.min_points then
                return rank.bonus
            end
        end
        return 0
    end
    
    -- Fallback a query diretta
    local q = "SELECT bonus_gloria FROM srv1_hunabku.hunter_ranks WHERE min_points <= " .. points .. " ORDER BY min_points DESC LIMIT 1"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        return tonumber(d[1].bonus_gloria) or 0
    end
    return 0
end

function hg_lib.get_trial_gloria_multiplier()
    local pid = pc.get_player_id()
    local q = "SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_trials WHERE player_id=" .. pid .. " AND status='in_progress' LIMIT 1"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] and tonumber(d[1].cnt) > 0 then
        return 0.5
    end
    return 1.0
end

function hg_lib.get_streak_message(day_number)
    local q = "SELECT message_text FROM srv1_hunabku.hunter_login_messages WHERE day_number = " .. day_number .. " LIMIT 1"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        local msg = d[1].message_text
        if msg then return string.gsub(msg, "_", " ") end
    end
    q = "SELECT message_text FROM srv1_hunabku.hunter_login_messages WHERE day_number <= " .. day_number .. " ORDER BY day_number DESC LIMIT 1"
    c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        local msg = d[1].message_text
        if msg then return string.gsub(msg, "_", " ") end
    end
    return nil
end

-- Restituisce il testo (usa direttamente il fallback, no multilingua)
function hg_lib.get_text(key, replacements, fallback)
    local txt = fallback

    -- Applica replacements
    if txt and replacements then
        for k, v in pairs(replacements) do
            txt = string.gsub(txt, "{" .. k .. "}", tostring(v))
        end
    end

    return txt
end

-- Restituisce il testo con colore (usa direttamente il fallback)
function hg_lib.get_text_colored(key, replacements, fallback, default_color)
    local txt = fallback
    local color = default_color

    -- Applica replacements
    if txt and replacements then
        for k, v in pairs(replacements) do
            txt = string.gsub(txt, "{" .. k .. "}", tostring(v))
        end
    end

    -- Applica colore se presente
    if txt then
        if color and color ~= "" then
            return "|cff" .. color .. txt .. "|r"
        end
        return txt
    end

    return nil
end

function hg_lib.get_fracture_voice(color_code, has_points)
    local key = "fracture_voice_" .. (has_points and "ok_" or "no_") .. color_code
    local txt = hg_lib.get_text(key)
    if txt then return txt end
    if has_points then
        return "Il portale si apre davanti a te..."
    else
        return "Non sei ancora degno."
    end
end

-- ============================================================
-- POWER RANK SYSTEM - Sistema punti potere per fratture avanzate
-- ============================================================
-- Punti potere per grado Hunter
hg_lib.POWER_RANK_VALUES = {
    ["E"] = 1,   ["E-Rank"] = 1,
    ["D"] = 5,   ["D-Rank"] = 5,
    ["C"] = 15,  ["C-Rank"] = 15,
    ["B"] = 40,  ["B-Rank"] = 40,
    ["A"] = 80,  ["A-Rank"] = 80,
    ["S"] = 150, ["S-Rank"] = 150,
    ["N"] = 250, ["N-Rank"] = 250
}

-- Requisiti Power Rank letti dal database (colonna force_power_rank)
-- Se force_power_rank = 0 -> usa sistema classico Party 4+
-- Se force_power_rank > 0 -> usa sistema Power Rank

-- Ottiene i dati completi di una frattura dal DB
function hg_lib.get_fracture_data(fracture_vnum)
    local q = "SELECT req_points, force_power_rank FROM srv1_hunabku.hunter_quest_fractures WHERE vnum=" .. fracture_vnum
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        return {
            req_points = tonumber(d[1].req_points) or 0,
            force_power_rank = tonumber(d[1].force_power_rank) or 0
        }
    end
    return { req_points = 0, force_power_rank = 0 }
end

-- Ottiene il requisito Power Rank per una frattura dal DB
function hg_lib.get_fracture_power_rank_req(fracture_vnum)
    local data = hg_lib.get_fracture_data(fracture_vnum)
    return data.force_power_rank
end

-- Ottiene il grado Hunter di un player dato il player_id
-- Legge direttamente dalla colonna hunter_rank della tabella hunter_quest_ranking
function hg_lib.get_player_rank_grade(player_id)
    local q = "SELECT hunter_rank FROM srv1_hunabku.hunter_quest_ranking WHERE player_id = " .. player_id
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        local rank = d[1].hunter_rank or "E"
        -- Se il rank e' nel formato "X-Rank", estrai solo la lettera
        if string.len(rank) > 1 then
            local letter = string.match(rank, "^(%a)")
            return letter or "E"
        end
        return rank
    end
    return "E"
end

-- Calcola il Power Rank di un singolo player
function hg_lib.get_player_power_rank(player_id)
    local grade = hg_lib.get_player_rank_grade(player_id)
    return hg_lib.POWER_RANK_VALUES[grade] or 1
end

-- Calcola il Power Rank totale del party
-- NOTA: Semplificato - ritorna solo i dati del player corrente
-- perche' party.for_each_member non e' disponibile su tutti i server
function hg_lib.get_party_power_rank()
    local pid = pc.get_player_id()
    local my_power = hg_lib.get_player_power_rank(pid)
    local my_grade = hg_lib.get_player_rank_grade(pid)
    
    if not party.is_party() then
        return my_power, {{name = pc.get_name(), grade = my_grade, power = my_power}}
    end
    
    -- In party: moltiplica per numero membri (stima)
    local member_count = party.get_near_count()
    if member_count < 1 then member_count = 1 end
    
    -- Stima power totale basata sul player corrente
    local estimated_total = my_power * member_count
    
    return estimated_total, {{name = pc.get_name(), grade = my_grade, power = my_power}}
end

-- ============================================================
-- SISTEMA DISTRIBUZIONE GLORIA PER MERITOCRAZIA (PARTY)
-- NOTA: Semplificato per compatibilita' - ogni player riceve per se'
-- ============================================================

-- Calcola la percentuale di Gloria (semplificato: 100% al chiamante)
function hg_lib.calculate_party_glory_shares()
    local pid = pc.get_player_id()
    return {{
        pid = pid,
        name = pc.get_name(),
        grade = hg_lib.get_player_rank_grade(pid),
        power = hg_lib.get_player_power_rank(pid),
        share = 100
    }}
end

-- Distribuisce la Gloria a tutti i membri del party secondo la meritocrazia
-- Ogni membro riceve la sua % e applica i propri bonus/malus personali
function hg_lib.distribute_party_glory(base_glory, source_type)
    local shares = hg_lib.calculate_party_glory_shares()
    local distribution_log = {}
    
    for i = 1, table.getn(shares) do
        local member = shares[i]
        local pid = member.pid
        local share_percent = member.share
        
        -- Calcola la Gloria base per questo membro
        local member_base_glory = math.floor(base_glory * share_percent / 100)
        
        -- Minimo 1 punto se partecipa
        if member_base_glory < 1 and share_percent > 0 then
            member_base_glory = 1
        end
        
        -- Ora applica i bonus/malus PERSONALI di ogni membro
        local final_glory = hg_lib.apply_personal_glory_modifiers(pid, member_base_glory)
        
        -- Salva i punti per questo membro
        if final_glory > 0 then
            hg_lib.award_glory_to_player(pid, final_glory)
            
            table.insert(distribution_log, {
                name = member.name,
                grade = member.grade,
                share = share_percent,
                base = member_base_glory,
                final = final_glory
            })
        end
    end
    
    return distribution_log
end

-- ============================================================
-- FUNZIONE UNIFICATA CALCOLO MODIFICATORI GLORIA
-- Centralizza TUTTA la logica dei bonus/malus in un unico punto
-- Ritorna: final_glory, modifier_log (per syschat dettagliato)
-- ============================================================
function hg_lib.calculate_glory_with_modifiers(base_glory, options)
    options = options or {}
    local pid = options.player_id or pc.get_player_id()
    local consume_focus = (options.consume_focus ~= false)  -- Default: consuma
    local register_event = (options.register_event ~= false)  -- Default: registra

    local final_glory = base_glory
    local modifier_log = {}

    -- 1. STREAK BONUS (login consecutivi)
    local streak_bonus = pc.getqf("hq_streak_bonus") or 0
    if streak_bonus > 0 then
        local streak_add = math.floor(final_glory * streak_bonus / 100)
        final_glory = final_glory + streak_add
        table.insert(modifier_log, {name = "Streak Bonus", value = "+" .. streak_bonus .. "%", add = streak_add})
    end

    -- 2. RANK BONUS (rank alto = bonus extra)
    local player_pts = pc.getqf("hq_total_points") or 0
    local rank_bonus = hg_lib.get_rank_bonus(player_pts)
    if rank_bonus > 0 then
        local rank_add = math.floor(final_glory * rank_bonus / 100)
        final_glory = final_glory + rank_add
        table.insert(modifier_log, {name = "Rank Bonus", value = "+" .. rank_bonus .. "%", add = rank_add})
    end

    -- 3. FOCUS HUNTER (+20%)
    local has_focus = game.get_event_flag("hq_hunter_focus_"..pid) or 0
    if has_focus == 1 then
        local focus_add = math.floor(final_glory * 0.20)
        final_glory = final_glory + focus_add
        if consume_focus then
            game.set_event_flag("hq_hunter_focus_"..pid, 0)  -- Consuma il buff
        end
        table.insert(modifier_log, {name = "Focus Hunter", value = "+20%", add = focus_add})
    end

    -- 4. FRACTURE BONUS (+50% se missioni complete)
    if hg_lib.has_fracture_bonus() then
        local frac_add = math.floor(final_glory * 0.50)
        final_glory = final_glory + frac_add
        table.insert(modifier_log, {name = "Bonus Missioni", value = "+50%", add = frac_add})
    end

    -- 5. EVENTO ATTIVO (moltiplicatore evento)
    local evt_name, evt_mult, evt_type = hg_lib.get_active_event()
    if evt_type == "points" and evt_mult ~= 1.0 then
        local before_evt = final_glory
        final_glory = math.floor(final_glory * evt_mult)
        local evt_diff = final_glory - before_evt
        table.insert(modifier_log, {name = "Evento " .. (evt_name or ""), value = "x" .. evt_mult, add = evt_diff})
        -- Registra partecipazione all'evento
        if register_event then
            hg_lib.register_event_participant()
        end
    end

    -- 6. TRIAL MALUS (-50% se ha una prova attiva)
    local trial_mult = hg_lib.get_trial_gloria_multiplier()
    if trial_mult < 1.0 then
        local before_trial = final_glory
        final_glory = math.floor(final_glory * trial_mult)
        local trial_sub = before_trial - final_glory
        table.insert(modifier_log, {name = "Prova Esame", value = "-50%", add = -trial_sub})
    end

    -- 7. MALUS EMERGENCY QUEST ATTIVA (-80% Gloria) - SEMPRE PER ULTIMO
    if pc.getqf("hq_emerg_active") == 1 then
        local before_emerg = final_glory
        final_glory = math.floor(final_glory * 0.20)  -- Solo 20% = -80%
        local emerg_sub = before_emerg - final_glory
        table.insert(modifier_log, {name = "EMERGENCY ATTIVA", value = "-80%", add = -emerg_sub})
    end

    return final_glory, modifier_log
end

-- Mostra syschat dettagliato dei modificatori gloria
function hg_lib.show_glory_details(source_type, source_name, base_glory, final_glory, modifier_log)
    hg_lib.syschat_t("GLORY_DETAIL_HEADER", "========== DETTAGLIO GLORIA =========", nil, "888888")
    syschat("|cffFFFFFF" .. source_type .. ": |r|cffFFD700" .. source_name .. "|r")
    syschat("|cffAAAAAA" .. hg_lib.get_text("GLORY_BASE", nil, "Gloria Base") .. ": |r|cffFFFFFF" .. base_glory .. "|r")
    for i = 1, table.getn(modifier_log) do
        local m = modifier_log[i]
        local color = m.add >= 0 and "|cff00FF00" or "|cffFF4444"
        local sign = m.add >= 0 and "+" or ""
        syschat("|cffAAAAAA" .. m.name .. " (" .. m.value .. "): |r" .. color .. sign .. m.add .. "|r")
    end
    syschat("|cffFFD700>>> " .. hg_lib.get_text("TOTAL", nil, "TOTALE") .. ": +" .. final_glory .. " " .. hg_lib.get_text("GLORY", nil, "Gloria") .. " <<<|r")
    hg_lib.syschat_t("GLORY_DETAIL_FOOTER", "======================================", nil, "888888")
end

-- Applica i modificatori personali di Gloria (wrapper per compatibilita')
-- NOTA: Questa funzione viene chiamata nel contesto del player (pc.*)
function hg_lib.apply_personal_glory_modifiers(player_id, base_glory)
    local final_glory, _ = hg_lib.calculate_glory_with_modifiers(base_glory, {player_id = player_id})
    return final_glory
end

-- Assegna Gloria a un player specifico (senza bonus, solo accumulo)
function hg_lib.award_glory_to_player(player_id, glory_amount)
    if glory_amount <= 0 then return end
    
    -- Security: Validate glory amount
    if not hg_lib.validate_glory_reward(glory_amount, "award_glory", 0) then
        hg_lib.log_alert("REWARD", "GLORY_BLOCKED", 
            string.format("player_id=%d amount=%d blocked=true", player_id, glory_amount))
        return  -- Blocca reward sospetto
    end
    
    -- Aggiorna DB direttamente per il player
    mysql_direct_query(string.format(
        "UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + %d, spendable_points = spendable_points + %d, daily_points = daily_points + %d, weekly_points = weekly_points + %d WHERE player_id = %d",
        glory_amount, glory_amount, glory_amount, glory_amount, player_id
    ))
end

-- Notifica tutti i membri del party della distribuzione Gloria
-- NOTA: Semplificato - notifica solo il player corrente
function hg_lib.notify_party_glory_distribution(distribution_log, total_glory, source_name)
    if table.getn(distribution_log) <= 1 then return end  -- Solo, no notifica
    
    local msg_parts = {}
    for i = 1, table.getn(distribution_log) do
        local m = distribution_log[i]
        table.insert(msg_parts, m.name .. "(" .. m.grade .. "):" .. m.final)
    end
    
    local msg = "[PARTY] " .. source_name .. " - Gloria divisa: " .. table.concat(msg_parts, ", ")
    
    -- Notifica al player corrente
    syschat("|cff00FFFF" .. msg .. "|r")
    
    -- Manda anche al client per effetti
    cmdchat("HunterPartyGloryDist " .. total_glory .. "|" .. table.getn(distribution_log))
end

-- ============================================================
-- DISTRIBUZIONE GLORIA ELITE CON MERITOCRAZIA
-- NOTA: Semplificato - tutta la gloria va al killer
-- OTTIMIZZATO: Usa calculate_glory_with_modifiers centralizzata
-- ============================================================
function hg_lib.distribute_party_glory_elite(base_glory, mob_info)
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local grade = hg_lib.get_player_rank_grade(pid)
    local power = hg_lib.POWER_RANK_VALUES[grade] or 1

    -- USA FUNZIONE CENTRALIZZATA per calcolo modificatori
    local final_glory, modifier_log = hg_lib.calculate_glory_with_modifiers(base_glory, {player_id = pid})

    -- Assegna gloria al killer
    if final_glory > 0 then
        hg_lib.award_glory_to_player(pid, final_glory)
    end

    -- Mostra syschat dettagliato
    local mob_name = (mob_info and mob_info.name) or "Elite"
    local type_name = (mob_info and mob_info.type_name) or "ELITE"
    hg_lib.show_glory_details(type_name, mob_name, base_glory, final_glory, modifier_log)
    
    -- Log per notifica
    local distribution_log = {{
        name = pname,
        grade = grade,
        power = power,
        share = 100,
        base = base_glory,
        final = final_glory
    }}
    
    -- Notifica
    syschat("|cffFFD700[ELITE]|r " .. mob_name .. " - |cffFFD700+" .. final_glory .. " " .. hg_lib.get_text("GLORY", nil, "Gloria") .. "|r")

    return distribution_log
end

-- Notifica speciale per distribuzione meritocratica
function hg_lib.notify_party_glory_meritocracy(distribution_log, total_glory, source_name)
    -- Costruisci messaggio dettagliato
    local killed_txt = hg_lib.get_text("KILLED", nil, "ucciso")
    local total_txt = hg_lib.get_text("TOTAL", nil, "Totale")
    local msg_header = "|cffFFD700[PARTY " .. hg_lib.get_text("GLORY", nil, "GLORIA") .. "]|r " .. source_name .. " " .. killed_txt .. "! " .. total_txt .. ": " .. total_glory

    syschat(msg_header)
    hg_lib.syschat_t("MERITOCRACY_DIST", "--- Distribuzione per Meritocrazia (Power Rank) ---", nil, "00FFFF")
    
    -- Per ogni membro, mostra la sua quota
    for i = 1, table.getn(distribution_log) do
        local m = distribution_log[i]
        local detail = string.format("|cff00FF00%s|r [%s] PR:%d (%d%%) = |cffFFD700+%d Gloria|r",
            m.name, m.grade, m.power, m.share, m.final)
        
        syschat(detail)
    end
    
    -- Effetto client
    cmdchat("HunterPartyMeritGlory " .. total_glory .. "|" .. table.getn(distribution_log))
end

-- ============================================================
-- FINE SISTEMA DISTRIBUZIONE GLORIA
-- ============================================================

-- Verifica se il party puo' forzare una frattura
function hg_lib.can_force_fracture(fracture_vnum)
    local required = hg_lib.get_fracture_power_rank_req(fracture_vnum)
    
    -- Se non definito o 0, usa sistema classico (party 4+)
    if not required or required == 0 then
        return party.is_party() and party.get_near_count() >= 4, "CLASSIC", 0, 0, nil
    end
    
    -- Sistema Power Rank
    local total_power, members = hg_lib.get_party_power_rank()
    return total_power >= required, "POWER_RANK", total_power, required, members
end

-- Ottiene la descrizione del requisito per una frattura
function hg_lib.get_fracture_requirement_text(fracture_vnum)
    local required = hg_lib.get_fracture_power_rank_req(fracture_vnum)
    
    if not required or required == 0 then
        return "Party di 4+ membri", "CLASSIC"
    end
    
    return "Power Rank: " .. required .. " punti", "POWER_RANK"
end

-- ============================================================
-- OTTIMIZZAZIONE item_name - Cache nomi item
-- ============================================================
_G.hunter_item_name_cache = {}

function hg_lib.item_name(vnum)
    if not vnum or vnum == 0 then
        return "Oggetto Sconosciuto"
    end
    
    -- PERFORMANCE: Check cache prima
    if _G.hunter_item_name_cache[vnum] then
        return _G.hunter_item_name_cache[vnum]
    end
    
    -- Prima prova dalla tabella hunter personalizzata (nomi italiani)
    local c, d = mysql_direct_query("SELECT name FROM srv1_hunabku.hunter_item_names WHERE vnum=" .. vnum)
    if c > 0 and d[1] and d[1].name then
        _G.hunter_item_name_cache[vnum] = d[1].name
        return d[1].name
    end
    
    -- Dizionario locale per item comuni Hunter
    local hunter_items = {
        [63000] = "Baule Rango E",
        [63001] = "Baule Rango D",
        [63002] = "Baule Rango C",
        [63003] = "Baule Rango B",
        [63004] = "Baule Rango A",
        [63005] = "Baule Rango S",
        [63006] = "Baule Rango ???",
        [63007] = "Baule Speciale",
        [63010] = "Scanner Frattura",
        [63011] = "Focus del Cacciatore",
        [63012] = "Chiave Dimensionale",
        [63013] = "Calibratore Fratture",
        [63014] = "Stabilizzatore Portale",
        [63015] = "Amuleto Risonanza",
        [63020] = "Buono Gloria",
        [63021] = "Buono Gloria x3",
        [63022] = "Buono Gloria x5",
        [63030] = "Frammento di Monarca",
        [63031] = "Essenza Ombra",
        [63032] = "Cristallo Dimensionale",
    }
    
    if hunter_items[vnum] then
        _G.hunter_item_name_cache[vnum] = hunter_items[vnum]  -- Cache anche i locali
        return hunter_items[vnum]
    end
    
    local name = "Item_" .. vnum
    _G.hunter_item_name_cache[vnum] = name  -- Cache anche i fallback
    return name
end

-- EVENTI PROGRAMMATI
function hg_lib.get_active_event()
    local event = hg_lib.get_current_scheduled_event()

    if event then
        local name = event.event_name or "Evento"
        local etype = event.event_type or "glory_rush"
        local glory = tonumber(event.reward_glory_base) or 50
        local desc = event.event_desc or ""

        -- Legge il moltiplicatore dal DB (colonna glory_multiplier), default basato su type
        local custom_mult = tonumber(event.glory_multiplier)

        local mult = 1.0
        local apply_to = "points"

        if etype == "glory_rush" then
            mult = custom_mult or 2.0  -- Default x2, ma usa DB se presente
            apply_to = "points"
            desc = "Gloria x" .. mult
        elseif etype == "first_rift" or etype == "rift_hunt" then
            mult = custom_mult or 1.5
            apply_to = "chance"
            desc = "Fratture +" .. math.floor((mult - 1) * 100)
        elseif etype == "double_spawn" then
            mult = custom_mult or 2.0
            apply_to = "chance"
            desc = "Spawn x" .. mult
        elseif etype == "super_metin" or etype == "metin_frenzy" then
            mult = custom_mult or 1.5
            apply_to = "chance"
            desc = "Metin +" .. math.floor((mult - 1) * 100)
        elseif etype == "first_boss" or etype == "boss_massacre" then
            mult = custom_mult or 1.5
            apply_to = "points"
            desc = "Boss Glory +" .. math.floor((mult - 1) * 100)
        else
            -- Tipo sconosciuto ma con moltiplicatore custom
            if custom_mult then
                mult = custom_mult
                apply_to = "points"
                desc = "Gloria x" .. mult
            end
        end

        return name, mult, apply_to, desc
    end

    return nil, 1.0, nil, nil
end

function hg_lib.get_current_scheduled_event()
    local t = os.date("*t")
    local wday = t.wday - 1
    local day_db = wday
    if wday == 0 then day_db = 7 end
        
    local current_hour = t.hour
    local current_minute = t.min
    local current_total = current_hour * 60 + current_minute
        
    local q = "SELECT id, event_name, event_type, event_desc, start_hour, start_minute, duration_minutes, min_rank, reward_glory_base, reward_glory_winner, color_scheme, glory_multiplier FROM srv1_hunabku.hunter_scheduled_events WHERE enabled=1 AND FIND_IN_SET(" .. day_db .. ", days_active) > 0 ORDER BY start_hour, start_minute"
        
    local c, d = mysql_direct_query(q)
        
    if c > 0 then
        for i = 1, c do
            local e = d[i]
            local start_hour = tonumber(e.start_hour) or 0
            local start_minute = tonumber(e.start_minute) or 0
            local duration = tonumber(e.duration_minutes) or 30
                
            local start_total = start_hour * 60 + start_minute
            local end_total = start_total + duration
                
            if current_total >= start_total and current_total < end_total then
                return e
            end
        end
    end
        
    return nil
end

-- SISTEMA SORTEGGIO EVENTO
function hg_lib.register_event_participant()
    local event = hg_lib.get_current_scheduled_event()
    if not event then return false end

    local event_id = tonumber(event.id)
    local event_name = event.event_name or "Evento"
    local winner_prize = tonumber(event.reward_glory_winner) or 200
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local today = os.date("%Y-%m-%d")

    -- Controlla se gia registrato oggi per questo evento
    local check_q = string.format(
        "SELECT id FROM srv1_hunabku.hunter_event_participants WHERE event_id=%d AND player_id=%d AND DATE(joined_at)='%s'",
        event_id, pid, today
    )
    local c = mysql_direct_query(check_q)

    if c == 0 then
        -- Prima partecipazione oggi, registra
        local insert_q = string.format(
            "INSERT INTO srv1_hunabku.hunter_event_participants (event_id, player_id, player_name, joined_at) VALUES (%d, %d, '%s', NOW())",
            event_id, pid, mysql_escape_string(pname)
        )
        mysql_direct_query(insert_q)

        -- Ottieni il rank del player per l'annuncio
        local rc, rd = mysql_direct_query("SELECT total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
        local pts = 0
        if rc > 0 and rd[1] then pts = tonumber(rd[1].total_points) or 0 end
        local rank_key = hg_lib.get_rank_key(pts)

        -- NOTICE_ALL: Annuncia la partecipazione in stile Solo Leveling
        local rank_colors = {
            E = "|cff808080", D = "|cff8B4513", C = "|cff00FF00",
            B = "|cff00BFFF", A = "|cffFFD700", S = "|cffFF4500", N = "|cffFF00FF"
        }
        local rcolor = rank_colors[rank_key] or "|cffFFFFFF"
        notice_all("|cffFFD700[SISTEMA]|r " .. rcolor .. pname .. " [" .. rank_key .. "-Rank]|r |cff00FF00si e' candidato al premio di|r |cffFFD700" .. event_name .. "|r")

        -- Notifica personale in stile Solo Leveling
        syschat("|cff00FF00=============================================|r")
        syschat("|cffFFD700       [REGISTRAZIONE COMPLETATA]|r")
        syschat("|cff00FF00=============================================|r")
        syschat("")
        syschat("|cffFFFFFF   Il Sistema ha registrato la tua presenza.|r")
        syschat("|cffFFFFFF   Sei ora in lizza per il premio finale.|r")
        syschat("")
        syschat("|cffFFD700   Premio Sorteggio: +" .. winner_prize .. " Gloria|r")
        syschat("")
        syschat("|cff888888   'La fortuna favorisce gli audaci.'|r")
        syschat("|cff00FF00=============================================|r")

        hg_lib.hunter_speak_color("CANDIDATURA ACCETTATA. RESTA IN GIOCO.", "GOLD")
        cmdchat("HunterEventJoined " .. event_id .. "|" .. hg_lib.clean_str(event_name) .. "|0")

        pc.setqf("hq_event_registered", 1)
        return true
    else
        -- GIA' REGISTRATO - Non mostrare nulla qui, verra' mostrato dal notify
        pc.setqf("hq_event_registered", 1)
        return false
    end
end

-- ============================================================
-- EVENTI "PRIMO VINCE" (first_rift, first_boss)
-- ============================================================
function hg_lib.check_first_rift_winner()
    local event = hg_lib.get_current_scheduled_event()
    if not event then return end
    
    local etype = event.event_type or ""
    if etype ~= "first_rift" then return end
    
    local event_id = tonumber(event.id)
    local today = os.date("%Y-%m-%d")
    
    -- Controlla se c'e' gia' un vincitore oggi per questo evento
    local check_q = string.format(
        "SELECT id FROM srv1_hunabku.hunter_event_winners WHERE event_id=%d AND DATE(won_at)='%s' AND winner_type='first_rift'",
        event_id, today
    )
    local c = mysql_direct_query(check_q)
    
    if c > 0 then
        -- Gia' c'e' un vincitore oggi, niente da fare
        return
    end
    
    -- QUESTO PLAYER E' IL PRIMO! Assegna il premio
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local glory_prize = tonumber(event.reward_glory_winner) or 500
    local event_name = event.event_name or "Frattura della Sera"
    
    -- Dai la gloria al vincitore
    mysql_direct_query(string.format(
        "UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + %d, spendable_points = spendable_points + %d WHERE player_id=%d",
        glory_prize, glory_prize, pid
    ))
    
    -- Registra come vincitore "first_rift"
    mysql_direct_query(string.format(
        "INSERT INTO srv1_hunabku.hunter_event_winners (event_id, player_id, player_name, winner_type, winner_data, won_at) VALUES (%d, %d, '%s', 'first_rift', '%d', NOW())",
        event_id, pid, mysql_escape_string(pname), glory_prize
    ))
    
    -- Notifica il vincitore
    local msg = hg_lib.get_text("EVENT_FIRST_WIN", {PTS = glory_prize}, "SEI IL PRIMO! HAI VINTO +" .. glory_prize .. " GLORIA!")
    hg_lib.hunter_speak_color(msg, "GOLD")
    syschat("|cffFFD700========================================|r")
    hg_lib.syschat_t("EVENT_FIRST_RIFT_TITLE", "[!] PRIMO A CONQUISTARE LA FRATTURA [!]", nil, "00FF00")
    hg_lib.syschat_t("EVENT_PRIZE", "Premio: +{PTS} Gloria!", {PTS = glory_prize}, "FFD700")
    syschat("|cffFFD700========================================|r")

    -- Annuncia a tutti
    notice_all("|cffFFD700[" .. hg_lib.get_text("EVENT", nil, "EVENTO") .. " " .. string.upper(event_name) .. "]|r")
    local first_msg = hg_lib.get_text("EVENT_FIRST_RIFT_ANNOUNCE", {NAME = pname}, pname .. " e' il PRIMO a conquistare una frattura!")
    notice_all("|cff00FF00" .. first_msg .. "|r")
    notice_all("|cffFFD700" .. hg_lib.get_text("EVENT_PRIZE", {PTS = glory_prize}, "Premio: +" .. glory_prize .. " Gloria!") .. "|r")
    
    hg_lib.send_player_data()
end

function hg_lib.check_first_boss_winner(boss_vnum)
    local event = hg_lib.get_current_scheduled_event()
    if not event then return end
    
    local etype = event.event_type or ""
    if etype ~= "first_boss" then return end
    
    local event_id = tonumber(event.id)
    local today = os.date("%Y-%m-%d")
    
    -- Controlla se c'e' gia' un vincitore oggi per questo evento
    local check_q = string.format(
        "SELECT id FROM srv1_hunabku.hunter_event_winners WHERE event_id=%d AND DATE(won_at)='%s' AND winner_type='first_boss'",
        event_id, today
    )
    local c = mysql_direct_query(check_q)
    
    if c > 0 then return end
    
    -- QUESTO PLAYER E' IL PRIMO! Assegna il premio
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local glory_prize = tonumber(event.reward_glory_winner) or 500
    local event_name = event.event_name or "Caccia al Boss"
    
    -- Dai la gloria
    mysql_direct_query(string.format(
        "UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + %d, spendable_points = spendable_points + %d WHERE player_id=%d",
        glory_prize, glory_prize, pid
    ))
    
    -- Registra vincitore
    mysql_direct_query(string.format(
        "INSERT INTO srv1_hunabku.hunter_event_winners (event_id, player_id, player_name, winner_type, winner_data, won_at) VALUES (%d, %d, '%s', 'first_boss', '%d', NOW())",
        event_id, pid, mysql_escape_string(pname), glory_prize
    ))
    
    -- === SYSCHAT DETTAGLIATO EVENTO VINCITORE ===
    syschat("|cffFFD700========================================|r")
    hg_lib.syschat_t("EVENT_FIRST_WINNER_TITLE", "[!!!] PRIMO CLASSIFICATO EVENTO [!!!]", nil, "FFD700")
    syschat("|cffFFD700========================================|r")
    syschat("")
    syschat("|cff00FFFF  " .. hg_lib.get_text("EVENT", nil, "Evento") .. ":|r |cffFFFFFF" .. event_name .. "|r")
    hg_lib.syschat_t("EVENT_YOU_WERE_FIRST", "Sei stato il PRIMO!", nil, "00FF00")
    syschat("")
    hg_lib.syschat_t("EVENT_GLORY_PRIZE", "Premio Gloria: +{PTS}", {PTS = glory_prize}, "FFD700")
    syschat("")
    hg_lib.syschat_t("EVENT_TOTAL", ">>> TOTALE: +{PTS} Gloria <<<", {PTS = glory_prize}, "00FF00")
    syschat("|cffFFD700========================================|r")
    -- =============================================
    
    -- Notifica
    local msg = hg_lib.get_text("EVENT_FIRST_WIN", {PTS = glory_prize}, "SEI IL PRIMO! HAI VINTO +" .. glory_prize .. " GLORIA!")
    hg_lib.hunter_speak_color(msg, "GOLD")
    local boss_msg = hg_lib.get_text("EVENT_FIRST_BOSS_ANNOUNCE", {NAME = pname, PTS = glory_prize}, pname .. " e' il PRIMO a uccidere un boss! +" .. glory_prize .. " Gloria!")
    notice_all("|cffFFD700[" .. hg_lib.get_text("EVENT", nil, "EVENTO") .. " " .. string.upper(event_name) .. "]|r " .. boss_msg)
    
    hg_lib.send_player_data()
end

function hg_lib.draw_event_winner(event_id)
    -- Prima controlla il tipo evento - se e' "primo vince" non fare sorteggio
    local type_q = string.format("SELECT event_type FROM srv1_hunabku.hunter_scheduled_events WHERE id=%d", event_id)
    local tc, td = mysql_direct_query(type_q)
    if tc > 0 then
        local etype = td[1].event_type or "glory_rush"
        if etype == "first_rift" or etype == "first_boss" then
            -- Per questi eventi il vincitore e' gia' stato assegnato durante l'azione
            -- Non fare sorteggio casuale
            return nil, 0
        end
    end
    
    -- Seleziona vincitore casuale tra i partecipanti di oggi
    local today = os.date("%Y-%m-%d")
    
    local q = string.format(
        "SELECT player_id, player_name FROM srv1_hunabku.hunter_event_participants WHERE event_id=%d AND DATE(joined_at)='%s' ORDER BY RAND() LIMIT 1",
        event_id, today
    )
    local c, d = mysql_direct_query(q)
    
    if c > 0 then
        local winner_id = tonumber(d[1].player_id)
        local winner_name = d[1].player_name
        
        -- Prendi la ricompensa dell'evento
        local eq = string.format("SELECT reward_glory_winner, event_name FROM srv1_hunabku.hunter_scheduled_events WHERE id=%d", event_id)
        local ec, ed = mysql_direct_query(eq)
        local glory_prize = 500
        local event_name = "Evento"
        if ec > 0 then
            glory_prize = tonumber(ed[1].reward_glory_winner) or 500
            event_name = ed[1].event_name or "Evento"
        end
        
        -- Dai la gloria al vincitore
        mysql_direct_query(string.format(
            "UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + %d, spendable_points = spendable_points + %d WHERE player_id=%d",
            glory_prize, glory_prize, winner_id
        ))
        
        -- Registra nella tabella vincitori
        mysql_direct_query(string.format(
            "INSERT INTO srv1_hunabku.hunter_event_winners (event_id, player_id, player_name, winner_type, winner_data, won_at) VALUES (%d, %d, '%s', 'lottery', '%d', NOW())",
            event_id, winner_id, mysql_escape_string(winner_name), glory_prize
        ))
        
        -- Pulisci i partecipanti di oggi per questo evento
        mysql_direct_query(string.format(
            "DELETE FROM srv1_hunabku.hunter_event_participants WHERE event_id=%d AND DATE(joined_at)='%s'",
            event_id, today
        ))
        
        -- Annuncia il vincitore a tutti
        local lottery_msg = hg_lib.get_text("EVENT_LOTTERY_WIN", {NAME = winner_name, PTS = glory_prize}, winner_name .. " ha vinto +" .. glory_prize .. " Gloria!")
        notice_all("|cffFFD700[" .. hg_lib.get_text("HUNTER_LOTTERY", nil, "HUNTER ESTRAZIONE") .. "]|r " .. lottery_msg)
        local congrats_msg = hg_lib.get_text("EVENT_CONGRATS", {EVENT = event_name}, "Congratulazioni al vincitore dell'evento " .. event_name .. "!")
        notice_all("|cff00FF00" .. congrats_msg .. "|r")

        -- Se il vincitore è il player corrente, mostra syschat dettagliato
        local current_pid = pc.get_player_id()
        if current_pid == winner_id then
            syschat("|cffFFD700=============================================|r")
            hg_lib.syschat_t("EVENT_LOTTERY_TITLE", "[!!!] HAI VINTO L'ESTRAZIONE! [!!!]", nil, "FFD700")
            syschat("|cffFFD700=============================================|r")
            syschat("")
            syschat("|cff00FFFF  " .. hg_lib.get_text("EVENT", nil, "Evento") .. ":|r |cffFFFFFF" .. event_name .. "|r")
            hg_lib.syschat_t("EVENT_LOTTERY_EXTRACTED", "Sei stato estratto tra i partecipanti!", nil, "00FF00")
            syschat("")
            hg_lib.syschat_t("EVENT_GLORY_PRIZE", "Premio Gloria: +{PTS}", {PTS = glory_prize}, "FFD700")
            syschat("")
            hg_lib.syschat_t("EVENT_TOTAL", ">>> TOTALE: +{PTS} Gloria <<<", {PTS = glory_prize}, "00FF00")
            syschat("|cffFFD700=============================================|r")
            hg_lib.hunter_speak_color("CONGRATULAZIONI! HAI VINTO +" .. glory_prize .. " GLORIA!", "GOLD")
        end
        
        return winner_name, glory_prize
    end
    
    return nil, 0
end

function hg_lib.check_event_end_and_draw()
    -- Controlla se un evento e appena finito e fai l'estrazione
    local t = os.date("*t")
    local wday = t.wday - 1
    local day_db = wday
    if wday == 0 then day_db = 7 end
    
    local current_hour = t.hour
    local current_minute = t.min
    local current_total = current_hour * 60 + current_minute
    
    local q = "SELECT id, event_name, start_hour, start_minute, duration_minutes FROM srv1_hunabku.hunter_scheduled_events WHERE enabled=1 AND FIND_IN_SET(" .. day_db .. ", days_active) > 0"
    local c, d = mysql_direct_query(q)
    
    if c > 0 then
        for i = 1, c do
            local e = d[i]
            local event_id = tonumber(e.id)
            local start_hour = tonumber(e.start_hour) or 0
            local start_minute = tonumber(e.start_minute) or 0
            local duration = tonumber(e.duration_minutes) or 30
            
            local start_total = start_hour * 60 + start_minute
            local end_total = start_total + duration
            
            -- Se siamo esattamente al minuto di fine evento (finestra di 1 minuto)
            if current_total >= end_total and current_total < end_total + 1 then
                -- FIX RACE CONDITION: Usa event_flag come lock per evitare multiple esecuzioni
                local lock_flag = "hq_event_draw_lock_" .. event_id
                local is_locked = game.get_event_flag(lock_flag) or 0

                if is_locked == 1 then
                    -- Già in corso di estrazione da un altro player, skip
                    return
                end

                -- Acquisisci il lock (valido 2 minuti)
                game.set_event_flag(lock_flag, 1)

                -- Controlla se non abbiamo gia estratto oggi (DB check)
                local today = os.date("%Y-%m-%d")
                local check_q = string.format(
                    "SELECT id FROM srv1_hunabku.hunter_event_winners WHERE event_id=%d AND DATE(won_at)='%s'",
                    event_id, today
                )
                local wc = mysql_direct_query(check_q)

                if wc == 0 then
                    -- Non ancora estratto, procedi
                    notice_all("|cffFFD700[HUNTER " .. hg_lib.get_text("EVENT", nil, "EVENTO") .. "]|r " .. hg_lib.get_text("EVENT_ENDED", {EVENT = e.event_name}, "L'evento " .. e.event_name .. " e terminato!"))
                    notice_all("|cff00FF00[" .. hg_lib.get_text("LOTTERY", nil, "ESTRAZIONE") .. "]|r " .. hg_lib.get_text("LOTTERY_IN_PROGRESS", nil, "Sorteggio vincitore in corso..."))

                    local winner, prize = hg_lib.draw_event_winner(event_id)
                    if not winner then
                        notice_all("|cffFF6600[" .. hg_lib.get_text("EVENT", nil, "EVENTO") .. "]|r " .. hg_lib.get_text("NO_PARTICIPANTS", nil, "Nessun partecipante oggi. Nessun vincitore."))
                    end
                end

                -- Rilascia il lock dopo 2 minuti (120 secondi)
                timer("hq_release_event_lock_" .. event_id, 120, "game.set_event_flag('" .. lock_flag .. "', 0)")
            end
        end
    end
end

-- LOGICA KILL & SPAWN
function hg_lib.is_elite_mob(vnum)
    if not _G.hunter_elite_cache or not next(_G.hunter_elite_cache) then
        hg_lib.load_elite_cache()
    end

    return _G.hunter_elite_cache[vnum] == true
end

function hg_lib.get_mob_info(vnum)
    if not _G.hunter_elite_data or not next(_G.hunter_elite_data) then
        hg_lib.load_elite_cache()
    end

    return _G.hunter_elite_data[vnum]
end

function hg_lib.show_awakening_sequence(name)
    cmdchat("HunterAwakening " .. hg_lib.clean_str(name))
    timer("hq_awaken_1", 1)
    timer("hq_awaken_2", 3)
    timer("hq_awaken_3", 5)
    timer("hq_awaken_4", 7)
    timer("hq_awaken_5", 9)
end

function hg_lib.show_rank_welcome(name, points)
    local rank_key = hg_lib.get_rank_key(points)
    local rank_data = hg_lib.get_rank_data(rank_key)
    cmdchat("HunterWelcome " .. rank_key .. "|" .. hg_lib.clean_str(name) .. "|" .. points)
    syschat("")
    syschat(rank_data.border)
    syschat(rank_data.title_line)
    syschat(rank_data.border)
    syschat("")
    syschat(rank_data.welcome_line1)
    syschat(rank_data.welcome_line2)
    syschat(rank_data.welcome_line3)
    syschat("")
    syschat(rank_data.stats_line)
    syschat("")
    syschat(rank_data.quote)
    syschat(rank_data.border)
end

-- Versione che usa direttamente il rank_num invece di ricalcolarlo dai punti
function hg_lib.show_rank_welcome_by_rank(name, rank_num, points)
    local rank_letters = {"E", "D", "C", "B", "A", "S", "N"}
    local rank_key = rank_letters[(rank_num or 0) + 1] or "E"
    local rank_data = hg_lib.get_rank_data(rank_key)
    cmdchat("HunterWelcome " .. rank_key .. "|" .. hg_lib.clean_str(name) .. "|" .. (points or 0))
    syschat("")
    syschat(rank_data.border)
    syschat(rank_data.title_line)
    syschat(rank_data.border)
    syschat("")
    syschat(rank_data.welcome_line1)
    syschat(rank_data.welcome_line2)
    syschat(rank_data.welcome_line3)
    syschat("")
    syschat(rank_data.stats_line)
    syschat("")
    syschat(rank_data.quote)
    syschat(rank_data.border)
end

function hg_lib.get_rank_key(points)
    local N = tonumber(hg_lib.get_config("rank_threshold_N")) or 1500000
    local S = tonumber(hg_lib.get_config("rank_threshold_S")) or 500000
    local A = tonumber(hg_lib.get_config("rank_threshold_A")) or 150000
    local B = tonumber(hg_lib.get_config("rank_threshold_B")) or 50000
    local C = tonumber(hg_lib.get_config("rank_threshold_C")) or 10000
    local D = tonumber(hg_lib.get_config("rank_threshold_D")) or 2000

    if points >= N then return "N"
    elseif points >= S then return "S"
    elseif points >= A then return "A"
    elseif points >= B then return "B"
    elseif points >= C then return "C"
    elseif points >= D then return "D"
    else return "E" end
end

function hg_lib.get_rank_data(rank_key)
    -- Fallback completi per ogni rank
    local fallback = {
        ["E"] = {
            border = "|cff808080====================================================|r",
            title_line = "|cff808080              [E-RANK] RISVEGLIATO|r",
            welcome_line1 = "|cffAAAAAA   Bentornato nel Sistema, Cacciatore.|r",
            welcome_line2 = "|cffAAAAAA   La strada e lunga, ma ogni viaggio|r",
            welcome_line3 = "|cffAAAAAA   inizia con un singolo passo.|r",
            stats_line = "|cff808080   >> Status: ATTIVO | Minacce: IN ATTESA <<|r",
            quote = "|cff808080   'Il debole di oggi... il forte di domani.'|r"
        },
        ["D"] = {
            border = "|cff8B4513====================================================|r",
            title_line = "|cff8B4513              [D-RANK] CACCIATORE|r",
            welcome_line1 = "|cffCD853F   Bentornato, Cacciatore di Rango D.|r",
            welcome_line2 = "|cffCD853F   Hai dimostrato di avere potenziale.|r",
            welcome_line3 = "|cffCD853F   Continua a crescere.|r",
            stats_line = "|cff8B4513   >> Status: ATTIVO | Minacce: BASSE <<|r",
            quote = "|cff8B4513   'Ogni caccia ti rende piu forte.'|r"
        },
        ["C"] = {
            border = "|cff00FF00====================================================|r",
            title_line = "|cff00FF00              [C-RANK] VETERANO|r",
            welcome_line1 = "|cff32CD32   Bentornato, Veterano di Rango C.|r",
            welcome_line2 = "|cff32CD32   La tua esperienza parla da sola.|r",
            welcome_line3 = "|cff32CD32   Le fratture ti temono.|r",
            stats_line = "|cff00FF00   >> Status: ATTIVO | Minacce: MODERATE <<|r",
            quote = "|cff00FF00   'La forza nasce dalla perseveranza.'|r"
        },
        ["B"] = {
            border = "|cff00BFFF====================================================|r",
            title_line = "|cff00BFFF              [B-RANK] ELITE|r",
            welcome_line1 = "|cff87CEEB   Bentornato, Elite di Rango B.|r",
            welcome_line2 = "|cff87CEEB   Pochi raggiungono questo livello.|r",
            welcome_line3 = "|cff87CEEB   Il Sistema riconosce il tuo valore.|r",
            stats_line = "|cff00BFFF   >> Status: ATTIVO | Minacce: SIGNIFICATIVE <<|r",
            quote = "|cff00BFFF   'I deboli fuggono, i forti combattono.'|r"
        },
        ["A"] = {
            border = "|cffFFD700====================================================|r",
            title_line = "|cffFFD700              [A-RANK] CAMPIONE|r",
            welcome_line1 = "|cffFFFF00   Bentornato, Campione di Rango A.|r",
            welcome_line2 = "|cffFFFF00   Sei tra i migliori cacciatori.|r",
            welcome_line3 = "|cffFFFF00   Le ombre tremano al tuo passaggio.|r",
            stats_line = "|cffFFD700   >> Status: ATTIVO | Minacce: ELEVATE <<|r",
            quote = "|cffFFD700   'Solo i veri guerrieri arrivano qui.'|r"
        },
        ["S"] = {
            border = "|cffFF4500====================================================|r",
            title_line = "|cffFF4500              [S-RANK] LEGGENDA|r",
            welcome_line1 = "|cffFF6347   Bentornato, Leggenda di Rango S.|r",
            welcome_line2 = "|cffFF6347   Il tuo nome risuona tra i cacciatori.|r",
            welcome_line3 = "|cffFF6347   Nessuna frattura puo fermarti.|r",
            stats_line = "|cffFF4500   >> Status: ATTIVO | Minacce: ESTREME <<|r",
            quote = "|cffFF4500   'Le leggende non muoiono mai.'|r"
        },
        ["N"] = {
            border = "|cffFF00FF====================================================|r",
            title_line = "|cffFF00FF          [N-RANK] MONARCA NAZIONALE|r",
            welcome_line1 = "|cffFF69B4   Bentornato, Monarca Nazionale.|r",
            welcome_line2 = "|cffFF69B4   Sei al vertice assoluto del Sistema.|r",
            welcome_line3 = "|cffFF69B4   Il mondo si inchina davanti a te.|r",
            stats_line = "|cffFF00FF   >> Status: SOVRANO | Minacce: ANNIENTATE <<|r",
            quote = "|cffFF00FF   'Io sono il Sistema.'|r"
        }
    }

    local fb = fallback[rank_key] or fallback["E"]

    return {
        border = fb.border,
        title_line = fb.title_line,
        welcome_line1 = fb.welcome_line1,
        welcome_line2 = fb.welcome_line2,
        welcome_line3 = fb.welcome_line3,
        stats_line = fb.stats_line,
        quote = fb.quote
    }
end

function hg_lib.check_login_streak()
    local today = math.floor(get_time() / 86400)
    local last_login = pc.getqf("hq_last_login_day") or 0
    local streak = pc.getqf("hq_login_streak") or 0
    if today > last_login + 1 then 
        streak = 1 
    elseif today == last_login + 1 then 
        streak = streak + 1 
    end
    pc.setqf("hq_login_streak", streak)
    pc.setqf("hq_last_login_day", today)
        
    local days_tier3 = tonumber(hg_lib.get_config("streak_days_tier3")) or 30
    local bonus_tier3 = tonumber(hg_lib.get_config("streak_bonus_30days")) or 20
    local days_tier2 = tonumber(hg_lib.get_config("streak_days_tier2")) or 7
    local bonus_tier2 = tonumber(hg_lib.get_config("streak_bonus_7days")) or 10
    local days_tier1 = tonumber(hg_lib.get_config("streak_days_tier1")) or 3
    local bonus_tier1 = tonumber(hg_lib.get_config("streak_bonus_3days")) or 5

    local bonus = 0
    if streak >= days_tier3 then
        bonus = bonus_tier3
    elseif streak >= days_tier2 then
        bonus = bonus_tier2
    elseif streak >= days_tier1 then
        bonus = bonus_tier1
    end
    pc.setqf("hq_streak_bonus", bonus)
    if streak > 1 then
        local db_msg = hg_lib.get_streak_message(streak)
        if db_msg then
            hg_lib.hunter_speak(db_msg)
        else
            hg_lib.hunter_speak("STREAK GIORNALIERA: " .. streak .. " GIORNI. BONUS: " .. bonus .. " pct")
        end
    end
end

function hg_lib.check_pending_rewards()
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT pending_daily_reward, pending_weekly_reward FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
    if c > 0 and d[1] then
        if (tonumber(d[1].pending_daily_reward) or 0) > 0 or (tonumber(d[1].pending_weekly_reward) or 0) > 0 then
            local msg = hg_lib.get_text("pending_rewards") or "RICOMPENSE IN ATTESA. CONTROLLA IL TERMINALE."
            hg_lib.hunter_speak(msg)
        end
    end
end

-- ============================================================
-- RESTORE EMERGENCY QUEST ON LOGIN
-- Se il player ha un'emergency quest attiva che non è scaduta,
-- riavvia l'UI con il tempo rimanente
-- ============================================================
function hg_lib.restore_emergency_on_login()
    local emerg_active = pc.getqf("hq_emerg_active") or 0
    if emerg_active ~= 1 then return end

    local expire_time = pc.getqf("hq_emerg_expire") or 0
    local now = get_time()

    if expire_time <= now then
        -- L'emergency è scaduta durante il logout - FALLIMENTO
        hg_lib.end_emergency("FAIL")
        return
    end

    -- Calcola tempo rimanente
    local remaining_seconds = expire_time - now
    local emerg_id = pc.getqf("hq_emerg_id") or 0
    local req = pc.getqf("hq_emerg_req") or 1
    local cur = pc.getqf("hq_emerg_cur") or 0
    local vnums_str = hg_lib.get_emerg_vnums()
    local penalty_pts = pc.getqf("hq_emerg_penalty_pts") or 0

    -- Recupera info dalla missione originale nel DB (se esiste)
    local title = "Emergency Quest"
    local description = "Completa la sfida prima che scada il tempo!"
    local difficulty = "NORMAL"

    -- SICUREZZA: Valida emerg_id come intero prima della query
    emerg_id = tonumber(emerg_id) or 0
    if emerg_id > 0 and emerg_id < 10000 then  -- Limita a range ragionevole
        local ok, err = pcall(function()
            local c, d = mysql_direct_query("SELECT name, description, difficulty FROM srv1_hunabku.hunter_quest_emergencies WHERE id=" .. emerg_id .. " LIMIT 1")
            if c > 0 and d[1] then
                title = d[1].name or title
                description = d[1].description or description
                difficulty = d[1].difficulty or difficulty
            end
        end)
        if not ok then
            -- Log errore ma continua con valori default
            hg_lib.log_info("EMERGENCY", "RESTORE_DB_ERROR", tostring(err))
        end
    end

    -- Riavvia l'UI del client con i dati esistenti
    local desc_clean = hg_lib.clean_str(description)
    local vnums_clean = hg_lib.clean_str(vnums_str)
    local penalty_str = tostring(penalty_pts)

    hg_lib.party_cmdchat("HunterEmergency " .. hg_lib.clean_str(title) .. "|" .. remaining_seconds .. "|" .. vnums_clean .. "|" .. req .. "|" .. desc_clean .. "|" .. difficulty .. "|" .. penalty_str)

    -- Invia anche l'aggiornamento del progresso corrente
    if cur > 0 then
        hg_lib.update_emergency(cur)
    end

    -- Riattiva il timer
    cleartimer("hunter_emerg_tmr")
    loop_timer("hunter_emerg_tmr", 1)

    -- Notifica il player
    local diff_color = {EASY = "GREEN", NORMAL = "BLUE", HARD = "ORANGE", EXTREME = "RED", GOD_MODE = "PURPLE"}
    local msg_color = diff_color[difficulty] or "BLUE"
    local msg = hg_lib.get_text("EMERG_RESTORED", nil, "[SYSTEM] Emergency Quest Ripristinata! Tempo: " .. remaining_seconds .. "s")
    hg_lib.hunter_speak_color(msg, msg_color)
end

-- ============================================================
-- RESEND EMERGENCY UI - Rimostra l'UI se il player ha un'emergency
-- ma la finestra non e' visibile (es. dopo aver provato ad aprire frattura)
-- ============================================================
function hg_lib.resend_emergency_ui()
    local emerg_active = pc.getqf("hq_emerg_active") or 0
    if emerg_active ~= 1 then return end

    local expire_time = pc.getqf("hq_emerg_expire") or 0
    local now = get_time()

    if expire_time <= now then
        -- Scaduta, non mostrare nulla
        return
    end

    -- Calcola tempo rimanente
    local remaining_seconds = expire_time - now
    local req = pc.getqf("hq_emerg_req") or 1
    local cur = pc.getqf("hq_emerg_cur") or 0
    local vnums_str = hg_lib.get_emerg_vnums()
    local penalty_pts = pc.getqf("hq_emerg_penalty_pts") or 0
    local emerg_id = pc.getqf("hq_emerg_id") or 0

    -- Recupera info dal DB se possibile
    local title = "Emergency Quest"
    local description = "Completa la sfida prima che scada il tempo!"
    local difficulty = "NORMAL"

    emerg_id = tonumber(emerg_id) or 0
    if emerg_id > 0 and emerg_id < 10000 then
        local ok, err = pcall(function()
            local c, d = mysql_direct_query("SELECT name, description, difficulty FROM srv1_hunabku.hunter_quest_emergencies WHERE id=" .. emerg_id .. " LIMIT 1")
            if c > 0 and d[1] then
                title = d[1].name or title
                description = d[1].description or description
                difficulty = d[1].difficulty or difficulty
            end
        end)
    end

    -- Invia UI al client
    local desc_clean = hg_lib.clean_str(description)
    local vnums_clean = hg_lib.clean_str(vnums_str)
    local penalty_str = tostring(penalty_pts)

    cmdchat("HunterEmergency " .. hg_lib.clean_str(title) .. "|" .. remaining_seconds .. "|" .. vnums_clean .. "|" .. req .. "|" .. desc_clean .. "|" .. difficulty .. "|" .. penalty_str)

    -- Invia anche il progresso corrente
    if cur > 0 then
        hg_lib.update_emergency(cur)
    end
end

-- ============================================================
-- CHECK GATE SELECTION - Notifica se il player e' stato sorteggiato
-- Chiamato al login per mostrare effetto + aprire finestra Gate
-- ============================================================
function hg_lib.check_gate_selection()
    local pid = pc.get_player_id()

    -- Cerca se il player ha un accesso Gate pendente
    local q = string.format([[
        SELECT ga.access_id, ga.gate_id, gc.gate_name, gc.min_rank, ga.expires_at,
               TIMESTAMPDIFF(MINUTE, NOW(), ga.expires_at) as minutes_left
        FROM srv1_hunabku.hunter_gate_access ga
        JOIN srv1_hunabku.hunter_gate_config gc ON ga.gate_id = gc.gate_id
        WHERE ga.player_id = %d
          AND ga.status = 'pending'
          AND ga.expires_at > NOW()
        ORDER BY ga.granted_at DESC
        LIMIT 1
    ]], pid)

    local c, d = mysql_direct_query(q)

    if c > 0 and d[1] then
        local gate_name = d[1].gate_name or "Gate"
        local rank_req = d[1].min_rank or "E"
        local minutes_left = tonumber(d[1].minutes_left) or 0
        local hours_left = math.floor(minutes_left / 60)
        local mins_left = minutes_left - (hours_left * 60)

        -- Invia comando al client per mostrare effetto e aprire finestra
        -- Formato: HunterGateSelected gateName|rank|hoursLeft|minsLeft
        cmdchat("HunterGateSelected " .. hg_lib.clean_str(gate_name) .. "|" .. rank_req .. "|" .. hours_left .. "|" .. mins_left)

        -- Messaggio syschat tradotto
        syschat("")
        syschat("|cffFFD700========================================|r")
        hg_lib.syschat_t("GATE_SELECTED_TITLE", "[!!!] SEI STATO SELEZIONATO! [!!!]", nil, "FFD700")
        syschat("|cffFFD700========================================|r")
        syschat("")
        hg_lib.syschat_t("GATE_SELECTED_MSG", "Hai accesso al Gate: {GATE}", {GATE = gate_name}, "00FF00")
        hg_lib.syschat_t("GATE_SELECTED_RANK", "Rango richiesto: {RANK}", {RANK = rank_req}, "00FFFF")
        hg_lib.syschat_t("GATE_SELECTED_TIME", "Tempo rimasto: {H}h {M}m", {H = hours_left, M = mins_left}, "FF6600")
        syschat("")
        hg_lib.syschat_t("GATE_SELECTED_HINT", "Apri il Terminale Hunter per entrare!", nil, "AAAAAA")
        syschat("|cffFFD700========================================|r")

        return true
    end

    return false
end

function hg_lib.check_if_overtaken()
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT overtaken_by, overtaken_diff, overtaken_label FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid .. " AND overtaken_by IS NOT NULL AND overtaken_by != ''")
    if c > 0 and d[1] and d[1].overtaken_by and d[1].overtaken_by ~= "" then
        local by_name = d[1].overtaken_by
        local diff = tonumber(d[1].overtaken_diff) or 0
        local label = d[1].overtaken_label or "Gloria"
        cmdchat("HunterRivalAlert " .. hg_lib.clean_str(by_name) .. "|" .. diff .. "|" .. hg_lib.clean_str(label) .. "|SUPERATO")
        mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET overtaken_by=NULL, overtaken_diff=0, overtaken_label=NULL WHERE player_id=" .. pid)
    end
end

function hg_lib.check_rank_up(old_points, new_points)
    local old_rank = hg_lib.get_rank_index(old_points)
    local new_rank = hg_lib.get_rank_index(new_points)
        
    if new_rank > old_rank then
        local new_letter = hg_lib.get_rank_letter(new_rank)
        local pid = pc.get_player_id()
            
        cmdchat("HunterRankUp " .. hg_lib.get_rank_letter(old_rank) .. "|" .. new_letter)
        pc.setqf("hq_rank_num", new_rank)

        hg_lib.flush_ranking_updates()

        mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET hunter_rank='" .. new_letter .. "', current_rank='" .. new_letter .. "' WHERE player_id=" .. pid)
            
        if new_rank >= 4 then
            notice_all("")
            local global_msg = hg_lib.get_text("rank_up_global", {NAME = pc.get_name(), RANK = new_letter}) or ("|cffFFD700[RANK UP]|r |cffFFFFFF" .. pc.get_name() .. "|r e' salito al rango [" .. new_letter .. "-RANK]!")
            notice_all(global_msg)
            notice_all("")
        end
            
        local msg = hg_lib.get_text("rank_up_msg", {RANK = new_letter}) or ("RANK UP! Sei ora un " .. new_letter .. "-RANK Hunter!")
        hg_lib.hunter_speak(msg)
    end
end

-- ============================================================
-- OTTIMIZZAZIONE check_overtake - Riduzione drastica query SQL
-- Con 300 giocatori e 300k kill/min, questa funzione era un bottleneck critico
-- NUOVA VERSIONE: Cooldown 60 secondi + batch queries + cache locale
-- ============================================================
_G.hunter_overtake_cooldown = {}  -- Cache cooldown per player

function hg_lib.check_overtake(pid, pname, col_name, added_val, label_nice)
    -- PERFORMANCE: Cooldown di 60 secondi per tipo di check per evitare spam query
    local now = get_time()
    local cooldown_key = pid .. "_" .. col_name
    local last_check = _G.hunter_overtake_cooldown[cooldown_key] or 0
    
    -- Se abbiamo già controllato negli ultimi 60 secondi, skip
    if now - last_check < 60 then
        return
    end
    _G.hunter_overtake_cooldown[cooldown_key] = now
    
    -- PERFORMANCE: Cache i limiti invece di fare query get_config ogni volta
    if not _G.hunter_rival_ranges then
        _G.hunter_rival_ranges = {
            ["daily_points"]    = hg_lib.get_config("rival_range_daily") or 500,
            ["weekly_points"]   = hg_lib.get_config("rival_range_weekly") or 2000,
            ["total_metins"]    = hg_lib.get_config("rival_range_metins") or 50,
            ["total_chests"]    = hg_lib.get_config("rival_range_chests") or 50,
            ["total_fractures"] = hg_lib.get_config("rival_range_fractures") or 20,
            ["total_points"]    = hg_lib.get_config("rival_range_total") or 50000,
        }
    end
    local limit = _G.hunter_rival_ranges[col_name] or 50000
    
    -- PERFORMANCE: Usa il valore in memoria invece di query al DB
    local my_score = pc.getqf("hq_" .. col_name) or 0
    local new_score = my_score + added_val
    
    -- UNA SOLA query ottimizzata invece di 4 separate
    -- NOTA: UNION ALL richiede parentesi attorno a ogni SELECT con ORDER BY/LIMIT
    local q = string.format([[
        (SELECT 'above' as type, player_name, %s as score FROM srv1_hunabku.hunter_quest_ranking
        WHERE %s > %d ORDER BY %s ASC LIMIT 1)
        UNION ALL
        (SELECT 'below' as type, player_name, %s as score FROM srv1_hunabku.hunter_quest_ranking
        WHERE %s < %d AND %s >= %d AND player_id != %d ORDER BY %s DESC LIMIT 1)
    ]], col_name, col_name, new_score, col_name, col_name, col_name, new_score, col_name, my_score, pid, col_name)
    
    local c, d = mysql_direct_query(q)
    
    if c > 0 then
        for i = 1, c do
            local row = d[i]
            local diff = math.abs(tonumber(row.score) - new_score)
            
            if diff > 0 and diff < limit then
                if row.type == "above" then
                    hg_lib.notify_rival(row.player_name, diff, label_nice)
                elseif row.type == "below" then
                    -- Segna che abbiamo superato qualcuno (senza query UPDATE immediata)
                    -- L'update verrà fatto nel flush periodico
                    if col_name == "daily_points" or col_name == "weekly_points" then
                        cmdchat("HunterOvertake " .. hg_lib.clean_str(row.player_name) .. "|0")
                    end
                end
            end
        end
    end
end

-- Helper: controlla se un vnum è nella stringa di vnum separati da virgola
function hg_lib.is_vnum_in_list(vnum, vnum_str)
    if not vnum_str or vnum_str == "" or vnum_str == "0" then
        return true  -- Se nessun vnum specificato, qualsiasi mob conta
    end
    local vnum_s = tostring(vnum)
    for v in string.gfind(vnum_str, "([^,]+)") do
        v = string.gsub(v, "^%s*(.-)%s*$", "%1")  -- trim spaces
        if v == vnum_s or v == "0" then
            return true
        end
    end
    return false
end

function hg_lib.on_emergency_kill(vnum)
    local emerg_active = pc.getqf("hq_emerg_active") or 0

    -- PERFORMANCE FIX: Usa flag party invece di iterare membri ad ogni kill
    if emerg_active ~= 1 then
        if party.is_party() then
            local leader_pid = party.get_leader_pid()
            local party_has_emergency = game.get_event_flag("hq_party_emergency_" .. leader_pid) or 0

            -- Se il party HA emergency attiva, cerca il membro owner
            if party_has_emergency == 1 then
                local pids = {party.get_member_pids()}
                for i, member_pid in ipairs(pids) do
                    q.begin_other_pc_block(member_pid)
                    local member_active = pc.getqf("hq_emerg_active") or 0
                    local member_vnum = pc.getqf("hq_emerg_vnum") or 0
                    local member_vnums = hg_lib.get_emerg_vnums()
                    q.end_other_pc_block()

                    -- Supporto multi-vnum: controlla se il vnum ucciso è valido
                    local vnum_matches = hg_lib.is_vnum_in_list(vnum, member_vnums)
                    if not vnum_matches and member_vnum ~= 0 then
                        vnum_matches = (member_vnum == vnum)
                    end

                    if member_active == 1 and vnum_matches then
                        -- Un membro del party ha l'emergency attiva! Eredita i flag
                        q.begin_other_pc_block(member_pid)
                        local req = pc.getqf("hq_emerg_req") or 1
                        local expire = pc.getqf("hq_emerg_expire") or 0
                        local reward_pts = pc.getqf("hq_emerg_reward_pts") or 0
                        local penalty_pts = pc.getqf("hq_emerg_penalty_pts") or 0
                        local emerg_id = pc.getqf("hq_emerg_id") or 0
                        q.end_other_pc_block()

                        pc.setqf("hq_emerg_active", 1)
                        pc.setqf("hq_emerg_vnum", member_vnum)
                        hg_lib.set_emerg_vnums(member_vnums)
                        pc.setqf("hq_emerg_req", req)
                        pc.setqf("hq_emerg_cur", 0)
                        pc.setqf("hq_emerg_expire", expire)
                        pc.setqf("hq_emerg_reward_pts", reward_pts)
                        pc.setqf("hq_emerg_penalty_pts", penalty_pts)
                        pc.setqf("hq_emerg_id", emerg_id)
                        emerg_active = 1
                        break
                    end
                end
            end
        end
    end

    if emerg_active == 1 then
        -- Usa la nuova funzione che controlla direttamente i flags
        local vnum_valid = hg_lib.is_vnum_in_emerg_list(vnum)

        if vnum_valid then
            local current = pc.getqf("hq_emerg_cur") + 1
            local required = pc.getqf("hq_emerg_req")
            pc.setqf("hq_emerg_cur", current)
            hg_lib.update_emergency(current)

            if current >= required then
                hg_lib.end_emergency("SUCCESS")
            end
        end
    end
end

function hg_lib.on_defense_mob_kill(killed_vnum)
    local pid = pc.get_player_id()
    
    -- Controlla se questo player ha una difesa attiva
    local defense_active = pc.getqf("hq_defense_active") or 0
    local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0
    
    -- SE NON HA DIFESA LOCALE, CONTROLLA SE IL SUO PARTY HA UNA DIFESA ATTIVA
    if defense_active ~= 1 or fracture_vid == 0 then
        if party.is_party() then
            local leader_pid = party.get_leader_pid()
            local party_vid = game.get_event_flag("hq_party_defense_vid_" .. leader_pid) or 0
            
            if party_vid > 0 then
                -- Il party ha una difesa attiva! Setta i flag locali
                fracture_vid = party_vid
                pc.setqf("hq_defense_active", 1)
                pc.setqf("hq_defense_fracture_vid", fracture_vid)
                defense_active = 1
            end
        end
    end
    
    -- Dopo il check party, verifica ancora
    if defense_active ~= 1 then
        return
    end
    
    if fracture_vid == 0 then
        return
    end
    
    -- Recupera il rank dalla flag globale
    local rank_idx = game.get_event_flag("hq_defense_rank_" .. fracture_vid) or 0
    local rank = hg_lib.get_rank_letter(rank_idx)
    
    -- Assicurati che la cache delle wave sia caricata
    if not _G.hunter_defense_waves_cache or not _G.hunter_defense_waves_cache[rank] then
        hg_lib.load_defense_waves_cache(rank)
    end
    
    -- Verifica se il mob e' valido per la difesa (silenzioso se non valido)
    local is_valid = hg_lib.is_valid_defense_mob(rank, killed_vnum)
    
    if not is_valid then
        return
    end
    
    -- Incrementa il contatore kill GLOBALE (basato sul VID della frattura)
    local current_killed = game.get_event_flag("hq_defense_killed_" .. fracture_vid) or 0
    current_killed = current_killed + 1
    game.set_event_flag("hq_defense_killed_" .. fracture_vid, current_killed)

    -- Aggiorna l'UI DIFESA con il progresso attuale
    local total_req = game.get_event_flag("hq_defense_req_" .. fracture_vid) or 0
    local current_wave = pc.getqf("hq_defense_wave") or 0
    if total_req > 0 then
        -- Invia update UI a TUTTO il party (non solo al killer)
        -- Formato: killed|required|wave
        hg_lib.party_cmdchat("HunterFractureDefenseTimer " .. current_killed .. "|" .. total_req .. "|" .. current_wave)
    end
end

-- NOTA: _internal_defense_kill rimossa (mai chiamata, logica legacy)

function hg_lib.process_elite_kill(vnum)
    local mob_info = hg_lib.get_mob_info(vnum)
    if not mob_info then return end
        
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local base_pts = mob_info.base_points
    
    -- === SEGNALE D'EMERGENZA: Forza Speed Kill su questo mob ===
    local force_speedkill = game.get_event_flag("hq_force_speedkill_"..pid) or 0
    if force_speedkill == 1 and pc.getqf("hq_speedkill_active") ~= 1 then
        -- Attiva speedkill forzato per questo mob
        pc.setqf("hq_speedkill_active", 1)
        pc.setqf("hq_speedkill_vnum", vnum)
        pc.setqf("hq_speedkill_start", get_time())
        pc.setqf("hq_speedkill_duration", 60)  -- 60 secondi per kill veloce
        game.set_event_flag("hq_force_speedkill_"..pid, 0)  -- Consuma il buff
        hg_lib.syschat_t("SPEEDKILL_ACTIVATED", "SPEED KILL ATTIVATO! Uccidi in 60s per x2 Gloria!", nil, "FF0000")
        cmdchat("HunterSpeedKillStart " .. vnum .. "|60|" .. hg_lib.clean_str(mob_info.name))
        cleartimer("hq_speedkill_timer")
        loop_timer("hq_speedkill_timer", 1)
    end
    -- ===========================================================
        
    local speedkill_active = pc.getqf("hq_speedkill_active") or 0
    local speedkill_vnum = pc.getqf("hq_speedkill_vnum") or 0

    if speedkill_active == 1 and speedkill_vnum == vnum then
        local start_time = pc.getqf("hq_speedkill_start") or 0
        local duration = pc.getqf("hq_speedkill_duration") or 300
        local elapsed = get_time() - start_time

        if elapsed <= duration then
            base_pts = base_pts * 2
            local msg = hg_lib.get_text("speedkill_success") or "SPEED KILL! GLORIA x2!"
            hg_lib.hunter_speak_color(msg, "GOLD")
        end
        
        pc.setqf("hq_speedkill_active", 0)
        cleartimer("hq_speedkill_timer")
        hg_lib.party_cmdchat("HunterSpeedKillEnd 1")
    end

    -- IMPORTANTE: Durante la difesa frattura, NON contare kill per Emergency
    -- I due sistemi devono rimanere separati
    if pc.getqf("hq_defense_active") ~= 1 and pc.getqf("hq_emerg_active") == 1 then
        -- Usa la funzione multi-vnum per controllare se questo mob è un target
        if hg_lib.is_vnum_in_emerg_list(vnum) then
            -- Incrementa il contatore kills
            hg_lib.on_emergency_kill(vnum)
        end
    end

    -- === RISONATORE DI GRUPPO (Party Focus +20% Gloria) ===
    -- Applica PRIMA della distribuzione, cosi' tutti ne beneficiano
    if party.is_party() then
        local leader_pid = party.get_leader_pid()
        local party_focus = game.get_event_flag("hq_party_focus_"..leader_pid) or 0
        if party_focus == 1 then
            local focus_bonus = math.floor(base_pts * 0.20)
            base_pts = base_pts + focus_bonus
            game.set_event_flag("hq_party_focus_"..leader_pid, 0)  -- Consuma il buff (una volta per party)
            syschat("|cff00FFFF[" .. hg_lib.get_text("RESONANCE", nil, "RISONANZA") .. "]|r " .. hg_lib.get_text("RESONANCE_BONUS", {BONUS = focus_bonus}, "+20% Gloria di Gruppo! (+" .. focus_bonus .. ")"))
        end
    end
    -- ======================================================
    
    -- ============================================================
    -- DISTRIBUZIONE GLORIA PER MERITOCRAZIA (PARTY)
    -- ============================================================
    if party.is_party() and party.get_near_count() >= 2 then
        -- Siamo in party! Distribuisci Gloria per meritocrazia
        local distribution = hg_lib.distribute_party_glory_elite(base_pts, mob_info)
        
        -- Aggiorna le statistiche solo per il killer (kill count)
        if mob_info.type_name == "SUPER_METIN" then
            pc.setqf("hq_pending_metins", (pc.getqf("hq_pending_metins") or 0) + 1)
            hg_lib.on_metin_kill(vnum)
        elseif mob_info.type_name == "BAULE" then
            pc.setqf("hq_pending_chests", (pc.getqf("hq_pending_chests") or 0) + 1)
            hg_lib.give_chest_reward()
        elseif mob_info.type_name == "BOSS" then
            hg_lib.on_boss_kill(vnum)
        end
        
        local pending = pc.getqf("hq_pending_elite") or 0
        if pending > 0 then pc.setqf("hq_pending_elite", pending - 1) end

        -- DETAILED STATS: Accumula elite kills (pending flush)
        pc.setqf("hq_pending_elite_kills", (pc.getqf("hq_pending_elite_kills") or 0) + 1)

        hg_lib.check_achievements()
        hg_lib.send_player_data()
        return  -- Esce perche' la distribuzione party e' gia' stata fatta
    end
    -- ============================================================
    
    -- MODALITA' SOLO (senza party) - mantiene la logica originale
    local original_base = base_pts  -- Salva il valore base per il log
    local modifier_log = {}  -- Log dei modificatori
    
    local streak_bonus = pc.getqf("hq_streak_bonus") or 0
    if streak_bonus > 0 then
        local streak_add = math.floor(base_pts * streak_bonus / 100)
        base_pts = base_pts + streak_add
        table.insert(modifier_log, {name = "Streak Bonus", value = "+" .. streak_bonus .. "%", add = streak_add})
    end
    
    -- === FOCUS DEL CACCIATORE (+20% Gloria) ===
    local has_focus = game.get_event_flag("hq_hunter_focus_"..pid) or 0
    if has_focus == 1 then
        local focus_bonus = math.floor(base_pts * 0.20)
        base_pts = base_pts + focus_bonus
        game.set_event_flag("hq_hunter_focus_"..pid, 0)  -- Consuma il buff
        table.insert(modifier_log, {name = "Focus Hunter", value = "+20%", add = focus_bonus})
    end
    -- ==========================================
        
    local player_pts = pc.getqf("hq_total_points") or 0
    local rank_bonus = hg_lib.get_rank_bonus(player_pts)
    if rank_bonus > 0 then
        local rank_add = math.floor(base_pts * rank_bonus / 100)
        base_pts = base_pts + rank_add
        table.insert(modifier_log, {name = "Rank Bonus", value = "+" .. rank_bonus .. "%", add = rank_add})
    end
    
    -- FRACTURE BONUS (+50% se missioni complete)
    if hg_lib.has_fracture_bonus() then
        local frac_add = math.floor(base_pts * 0.50)
        base_pts = base_pts + frac_add
        table.insert(modifier_log, {name = "Bonus Missioni", value = "+50%", add = frac_add})
    end
        
    local evt_name, evt_mult, evt_type = hg_lib.get_active_event()
    if evt_type == "points" and evt_mult ~= 1.0 then
        local before_evt = base_pts
        base_pts = math.floor(base_pts * evt_mult)
        local evt_diff = base_pts - before_evt
        table.insert(modifier_log, {name = "Evento " .. (evt_name or ""), value = "x" .. evt_mult, add = evt_diff})
        -- Registra partecipazione all'evento (se non già registrato)
        hg_lib.register_event_participant()
    end

    local trial_mult = hg_lib.get_trial_gloria_multiplier()
    if trial_mult < 1.0 then
        local before_trial = base_pts
        base_pts = math.floor(base_pts * trial_mult)
        local trial_sub = before_trial - base_pts
        table.insert(modifier_log, {name = "Prova Esame", value = "-50%", add = -trial_sub})
    end

    -- MALUS EMERGENCY QUEST ATTIVA (-80% Gloria)
    if pc.getqf("hq_emerg_active") == 1 then
        local before_emerg = base_pts
        base_pts = math.floor(base_pts * 0.20)  -- Solo 20% = -80%
        local emerg_sub = before_emerg - base_pts
        table.insert(modifier_log, {name = "EMERGENCY ATTIVA", value = "-80%", add = -emerg_sub})
    end

    -- SYSCHAT DETTAGLIATO DEI MODIFICATORI
    local glory_label = hg_lib.get_text("GLORY", nil, "Gloria")
    syschat("|cff888888========== " .. hg_lib.get_text("GLORY_DETAIL", nil, "DETTAGLIO GLORIA") .. " =========|r")
    syschat("|cffFFFFFF" .. mob_info.type_name .. ": |r|cffFFD700" .. mob_info.name .. "|r")
    syschat("|cffAAAAAA" .. hg_lib.get_text("BASE_GLORY", nil, "Gloria Base") .. ": |r|cffFFFFFF" .. original_base .. "|r")
    for i = 1, table.getn(modifier_log) do
        local m = modifier_log[i]
        local color = m.add >= 0 and "|cff00FF00" or "|cffFF4444"
        local sign = m.add >= 0 and "+" or ""
        syschat("|cffAAAAAA" .. m.name .. " (" .. m.value .. "): |r" .. color .. sign .. m.add .. "|r")
    end
    syschat("|cffFFD700>>> " .. hg_lib.get_text("TOTAL", nil, "TOTALE") .. ": +" .. base_pts .. " " .. glory_label .. " <<<|r")
    syschat("|cff888888======================================|r")

    hg_lib.check_overtake(pid, pname, "daily_points", base_pts, "GIORNALIERA")
    hg_lib.check_overtake(pid, pname, "weekly_points", base_pts, "SETTIMANALE")

    hg_lib.add_pending_points(base_pts, base_pts, base_pts)
    hg_lib.add_pending_kill()

    pc.setqf("hq_total_kills", (pc.getqf("hq_total_kills") or 0) + 1)
    local new_total_pts = (pc.getqf("hq_total_points") or 0) + base_pts
    pc.setqf("hq_total_points", new_total_pts)

    hg_lib.check_rank_up(player_pts, new_total_pts)

    if mob_info.type_name == "SUPER_METIN" then
        hg_lib.check_overtake(pid, pname, "total_metins", 1, "METIN")
        pc.setqf("hq_pending_metins", (pc.getqf("hq_pending_metins") or 0) + 1)
        hg_lib.on_metin_kill(vnum)
    elseif mob_info.type_name == "BAULE" then
        hg_lib.check_overtake(pid, pname, "total_chests", 1, "BAULI")
        pc.setqf("hq_pending_chests", (pc.getqf("hq_pending_chests") or 0) + 1)
        hg_lib.give_chest_reward()
    elseif mob_info.type_name == "BOSS" then
        hg_lib.on_boss_kill(vnum)
    end
        
    local pending = pc.getqf("hq_pending_elite") or 0
    if pending > 0 then pc.setqf("hq_pending_elite", pending - 1) end

    -- DETAILED STATS: Accumula elite kills (pending flush)
    pc.setqf("hq_pending_elite_kills", (pc.getqf("hq_pending_elite_kills") or 0) + 1)

    local msg = hg_lib.get_text("target_eliminated", {NAME = mob_info.name, POINTS = base_pts}) or ("BERSAGLIO ELIMINATO: " .. mob_info.name .. " | +" .. base_pts .. " GLORIA")
    hg_lib.hunter_speak_color(msg, mob_info.rank_color or "BLUE")

    hg_lib.check_achievements()
    hg_lib.send_player_data()
end

function hg_lib.process_normal_kill()
    -- Se c'è Emergency Quest attiva, controlla se scaduta
    if pc.getqf("hq_emerg_active") == 1 then
        local expire = pc.getqf("hq_emerg_expire") or 0
        if get_time() > expire then
            -- SCADUTA! Chiama end_emergency per applicare penalità
            hg_lib.end_emergency("FAIL")
        end
        -- Durante emergency attiva, applica malus -80% Gloria (non blocca)
        -- Il malus viene applicato in on_elite_kill e on_chest_open
        return
    end
    
    -- NON contare kill durante Difesa Frattura (i mob della difesa non fanno spawnare fratture)
    -- Check per player SOLO
    if pc.getqf("hq_defense_active") == 1 then
        return
    end
    -- Check per player in PARTY (il membro non ha hq_defense_active ma il party ha il flag)
    if party.is_party() then
        local defense_active = party.getf("hunter_level_bridge", "defense_active") or 0
        if defense_active == 1 then
            return
        end
    end

    local base_threshold = hg_lib.get_config("spawn_threshold_normal")
    if base_threshold <= 0 then base_threshold = 500 end 

    local daily_f = pc.getqf("hq_daily_fracture_count") or 0
    
    local last_day = pc.getqf("hq_last_fracture_day") or 0
    local today = tonumber(os.date("%j"))
    if last_day ~= today then
        daily_f = 0
        pc.setqf("hq_daily_fracture_count", 0)
        pc.setqf("hq_last_fracture_day", today)
    end

    local penalty = 0
    if daily_f >= 5 and daily_f < 15 then
        penalty = (daily_f - 5) * 150
    elseif daily_f >= 15 then
        penalty = (10 * 150) + ((daily_f - 15) * 500)
    end

    local final_threshold = base_threshold + penalty

    local evt_name, evt_mult, evt_type = hg_lib.get_active_event()
    if evt_type == "threshold" then 
        final_threshold = math.floor(final_threshold * evt_mult)
    elseif evt_type == "chance" then
        final_threshold = math.floor(final_threshold * 0.7)
    end
        
    local streak = pc.getqf("hq_login_streak") or 0
    final_threshold = math.max(50, final_threshold - (streak * 5))
        
    local kills = (pc.getqf("hq_normal_kills") or 0) + 1
    pc.setqf("hq_normal_kills", kills)
        
    if kills >= final_threshold then 
        pc.setqf("hq_normal_kills", 0)
        
        pc.setqf("hq_daily_fracture_count", daily_f + 1)
            
        local emerg_chance = hg_lib.get_config("emergency_chance_percent")
        if emerg_chance <= 0 then emerg_chance = 35 end 
            
        local roll = number(1, 100)
            
        if roll <= emerg_chance then
            hg_lib.trigger_random_emergency()
        else
            hg_lib.spawn_fracture() 
        end
    end
end

function hg_lib.trigger_random_emergency()
    if pc.getqf("hq_defense_active") == 1 then return end
    if pc.getqf("hq_emerg_active") == 1 then return end
    if pc.getqf("hq_speedkill_active") == 1 then return end

    local lv = pc.get_level()
    local player_rank = hg_lib.get_rank_from_level(lv)
    local rank_range = hg_lib.get_level_range_for_rank(player_rank)

    -- Filtra emergency quest in base al rank del player (evita missioni troppo difficili/facili)
    -- La missione deve avere min_level e max_level che si sovrappongono al range del rank del player
    local q = string.format([[
        SELECT id, name, description, duration_seconds, target_count, target_vnum,
               reward_points, reward_item_vnum, reward_item_count, difficulty
        FROM srv1_hunabku.hunter_quest_emergencies
        WHERE enabled = 1
          AND min_level <= %d
          AND max_level >= %d
          AND ((min_level >= %d AND min_level <= %d) OR (max_level >= %d AND max_level <= %d)
               OR (min_level <= %d AND max_level >= %d))
        ORDER BY RAND() LIMIT 1
    ]], lv, lv, rank_range.min, rank_range.max, rank_range.min, rank_range.max,
        rank_range.min, rank_range.max)

    local c, d = mysql_direct_query(q)

    if c > 0 and d[1] then
        local mission = d[1]
        local reward_pts = tonumber(mission.reward_points) or 0
        -- Penalità = 50% della ricompensa (configurabile)
        local penalty_pts = math.floor(reward_pts * 0.5)
        local emerg_id = tonumber(mission.id) or 0
        local reward_vnum = tonumber(mission.reward_item_vnum) or 0
        local reward_count = tonumber(mission.reward_item_count) or 0

        -- Setta i flag reward su TUTTI i membri del party (o solo player se solo)
        -- Questo garantisce che anche se il triggerante si slogga, gli altri avranno i flag
        if party.is_party() then
            local pids = {party.get_member_pids()}
            for i, member_pid in ipairs(pids) do
                q.begin_other_pc_block(member_pid)
                pc.setqf("hq_emerg_id", emerg_id)
                pc.setqf("hq_emerg_reward_pts", reward_pts)
                pc.setqf("hq_emerg_penalty_pts", penalty_pts)
                pc.setqf("hq_emerg_reward_vnum", reward_vnum)
                pc.setqf("hq_emerg_reward_count", reward_count)
                q.end_other_pc_block()
            end
        else
            pc.setqf("hq_emerg_id", emerg_id)
            pc.setqf("hq_emerg_reward_pts", reward_pts)
            pc.setqf("hq_emerg_penalty_pts", penalty_pts)
            pc.setqf("hq_emerg_reward_vnum", reward_vnum)
            pc.setqf("hq_emerg_reward_count", reward_count)
        end

        -- Passa tutti i parametri incluso descrizione, difficoltà e penalità
        hg_lib.start_emergency(
            mission.name,
            tonumber(mission.duration_seconds),
            tonumber(mission.target_vnum),
            tonumber(mission.target_count),
            mission.description or "Completa la sfida prima che scada il tempo!",
            mission.difficulty or "NORMAL",
            penalty_pts,
            tostring(mission.target_vnum)  -- vnums singolo per ora
        )

        local diff_color = {EASY = "|cff00FF00", NORMAL = "|cff00CCFF", HARD = "|cffFF8800", EXTREME = "|cffFF0000", GOD_MODE = "|cffFF00FF"}
        local dc = diff_color[mission.difficulty] or "|cffFFFFFF"
        syschat(dc .. "[" .. mission.difficulty .. "]|r Missione: " .. mission.name)
    else
        -- Fallback: emergency generica
        local fallback_penalty = 25
        if party.is_party() then
            local pids = {party.get_member_pids()}
            for i, member_pid in ipairs(pids) do
                q.begin_other_pc_block(member_pid)
                pc.setqf("hq_emerg_id", 0)
                pc.setqf("hq_emerg_reward_pts", 0)
                pc.setqf("hq_emerg_penalty_pts", fallback_penalty)
                pc.setqf("hq_emerg_reward_vnum", 0)
                pc.setqf("hq_emerg_reward_count", 0)
                q.end_other_pc_block()
            end
        else
            pc.setqf("hq_emerg_id", 0)
            pc.setqf("hq_emerg_reward_pts", 0)
            pc.setqf("hq_emerg_penalty_pts", fallback_penalty)
            pc.setqf("hq_emerg_reward_vnum", 0)
            pc.setqf("hq_emerg_reward_count", 0)
        end
        hg_lib.start_emergency("Orda Improvvisa", 60, 0, 20, "Elimina i nemici prima che il tempo scada!", "EASY", fallback_penalty, "0")
    end
end

-- ============================================================
-- SISTEMA BAULI CLICCABILI
-- Quando un player clicca un baule spawnnato, riceve Gloria + Item
-- Se in party, la Gloria viene divisa per meritocrazia
-- ============================================================

function hg_lib.open_chest(chest_vnum)
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    
    -- Recupera dati baule dal DB
    local c, d = mysql_direct_query("SELECT name, rank_tier, glory_min, glory_max, item_vnum, item_quantity, item_chance, color_code FROM srv1_hunabku.hunter_chest_rewards WHERE vnum=" .. chest_vnum .. " AND enabled=1")
    
    if c == 0 or not d[1] then
        -- Fallback: usa vecchio sistema se il baule non e' configurato
        hg_lib.give_chest_reward()
        return
    end
    
    local chest = d[1]
    local chest_name = chest.name or "Baule"
    local rank_tier = tonumber(chest.rank_tier) or 1
    local glory_min = tonumber(chest.glory_min) or 20
    local glory_max = tonumber(chest.glory_max) or 50
    local item_vnum = tonumber(chest.item_vnum) or 0
    local item_qty = tonumber(chest.item_quantity) or 1
    local item_chance = tonumber(chest.item_chance) or 0
    local color_code = chest.color_code or "GREEN"
    
    -- Calcola Gloria base (random tra min e max)
    local base_glory = math.random(glory_min, glory_max)
    
    -- === CHIAVE DIMENSIONALE: Bonus se attivo ===
    local has_key = false
    local force_bonus = game.get_event_flag("hq_force_chest_"..pid) or 0
    if force_bonus == 1 then
        base_glory = math.floor(base_glory * 1.5)  -- +50% Gloria
        item_chance = item_chance + 30  -- +30% chance item
        game.set_event_flag("hq_force_chest_"..pid, 0)  -- Consuma
        has_key = true
    end
    -- ============================================
    
    -- ============================================================
    -- ITEM BASE (item garantito dalla tabella hunter_chest_rewards)
    -- ============================================================
    local got_item = false
    local item_name_str = ""
    if item_vnum > 0 and item_chance > 0 then
        local roll = math.random(1, 100)
        if roll <= item_chance then
            pc.give_item2(item_vnum, item_qty)
            got_item = true
            item_name_str = hg_lib.item_name(item_vnum) or "Oggetto Raro"
            if item_qty > 1 then
                item_name_str = item_name_str .. " x" .. item_qty
            end
        end
    end
    
    -- ============================================================
    -- SISTEMA JACKPOT (hunter_chest_loot)
    -- Possibilita' di ottenere Gloria extra o Item rari
    -- ============================================================
    local jackpot_glory = 0
    local jackpot_items = ""
    local jackpot_items_list = {}
    
    -- Query per possibili jackpot (filtrati per rank_tier del baule)
    local jq = "SELECT id, loot_type, item_vnum, item_quantity, glory_min, glory_max, drop_chance, name, is_jackpot "
    jq = jq .. "FROM srv1_hunabku.hunter_chest_loot "
    jq = jq .. "WHERE enabled=1 AND min_rank_tier <= " .. rank_tier .. " "
    jq = jq .. "AND (chest_vnum = 0 OR chest_vnum = " .. chest_vnum .. ") "
    jq = jq .. "ORDER BY drop_chance ASC"  -- Prima i piu' rari
    
    local jc, jd = mysql_direct_query(jq)
    
    if jc > 0 and jd then
        for i = 1, jc do
            local loot = jd[i]
            local drop_roll = math.random(1, 100)
            local drop_chance = tonumber(loot.drop_chance) or 0
            
            -- Chiave dimensionale aumenta chance jackpot
            if has_key then
                drop_chance = drop_chance + 15
            end
            
            if drop_roll <= drop_chance then
                local loot_type = loot.loot_type
                local is_jackpot = tonumber(loot.is_jackpot) or 0
                
                if loot_type == "GLORY" then
                    -- JACKPOT GLORIA
                    local g_min = tonumber(loot.glory_min) or 100
                    local g_max = tonumber(loot.glory_max) or 500
                    local bonus_glory = math.random(g_min, g_max)
                    jackpot_glory = jackpot_glory + bonus_glory
                    
                    -- Assegna subito la gloria bonus
                    hg_lib.award_glory_to_player(pid, bonus_glory)
                    
                elseif loot_type == "ITEM" then
                    -- JACKPOT ITEM
                    local j_vnum = tonumber(loot.item_vnum) or 0
                    local j_qty = tonumber(loot.item_quantity) or 1
                    local j_name = loot.name or "Item Raro"
                    
                    if j_vnum > 0 then
                        pc.give_item2(j_vnum, j_qty)
                        table.insert(jackpot_items_list, j_name)
                    end
                end
            end
        end
    end
    
    -- Prepara stringa item jackpot per client
    if table.getn(jackpot_items_list) > 0 then
        jackpot_items = table.concat(jackpot_items_list, ", ")
    end
    
    -- ============================================================
    -- DISTRIBUZIONE GLORIA
    -- In party: solo chi apre riceve (semplificato per compatibilita')
    -- ============================================================
    local final_glory = hg_lib.apply_solo_chest_modifiers(pid, base_glory)
    
    -- Assegna Gloria base a chi ha aperto
    hg_lib.award_glory_to_player(pid, final_glory)
    
    -- Security Log: Chest opened
    hg_lib.log_chest_open(chest_name, final_glory, got_item and item_name_str or "none")
    
    -- Statistiche
    pc.setqf("hq_pending_chests", (pc.getqf("hq_pending_chests") or 0) + 1)

    -- DETAILED STATS: Accumula baule per grado (pending flush)
    local grade_keys = {[1]="hq_pending_chest_e", [2]="hq_pending_chest_d", [3]="hq_pending_chest_c",
                        [4]="hq_pending_chest_b", [5]="hq_pending_chest_a", [6]="hq_pending_chest_s", [7]="hq_pending_chest_n"}
    local grade_key = grade_keys[rank_tier]
    if grade_key then
        pc.setqf(grade_key, (pc.getqf(grade_key) or 0) + 1)
    end

    -- PERFORMANCE: Accumula Trial progress invece di query immediata
    hg_lib.add_trial_progress("chest_open", 1)

    -- Aggiorna missioni giornaliere per apertura bauli
    hg_lib.update_mission_progress("open_chest", 1, chest_vnum)

    -- EFFETTO EPICO CLIENT 
    -- Formato: vnum|glory|name|color|itemName|jackpotGlory|jackpotItems
    local effect_data = chest_vnum .. "|" .. final_glory .. "|" .. hg_lib.clean_str(chest_name) .. "|" .. color_code
    effect_data = effect_data .. "|" .. (got_item and hg_lib.clean_str(item_name_str) or "")
    effect_data = effect_data .. "|" .. jackpot_glory
    effect_data = effect_data .. "|" .. (jackpot_items ~= "" and hg_lib.clean_str(jackpot_items) or "")
    
    -- Invia effetto a TUTTI i membri del party
    hg_lib.party_cmdchat("HunterChestOpened " .. effect_data)
    
    -- Messaggio chiave dimensionale (solo se usata)
    if has_key then
        hg_lib.syschat_t("DIMKEY_TREASURE", "Tesoro nascosto rivelato!", nil, "FFD700")
    end

    -- Notifica party (semplice)
    if party.is_party() then
        syschat("|cff00A8FF[" .. hg_lib.get_text("SYSTEM", nil, "SISTEMA") .. "]|r " .. hg_lib.get_text("CHEST_OPENED", {NAME = chest_name, PTS = final_glory}, "Hai aperto " .. chest_name .. " - +" .. final_glory .. " Gloria"))
        if jackpot_glory > 0 then
            syschat("|cffFF00FF*** JACKPOT! +|r|cffFFD700" .. jackpot_glory .. " " .. hg_lib.get_text("GLORY_EXTRA", nil, "Gloria Extra") .. "!|r")
        end
        if jackpot_items ~= "" then
            syschat("|cffFF00FF*** BONUS! |r|cff00FF00" .. jackpot_items .. "|r")
        end
    end
    
    -- Verifica completamento trial
    hg_lib.check_trial_completion_status()
    
    -- Aggiorna dati client
    hg_lib.send_player_data()
end

-- Applica modificatori solo player per bauli
-- OTTIMIZZATO: Usa calculate_glory_with_modifiers centralizzata
function hg_lib.apply_solo_chest_modifiers(player_id, base_glory)
    -- USA FUNZIONE CENTRALIZZATA per calcolo modificatori
    local final_glory, modifier_log = hg_lib.calculate_glory_with_modifiers(base_glory, {player_id = player_id})

    -- Mostra syschat dettagliato
    hg_lib.show_glory_details("BAULE", "Tesoro", base_glory, final_glory, modifier_log)

    return final_glory
end

-- Distribuisce Gloria baule al party per meritocrazia
-- NOTA: Semplificata - gloria va solo a chi apre (party.for_each_member non disponibile)
function hg_lib.distribute_chest_glory(base_glory, chest_name, color_code, got_item, item_name_str, opener_jackpot_glory, opener_jackpot_items)
    local opener_pid = pc.get_player_id()
    color_code = color_code or "GOLD"
    opener_jackpot_glory = opener_jackpot_glory or 0
    opener_jackpot_items = opener_jackpot_items or ""
    
    -- Solo chi apre riceve la gloria
    local grade = hg_lib.get_player_rank_grade(opener_pid)
    local final_glory = hg_lib.apply_solo_chest_modifiers(opener_pid, base_glory)
    
    -- Assegna
    hg_lib.award_glory_to_player(opener_pid, final_glory)
    
    local distribution_log = {{
        pid = opener_pid,
        name = pc.get_name(),
        grade = grade,
        power = hg_lib.POWER_RANK_VALUES[grade] or 1,
        share = 100,
        final = final_glory
    }}
    
    -- Effetto client
    local effect_data = "0|" .. final_glory .. "|" .. hg_lib.clean_str(chest_name) .. "|" .. color_code
    effect_data = effect_data .. "|" .. (got_item and hg_lib.clean_str(item_name_str) or "")
    effect_data = effect_data .. "|" .. opener_jackpot_glory
    effect_data = effect_data .. "|" .. (opener_jackpot_items ~= "" and hg_lib.clean_str(opener_jackpot_items) or "")
    cmdchat("HunterChestOpened " .. effect_data)
    
    -- Notifica
    syschat("|cff00A8FF[" .. hg_lib.get_text("SYSTEM", nil, "SISTEMA") .. "]|r " .. chest_name .. " - |cffFFD700+" .. final_glory .. " " .. hg_lib.get_text("GLORY", nil, "Gloria") .. "|r")
    if opener_jackpot_glory > 0 then
        syschat("|cffFF00FF*** JACKPOT! +|r|cffFFD700" .. opener_jackpot_glory .. " " .. hg_lib.get_text("GLORY_EXTRA", nil, "Gloria Extra") .. "!|r")
    end
    if opener_jackpot_items ~= "" then
        syschat("|cffFF00FF*** BONUS! |r|cff00FF00" .. opener_jackpot_items .. "|r")
    end

    return distribution_log
end
-- ============================================================
-- FINE SISTEMA BAULI
-- ============================================================

function hg_lib.give_chest_reward()
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT item_vnum, item_quantity, bonus_points FROM srv1_hunabku.hunter_quest_jackpot_rewards WHERE type_name='BAULE' ORDER BY RAND() LIMIT 1")

    if c > 0 and d[1] then
        local v, q, b = tonumber(d[1].item_vnum), tonumber(d[1].item_quantity), tonumber(d[1].bonus_points) or 0
        pc.give_item2(v, q)

        local msg = hg_lib.get_text("CHEST_OPENED_ITEM", {ITEM = hg_lib.item_name(v)}, "BAULE APERTO: OTTENUTO " .. hg_lib.item_name(v))
        hg_lib.hunter_speak(msg)

        -- === CHIAVE DIMENSIONALE: Forza bonus se flag attivo ===
        local force_bonus = game.get_event_flag("hq_force_chest_"..pid) or 0
        if force_bonus == 1 then
            if b == 0 or b == nil then
                b = math.random(500, 2000)  -- Garantisce bonus se non c'era
            else
                b = math.floor(b * 1.5)  -- Aumenta bonus esistente del 50%
            end
            game.set_event_flag("hq_force_chest_"..pid, 0)  -- Consuma il buff
            hg_lib.syschat_t("DIMKEY_TREASURE", "Tesoro nascosto rivelato!", nil, "FFD700")
        end
        -- === FINE CHIAVE DIMENSIONALE ===
        
        if b > 0 then
            mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points=total_points+"..b..", spendable_points=spendable_points+"..b.." WHERE player_id="..pid)
            local bonus_msg = hg_lib.get_text("chest_bonus", {POINTS = b}) or ("Incredibile! Il baule conteneva anche " .. b .. " Gloria!")
            syschat("|cffFFD700[BONUS]|r " .. bonus_msg)
        end

        -- PERFORMANCE: Accumula Trial progress invece di query immediata
        hg_lib.add_trial_progress("chest_open", 1)

        -- Aggiorna missioni giornaliere per apertura bauli (reward auto-open)
        hg_lib.update_mission_progress("open_chest", 1, 0)
        -- ==========================
    end
end

-- ============================================================
-- CACHE ACHIEVEMENTS - Carica una volta, check locale
-- ============================================================
_G.hunter_achievements_cache = nil
_G.hunter_achievements_cache_time = 0

function hg_lib.check_achievements()
    local k, p = pc.getqf("hq_total_kills") or 0, pc.getqf("hq_total_points") or 0
    
    -- PERFORMANCE: Cache achievements config per 10 minuti
    local now = get_time()
    if not _G.hunter_achievements_cache or (now - _G.hunter_achievements_cache_time) > 600 then
        local c, d = mysql_direct_query("SELECT id, type, requirement FROM srv1_hunabku.hunter_quest_achievements_config WHERE enabled=1")
        if c > 0 then
            _G.hunter_achievements_cache = d
            _G.hunter_achievements_cache_time = now
        else
            return
        end
    end
    
    local u = 0
    local d = _G.hunter_achievements_cache
    if d then
        for i=1,table.getn(d) do
            local aid, at, req = tonumber(d[i].id), tonumber(d[i].type), tonumber(d[i].requirement)
            local prg = p
            if at == 1 then prg = k end
            if prg >= req and pc.getqf("hq_ach_clm_" .. aid) ~= 1 then 
                u = u + 1 
            end
        end
    end
    if u > 0 then 
        local msg = hg_lib.get_text("achievements_unlocked", {COUNT = u}) or ("TRAGUARDI SBLOCCATI: " .. u)
        hg_lib.hunter_speak(msg)
    end
end

-- ============================================================
-- CACHE FRACTURES - Carica lista fratture una volta
-- ============================================================
_G.hunter_fractures_cache = nil
_G.hunter_fractures_cache_time = 0

function hg_lib.get_fractures_cached()
    local now = get_time()
    if not _G.hunter_fractures_cache or (now - _G.hunter_fractures_cache_time) > 300 then
        local c, d = mysql_direct_query("SELECT vnum, name, rank_label, spawn_chance, req_points, color_code FROM srv1_hunabku.hunter_quest_fractures WHERE enabled=1 ORDER BY spawn_chance DESC")
        if c > 0 then
            _G.hunter_fractures_cache = {count = c, data = d}
            _G.hunter_fractures_cache_time = now
        end
    end
    return _G.hunter_fractures_cache
end

function hg_lib.spawn_fracture()
    local pid = pc.get_player_id()
    local map_index = pc.get_map_index()
    local is_in_dungeon = hg_lib.is_dungeon_map(map_index)
    
    -- === CALIBRATORE: Controlla se c'e' un rank minimo forzato ===
    local calibrator_active = game.get_event_flag("hq_fracture_rank_"..pid) or 0
    local use_calibrator = false
    if calibrator_active == 1 then
        use_calibrator = true
        game.set_event_flag("hq_fracture_rank_"..pid, 0)  -- Consuma il buff
        syschat("|cffFF6600[" .. hg_lib.get_text("CALIBRATOR", nil, "CALIBRATORE") .. "]|r " .. hg_lib.get_text("CALIBRATOR_ACTIVE_MSG", nil, "Filtro attivo: Rango C+ garantito!"))
    end
    -- ==============================================================
    
    -- PERFORMANCE: Usa cache invece di query diretta
    local cached = hg_lib.get_fractures_cached()
    if not cached then return end
    local c, d = cached.count, cached.data
    if c == 0 then return end
        
    local roll = number(1, 100)
    local evt_name = hg_lib.get_active_event()
    if evt_name == "RED+MOON" then 
        roll = number(50, 100) 
    end
    local sel_vnum, sel_rank, sel_color, cumul = 16060, "E-Rank", "GREEN", 0
    local found = false
    
    for i = 1, c do 
        local rank_label = d[i].rank_label or ""
        local skip_this = false
        
        -- Se calibratore attivo, salta fratture sotto rank C
        if use_calibrator then
            if not (string.find(rank_label, "C") or string.find(rank_label, "B") or string.find(rank_label, "A") or string.find(rank_label, "S")) then
                skip_this = true
            end
        end
        
        -- DUNGEON RESTRICTION: In dungeon, max rank C (skip B, A, S, N)
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
        
    local x, y = pc.get_local_x(), pc.get_local_y()
    mob.spawn(sel_vnum, x + 3, y + 3, 1)
    local msg = hg_lib.get_text("fracture_detected", {RANK = sel_rank}) or ("ATTENZIONE: FRATTURA " .. sel_rank .. " RILEVATA.")
    hg_lib.hunter_speak_color(msg, sel_color)
end

function hg_lib.open_gate(fname, frank, fcolor, pid)
    if pc.getqf("hq_defense_active") == 1 then
        syschat("|cffFF0000[" .. hg_lib.get_text("CONFLICT", nil, "CONFLITTO") .. "]|r " .. hg_lib.get_text("CONFLICT_DEFENSE", nil, "Stai gia' difendendo un'altra frattura!"))
        return
    end

    -- Prova npc.get_vid(), se fallisce usa il VID salvato dal click
    local fracture_vid = npc.get_vid()
    if fracture_vid == nil or fracture_vid == 0 then
        fracture_vid = pc.getqf("hq_temp_gate_vid") or 0
    end

    if fracture_vid == 0 then
        syschat("|cffFF0000[" .. hg_lib.get_text("ERROR", nil, "ERRORE") .. "]|r " .. hg_lib.get_text("ERROR_IDENTIFY_FRACTURE", nil, "Impossibile identificare la frattura!"))
        return
    end

    -- === SIGILLO DI CONQUISTA: Salta la difesa e apre direttamente ===
    local force_conquest = game.get_event_flag("hq_force_conquest_"..pid) or 0
    if force_conquest == 1 then
        game.set_event_flag("hq_force_conquest_"..pid, 0)  -- Consuma il buff
        syschat("|cffFFD700[" .. hg_lib.get_text("SEAL_OF_CONQUEST", nil, "SIGILLO DI CONQUISTA") .. "]|r " .. hg_lib.get_text("SEAL_INSTANT_OPEN", nil, "La frattura si apre istantaneamente!"))
        
        -- Salva i dati per finalize
        if not hunter_defense_data then hunter_defense_data = {} end
        hunter_defense_data[pid] = { rank = frank, fname = fname, color = fcolor }
        
        -- Completa direttamente senza difesa
        hg_lib.finalize_gate_opening(fracture_vid)
        return
    end
    -- === FINE SIGILLO DI CONQUISTA ===
    
    game.set_event_flag("hq_gate_lock_"..fracture_vid, pid)
    game.set_event_flag("hq_gate_time_"..fracture_vid, get_time() + 90)

    hg_lib.load_defense_waves_cache(frank)

    local fx, fy = pc.get_local_x(), pc.get_local_y()
    
    -- Security Log: Defense started
    hg_lib.log_defense_start(fracture_vid, frank)

    pc.setqf("hq_defense_x", fx)
    pc.setqf("hq_defense_y", fy)
    pc.setqf("hq_defense_active", 1)
    pc.setqf("hq_defense_start", get_time())
    pc.setqf("hq_defense_wave", 0)
    pc.setqf("hq_defense_last_check", get_time())
    pc.setqf("hq_defense_fracture_vid", fracture_vid)

    if not hunter_defense_data then hunter_defense_data = {} end
    hunter_defense_data[pid] = { rank = frank, fname = fname, color = fcolor }

    -- Calcola il totale mob richiesti per questo rank
    local total_mobs_req = hg_lib.get_defense_total_mobs(frank)
    
    -- Se total_mobs_req = 0, ricarica la cache
    if total_mobs_req == 0 then
        hg_lib.load_defense_waves_cache(frank)
        total_mobs_req = hg_lib.get_defense_total_mobs(frank)
    end
    
    -- NOTA: total_mobs_req iniziale = 0, poi viene incrementato da ogni wave
    -- Settiamo a 0 e lasciamo che le wave aggiornino il totale
    pc.setqf("hq_defense_mob_req", 0)   
    pc.setqf("hq_defense_mob_killed", 0) 

    -- Durata difesa in base al rank (E/D/C = 60s, B+ aumenta)
    local duration = hg_lib.get_defense_duration_by_rank(frank)
    pc.setqf("hq_defense_duration", duration)

    -- SEMPRE: Setta flag globali basate sul VID (funziona sia SOLO che PARTY)
    local rank_idx = hg_lib.get_rank_index_by_letter(frank)
    game.set_event_flag("hq_defense_rank_" .. fracture_vid, rank_idx)
    game.set_event_flag("hq_defense_killed_" .. fracture_vid, 0)
    game.set_event_flag("hq_defense_req_" .. fracture_vid, total_mobs_req)  -- Setta subito il totale richiesto
    
    -- PARTY: Attiva difesa su TUTTI i membri con TUTTI i flag necessari
    if party.is_party() then
        -- USA LEADER_PID per la flag party (cosi' tutti i membri possono trovarla!)
        local leader_pid = party.get_leader_pid()
        game.set_event_flag("hq_party_defense_vid_" .. leader_pid, fracture_vid)
        
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            -- Setta su TUTTI i membri (incluso chi ha cliccato per ultimo)
            q.begin_other_pc_block(member_pid)
            
            -- Flag difesa attiva
            pc.setqf("hq_defense_active", 1)
            pc.setqf("hq_defense_start", get_time())
            pc.setqf("hq_defense_fracture_vid", fracture_vid)
            
            -- Flag posizione (centro difesa)
            pc.setqf("hq_defense_x", fx)
            pc.setqf("hq_defense_y", fy)
            
            -- Flag wave e kill (ogni membro tiene traccia locale)
            pc.setqf("hq_defense_wave", 0)
            pc.setqf("hq_defense_last_check", get_time())
            pc.setqf("hq_defense_mob_req", 0)
            pc.setqf("hq_defense_mob_killed", 0)
            pc.setqf("hq_defense_duration", duration)
            
            q.end_other_pc_block()
        end
        
        -- Salva anche i dati defense per tutti
        if not hunter_defense_data then hunter_defense_data = {} end
        for i, member_pid in ipairs(pids) do
            hunter_defense_data[member_pid] = { rank = frank, fname = fname, color = fcolor }
        end
    end

    local defense_title = "DIFESA " .. fname

    -- Mapping rank -> difficulty per colori UI
    local rank_to_difficulty = {
        E = "EASY", D = "NORMAL", C = "NORMAL",
        B = "HARD", A = "EXTREME", S = "GOD_MODE", N = "GOD_MODE"
    }
    local difficulty = rank_to_difficulty[frank] or "NORMAL"
    local description = "Uccidi " .. total_mobs_req .. " mob per aprire la frattura!"

    -- Invia UI DIFESA FRATTURA dedicata (separata dall'Emergency Quest)
    -- Formato: fracture_name|duration|rank|totalMobs
    hg_lib.party_cmdchat("HunterFractureDefenseStart " .. hg_lib.clean_str(defense_title) .. "|" .. duration .. "|" .. frank .. "|" .. total_mobs_req)

    local msg = hg_lib.get_text("defense_start", {SECONDS = duration}, "UCCIDI TUTTI I MOB! Hai " .. duration .. " secondi!")
    hg_lib.party_hunter_speak_color(msg, fcolor)

    -- Notifica party
    if party.is_party() then
        local party_msg = hg_lib.get_text("DEFENSE_PARTY_START", {MOBS = total_mobs_req, SECONDS = duration}, "[HUNTER] DIFESA INIZIATA! Uccidete " .. total_mobs_req .. " mob in " .. duration .. " secondi!")
        party.syschat(party_msg)
    end

    cleartimer("hq_defense_timer")
    loop_timer("hq_defense_timer", 1)
end

-- Invia cmdchat a tutti i membri del party (o solo al player se solo)
function hg_lib.party_cmdchat(cmd)
    -- SEMPRE invia al player corrente prima (altrimenti potrebbe non riceverlo)
    cmdchat(cmd)

    if party.is_party() then
        -- Poi invia agli altri membri del party
        local my_pid = pc.get_player_id()
        local pids = {party.get_member_pids()}
        for i, pid in ipairs(pids) do
            if pid ~= my_pid then
                q.begin_other_pc_block(pid)
                cmdchat(cmd)
                q.end_other_pc_block()
            end
        end
    end
end

-- Invia hunter_speak_color a tutti i membri del party (o solo al player se solo)
function hg_lib.party_hunter_speak_color(msg, color)
    if party.is_party() then
        -- Invia a tutti i membri del party
        local pids = {party.get_member_pids()}
        for i, pid in ipairs(pids) do
            q.begin_other_pc_block(pid)
            cmdchat("HunterSystemSpeak " .. (color or "WHITE") .. "|" .. hg_lib.clean_str(msg))
            q.end_other_pc_block()
        end
    else
        -- Solo player
        hg_lib.hunter_speak_color(msg, color)
    end
end

-- Durata difesa in base al rank della frattura
function hg_lib.get_defense_duration_by_rank(rank_grade)
    rank_grade = hg_lib.validate_rank(rank_grade)
    
    -- Prova a leggere dal DB (defense_duration_X)
    local key = "defense_duration_" .. rank_grade
    local q = "SELECT config_value FROM srv1_hunabku.hunter_fracture_defense_config WHERE config_key='" .. key .. "'"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        return tonumber(d[1].config_value) or 60
    end
    
    -- Fallback: valori hardcoded
    local durations = {
        E = 60,   -- Base
        D = 60,   -- Base
        C = 60,   -- Base
        B = 90,   -- +30 sec
        A = 120,  -- +60 sec (2 min)
        S = 150,  -- +90 sec (2.5 min)
        N = 180   -- +120 sec (3 min)
    }
    return durations[rank_grade] or 60
end

function hg_lib.get_defense_config(key, default_val)
    local q = "SELECT config_value FROM srv1_hunabku.hunter_fracture_defense_config WHERE config_key='" .. key .. "'"
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        return tonumber(d[1].config_value) or default_val
    end
    return default_val
end

function hg_lib.check_defense_distance()
    local fx = pc.getqf("hq_defense_x") or 0
    local fy = pc.getqf("hq_defense_y") or 0
    if fx == 0 and fy == 0 then return false end
    local px, py = pc.get_local_x(), pc.get_local_y()
    local dx = px - fx
    local dy = py - fy
    local dist = math.sqrt(dx * dx + dy * dy)
    local max_dist = hg_lib.get_defense_config("check_distance", 10)
    return dist <= max_dist
end

-- Controlla distanza di TUTTI i membri del party dalla frattura
-- Ritorna: ok (bool), nome_lontano (string o nil)
function hg_lib.check_party_defense_distance()
    local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0
    if fracture_vid == 0 then return false, nil end
    
    local fx = pc.getqf("hq_defense_x") or 0
    local fy = pc.getqf("hq_defense_y") or 0
    if fx == 0 and fy == 0 then return false, nil end
    
    local max_dist = hg_lib.get_defense_config("check_distance", 10)
    
    -- Se NON in party, controlla solo il player corrente
    if not party.is_party() then
        local px, py = pc.get_local_x(), pc.get_local_y()
        local dx = px - fx
        local dy = py - fy
        local dist = math.sqrt(dx * dx + dy * dy)
        if dist > max_dist then
            return false, pc.get_name()
        end
        return true, nil
    end
    
    -- IN PARTY: Controlla TUTTI i membri
    local pids = {party.get_member_pids()}
    for i, member_pid in ipairs(pids) do
        q.begin_other_pc_block(member_pid)
        
        -- Verifica che il membro sia nella stessa mappa
        local member_map = pc.get_map_index()
        local leader_map = 0
        q.end_other_pc_block()
        
        -- Riprendi il contesto del leader per la mappa
        leader_map = pc.get_map_index()
        
        q.begin_other_pc_block(member_pid)
        member_map = pc.get_map_index()
        
        -- Se il membro e' in una mappa diversa, e' considerato lontano
        if member_map ~= leader_map then
            local member_name = pc.get_name()
            q.end_other_pc_block()
            return false, member_name
        end
        
        -- Controlla distanza del membro
        local mx, my = pc.get_local_x(), pc.get_local_y()
        local member_name = pc.get_name()
        q.end_other_pc_block()
        
        local dx = mx - fx
        local dy = my - fy
        local dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > max_dist then
            return false, member_name
        end
    end
    
    return true, nil
end

function hg_lib.spawn_defense_wave(wave_num, rank_grade)
    local ok, err = pcall(function()
        rank_grade = hg_lib.validate_rank(rank_grade)

        if not _G.hunter_defense_waves_cache or not _G.hunter_defense_waves_cache[rank_grade] then
            return
        end

        local wave_data = _G.hunter_defense_waves_cache[rank_grade][wave_num]
        if not wave_data or not wave_data.mobs then return end

        local fx = pc.getqf("hq_defense_x") or 0
        local fy = pc.getqf("hq_defense_y") or 0
        
        local current_req = pc.getqf("hq_defense_mob_req") or 0
        local added_req = 0

        for i, mob_info in ipairs(wave_data.mobs) do
            local vnum = mob_info.vnum or 0
            local count = mob_info.count or 1
            local radius = mob_info.radius or 7

            if count > 0 and vnum > 0 then
                local buffer = 2 
                local actual_spawn = count + buffer
                
                added_req = added_req + count
                
                for j = 1, actual_spawn do
                    local angle = (360 / actual_spawn) * j
                    local rad = math.rad(angle)
                    local sx = fx + math.floor(math.cos(rad) * radius)
                    local sy = fy + math.floor(math.sin(rad) * radius)
                    mob.spawn(vnum, sx, sy, 1)
                end
            end
        end
        
        pc.setqf("hq_defense_mob_req", current_req + added_req)
        
        -- NOTA: hq_defense_req_ viene settato una sola volta all'inizio con il totale
        -- Le wave non incrementano piu' il totale

        local msg = hg_lib.get_text("defense_wave_spawn", {WAVE = wave_num}) or ("ONDATA " .. wave_num .. "! DIFENDITI!")
        local fcolor = "RED"
        if hunter_defense_data and hunter_defense_data[pc.get_player_id()] then
            fcolor = hunter_defense_data[pc.get_player_id()].color or "RED"
        end

        -- FIX: Usa party_hunter_speak_color per inviare messaggi colorati a tutto il party
        local wave_msg = hg_lib.get_text("WAVE_NOTIFICATION", {WAVE = wave_num, MOBS = added_req}, "[ONDATA " .. wave_num .. "] +" .. added_req .. " nemici!")
        hg_lib.party_hunter_speak_color(wave_msg, fcolor)
    end)
end

function hg_lib.is_valid_defense_mob(rank_grade, vnum)
    local clean_rank = string.sub(rank_grade, 1, 1)
    clean_rank = hg_lib.validate_rank(clean_rank)

    if not _G.hunter_defense_waves_cache or not _G.hunter_defense_waves_cache[clean_rank] then
        hg_lib.load_defense_waves_cache(clean_rank)
    end
    
    local waves = _G.hunter_defense_waves_cache[clean_rank]
    if not waves then 
        return false 
    end
    
    for w_num, w_data in pairs(waves) do
        if w_data.mobs then
            for _, m_info in ipairs(w_data.mobs) do
                if tonumber(m_info.vnum) == tonumber(vnum) then
                    return true
                end
            end
        end
    end
    
    return false
end

-- FIX: Aggiunto salvataggio timestamp vittoria per logica 5 minuti
function hg_lib.complete_defense_success()
    local pid = pc.get_player_id()
    local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0

    local fname = "Frattura"
    local fcolor = "PURPLE"
    local frank = "E"
    if hunter_defense_data and hunter_defense_data[pid] then
        fname = hunter_defense_data[pid].fname
        fcolor = hunter_defense_data[pid].color
        frank = hunter_defense_data[pid].rank or "E"
    end
    
    -- Security Log: Defense completed
    hg_lib.log_info("DEFENSE", "DEFENSE_SUCCESS", 
        string.format("fracture_vid=%d rank=%s", fracture_vid, frank))

    pc.setqf("hq_defense_active", 0)
    cleartimer("hq_defense_timer")

    -- Invia chiusura UI DIFESA a tutto il party
    hg_lib.party_cmdchat("HunterFractureDefenseComplete 1")

    -- Reset flag su TUTTI i membri del party
    if party.is_party() then
        local success_msg = hg_lib.get_text("DEFENSE_SUCCESS", nil, "[HUNTER] DIFESA COMPLETATA CON SUCCESSO!")
        party.syschat(success_msg)
        
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_defense_active", 0)
            pc.setqf("hq_defense_fracture_vid", 0)
            pc.setqf("hq_defense_x", 0)
            pc.setqf("hq_defense_y", 0)
            pc.setqf("hq_defense_wave", 0)
            pc.setqf("hq_defense_mob_req", 0)
            pc.setqf("hq_defense_mob_killed", 0)
            q.end_other_pc_block()
            
            -- Pulisci hunter_defense_data per questo membro
            if hunter_defense_data and hunter_defense_data[member_pid] then
                hunter_defense_data[member_pid] = nil
            end
        end
    end

    if fracture_vid > 0 then
        game.set_event_flag("hq_gate_lock_"..fracture_vid, 0)   
        game.set_event_flag("hq_gate_conq_"..fracture_vid, pid) 
        -- FIX: Salva timestamp vittoria per scadenza 5 minuti
        game.set_event_flag("hq_gate_conq_time_"..fracture_vid, get_time())
        
        -- FIX: Salva rank e color per finalize_gate_opening (che viene chiamata DOPO la pulizia)
        local rank_idx_map = {E=0, D=1, C=2, B=3, A=4, S=5, N=6}
        game.set_event_flag("hq_gate_data_rank_"..fracture_vid, rank_idx_map[frank] or 0)
        -- Color index: PURPLE=0, BLUE=1, GREEN=2, YELLOW=3, ORANGE=4, RED=5, BLACK=6
        local color_idx_map = {PURPLE=0, BLUE=1, GREEN=2, YELLOW=3, ORANGE=4, RED=5, BLACK=6}
        game.set_event_flag("hq_gate_data_color_"..fracture_vid, color_idx_map[fcolor] or 0)
        
        -- CLEANUP: Pulisci flag globali della difesa
        game.set_event_flag("hq_defense_rank_"..fracture_vid, 0)
        game.set_event_flag("hq_defense_killed_"..fracture_vid, 0)
        game.set_event_flag("hq_defense_req_"..fracture_vid, 0)
        -- Pulisci flag party (usa leader_pid se in party)
        if party.is_party() then
            local leader_pid = party.get_leader_pid()
            game.set_event_flag("hq_party_defense_vid_"..leader_pid, 0)
        end
    end

    hg_lib.check_overtake(pid, pc.get_name(), "total_fractures", 1, "ESPLORATORI")
    pc.setqf("hq_pending_fractures", (pc.getqf("hq_pending_fractures") or 0) + 1)
    pc.setqf("hq_elite_spawn_time", get_time())
    pc.setqf("hq_pending_elite", (pc.getqf("hq_pending_elite") or 0) + 1)

    -- DETAILED STATS: Accumula defense wins (pending flush)
    if party.is_party() then
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_pending_defense_wins", (pc.getqf("hq_pending_defense_wins") or 0) + 1)
            q.end_other_pc_block()
        end
    else
        pc.setqf("hq_pending_defense_wins", (pc.getqf("hq_pending_defense_wins") or 0) + 1)
    end

    local msg = hg_lib.get_text("defense_success_click") or "FRATTURA CONQUISTATA! Hai 5 minuti per aprirla!"
    hg_lib.party_hunter_speak_color(msg, fcolor)
    hg_lib.party_cmdchat("HunterSystemSpeak " .. fcolor .. "|TOCCA IL PORTALE!")
    
    -- Registra partecipazione automatica all'evento (se attivo)
    hg_lib.register_event_participant()

    -- CHECK: Se evento "first_rift" attivo, il PRIMO a conquistare vince!
    hg_lib.check_first_rift_winner()

    -- Ripristina UI dell'Emergency vera se c'è ancora una attiva
    hg_lib.resend_emergency_ui()
end

function hg_lib.fail_defense(reason)
    local pid = pc.get_player_id()
    local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0
    
    -- Security Log: Defense failed
    hg_lib.log_info("DEFENSE", "DEFENSE_FAILED", 
        string.format("fracture_vid=%d reason=%s", fracture_vid, reason or "unknown"))
        
    local fcolor = "RED"
    local frank = "E"  -- Default rank
    
    -- PRIMA leggi il rank dalla event_flag (piu' affidabile)
    -- NOTA: rank_idx usa 0=E, 1=D, 2=C, 3=B, 4=A, 5=S, 6=N
    if fracture_vid > 0 then
        local rank_idx = game.get_event_flag("hq_defense_rank_"..fracture_vid) or 0
        local rank_letters = {[0]="E", [1]="D", [2]="C", [3]="B", [4]="A", [5]="S", [6]="N"}
        frank = rank_letters[rank_idx] or "E"
    end
    
    -- Fallback su hunter_defense_data se frank e' ancora E (potrebbe essere corretto o no)
    if hunter_defense_data and hunter_defense_data[pid] and hunter_defense_data[pid].rank then
        fcolor = hunter_defense_data[pid].color or "RED"
        local stored_rank = hunter_defense_data[pid].rank
        -- Usa hunter_defense_data solo se ha un rank diverso da E
        if stored_rank ~= "E" and stored_rank ~= "E-Rank" then
            frank = stored_rank
        end
    end
    
    -- Determina se la frattura deve essere distrutta o puo' essere riprovata
    -- E, D, C = puoi riprovare (frattura rimane)
    -- B, A, S, N = frattura distrutta (supporta sia "S" che "S-Rank")
    local destroy_on_fail = (
        frank == "B" or frank == "B-Rank" or 
        frank == "A" or frank == "A-Rank" or 
        frank == "S" or frank == "S-Rank" or 
        frank == "N" or frank == "N-Rank"
    )

    pc.setqf("hq_defense_active", 0)
    cleartimer("hq_defense_timer")

    -- Invia chiusura UI DIFESA a tutto il party
    hg_lib.party_cmdchat("HunterFractureDefenseComplete 0")

    -- Reset flag su TUTTI i membri del party
    if party.is_party() then
        if destroy_on_fail then
            local msg = hg_lib.get_text("DEFENSE_FAILED_DESTROYED", {REASON = reason, RANK = frank}, "[HUNTER] DIFESA FALLITA! " .. reason .. " - La Frattura Rank " .. frank .. " e' stata DISTRUTTA!")
            party.syschat(msg)
        else
            local msg = hg_lib.get_text("DEFENSE_FAILED_RETRY", {REASON = reason, RANK = frank}, "[HUNTER] DIFESA FALLITA! " .. reason .. " - La Frattura Rank " .. frank .. " e' ancora li, puoi riprovare!")
            party.syschat(msg)
        end
        
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_defense_active", 0)
            pc.setqf("hq_defense_fracture_vid", 0)
            pc.setqf("hq_defense_x", 0)
            pc.setqf("hq_defense_y", 0)
            pc.setqf("hq_defense_wave", 0)
            pc.setqf("hq_defense_mob_req", 0)
            pc.setqf("hq_defense_mob_killed", 0)
            q.end_other_pc_block()
            
            -- Pulisci hunter_defense_data per questo membro
            if hunter_defense_data and hunter_defense_data[member_pid] then
                hunter_defense_data[member_pid] = nil
            end
        end
    end

    if fracture_vid > 0 then
        game.set_event_flag("hq_gate_lock_"..fracture_vid, 0)
        game.set_event_flag("hq_gate_conq_"..fracture_vid, 0)
        -- CLEANUP: Pulisci flag globali della difesa
        game.set_event_flag("hq_defense_rank_"..fracture_vid, 0)
        game.set_event_flag("hq_defense_killed_"..fracture_vid, 0)
        game.set_event_flag("hq_defense_req_"..fracture_vid, 0)
        -- Pulisci flag party (usa leader_pid se in party)
        if party.is_party() then
            local leader_pid = party.get_leader_pid()
            game.set_event_flag("hq_party_defense_vid_"..leader_pid, 0)
        end
        pc.setqf("hq_defense_fracture_vid", 0)
        
        -- RANK-BASED DESTRUCTION:
        -- Solo rank B, A, S, N perdono la frattura al fallimento
        -- Rank E, D, C possono riprovare (frattura rimane)
        if destroy_on_fail then
            -- Marca la frattura come "da rimuovere"
            game.set_event_flag("hq_gate_destroy_"..fracture_vid, 1)
            
            -- Metodo 1: mob.kill (se disponibile)
            if mob and mob.kill then
                mob.kill(fracture_vid)
            end
            
            -- Metodo 2: purge_vid (alternativo)
            if purge_vid then
                purge_vid(fracture_vid)
            end
            
            -- Metodo 3: kill_mob_vid (alternativo)
            if kill_mob_vid then
                kill_mob_vid(fracture_vid)
            end
            
            -- Messaggio chiaro al player
            syschat("|cffFF0000============================================|r")
            hg_lib.syschat_t("DEFENSE_FAILED", "DIFESA FALLITA!", nil, "FF0000")
            hg_lib.syschat_t("DEFENSE_DESTROYED", "La Frattura {RANK} e' stata DISTRUTTA!", {RANK = frank}, "FF0000")
            hg_lib.syschat_t("DEFENSE_HIGH_RANK_WARNING1", "Le fratture di Rank B e superiori", nil, "FF6600")
            hg_lib.syschat_t("DEFENSE_HIGH_RANK_WARNING2", "vengono distrutte se fallisci la difesa.", nil, "FF6600")
            hg_lib.syschat_t("DEFENSE_SORRY", "Mi dispiace, Hunter. Buona caccia!", nil, "FFFF00")
            syschat("|cffFF0000============================================|r")
        else
            syschat("|cffFFFF00============================================|r")
            hg_lib.syschat_t("DEFENSE_FAILED", "DIFESA FALLITA!", nil, "FFFF00")
            hg_lib.syschat_t("DEFENSE_STILL_AVAILABLE", "La Frattura {RANK} e' ancora disponibile.", {RANK = frank}, "00FF00")
            hg_lib.syschat_t("DEFENSE_CAN_RETRY", "Puoi riprovare la difesa!", nil, "00FF00")
            syschat("|cffFFFF00============================================|r")
        end
    end

    if hunter_defense_data and hunter_defense_data[pid] then
        hunter_defense_data[pid] = nil
    end

    -- Messaggio finale differenziato per rank (NPC speak)
    local msg
    if destroy_on_fail then
        msg = hg_lib.get_text("defense_failed_destroyed") or ("DIFESA FALLITA! " .. reason .. " - Le fratture Rank " .. frank .. " e superiori vengono DISTRUTTE se fallisci!")
    else
        msg = hg_lib.get_text("defense_failed_retry") or ("DIFESA FALLITA! " .. reason .. " - La frattura Rank " .. frank .. " e' ancora li, puoi riprovare!")
    end
    hg_lib.hunter_speak_color(msg, "RED")

    -- DETAILED STATS: Accumula defense losses (pending flush)
    if party.is_party() then
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_pending_defense_losses", (pc.getqf("hq_pending_defense_losses") or 0) + 1)
            q.end_other_pc_block()
        end
    else
        pc.setqf("hq_pending_defense_losses", (pc.getqf("hq_pending_defense_losses") or 0) + 1)
    end

    -- Ripristina UI dell'Emergency vera se c'è ancora una attiva
    hg_lib.resend_emergency_ui()
end

function hg_lib.spawn_gate_mob_and_alert(rank_label, fcolor)
    -- Converti rank_label in rank_tier numerico (1=E, 2=D, 3=C, 4=B, 5=A, 6=S, 7=N)
    local rank_tier_map = {
        ["E-Rank"] = 1, ["E"] = 1,
        ["D-Rank"] = 2, ["D"] = 2,
        ["C-Rank"] = 3, ["C"] = 3,
        ["B-Rank"] = 4, ["B"] = 4,
        ["A-Rank"] = 5, ["A"] = 5,
        ["S-Rank"] = 6, ["S"] = 6,
        ["N-Rank"] = 7, ["N"] = 7
    }
    local max_tier = rank_tier_map[rank_label] or 1
    
    -- PERFORMANCE: Cache spawn types per 5 minuti
    if not _G.hunter_spawn_types_cache or (get_time() - (_G.hunter_spawn_types_cache_time or 0)) > 300 then
        local tc, td = mysql_direct_query("SELECT type_name, probability FROM srv1_hunabku.hunter_quest_spawn_types WHERE enabled=1")
        if tc > 0 then
            local total = 0
            for i = 1, tc do total = total + tonumber(td[i].probability) end
            _G.hunter_spawn_types_cache = {count = tc, data = td, total = total}
            _G.hunter_spawn_types_cache_time = get_time()
        end
    end
    
    local cached_types = _G.hunter_spawn_types_cache
    if not cached_types then return end
    local c, d = cached_types.count, cached_types.data
    local total_prob = cached_types.total
    
    -- Se total_prob e 0, evita crash
    if total_prob <= 0 then total_prob = 1 end

    local roll = number(1, total_prob) -- Usa la somma reale, non 1000 fisso
    local cumul = 0
    local sel_type = d[1].type_name -- Default al primo disponibile
    
    for i = 1, c do 
        cumul = cumul + tonumber(d[i].probability)
        if roll <= cumul then 
            sel_type = d[i].type_name
            break 
        end 
    end
        
    local lv = pc.get_level()
    -- FILTRO PER RANK: spawna solo mob con rank_tier <= rango della frattura
    local q = "SELECT vnum, name, rank_color FROM srv1_hunabku.hunter_quest_spawns WHERE type_name='" .. sel_type .. "' AND enabled=1 AND rank_tier<=" .. max_tier .. " AND min_level<=" .. lv .. " AND max_level>=" .. lv .. " ORDER BY RAND() LIMIT 1"
    local mc, md = mysql_direct_query(q)
    
    -- Fallback: cerca qualsiasi livello ma sempre rispettando il rank
    if mc == 0 then 
        q = "SELECT vnum, name, rank_color FROM srv1_hunabku.hunter_quest_spawns WHERE type_name='" .. sel_type .. "' AND enabled=1 AND rank_tier<=" .. max_tier .. " ORDER BY RAND() LIMIT 1"
        mc, md = mysql_direct_query(q) 
    end
    
    -- Fallback estremo: se ancora nulla, prendi il mob piu basso di quel tipo
    if mc == 0 then 
        q = "SELECT vnum, name, rank_color FROM srv1_hunabku.hunter_quest_spawns WHERE type_name='" .. sel_type .. "' AND enabled=1 ORDER BY rank_tier ASC LIMIT 1"
        mc, md = mysql_direct_query(q) 
    end
        
    if mc > 0 and md[1] then
        local mob_name = md[1].name
        if not mob_name or mob_name == "" then mob_name = "Bersaglio Misterioso" end

        local x, y = pc.get_local_x(), pc.get_local_y()
        local spawned_vnum = tonumber(md[1].vnum)
        mob.spawn(spawned_vnum, x + 5, y + 5, 1)

        local mob_color = md[1].rank_color or "PURPLE"

        if sel_type == "BAULE" then
            local msg = hg_lib.get_text("spawn_chest_detected") or "BAULE DEL TESORO RILEVATO!"
            -- Notifica tutto il party
            hg_lib.party_hunter_speak_color(msg, fcolor or "GOLD")
        else
            -- Gestione Boss/Metin
            local msg = "*** MINACCIA RILEVATA: " .. mob_name .. " [" .. rank_label .. "] ***"
            -- Notifica tutto il party
            hg_lib.party_hunter_speak_color(msg, mob_color)

            if sel_type == "BOSS" or sel_type == "SUPER_METIN" then
                -- Invia alert a TUTTI i membri del party
                hg_lib.party_cmdchat("HunterBossAlert " .. string.gsub(mob_name, " ", "+"))
            end
            
            -- Logica Speed Kill
            local emergency_title = ""
            local emergency_seconds = 0
            local bonus_points = 0
            
            if sel_type == "BOSS" then
                emergency_title = "UCCIDI: "..mob_name
                emergency_seconds = 60
                local db_val = hg_lib.get_config("speedkill_boss_bonus_pts")
                if db_val <= 0 then db_val = 300 end
                bonus_points = db_val
            elseif sel_type == "SUPER_METIN" then
                emergency_title = "DISTRUGGI: "..mob_name
                emergency_seconds = 300
                local db_val = hg_lib.get_config("speedkill_metin_bonus_pts")
                if db_val <= 0 then db_val = 150 end
                bonus_points = db_val
            end

            if emergency_seconds > 0 then
                -- Setta reward su TUTTI i membri del party
                if party.is_party() then
                    local pids = {party.get_member_pids()}
                    for i, member_pid in ipairs(pids) do
                        q.begin_other_pc_block(member_pid)
                        pc.setqf("hq_emerg_reward_pts", bonus_points)
                        pc.setqf("hq_emerg_reward_vnum", 0)
                        pc.setqf("hq_emerg_reward_count", 0)
                        pc.setqf("hq_speedkill_active", 1)
                        pc.setqf("hq_speedkill_vnum", spawned_vnum)
                        pc.setqf("hq_speedkill_start", get_time())
                        pc.setqf("hq_speedkill_duration", emergency_seconds)
                        q.end_other_pc_block()
                    end
                else
                    pc.setqf("hq_emerg_reward_pts", bonus_points)
                    pc.setqf("hq_emerg_reward_vnum", 0)
                    pc.setqf("hq_emerg_reward_count", 0)
                    pc.setqf("hq_speedkill_active", 1)
                    pc.setqf("hq_speedkill_vnum", spawned_vnum)
                    pc.setqf("hq_speedkill_start", get_time())
                    pc.setqf("hq_speedkill_duration", emergency_seconds)
                end
                
                -- NON usare start_emergency per Boss/Super Metin
                -- Ora abbiamo la UI dedicata SpeedKillTimer che non confligge con le fratture

                cleartimer("hq_speedkill_timer")
                loop_timer("hq_speedkill_timer", 1)

                -- Invia UI Speed Kill a tutti i membri del party
                hg_lib.party_cmdchat("HunterSpeedKillStart " .. sel_type .. "|" .. emergency_seconds .. "|" .. string.gsub(mob_name, " ", "+"))

                local sk_msg = ">> SFIDA VELOCITA': Abbattilo in " .. emergency_seconds .. "s per DOPPIA GLORIA! <<"
                -- Notifica tutto il party
                hg_lib.party_hunter_speak_color(sk_msg, "GOLD")
            end
            
            local pname = pc.get_name()
            local map_name = hg_lib.get_map_name()
            local channel = hg_lib.get_channel()
            local location_str = ""
            if channel > 0 then
                location_str = " | " .. map_name .. " CH" .. channel .. " (" .. x .. ", " .. y .. ")"
            else
                location_str = " | " .. map_name .. " (" .. x .. ", " .. y .. ")"
            end
            local awakening_msg = hg_lib.get_text("AWAKENING_NOTICE", {PLAYER = pname, MOB = mob_name, RANK = rank_label, LOCATION = location_str}, pname .. " ha risvegliato: " .. mob_name .. " (" .. rank_label .. ")" .. location_str)
            notice_all("|cffFF4444[HUNTER]|r " .. awakening_msg)
        end
    end
end

-- FIX: Aggiunta pulizia flag timestamp vittoria
function hg_lib.finalize_gate_opening(vid)
    local pid = pc.get_player_id()
    
    -- FIX: Recupera rank e color dalle event_flags (salvate in complete_defense_success)
    -- Questi dati sono stati salvati PRIMA della pulizia di hunter_defense_data
    local rank_idx = game.get_event_flag("hq_gate_data_rank_"..vid) or 0
    local color_idx = game.get_event_flag("hq_gate_data_color_"..vid) or 0
    
    local rank_letters = {[0]="E", [1]="D", [2]="C", [3]="B", [4]="A", [5]="S", [6]="N"}
    local color_names = {[0]="PURPLE", [1]="BLUE", [2]="GREEN", [3]="YELLOW", [4]="ORANGE", [5]="RED", [6]="BLACK"}
    
    local frank = rank_letters[rank_idx] or "E"
    local fcolor = color_names[color_idx] or "PURPLE"
    
    -- Fallback su hunter_defense_data se event_flag non aveva dati
    if hunter_defense_data and hunter_defense_data[pid] then
        if rank_idx == 0 and hunter_defense_data[pid].rank then
            frank = hunter_defense_data[pid].rank
        end
        if color_idx == 0 and hunter_defense_data[pid].color then
            fcolor = hunter_defense_data[pid].color
        end
        hunter_defense_data[pid] = nil
    end
    
    -- Pulisci le event_flags dei dati gate
    game.set_event_flag("hq_gate_data_rank_"..vid, 0)
    game.set_event_flag("hq_gate_data_color_"..vid, 0)
    
    -- Pulisci flag su TUTTI i membri del party
    if party.is_party() then
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            q.begin_other_pc_block(member_pid)
            pc.setqf("hq_defense_fracture_vid", 0)
            pc.setqf("hq_defense_active", 0)
            q.end_other_pc_block()
            
            -- Pulisci hunter_defense_data per questo membro
            if hunter_defense_data and hunter_defense_data[member_pid] then
                hunter_defense_data[member_pid] = nil
            end
        end
        
        -- Pulisci flag party defense
        local leader_pid = party.get_leader_pid()
        game.set_event_flag("hq_party_defense_vid_" .. leader_pid, 0)
    else
        pc.setqf("hq_defense_fracture_vid", 0)
    end
        
    game.set_event_flag("hq_gate_lock_"..vid, 0)
    game.set_event_flag("hq_gate_conq_"..vid, 0)
    game.set_event_flag("hq_gate_conq_time_"..vid, 0)
    
    -- === NUOVO: ASSEGNA IL PUNTO QUI ===
    -- Ora il punto viene dato solo quando la frattura si apre effettivamente
    hg_lib.on_fracture_seal()
    -- ===================================
        
    hg_lib.spawn_gate_mob_and_alert(frank, fcolor)
    npc.purge() -- L'NPC sparisce, quindi non puo' essere riusata
        
    pc.setqf("hq_elite_spawn_time", get_time())
end

function hg_lib.send_all_data()
    hg_lib.send_player_data()
    hg_lib.send_ranking("daily")
    hg_lib.send_ranking("weekly")
    hg_lib.send_ranking("total")
    hg_lib.send_ranking_kills("daily")
    hg_lib.send_ranking_kills("weekly")
    hg_lib.send_ranking_kills("total")
    hg_lib.send_ranking_special("fractures")
    hg_lib.send_ranking_special("chests")
    hg_lib.send_ranking_special("metins")
    hg_lib.send_shop()
    hg_lib.send_achievements()
    hg_lib.send_calendar()
    hg_lib.send_timers()
    hg_lib.send_event()
    hg_lib.send_fractures()
end

-- ============================================================
-- MEMORY LEAK CLEANUP - Pulizia periodica tabelle globali
-- Previene memory leak rimuovendo entry vecchie/inutilizzate
-- ============================================================
function hg_lib.cleanup_global_tables()
    local now = get_time()
    local cleanup_threshold = 3600  -- 1 ora

    -- 1. Pulisci hunter_temp_gate_data (dati gate temporanei)
    if _G.hunter_temp_gate_data then
        local count_before = 0
        local count_after = 0
        for pid, data in pairs(_G.hunter_temp_gate_data) do
            count_before = count_before + 1
            -- Rimuovi se più vecchio di 1 ora
            if data.timestamp and (now - data.timestamp > cleanup_threshold) then
                _G.hunter_temp_gate_data[pid] = nil
            else
                count_after = count_after + 1
            end
        end
        if count_before > count_after then
            -- Log cleanup (opzionale)
            -- syschat("Cleanup: hunter_temp_gate_data " .. (count_before - count_after) .. " entries removed")
        end
    end

    -- 2. Pulisci hunter_mission_buffer (buffer missioni per player offline)
    if _G.hunter_mission_buffer then
        -- Qui non possiamo controllare se il player è online facilmente
        -- Quindi rimuoviamo solo buffer molto vecchi (usa throttle timestamp)
        for pid, buffer in pairs(_G.hunter_mission_buffer) do
            -- Se il buffer è vuoto, rimuovilo
            local is_empty = true
            for k, v in pairs(buffer) do
                is_empty = false
                break
            end
            if is_empty then
                _G.hunter_mission_buffer[pid] = nil
            end
        end
    end

    -- 3. Pulisci hunter_mission_throttle (timestamp vecchi)
    if _G.hunter_mission_throttle then
        for key, timestamp in pairs(_G.hunter_mission_throttle) do
            -- Rimuovi timestamp più vecchi di 1 ora
            if now - timestamp > cleanup_threshold then
                _G.hunter_mission_throttle[key] = nil
            end
        end
    end

    -- 4. Pulisci hunter_player_data_cache (timestamp vecchi)
    if _G.hunter_player_data_cache then
        for pid, timestamp in pairs(_G.hunter_player_data_cache) do
            -- Rimuovi timestamp più vecchi di 10 minuti
            if now - timestamp > 600 then
                _G.hunter_player_data_cache[pid] = nil
            end
        end
    end

    -- NOTE: hunter_elite_cache, hunter_defense_waves_cache sono cache statiche,
    -- non crescono nel tempo quindi non serve cleanup
end

-- ============================================================
-- OTTIMIZZAZIONE send_player_data - Throttling per ridurre carico
-- Con 300K kill/min, questa funzione era chiamata troppo spesso
-- NUOVA VERSIONE: Throttle 3 secondi + UNA query invece di 3
-- ============================================================
_G.hunter_player_data_cache = {}  -- Cache per throttling

function hg_lib.send_player_data(force)
    local pid = pc.get_player_id()
    local now = get_time()
    
    -- PERFORMANCE: Throttle a max 1 call ogni 3 secondi (a meno che force=true)
    local last_send = _G.hunter_player_data_cache[pid] or 0
    if not force and (now - last_send < 3) then
        return  -- Skip, troppo presto
    end
    _G.hunter_player_data_cache[pid] = now
    
    -- PERFORMANCE: UNA SOLA query con subquery invece di 3 separate
    local q = string.format([[
        SELECT
            r.total_points, r.spendable_points, r.daily_points, r.weekly_points,
            r.total_kills, r.daily_kills, r.weekly_kills,
            r.total_fractures, r.total_chests, r.total_metins,
            r.pending_daily_reward, r.pending_weekly_reward,
            (SELECT COUNT(*) FROM srv1_hunabku.hunter_quest_ranking WHERE daily_points > r.daily_points) + 1 as pos_d,
            (SELECT COUNT(*) FROM srv1_hunabku.hunter_quest_ranking WHERE weekly_points > r.weekly_points) + 1 as pos_w,
            r.chests_e, r.chests_d, r.chests_c, r.chests_b, r.chests_a, r.chests_s, r.chests_n,
            r.boss_kills_easy, r.boss_kills_medium, r.boss_kills_hard, r.boss_kills_elite,
            r.metin_kills_normal, r.metin_kills_special,
            r.defense_wins, r.defense_losses, r.elite_kills
        FROM srv1_hunabku.hunter_quest_ranking r
        WHERE r.player_id = %d
    ]], pid)
    
    local c, d = mysql_direct_query(q)
    if c > 0 and d[1] then
        local total_pts = tonumber(d[1].total_points) or 0
        local dp = tonumber(d[1].daily_points) or 0
        local wp = tonumber(d[1].weekly_points) or 0
        
        local new_rank_num = hg_lib.get_rank_index(total_pts)
        pc.setqf("hq_rank_num", new_rank_num)
        
        local pos_d = dp > 0 and (tonumber(d[1].pos_d) or 0) or 0
        local pos_w = wp > 0 and (tonumber(d[1].pos_w) or 0) or 0
            
        local pkt = hg_lib.clean_str(pc.get_name()) .. "|" ..
            total_pts .. "|" ..
            (tonumber(d[1].spendable_points) or 0) .. "|" ..
            dp .. "|" .. wp .. "|" ..
            (tonumber(d[1].total_kills) or 0) .. "|" ..
            (tonumber(d[1].daily_kills) or 0) .. "|" ..
            (tonumber(d[1].weekly_kills) or 0) .. "|" ..
            (pc.getqf("hq_login_streak") or 0) .. "|" ..
            (pc.getqf("hq_streak_bonus") or 0) .. "|" ..
            (tonumber(d[1].total_fractures) or 0) .. "|" ..
            (tonumber(d[1].total_chests) or 0) .. "|" ..
            (tonumber(d[1].total_metins) or 0) .. "|" ..
            (tonumber(d[1].pending_daily_reward) or 0) .. "|" ..
            (tonumber(d[1].pending_weekly_reward) or 0) .. "|" ..
            pos_d .. "|" .. pos_w .. "|" ..
            (tonumber(d[1].chests_e) or 0) .. "|" .. (tonumber(d[1].chests_d) or 0) .. "|" .. (tonumber(d[1].chests_c) or 0) .. "|" ..
            (tonumber(d[1].chests_b) or 0) .. "|" .. (tonumber(d[1].chests_a) or 0) .. "|" .. (tonumber(d[1].chests_s) or 0) .. "|" .. (tonumber(d[1].chests_n) or 0) .. "|" ..
            (tonumber(d[1].boss_kills_easy) or 0) .. "|" .. (tonumber(d[1].boss_kills_medium) or 0) .. "|" .. (tonumber(d[1].boss_kills_hard) or 0) .. "|" .. (tonumber(d[1].boss_kills_elite) or 0) .. "|" ..
            (tonumber(d[1].metin_kills_normal) or 0) .. "|" .. (tonumber(d[1].metin_kills_special) or 0) .. "|" ..
            (tonumber(d[1].defense_wins) or 0) .. "|" .. (tonumber(d[1].defense_losses) or 0) .. "|" ..
            (tonumber(d[1].elite_kills) or 0)
        cmdchat("HunterPlayerData " .. pkt)
    end
end

function hg_lib.send_ranking(rtype)
    local col, kcol, cmd = "total_points", "total_kills", "HunterRankingTotal"
    if rtype == "daily" then 
        col, kcol, cmd = "daily_points", "daily_kills", "HunterRankingDaily"
    elseif rtype == "weekly" then 
        col, kcol, cmd = "weekly_points", "weekly_kills", "HunterRankingWeekly" 
    end
    local q = "SELECT player_name, " .. col .. " as pts, " .. kcol .. " as kills FROM srv1_hunabku.hunter_quest_ranking WHERE " .. col .. " > 0 ORDER BY " .. col .. " DESC LIMIT 10"
    local c, d = mysql_direct_query(q)
    local str = ""
    if c > 0 then 
        for i=1,c do 
            str = str .. hg_lib.clean_str(d[i].player_name) .. "," .. d[i].pts .. "," .. d[i].kills .. ";" 
        end 
    end
    local result = "EMPTY"
    if str ~= "" then result = str end
    cmdchat(cmd .. " " .. result)
end

function hg_lib.send_ranking_kills(rtype)
    local col, cmd = "total_kills", "HunterRankingTotalKills"
    if rtype == "daily" then 
        col, cmd = "daily_kills", "HunterRankingDailyKills"
    elseif rtype == "weekly" then 
        col, cmd = "weekly_kills", "HunterRankingWeeklyKills" 
    end
    local q = "SELECT player_name, " .. col .. " as val, total_points FROM srv1_hunabku.hunter_quest_ranking WHERE " .. col .. " > 0 ORDER BY " .. col .. " DESC LIMIT 10"
    local c, d = mysql_direct_query(q)
    local str = ""
    if c > 0 then 
        for i=1,c do 
            str = str .. hg_lib.clean_str(d[i].player_name) .. "," .. d[i].val .. "," .. d[i].total_points .. ";" 
        end 
    end
    cmdchat(cmd .. " " .. (str == "" and "EMPTY" or str))
end

function hg_lib.send_ranking_special(cat)
    local col, cmd = "total_fractures", "HunterRankingFractures"
    if cat == "chests" then 
        col, cmd = "total_chests", "HunterRankingChests"
    elseif cat == "metins" then 
        col, cmd = "total_metins", "HunterRankingMetins" 
    end
    local q = "SELECT player_name, " .. col .. " as val, total_points FROM srv1_hunabku.hunter_quest_ranking WHERE " .. col .. " > 0 ORDER BY " .. col .. " DESC LIMIT 10"
    local c, d = mysql_direct_query(q)
    local str = ""
    if c > 0 then 
        for i=1,c do 
            str = str .. hg_lib.clean_str(d[i].player_name) .. "," .. d[i].val .. "," .. d[i].total_points .. ";" 
        end 
    end
    cmdchat(cmd .. " " .. (str == "" and "EMPTY" or str))
end

function hg_lib.send_shop()
    local c, d = mysql_direct_query("SELECT id, item_vnum, item_count, price_points, description FROM srv1_hunabku.hunter_quest_shop WHERE enabled=1 ORDER BY display_order")
    local str = ""
    if c > 0 then 
        for i=1,c do 
            str = str .. d[i].id .. "," .. d[i].item_vnum .. "," .. d[i].item_count .. "," .. d[i].price_points .. "," .. hg_lib.clean_str(d[i].description) .. ";" 
        end 
    end
    local result = "EMPTY"
    if str ~= "" then result = str end
    cmdchat("HunterShopItems " .. result)
end

function hg_lib.send_achievements()
    local c, d = mysql_direct_query("SELECT id, name, type, requirement FROM srv1_hunabku.hunter_quest_achievements_config WHERE enabled=1 ORDER BY requirement")
    local str = ""
    if c > 0 then
        local k, p = pc.getqf("hq_total_kills") or 0, pc.getqf("hq_total_points") or 0
        for i=1,c do
            local aid, at, req = tonumber(d[i].id), tonumber(d[i].type), tonumber(d[i].requirement)
            local prg = k
            if at ~= 1 then prg = p end
            local unl = 0
            if prg >= req then unl = 1 end
            local clm = pc.getqf("hq_ach_clm_" .. aid) or 0
            str = str .. aid .. "," .. hg_lib.clean_str(d[i].name) .. "," .. at .. "," .. req .. "," .. prg .. "," .. unl .. "," .. clm .. ";"
        end
    end
    local result = "EMPTY"
    if str ~= "" then result = str end
    cmdchat("HunterAchievements " .. result)
end

function hg_lib.send_calendar()
    local c, d = mysql_direct_query("SELECT DISTINCT SUBSTRING_INDEX(days_active, ',', 1) as day_index, event_name, start_hour, (start_hour + FLOOR(duration_minutes/60)) as end_hour FROM srv1_hunabku.hunter_scheduled_events WHERE enabled = 1 ORDER BY start_hour LIMIT 21")
    local str = ""
    if c > 0 then 
        for i=1,c do
            local day_idx = tonumber(d[i].day_index) or 1
            day_idx = day_idx - 1
            str = str .. day_idx .. "," .. hg_lib.clean_str(d[i].event_name) .. "," .. d[i].start_hour .. "," .. d[i].end_hour .. ";" 
        end 
    end
    local result = "EMPTY"
    if str ~= "" then result = str end
    cmdchat("HunterCalendar " .. result)
end

function hg_lib.send_timers()
    local ts = get_time()
    local hour = hg_lib.get_hour_from_ts(ts)
    local min = hg_lib.get_min_from_ts(ts)
    local sec = hg_lib.get_sec_from_ts(ts)
    local seconds_today = (hour * 3600) + (min * 60) + sec
    local daily = 86400 - seconds_today
    local wday = hg_lib.get_day_db_from_ts(ts)
    local days_to_mon = 8 - wday
    if days_to_mon == 8 then days_to_mon = 7 end
    local weekly = (days_to_mon * 86400) - seconds_today
    cmdchat("HunterTimers " .. daily .. "|" .. weekly)
end

function hg_lib.send_event()
    local event = hg_lib.get_current_scheduled_event()
    local result = "NONE"
        
    if event then
        local name = event.event_name or "Evento"
        local desc = event.event_desc or ""
        local etype = event.event_type or "glory_rush"
        local reward = tonumber(event.reward_glory_base) or 50
        local winner = tonumber(event.reward_glory_winner) or 200
            
        local t = os.date("*t")
        local current_hour = t.hour
        local current_minute = t.min
        local current_total = current_hour * 60 + current_minute
            
        local start_total = tonumber(event.start_hour) * 60 + tonumber(event.start_minute)
        local duration = tonumber(event.duration_minutes) or 30
        local end_total = start_total + duration
            
        local remaining_minutes = end_total - current_total
        local remaining_seconds = remaining_minutes * 60
            
        result = hg_lib.clean_str(name) .. "|" .. 
                 hg_lib.clean_str(desc) .. "|" .. 
                 etype .. "|" .. 
                 math.floor(remaining_seconds) .. "|" .. 
                 reward .. "|" .. 
                 winner
    end
    cmdchat("HunterActiveEvent " .. result)
end

function hg_lib.send_fractures()
    local c, d = mysql_direct_query("SELECT name, req_points FROM srv1_hunabku.hunter_quest_fractures WHERE enabled=1 ORDER BY req_points")
    local str = ""
    if c > 0 then 
        for i=1,c do 
            str = str .. hg_lib.clean_str(d[i].name) .. "," .. d[i].req_points .. ";" 
        end 
    end
    local result = "EMPTY"
    if str ~= "" then result = str end
    cmdchat("HunterFractures " .. result)
end

function hg_lib.achiev_claim(id)
    local c, d = mysql_direct_query("SELECT name, type, requirement, reward_vnum, reward_count FROM srv1_hunabku.hunter_quest_achievements_config WHERE id="..id)
    if c == 0 or not d[1] then return end
        
    local name, req, vnum, count = d[1].name, tonumber(d[1].requirement), tonumber(d[1].reward_vnum), tonumber(d[1].reward_count)
    local atype = tonumber(d[1].type)
    local prog = pc.getqf("hq_total_points")
    if atype == 1 then prog = pc.getqf("hq_total_kills") end
    local is_claimed = (pc.getqf("hq_ach_clm_"..id) == 1)
    local is_unlocked = (prog >= req)
        
    say_title("|cffFFD700ACHIEVEMENT: " .. name .. "|r")
    say("Requisito: " .. req .. (atype==1 and " Kills" or " Gloria"))
    say("Ricompensa: x" .. count .. " " .. hg_lib.item_name(vnum))
    say_item_vnum(vnum)
    say("")
    if is_claimed then 
        say("|cffFF0000[!] RICOMPENSA GIA' RISCOSSA|r")
        select("Chiudi")
    elseif not is_unlocked then 
        say("|cff888888[!] BLOCCATO - Impegnati di piu'|r")
        select("Chiudi")
    else
        if select("Riscuoti Premio", "Chiudi") == 1 then
            pc.setqf("hq_ach_clm_"..id, 1)
            pc.give_item2(vnum, count)
            hg_lib.hunter_speak("OGGETTO RICEVUTO: " .. hg_lib.item_name(vnum))
            hg_lib.send_achievements()
        end
    end
end

function hg_lib.smart_claim_reward()
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT pending_daily_reward, pending_weekly_reward FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
    if c == 0 or not d[1] then return end
        
    local pd, pw = tonumber(d[1].pending_daily_reward) or 0, tonumber(d[1].pending_weekly_reward) or 0
    if pd == 0 and pw == 0 then 
        say_title("RICOMPENSE HUNTER")
        say("Nessun premio in attesa al momento.")
        say("Scala la classifica per ottenere gloria!")
        select("Chiudi")
        return 
    end
        
    say_title("PREMI DISPONIBILI")
    local opts, rdata = {}, {}
    if pd > 0 then
        local rc, rd = mysql_direct_query("SELECT item_vnum, item_quantity FROM srv1_hunabku.hunter_quest_rewards WHERE reward_type='daily' AND rank_position=" .. pd)
        if rc > 0 and rd[1] then
            say("|cff00FFFF[DAILY RANK]|r Posizione: |cffFFD700" .. pd .. "|r")
            say_item_vnum(tonumber(rd[1].item_vnum))
            table.insert(opts, "Riscuoti Premio Giornaliero")
            table.insert(rdata, {t="daily", p=pd, v=tonumber(rd[1].item_vnum), q=tonumber(rd[1].item_quantity)})
        end
    end
    if pw > 0 then
        local rc, rd = mysql_direct_query("SELECT item_vnum, item_quantity FROM srv1_hunabku.hunter_quest_rewards WHERE reward_type='weekly' AND rank_position=" .. pw)
        if rc > 0 and rd[1] then
            say("|cffFFD700[WEEKLY RANK]|r Posizione: |cffFFD700" .. pw .. "|r")
            say_item_vnum(tonumber(rd[1].item_vnum))
            table.insert(opts, "Riscuoti Premio Settimanale")
            table.insert(rdata, {t="weekly", p=pw, v=tonumber(rd[1].item_vnum), q=tonumber(rd[1].item_quantity)})
        end
    end
    if pd > 0 and pw > 0 then 
        table.insert(opts, "Riscuoti TUTTO") 
    end
    table.insert(opts, "Annulla")
    local s = select_table(opts)
    if s == table.getn(opts) then return end
        
    if pd > 0 and pw > 0 and s == table.getn(opts)-1 then
        hg_lib.give_pending_reward("daily", pd)
        hg_lib.give_pending_reward("weekly", pw)
    elseif rdata[s] then
        hg_lib.give_pending_reward(rdata[s].t, rdata[s].p)
    end
    hg_lib.send_player_data()
end

function hg_lib.give_pending_reward(rtype, pos)
    if pc.getqf("hq_reward_lock") == 1 then 
        syschat("Attendere prego...")
        return 
    end
    pc.setqf("hq_reward_lock", 1) 

    local pid = pc.get_player_id()
    local rc, rd = mysql_direct_query("SELECT item_vnum, item_quantity FROM srv1_hunabku.hunter_quest_rewards WHERE reward_type='" .. rtype .. "' AND rank_position=" .. pos)
    
    if rc > 0 and rd[1] then
        mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET " .. (rtype=="weekly" and "pending_weekly_reward" or "pending_daily_reward") .. " = 0 WHERE player_id=" .. pid)
        
        pc.give_item2(tonumber(rd[1].item_vnum), tonumber(rd[1].item_quantity))
        
        local pname = pc.get_name()
        local rtype_label = rtype == "daily" and (hg_lib.get_text("reward_type_daily") or "Giornaliera") or (hg_lib.get_text("reward_type_weekly") or "Settimanale")
        local msg = hg_lib.get_text("reward_claimed", {PLAYER = pname, TYPE = rtype_label}) or ("|cffFFD700[HUNTER]|r " .. pname .. " ha riscosso il premio Top Classifica " .. rtype_label .. "!")
        notice_all(msg)
    end

    pc.setqf("hq_reward_lock", 0)
end

function hg_lib.shop_buy_confirm(id)
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT item_vnum, item_count, price_points, description FROM srv1_hunabku.hunter_quest_shop WHERE id=" .. id)
    
    if c > 0 and d[1] then
        local vnum = tonumber(d[1].item_vnum)
        local count = tonumber(d[1].item_count)
        local price = tonumber(d[1].price_points)
        
        if price <= 0 then
            syschat("|cffFF0000[SECURITY]|r Errore: Prezzo oggetto non valido.")
            return
        end

        local title = hg_lib.get_text("shop_title") or "MERCANTE HUNTER"
        local ask = hg_lib.get_text("shop_ask") or "Vuoi acquistare questo oggetto?"
        local opt_confirm = hg_lib.get_text("shop_opt_confirm") or "Conferma Acquisto"
        local opt_cancel = hg_lib.get_text("shop_opt_cancel") or "Annulla"
            
        say_title(title)
        say(ask)
        say("")
        say_item_vnum(vnum)
        say("Quantita': |cff00FFFFx" .. count .. "|r") 
        say("Costo: |cffFFA500" .. price .. " Gloria Spendibile|r")
        
        if select(opt_confirm, opt_cancel) == 1 then
            local wc, wd = mysql_direct_query("SELECT spendable_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
            local wallet = 0
            if wc > 0 and wd[1] then wallet = tonumber(wd[1].spendable_points) or 0 end
            
            if wallet >= price then
                mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET spendable_points = spendable_points - " .. price .. " WHERE player_id=" .. pid)
                pc.give_item2(vnum, count)
                
                local msg = hg_lib.get_text("shop_success", {POINTS = price}) or ("TRANSAZIONE COMPLETATA. -" .. price .. " GLORIA")
                hg_lib.hunter_speak(msg)
                hg_lib.send_player_data()
            else
                local msg = hg_lib.get_text("shop_error_funds") or "ERRORE: GLORIA INSUFFICIENTE."
                hg_lib.hunter_speak(msg)
            end
        end
    else
        syschat("Oggetto non trovato.")
    end
end

function hg_lib.announce_daily_winners()
    local q = "SELECT player_name, daily_points FROM srv1_hunabku.hunter_quest_ranking WHERE daily_points > 0 ORDER BY daily_points DESC LIMIT 3"
    local c, d = mysql_direct_query(q)
    if c > 0 then
        local sep_daily = hg_lib.get_text("winners_sep_daily") or "|cffFFD700======================================|r"
        local title_daily = hg_lib.get_text("winners_title_daily") or "|cffFFD700[HUNTER SYSTEM]|r |cff00FFFF* VINCITORI CLASSIFICA GIORNALIERA *|r"
        notice_all("")
        notice_all(sep_daily)
        notice_all(title_daily)
        notice_all(sep_daily)
        for i = 1, c do
            local medal = ""
            local color = ""
            if i == 1 then medal = "[1]" color = "|cffFFD700" end
            if i == 2 then medal = "[2]" color = "|cffC0C0C0" end
            if i == 3 then medal = "[3]" color = "|cffCD7F32" end
            notice_all(medal .. " " .. color .. d[i].player_name .. "|r - |cffFFFFFF" .. d[i].daily_points .. " Gloria|r")
        end
        notice_all(sep_daily)
        notice_all("")
        local msg = "[HUNTER SYSTEM] Vincitori Gloria: "
        for i = 1, c do
            if i > 1 then msg = msg .. ", " end
            msg = msg .. d[i].player_name .. " (" .. d[i].daily_points .. ")"
        end
        hg_lib.hunter_speak(msg)
    end

    local qk = "SELECT player_name, daily_kills FROM srv1_hunabku.hunter_quest_ranking WHERE daily_kills > 0 ORDER BY daily_kills DESC LIMIT 3"
    local ck, dk = mysql_direct_query(qk)
    if ck > 0 then
        local sep_kill = hg_lib.get_text("winners_sep_kill") or "|cffFF8800======================================|r"
        local title_kill = hg_lib.get_text("winners_title_kill") or "|cffFF8800[HUNTER SYSTEM]|r |cffFF8800* VINCITORI CLASSIFICA KILL GIORNALIERA *|r"
        notice_all("")
        notice_all(sep_kill)
        notice_all(title_kill)
        notice_all(sep_kill)
        for i = 1, ck do
            local medal = ""
            local color = ""
            if i == 1 then medal = "[1]" color = "|cffFFD700" end
            if i == 2 then medal = "[2]" color = "|cffC0C0C0" end
            if i == 3 then medal = "[3]" color = "|cffCD7F32" end
            notice_all(medal .. " " .. color .. dk[i].player_name .. "|r - |cffFFFFFF" .. dk[i].daily_kills .. " Kill|r")
        end
        notice_all(sep_kill)
        notice_all("")
        local msgk = "[HUNTER SYSTEM] Vincitori Kill: "
        for i = 1, ck do
            if i > 1 then msgk = msgk .. ", " end
            msgk = msgk .. dk[i].player_name .. " (" .. dk[i].daily_kills .. ")"
        end
        hg_lib.hunter_speak(msgk)
    end
end

function hg_lib.announce_weekly_winners()
    local q = "SELECT player_name, weekly_points FROM srv1_hunabku.hunter_quest_ranking WHERE weekly_points > 0 ORDER BY weekly_points DESC LIMIT 3"
    local c, d = mysql_direct_query(q)
    if c > 0 then
        local sep_weekly = hg_lib.get_text("winners_sep_weekly") or "|cffFF6600======================================|r"
        local title_weekly = hg_lib.get_text("winners_title_weekly") or "|cffFF6600[HUNTER SYSTEM]|r |cffFFD700** VINCITORI CLASSIFICA SETTIMANALE **|r"
        notice_all("")
        notice_all(sep_weekly)
        notice_all(title_weekly)
        notice_all(sep_weekly)
        for i = 1, c do
            local medal = ""
            local color = ""
            if i == 1 then medal = "[1]" color = "|cffFFD700" end
            if i == 2 then medal = "[2]" color = "|cffC0C0C0" end
            if i == 3 then medal = "[3]" color = "|cffCD7F32" end
            notice_all(medal .. " " .. color .. d[i].player_name .. "|r - |cffFFFFFF" .. d[i].weekly_points .. " Gloria|r")
        end
        notice_all(sep_weekly)
        notice_all("")
    end
end

function hg_lib.process_daily_reset()
    -- STEP 1: Applica penalità per missioni NON completate del giorno precedente
    hg_lib.apply_mission_penalties()
    
    -- STEP 2: Assegna premi classifica
    hg_lib.assign_rank_prizes("daily")
    
    -- STEP 3: Resetta punti giornalieri
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET daily_points = 0, daily_kills = 0")
    
    local msg = hg_lib.get_text("reset_daily") or "|cffFFD700[HUNTER SYSTEM]|r Classifica Giornaliera Resettata! La corsa al potere ricomincia."
    notice_all(msg)
end

-- Applica penalità gloria per missioni non completate
function hg_lib.apply_mission_penalties()
    local yesterday = os.date("%Y-%m-%d", os.time() - 86400)
    
    -- Trova tutte le missioni 'active' (non completate) del giorno precedente
    local q = "SELECT pm.id, pm.player_id, pm.penalty_glory FROM srv1_hunabku.hunter_player_missions pm WHERE pm.assigned_date = '" .. yesterday .. "' AND pm.status = 'active'"
    local c, d = mysql_direct_query(q)
    
    if c > 0 then
        for i = 1, c do
            local mission = d[i]
            local player_id = tonumber(mission.player_id) or 0
            local penalty = tonumber(mission.penalty_glory) or 25
            
            if player_id > 0 and penalty > 0 then
                -- Sottrai penalità SOLO da total_points (non da spendable_points)
                -- Usa GREATEST per non andare sotto 0
                mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = GREATEST(0, total_points - " .. penalty .. ") WHERE player_id = " .. player_id)
                
                -- Marca la missione come 'failed'
                mysql_direct_query("UPDATE srv1_hunabku.hunter_player_missions SET status = 'failed' WHERE id = " .. mission.id)
            end
        end
    end
end

function hg_lib.process_weekly_reset()
    hg_lib.assign_rank_prizes("weekly")
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET weekly_points = 0, weekly_kills = 0")
    local msg = hg_lib.get_text("reset_weekly") or "|cffFF6600[HUNTER SYSTEM]|r Classifica Settimanale Resettata! I premi sono stati distribuiti."
    notice_all(msg)
end

function hg_lib.assign_rank_prizes(rtype)
    local col = rtype == "weekly" and "weekly_points" or "daily_points"
    local pcol = rtype == "weekly" and "pending_weekly_reward" or "pending_daily_reward"
    local q = "SELECT player_id FROM srv1_hunabku.hunter_quest_ranking WHERE " .. col .. " > 0 ORDER BY " .. col .. " DESC LIMIT 3"
    local c, d = mysql_direct_query(q)
    if c > 0 then
        for i=1,c do 
            mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET " .. pcol .. " = " .. i .. " WHERE player_id = " .. d[i].player_id) 
        end
    end
end

function hg_lib.assign_daily_missions()
    local pid = pc.get_player_id()
    local pname = pc.get_name()
    local today = hg_lib.get_today_date()
        
    local last_assign_day = pc.getqf("hq_last_assign_day") or 0
    local current_day = tonumber(os.date("%j")) or 0
    
    -- FIX: Conta TUTTE le missioni di oggi (active + completed), non solo active!
    -- Altrimenti quando ne completi una, il sistema pensa di doverle riassegnare
    if last_assign_day == current_day then
        local c, d = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
        if c > 0 and tonumber(d[1].cnt) >= 3 then
            -- Missioni gia assegnate oggi, invia i dati al client
            hg_lib.send_daily_missions()
            return false
        end
    end
    
    -- FIX: Stessa correzione qui - conta TUTTE le missioni, non solo active
    local c, d = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
    if c > 0 and tonumber(d[1].cnt) >= 3 then
        pc.setqf("hq_last_assign_day", current_day)
        -- Missioni gia presenti, invia i dati al client
        hg_lib.send_daily_missions()
        return false
    end
        
    pc.setqf("hq_last_assign_day", current_day)
        
    local rc, rd = mysql_direct_query("SELECT total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
    local pts = 0
    if rc > 0 and rd[1] then pts = tonumber(rd[1].total_points) or 0 end
    local rank_idx = hg_lib.get_rank_index(pts)
    local rank_letter = hg_lib.get_rank_letter(rank_idx)

    -- SECURITY FIX: Escape player name to prevent SQL injection
    local safe_pname = mysql_escape_string(pname)
    mysql_direct_query("CALL srv1_hunabku.sp_assign_daily_missions(" .. pid .. ", '" .. rank_letter .. "', '" .. safe_pname .. "')")
        
    local vc, vd = mysql_direct_query("SELECT COUNT(*) as cnt FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "' AND status='active'")
    local inserted_count = 0
    if vc > 0 and vd[1] then inserted_count = tonumber(vd[1].cnt) or 0 end
        
    if inserted_count >= 3 then
        hg_lib.send_daily_missions()
        timer("hq_missions_notify", 6)
        return true
    else
        syschat("|cffFF0000[HUNTER ERROR] Impossibile assegnare missioni. Contatta un GM.|r")
        return false
    end
end

function hg_lib.send_daily_missions()
    local pid = pc.get_player_id()
    local today = hg_lib.get_today_date()
    local q = "SELECT pm.id, pm.mission_slot, md.mission_name, md.mission_type, pm.current_progress, pm.target_count, pm.status, pm.reward_glory, pm.penalty_glory, md.time_limit_minutes FROM srv1_hunabku.hunter_player_missions pm LEFT JOIN srv1_hunabku.hunter_mission_definitions md ON pm.mission_def_id = md.mission_id WHERE pm.player_id=" .. pid .. " AND pm.assigned_date='" .. today .. "' ORDER BY pm.mission_slot"
    local c, d = mysql_direct_query(q)
        
    cmdchat("HunterMissionsCount " .. c)
        
    if c > 0 then
        for i = 1, c do
            local m = d[i]
            local remaining = 0
            local time_limit = tonumber(m.time_limit_minutes) or 0
            if time_limit > 0 then
                remaining = time_limit * 60
            end
            local pkt = tostring(tonumber(m.id) or 0) .. "|" ..
                hg_lib.clean_str(m.mission_name or "Missione") .. "|" ..
                (m.mission_type or "kill_mob") .. "|" ..
                tostring(tonumber(m.current_progress) or 0) .. "|" ..
                tostring(tonumber(m.target_count) or 10) .. "|" ..
                tostring(tonumber(m.reward_glory) or 50) .. "|" ..
                tostring(tonumber(m.penalty_glory) or 25) .. "|" ..
                (m.status or "active")
            cmdchat("HunterMissionData " .. pkt)
        end
    end
end

-- ============================================================
-- FUNZIONE INTERNA: Processa il buffer missioni per un player
-- OTTIMIZZATO: Logica centralizzata (era duplicata in 2 funzioni)
-- ============================================================
function hg_lib._process_mission_buffer_internal(pid)
    _G.hunter_mission_buffer = _G.hunter_mission_buffer or {}
    local player_buffer = _G.hunter_mission_buffer[pid]
    if not player_buffer or next(player_buffer) == nil then
        return -- Buffer vuoto, niente da fare
    end

    -- FLUSH: Processa tutte le missioni attive del player
    local q = "SELECT pm.id, pm.current_progress, pm.target_count, pm.reward_glory, md.mission_name, md.target_vnum, md.mission_type FROM srv1_hunabku.hunter_player_missions pm LEFT JOIN srv1_hunabku.hunter_mission_definitions md ON pm.mission_def_id = md.mission_id WHERE pm.player_id=" .. pid .. " AND pm.assigned_date=CURDATE() AND pm.status='active'"
    local c, d = mysql_direct_query(q)

    if c > 0 then
        for i = 1, c do
            local m = d[i]
            local mid = tonumber(m.id)
            local cur = tonumber(m.current_progress) or 0
            local target_count = tonumber(m.target_count) or 10
            local m_type = m.mission_type or "kill_mob"
            local m_target = tonumber(m.target_vnum) or 0

            -- Trova il progresso nel buffer per questa missione
            local progress_to_add = 0
            local check_key = m_type .. "_" .. m_target

            if player_buffer[check_key] and player_buffer[check_key] > 0 then
                progress_to_add = player_buffer[check_key]
            end

            if progress_to_add > 0 then
                local new_progress = math.min(cur + progress_to_add, target_count)

                -- Aggiorna solo se c'è effettivamente progresso
                if new_progress > cur then
                    mysql_direct_query("UPDATE srv1_hunabku.hunter_player_missions SET current_progress=" .. new_progress .. " WHERE id=" .. mid)
                    cmdchat("HunterMissionProgress " .. mid .. "|" .. new_progress .. "|" .. target_count)

                    if new_progress >= target_count then
                        hg_lib.complete_mission(mid)
                    end
                end
            end
        end
    end

    -- Svuota il buffer del player dopo il flush
    _G.hunter_mission_buffer[pid] = {}
end

function hg_lib.update_mission_progress(mission_type, amount, target_vnum)
    local pid = pc.get_player_id()
    target_vnum = target_vnum or 0

    -- PERFORMANCE: Throttle mission updates - max 1 flush ogni 1 secondo per player
    local now = get_time()
    local throttle_key = pid .. "_mission_flush"
    _G.hunter_mission_throttle = _G.hunter_mission_throttle or {}
    local last_flush = _G.hunter_mission_throttle[throttle_key] or 0

    -- SEMPRE accumula nel buffer (fix: accumula TUTTE le kill)
    _G.hunter_mission_buffer = _G.hunter_mission_buffer or {}
    _G.hunter_mission_buffer[pid] = _G.hunter_mission_buffer[pid] or {}
    local player_buffer = _G.hunter_mission_buffer[pid]

    -- Accumula per tipo + vnum specifico
    local buffer_key = mission_type .. "_" .. target_vnum
    player_buffer[buffer_key] = (player_buffer[buffer_key] or 0) + amount

    -- Accumula anche per missioni generiche (target_vnum = 0)
    if target_vnum > 0 then
        local generic_key = mission_type .. "_0"
        player_buffer[generic_key] = (player_buffer[generic_key] or 0) + amount
    end

    -- Se non è passato abbastanza tempo, esci (il buffer verrà processato dopo)
    if now - last_flush < 1 then
        return
    end
    _G.hunter_mission_throttle[throttle_key] = now

    -- USA FUNZIONE CENTRALIZZATA
    hg_lib._process_mission_buffer_internal(pid)
end

-- Funzione separata per forzare il flush del buffer missioni (bypassa throttle)
function hg_lib.flush_mission_buffer(pid)
    pid = pid or pc.get_player_id()

    -- USA FUNZIONE CENTRALIZZATA
    hg_lib._process_mission_buffer_internal(pid)

    -- Aggiorna timestamp throttle
    _G.hunter_mission_throttle = _G.hunter_mission_throttle or {}
    _G.hunter_mission_throttle[pid .. "_mission_flush"] = get_time()
end

function hg_lib.complete_mission(mission_id)
    local pid = pc.get_player_id()
    local today = hg_lib.get_today_date()
    local c, d = mysql_direct_query("SELECT pm.reward_glory, pm.status, md.mission_name FROM srv1_hunabku.hunter_player_missions pm LEFT JOIN srv1_hunabku.hunter_mission_definitions md ON pm.mission_def_id = md.mission_id WHERE pm.id=" .. mission_id .. " AND pm.player_id=" .. pid)
    if c == 0 or d[1].status ~= "active" then return end
        
    local reward = tonumber(d[1].reward_glory) or 50
    local name = d[1].mission_name or "Missione"
        
    mysql_direct_query("UPDATE srv1_hunabku.hunter_player_missions SET status='completed', completed_at=NOW() WHERE id=" .. mission_id)
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + " .. reward .. ", spendable_points = spendable_points + " .. reward .. ", daily_points = daily_points + " .. reward .. ", weekly_points = weekly_points + " .. reward .. " WHERE player_id=" .. pid)
        
    local cc, cd = mysql_direct_query("SELECT COUNT(*) as completed FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "' AND status='completed'")
    local completed_count = 1
    if cc > 0 and cd[1] then completed_count = tonumber(cd[1].completed) or 1 end
        
    syschat("|cff00FF00========================================|r")
    syschat("|cff00FF00  [" .. hg_lib.get_text("MISSION_COMPLETED", nil, "MISSIONE COMPLETATA") .. "]|r |cffFFFFFF" .. name .. "|r")
    syschat("|cffFFD700  +" .. reward .. " " .. hg_lib.get_text("GLORY", nil, "Gloria") .. "!|r |cffAAAAAA(" .. completed_count .. "/3 " .. hg_lib.get_text("COMPLETE", nil, "complete") .. ")|r")
    syschat("|cff00FF00========================================|r")

    local speak_msg = hg_lib.get_text("MISSION_COMPLETE_SPEAK", {REWARD = reward}, "MISSIONE COMPLETATA! +" .. reward .. " GLORIA")
    hg_lib.hunter_speak(speak_msg)
    cmdchat("HunterMissionComplete " .. mission_id .. "|" .. hg_lib.clean_str(name) .. "|" .. reward)
        
    hg_lib.check_all_missions_complete()
    hg_lib.send_player_data()
end

function hg_lib.check_all_missions_complete()
    local pid = pc.get_player_id()
    local today = hg_lib.get_today_date()
    local today_num = tonumber(os.date("%j")) or 0  -- Giorno dell'anno come numero
    local c, d = mysql_direct_query("SELECT COUNT(*) as total, SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
        
    if c > 0 and d[1] then
        local total = tonumber(d[1].total) or 0
        local completed = tonumber(d[1].completed) or 0
            
        if total >= 3 and completed >= 3 then
            -- Controlla se il bonus è già stato dato oggi (evita duplicati)
            local already_claimed = pc.getqf("hq_daily_bonus_claimed") or 0
            if already_claimed == today_num then
                return -- Bonus già riscosso oggi
            end
            pc.setqf("hq_daily_bonus_claimed", today_num)
            
            -- === ATTIVA BONUS FRATTURE ===
            hg_lib.activate_fracture_bonus()
            -- =============================
            
            -- Recupera i dettagli delle singole missioni
            local sc, sd = mysql_direct_query("SELECT mission_def_id, reward_glory FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "' AND status='completed' ORDER BY id")
            if sc > 0 then
                local total_glory = 0
                local mission_details = {}
                
                for i = 1, sc do
                    local glory = tonumber(sd[i].reward_glory) or 0
                    total_glory = total_glory + glory
                    table.insert(mission_details, glory)
                end
                
                local bonus = math.floor(total_glory * 0.5)
                
                if bonus > 0 then
                    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + " .. bonus .. ", spendable_points = spendable_points + " .. bonus .. " WHERE player_id=" .. pid)
                    
                    -- === SYSCHAT DETTAGLIATO BONUS MISSIONI ===
                    local glory_label = hg_lib.get_text("GLORY", nil, "Gloria")
                    local mission_label = hg_lib.get_text("MISSION", nil, "Missione")
                    syschat("|cffFFD700=============================================|r")
                    syschat("|cffFFD700  [!!!] " .. hg_lib.get_text("ALL_MISSIONS_COMPLETE", nil, "TUTTE LE MISSIONI COMPLETE!") .. " [!!!]|r")
                    syschat("|cffFFD700=============================================|r")
                    syschat("")
                    syschat("|cff00FFFF  " .. hg_lib.get_text("GLORY_FROM_MISSIONS", nil, "Gloria dalle Missioni:") .. "|r")
                    for idx, glory in ipairs(mission_details) do
                        syschat("|cffFFFFFF    " .. mission_label .. " " .. idx .. ": +" .. glory .. " " .. glory_label .. "|r")
                    end
                    syschat("|cff00FF00  ────────────────────────────────|r")
                    syschat("|cffFFFFFF  " .. hg_lib.get_text("TOTAL_MISSIONS", nil, "Totale Missioni") .. ": |r|cff00FF00+" .. total_glory .. " " .. glory_label .. "|r")
                    syschat("")
                    syschat("|cffFFD700  [" .. hg_lib.get_text("BONUS_50_COMPLETION", nil, "BONUS 50% COMPLETAMENTO") .. "]|r")
                    syschat("|cffFFD700    +" .. bonus .. " " .. hg_lib.get_text("GLORY_EXTRA", nil, "Gloria Extra") .. "!|r")
                    syschat("")
                    syschat("|cff00FF00  >>> " .. hg_lib.get_text("TOTAL_EARNED", nil, "TOTALE GUADAGNATO") .. ": +" .. (total_glory + bonus) .. " " .. glory_label .. " <<<|r")
                    syschat("")
                    syschat("|cffFF6600  [" .. hg_lib.get_text("ACTIVATED", nil, "ATTIVATO") .. "] " .. hg_lib.get_text("FRACTURE_BONUS", nil, "Bonus Fratture +50%") .. "|r")
                    syschat("|cffAAAAAA  (" .. hg_lib.get_text("VALID_UNTIL_RESET", nil, "valido fino al reset di mezzanotte") .. ")|r")
                    syschat("|cffFFD700=============================================|r")
                    -- ============================================
                    
                    local msg = hg_lib.get_text("mission_all_complete") or "TUTTE LE MISSIONI COMPLETE! BONUS x1.5!"
                    hg_lib.hunter_speak_color(msg, "GOLD")
                    
                    cmdchat("HunterAllMissionsComplete " .. bonus .. "|FRACTURE_BONUS_ACTIVE")
                end
            end
        end
    end
end

-- Funzione per attivare il bonus fratture
function hg_lib.activate_fracture_bonus()
    local pid = pc.get_player_id()
    -- Usa il giorno dell'anno (1-366) come numero intero invece di stringa
    local day_of_year = tonumber(os.date("%j")) or 0
    pc.setqf("hq_fracture_bonus_active", 1)
    pc.setqf("hq_fracture_bonus_day", day_of_year)
end

-- Funzione per controllare se il bonus fratture è ancora attivo
function hg_lib.has_fracture_bonus()
    local pid = pc.get_player_id()
    local today_num = tonumber(os.date("%j")) or 0
    local bonus_active = pc.getqf("hq_fracture_bonus_active") or 0
    local bonus_day = pc.getqf("hq_fracture_bonus_day") or 0
    
    -- Il bonus scade al reset delle missioni (nuovo giorno)
    if bonus_active == 1 and bonus_day == today_num then
        return true
    else
        -- Resetta il bonus se è il giorno dopo
        pc.setqf("hq_fracture_bonus_active", 0)
        return false
    end
end

function hg_lib.on_mob_kill(mob_vnum)
    local pid = pc.get_player_id()
    local mob_info = hg_lib.get_mob_info(mob_vnum)

    -- FIX: Accumula TUTTI i tipi nel buffer PRIMA del flush
    -- Questo evita che il throttle blocchi gli altri tipi
    _G.hunter_mission_buffer = _G.hunter_mission_buffer or {}
    _G.hunter_mission_buffer[pid] = _G.hunter_mission_buffer[pid] or {}
    local player_buffer = _G.hunter_mission_buffer[pid]
    
    -- Accumula per kill_mob (sempre)
    local key_mob = "kill_mob_" .. mob_vnum
    local key_mob_generic = "kill_mob_0"
    player_buffer[key_mob] = (player_buffer[key_mob] or 0) + 1
    player_buffer[key_mob_generic] = (player_buffer[key_mob_generic] or 0) + 1
    
    -- Accumula per kill_boss (sempre - sara' la missione a filtrare per target_vnum)
    local key_boss = "kill_boss_" .. mob_vnum
    local key_boss_generic = "kill_boss_0"
    player_buffer[key_boss] = (player_buffer[key_boss] or 0) + 1
    player_buffer[key_boss_generic] = (player_buffer[key_boss_generic] or 0) + 1
    
    -- Accumula per kill_metin (sempre - sara' la missione a filtrare per target_vnum)
    local key_metin = "kill_metin_" .. mob_vnum
    local key_metin_generic = "kill_metin_0"
    player_buffer[key_metin] = (player_buffer[key_metin] or 0) + 1
    player_buffer[key_metin_generic] = (player_buffer[key_metin_generic] or 0) + 1
    
    -- ORA fai il flush (una sola volta, con tutti i dati nel buffer)
    hg_lib.flush_mission_buffer(pid)

    -- PERFORMANCE FIX: Trial completion check rimosso da qui (troppo spam)
    -- Ora controllato solo dal timer da 5 minuti o al completamento effettivo
end

function hg_lib.check_trial_completion_status()
    local pid = pc.get_player_id()
    
    -- IMPORTANTE: Prima flush i trial pendenti per avere dati aggiornati
    -- Necessario per rilevare completamento in tempo reale
    local boss_kills = pc.getqf("hq_trial_boss_kill") or 0
    local metin_kills = pc.getqf("hq_trial_metin_kill") or 0
    local chest_opens = pc.getqf("hq_trial_chest_open") or 0
    local fracture_seals = pc.getqf("hq_trial_fracture_seal") or 0
    
    -- Se ci sono valori pendenti, flush prima del check
    if boss_kills > 0 or metin_kills > 0 or chest_opens > 0 or fracture_seals > 0 then
        local flush_q = string.format([[
            UPDATE srv1_hunabku.hunter_player_trials 
            SET boss_kills = boss_kills + %d,
                metin_kills = metin_kills + %d,
                chest_opens = chest_opens + %d,
                fracture_seals = fracture_seals + %d
            WHERE player_id = %d AND status = 'in_progress'
        ]], boss_kills, metin_kills, chest_opens, fracture_seals, pid)
        mysql_direct_query(flush_q)
        
        -- Reset accumulatori
        pc.setqf("hq_trial_boss_kill", 0)
        pc.setqf("hq_trial_metin_kill", 0)
        pc.setqf("hq_trial_chest_open", 0)
        pc.setqf("hq_trial_fracture_seal", 0)
    end
    
    -- Chiama la procedura che verifica se i requisiti sono soddisfatti
    -- Restituisce: completed (1/0), new_rank, reward, title
    local q = "CALL srv1_hunabku.sp_check_trial_complete(" .. pid .. ", @completed, @new_rank, @reward, @title)"
    mysql_direct_query(q)
    local c, d = mysql_direct_query("SELECT @completed as res, @new_rank as nr, @reward as rw, @title as tt")
    
    if c > 0 and d[1] and tonumber(d[1].res) == 1 then
        local new_rank = d[1].nr
        local reward = tonumber(d[1].rw) or 0
        local title = d[1].tt or ""
        
        -- Effetto sonoro/visivo
        cmdchat("HunterTrialComplete " .. new_rank .. "|" .. reward .. "|Rank+Up")
        
        -- Messaggio in chat
        local trial_complete_msg = hg_lib.get_text("TRIAL_COMPLETE_RANK", {RANK = new_rank}, "PROVA COMPLETATA! Sei stato promosso al rango " .. new_rank .. "!")
        local trial_reward_msg = hg_lib.get_text("TRIAL_REWARD", {REWARD = reward}, "Ricompensa: +" .. reward .. " Gloria")
        syschat("|cffFFD700[HUNTER SYSTEM]|r " .. trial_complete_msg)
        syschat("|cffFFD700[HUNTER SYSTEM]|r " .. trial_reward_msg)
        
        -- Aggiorna il rank in memoria del client
        local rank_idx = hg_lib.get_rank_index_by_letter(new_rank)
        pc.setqf("hq_rank_num", rank_idx)
        
        -- Aggiorna interfaccia
        hg_lib.send_player_data()
    end
end

function hg_lib.on_boss_kill(boss_vnum)
    local pid = pc.get_player_id()
    -- Aggiorna missioni giornaliere
    hg_lib.update_mission_progress("kill_boss", 1, boss_vnum)
    -- PERFORMANCE: Accumula Trial progress invece di query immediata
    hg_lib.add_trial_progress("boss_kill", 1)

    -- DETAILED STATS: Accumula boss per difficoltà (pending flush)
    local mob_info = hg_lib.get_mob_info(boss_vnum)
    if mob_info then
        local base_points = mob_info.base_points or 0
        local difficulty_key = "hq_pending_boss_easy"  -- Default
        if base_points > 5000 then
            difficulty_key = "hq_pending_boss_elite"
        elseif base_points > 1500 then
            difficulty_key = "hq_pending_boss_hard"
        elseif base_points > 500 then
            difficulty_key = "hq_pending_boss_medium"
        end
        pc.setqf(difficulty_key, (pc.getqf(difficulty_key) or 0) + 1)
    end

    -- CHECK: Se evento "first_boss" attivo, il PRIMO a uccidere vince!
    hg_lib.check_first_boss_winner(boss_vnum)
end

function hg_lib.on_metin_kill(metin_vnum)
    local pid = pc.get_player_id()
    -- Aggiorna missioni giornaliere
    hg_lib.update_mission_progress("kill_metin", 1, metin_vnum)
    -- PERFORMANCE: Accumula Trial progress invece di query immediata
    hg_lib.add_trial_progress("metin_kill", 1)

    -- DETAILED STATS: Accumula metin per tipo (pending flush)
    local mob_info = hg_lib.get_mob_info(metin_vnum)
    if mob_info then
        local base_points = mob_info.base_points or 0
        local metin_key = base_points > 1000 and "hq_pending_metin_special" or "hq_pending_metin_normal"
        pc.setqf(metin_key, (pc.getqf(metin_key) or 0) + 1)
    end
end

function hg_lib.on_fracture_seal()
    local pid = pc.get_player_id()
    local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0

    -- Security Log: Fracture sealed
    local frank = "E"
    if hunter_defense_data and hunter_defense_data[pid] then
        frank = hunter_defense_data[pid].rank or "E"
    end
    hg_lib.log_fracture_seal(fracture_vid, frank, 0)

    -- 1. Aggiorna Missioni Giornaliere per il giocatore corrente
    hg_lib.update_mission_progress("seal_fracture", 1, 0)
    hg_lib.add_trial_progress("fracture_seal", 1)

    -- 2. Aggiorna Missioni anche per tutti i membri del party
    if party.is_party() then
        local pids = {party.get_member_pids()}
        for i, member_pid in ipairs(pids) do
            if member_pid ~= pid then
                q.begin_other_pc_block(member_pid)
                hg_lib.update_mission_progress("seal_fracture", 1, 0)
                hg_lib.add_trial_progress("fracture_seal", 1)
                q.end_other_pc_block()
            end
        end
    end

    -- 3. Controlla se la prova è stata completata con questa azione
    hg_lib.check_trial_completion_status()

    -- 4. Registra partecipazione automatica all'evento (se attivo)
    hg_lib.register_event_participant()
end

function hg_lib.check_missions_reminder()
    local pid = pc.get_player_id()
    local today = hg_lib.get_today_date()
    local ts = get_time()
    local current_hour = hg_lib.get_hour_from_ts(ts)
        
    if current_hour < 22 then return end
        
    local last_reminder = pc.getqf("hq_last_reminder_hour") or 0
    if last_reminder == current_hour then return end
        
    local c, d = mysql_direct_query("SELECT COUNT(*) as total, SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pid .. " AND assigned_date='" .. today .. "'")
        
    if c > 0 and d[1] then
        local total = tonumber(d[1].total) or 0
        local completed = tonumber(d[1].completed) or 0
        local incomplete = total - completed
            
        if incomplete > 0 and total >= 3 then
            pc.setqf("hq_last_reminder_hour", current_hour)
            local hours_left = 24 - current_hour
            local warning_msg = hg_lib.get_text("WARNING_INCOMPLETE_MISSIONS", {COUNT = incomplete}, "Hai " .. incomplete .. " missioni incomplete!")
            local reset_msg = hg_lib.get_text("RESET_IN_HOURS", {HOURS = hours_left}, "Reset tra " .. hours_left .. " ore")
            local penalty_msg = hg_lib.get_text("COMPLETE_TO_AVOID_PENALTY", nil, "Completa per evitare penalita'!")
            syschat("|cffFF4444========================================|r")
            syschat("|cffFF0000  [" .. hg_lib.get_text("WARNING", nil, "ATTENZIONE") .. "]|r |cffFFFFFF" .. warning_msg .. "|r")
            syschat("|cffFFAA00  " .. reset_msg .. "|r |cffFF4444- " .. penalty_msg .. "|r")
            syschat("|cffFF4444========================================|r")
        end
    end
end

function hg_lib.send_today_events(openWindow)
    local t = os.date("*t")
    local wday = t.wday - 1
    local day_db = wday
    if wday == 0 then day_db = 7 end
        
    local current_hour = t.hour
    local current_minute = t.min
    local current_total = current_hour * 60 + current_minute
        
    local q = "SELECT id, event_name, event_type, event_desc, start_hour, start_minute, duration_minutes, min_rank, reward_glory_base, reward_glory_winner, color_scheme, glory_multiplier FROM srv1_hunabku.hunter_scheduled_events WHERE enabled=1 AND FIND_IN_SET(" .. day_db .. ", days_active) > 0 ORDER BY start_hour, start_minute"
    local c, d = mysql_direct_query(q)
    local BATCH_SIZE = 5
    local events_sent = 0
        
    cmdchat("HunterEventsCount " .. c)
        
    if c > 0 then
        local batch = ""
        for i = 1, c do
            local e = d[i]
            local start_hour = tonumber(e.start_hour) or 0
            local start_minute = tonumber(e.start_minute) or 0
            local duration = tonumber(e.duration_minutes) or 30
            local start_total = start_hour * 60 + start_minute
            local end_total = start_total + duration
            local end_hour = math.floor(end_total / 60)
            local end_minute = hg_lib.modulo(end_total, 60)
            
            if end_hour >= 24 then end_hour = end_hour - 24 end
                
            local status = "upcoming"
            if current_total >= start_total and current_total < end_total then
                status = "active"
            elseif current_total >= end_total then
                status = "ended"
            end
                
            local start_time = hg_lib.format_time(start_hour, start_minute)
            local end_time = hg_lib.format_time(end_hour, end_minute)
            local reward_str = "+" .. (e.reward_glory_base or 50) .. "+Gloria"
            local winner_prize = tonumber(e.reward_glory_winner) or 200
                
            local pkt = tostring(tonumber(e.id) or 0) .. "~" ..
                hg_lib.clean_str(e.event_name or "Evento") .. "~" ..
                start_time .. "~" ..
                end_time .. "~" ..
                (e.event_type or "glory_rush") .. "~" ..
                reward_str .. "~" ..
                status .. "~" ..
                (e.min_rank or "E") .. "~" ..
                winner_prize
                
            if batch ~= "" then batch = batch .. ";" end
            batch = batch .. pkt
            events_sent = events_sent + 1
                
            if events_sent >= BATCH_SIZE or i == c then
                cmdchat("HunterEventBatch " .. batch)
                batch = ""
                events_sent = 0
            end
        end
    end
        
    if openWindow then
        cmdchat("HunterEventsOpen")
    end
end

function hg_lib.check_active_event_notify()
    local event = hg_lib.get_current_scheduled_event()
    if event then
        local event_id = tonumber(event.id)
        local name = event.event_name or "Evento"
        local etype = event.event_type or "glory_rush"
        local desc = event.event_desc or ""
        local reward = tonumber(event.reward_glory_base) or 50
        local winner_reward = tonumber(event.reward_glory_winner) or 200
        local color = event.color_scheme or "GOLD"
        local duration = tonumber(event.duration_minutes) or 30

        local ts = get_time()
        local current_hour = hg_lib.get_hour_from_ts(ts)
        local current_minute = hg_lib.get_min_from_ts(ts)
        local current_total = current_hour * 60 + current_minute
        local start_total = tonumber(event.start_hour) * 60 + tonumber(event.start_minute)
        local end_total = start_total + duration
        local remaining = end_total - current_total

        -- Controlla se già registrato
        local pid = pc.get_player_id()
        local today = os.date("%Y-%m-%d")
        local check_q = string.format(
            "SELECT id FROM srv1_hunabku.hunter_event_participants WHERE event_id=%d AND player_id=%d AND DATE(joined_at)='%s'",
            event_id, pid, today
        )
        local c = mysql_direct_query(check_q)
        local is_registered = (c > 0) and 1 or 0

        pc.setqf("hq_event_reward", reward)
        pc.setqf("hq_event_remaining", remaining)
        pc.setqf("hq_event_winner", winner_reward)
        pc.setqf("hq_event_registered", is_registered)

        timer("hq_event_notify", 8)
        cmdchat("HunterEventStatus " .. hg_lib.clean_str(name) .. "|" .. remaining * 60 .. "|" .. etype)
    else
        -- Nessun evento attivo, resetta il flag
        pc.setqf("hq_event_registered", 0)
    end
end

function hg_lib.join_event(event_id)
    local pid = pc.get_player_id()
    local c, d = mysql_direct_query("SELECT event_name, event_type, reward_glory_base, reward_glory_winner, min_rank, color_scheme FROM srv1_hunabku.hunter_scheduled_events WHERE id=" .. event_id)
    if c == 0 then
        hg_lib.hunter_speak("Evento non trovato.")
        return
    end
        
    local event_name = d[1].event_name or "Evento"
    local event_type = d[1].event_type or "glory_rush"
    local glory_base = tonumber(d[1].reward_glory_base) or 50
    local glory_winner = tonumber(d[1].reward_glory_winner) or 200
    local min_rank = d[1].min_rank or "E"
    local color = d[1].color_scheme or "GOLD"
        
    local rc, rd = mysql_direct_query("SELECT total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
    local pts = 0
    if rc > 0 and rd[1] then pts = tonumber(rd[1].total_points) or 0 end
    local player_rank_num = hg_lib.get_rank_index(pts)
    local required_rank_num = hg_lib.get_rank_index_by_letter(min_rank)
        
    if player_rank_num < required_rank_num then
        hg_lib.hunter_speak_color("Rank insufficiente! Richiesto: " .. min_rank .. "-Rank", "RED")
        return
    end
        
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points = total_points + " .. glory_base .. ", spendable_points = spendable_points + " .. glory_base .. ", daily_points = daily_points + " .. glory_base .. ", weekly_points = weekly_points + " .. glory_base .. " WHERE player_id=" .. pid)
    
    -- === SYSCHAT DETTAGLIATO PARTECIPAZIONE EVENTO ===
    syschat("|cffFFAA00========================================|r")
    syschat("|cffFFAA00  [ISCRIZIONE EVENTO]|r |cffFFFFFF" .. event_name .. "|r")
    syschat("|cffFFAA00========================================|r")
    syschat("")
    syschat("|cff00FFFF  Gloria Partecipazione:|r |cffFFFFFF+" .. glory_base .. "|r")
    if event_type == "first_rift" or event_type == "first_boss" then
        syschat("|cffFFD700  Premio 1° Classificato:|r |cffFF6600+" .. glory_winner .. " Gloria!|r")
    elseif event_type == "glory_rush" then
        syschat("|cffFF6600  [BONUS ATTIVO] Gloria aumentata durante evento!|r")
    end
    syschat("")
    syschat("|cff00FF00  >>> TOTALE: +" .. glory_base .. " Gloria <<<|r")
    syschat("|cffFFAA00========================================|r")
    -- ==================================================
        
    local msg = "Partecipi a " .. event_name .. "! +" .. glory_base .. " Gloria"
    if event_type == "first_rift" or event_type == "first_boss" then
        msg = msg .. " (Se arrivi PRIMO: +" .. glory_winner .. "!)"
    elseif event_type == "glory_rush" then
        msg = msg .. " (Bonus Gloria ATTIVO!)"
    end
        
    hg_lib.hunter_speak_color(msg, color)
    cmdchat("HunterEventJoined " .. event_id .. "|" .. hg_lib.clean_str(event_name) .. "|" .. glory_base)
        
    hg_lib.send_player_data()
end

-- ============================================================
-- SHOP SYSTEM
-- ============================================================
function hg_lib.shop_buy_item(item_id)
    local pid = pc.get_player_id()
    
    -- Prendi info item dallo shop (usa hunter_quest_shop esistente)
    local q = "SELECT description, price_points, item_vnum, item_count FROM srv1_hunabku.hunter_quest_shop WHERE id=" .. item_id .. " AND enabled=1"
    local c, d = mysql_direct_query(q)
    
    if c == 0 then
        hg_lib.syschat_t("SHOP_NOT_AVAILABLE", "Oggetto non disponibile.", nil, "FF0000")
        return
    end

    local item_name = d[1].description or "Item"
    local price = tonumber(d[1].price_points) or 0
    local item_vnum = tonumber(d[1].item_vnum) or 0
    local item_count = tonumber(d[1].item_count) or 1

    -- Controlla gloria spendibile
    local rc, rd = mysql_direct_query("SELECT spendable_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
    if rc == 0 then
        hg_lib.syschat_t("SHOP_NOT_HUNTER", "Non sei un Hunter!", nil, "FF0000")
        return
    end

    local spendable = tonumber(rd[1].spendable_points) or 0

    -- Controlla gloria spendibile
    if spendable < price then
        syschat("|cffFF0000[SHOP]|r " .. hg_lib.get_text("SHOP_INSUFFICIENT", {HAVE = spendable, NEED = price}, "Gloria insufficiente! Hai " .. spendable .. ", serve " .. price))
        return
    end

    -- ANTI-EXPLOIT: Lock per prevenire double-click
    local lock_key = "hq_shop_lock"
    if pc.getqf(lock_key) == 1 then
        syschat("|cffFF6600[SHOP]|r Attendi qualche secondo...")
        return
    end
    pc.setqf(lock_key, 1)

    -- Controlla inventario
    if pc.count_empty_inventory(0) < 1 then
        pc.setqf(lock_key, 0)
        hg_lib.syschat_t("SHOP_INV_FULL", "Inventario pieno!", nil, "FF0000")
        return
    end

    -- CRITICAL FIX: Dai item PRIMA di sottrarre punti (atomic operation)
    -- Se give_item2 fallisce, non sottraiamo punti
    local success = pc.give_item2(item_vnum, item_count)

    if not success or success == 0 then
        pc.setqf(lock_key, 0)
        syschat("|cffFF0000[SHOP]|r Errore durante la consegna. Contatta un GM.")
        hg_lib.log_error("SHOP", "give_item2 failed", "item_id=" .. item_id .. " vnum=" .. item_vnum)
        return
    end

    -- Item dato con successo, ora sottrai punti
    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET spendable_points = spendable_points - " .. price .. " WHERE player_id=" .. pid)

    -- LOG TRANSAZIONE (AUDIT TRAIL)
    local pname = mysql_escape_string(pc.get_name())
    mysql_direct_query(string.format(
        "INSERT INTO srv1_hunabku.hunter_shop_purchases (player_id, player_name, item_id, item_vnum, item_count, price_paid, purchased_at) VALUES (%d, '%s', %d, %d, %d, %d, NOW())",
        pid, pname, item_id, item_vnum, item_count, price
    ))

    syschat("|cff00FF00[SHOP]|r " .. hg_lib.get_text("SHOP_PURCHASED", {ITEM = item_name, COUNT = item_count}, "Acquistato: " .. item_name .. " x" .. item_count))
    syschat("|cffFFD700[SHOP]|r -" .. price .. " " .. hg_lib.get_text("SPENDABLE_GLORY", nil, "Gloria Spendibile"))

    -- Rilascia lock dopo 2 secondi
    timer("hq_shop_unlock", 2, "pc.setqf('hq_shop_lock', 0)")
    
    -- Aggiorna UI
    hg_lib.send_player_data()
end

-- ============================================================
-- ACHIEVEMENTS SYSTEM
-- ============================================================
function hg_lib.get_player_achievements(pid)
    -- Prendi configurazione achievements
    local cq = "SELECT id, name, type, requirement, reward_vnum, reward_count FROM srv1_hunabku.hunter_quest_achievements_config WHERE enabled=1 ORDER BY type, requirement"
    local cc, cd = mysql_direct_query(cq)
    
    if cc == 0 then return {} end
    
    -- Prendi statistiche giocatore
    local sq = "SELECT total_kills, total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid
    local sc, sd = mysql_direct_query(sq)
    
    local kills = 0
    local points = 0
    if sc > 0 and sd[1] then
        kills = tonumber(sd[1].total_kills) or 0
        points = tonumber(sd[1].total_points) or 0
    end
    
    -- Prendi achievements riscossi
    local claimed_map = {}
    local rq = "SELECT achievement_id FROM srv1_hunabku.hunter_achievements_claimed WHERE player_id=" .. pid
    local rc, rd = mysql_direct_query(rq)
    if rc > 0 then
        for i = 1, rc do
            claimed_map[tonumber(rd[i].achievement_id)] = true
        end
    end
    
    -- Costruisci lista
    local result = {}
    for i = 1, cc do
        local a = cd[i]
        local ach_id = tonumber(a.id)
        local ach_type = tonumber(a.type) or 1
        local req = tonumber(a.requirement) or 0
        
        -- type 1 = kills, type 2 = points
        local progress = (ach_type == 1) and kills or points
        local unlocked = progress >= req
        local claimed = claimed_map[ach_id] or false
        
        table.insert(result, {
            id = ach_id,
            name = a.name or "",
            progress = progress,
            requirement = req,
            unlocked = unlocked,
            claimed = claimed,
            reward_vnum = tonumber(a.reward_vnum) or 0,
            reward_count = tonumber(a.reward_count) or 1
        })
    end
    
    return result
end

function hg_lib.claim_achievement(ach_id)
    local pid = pc.get_player_id()
    
    -- Prendi info achievement
    local q = "SELECT name, type, requirement, reward_vnum, reward_count FROM srv1_hunabku.hunter_quest_achievements_config WHERE id=" .. ach_id .. " AND enabled=1"
    local c, d = mysql_direct_query(q)
    
    if c == 0 then
        hg_lib.syschat_t("ACH_NOT_FOUND", "Non trovato.", nil, "FF0000")
        return
    end

    local ach_name = d[1].name or "Achievement"
    local ach_type = tonumber(d[1].type) or 1
    local req = tonumber(d[1].requirement) or 0
    local reward_vnum = tonumber(d[1].reward_vnum) or 0
    local reward_count = tonumber(d[1].reward_count) or 1

    -- Controlla se gia riscosso
    local check_q = "SELECT id FROM srv1_hunabku.hunter_achievements_claimed WHERE player_id=" .. pid .. " AND achievement_id=" .. ach_id
    local cc = mysql_direct_query(check_q)
    if cc > 0 then
        hg_lib.syschat_t("ACH_ALREADY_CLAIMED", "Gia' riscosso!", nil, "FF6600")
        return
    end

    -- Controlla progresso
    local sq = "SELECT total_kills, total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid
    local sc, sd = mysql_direct_query(sq)
    if sc == 0 then
        hg_lib.syschat_t("ACH_NOT_HUNTER", "Non sei un Hunter!", nil, "FF0000")
        return
    end

    local kills = tonumber(sd[1].total_kills) or 0
    local points = tonumber(sd[1].total_points) or 0
    local progress = (ach_type == 1) and kills or points

    if progress < req then
        syschat("|cffFF0000[" .. hg_lib.get_text("ACHIEVEMENT", nil, "TRAGUARDO") .. "]|r " .. hg_lib.get_text("ACH_NOT_UNLOCKED", {PROG = progress, REQ = req}, "Non ancora sbloccato! " .. progress .. "/" .. req))
        return
    end

    -- ANTI-EXPLOIT: Lock per prevenire double-click
    local lock_key = "hq_ach_lock"
    if pc.getqf(lock_key) == 1 then
        syschat("|cffFF6600[ACHIEVEMENT]|r Attendi qualche secondo...")
        return
    end
    pc.setqf(lock_key, 1)

    -- Controlla inventario
    if pc.count_empty_inventory(0) < 1 then
        pc.setqf(lock_key, 0)
        hg_lib.syschat_t("ACH_INV_FULL", "Inventario pieno!", nil, "FF0000")
        return
    end

    -- CRITICAL FIX: Dai item PRIMA di marcare come claimed
    -- Se give_item2 fallisce, il player può ritentare
    local success = pc.give_item2(reward_vnum, reward_count)

    if not success or success == 0 then
        pc.setqf(lock_key, 0)
        syschat("|cffFF0000[ACHIEVEMENT]|r Errore durante la consegna. Contatta un GM.")
        hg_lib.log_error("ACHIEVEMENT", "give_item2 failed", "ach_id=" .. ach_id .. " vnum=" .. reward_vnum)
        return
    end

    -- Item dato con successo, ora marca come claimed
    mysql_direct_query("INSERT INTO srv1_hunabku.hunter_achievements_claimed (player_id, achievement_id, claimed_at) VALUES (" .. pid .. ", " .. ach_id .. ", NOW())")

    syschat("|cff00FF00[" .. hg_lib.get_text("ACHIEVEMENT", nil, "TRAGUARDO") .. "]|r " .. ach_name .. " " .. hg_lib.get_text("COMPLETED", nil, "completato") .. "!")
    syschat("|cffFFD700[" .. hg_lib.get_text("REWARD", nil, "RICOMPENSA") .. "]|r " .. hg_lib.get_text("ACH_RECEIVED", {COUNT = reward_count}, "Ricevuto x" .. reward_count .. " oggetto!"))

    -- Rilascia lock dopo 2 secondi
    timer("hq_ach_unlock", 2, "pc.setqf('hq_ach_lock', 0)")
    
    -- Aggiorna UI
    cmdchat("HunterAchievementClaimed " .. ach_id)
end

function hg_lib.smart_claim_all()
    local pid = pc.get_player_id()

    -- ANTI-EXPLOIT: Lock per prevenire double-click
    local lock_key = "hq_smart_claim_lock"
    if pc.getqf(lock_key) == 1 then
        syschat("|cffFF6600[SMART CLAIM]|r Attendi qualche secondo...")
        return
    end
    pc.setqf(lock_key, 1)

    local achievements = hg_lib.get_player_achievements(pid)
    local claimed_count = 0
    local failed_count = 0

    for _, a in ipairs(achievements) do
        if a.unlocked and not a.claimed then
            -- CRITICAL FIX: Controlla inventario AD OGNI iterazione
            if pc.count_empty_inventory(0) < 1 then
                syschat("|cffFF6600[SMART CLAIM]|r " .. hg_lib.get_text("SMART_INV_FULL", {COUNT = claimed_count}, "Inventario pieno! Riscossi " .. claimed_count .. " traguardi."))
                pc.setqf(lock_key, 0)
                return
            end

            -- CRITICAL FIX: Dai item PRIMA di marcare come claimed
            local success = pc.give_item2(a.reward_vnum, a.reward_count)

            if success and success ~= 0 then
                -- Item dato con successo, marca come claimed
                mysql_direct_query("INSERT INTO srv1_hunabku.hunter_achievements_claimed (player_id, achievement_id, claimed_at) VALUES (" .. pid .. ", " .. a.id .. ", NOW())")
                claimed_count = claimed_count + 1
            else
                -- Fallito, logga e continua
                hg_lib.log_error("SMART_CLAIM", "give_item2 failed", "ach_id=" .. a.id)
                failed_count = failed_count + 1
            end
        end
    end

    if claimed_count > 0 then
        syschat("|cff00FF00[SMART CLAIM]|r " .. hg_lib.get_text("SMART_CLAIMED", {COUNT = claimed_count}, "Riscossi " .. claimed_count .. " traguardi!"))
        if failed_count > 0 then
            syschat("|cffFF6600[SMART CLAIM]|r " .. failed_count .. " traguardi non riscossi (errore). Contatta un GM.")
        end
    else
        hg_lib.syschat_t("SMART_NONE", "Nessun traguardo da riscuotere.", nil, "FFD700")
    end

    -- Rilascia lock dopo 3 secondi
    timer("hq_smart_claim_unlock", 3, "pc.setqf('hq_smart_claim_lock', 0)")
end

