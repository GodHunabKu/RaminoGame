-- =================================================================
-- HUNTER ITEMS HANDLER (Versione Creativa + Multi-Language)
--
-- Ogni oggetto ora ha un feedback testuale piu' ricco e immersivo,
-- in linea con il tema del sistema Hunter.
-- Supporto multi-lingua tramite hg_lib.get_text()
-- =================================================================

quest hunter_items begin
    state start begin

        -- Item: Scanner di Fratture (Evoca Subito)
        when 50160.use begin
            local msg = hg_lib.get_text("ITEM_SCANNER_ACTIVE", nil, "Scanner in funzione... Frattura rilevata!")
            hg_lib.hunter_speak_color(msg, "BLUE")
            hg_lib.spawn_fracture()
            item.remove()
        end

        -- Item: Stabilizzatore di Rango (Scegli Rank)
        when 50161.use begin
            say_title(hg_lib.get_text("ITEM_STABILIZER_TITLE", nil, "STABILIZZATORE DI RANGO"))
            say("")
            say(hg_lib.get_text("ITEM_STABILIZER_DESC1", nil, "L'artefatto risuona, pronto a piegare la realta'."))
            say(hg_lib.get_text("ITEM_STABILIZER_DESC2", nil, "Focalizzati sull'energia che desideri richiamare."))
            say("")

            -- PERFORMANCE: Usa la cache invece di query
            local cached = hg_lib.get_fractures_cached()
            if not cached or cached.count == 0 then
                syschat("[HUNTER] " .. hg_lib.get_text("ITEM_NO_FRACTURES", nil, "Nessuna frattura disponibile nei registri."))
                return
            end

            local options, data = {}, {}
            for i = 1, cached.count do
                local f = cached.data[i]
                table.insert(options, hg_lib.get_text("RANK", nil, "Rango") .. " " .. f.rank_label)
                table.insert(data, {vnum = tonumber(f.vnum), rank = f.rank_label, color = f.color_code})
            end
            table.insert(options, hg_lib.get_text("CANCEL", nil, "Annulla"))

            local s = select_table(options)
            if s <= table.getn(data) then
                local choice = data[s]
                local x, y = pc.get_local_x(), pc.get_local_y()
                mob.spawn(choice.vnum, x + 3, y + 3, 1)
                hg_lib.add_fracture_ping(x + 3, y + 3)
                syschat("[HUNTER] " .. hg_lib.get_text("ITEM_FRACTURE_SUMMONED", {RANK = choice.rank}, "Frattura " .. choice.rank .. " evocata!"))
                item.remove()
            end
        end

        -- Item: Focus del Cacciatore (+20% Gloria)
        when 50162.use begin
            local pid = pc.get_player_id()
            game.set_event_flag("hq_hunter_focus_"..pid, 1)
            local speak_msg = hg_lib.get_text("ITEM_FOCUS_SPEAK", nil, "I tuoi sensi si acuiscono. Il flusso di Gloria dalla prossima minaccia sara' amplificato.")
            hg_lib.hunter_speak_color(speak_msg, "GOLD")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_FOCUS_SYSCHAT", nil, "Effetto Focus attivo: la tua percezione delle ricompense e' aumentata."))
            item.remove()
        end

        -- Item: Chiave Dimensionale (Forza Baule)
        when 50163.use begin
            local pid = pc.get_player_id()
            game.set_event_flag("hq_force_chest_"..pid, 1)
            local speak_msg = hg_lib.get_text("ITEM_DIMKEY_SPEAK", nil, "La Chiave Dimensionale si attiva... Il prossimo baule rivelera' i suoi tesori nascosti!")
            hg_lib.hunter_speak_color(speak_msg, "GOLD")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_DIMKEY_SYSCHAT", nil, "Il prossimo baule garantira' un bonus Gloria extra!"))
            item.remove()
        end

        -- Item: Sigillo di Conquista (Salta Difesa)
        when 50164.use begin
            local pid = pc.get_player_id()
            game.set_event_flag("hq_force_conquest_"..pid, 1)
            local speak_msg = hg_lib.get_text("ITEM_SEAL_SPEAK", nil, "Il Sigillo pulsa con potere... La prossima Frattura che toccherai verra' immediatamente soggiogata.")
            hg_lib.hunter_speak_color(speak_msg, "PURPLE")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_SEAL_SYSCHAT", nil, "L'energia del Sigillo ti permettera' di saltare la fase di difesa."))
            item.remove()
        end

        -- Item: Segnale d'Emergenza (Forza Speed Kill)
        when 50165.use begin
            local pid = pc.get_player_id()
            game.set_event_flag("hq_force_speedkill_"..pid, 1)
            local speak_msg = hg_lib.get_text("ITEM_SIGNAL_SPEAK", nil, "Il segnale inviato al Sistema. La prossima minaccia sara' designata come bersaglio ad alta priorita'.")
            hg_lib.hunter_speak_color(speak_msg, "RED")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_SIGNAL_SYSCHAT", nil, "Una Missione d'Emergenza verra' attivata contro il prossimo bersaglio Elite."))
            item.remove()
        end

        -- Item: Risonatore di Gruppo (Party Focus)
        when 50166.use begin
            if not party.is_party() then
                syschat("[HUNTER] " .. hg_lib.get_text("ITEM_RESONATOR_NOPARTY", nil, "Devi essere in un party per usare questo oggetto!"))
                return
            end

            -- Applica focus usando il PID del LEADER (cosi' tutti nel party ne beneficiano)
            local leader_pid = party.get_leader_pid()
            game.set_event_flag("hq_party_focus_"..leader_pid, 1)

            local speak_msg = hg_lib.get_text("ITEM_RESONATOR_SPEAK", nil, "RISONANZA DI GRUPPO ATTIVATA! +20% Gloria per il party sulla prossima kill elite!")
            hg_lib.hunter_speak_color(speak_msg, "CYAN")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_RESONATOR_SYSCHAT", nil, "Risonatore attivato! Il party riceve +20% Gloria sulla prossima kill elite!"))
            item.remove()
        end

        -- Item: Calibratore di Probabilita' (Garantisce Rango C+)
        when 50167.use begin
            local pid = pc.get_player_id()
            game.set_event_flag("hq_fracture_rank_"..pid, 1)
            local speak_msg = hg_lib.get_text("ITEM_CALIBRATOR_SPEAK", nil, "Il Calibratore altera le costanti. Le anomalie di basso livello verranno filtrate dal prossimo scan.")
            hg_lib.hunter_speak_color(speak_msg, "ORANGE")
            syschat("[HUNTER] " .. hg_lib.get_text("ITEM_CALIBRATOR_SYSCHAT", nil, "Il Calibratore e' attivo: la prossima frattura casuale sara' di Rango C o superiore."))
            item.remove()
        end

        -- Item: Frammento di Monarca (S-Rank + Focus)
        when 50168.use begin
            -- PERFORMANCE: Usa la cache invece di query
            local cached = hg_lib.get_fractures_cached()
            local s_rank_fractures = {}

            if cached and cached.count > 0 then
                for i = 1, cached.count do
                    local f = cached.data[i]
                    if string.find(f.rank_label, "S-Rank") then
                        table.insert(s_rank_fractures, f)
                    end
                end
            end

            if table.getn(s_rank_fractures) > 0 then
                -- Seleziona casualmente una S-Rank
                local choice = s_rank_fractures[number(1, table.getn(s_rank_fractures))]
                local x, y = pc.get_local_x(), pc.get_local_y()

                mob.spawn(tonumber(choice.vnum), x + 3, y + 3, 1)
                hg_lib.add_fracture_ping(x + 3, y + 3)

                local msg = hg_lib.get_text("ITEM_MONARCH_DETECTED", {RANK = choice.rank_label}, "Potere assoluto. Una Frattura "..choice.rank_label.." squarcia la realta'.")
                hg_lib.hunter_speak_color(msg, choice.color_code or "PURPLE")

                -- Applica anche il focus
                local pid = pc.get_player_id()
                game.set_event_flag("hq_hunter_focus_"..pid, 1)
                hg_lib.hunter_speak_color(hg_lib.get_text("FOCUS_ACTIVE", nil, "FOCUS ATTIVO."), "GOLD")

                item.remove()
            else
                hg_lib.hunter_speak(hg_lib.get_text("ITEM_NO_SRANK", nil, "Nessuna Frattura di Rango S trovata nei registri del Sistema."))
            end
        end
    end
end
