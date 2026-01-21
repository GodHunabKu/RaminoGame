quest hunter_level_bridge begin

    state start begin

        -- ============================================================
        -- EVENT HANDLERS (Usando hg_lib per evitare conflitti)
        -- ============================================================
        when letter begin
             -- FIX: Rimossa la pulizia manuale pericolosa della cache globale.
             -- La gestione è ora affidata in modo sicuro a hg_lib.load_elite_cache()
             send_letter("Hunter Terminal")

             -- PERFORMANCE: Carica cache configurazioni (una query all'avvio)
             hg_lib.load_config_cache()
             
             -- PERFORMANCE: Carica cache mob elite (una query all'avvio invece di N query ai kill)
             hg_lib.load_elite_cache()

             -- PERFORMANCE: Avvia timer salvataggio periodico ranking (ogni 5 minuti)
             cleartimer("hq_ranking_flush_timer")
             loop_timer("hq_ranking_flush_timer", 300)
             
             -- EVENTO: Timer per controllare fine eventi e sorteggio (ogni 60 sec)
             cleartimer("hq_event_check_timer")
             loop_timer("hq_event_check_timer", 60)

             -- MEMORY LEAK FIX: Timer cleanup tabelle globali (ogni 1 ora)
             cleartimer("hq_cleanup_timer")
             loop_timer("hq_cleanup_timer", 3600)

             -- FIX RACE CONDITION: Pulisci flag globali stale al login del player
             -- Questo previene stati inconsistenti se il server è crashato o riavviato
             local pid = pc.get_player_id()
             local old_gate_vid = pc.getqf("hq_defense_fracture_vid") or 0
             if old_gate_vid > 0 then
                 -- Pulisci le flag globali associate a questa gate
                 game.set_event_flag("hq_gate_conq_" .. old_gate_vid, 0)
                 game.set_event_flag("hq_gate_lock_" .. old_gate_vid, 0)
                 game.set_event_flag("hq_gate_time_" .. old_gate_vid, 0)
                 game.set_event_flag("hq_defense_killed_" .. old_gate_vid, 0)
                 game.set_event_flag("hq_defense_req_" .. old_gate_vid, 0)
             end

             -- CLEANUP: Se player riconnette durante difesa attiva, pulisci stato
             if pc.getqf("hq_defense_active") == 1 then
                 pc.setqf("hq_defense_active", 0)
                 pc.setqf("hq_defense_x", 0)
                 pc.setqf("hq_defense_y", 0)
                 pc.setqf("hq_defense_mob_total", 0)
                 pc.setqf("hq_defense_mob_killed", 0)
                 pc.setqf("hq_defense_fracture_vid", 0)
                 cleartimer("hq_defense_timer")
             end
             if pc.getqf("hq_speedkill_active") == 1 then
                 pc.setqf("hq_speedkill_active", 0)
                 cleartimer("hq_speedkill_timer")
             end
        end

when chat."/hunter_request_trial_data" begin
            local pid = pc.get_player_id()
            
            -- 1. Invia stato Gate (se attivo)
            local gate_vid = pc.getqf("hq_defense_fracture_vid") or 0
            if gate_vid > 0 then
                -- Recupera dati gate dalla memoria o ricalcola
                -- Per semplicit�, rimandiamo lo stato di difesa se attivo
                local end_time = game.get_event_flag("hq_gate_time_"..gate_vid)
                local remaining = end_time - get_time()
                if remaining > 0 then
                    -- Recupera nome e colore (salvati in hunter_defense_data)
                    local ddata = hunter_defense_data[pid]
                    if ddata then
                        cmdchat("HunterGateStatus " .. gate_vid .. "|" .. hg_lib.clean_str(ddata.fname) .. "|" .. remaining .. "|" .. ddata.color)
                    end
                end
            end

            -- 2. Invia stato Trial (Rank Up)
            -- Chiama la procedura SQL per ottenere i dati della trial corrente
            local q = "SELECT t.trial_id, t.trial_name, t.to_rank, t.color_code, "
            q = q .. "pt.boss_kills, rt.required_boss_kills, "
            q = q .. "pt.metin_kills, rt.required_metin_kills, "
            q = q .. "pt.fracture_seals, rt.required_fracture_seals, "
            q = q .. "pt.chest_opens, rt.required_chest_opens, "
            q = q .. "pt.daily_missions, rt.required_daily_missions, "
            q = q .. "UNIX_TIMESTAMP(pt.expires_at) - UNIX_TIMESTAMP(NOW()) as remaining "
            q = q .. "FROM srv1_hunabku.hunter_player_trials pt "
            q = q .. "JOIN srv1_hunabku.hunter_rank_trials rt ON pt.trial_id = rt.trial_id "
            q = q .. "JOIN srv1_hunabku.hunter_quest_ranking r ON pt.player_id = r.player_id "
            q = q .. "WHERE pt.player_id = " .. pid .. " AND pt.status = 'in_progress'"
            
            local c, d = mysql_direct_query(q)
            if c > 0 and d[1] then
                local t = d[1]
                local rem = tonumber(t.remaining)
                if not rem or rem < 0 then rem = -1 end
                
                -- Costruisce la stringa dati per il client
                local pkt = t.trial_id .. "|" .. hg_lib.clean_str(t.trial_name) .. "|" .. t.to_rank .. "|" .. t.color_code .. "|" .. rem .. "|"
                pkt = pkt .. t.boss_kills .. "|" .. t.required_boss_kills .. "|"
                pkt = pkt .. t.metin_kills .. "|" .. t.required_metin_kills .. "|"
                pkt = pkt .. t.fracture_seals .. "|" .. t.required_fracture_seals .. "|"
                pkt = pkt .. t.chest_opens .. "|" .. t.required_chest_opens .. "|"
                pkt = pkt .. t.daily_missions .. "|" .. t.required_daily_missions
                
                cmdchat("HunterTrialStatus " .. pkt)
            else
                -- Nessuna trial attiva, invia pacchetto vuoto per resettare la UI
                cmdchat("HunterTrialStatus 0||||-1|0|0|0|0|0|0|0|0|0|0")
            end
        end

        when levelup with pc.get_level() == 5 begin
            cmdchat("HunterAwakening " .. hg_lib.clean_str(pc.get_name()))
            timer("hq_lv5_msg1", 2)
            timer("hq_lv5_msg2", 5)
            timer("hq_lv5_msg3", 8)
        end

        when hq_lv5_msg1.timer begin
            local t1 = hg_lib.get_text_colored("lv5_line1a") or "|cffFF0000========================================|r"
            local t2 = hg_lib.get_text_colored("lv5_line1b") or "|cffFF0000   ! ! ! ANOMALIA RILEVATA ! ! !|r"
            local t3 = hg_lib.get_text_colored("lv5_line1c") or "|cffFF0000========================================|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
        end

        when hq_lv5_msg2.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("lv5_line2a") or "|cff888888   Il Sistema ti ha notato...|r"
            local t2 = hg_lib.get_text_colored("lv5_line2b") or "|cff888888   Qualcosa si sta risvegliando.|r"
            syschat(t1)
            syschat(t2)
        end

        when hq_lv5_msg3.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("lv5_line3a") or "|cffFFD700   Raggiungi il livello 30...|r"
            local t2 = hg_lib.get_text_colored("lv5_line3b") or "|cffFFD700   ...e scoprirai la verita.|r"
            syschat(t1)
            syschat(t2)
            syschat("")
        end

        when levelup with pc.get_level() == 30 begin
            local pid = pc.get_player_id()
            local pname = mysql_escape_string(pc.get_name())
            local chk, _ = mysql_direct_query("SELECT player_id FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
            if chk == 0 then 
                mysql_direct_query("INSERT INTO srv1_hunabku.hunter_quest_ranking (player_id, player_name, total_points, spendable_points) VALUES (" .. pid .. ", '" .. pname .. "', 0, 0)")
            end
            
            cmdchat("HunterActivation " .. hg_lib.clean_str(pc.get_name()))
            timer("hq_lv30_msg1", 2)
            timer("hq_lv30_msg2", 5)
            timer("hq_lv30_msg3", 8)
            timer("hq_lv30_msg4", 11)
        end

        when hq_lv30_msg1.timer begin
            local t1 = hg_lib.get_text_colored("lv30_line1a") or "|cff0099FF========================================|r"
            local t2 = hg_lib.get_text_colored("lv30_line1b") or "|cff0099FF       [ S Y S T E M ]|r"
            local t3 = hg_lib.get_text_colored("lv30_line1c") or "|cff0099FF========================================|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
        end

        when hq_lv30_msg2.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("lv30_line2a") or "|cffFFD700   HUNTER SYSTEM ATTIVATO|r"
            local t2 = hg_lib.get_text("lv30_line2b", {NAME = pc.get_name()}) or ("   Benvenuto, " .. pc.get_name())
            syschat(t1)
            syschat("|cffFFFFFF" .. t2 .. "|r")
        end

        when hq_lv30_msg3.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("lv30_line3a") or "|cff00FF00   >> Da oggi lotterai per la Gloria!|r"
            local t2 = hg_lib.get_text_colored("lv30_line3b") or "|cff00FF00   >> Fratture, Classifiche, Tesori...|r"
            local t3 = hg_lib.get_text_colored("lv30_line3c") or "|cff00FF00   >> Ti attendono.|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
        end

        when hq_lv30_msg4.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("lv30_line4a") or "|cffFF6600   A R I S E|r"
            local t2 = hg_lib.get_text_colored("lv30_line4b") or "|cffFFFFFF   Il tuo viaggio come Hunter inizia ORA.|r"
            local t3 = hg_lib.get_text_colored("lv30_line4c") or "|cff00FFFF   [Y] - Apri Hunter Terminal|r"
            local t4 = hg_lib.get_text_colored("lv30_line1c") or "|cff0099FF========================================|r"
            syschat(t1)
            syschat(t2)
            syschat("")
            syschat(t3)
            syschat(t4)
        end

        when login with pc.get_level() >= 5 begin
            local pid = pc.get_player_id()
            local pname = mysql_escape_string(pc.get_name())
            local chk, res = mysql_direct_query("SELECT player_id, total_points FROM srv1_hunabku.hunter_quest_ranking WHERE player_id=" .. pid)
            if chk == 0 then 
                mysql_direct_query("INSERT INTO srv1_hunabku.hunter_quest_ranking (player_id, player_name, total_points, spendable_points) VALUES (" .. pid .. ", '" .. pname .. "', 0, 0)")
            else 
                mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET player_name='" .. pname .. "' WHERE player_id=" .. pid) 
            end
            
            local total_pts = 0
            if chk > 0 and res[1] then
                total_pts = tonumber(res[1].total_points) or 0
            end
            
            local rank_num = hg_lib.get_rank_index(total_pts)
            pc.setqf("hq_rank_num", rank_num)
            pc.setqf("hq_welcome_pts", total_pts)
            
            local last_logout = pc.getqf("hq_last_logout") or 0
            local current_time = get_time()
            local offline_seconds = current_time - last_logout
            local welcome_threshold = hg_lib.get_config("welcome_offline_seconds") or 120
            local show_welcome = (offline_seconds >= welcome_threshold)
            
            hg_lib.check_login_streak()
            hg_lib.check_pending_rewards()
            -- Gate selection check RITARDATO di 8 secondi per non sovrapporsi
            -- al sistema di inizializzazione e welcome message
            timer("hq_gate_selection_check", 8)
            hg_lib.assign_daily_missions()
            hg_lib.send_today_events(false)
            hg_lib.check_active_event_notify()
            
            -- Invia TUTTI i dati del terminale al client al login
            -- (player data, ranking, shop, achievements, timers, etc.)
            hg_lib.send_all_data()

            if pc.getqf("hq_intro") == 0 then 
                pc.setqf("hq_intro", 1)
                hg_lib.show_awakening_sequence(pname)
            elseif show_welcome then
                cmdchat("HunterSystemInit")
                timer("hq_welcome_msg", 4)
            end
            
            cleartimer("hunter_update_timer")
            local timer_update = hg_lib.get_config("timer_update_stats") or 60
            loop_timer("hunter_update_timer", timer_update)
            cleartimer("hunter_tips_timer")
            local timer_tips = hg_lib.get_config("timer_tips_random") or 90
            loop_timer("hunter_tips_timer", timer_tips)
            cleartimer("hunter_reset_check")
            local timer_reset = hg_lib.get_config("timer_reset_check") or 60
            loop_timer("hunter_reset_check", timer_reset)

            -- PERSISTENZA EMERGENCY QUEST: Restaura se ancora attiva, altrimenti fallisce
            -- Timer a 6 secondi per apparire DOPO tutti gli altri messaggi di login
            timer("hq_restore_emergency", 6)
        end

        when logout begin
            local pid = pc.get_player_id()

            -- PERFORMANCE: Salva accumulatori ranking PRIMA del logout (CRITICO!)
            -- FIX: Usa pcall per evitare che un errore SQL blocchi il logout
            local status, err = pcall(hg_lib.flush_ranking_updates)
            if not status then
                -- Log errore ma non bloccare il logout
                syserr("HunterSystem: Flush failed for pid " .. pid .. " : " .. tostring(err))
            end

            -- Salva tempo logout
            pc.setqf("hq_last_logout", get_time())

            -- MEMORY LEAK FIX: Pulisci tabelle globali per questo player in modo sicuro
            if _G.hunter_temp_gate_data and _G.hunter_temp_gate_data[pid] then
                _G.hunter_temp_gate_data[pid] = nil
            end
            if hunter_defense_data and hunter_defense_data[pid] then
                hunter_defense_data[pid] = nil
            end
            
            -- Pulisci anche buffer missioni per questo player
            if _G.hunter_mission_buffer and _G.hunter_mission_buffer[pid] then
                _G.hunter_mission_buffer[pid] = nil
            end
            -- Pulisci anche throttle missioni
            if _G.hunter_mission_throttle then
                local throttle_key = pid .. "_mission_flush"
                _G.hunter_mission_throttle[throttle_key] = nil
            end
            -- Pulisci kill tracking per questo player
            if _G.hunter_kill_tracking and _G.hunter_kill_tracking[pid] then
                _G.hunter_kill_tracking[pid] = nil
            end
            -- Pulisci send_player_data throttle
            if _G.hunter_player_data_throttle and _G.hunter_player_data_throttle[pid] then
                _G.hunter_player_data_throttle[pid] = nil
            end
        end

        when hq_welcome_msg.timer begin
            -- Usa rank_num già calcolato invece di ricalcolarlo dai punti
            local rank_num = pc.getqf("hq_rank_num") or 0
            local pts = pc.getqf("hq_welcome_pts") or 0
            hg_lib.show_rank_welcome_by_rank(pc.get_name(), rank_num, pts)
        end

        when hq_restore_emergency.timer begin
            -- Ripristina emergency quest se attiva, altrimenti la fallisce
            hg_lib.restore_emergency_on_login()
        end

        when hq_gate_selection_check.timer begin
            -- Notifica se il player e' stato sorteggiato per un Gate
            -- Ritardato per non sovrapporsi al sistema di inizializzazione
            hg_lib.check_gate_selection()
        end

        when hq_awaken_1.timer begin
            local speak = hg_lib.get_text("awaken1_speak") or "[SYSTEM] SCANSIONE BIOLOGICA IN CORSO..."
            cmdchat("HunterSystemSpeak E|" .. hg_lib.clean_str(speak))
            local t1 = hg_lib.get_text_colored("awaken1_line1") or "|cff00FFFF========================================|r"
            local t2 = hg_lib.get_text_colored("awaken1_line2") or "|cffFFFFFF        ...ANALISI IN CORSO...|r"
            local t3 = hg_lib.get_text_colored("awaken1_line3") or "|cff00FFFF========================================|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
        end

        when hq_awaken_2.timer begin
            local speak = hg_lib.get_text("awaken2_speak") or "[SYSTEM] COMPATIBILITA CONFERMATA."
            cmdchat("HunterSystemSpeak E|" .. hg_lib.clean_str(speak))
            syschat("")
            local t1 = hg_lib.get_text_colored("awaken2_line1") or "|cff00FF00   >> COMPATIBILITA: 100 pct <<|r"
            local t2 = hg_lib.get_text_colored("awaken2_line2") or "|cff00FF00   >> REQUISITI: SODDISFATTI <<|r"
            syschat(t1)
            syschat(t2)
        end

        when hq_awaken_3.timer begin
            local speak = hg_lib.get_text("awaken3_speak") or "[SYSTEM] NUOVO CACCIATORE REGISTRATO."
            cmdchat("HunterSystemSpeak E|" .. hg_lib.clean_str(speak))
            syschat("")
            local t1 = hg_lib.get_text("awaken3_line1", {NAME = pc.get_name()}) or ("   NOME: " .. pc.get_name())
            local t2 = hg_lib.get_text_colored("awaken3_line2") or "|cff808080   RANGO INIZIALE: [E-RANK]|r"
            syschat("|cffFFD700" .. t1 .. "|r")
            syschat(t2)
        end

        when hq_awaken_4.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("awaken4_line1") or "|cffFF0000========================================|r"
            local t2 = hg_lib.get_text_colored("awaken4_line2") or "|cffFF6600   !! RISVEGLIO COMPLETATO !!|r"
            local t3 = hg_lib.get_text_colored("awaken4_line3") or "|cffFF0000========================================|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
            local speak = hg_lib.get_text("awaken4_speak", {NAME = pc.get_name()}) or ("RISVEGLIO COMPLETATO. BENVENUTO, " .. pc.get_name() .. ".")
            cmdchat("HunterSystemSpeak E|" .. hg_lib.clean_str(speak))
        end

        when hq_awaken_5.timer begin
            syschat("")
            local t1 = hg_lib.get_text_colored("awaken5_line1") or "|cffFFD700====================================================|r"
            local t2 = hg_lib.get_text_colored("awaken5_line2") or "|cff00FFFF        *** HUNTER SYSTEM v36.0 ATTIVATO ***|r"
            local t3 = hg_lib.get_text_colored("awaken5_line3") or "|cffFFD700====================================================|r"
            local t4 = hg_lib.get_text_colored("awaken5_line4") or "|cffFFFFFF   Il Sistema ti ha scelto. Da questo momento:|r"
            local t5 = hg_lib.get_text_colored("awaken5_line5") or "|cff00FF00   >> Ogni nemico cadra sotto la tua lama|r"
            local t6 = hg_lib.get_text_colored("awaken5_line6") or "|cff00FF00   >> Ogni vittoria sara registrata|r"
            local t7 = hg_lib.get_text_colored("awaken5_line7") or "|cff00FF00   >> Ogni rank sara conquistato|r"
            local t8 = hg_lib.get_text_colored("awaken5_line8") or "|cffFFAA00   'Inizia con un solo passo...'|r"
            local t9 = hg_lib.get_text_colored("awaken5_line9") or "|cffFFAA00   'Finisci come una Leggenda.'|r"
            local t10 = hg_lib.get_text_colored("awaken5_line10") or "|cff00FF00   [Y] - Apri Hunter Terminal|r"
            syschat(t1)
            syschat(t2)
            syschat(t3)
            syschat("")
            syschat(t4)
            syschat(t5)
            syschat(t6)
            syschat(t7)
            syschat("")
            syschat(t8)
            syschat(t9)
            syschat("")
            syschat(t10)
            syschat(t1)
        end

        when hunter_reset_check.timer begin
            -- OTTIMIZZAZIONE: Usa flag per evitare check ripetuti inutili
            local today = math.floor(get_time() / 86400)
            local last_check_day = pc.getqf("hq_last_reset_check_day") or 0
            
            -- Se abbiamo gia' fatto tutti i check per oggi, salta
            local daily_done = pc.getqf("hq_daily_reset_done") or 0
            local reminder_done = pc.getqf("hq_reminder_done") or 0
            
            -- Nuovo giorno? Resetta i flag
            if last_check_day < today then
                pc.setqf("hq_last_reset_check_day", today)
                pc.setqf("hq_daily_reset_done", 0)
                pc.setqf("hq_reminder_done", 0)
                daily_done = 0
                reminder_done = 0
            end
            
            -- Se entrambi i check sono gia' stati fatti oggi, non fare nulla
            if daily_done == 1 and reminder_done == 1 then
                return
            end
            
            local ts = get_time()
            local hour = hg_lib.get_hour_from_ts(ts)
            local min = hg_lib.get_min_from_ts(ts)
            local dow = hg_lib.get_dow_from_ts(ts)
            
            -- Reminder missioni: solo una volta dopo le 22
            if hour >= 22 and reminder_done == 0 then
                hg_lib.check_missions_reminder()
                pc.setqf("hq_reminder_done", 1)
            end
            
            -- Reset giornaliero: solo a mezzanotte, una volta
            if hour == 0 and min <= 1 and daily_done == 0 then
                local last_daily = game.get_event_flag("hunter_last_daily_reset") or 0
                if last_daily < today then
                    game.set_event_flag("hunter_last_daily_reset", today)
                    hg_lib.announce_daily_winners()
                    hg_lib.process_daily_reset()
                    
                    -- NUOVO GIORNO: Invia cmdchat per aggiornare UI eventi
                    cmdchat("HunterNewDay")
                    -- Refresh lista eventi per il nuovo giorno (dopo 2 sec per dare tempo al reset)
                    timer("hq_refresh_events_newday", 2)
                end
                
                if dow == 1 then
                    local last_weekly = game.get_event_flag("hunter_last_weekly_reset") or 0
                    local this_week = math.floor(get_time() / 604800)
                    if last_weekly < this_week then
                        game.set_event_flag("hunter_last_weekly_reset", this_week)
                        hg_lib.announce_weekly_winners()
                        hg_lib.process_weekly_reset()
                    end
                end
                
                pc.setqf("hq_daily_reset_done", 1)
            end
        end

        when hunter_update_timer.timer begin
            -- SOLO check overtake (leggero), no invio dati pesanti
            hg_lib.check_if_overtaken()
        end

        when hunter_emerg_tmr.timer begin
            if pc.getqf("hq_emerg_active") == 1 then
                local expire = pc.getqf("hq_emerg_expire") or 0
                if get_time() > expire then
                    hg_lib.end_emergency("FAIL")
                end
            else
                cleartimer("hunter_emerg_tmr")
            end
        end

        when hunter_tips_timer.timer begin
            -- Invia tip individuale al player (non piu' notice_all che spamma la chat)
            local pid = pc.get_player_id()
            local last = pc.getqf("hq_last_tip_time") or 0
            if get_time() - last < 60 then return end  -- Cooldown 60 sec per player
            local c, d = mysql_direct_query("SELECT tip_text FROM srv1_hunabku.hunter_quest_tips ORDER BY RAND() LIMIT 1")
            if c > 0 and d[1] then
                local tip_text = string.gsub(d[1].tip_text, " ", "+")
                cmdchat("HunterTip " .. tip_text)
                pc.setqf("hq_last_tip_time", get_time())
            end
        end

        when kill with not npc.is_pc() and pc.get_level() >= 5 begin
            local vnum = npc.get_race()
            local mob_level = npc.get_level()
            local player_level = pc.get_level()
            
            hg_lib.on_emergency_kill(vnum)
            hg_lib.on_defense_mob_kill(vnum)
            hg_lib.on_mob_kill(vnum)  -- Semplice: passa solo il vnum
            
            -- I mob Elite (Boss/Metin/Bauli) vengono SEMPRE processati
            -- Il level range check è solo per mob normali (spawning fratture)
            if hg_lib.is_elite_mob(vnum) then
                hg_lib.process_elite_kill(vnum)
            else
                -- FIX EXPLOIT: Solo mob normali entro +/- 30 livelli contano per spawning fratture
                local level_range = 30
                local level_diff = math.abs(player_level - mob_level)
                if level_diff <= level_range then
                    hg_lib.process_normal_kill()
                end
            end
        end

        -- ============================================================
        -- GESTIONE FRATTURE E DIFESA (FIX LOGICA KING OF THE HILL)
        -- ============================================================
        when 16060.click or 16061.click or 16062.click or 16063.click or 16064.click or 16065.click or 16066.click begin
            local vnum = npc.get_race()
            local vid = npc.get_vid() -- ID Univoco di questa specifica frattura
            local pid = pc.get_player_id()
            
            -- FIX: Se la frattura è stata marcata per la distruzione (difesa fallita), rimuovila
            local should_destroy = game.get_event_flag("hq_gate_destroy_"..vid) or 0
            if should_destroy == 1 then
                game.set_event_flag("hq_gate_destroy_"..vid, 0)
                syschat("|cffFF0000[HUNTER SYSTEM]|r Questa frattura e' stata distrutta!")
                syschat("|cffFF6600[HUNTER SYSTEM]|r Un altro Hunter ha fallito la difesa.")
                syschat("|cffFFFF00[HUNTER SYSTEM]|r Cerca un'altra frattura. Buona caccia!")
                npc.purge()  -- Rimuove la frattura
                return
            end
            
            -- Salva il VID per controlli successivi (es. WhatIf)
            pc.setqf("hq_temp_gate_vid", vid) 

            -- 1. CONTROLLO PROPRIETARIO (VITTORIA PRECEDENTE)
            local owner_pid = game.get_event_flag("hq_gate_conq_"..vid)
            
            if owner_pid > 0 then
                local conq_time = game.get_event_flag("hq_gate_conq_time_"..vid)
                local time_diff = get_time() - conq_time
                local timeout = 300 -- 5 Minuti (300 secondi)

                if time_diff > timeout then
                    -- TEMPO SCADUTO! La frattura torna libera per tutti
                    game.set_event_flag("hq_gate_conq_"..vid, 0)
                    game.set_event_flag("hq_gate_conq_time_"..vid, 0)
                    owner_pid = 0 -- Ora la trattiamo come libera
                    syschat("|cff00FF00[SISTEMA]|r Il diritto di conquista precedente e' scaduto. La frattura e' libera!")
                elseif owner_pid == pid then
                    -- E' il proprietario e siamo nel tempo limite -> APRE
                    hg_lib.finalize_gate_opening(vid)
                    game.set_event_flag("hq_gate_conq_time_"..vid, 0)
                    return
                else
                    -- E' di un altro ed e' ancora nel tempo limite
                    local left = timeout - time_diff
                    syschat("|cffFF0000[SISTEMA]|r Frattura conquistata da un altro Hunter!")
                    syschat("|cffFF0000[SISTEMA]|r Tornera' disponibile tra " .. left .. " secondi se non viene aperta.")
                    return
                end
            end

            -- 2. CONTROLLO DIFESA IN CORSO
            local lock_pid = game.get_event_flag("hq_gate_lock_"..vid)
            local lock_time = game.get_event_flag("hq_gate_time_"..vid)
            
            if lock_pid > 0 then
                if get_time() > lock_time then
                    game.set_event_flag("hq_gate_lock_"..vid, 0) -- Sblocca timeout difesa
                elseif lock_pid == pid then
                    syschat("|cffFFFF00[SISTEMA]|r Concentrati sulla difesa! Non distrarti!")
                    return
                else
                    syschat("|cffFF0000[SISTEMA]|r Un altro Hunter sta gia' sfidando questa frattura.")
                    return
                end
            end

            -- ============================================================
            -- CONTROLLO PRENOTAZIONE PARTY (Protegge da "furti")
            -- ============================================================
            local reserved_leader = game.get_event_flag("hq_gate_reserved_" .. vid) or 0
            local reserved_time = game.get_event_flag("hq_gate_reserved_time_" .. vid) or 0
            local reservation_timeout = 60  -- 60 secondi per far toccare tutti
            
            if reserved_leader > 0 then
                -- Controlla se la prenotazione e' scaduta
                if get_time() - reserved_time > reservation_timeout then
                    -- Scaduta! Libera la frattura
                    syschat("|cff00FF00[SISTEMA]|r La prenotazione precedente e' scaduta!")
                    game.set_event_flag("hq_gate_reserved_" .. vid, 0)
                    game.set_event_flag("hq_gate_reserved_time_" .. vid, 0)
                    -- Pulisci anche le flag di touch del party precedente
                    game.set_event_flag("hq_gate_touch_time_" .. vid, 0)
                    reserved_leader = 0
                else
                    -- Prenotazione ancora valida - controlla se questo player fa parte del party prenotato
                    local is_in_reserved_party = false
                    
                    if party.is_party() then
                        local my_leader = party.get_leader_pid()
                        if my_leader == reserved_leader then
                            is_in_reserved_party = true
                        end
                    elseif pid == reserved_leader then
                        -- Player solo che aveva prenotato
                        is_in_reserved_party = true
                    end
                    
                    if not is_in_reserved_party then
                        local remaining = reservation_timeout - (get_time() - reserved_time)
                        syschat("|cffFF0000[SISTEMA]|r Frattura riservata da un altro party!")
                        syschat("|cffFF0000[SISTEMA]|r Tornera' disponibile tra " .. remaining .. " secondi.")
                        return
                    end
                end
            end
            -- ============================================================
            -- FINE CONTROLLO PRENOTAZIONE
            -- ============================================================

            -- ============================================================
            -- NUOVA LOGICA PARTY: TUTTI DEVONO TOCCARE LA FRATTURA
            -- ============================================================
            if party.is_party() then
                local leader_pid = party.get_leader_pid()
                local pids = {party.get_member_pids()}
                local total_members = table.getn(pids)
                
                -- Timeout: 60 secondi per far toccare tutti
                local touch_timeout = 60
                local first_touch_time = game.get_event_flag("hq_gate_touch_time_" .. vid) or 0
                
                -- Se e' il PRIMO tocco del party, PRENOTA la frattura!
                if first_touch_time == 0 then
                    game.set_event_flag("hq_gate_touch_time_" .. vid, get_time())
                    game.set_event_flag("hq_gate_reserved_" .. vid, leader_pid)
                    game.set_event_flag("hq_gate_reserved_time_" .. vid, get_time())
                    syschat("|cff00FF00[SISTEMA]|r Frattura RISERVATA al tuo party per 60 secondi!")
                    party.syschat("[HUNTER] Frattura riservata! Tutti devono toccarla entro 60 secondi!")
                    first_touch_time = get_time()
                end
                
                -- Se e' passato troppo tempo dal primo tocco, resetta tutto
                if get_time() - first_touch_time > touch_timeout then
                    syschat("|cffFF0000[SISTEMA]|r Tempo scaduto! Il party ha perso la prenotazione.")
                    party.syschat("[HUNTER] Tempo scaduto! La frattura e' tornata libera.")
                    
                    -- Pulisci tutte le flag
                    game.set_event_flag("hq_gate_touch_time_" .. vid, 0)
                    game.set_event_flag("hq_gate_reserved_" .. vid, 0)
                    game.set_event_flag("hq_gate_reserved_time_" .. vid, 0)
                    for i, member_pid in ipairs(pids) do
                        game.set_event_flag("hq_gate_touch_" .. vid .. "_" .. member_pid, 0)
                    end
                    return  -- Esce, dovra' ritoccare
                end
                
                -- Registra che questo player ha toccato la frattura
                game.set_event_flag("hq_gate_touch_" .. vid .. "_" .. pid, 1)
                
                -- Conta quanti membri hanno toccato
                local touched_count = 0
                local missing_names = {}
                
                for i, member_pid in ipairs(pids) do
                    local has_touched = game.get_event_flag("hq_gate_touch_" .. vid .. "_" .. member_pid) or 0
                    if has_touched == 1 then
                        touched_count = touched_count + 1
                    else
                        -- Il nome verra' mostrato come PID (evita query lente)
                        -- In alternativa: pc.get_name() nel contesto del membro
                        table.insert(missing_names, "Membro#" .. i)
                    end
                end
                
                syschat("|cff00FFFF[PARTY GATE]|r Membri pronti: " .. touched_count .. "/" .. total_members)
                
                -- Se NON tutti hanno toccato, aspetta
                if touched_count < total_members then
                    local elapsed = get_time() - first_touch_time
                    -- SANITY CHECK: elapsed non puo' essere negativo o > timeout
                    if elapsed < 0 then elapsed = 0 end
                    if elapsed > touch_timeout then elapsed = touch_timeout end
                    local remaining = touch_timeout - elapsed
                    if remaining < 0 then remaining = 0 end
                    
                    syschat("|cffFFFF00[SISTEMA]|r In attesa degli altri membri... (" .. remaining .. "s)")
                    if table.getn(missing_names) > 0 then
                        local missing_str = table.concat(missing_names, ", ")
                        syschat("|cffFFAA00[MANCANO]|r " .. missing_str)
                    end
                    
                    -- Notifica il party
                    party.syschat("[HUNTER] " .. pc.get_name() .. " e' pronto! (" .. touched_count .. "/" .. total_members .. ") - " .. remaining .. "s rimasti")
                    return
                end
                
                -- TUTTI HANNO TOCCATO! Procedi con l'apertura
                syschat("|cff00FF00[SISTEMA]|r Tutti i membri sono pronti! Apertura frattura...")
                party.syschat("[HUNTER] Tutti pronti! La frattura si sta aprendo!")
                
                -- Pulisci le flag di touch e prenotazione (la difesa prendera' il controllo)
                game.set_event_flag("hq_gate_touch_time_" .. vid, 0)
                game.set_event_flag("hq_gate_reserved_" .. vid, 0)
                game.set_event_flag("hq_gate_reserved_time_" .. vid, 0)
                for i, member_pid in ipairs(pids) do
                    game.set_event_flag("hq_gate_touch_" .. vid .. "_" .. member_pid, 0)
                end
            end
            -- ============================================================
            -- FINE LOGICA PARTY TOUCH
            -- ============================================================

            -- 3. LOGICA APERTURA (SE LIBERA)
            -- PERFORMANCE: Usa cache fratture invece di query
            local cached_fracs = hg_lib.get_fractures_cached()
            local fname, frank, freq, fcolor = nil, nil, 0, "PURPLE"
            if cached_fracs and cached_fracs.data then
                for i = 1, cached_fracs.count do
                    if tonumber(cached_fracs.data[i].vnum) == vnum then
                        fname = cached_fracs.data[i].name or cached_fracs.data[i].rank_label
                        frank = cached_fracs.data[i].rank_label
                        freq = tonumber(cached_fracs.data[i].req_points) or 0
                        fcolor = cached_fracs.data[i].color_code or "PURPLE"
                        break
                    end
                end
            end
            -- Fallback query se non in cache
            if not fname then
                local c, d = mysql_direct_query("SELECT name, rank_label, req_points, color_code FROM srv1_hunabku.hunter_quest_fractures WHERE vnum=" .. vnum)
                if c == 0 or not d[1] then return end
                fname, frank, freq = d[1].name, d[1].rank_label, tonumber(d[1].req_points) or 0
                fcolor = d[1].color_code or "PURPLE"
            end
            
            -- PERFORMANCE: Usa qf invece di query per player_pts
            local player_pts = pc.getqf("hq_total_points") or 0
            
            -- Salva dati gate temporanei
            pc.setqf("hq_temp_gate_vnum", vnum)
            pc.setqf("hq_temp_gate_freq", freq)
            pc.setqf("hq_temp_player_pts", player_pts)
            hg_lib.set_temp_gate_data(pid, {
                fname = fname,
                frank = frank,
                fcolor = fcolor
            })
            
            local whatif_chance = hg_lib.get_config("whatif_chance_percent") or 50
            if number(1, 100) <= whatif_chance then
                -- === WHAT-IF SCENARIO ===
                local voice_ok = hg_lib.get_fracture_voice(fcolor, true)
                local voice_no = hg_lib.get_fracture_voice(fcolor, false)
                local seal_bonus = hg_lib.get_config("seal_fracture_bonus") or 200
                local opt1_ok = hg_lib.get_text("whatif_opt1_ok") or ">> ATTRAVERSA IL PORTALE"
                local opt2 = hg_lib.get_text("whatif_opt2_seal", {POINTS = seal_bonus}) or ("|| SIGILLA [+" .. seal_bonus .. " Gloria]")
                local opt3 = hg_lib.get_text("whatif_opt3_retreat") or "<< INDIETREGGIA"
                
                local question_text = ""
                local opt1 = ""
                
                -- Se req_points = 0, la frattura e' GRATUITA (aperta a tutti)
                -- OPPURE se il player ha abbastanza Gloria, puo' entrare normalmente
                if freq == 0 or player_pts >= freq then
                    question_text = "? " .. string.upper(fname) .. " ?|'" .. voice_ok .. "'"
                    opt1 = opt1_ok
                else
                    -- Controlla requisiti per forzare (Power Rank o Party classico)
                    local can_force, force_type, total_power, required_power = hg_lib.can_force_fracture(vnum)
                    local mancano = freq - player_pts
                    
                    if force_type == "POWER_RANK" then
                        -- Sistema Power Rank per fratture B+
                        local power_text = "Power Rank: " .. (total_power or 0) .. "/" .. (required_power or 0)
                        if can_force then
                            question_text = "? " .. string.upper(fname) .. " ?|'" .. voice_no .. "'|[Gloria: " .. freq .. " | " .. power_text .. " OK!]"
                            opt1 = ">> FORZA [" .. power_text .. "]"
                        else
                            question_text = "? " .. string.upper(fname) .. " ?|'" .. voice_no .. "'|[Gloria: " .. freq .. " | " .. power_text .. "]"
                            opt1 = ">> FORZA [Serve " .. required_power .. " PR]"
                        end
                    else
                        -- Sistema classico Party 4+ per fratture E/D/C
                        if can_force then
                            question_text = "? " .. string.upper(fname) .. " ?|'" .. voice_no .. "'|[Richiesti: " .. freq .. " | Party 4+ OK!]"
                            opt1 = ">> FORZA [Party 4+]"
                        else
                            question_text = "? " .. string.upper(fname) .. " ?|'" .. voice_no .. "'|[Richiesti: " .. freq .. " | Mancano: " .. mancano .. "]"
                            opt1 = ">> FORZA [Party 4+]"
                        end
                    end
                end
                
                hg_lib.ask_choice_color("gate_main", question_text, opt1, opt2, opt3, fcolor)
            else
                -- === CLASSIC QUEST SCENARIO ===
                say_title("? " .. fname .. " ?")
                say("")
                say(hg_lib.get_text("classic_gate_intro") or "Questo portale emana un'energia instabile.")
                say("")
                
                -- Controlla requisiti per forzare
                local can_force, force_type, total_power, required_power, members = hg_lib.can_force_fracture(vnum)
                
                -- Se req_points = 0 (GRATUITA) o player ha abbastanza Gloria
                if freq == 0 or player_pts >= freq then
                    say(hg_lib.get_text("classic_gate_worthy") or "Il tuo Rango Hunter e' sufficiente.")
                    say(hg_lib.get_text("classic_gate_ask") or "Vuoi spezzare il sigillo ed entrare?")
                    say("")
                    if select("Apri Gate", "Chiudi") == 1 then
                        -- FIX: Check se il player sta già difendendo un'altra frattura
                        if pc.getqf("hq_defense_active") == 1 then
                            say_title("CONFLITTO!")
                            say("Stai gia' difendendo un'altra frattura!")
                            say("Completa prima quella.")
                            return
                        end
                        if game.get_event_flag("hq_gate_lock_"..vid) > 0 or game.get_event_flag("hq_gate_conq_"..vid) > 0 then
                            say_title("Troppo Tardi!")
                            say("Un altro Hunter e' stato piu' veloce.")
                            return
                        end
                        hg_lib.open_gate(fname, frank, fcolor, pid)
                    end
                else
                    say(hg_lib.get_text("classic_gate_not_worthy") or "Non possiedi abbastanza Gloria.")
                    say("Gloria Richiesta: " .. freq)
                    say("")
                    
                    if force_type == "POWER_RANK" then
                        -- Sistema Power Rank per fratture B/A/S/N
                        say_reward("=== SISTEMA POWER RANK ===")
                        say("Questa frattura richiede Power Rank!")
                        say("")
                        say("Power Rank Party: " .. (total_power or 0) .. " / " .. (required_power or 0))
                        say("")
                        if members and table.getn(members) > 0 then
                            say("Membri:")
                            for _, m in ipairs(members) do
                                say("  - " .. m.name .. " [" .. m.grade .. "-Rank] = " .. m.power .. " PR")
                            end
                            say("")
                        end
                        
                        if can_force then
                            say_reward("Power Rank SUFFICIENTE!")
                            if select("Forza Gate", "Chiudi") == 1 then
                                -- FIX: Check se il player sta già difendendo un'altra frattura
                                if pc.getqf("hq_defense_active") == 1 then
                                    say_title("CONFLITTO!")
                                    say("Stai gia' difendendo un'altra frattura!")
                                    say("Completa prima quella.")
                                    return
                                end
                                if game.get_event_flag("hq_gate_lock_"..vid) > 0 or game.get_event_flag("hq_gate_conq_"..vid) > 0 then
                                    say_title("Troppo Tardi!")
                                    say("Un altro Hunter e' stato piu' veloce.")
                                    return
                                end
                                hg_lib.open_gate(fname, frank, fcolor, pid)
                            end
                        else
                            say("|cffFF0000Power Rank INSUFFICIENTE!|r")
                            say("Recluta Hunter piu' forti nel party.")
                            select("Chiudi")
                        end
                    else
                        -- Sistema classico Party 4+ per fratture E/D/C
                        if can_force then
                            say_reward("Il tuo Party (4+) puo' forzarlo!")
                            if select("Forza Gate", "Chiudi") == 1 then
                                -- FIX: Check se il player sta già difendendo un'altra frattura
                                if pc.getqf("hq_defense_active") == 1 then
                                    say_title("CONFLITTO!")
                                    say("Stai gia' difendendo un'altra frattura!")
                                    say("Completa prima quella.")
                                    return
                                end
                                if game.get_event_flag("hq_gate_lock_"..vid) > 0 or game.get_event_flag("hq_gate_conq_"..vid) > 0 then
                                    say_title("Troppo Tardi!")
                                    say("Un altro Hunter e' stato piu' veloce.")
                                    return
                                end
                                hg_lib.open_gate(fname, frank, fcolor, pid)
                            end
                        else
                            say("Servono almeno 4 membri nel party.")
                            select("Chiudi")
                        end
                    end
                end
            end
        end 

        -- ============================================================
        -- GESTIONE BAULI/CASSE CLICCABILI (63000-63007)
        -- I bauli vengono spawnati nelle fratture e danno Gloria + Item
        -- La Gloria viene divisa per meritocrazia se in party
        -- FIX RACE CONDITION: npc.purge() PRIMA di open_chest per evitare double loot
        -- ============================================================
        when 63000.click or 63001.click or 63002.click or 63003.click or 63004.click or 63005.click or 63006.click or 63007.click begin
            local chest_vnum = npc.get_race()
            local chest_vid = npc.get_vid()
            local pid = pc.get_player_id()
            
            -- ANTI-SPAM per singolo player (pc.getqf e' in RAM, veloce)
            local last_click = pc.getqf("hq_anti_spam_chest") or 0
            if get_time() - last_click < 2 then 
                return -- Anti-autoclick lato client
            end
            pc.setqf("hq_anti_spam_chest", get_time())
            
            -- Verifica che il baule non sia gia' stato aperto (flag globale)
            -- NOTA: Usiamo un timestamp invece di un flag 0/1 per evitare problemi con VID riutilizzati
            local opened_time = game.get_event_flag("hq_chest_opened_"..chest_vid) or 0
            if opened_time > 0 then
                -- Se aperto meno di 60 secondi fa, blocca (previene double loot e considera VID riciclati)
                local time_diff = get_time() - opened_time
                if time_diff < 60 then
                    syschat("|cffFF0000[BAULE]|r Questo baule e' gia' stato aperto!")
                    return
                end
                -- Altrimenti la flag e' vecchia, il VID e' stato riutilizzato - procedi
            end
            
            -- LOCK IMMEDIATO - Prima di qualsiasi altra cosa
            game.set_event_flag("hq_chest_opened_"..chest_vid, get_time())
            
            -- FIX RACE CONDITION: Rimuovi NPC PRIMA di dare il premio
            -- Cosi' se un secondo click arriva, l'NPC non esiste piu' lato server core
            npc.purge()
            
            -- Effetto visivo apertura
            cmdchat("HunterChestOpening " .. chest_vid)
            
            -- Ora dai il premio (l'NPC e' gia' stato rimosso)
            hg_lib.open_chest(chest_vnum)
        end
        -- ============================================================
        -- FINE GESTIONE BAULI
        -- ============================================================

        when chat."/hunter_whatif_answer" begin
            local txt = pc.get_chat_msg()
            
            -- SECURITY FIX: Validazione lunghezza input per evitare crash
            if not txt or string.len(txt) > 100 then
                return
            end
            
            local space1 = string.find(txt, " ", 1, true) or 0
            local space2 = string.find(txt, " ", space1 + 1, true) or 0
            local qid = ""
            local choice = 0
            if space1 > 0 and space2 > 0 then
                qid = string.sub(txt, space1 + 1, space2 - 1)
                choice = tonumber(string.sub(txt, space2 + 1)) or 0
            end
            
            -- SECURITY FIX: Whitelist qid validi per evitare exploit
            local valid_qids = {["gate_main"] = true, ["gm_test"] = true}
            if not valid_qids[qid] then
                return  -- qid non valido, ignora
            end
            
            -- SECURITY FIX: Validazione choice (solo 1, 2, 3)
            if choice < 1 or choice > 3 then
                return
            end
            
            if qid == "gate_main" then
                local vnum = pc.getqf("hq_temp_gate_vnum")
                local freq = pc.getqf("hq_temp_gate_freq") or 0
                local player_pts = pc.getqf("hq_temp_player_pts") or 0
                local pid = pc.get_player_id()
                
                -- RECUPERA IL VID SALVATO
                local vid = pc.getqf("hq_temp_gate_vid")

                local temp_data = hg_lib.get_temp_gate_data(pid)
                local fname = temp_data.fname or "Frattura"
                local frank = temp_data.frank or "E-Rank"
                local fcolor = temp_data.fcolor or "PURPLE"
                
                if choice == 1 then
                    -- FIX: Check se il player sta già difendendo un'altra frattura
                    if pc.getqf("hq_defense_active") == 1 then
                        hg_lib.hunter_speak_color("CONFLITTO! Stai gia' difendendo un'altra frattura!", "RED")
                        return
                    end

                    -- FIX RACE CONDITION (WHAT-IF)
                    if game.get_event_flag("hq_gate_lock_"..vid) > 0 or game.get_event_flag("hq_gate_conq_"..vid) > 0 then
                        hg_lib.hunter_speak_color("TROPPO TARDI! Un altro Hunter ti ha preceduto.", "RED")
                        return
                    end

                    -- Controlla requisiti per forzare (Power Rank o Party classico)
                    local can_force, force_type, total_power, required_power = hg_lib.can_force_fracture(vnum)

                    -- Se req_points = 0 (gratuita) OPPURE player ha abbastanza Gloria
                    if freq == 0 or player_pts >= freq then
                        local msg = hg_lib.get_text("whatif_seal_break") or "IL SIGILLO SI SPEZZA. PREPARATI."
                        hg_lib.hunter_speak_color(msg, fcolor)
                        hg_lib.open_gate(fname, frank, fcolor, pid)
                    else
                        if can_force then
                            if force_type == "POWER_RANK" then
                                local msg = "POWER RANK SUFFICIENTE! [" .. (total_power or 0) .. "/" .. (required_power or 0) .. "]"
                                hg_lib.hunter_speak_color(msg, fcolor)
                            else
                                local msg = hg_lib.get_text("whatif_party_force") or "IL PARTY FORZA IL SIGILLO!"
                                hg_lib.hunter_speak_color(msg, fcolor)
                            end
                            hg_lib.open_gate(fname, frank, fcolor, pid)
                            local raid_msg = hg_lib.get_text("classic_raid_announce", {PLAYER = pc.get_name(), RANK = frank}) or ("|cffFF0000[RAID]|r Il Party di " .. pc.get_name() .. " ha forzato un Gate " .. frank .. "!")
                            notice_all(raid_msg)
                        else
                            if force_type == "POWER_RANK" then
                                local msg = "POWER RANK INSUFFICIENTE! [" .. (total_power or 0) .. "/" .. (required_power or 0) .. "]"
                                hg_lib.hunter_speak_color(msg, "RED")
                            else
                                local msg = hg_lib.get_text("whatif_need_party") or "ERRORE: SERVONO 4 MEMBRI VICINI."
                                hg_lib.hunter_speak_color(msg, "RED")
                            end
                        end
                    end
                elseif choice == 2 then
                    -- Anche per sigillare, controlliamo che esista ancora
                    if game.get_event_flag("hq_gate_lock_"..vid) > 0 then
                        hg_lib.hunter_speak_color("TROPPO TARDI! Frattura gia' ingaggiata.", "RED")
                        return
                    end

                    npc.purge() -- La frattura sparisce
                    local bonus = hg_lib.get_config("seal_fracture_bonus") or 200
                    
                    -- === APPLICA BONUS FRATTURE SE ATTIVO ===
                    local base_bonus = hg_lib.get_config("seal_fracture_bonus") or 200
                    local fracture_multiplier = 1.0
                    local has_frac_bonus = hg_lib.has_fracture_bonus()
                    
                    if has_frac_bonus then
                        fracture_multiplier = 1.5
                        bonus = math.floor(base_bonus * fracture_multiplier)
                    else
                        bonus = base_bonus
                    end
                    -- =========================================
                    
                    mysql_direct_query("UPDATE srv1_hunabku.hunter_quest_ranking SET total_points=total_points+" .. bonus .. ", spendable_points=spendable_points+" .. bonus .. " WHERE player_id=" .. pid)
                    
                    -- === AGGIUNGI QUESTO ===
                    hg_lib.on_fracture_seal() -- Conta come frattura sigillata
                    -- =======================

                    -- === SYSCHAT DETTAGLIATO SIGILLO FRATTURA ===
                    syschat("|cffAA00FF========================================|r")
                    syschat("|cffAA00FF  [FRATTURA SIGILLATA]|r |cffFFFFFF" .. fname .. "|r")
                    syschat("|cffAA00FF========================================|r")
                    syschat("")
                    syschat("|cff00FFFF  Gloria Base Sigillo:|r |cffFFFFFF" .. base_bonus .. "|r")
                    if has_frac_bonus then
                        local frac_bonus_val = math.floor(base_bonus * 0.5)
                        syschat("|cffFF6600  Bonus Missioni 3/3 (+50%):|r |cff00FF00+" .. frac_bonus_val .. "|r")
                    end
                    syschat("|cff00FF00  ────────────────────────────────|r")
                    syschat("|cff00FF00  >>> TOTALE: +" .. bonus .. " Gloria <<<|r")
                    syschat("|cffAA00FF========================================|r")
                    -- =============================================
                    
                    local msg = hg_lib.get_text("whatif_sealed", {POINTS = bonus}) or ("FRATTURA SIGILLATA. +" .. bonus .. " GLORIA")
                    hg_lib.hunter_speak_color(msg, fcolor)
                    hg_lib.send_player_data()
                elseif choice == 3 then
                    local msg = hg_lib.get_text("whatif_retreat") or "TI ALLONTANI DALLA FRATTURA."
                    hg_lib.hunter_speak_color(msg, fcolor)
                end
                
                pc.setqf("hq_temp_gate_vnum", 0)
                pc.setqf("hq_temp_gate_freq", 0)
                pc.setqf("hq_temp_player_pts", 0)
                hg_lib.set_temp_gate_data(pid, nil)
            end
        end

        when hq_speedkill_timer.timer begin
            if pc.getqf("hq_speedkill_active") ~= 1 then
                cleartimer("hq_speedkill_timer")
                return
            end
            local start_time = pc.getqf("hq_speedkill_start") or 0
            local duration = pc.getqf("hq_speedkill_duration") or 300
            local elapsed = get_time() - start_time
            local remaining = duration - elapsed
            cmdchat("HunterSpeedKillTimer " .. math.max(0, remaining))
            if remaining <= 0 then
                pc.setqf("hq_speedkill_active", 0)
                cleartimer("hq_speedkill_timer")
                cmdchat("HunterSpeedKillEnd 0")
                
                -- TESTO TIMER SCADUTO (ASCII SAFE)
                local msg = "[!] BONUS VELOCITA' SVANITO (x1 Gloria)"
                hg_lib.hunter_speak_color(msg, "ORANGE")
            end
        end

        when hq_ranking_flush_timer.timer begin
            -- Flush accumulatori ranking su DB
            hg_lib.flush_ranking_updates()
        end

        when hq_event_check_timer.timer begin
            -- Controlla se un evento e finito e fai sorteggio
            hg_lib.check_event_end_and_draw()
        end

        when hq_cleanup_timer.timer begin
            -- Pulizia periodica tabelle globali (previene memory leak)
            hg_lib.cleanup_global_tables()
        end

        when hq_refresh_events_newday.timer begin
            -- Invia la nuova lista eventi del giorno
            hg_lib.send_today_events(false)
        end

        when hq_defense_timer.timer begin
            if pc.getqf("hq_defense_active") ~= 1 then
                cleartimer("hq_defense_timer")
                return
            end

            local start_time = pc.getqf("hq_defense_start") or 0
            local elapsed = get_time() - start_time
            -- Legge la durata specifica per questo rank (salvata in open_gate)
            local duration = pc.getqf("hq_defense_duration") or 60
            
            local last_check = pc.getqf("hq_defense_last_check") or 0
            -- PERFORMANCE FIX: Check distanza ogni 5 secondi (riduce carico CPU)
            local check_interval = hg_lib.get_defense_config("check_interval", 5)

            if get_time() - last_check >= check_interval then
                pc.setqf("hq_defense_last_check", get_time())
                -- Controlla distanza di TUTTI i membri del party
                local all_near, far_member = hg_lib.check_party_defense_distance()
                if not all_near then
                    local reason = far_member and (far_member .. " si e' allontanato!") or "Un membro si e' allontanato!"
                    hg_lib.fail_defense(reason)
                    return
                end
            end

            -- Spawn ondate in base al tempo (PERFORMANCE: usa cache!)
            local pid = pc.get_player_id()
            local frank = "E"
            if hunter_defense_data and hunter_defense_data[pid] then
                frank = hunter_defense_data[pid].rank
            end
            frank = hg_lib.validate_rank(frank)
            local current_wave = pc.getqf("hq_defense_wave") or 0

            -- PERFORMANCE: Leggi dalla cache invece che dal DB (NO QUERY OGNI SECONDO!)
            if _G.hunter_defense_waves_cache and _G.hunter_defense_waves_cache[frank] then
                local waves = _G.hunter_defense_waves_cache[frank]

                -- Itera sulle wave nella cache
                for wave_num, wave_data in pairs(waves) do
                    local spawn_time = wave_data.spawn_time

                    if elapsed >= spawn_time and wave_num > current_wave then
                        hg_lib.spawn_defense_wave(wave_num, frank)
                        pc.setqf("hq_defense_wave", wave_num)
                    end
                end
            end

            if elapsed >= duration then
                -- Leggi TUTTO dalla flag GLOBALE (condivisa, funziona sia SOLO che PARTY)
                local fracture_vid = pc.getqf("hq_defense_fracture_vid") or 0
                local killed = 0
                local total = 0
                
                if fracture_vid > 0 then
                    killed = game.get_event_flag("hq_defense_killed_" .. fracture_vid) or 0
                    total = game.get_event_flag("hq_defense_req_" .. fracture_vid) or 0
                end

                if killed >= total and total > 0 then
                    hg_lib.complete_defense_success()
                else
                    local remaining_mobs = total - killed
                    hg_lib.fail_defense("TEMPO SCADUTO! Mob rimasti: " .. remaining_mobs)
                end
            end
        end

        when button or info begin
            local pid = pc.get_player_id()
            local buy_id = tonumber(game.get_event_flag("hunter_buy_id_"..pid)) or 0
            if buy_id > 0 then 
                game.set_event_flag("hunter_buy_id_"..pid, 0)
                hg_lib.shop_buy_confirm(buy_id)
                return 
            end
            local clm_id = tonumber(game.get_event_flag("hunter_claim_id_"..pid)) or 0
            if clm_id > 0 then 
                game.set_event_flag("hunter_claim_id_"..pid, 0)
                hg_lib.achiev_claim(clm_id)
                return 
            end
            local smart_btn = tonumber(game.get_event_flag("hunter_claim_btn_"..pid)) or 0
            if smart_btn > 0 then 
                game.set_event_flag("hunter_claim_btn_"..pid, 0)
                hg_lib.smart_claim_reward()
                return 
            end
            cmdchat("HunterOpenWindow")
            hg_lib.send_all_data()
        end

        -- NOTA: L'iscrizione agli eventi e' AUTOMATICA quando il player guadagna Gloria
        -- (uccide boss, metin, conquista fratture). Non serve comando manuale.

        when chat."/hunter_request_data" begin 
            hg_lib.send_all_data() 
        end

        when chat."/hunter_refresh_rank" begin
            local pid = pc.get_player_id()
            -- PERFORMANCE: Usa qf invece di query, poi sincronizza
            local pts = pc.getqf("hq_total_points") or 0
            local rank_num = hg_lib.get_rank_index(pts)
            pc.setqf("hq_rank_num", rank_num)
            local rank_key = hg_lib.get_rank_letter(rank_num)
            syschat("[HUNTER] Rank aggiornato: " .. rank_key .. " (" .. pts .. " Gloria)")
        end

        when chat."/htest_msg" with pc.is_gm() begin 
            hg_lib.hunter_speak("TEST MESSAGGIO SISTEMA V36") 
        end

        when chat."/htest_emerg" with pc.is_gm() begin 
            hg_lib.trigger_random_emergency() 
        end

        when chat."/htest_whatif" with pc.is_gm() begin 
            hg_lib.ask_choice_color("gm_test", "Test GM: Scegli", "Opzione A", "Opzione B", "Opzione C", "GOLD")
        end

        when chat."/htest_rival" with pc.is_gm() begin 
            hg_lib.notify_rival("TestRival", 99999, "TestLabel") 
        end

        when chat."/htest_boss" with pc.is_gm() begin 
            cmdchat("HunterBossAlert Demone+della+Frattura") 
        end

        when chat."/htest_init" with pc.is_gm() begin 
            cmdchat("HunterSystemInit") 
        end

        when chat."/htest_awaken" with pc.is_gm() begin 
            cmdchat("HunterAwakening " .. hg_lib.clean_str(pc.get_name())) 
        end

        when chat."/htest_activate" with pc.is_gm() begin 
            cmdchat("HunterActivation " .. hg_lib.clean_str(pc.get_name())) 
        end

        when chat."/htest_rankup" with pc.is_gm() begin 
            cmdchat("HunterRankUp E|D") 
        end

        when chat."/htest_overtake" with pc.is_gm() begin 
            cmdchat("HunterOvertake TestPlayer|3") 
        end

        -- DEBUG: Controlla lo stato del bonus missioni
        when chat."/htest_bonus_status" with pc.is_gm() begin 
            local today = hg_lib.get_today_date()
            local bonus_active = pc.getqf("hq_fracture_bonus_active") or 0
            local bonus_day = pc.getqf("hq_fracture_bonus_day") or "N/A"
            local daily_claimed = pc.getqf("hq_daily_bonus_claimed") or "N/A"
            local has_bonus = hg_lib.has_fracture_bonus()
            
            syschat("|cff00FFFF========== DEBUG BONUS STATUS =========|r")
            syschat("|cffFFFFFFData Oggi: |r|cffFFD700" .. today .. "|r")
            syschat("|cffFFFFFFBonus Active Flag: |r|cffFFD700" .. bonus_active .. "|r")
            syschat("|cffFFFFFFBonus Day: |r|cffFFD700" .. tostring(bonus_day) .. "|r")
            syschat("|cffFFFFFFDaily Claimed: |r|cffFFD700" .. tostring(daily_claimed) .. "|r")
            syschat("|cffFFFFFFhas_fracture_bonus(): |r|cff00FF00" .. tostring(has_bonus) .. "|r")
            syschat("|cff00FFFF==========================================|r")
        end

        -- DEBUG: Attiva manualmente il bonus missioni
        when chat."/htest_activate_bonus" with pc.is_gm() begin 
            hg_lib.activate_fracture_bonus()
            syschat("|cff00FF00[DEBUG]|r Bonus Missioni ATTIVATO manualmente!")
            syschat("|cffFFFFFF+50% Gloria su Boss/Metin/Bauli fino a mezzanotte!|r")
        end

        when chat."/hunter_reset_daily" with pc.is_gm() begin 
            hg_lib.process_daily_reset() 
        end

        when chat."/hunter_reset_weekly" with pc.is_gm() begin 
            hg_lib.process_weekly_reset() 
        end

        when hq_missions_notify.timer begin
            local msg1 = hg_lib.get_text("missions_assigned") or "3 NUOVE MISSIONI GIORNALIERE ASSEGNATE!"
            hg_lib.hunter_speak_color(msg1, "CYAN")
            syschat("|cff00FFFF>> Apri il Terminale Hunter per vederle <<|r")
            syschat("|cffFFAA00   Completale tutte per bonus Gloria x1.5!|r")
        end

        when hq_event_notify.timer begin
            local reward = pc.getqf("hq_event_reward") or 50
            local remaining = pc.getqf("hq_event_remaining") or 30
            local winner = pc.getqf("hq_event_winner") or 200
            local is_registered = pc.getqf("hq_event_registered") or 0

            if is_registered == 1 then
                -- GIA' REGISTRATO - Messaggio in stile Solo Leveling
                syschat("|cff00FFFF=============================================|r")
                syschat("|cffFFD700         [CANDIDATURA ATTIVA]|r")
                syschat("|cff00FFFF=============================================|r")
                syschat("")
                syschat("|cff00FF00   Sei gia' iscritto all'estrazione.|r")
                syschat("|cffFFFFFF   Resta online per scoprire l'esito.|r")
                syschat("")
                syschat("|cffFFD700   Premio in palio: +" .. winner .. " Gloria|r")
                syschat("|cffAAAAAA   Tempo rimanente: " .. remaining .. " minuti|r")
                syschat("")
                syschat("|cff888888   'Il destino premia chi persevera.'|r")
                syschat("|cff00FFFF=============================================|r")
                hg_lib.hunter_speak_color("CANDIDATURA ATTIVA. ATTENDI L'ESITO.", "CYAN")
            else
                -- NON REGISTRATO - Invita a partecipare
                syschat("|cffFFAA00=============================================|r")
                syschat("|cffFFD700         [EVENTO IN CORSO]|r")
                syschat("|cffFFAA00=============================================|r")
                syschat("")
                syschat("|cff00FF00   Guadagna Gloria per candidarti!|r")
                syschat("|cffFFFFFF   Ogni azione ti avvicina al premio.|r")
                syschat("")
                syschat("|cffFFD700   Premio estrazione: +" .. winner .. " Gloria|r")
                syschat("|cffAAAAAA   Tempo rimanente: " .. remaining .. " minuti|r")
                syschat("")
                syschat("|cff888888   'Solo chi combatte puo' vincere.'|r")
                syschat("|cffFFAA00=============================================|r")
                hg_lib.hunter_speak_color("EVENTO ATTIVO! COMBATTI PER ISCRIVERTI!", "GOLD")
            end
        end

        -- QUICK ACCESS: Apre RankUp/GateAccess dalla finestra Trial
        when chat."/hunter_open_rankup" begin
            -- Apre la quest del terminale per RankUp e Gate Access
            -- Invia i dati player e apre la finestra principale
            hg_lib.send_player_data()
            cmdchat("HunterOpenRankUp")
        end

        -- QUICK ACCESS: Apre Missioni ed Eventi dalla finestra Trial
        when chat."/hunter_open_missions_events" begin
            -- Invia i dati delle missioni
            hg_lib.assign_daily_missions()
            hg_lib.send_daily_missions()
            -- Apre la finestra missioni
            cmdchat("HunterMissionsOpen")
            -- Invia e apre gli eventi
            hg_lib.send_today_events(true)
        end

        when chat."/hunter_missions" begin
            hg_lib.assign_daily_missions()
            hg_lib.send_daily_missions()
            cmdchat("HunterMissionsOpen")
        end

        when chat."/hunter_events" begin
            hg_lib.send_today_events(true)
        end

        when chat."/hunter_events_silent" begin
            hg_lib.send_today_events(false)
        end

        -- SHOP - Acquisto oggetti con Gloria
        when chat."/hunter_buy" begin
            local item_id = tonumber(string.gsub(input, "/hunter_buy ", "")) or 0
            if item_id > 0 then
                hg_lib.shop_buy_item(item_id)
            end
        end

        -- ACHIEVEMENTS - Riscuoti ricompensa
        when chat."/hunter_claim" begin
            local ach_id = tonumber(string.gsub(input, "/hunter_claim ", "")) or 0
            if ach_id > 0 then
                hg_lib.claim_achievement(ach_id)
            end
        end

        -- SMART CLAIM - Riscuoti tutte le ricompense disponibili
        when chat."/hunter_smart_claim" begin
            hg_lib.smart_claim_all()
        end

        -- TIMER UNLOCK - Shop lock release
        when hq_shop_unlock.timer begin
            pc.setqf("hq_shop_lock", 0)
        end

        -- TIMER UNLOCK - Achievement lock release
        when hq_ach_unlock.timer begin
            pc.setqf("hq_ach_lock", 0)
        end

        -- TIMER UNLOCK - Smart claim lock release
        when hq_smart_claim_unlock.timer begin
            pc.setqf("hq_smart_claim_lock", 0)
        end

        -- TIMER UNLOCK - Event lock release
        when hq_release_event_lock.timer begin
            local lock_flag = pc.getqf("hq_pending_lock_flag")
            if lock_flag and lock_flag ~= "" and lock_flag ~= 0 then
                game.set_event_flag(lock_flag, 0)
                pc.setqf("hq_pending_lock_flag", 0)
            end
        end

    end
end