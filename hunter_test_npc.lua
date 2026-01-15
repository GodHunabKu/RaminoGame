quest hunter_test_npc begin
    state start begin
    
        when 9009.click with pc.is_gm() begin
            
            local function clean_str(str)
                if str == nil then return "" end
                return string.gsub(tostring(str), " ", "+")
            end
            
            say_title("HUNTER VISUAL DEBUGGER")
            say("")
            say("Pannello completo per testare ogni singola")
            say("animazione Python del sistema Hunter.")
            say("")
            
            local main = select(
                "1. TEST AWAKENING (Livelli)",
                "2. TEST GATE FX (Occhi, Vittoria)",
                "3. TEST RANK UP & SYSTEM",
                "4. TEST MISSIONI & EVENTI",
                "5. TEST NOTIFICHE & ALERT",
                "6. TEST DEFENSE & SPEEDKILL",
                "7. GESTIONE LOGICA (Spawn, DB)",
                "Chiudi"
            )

            -- ============================================================
            -- 1. TEST AWAKENING (TUTTI I LIVELLI)
            -- ============================================================
            if main == 1 then
                say_title("AWAKENING EFFECTS")
                say("")
                say("Scegli la fascia di livello da testare.")
                say("Ogni livello ha un effetto unico!")
                say("")
                
                local awk_cat = select(
                    "Lv 5-30 (Inizio + Sistema)",
                    "Lv 40-80 (Crescita)",
                    "Lv 90-130 (Leggenda + Monarca)",
                    "Indietro"
                )

                if awk_cat == 1 then
                    say_title("AWAKENING LV 5-30")
                    say("")
                    say("Lv 5 = Risveglio Iniziale (Abilita)")
                    say("Lv 30 = Sistema Attivato (Terminale)")
                    say("")
                    local l = select(
                        "Lv 5 - RISVEGLIO (Blu)",
                        "Lv 10 - PRIMA EVOLUZIONE",
                        "Lv 15 - ADATTAMENTO",
                        "Lv 20 - RISONANZA",
                        "Lv 25 - MANIFESTAZIONE",
                        "Lv 30 - SISTEMA ATTIVATO",
                        "Indietro"
                    )
                    if l == 1 then cmdchat("HunterAwakening 5")
                    elseif l == 2 then cmdchat("HunterAwakening 10")
                    elseif l == 3 then cmdchat("HunterAwakening 15")
                    elseif l == 4 then cmdchat("HunterAwakening 20")
                    elseif l == 5 then cmdchat("HunterAwakening 25")
                    elseif l == 6 then cmdchat("HunterAwakening 30")
                    end
                
                elseif awk_cat == 2 then
                    say_title("AWAKENING LV 40-80")
                    say("")
                    local l = select(
                        "Lv 40 - CONSOLIDAMENTO",
                        "Lv 50 - META DEL CAMMINO",
                        "Lv 60 - MATURAZIONE",
                        "Lv 70 - RISVEGLIO AVANZATO",
                        "Lv 80 - MAESTRIA",
                        "Indietro"
                    )
                    if l == 1 then cmdchat("HunterAwakening 40")
                    elseif l == 2 then cmdchat("HunterAwakening 50")
                    elseif l == 3 then cmdchat("HunterAwakening 60")
                    elseif l == 4 then cmdchat("HunterAwakening 70")
                    elseif l == 5 then cmdchat("HunterAwakening 80")
                    end

                elseif awk_cat == 3 then
                    say_title("AWAKENING LV 90-130")
                    say("")
                    say("Lv 100 = ARISE!")
                    say("Lv 130 = I ALONE LEVEL UP")
                    say("")
                    local l = select(
                        "Lv 90 - SOGLIA LEGGENDARIA",
                        "Lv 100 - CENTENARIO (ARISE)",
                        "Lv 110 - TRASCENDENZA",
                        "Lv 120 - ASCENSIONE",
                        "Lv 130 - MONARCA",
                        "Indietro"
                    )
                    if l == 1 then cmdchat("HunterAwakening 90")
                    elseif l == 2 then cmdchat("HunterAwakening 100")
                    elseif l == 3 then cmdchat("HunterAwakening 110")
                    elseif l == 4 then cmdchat("HunterAwakening 120")
                    elseif l == 5 then cmdchat("HunterAwakening 130")
                    end
                end

            -- ============================================================
            -- 2. TEST GATE FX (GLI OCCHI E LE VITTORIE)
            -- ============================================================
            elseif main == 2 then
                say_title("GATE EFFECTS")
                say("")
                say("Testa le animazioni di entrata/uscita Gate")
                say("e gli effetti epici di vittoria/sconfitta.")
                say("")
                
                local g_sel = select(
                    "Entrata: Occhi ROSSI",
                    "Entrata: Occhi VIOLA",
                    "Entrata: Occhi ORO",
                    "Entrata: Occhi BLU",
                    "Vittoria Gate (+Gloria)",
                    "Sconfitta Gate (-Gloria)",
                    "Popup Progresso Trial",
                    "Indietro"
                )

                if g_sel == 1 then
                    cmdchat("HunterGateEntry Gate+E-Rank|RED")
                    syschat("FX: Occhi Rossi inviati")
                elseif g_sel == 2 then
                    cmdchat("HunterGateEntry Gate+A-Rank|PURPLE")
                    syschat("FX: Occhi Viola inviati")
                elseif g_sel == 3 then
                    cmdchat("HunterGateEntry Gate+S-Rank|GOLD")
                    syschat("FX: Occhi Oro inviati")
                elseif g_sel == 4 then
                    cmdchat("HunterGateEntry Gate+B-Rank|BLUE")
                    syschat("FX: Occhi Blu inviati")
                elseif g_sel == 5 then
                    cmdchat("HunterGateVictory Gate+Completato|5000")
                    syschat("FX: Vittoria inviata")
                elseif g_sel == 6 then
                    cmdchat("HunterGateDefeat 250")
                    syschat("FX: Sconfitta inviata")
                elseif g_sel == 7 then
                    say_title("TRIAL PROGRESS")
                    say("")
                    local prog = select(
                        "Boss 1/5",
                        "Metin 3/10",
                        "Fratture 2/3",
                        "Bauli 4/5",
                        "Missioni 2/3",
                        "Indietro"
                    )
                    if prog == 1 then cmdchat("HunterTrialProgressPopup boss|1|5")
                    elseif prog == 2 then cmdchat("HunterTrialProgressPopup metin|3|10")
                    elseif prog == 3 then cmdchat("HunterTrialProgressPopup fracture|2|3")
                    elseif prog == 4 then cmdchat("HunterTrialProgressPopup chest|4|5")
                    elseif prog == 5 then cmdchat("HunterTrialProgressPopup mission|2|3")
                    end
                end

            -- ============================================================
            -- 3. TEST RANK UP & SYSTEM
            -- ============================================================
            elseif main == 3 then
                say_title("RANK UP & SYSTEM")
                say("")
                say("Testa le animazioni di promozione rank")
                say("e gli effetti di sistema.")
                say("")
                
                local sys_sel = select(
                    "Rank Up: E -> D",
                    "Rank Up: D -> C",
                    "Rank Up: C -> B",
                    "Rank Up: B -> A",
                    "Rank Up: A -> S",
                    "Rank Up: S -> N (MONARCA)",
                    "System Init (Login)",
                    "Boss Alert",
                    "Overtake (Sorpasso)",
                    "Indietro"
                )

                if sys_sel == 1 then cmdchat("HunterRankUp E|D")
                elseif sys_sel == 2 then cmdchat("HunterRankUp D|C")
                elseif sys_sel == 3 then cmdchat("HunterRankUp C|B")
                elseif sys_sel == 4 then cmdchat("HunterRankUp B|A")
                elseif sys_sel == 5 then cmdchat("HunterRankUp A|S")
                elseif sys_sel == 6 then cmdchat("HunterRankUp S|N")
                elseif sys_sel == 7 then cmdchat("HunterSystemInit")
                elseif sys_sel == 8 then 
                    say_title("BOSS ALERT")
                    say("")
                    local boss = select(
                        "Re dei Demoni",
                        "Drago Nero",
                        "Signore delle Ombre",
                        "Indietro"
                    )
                    if boss == 1 then cmdchat("HunterBossAlert Re+dei+Demoni")
                    elseif boss == 2 then cmdchat("HunterBossAlert Drago+Nero")
                    elseif boss == 3 then cmdchat("HunterBossAlert Signore+delle+Ombre")
                    end
                elseif sys_sel == 9 then
                    cmdchat("HunterOvertake TopPlayer|3")
                    syschat("FX: Sorpasso inviato")
                end

            -- ============================================================
            -- 4. TEST MISSIONI & EVENTI
            -- ============================================================
            elseif main == 4 then
                say_title("MISSIONI & EVENTI")
                say("")
                
                local ui_sel = select(
                    "Progresso Missione (1/10)",
                    "Progresso Missione (5/10)",
                    "Missione Completata",
                    "Tutte le Missioni Complete",
                    "Evento Joined (Iscritto)",
                    "Evento Status Widget",
                    "Apri Pannello Missioni",
                    "Apri Pannello Eventi",
                    "Indietro"
                )

                if ui_sel == 1 then 
                    cmdchat("HunterMissionProgress 1|1|10")
                    syschat("UI: Progresso missione 1/10")
                elseif ui_sel == 2 then 
                    cmdchat("HunterMissionProgress 1|5|10")
                    syschat("UI: Progresso missione 5/10")
                elseif ui_sel == 3 then 
                    cmdchat("HunterMissionComplete 1|Uccidi+10+Orchi|100")
                    syschat("UI: Missione completata")
                elseif ui_sel == 4 then 
                    cmdchat("HunterAllMissionsComplete 500|FRACTURE_BONUS_ACTIVE")
                    syschat("UI: Tutte le missioni complete!")
                elseif ui_sel == 5 then 
                    cmdchat("HunterEventJoined 1|Glory+Rush|150")
                    syschat("UI: Iscritto a evento")
                elseif ui_sel == 6 then 
                    cmdchat("HunterEventStatus Glory+Rush|120|glory_rush|Guadagna+piu+Gloria+possibile!|+100+Gloria")
                    syschat("UI: Widget evento attivo")
                elseif ui_sel == 7 then 
                    -- Prima invia i dati delle missioni, poi apre il pannello
                    hg_lib.send_daily_missions()
                    cmdchat("HunterMissionsOpen")
                elseif ui_sel == 8 then 
                    cmdchat("HunterEventsOpen")
                end

            -- ============================================================
            -- 5. TEST NOTIFICHE & ALERT
            -- ============================================================
            elseif main == 5 then
                say_title("NOTIFICHE & ALERT")
                say("")
                
                local notif_sel = select(
                    "System Speak (Messaggio)",
                    "Welcome Message",
                    "WhatIf Dialog",
                    "Sys Message (Colorato)",
                    "Rival Alert",
                    "Indietro"
                )

                if notif_sel == 1 then
                    say_title("SYSTEM SPEAK")
                    say("")
                    local msg_sel = select(
                        "Messaggio E-Rank",
                        "Messaggio A-Rank",
                        "Messaggio S-Rank",
                        "Messaggio N-Rank",
                        "Indietro"
                    )
                    if msg_sel == 1 then cmdchat("HunterSystemSpeak E|Benvenuto+nel+sistema")
                    elseif msg_sel == 2 then cmdchat("HunterSystemSpeak A|Il+tuo+potere+cresce")
                    elseif msg_sel == 3 then cmdchat("HunterSystemSpeak S|Sei+tra+i+migliori")
                    elseif msg_sel == 4 then cmdchat("HunterSystemSpeak N|IO+SONO+IL+MONARCA")
                    end
                elseif notif_sel == 2 then
                    local name = clean_str(pc.get_name())
                    cmdchat("HunterWelcome A|" .. name .. "|15000")
                    syschat("UI: Welcome message inviato")
                elseif notif_sel == 3 then
                    cmdchat("HunterWhatIf 1|Vuoi+accettare+la+sfida?|Accetta|Rifiuta||PURPLE")
                    syschat("UI: WhatIf dialog aperto")
                elseif notif_sel == 4 then
                    say_title("SYS MESSAGE")
                    say("")
                    local col = select(
                        "Viola (PURPLE)",
                        "Oro (GOLD)",
                        "Rosso (RED)",
                        "Blu (BLUE)",
                        "Indietro"
                    )
                    if col == 1 then cmdchat("HunterSysMsg Test+messaggio+sistema|PURPLE")
                    elseif col == 2 then cmdchat("HunterSysMsg Test+messaggio+sistema|GOLD")
                    elseif col == 3 then cmdchat("HunterSysMsg Test+messaggio+sistema|RED")
                    elseif col == 4 then cmdchat("HunterSysMsg Test+messaggio+sistema|BLUE")
                    end
                elseif notif_sel == 5 then
                    cmdchat("HunterRivalAlert TopRival|12500|Gloria|VICINO")
                    syschat("UI: Rival alert inviato")
                end

            -- ============================================================
            -- 6. TEST DEFENSE & SPEEDKILL
            -- ============================================================
            elseif main == 6 then
                say_title("DEFENSE & SPEEDKILL")
                say("")
                say("Testa i sistemi di difesa frattura")
                say("e le sfide speed kill.")
                say("")
                
                local def_sel = select(
                    "Fracture Defense Start",
                    "Fracture Defense Timer",
                    "Fracture Defense Complete (Win)",
                    "Fracture Defense Complete (Fail)",
                    "Speed Kill Start",
                    "Speed Kill Timer",
                    "Speed Kill End (Bonus)",
                    "Speed Kill End (No Bonus)",
                    "Emergency Quest Start",
                    "Emergency Quest Update",
                    "Emergency Quest Close",
                    "Indietro"
                )

                if def_sel == 1 then
                    cmdchat("HunterFractureDefenseStart Frattura+Dimensionale|60|PURPLE")
                    syschat("FX: Defense start")
                elseif def_sel == 2 then
                    cmdchat("HunterFractureDefenseTimer 30")
                    syschat("FX: Timer 30s")
                elseif def_sel == 3 then
                    cmdchat("HunterFractureDefenseComplete 1|Difesa+Completata!")
                    syschat("FX: Defense win")
                elseif def_sel == 4 then
                    cmdchat("HunterFractureDefenseComplete 0|Difesa+Fallita!")
                    syschat("FX: Defense fail")
                elseif def_sel == 5 then
                    cmdchat("HunterSpeedKillStart BOSS|30|RED")
                    syschat("FX: Speed kill start")
                elseif def_sel == 6 then
                    cmdchat("HunterSpeedKillTimer 15")
                    syschat("FX: Timer 15s")
                elseif def_sel == 7 then
                    cmdchat("HunterSpeedKillEnd 1|500")
                    syschat("FX: Speed kill bonus!")
                elseif def_sel == 8 then
                    cmdchat("HunterSpeedKillEnd 0|0")
                    syschat("FX: Speed kill no bonus")
                elseif def_sel == 9 then
                    cmdchat("HunterEmergency Invasione+Demoniaca|60|6790|10")
                    syschat("FX: Emergency start")
                elseif def_sel == 10 then
                    cmdchat("HunterEmergencyUpdate 5")
                    syschat("FX: Emergency update: 5 kills")
                elseif def_sel == 11 then
                    say_title("EMERGENCY CLOSE")
                    say("")
                    local ec = select("SUCCESS", "FAIL", "TIMEOUT", "Indietro")
                    if ec == 1 then cmdchat("HunterEmergencyClose SUCCESS")
                    elseif ec == 2 then cmdchat("HunterEmergencyClose FAIL")
                    elseif ec == 3 then cmdchat("HunterEmergencyClose TIMEOUT")
                    end
                end

            -- ============================================================
            -- 7. GESTIONE LOGICA (SPAWN, DB)
            -- ============================================================
            elseif main == 7 then
                say_title("LOGICA SERVER")
                say("")
                say("Spawn mob e gestione database.")
                say("")
                
                local log_sel = select(
                    "Spawn Frattura (E/D/C)",
                    "Spawn Frattura (B/A/S/N)",
                    "TEST POWER RANK",
                    "Spawn Metin Hunter",
                    "Spawn Boss Alastor",
                    "Assegna Missioni Giornaliere",
                    "Reset Missioni Giornaliere",
                    "Wipe Dati Player (ATTENZIONE)",
                    "Indietro"
                )
                
                if log_sel == 1 then 
                    say_title("FRATTURE E/D/C")
                    say("")
                    say("Queste fratture usano il sistema classico:")
                    say("Party di 4+ membri per forzare.")
                    say("")
                    local fr = select("E-Rank (16060)", "D-Rank (16061)", "C-Rank (16062)", "Indietro")
                    if fr == 1 then mob.spawn(16060, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura E-Rank")
                    elseif fr == 2 then mob.spawn(16061, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura D-Rank")
                    elseif fr == 3 then mob.spawn(16062, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura C-Rank")
                    end
                    
                elseif log_sel == 2 then 
                    say_title("FRATTURE B/A/S/N")
                    say("")
                    say("Queste fratture usano il POWER RANK!")
                    say("(Valori letti dal database)")
                    say("")
                    local fr = select("B-Rank (16063)", "A-Rank (16064)", "S-Rank (16065)", "N-Rank (16066)", "Indietro")
                    if fr == 1 then mob.spawn(16063, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura B-Rank")
                    elseif fr == 2 then mob.spawn(16064, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura A-Rank")
                    elseif fr == 3 then mob.spawn(16065, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura S-Rank")
                    elseif fr == 4 then mob.spawn(16066, pc.get_local_x(), pc.get_local_y(), 1) syschat("SPAWN: Frattura N-Rank")
                    end
                    
                elseif log_sel == 3 then
                    -- Test Power Rank
                    say_title("POWER RANK TEST")
                    say("")
                    
                    local my_grade = hg_lib.get_player_rank_grade(pc.get_player_id())
                    local my_power = hg_lib.get_player_power_rank(pc.get_player_id())
                    local party_power, members = hg_lib.get_party_power_rank()
                    
                    say("Il tuo grado: " .. (my_grade or "NONE"))
                    say("Il tuo Power Rank: " .. my_power .. " punti")
                    say("")
                    say("Power Rank Party: " .. party_power .. " punti")
                    say("Membri nel party vicini: " .. table.getn(members))
                    say("")
                    say("VALORI PR: E=1|D=5|C=15|B=40|A=80|S=150|N=250")
                    say("")
                    
                    local test_what = select(
                        "Testa Frattura B (16063)",
                        "Testa Frattura A (16064)",
                        "Testa Frattura S (16065)",
                        "Testa Frattura N (16066)",
                        "Indietro"
                    )
                    
                    local test_vnums = {16063, 16064, 16065, 16066}
                    if test_what >= 1 and test_what <= 4 then
                        local vnum = test_vnums[test_what]
                        local can_force, force_type, total_pr, required_pr, members_list = hg_lib.can_force_fracture(vnum)
                        
                        say_title("RISULTATO TEST")
                        say("")
                        say("Frattura testata: VNUM " .. vnum)
                        say("Tipo forzatura: " .. (force_type or "N/A"))
                        
                        if force_type == "POWER_RANK" then
                            say("Power Rank totale: " .. (total_pr or 0) .. " / " .. (required_pr or 0) .. " richiesti")
                            say("Membri validi: " .. (members_list and table.getn(members_list) or 0))
                            say("")
                            if can_force then
                                say("[OK] Puoi forzare questa frattura!")
                            else
                                say("[X] NON puoi forzare!")
                                say("Mancano " .. ((required_pr or 0) - (total_pr or 0)) .. " PR")
                            end
                        else
                            say("Questa frattura usa Party 4+")
                            say("")
                            if can_force then
                                say("[OK] Hai un party di 4+ membri!")
                            else
                                say("[X] Servono 4 membri nel party!")
                            end
                        end
                    end
                    
                elseif log_sel == 4 then 
                    mob.spawn(63013, pc.get_local_x(), pc.get_local_y(), 1)
                    syschat("SPAWN: Metin Hunter")
                elseif log_sel == 5 then 
                    mob.spawn(6790, pc.get_local_x(), pc.get_local_y(), 1)
                    syschat("SPAWN: Boss Alastor")
                elseif log_sel == 6 then 
                    -- Usa la funzione della libreria che assegna E invia le missioni
                    hg_lib.assign_daily_missions()
                    syschat("DB: Missioni assegnate e inviate al client")
                elseif log_sel == 7 then
                    mysql_direct_query("DELETE FROM srv1_hunabku.hunter_player_missions WHERE player_id=" .. pc.get_player_id() .. " AND assigned_date=CURDATE()")
                    syschat("DB: Missioni resettate")
                elseif log_sel == 8 then
                    say_title("!!! ATTENZIONE !!!")
                    say("")
                    say("Stai per CANCELLARE tutti i tuoi dati Hunter!")
                    say("Rank, Gloria, Missioni, Trial, tutto PERSO!")
                    say("")
                    local confirm = select("Si, cancella tutto", "No, annulla")
                    if confirm == 1 then
                        local pid = pc.get_player_id()
                        mysql_direct_query("DELETE FROM srv1_hunabku.hunter_quest_ranking WHERE player_id="..pid)
                        mysql_direct_query("DELETE FROM srv1_hunabku.hunter_player_missions WHERE player_id="..pid)
                        mysql_direct_query("DELETE FROM srv1_hunabku.hunter_player_trials WHERE player_id="..pid)
                        pc.setqf("hq_intro", 0)
                        pc.setqf("hq_rank_num", 0)
                        pc.setqf("hq_level", 0)
                        syschat("DB: Player resettato. Rilogga per applicare.")
                    end
                end
            end
        end
    end
end
