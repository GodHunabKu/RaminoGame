# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
 HUNTER SYSTEM - FRACTURE PORTAL WINDOW
 UI immersiva per preview frattura con effetto "risucchio"
 
 Caratteristiche:
 - Dimensione scala con il rank (E=piccola, N=enorme)
 - Colori basati sul tema della frattura
 - Effetti pulsanti e animazioni
 - Preview requisiti, ricompense e penalità
═══════════════════════════════════════════════════════════════════════════════
"""

import ui
import wndMgr
import app
import net
import math
import uiQuest # Necessario per il fix monkey patch
import dbg

# ═══════════════════════════════════════════════════════════════════════════════
#  MONKEY PATCH: Fix Crash uiQuest.py (AttributeError in OnInput)
#  La funzione standard OnInput crasha con setskin(NOWINDOW) su questo client.
#  Avvolgiamo la funzione originale per ignorare l'errore specifico.
# ═══════════════════════════════════════════════════════════════════════════════
try:
    if hasattr(uiQuest.QuestDialog, 'OnInput') and not hasattr(uiQuest.QuestDialog, 'OriginalOnInput'):
        uiQuest.QuestDialog.OriginalOnInput = uiQuest.QuestDialog.OnInput
        
        def SafeOnInput(self, *args, **kwargs):
            try:
                return self.OriginalOnInput(*args, **kwargs)
            except AttributeError:
                # Ignora crash SetParent(None) -> 'NoneType' object has no attribute 'hWnd'
                pass
            except Exception as e:
                dbg.TraceError("uiQuest SafeOnInput ignored error: " + str(e))
                
        uiQuest.QuestDialog.OnInput = SafeOnInput
except:
    pass
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIGURAZIONE RANK - Dimensioni e intensità per ogni rank
# ═══════════════════════════════════════════════════════════════════════════════
RANK_CONFIG = {
    "E": {
        "name": "E-RANK",
        "subtitle": "Frattura Minore",
        "width": 380,
        "height": 320,
        "glow_intensity": 0.4,
        "pulse_speed": 1.5,
        "border_width": 2,
        "particle_count": 3,
    },
    "D": {
        "name": "D-RANK", 
        "subtitle": "Frattura Instabile",
        "width": 400,
        "height": 350,
        "glow_intensity": 0.5,
        "pulse_speed": 1.8,
        "border_width": 2,
        "particle_count": 4,
    },
    "C": {
        "name": "C-RANK",
        "subtitle": "Frattura Pericolosa",
        "width": 420,
        "height": 380,
        "glow_intensity": 0.6,
        "pulse_speed": 2.0,
        "border_width": 3,
        "particle_count": 5,
    },
    "B": {
        "name": "B-RANK",
        "subtitle": "Frattura Letale",
        "width": 450,
        "height": 420,
        "glow_intensity": 0.7,
        "pulse_speed": 2.2,
        "border_width": 3,
        "particle_count": 6,
    },
    "A": {
        "name": "A-RANK",
        "subtitle": "Frattura Catastrofica",
        "width": 480,
        "height": 460,
        "glow_intensity": 0.8,
        "pulse_speed": 2.5,
        "border_width": 4,
        "particle_count": 7,
    },
    "S": {
        "name": "S-RANK",
        "subtitle": "Frattura Apocalittica",
        "width": 520,
        "height": 500,
        "glow_intensity": 0.9,
        "pulse_speed": 3.0,
        "border_width": 4,
        "particle_count": 8,
    },
    "N": {
        "name": "NAZIONALE",
        "subtitle": "Frattura del Monarca",
        "width": 560,
        "height": 540,
        "glow_intensity": 1.0,
        "pulse_speed": 3.5,
        "border_width": 5,
        "particle_count": 10,
    },
}

# Schemi colori per fratture
FRACTURE_COLORS = {
    "GREEN": {
        "primary": 0xFF00FF00,
        "secondary": 0xFF00AA00,
        "glow": 0x6600FF00,
        "bg": 0xF0021002,
        "text": 0xFF88FF88,
        "accent": 0xFF44FF44,
    },
    "BLUE": {
        "primary": 0xFF0099FF,
        "secondary": 0xFF0066CC,
        "glow": 0x660099FF,
        "bg": 0xF0010208,
        "text": 0xFF88CCFF,
        "accent": 0xFF44AAFF,
    },
    "ORANGE": {
        "primary": 0xFFFF6600,
        "secondary": 0xFFCC4400,
        "glow": 0x66FF6600,
        "bg": 0xF0080401,
        "text": 0xFFFFAA66,
        "accent": 0xFFFF8833,
    },
    "RED": {
        "primary": 0xFFFF0000,
        "secondary": 0xFFCC0000,
        "glow": 0x66FF0000,
        "bg": 0xF0080101,
        "text": 0xFFFF6666,
        "accent": 0xFFFF3333,
    },
    "GOLD": {
        "primary": 0xFFFFD700,
        "secondary": 0xFFCCAA00,
        "glow": 0x66FFD700,
        "bg": 0xF0080601,
        "text": 0xFFFFEE88,
        "accent": 0xFFFFDD44,
    },
    "PURPLE": {
        "primary": 0xFF9900FF,
        "secondary": 0xFF6600CC,
        "glow": 0x669900FF,
        "bg": 0xF0040108,
        "text": 0xFFCC88FF,
        "accent": 0xFFBB44FF,
    },
    "BLACKWHITE": {
        "primary": 0xFFFFFFFF,
        "secondary": 0xFFAAAAAA,
        "glow": 0x66FFFFFF,
        "bg": 0xF0050505,
        "text": 0xFFDDDDDD,
        "accent": 0xFFEEEEEE,
    },
}


class FracturePortalWindow(ui.Window):
    """
    Finestra preview frattura con effetto portale/risucchio
    Dimensione e intensità scalano con il rank
    """
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        
        # Dati frattura
        self.fractureName = ""
        self.fractureRank = "E"
        self.fractureColor = "PURPLE"
        self.fractureVnum = 0
        self.reqGlory = 0
        self.reqPowerRank = 0
        self.canEnter = False
        self.canForce = False
        self.playerGlory = 0
        self.partyPowerRank = 0
        self.rewards = []
        self.sealBonus = 200
        
        # Animazione
        self.startTime = 0
        self.pulsePhase = 0.0
        self.vortexAngle = 0.0
        self.isClosing = False
        self.closeStartTime = 0
        
        # UI elements
        self.elements = {}
        self.particles = []
        
        self.Hide()
    
    def __del__(self):
        self.Destroy()
        ui.Window.__del__(self)
    
    def CleanupUI(self):
        """Helper per pulire completamente le risorse UI"""
        # Pulisci particelle
        if self.particles:
            for p in self.particles:
                if p and p.get("bar"):
                    p["bar"].Hide()
                    # p["bar"].SetParent(None) # CRASH FIX: Client non supporta None
                    p["bar"] = None
        self.particles = []
        
        # Pulisci elementi UI
        if self.elements:
            for key in self.elements:
                elem = self.elements[key]
                if elem:
                    if hasattr(elem, 'Hide'): elem.Hide()
                    if hasattr(elem, 'SetEvent'): elem.SetEvent(None)
                    # if hasattr(elem, 'SetParent'): elem.SetParent(None) # CRASH FIX
                    # Alcuni elementi complessi (Grid, ecc) hanno Destroy
                    if hasattr(elem, 'Destroy'): elem.Destroy()
        self.elements = {}

    def Destroy(self):
        """Pulisce tutte le risorse per evitare memory leaks"""
        self.CleanupUI()
    
    def RestoreGameUI(self):
        """Ripristina la UI del gioco dopo la chiusura della finestra portale"""
        try:
            # Usa la funzione globale in hunter.py che ha il riferimento all'interfaccia
            import hunter
            hunter.RestoreGameInterface()
        except Exception as e:
            import dbg
            dbg.TraceError("FracturePortal.RestoreGameUI error: " + str(e))
        
    def BuildUI(self):
        """Costruisce la UI basata sul rank e colore corrente"""
        # Pulisci elementi precedenti
        self.CleanupUI()
        
        # Ottieni configurazione rank
        rankCfg = RANK_CONFIG.get(self.fractureRank, RANK_CONFIG["E"])
        colors = FRACTURE_COLORS.get(self.fractureColor, FRACTURE_COLORS["PURPLE"])
        
        w = rankCfg["width"]
        h = rankCfg["height"]
        borderW = rankCfg["border_width"]
        
        self.SetSize(w, h)
        self.SetPosition((self.screenWidth - w) // 2, (self.screenHeight - h) // 2)
        
        # ═══════════════════════════════════════════════════════════════════
        # LAYER 1: Glow esterno (effetto alone)
        # ═══════════════════════════════════════════════════════════════════
        glowSize = 20
        self.elements["glow_outer"] = ui.Bar()
        self.elements["glow_outer"].SetParent(self)
        self.elements["glow_outer"].SetPosition(-glowSize, -glowSize)
        self.elements["glow_outer"].SetSize(w + glowSize*2, h + glowSize*2)
        self.elements["glow_outer"].SetColor(colors["glow"])
        self.elements["glow_outer"].AddFlag("not_pick")
        self.elements["glow_outer"].Show()
        
        # ═══════════════════════════════════════════════════════════════════
        # LAYER 2: Background principale scuro
        # ═══════════════════════════════════════════════════════════════════
        self.elements["bg"] = ui.Bar()
        self.elements["bg"].SetParent(self)
        self.elements["bg"].SetPosition(0, 0)
        self.elements["bg"].SetSize(w, h)
        self.elements["bg"].SetColor(colors["bg"])
        self.elements["bg"].AddFlag("not_pick")
        self.elements["bg"].Show()
        
        # ═══════════════════════════════════════════════════════════════════
        # LAYER 3: Bordi animati (vortice)
        # ═══════════════════════════════════════════════════════════════════
        # Bordo top
        self.elements["border_top"] = ui.Bar()
        self.elements["border_top"].SetParent(self)
        self.elements["border_top"].SetPosition(0, 0)
        self.elements["border_top"].SetSize(w, borderW)
        self.elements["border_top"].SetColor(colors["primary"])
        self.elements["border_top"].AddFlag("not_pick")
        self.elements["border_top"].Show()
        
        # Bordo bottom
        self.elements["border_bottom"] = ui.Bar()
        self.elements["border_bottom"].SetParent(self)
        self.elements["border_bottom"].SetPosition(0, h - borderW)
        self.elements["border_bottom"].SetSize(w, borderW)
        self.elements["border_bottom"].SetColor(colors["primary"])
        self.elements["border_bottom"].AddFlag("not_pick")
        self.elements["border_bottom"].Show()
        
        # Bordo left
        self.elements["border_left"] = ui.Bar()
        self.elements["border_left"].SetParent(self)
        self.elements["border_left"].SetPosition(0, 0)
        self.elements["border_left"].SetSize(borderW, h)
        self.elements["border_left"].SetColor(colors["primary"])
        self.elements["border_left"].AddFlag("not_pick")
        self.elements["border_left"].Show()
        
        # Bordo right
        self.elements["border_right"] = ui.Bar()
        self.elements["border_right"].SetParent(self)
        self.elements["border_right"].SetPosition(w - borderW, 0)
        self.elements["border_right"].SetSize(borderW, h)
        self.elements["border_right"].SetColor(colors["primary"])
        self.elements["border_right"].AddFlag("not_pick")
        self.elements["border_right"].Show()
        
        # ═══════════════════════════════════════════════════════════════════
        # LAYER 4: Left accent bar (firma Solo Leveling)
        # ═══════════════════════════════════════════════════════════════════
        self.elements["accent_l"] = ui.Bar()
        self.elements["accent_l"].SetParent(self)
        self.elements["accent_l"].SetPosition(0, 0)
        self.elements["accent_l"].SetSize(borderW + 2, h)
        self.elements["accent_l"].SetColor(colors["accent"])
        self.elements["accent_l"].AddFlag("not_pick")
        self.elements["accent_l"].Show()

        # Corner L-bracket ticks (4 orizzontali, puliti)
        tickLen = 18
        cTickColor = colors["primary"]
        for key, cx, cy, cw, ch in [
            ("cTLH", borderW + 2, borderW, tickLen, 1),
            ("cTRH", w - borderW - tickLen - 2, borderW, tickLen, 1),
            ("cBLH", borderW + 2, h - borderW - 1, tickLen, 1),
            ("cBRH", w - borderW - tickLen - 2, h - borderW - 1, tickLen, 1),
        ]:
            ct = ui.Bar(); ct.SetParent(self); ct.SetPosition(cx, cy); ct.SetSize(cw, ch)
            ct.SetColor(cTickColor); ct.AddFlag("not_pick"); ct.Show()
            self.elements[key] = ct
        
        # ═══════════════════════════════════════════════════════════════════
        # TITOLO FRATTURA (grande, in alto)
        # ═══════════════════════════════════════════════════════════════════
        yOffset = 15
        
        # Rank label
        self.elements["rank_label"] = ui.TextLine()
        self.elements["rank_label"].SetParent(self)
        self.elements["rank_label"].SetPosition(w // 2, yOffset)
        self.elements["rank_label"].SetHorizontalAlignCenter()
        self.elements["rank_label"].SetText("[ %s ]" % rankCfg["name"])
        self.elements["rank_label"].SetPackedFontColor(colors["primary"])
        self.elements["rank_label"].SetOutline()
        self.elements["rank_label"].Show()
        
        yOffset += 22
        
        # Nome frattura
        self.elements["fracture_name"] = ui.TextLine()
        self.elements["fracture_name"].SetParent(self)
        self.elements["fracture_name"].SetPosition(w // 2, yOffset)
        self.elements["fracture_name"].SetHorizontalAlignCenter()
        self.elements["fracture_name"].SetText(self.fractureName.upper())
        self.elements["fracture_name"].SetPackedFontColor(0xFFFFFFFF)
        self.elements["fracture_name"].SetOutline()
        self.elements["fracture_name"].Show()
        
        yOffset += 20
        
        # Sottotitolo rank
        self.elements["subtitle"] = ui.TextLine()
        self.elements["subtitle"].SetParent(self)
        self.elements["subtitle"].SetPosition(w // 2, yOffset)
        self.elements["subtitle"].SetHorizontalAlignCenter()
        self.elements["subtitle"].SetText(rankCfg["subtitle"])
        self.elements["subtitle"].SetPackedFontColor(colors["text"])
        self.elements["subtitle"].Show()
        
        yOffset += 30
        
        # ═══════════════════════════════════════════════════════════════════
        # SEPARATORE
        # ═══════════════════════════════════════════════════════════════════
        self.elements["sep1"] = ui.Bar()
        self.elements["sep1"].SetParent(self)
        self.elements["sep1"].SetPosition(20, yOffset)
        self.elements["sep1"].SetSize(w - 40, 1)
        self.elements["sep1"].SetColor(colors["secondary"])
        self.elements["sep1"].AddFlag("not_pick")
        self.elements["sep1"].Show()
        
        yOffset += 15
        
        # ═══════════════════════════════════════════════════════════════════
        # SEZIONE REQUISITI
        # ═══════════════════════════════════════════════════════════════════
        self.elements["req_title"] = ui.TextLine()
        self.elements["req_title"].SetParent(self)
        self.elements["req_title"].SetPosition(20, yOffset)
        self.elements["req_title"].SetText("REQUISITI")
        self.elements["req_title"].SetPackedFontColor(colors["accent"])
        self.elements["req_title"].Show()
        
        yOffset += 18
        
        # Requisito Gloria
        if self.reqGlory > 0:
            gloryColor = 0xFF00FF00 if self.playerGlory >= self.reqGlory else 0xFFFF4444
            self.elements["req_glory"] = ui.TextLine()
            self.elements["req_glory"].SetParent(self)
            self.elements["req_glory"].SetPosition(30, yOffset)
            self.elements["req_glory"].SetText("Gloria: %d / %d" % (self.playerGlory, self.reqGlory))
            self.elements["req_glory"].SetPackedFontColor(gloryColor)
            self.elements["req_glory"].Show()
            yOffset += 16
        
        # Requisito Power Rank
        if self.reqPowerRank > 0:
            prColor = 0xFF00FF00 if self.partyPowerRank >= self.reqPowerRank else 0xFFFF4444
            self.elements["req_power"] = ui.TextLine()
            self.elements["req_power"].SetParent(self)
            self.elements["req_power"].SetPosition(30, yOffset)
            self.elements["req_power"].SetText("Power Rank: %d / %d" % (self.partyPowerRank, self.reqPowerRank))
            self.elements["req_power"].SetPackedFontColor(prColor)
            self.elements["req_power"].Show()
            yOffset += 16
        
        # Se nessun requisito
        if self.reqGlory == 0 and self.reqPowerRank == 0:
            self.elements["req_free"] = ui.TextLine()
            self.elements["req_free"].SetParent(self)
            self.elements["req_free"].SetPosition(30, yOffset)
            self.elements["req_free"].SetText("Nessuno - Frattura Aperta")
            self.elements["req_free"].SetPackedFontColor(0xFF00FF00)
            self.elements["req_free"].Show()
            yOffset += 16
        
        yOffset += 10
        
        # ═══════════════════════════════════════════════════════════════════
        # SEZIONE INFO MISSIONE (Livello, Struttura, Strategia)
        # ═══════════════════════════════════════════════════════════════════
        self.elements["info_title"] = ui.TextLine()
        self.elements["info_title"].SetParent(self)
        self.elements["info_title"].SetPosition(20, yOffset)
        self.elements["info_title"].SetText("DETTAGLI MISSIONE")
        self.elements["info_title"].SetPackedFontColor(0xFF00FFFF) # Ciano
        self.elements["info_title"].Show()
        yOffset += 18
        
        # Livello
        self.elements["info_lvl"] = ui.TextLine()
        self.elements["info_lvl"].SetParent(self)
        self.elements["info_lvl"].SetPosition(30, yOffset)
        self.elements["info_lvl"].SetText("Livello Consigliato: %s" % self.levelInfo)
        self.elements["info_lvl"].SetPackedFontColor(0xFFDDDDDD)
        self.elements["info_lvl"].Show()
        yOffset += 14
        
        # Struttura
        self.elements["info_wave"] = ui.TextLine()
        self.elements["info_wave"].SetParent(self)
        self.elements["info_wave"].SetPosition(30, yOffset)
        self.elements["info_wave"].SetText("Struttura: %s" % self.waveInfo)
        self.elements["info_wave"].SetPackedFontColor(0xFFDDDDDD)
        self.elements["info_wave"].Show()
        yOffset += 14
        
        # Coraggio (Lo metto qui invece che alla fine)
        if self.courageInfo:
            self.elements["info_courage"] = ui.TextLine()
            self.elements["info_courage"].SetParent(self)
            self.elements["info_courage"].SetPosition(30, yOffset)
            self.elements["info_courage"].SetText(self.courageInfo)
            self.elements["info_courage"].SetPackedFontColor(0xFFFFAA00)
            self.elements["info_courage"].Show()
            yOffset += 14
            
        # Strategia (Solo se presente)
        if self.strategyHint and self.strategyHint != "Nessuna info.":
            hintColor = 0xFFFF4444 if self.fractureRank in ["S", "N", "A"] else 0xFFFFA500
            self.elements["info_hint"] = ui.TextLine()
            self.elements["info_hint"].SetParent(self)
            self.elements["info_hint"].SetPosition(30, yOffset)
            self.elements["info_hint"].SetText("Consiglio: %s" % self.strategyHint)
            self.elements["info_hint"].SetPackedFontColor(hintColor)
            self.elements["info_hint"].Show()
            yOffset += 14
            
        yOffset += 10

        # ═══════════════════════════════════════════════════════════════════
        # SEZIONE RICOMPENSE
        # ═══════════════════════════════════════════════════════════════════
        self.elements["reward_title"] = ui.TextLine()
        self.elements["reward_title"].SetParent(self)
        self.elements["reward_title"].SetPosition(20, yOffset)
        self.elements["reward_title"].SetText("RICOMPENSE POSSIBILI")
        self.elements["reward_title"].SetPackedFontColor(0xFFFFD700)
        self.elements["reward_title"].Show()
        
        yOffset += 18
        
        # Lista ricompense (max 4)
        rewardList = self.rewards[:4] if self.rewards else ["Gloria variabile", "Oggetti rari", "Esperienza"]
        for i, reward in enumerate(rewardList):
            self.elements["reward_%d" % i] = ui.TextLine()
            self.elements["reward_%d" % i].SetParent(self)
            self.elements["reward_%d" % i].SetPosition(30, yOffset)
            self.elements["reward_%d" % i].SetText("* %s" % reward)
            self.elements["reward_%d" % i].SetPackedFontColor(0xFFCCCCCC)
            self.elements["reward_%d" % i].Show()
            yOffset += 14
        
        yOffset += 10
        
        # ═══════════════════════════════════════════════════════════════════
        # SEZIONE WARNING (penalità fallimento)
        # ═══════════════════════════════════════════════════════════════════
        self.elements["warn_title"] = ui.TextLine()
        self.elements["warn_title"].SetParent(self)
        self.elements["warn_title"].SetPosition(20, yOffset)
        self.elements["warn_title"].SetText("IN CASO DI FALLIMENTO")
        self.elements["warn_title"].SetPackedFontColor(0xFFFF4444)
        self.elements["warn_title"].Show()
        
        yOffset += 18
        
        self.elements["warn_text"] = ui.TextLine()
        self.elements["warn_text"].SetParent(self)
        self.elements["warn_text"].SetPosition(30, yOffset)
        self.elements["warn_text"].SetText("Perderai parte della Gloria guadagnata")
        self.elements["warn_text"].SetPackedFontColor(0xFFAA6666)
        self.elements["warn_text"].Show()
        
        yOffset += 20
        
        # ═══════════════════════════════════════════════════════════════════
        # SEPARATORE 2
        # ═══════════════════════════════════════════════════════════════════
        self.elements["sep2"] = ui.Bar()
        self.elements["sep2"].SetParent(self)
        self.elements["sep2"].SetPosition(20, yOffset)
        self.elements["sep2"].SetSize(w - 40, 1)
        self.elements["sep2"].SetColor(colors["secondary"])
        self.elements["sep2"].AddFlag("not_pick")
        self.elements["sep2"].Show()
        
        yOffset += 15
        
        # ═══════════════════════════════════════════════════════════════════
        # INFO SIGILLO
        # ═══════════════════════════════════════════════════════════════════
        self.elements["seal_info"] = ui.TextLine()
        self.elements["seal_info"].SetParent(self)
        self.elements["seal_info"].SetPosition(w // 2, yOffset)
        self.elements["seal_info"].SetHorizontalAlignCenter()
        self.elements["seal_info"].SetText("Sigilla: +%d Gloria (senza rischi)" % self.sealBonus)
        self.elements["seal_info"].SetPackedFontColor(0xFF88FFFF)
        self.elements["seal_info"].Show()
        
        # ═══════════════════════════════════════════════════════════════════
        # PULSANTI (in basso) — stile Solo Leveling con decorazioni
        # ═══════════════════════════════════════════════════════════════════
        btnW = 115
        btnH = 40
        btnSpacing = 14
        totalBtnWidth = btnW * 3 + btnSpacing * 2
        btnStartX = (w - totalBtnWidth) // 2
        btnY = h - 62

        # Colori per i 3 pulsanti
        enterBgCol  = 0xFF003800 if (self.canEnter or self.canForce) else 0xFF3A2200
        enterTpCol  = 0xFF00FF55 if (self.canEnter or self.canForce) else 0xFFFF8800
        enterAcCol  = 0xFF00CC44 if (self.canEnter or self.canForce) else 0xFFCC6600
        enterGlCol  = 0x1800FF55 if (self.canEnter or self.canForce) else 0x18FF8800

        sealBgCol   = 0xFF001C2A
        sealTpCol   = 0xFF00CCFF
        sealAcCol   = 0xFF0099CC
        sealGlCol   = 0x1800CCFF

        backBgCol   = 0xFF280000
        backTpCol   = 0xFFFF3333
        backAcCol   = 0xFFCC2222
        backGlCol   = 0x18FF3333

        btnDefs = [
            ("enter", btnStartX,                         enterBgCol, enterTpCol, enterAcCol, enterGlCol, "APRI",     self.OnClickEnter),
            ("seal",  btnStartX + btnW + btnSpacing,     sealBgCol,  sealTpCol,  sealAcCol,  sealGlCol,  "SIGILLA",  self.OnClickSeal),
            ("back",  btnStartX + (btnW + btnSpacing)*2, backBgCol,  backTpCol,  backAcCol,  backGlCol,  "INDIETRO", self.OnClickBack),
        ]

        for name, bx, bgCol, topCol, acCol, glCol, label, event in btnDefs:
            # Background scuro
            bg = ui.Bar(); bg.SetParent(self)
            bg.SetPosition(bx, btnY)
            bg.SetSize(btnW, btnH)
            bg.SetColor(bgCol); bg.AddFlag("not_pick"); bg.Show()
            self.elements["btn_%s_bg" % name] = bg

            # Bordo top 3px colorato (firma visiva)
            tb = ui.Bar(); tb.SetParent(self)
            tb.SetPosition(bx, btnY)
            tb.SetSize(btnW, 3)
            tb.SetColor(topCol); tb.AddFlag("not_pick"); tb.Show()
            self.elements["btn_%s_top" % name] = tb

            # Accent bar left 3px
            al = ui.Bar(); al.SetParent(self)
            al.SetPosition(bx, btnY)
            al.SetSize(3, btnH)
            al.SetColor(acCol); al.AddFlag("not_pick"); al.Show()
            self.elements["btn_%s_acc" % name] = al

            # Pulsante interattivo sopra tutto
            btn = ui.Button(); btn.SetParent(self)
            btn.SetPosition(bx, btnY)
            btn.SetSize(btnW, btnH)
            btn.SetText(label)
            btn.SetEvent(event)
            btn.Show()
            self.elements["btn_%s" % name] = btn
        
        # ═══════════════════════════════════════════════════════════════════
        # PARTICELLE DECORATIVE (effetto vortice)
        # ═══════════════════════════════════════════════════════════════════
        particleCount = rankCfg["particle_count"]
        for i in range(particleCount):
            particle = ui.Bar()
            particle.SetParent(self)
            particle.SetSize(3, 3)
            particle.SetColor(colors["accent"])
            particle.AddFlag("not_pick")
            particle.Show()
            self.particles.append({
                "bar": particle,
                "angle": (360.0 / particleCount) * i,
                "radius": min(w, h) // 3,
                "speed": 0.5 + (i * 0.1),
            })
    
    def ShowPortal(self, data):
        """
        Mostra la finestra con i dati della frattura
        data = {
            name, rank, color, vnum, req_glory, req_power_rank,
            can_enter, can_force, player_glory, party_power_rank,
            rewards, seal_bonus
        }
        """
        self.fractureName = data.get("name", "Frattura Sconosciuta")
        self.fractureRank = data.get("rank", "E")
        self.fractureColor = data.get("color", "PURPLE")
        self.fractureVnum = data.get("vnum", 0)
        self.reqGlory = data.get("req_glory", 0)
        self.reqPowerRank = data.get("req_power_rank", 0)
        self.canEnter = data.get("can_enter", False)
        self.canForce = data.get("can_force", False)
        self.playerGlory = data.get("player_glory", 0)
        self.partyPowerRank = data.get("party_power_rank", 0)
        self.rewards = data.get("rewards", [])
        self.sealBonus = data.get("seal_bonus", 200)
        self.courageInfo = data.get("courage_info", "")
        self.levelInfo = data.get("level_info", "??")
        self.waveInfo = data.get("wave_info", "??")
        self.strategyHint = data.get("strategy_hint", "")
        
        self.startTime = app.GetTime()
        self.pulsePhase = 0.0
        self.vortexAngle = 0.0
        self.isClosing = False
        
        self.BuildUI()
        self.SetTop()
        self.Show()

        # NOTA: Non toccare il QuestCurtain qui - viene gestito correttamente
        # da RestoreGameInterface() quando la finestra si chiude
    
    def OnClickEnter(self):
        """Player clicca ENTRA"""
        if self.isClosing: return
        
        import dbg
        dbg.TraceError("HunterPortal: Click ENTRA vnum=%d" % self.fractureVnum)
        
        # TRICK: Usa input quest string invece di chat command
        net.SendQuestInputStringPacket("1")
        
        # Flag per dire che abbiamo sceto (evita CANCEL al close)
        self.isClosing = True 
        self.closeStartTime = app.GetTime()
        # Disabilita bottoni per feedback visivo
        if "btn_enter" in self.elements: self.elements["btn_enter"].Disable()
        if "btn_seal" in self.elements: self.elements["btn_seal"].Disable()
    
    def OnClickSeal(self):
        """Player clicca SIGILLA"""
        if self.isClosing: return
        
        import dbg
        dbg.TraceError("HunterPortal: Click SIGILLA vnum=%d" % self.fractureVnum)
        
        # TRICK: Usa input quest string
        net.SendQuestInputStringPacket("2")
        
        self.isClosing = True
        self.closeStartTime = app.GetTime()
        # Disabilita bottoni
        if "btn_enter" in self.elements: self.elements["btn_enter"].Disable()
        if "btn_seal" in self.elements: self.elements["btn_seal"].Disable()
    
    def OnClickBack(self):
        """Player clicca INDIETRO"""
        self.StartClose() # Invia CANCEL grazie alla modifica sopra
    
    def StartClose(self):
        """Inizia animazione di chiusura"""
        # Se chiudiamo senza aver scelto, sblocchiamo la quest
        if not self.isClosing:
            net.SendQuestInputStringPacket("CANCEL")
            
        self.isClosing = True
        self.closeStartTime = app.GetTime()
    
    def OnPressEscapeKey(self):
        self.StartClose()
        return True
    
    def OnUpdate(self):
        if not self.IsShow():
            return
        
        currentTime = app.GetTime()
        elapsed = currentTime - self.startTime
        
        # Animazione chiusura
        if self.isClosing:
            closeElapsed = currentTime - self.closeStartTime
            if closeElapsed > 0.3:
                # MEMORY LEAK FIX: Non chiamare Destroy qui, solo Hide
                # Destroy viene chiamato quando si ricostruisce la UI o nel distruttore
                self.Hide()
                self.isClosing = False
                
                # FIX UI BUG: Ripristina la UI del gioco dopo la chiusura
                self.RestoreGameUI()
                return
            # Fade out
            alpha = int(255 * (1.0 - closeElapsed / 0.3))
            # Potremmo applicare alpha se supportato
        
        # Ottieni configurazione
        rankCfg = RANK_CONFIG.get(self.fractureRank, RANK_CONFIG["E"])
        colors = FRACTURE_COLORS.get(self.fractureColor, FRACTURE_COLORS["PURPLE"])
        
        # Pulsazione bordi
        pulseSpeed = rankCfg["pulse_speed"]
        self.pulsePhase = (elapsed * pulseSpeed) % (2 * 3.14159)
        pulseValue = 0.5 + 0.5 * math.sin(self.pulsePhase)
        
        # Modifica colore bordi con pulsazione
        baseColor = colors["primary"]
        r = (baseColor >> 16) & 0xFF
        g = (baseColor >> 8) & 0xFF
        b = baseColor & 0xFF
        
        # Intensifica con pulsazione
        intensity = 0.7 + 0.3 * pulseValue
        r = min(255, int(r * intensity))
        g = min(255, int(g * intensity))
        b = min(255, int(b * intensity))
        pulseColor = 0xFF000000 | (r << 16) | (g << 8) | b
        
        # Applica ai bordi
        if "border_top" in self.elements:
            self.elements["border_top"].SetColor(pulseColor)
            self.elements["border_bottom"].SetColor(pulseColor)
            self.elements["border_left"].SetColor(pulseColor)
            self.elements["border_right"].SetColor(pulseColor)
        
        # Glow esterno pulsante
        glowIntensity = rankCfg["glow_intensity"]
        glowAlpha = int(60 + 40 * pulseValue * glowIntensity)
        glowR = (colors["glow"] >> 16) & 0xFF
        glowG = (colors["glow"] >> 8) & 0xFF
        glowB = colors["glow"] & 0xFF
        newGlow = (glowAlpha << 24) | (glowR << 16) | (glowG << 8) | glowB
        if "glow_outer" in self.elements:
            self.elements["glow_outer"].SetColor(newGlow)
        
        # Animazione particelle (vortice)
        self.vortexAngle += 2.0  # Gradi per frame
        w, hh = self.GetWidth(), self.GetHeight()
        centerX = w // 2
        centerY = hh // 2
        
        for p in self.particles:
            p["angle"] += p["speed"]
            if p["angle"] >= 360:
                p["angle"] -= 360
            
            rad = (p["angle"] + self.vortexAngle) * 3.14159 / 180.0
            px = centerX + int(p["radius"] * math.cos(rad)) - 1
            py = centerY + int(p["radius"] * math.sin(rad)) - 1
            p["bar"].SetPosition(px, py)


# ═══════════════════════════════════════════════════════════════════════════════
#  FUNZIONE HELPER per parsing dati dal server
# ═══════════════════════════════════════════════════════════════════════════════
def ParseFracturePreviewData(cmdData):
    """
    Parsa stringa dal server nel formato:
    name|rank|color|vnum|req_glory|req_power_rank|can_enter|can_force|player_glory|party_power_rank|seal_bonus|rewards|courage_info|level_info|wave_info|strategy_hint
    """
    try:
        parts = cmdData.split("|")
        if len(parts) < 12:
            return None
        
        rewards = []
        if len(parts) > 11 and parts[11]:
            rewards = parts[11].split(";")
        
        return {
            "name": parts[0].replace("+", " "),
            "rank": parts[1],
            "color": parts[2],
            "vnum": int(parts[3]),
            "req_glory": int(parts[4]),
            "req_power_rank": int(parts[5]),
            "can_enter": parts[6] == "1",
            "can_force": parts[7] == "1",
            "player_glory": int(parts[8]),
            "party_power_rank": int(parts[9]),
            "seal_bonus": int(parts[10]),
            "rewards": rewards,
            "courage_info": parts[12].replace("+", " ") if len(parts) > 12 else "",
            "level_info": parts[13].replace("+", " ") if len(parts) > 13 else "??",
            "wave_info": parts[14].replace("+", " ") if len(parts) > 14 else "??",
            "strategy_hint": parts[15].replace("+", " ") if len(parts) > 15 else ""
        }
    except Exception as e:
        import dbg
        dbg.TraceError("ParseFracturePreviewData error: " + str(e) + " data=" + str(cmdData))
        return None