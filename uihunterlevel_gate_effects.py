# -*- coding: utf-8 -*-
import ui
import wndMgr
import app
import math

# ==============================================================================
# CONFIGURAZIONE E COLORI
# ==============================================================================
COLOR_CODES = {
    "RED": 0xFFE74C3C,
    "BLUE": 0xFF3498DB,
    "PURPLE": 0xFF9B59B6,
    "GOLD": 0xFFF1C40F,
    "GREEN": 0xFF2ECC71,
    "ORANGE": 0xFFE67E22,
    "BLACKWHITE": 0xFFCCCCCC,
    "SYSTEM": 0xFF00A8FF # Azzurro tipico del "Sistema"
}

def GetColor(code):
    return COLOR_CODES.get(code, 0xFFFFFFFF)

# ==============================================================================
# 1. GATE ENTRY: "SYSTEM LOCKDOWN" (Versione FIXATA)
# ==============================================================================
class GateEntryEffect(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        # Rimuovi il flag 'top' se da problemi su alcuni client, 
        # useremo SetTop() manuale
        
        self.startTime = 0
        self.gateName = "Gate"
        self.baseColor = 0xFFFFFFFF
        
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        # 1. Sfondo Totale (Abisso digitale)
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0xFF000000)
        self.bg.Show()

        # 2. Linea di Scansione (Scanline verticale)
        self.scanLine = ui.Bar()
        self.scanLine.SetParent(self)
        self.scanLine.SetPosition(0, 0)
        self.scanLine.SetSize(self.screenWidth, 2)
        self.scanLine.SetColor(0xFF00A8FF) # Azzurro sistema
        self.scanLine.Hide()

        # 3. Box Centrale "ALERT"
        self.alertBox = ui.Bar()
        self.alertBox.SetParent(self)
        self.alertBox.SetSize(600, 150)
        self.alertBox.SetPosition(self.screenWidth/2 - 300, self.screenHeight/2 - 75)
        self.alertBox.SetColor(0xDD000000) # Semi-trasparente
        self.alertBox.Hide()

        # Bordi del box (Sinistra e Destra spessi)
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self.alertBox)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(5, 150)
        self.borderLeft.SetColor(0xFF00A8FF)
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self.alertBox)
        self.borderRight.SetPosition(595, 0)
        self.borderRight.SetSize(5, 150)
        self.borderRight.SetColor(0xFF00A8FF)
        self.borderRight.Show()

        # Testo Principale
        self.mainText = ui.TextLine()
        self.mainText.SetParent(self.alertBox)
        self.mainText.SetPosition(300, 30)
        self.mainText.SetHorizontalAlignCenter()
        self.mainText.SetText("! SYSTEM ALERT !")
        self.mainText.SetOutline()
        # RIMOSSO: self.mainText.SetFontName(ui.def_font_large) -> Causava crash
        self.mainText.Show()

        # Testo Secondario (Nome Gate)
        self.subText = ui.TextLine()
        self.subText.SetParent(self.alertBox)
        self.subText.SetPosition(300, 80)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText("")
        self.subText.SetOutline()
        self.subText.Show()

        # Glitch Bars (Barre casuali che appaiono)
        self.glitchBars = []
        for i in xrange(15): # Aumentate barre glitch
            b = ui.Bar()
            b.SetParent(self)
            b.SetColor(0xFFFFFFFF)
            b.AddFlag("not_pick")
            b.Hide()
            self.glitchBars.append(b)

    def Start(self, gateName, colorCode):
        self.gateName = gateName.replace("+", " ").upper()
        self.baseColor = GetColor(colorCode)
        self.startTime = app.GetTime()
        
        # ==========================================
        # HARD RESET DEGLI STATI VISIVI (FIX)
        # ==========================================
        self.bg.SetColor(0xFF000000)
        
        # 1. Ripristina dimensioni originali del box (che si era rimpicciolito alla fine)
        self.alertBox.SetSize(600, 150)
        self.alertBox.SetPosition(int(self.screenWidth/2 - 300), int(self.screenHeight/2 - 75))
        
        # 2. Mostra di nuovo i componenti interni (che erano stati nascosti)
        self.mainText.Show()
        self.mainText.SetText("! DANGER !")
        self.mainText.SetPackedFontColor(0xFFFF0000)
        
        self.subText.Show()
        self.subText.SetText("")
        
        self.borderLeft.Show()
        self.borderRight.Show()
        
        # 3. Nascondi container principali per l'inizio animazione
        self.alertBox.Hide()
        self.scanLine.Hide()
        for b in self.glitchBars:
            b.Hide()
        
        # Avvia finestra principale
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.IsShow(): return
        t = app.GetTime() - self.startTime

        # FASE 1: BLACKOUT + SCANLINE (0.0s - 1.0s)
        if t < 1.0:
            self.scanLine.Show()
            # La linea scende velocemente
            yPos = int((t / 1.0) * self.screenHeight)
            self.scanLine.SetPosition(0, yPos)
            
            # Glitch casuali
            for b in self.glitchBars:
                if app.GetRandom(0, 100) > 75:
                    w = app.GetRandom(50, 400)
                    x = app.GetRandom(0, self.screenWidth - w)
                    y = app.GetRandom(0, self.screenHeight)
                    b.SetPosition(x, y)
                    b.SetSize(w, app.GetRandom(2, 5))
                    b.SetColor(self.baseColor)
                    b.Show()
                else:
                    b.Hide()

        # FASE 2: ALERT BOX IMPACT (1.0s - 1.2s)
        elif t < 1.2:
            self.scanLine.Hide()
            for b in self.glitchBars: b.Hide()
            
            # Flash del box
            self.alertBox.Show()
            self.borderLeft.SetColor(self.baseColor)
            self.borderRight.SetColor(self.baseColor)
            self.mainText.SetPackedFontColor(self.baseColor)
            self.mainText.SetText("! DUNGEON DETECTED !")

        # FASE 3: TYPEWRITER EFFECT & PULSE (1.2s - 4.0s)
        elif t < 4.0:
            self.alertBox.Show()
            
            # Scrittura tipo terminale
            fullStr = "ENTERING: " + self.gateName
            dt = t - 1.2
            charCount = int(dt * 25) # Velocità scrittura aumentata
            if charCount > len(fullStr): charCount = len(fullStr)
            self.subText.SetText(fullStr[:charCount])
            
            # Pulsazione Colore
            import math
            pulse = abs(math.sin(t * 6.0)) # Più veloce
            
            # Estrazione RGB per interpolazione
            r = (self.baseColor >> 16) & 0xFF
            g = (self.baseColor >> 8) & 0xFF
            b = self.baseColor & 0xFF
            
            # Colore bordi che pulsa
            mr = int(r * pulse)
            mg = int(g * pulse)
            mb = int(b * pulse)
            col = (0xFF << 24) | (mr << 16) | (mg << 8) | mb
            
            self.borderLeft.SetColor(col)
            self.borderRight.SetColor(col)
            self.subText.SetPackedFontColor(0xFFFFFFFF)

            # Sfondo: Aura tech che pulsa leggermente
            # Usiamo solo i canali colore con un alpha basso
            bgPulse = int(pulse * 80)
            br = int(r * 0.2)
            bgcol = (bgPulse << 24) | (br << 16) | (0 << 8) | 0
            self.bg.SetColor(bgcol) 

        # FASE 4: SYSTEM SHUTDOWN (Fade Out) (4.0s - 5.0s)
        elif t < 5.0:
            normT = (t - 4.0)
            # Box collassa orizzontalmente
            currentWidth = int(600 * (1.0 - normT))
            if currentWidth < 0: currentWidth = 0
            
            self.alertBox.SetSize(currentWidth, 150 if normT < 0.3 else 2) 
            self.alertBox.SetPosition(int(self.screenWidth/2 - currentWidth/2), int(self.screenHeight/2 - 75))
            
            self.mainText.Hide()
            self.subText.Hide()
            self.borderLeft.Hide()
            self.borderRight.Hide()
            
            # Sfondo Fade to black e poi invisibile
            alpha = int((1.0 - normT) * 255)
            self.bg.SetColor((alpha << 24) | 0x000000)

        else:
            self.Hide()

# ==============================================================================
# 2. VITTORIA: "LEVEL UP / GOLDEN AGE" (Funziona bene, lascio invariato)
# ==============================================================================
class GateVictoryEffect(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.startTime = 0
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0xAA000000) 
        self.bg.Show()

        self.banner = ui.Bar()
        self.banner.SetParent(self)
        self.banner.SetSize(0, 100)
        self.banner.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 50))
        self.banner.SetColor(0xCCFFD700)
        self.banner.Show()

        self.title = ui.TextLine()
        self.title.SetParent(self)
        self.title.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 20))
        self.title.SetHorizontalAlignCenter()
        self.title.SetText("DUNGEON COMPLETATO")
        self.title.SetPackedFontColor(0xFFFFFFFF)
        self.title.SetOutline()
        self.title.Show()

        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 + 10))
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFFF00)
        self.rewardText.SetOutline()
        self.rewardText.Show()

        self.particles = []
        for i in xrange(20):
            p = ui.Bar()
            p.SetParent(self)
            p.SetSize(4, 4)
            p.SetColor(0xFFFFD700)
            p.Hide()
            self.particles.append([p, 0, 0])

    def Start(self, gateName, gloria):
        self.startTime = app.GetTime()
        self.rewardText.SetText("Ricompensa: +%d Gloria" % gloria)
        self.banner.SetSize(0, 100)
        self.Show()
        self.SetTop()
        
        for p in self.particles:
            p[0].SetPosition(int(self.screenWidth/2), int(self.screenHeight/2))
            p[0].Show()
            p[1] = app.GetRandom(-10, 10)
            p[2] = app.GetRandom(-10, 10)

    def OnUpdate(self):
        if not self.IsShow(): return
        t = app.GetTime() - self.startTime

        if t < 0.5:
            width = int((t / 0.5) * self.screenWidth)
            self.banner.SetSize(width, 100)
            self.banner.SetPosition(int(self.screenWidth/2 - width/2), int(self.screenHeight/2 - 50))
        else:
            self.banner.SetSize(self.screenWidth, 100)
            self.banner.SetPosition(0, int(self.screenHeight/2 - 50))

        if t < 3.0:
            for p in self.particles:
                x, y = p[0].GetLocalPosition()
                x += p[1]
                y += p[2]
                p[2] += 0.5 # Gravità
                p[0].SetPosition(int(x), int(y))
                
        if t > 4.0:
            self.Hide()

# ==============================================================================
# 3. SCONFITTA (ROTTURA E SANGUE) (Funziona bene, lascio invariato)
# ==============================================================================
class GateDefeatEffect(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.startTime = 0
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.Show()

        self.cracks = []
        for i in xrange(5):
            c = ui.Bar()
            c.SetParent(self)
            c.SetColor(0xFF000000)
            c.Hide()
            self.cracks.append(c)

        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2))
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("CRITICAL FAILURE")
        self.text.SetPackedFontColor(0xFF000000)
        self.text.SetOutline()
        self.text.Show()

    def Start(self, penalty):
        self.startTime = app.GetTime()
        self.text.SetText("SEI MORTO (-%d GLORIA)" % penalty)
        
        for c in self.cracks:
            w = app.GetRandom(50, 400)
            h = app.GetRandom(2, 5)
            x = app.GetRandom(0, self.screenWidth - w)
            y = app.GetRandom(0, self.screenHeight)
            c.SetPosition(x, y)
            c.SetSize(w, h)
            c.Show()
            
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.IsShow(): return
        t = app.GetTime() - self.startTime

        if t < 0.2:
            self.bg.SetColor(0xCCFFFFFF)
        elif t < 3.0:
            self.bg.SetColor(0x88990000)
            self.text.SetPackedFontColor(0xFFFFFFFF)
        else:
            self.Hide()

# ==============================================================================
# 4. POPUP PROGRESSO: "TOAST NOTIFICATION" (Bug Fix)
# ==============================================================================
class TrialProgressPopup(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        
        self.w = 260
        self.h = 50
        
        # Coordinate base per evitare bug di calcolo
        self.screenWidth = wndMgr.GetScreenWidth()
        self.baseX = self.screenWidth
        self.visibleX = self.screenWidth - self.w - 20
        self.y = 200 # Spostato leggermente più in basso
        
        self.SetSize(self.w, self.h)
        self.SetPosition(self.baseX, self.y)
        self.AddFlag("not_pick")
        # Top flag removed to avoid issues on some clients
        
        self.targetX = self.baseX 
        self.startTime = 0
        
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.w, self.h)
        self.bg.SetPosition(0, 0)
        self.bg.SetColor(0xEE111111) 
        self.bg.Show()

        self.sideBar = ui.Bar()
        self.sideBar.SetParent(self.bg)
        self.sideBar.SetSize(5, self.h)
        self.sideBar.SetPosition(0, 0)
        self.sideBar.SetColor(0xFFFFFFFF)
        self.sideBar.Show()

        self.titleText = ui.TextLine()
        self.titleText.SetParent(self.bg)
        self.titleText.SetPosition(15, 8)
        self.titleText.SetText("UPDATE")
        self.titleText.SetPackedFontColor(0xFFAAAAAA)
        self.titleText.Show()

        self.progText = ui.TextLine()
        self.progText.SetParent(self.bg)
        self.progText.SetPosition(15, 25)
        self.progText.SetText("")
        self.progText.SetPackedFontColor(0xFFFFFFFF)
        self.progText.Show()

    def AddPopup(self, pType, current, required):
        pType = pType.upper()
        colMap = {
            "BOSS": 0xFFFF0000,
            "METIN": 0xFFFFD700,
            "FRACTURE": 0xFF9900FF,
            "MISSION": 0xFF00FF00,
            "CHEST": 0xFF3498DB
        }
        barColor = colMap.get(pType, 0xFFFFFFFF)
        self.sideBar.SetColor(barColor)
        
        self.titleText.SetText(pType)
        self.progText.SetText("Completato: %d / %d" % (current, required))
        
        # Reset stato
        self.SetPosition(self.baseX, self.y)
        self.targetX = self.visibleX
        self.startTime = app.GetTime()
        
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.IsShow(): return
        
        elapsed = app.GetTime() - self.startTime
        cx, cy = self.GetLocalPosition() # returns int, int usually
        
        # ANIMAZIONE ENTRATA (0-0.5)
        if elapsed < 0.5:
            # Interpolazione lineare sicura con int
            dist = self.targetX - cx
            step = int(dist * 0.2)
            # Se siamo molto vicini, snap alla fine
            if abs(dist) < 2: 
                self.SetPosition(int(self.targetX), int(self.y))
            else:
                self.SetPosition(int(cx + step), int(self.y))
                
        # PAUSA (0.5 - 3.5)
        elif elapsed < 3.5:
            self.SetPosition(int(self.visibleX), int(self.y))
            
        # ANIMAZIONE USCITA (3.5 - 4.5)
        elif elapsed < 4.5:
            targetOut = self.baseX + 10
            dist = targetOut - cx
            step = int(dist * 0.2)
            # Forza minima movimento per evitare che sembri bloccato
            if step < 2: step = 2
            
            self.SetPosition(int(cx + step), int(self.y))
            
        else:
            self.Hide()

# ==============================================================================
# 5. CHEST OPEN: "SISTEMA - OGGETTO OTTENUTO" - Stile SOLO LEVELING
# ==============================================================================
class ChestOpenEffect(ui.Window):
    """
    Effetto apertura baule in stile Solo Leveling:
    - Sfondo nero con glitch
    - Box stile "Sistema" con bordi azzurri
    - Testo typewriter
    - Jackpot con effetto speciale
    """
    
    # Colori tema Solo Leveling
    SYSTEM_BLUE = 0xFF00A8FF
    SYSTEM_CYAN = 0xFF00FFFF
    JACKPOT_GOLD = 0xFFFFD700
    JACKPOT_PURPLE = 0xFFAA00FF
    
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        
        self.startTime = 0
        self.chestName = "Baule"
        self.glory = 0
        self.baseColor = 0xFF00A8FF
        self.hasItem = False
        self.hasJackpot = False
        self.jackpotGlory = 0
        self.itemName = ""
        self.rewardLines = []
        
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        # === SFONDO NERO ===
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.Show()

        # === GLITCH BARS (effetto interferenza) ===
        self.glitchBars = []
        for i in xrange(12):
            b = ui.Bar()
            b.SetParent(self)
            b.SetColor(0xFF00A8FF)
            b.AddFlag("not_pick")
            b.Hide()
            self.glitchBars.append(b)

        # === SCANLINE ===
        self.scanLine = ui.Bar()
        self.scanLine.SetParent(self)
        self.scanLine.SetPosition(0, 0)
        self.scanLine.SetSize(self.screenWidth, 2)
        self.scanLine.SetColor(0xFF00A8FF)
        self.scanLine.Hide()

        # === BOX PRINCIPALE (stile Sistema) ===
        self.mainBox = ui.Bar()
        self.mainBox.SetParent(self)
        self.mainBox.SetSize(550, 280)
        self.mainBox.SetPosition(self.screenWidth/2 - 275, self.screenHeight/2 - 140)
        self.mainBox.SetColor(0x00000000)
        self.mainBox.Hide()

        # Bordo sinistro luminoso
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self.mainBox)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(4, 280)
        self.borderLeft.SetColor(0xFF00A8FF)
        self.borderLeft.Show()

        # Bordo destro luminoso
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self.mainBox)
        self.borderRight.SetPosition(546, 0)
        self.borderRight.SetSize(4, 280)
        self.borderRight.SetColor(0xFF00A8FF)
        self.borderRight.Show()

        # Bordo top
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self.mainBox)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(550, 2)
        self.borderTop.SetColor(0xFF00A8FF)
        self.borderTop.Show()

        # Bordo bottom
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self.mainBox)
        self.borderBottom.SetPosition(0, 278)
        self.borderBottom.SetSize(550, 2)
        self.borderBottom.SetColor(0xFF00A8FF)
        self.borderBottom.Show()

        # Sfondo interno semi-trasparente
        self.boxInner = ui.Bar()
        self.boxInner.SetParent(self.mainBox)
        self.boxInner.SetPosition(4, 2)
        self.boxInner.SetSize(542, 276)
        self.boxInner.SetColor(0xDD0A0A12)
        self.boxInner.Show()

        # === HEADER "SISTEMA" ===
        self.headerText = ui.TextLine()
        self.headerText.SetParent(self.mainBox)
        self.headerText.SetPosition(275, 15)
        self.headerText.SetHorizontalAlignCenter()
        self.headerText.SetText("")
        self.headerText.SetPackedFontColor(0xFF00A8FF)
        self.headerText.SetOutline()
        self.headerText.Show()

        # Linea separatore header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self.mainBox)
        self.headerLine.SetPosition(20, 45)
        self.headerLine.SetSize(510, 1)
        self.headerLine.SetColor(0xFF00A8FF)
        self.headerLine.Show()

        # === TITOLO BAULE ===
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self.mainBox)
        self.titleText.SetPosition(275, 60)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetOutline()
        self.titleText.Show()

        # === ICONA BAULE (ASCII art style) ===
        self.iconLine1 = ui.TextLine()
        self.iconLine1.SetParent(self.mainBox)
        self.iconLine1.SetPosition(275, 90)
        self.iconLine1.SetHorizontalAlignCenter()
        self.iconLine1.SetText("")
        self.iconLine1.SetPackedFontColor(0xFFFFD700)
        self.iconLine1.Show()

        # === CONTENUTO RICOMPENSE ===
        self.rewardTexts = []
        for i in xrange(5):
            t = ui.TextLine()
            t.SetParent(self.mainBox)
            t.SetPosition(275, 115 + i * 25)
            t.SetHorizontalAlignCenter()
            t.SetText("")
            t.SetOutline()
            t.Show()
            self.rewardTexts.append(t)

        # === JACKPOT BANNER (nascosto di default) ===
        self.jackpotBanner = ui.Bar()
        self.jackpotBanner.SetParent(self.mainBox)
        self.jackpotBanner.SetPosition(50, 200)
        self.jackpotBanner.SetSize(450, 35)
        self.jackpotBanner.SetColor(0x00000000)
        self.jackpotBanner.Hide()

        self.jackpotText = ui.TextLine()
        self.jackpotText.SetParent(self.jackpotBanner)
        self.jackpotText.SetPosition(225, 8)
        self.jackpotText.SetHorizontalAlignCenter()
        self.jackpotText.SetText("")
        self.jackpotText.SetPackedFontColor(0xFFFFD700)
        self.jackpotText.SetOutline()
        self.jackpotText.Show()

        # === FOOTER ===
        self.footerText = ui.TextLine()
        self.footerText.SetParent(self.mainBox)
        self.footerText.SetPosition(275, 250)
        self.footerText.SetHorizontalAlignCenter()
        self.footerText.SetText("")
        self.footerText.SetPackedFontColor(0x88FFFFFF)
        self.footerText.Show()

    def Start(self, chestName, glory, colorCode, itemName="", jackpotGlory=0, jackpotItems=""):
        """
        Avvia l'effetto
        jackpotGlory: Gloria bonus da jackpot (0 = nessun jackpot)
        jackpotItems: Nome item jackpot separati da virgola
        """
        self.chestName = chestName.replace("+", " ")
        self.glory = glory
        self.baseColor = GetColor(colorCode)
        self.hasItem = len(itemName) > 0
        self.itemName = itemName.replace("+", " ") if self.hasItem else ""
        self.hasJackpot = jackpotGlory > 0 or len(jackpotItems) > 0
        self.jackpotGlory = jackpotGlory
        self.jackpotItems = jackpotItems.replace("+", " ") if len(jackpotItems) > 0 else ""
        self.startTime = app.GetTime()
        
        # Reset stati visivi
        self.bg.SetColor(0x00000000)
        self.mainBox.Hide()
        self.scanLine.Hide()
        self.jackpotBanner.Hide()
        
        for b in self.glitchBars:
            b.Hide()
        
        # Reset testi
        self.headerText.SetText("")
        self.titleText.SetText("")
        self.iconLine1.SetText("")
        for t in self.rewardTexts:
            t.SetText("")
        self.jackpotText.SetText("")
        self.footerText.SetText("")
        
        # Prepara linee ricompensa
        self.rewardLines = []
        self.rewardLines.append(("+ " + str(self.glory) + " GLORIA", 0xFF00FF00))
        
        if self.hasItem:
            self.rewardLines.append(("ITEM: " + self.itemName, 0xFFFFD700))
        
        if self.hasJackpot:
            if self.jackpotGlory > 0:
                self.rewardLines.append((">>> JACKPOT: +" + str(self.jackpotGlory) + " GLORIA <<<", 0xFFFF00FF))
            if len(self.jackpotItems) > 0:
                self.rewardLines.append((">>> JACKPOT ITEM: " + self.jackpotItems + " <<<", 0xFFFFD700))
        
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if self.startTime == 0:
            return
        
        t = app.GetTime() - self.startTime
        duration = 5.0 if self.hasJackpot else 4.0
        
        if t > duration:
            self.startTime = 0
            self.Hide()
            return
        
        # === FASE 1: BLACKOUT + GLITCH (0 - 0.8s) ===
        if t < 0.8:
            progress = t / 0.8
            bgAlpha = int(220 * progress)
            self.bg.SetColor((bgAlpha << 24) | 0x000508)
            
            # Scanline veloce
            self.scanLine.Show()
            scanY = int((t * 3 % 1.0) * self.screenHeight)
            self.scanLine.SetPosition(0, scanY)
            self.scanLine.SetColor(0x6600A8FF)
            
            # Glitch casuali
            for b in self.glitchBars:
                if app.GetRandom(0, 100) > 70:
                    w = app.GetRandom(100, 500)
                    x = app.GetRandom(0, self.screenWidth - w)
                    y = app.GetRandom(0, self.screenHeight)
                    b.SetPosition(x, y)
                    b.SetSize(w, app.GetRandom(1, 4))
                    glitchAlpha = app.GetRandom(30, 100)
                    b.SetColor((glitchAlpha << 24) | 0x00A8FF)
                    b.Show()
                else:
                    b.Hide()
        
        # === FASE 2: BOX APPARE CON IMPATTO (0.8 - 1.2s) ===
        elif t < 1.2:
            self.scanLine.Hide()
            for b in self.glitchBars:
                b.Hide()
            
            self.bg.SetColor(0xDC000508)
            self.mainBox.Show()
            
            # Flash sui bordi
            progress = (t - 0.8) / 0.4
            flashIntensity = int(255 * (1.0 - progress))
            
            if self.hasJackpot:
                borderColor = (0xFF << 24) | 0xFFD700  # Oro per jackpot
            else:
                borderColor = (0xFF << 24) | (self.baseColor & 0x00FFFFFF)
            
            self.borderLeft.SetColor(borderColor)
            self.borderRight.SetColor(borderColor)
            self.borderTop.SetColor(borderColor)
            self.borderBottom.SetColor(borderColor)
            
            # Header appare
            self.headerText.SetText("[ SISTEMA ]")
            self.headerText.SetPackedFontColor(0xFF00A8FF)
        
        # === FASE 3: TYPEWRITER CONTENUTO (1.2 - 3.5s) ===
        elif t < 3.5:
            dt = t - 1.2
            
            # Titolo baule (typewriter)
            titleFull = self.chestName.upper() + " APERTO"
            charCount = int(dt * 20)
            if charCount > len(titleFull):
                charCount = len(titleFull)
            self.titleText.SetText(titleFull[:charCount])
            self.titleText.SetPackedFontColor(self.baseColor)
            
            # Icona baule
            if dt > 0.3:
                if self.hasJackpot:
                    self.iconLine1.SetText("*** JACKPOT! ***")
                    # Effetto rainbow/pulse per jackpot
                    import math
                    hue = (t * 2) % 1.0
                    r = int(255 * (0.5 + 0.5 * math.sin(hue * 6.28)))
                    g = int(255 * (0.5 + 0.5 * math.sin(hue * 6.28 + 2.09)))
                    b = int(255 * (0.5 + 0.5 * math.sin(hue * 6.28 + 4.18)))
                    self.iconLine1.SetPackedFontColor((0xFF << 24) | (r << 16) | (g << 8) | b)
                else:
                    self.iconLine1.SetText("[=== TESORO ===]")
                    self.iconLine1.SetPackedFontColor(0xFFFFD700)
            
            # Ricompense (appaiono una alla volta)
            rewardDelay = 0.6
            for i, (text, color) in enumerate(self.rewardLines):
                if dt > rewardDelay + i * 0.4:
                    lineTime = dt - (rewardDelay + i * 0.4)
                    lineChars = int(lineTime * 30)
                    if lineChars > len(text):
                        lineChars = len(text)
                    if i < len(self.rewardTexts):
                        self.rewardTexts[i].SetText(text[:lineChars])
                        self.rewardTexts[i].SetPackedFontColor(color)
            
            # Jackpot banner lampeggiante
            if self.hasJackpot and dt > 1.5:
                self.jackpotBanner.Show()
                import math
                pulse = 0.5 + 0.5 * math.sin((t - 2.7) * 8)
                bannerAlpha = int(200 * pulse)
                self.jackpotBanner.SetColor((bannerAlpha << 24) | 0xFFD700)
                self.jackpotText.SetText("!!! FORTUNA INCREDIBILE !!!")
            
            # Pulsazione bordi
            import math
            pulse = 0.6 + 0.4 * math.sin(t * 4)
            pulseAlpha = int(255 * pulse)
            
            if self.hasJackpot:
                # Bordi oro/viola alternati per jackpot
                if int(t * 4) % 2 == 0:
                    borderColor = (pulseAlpha << 24) | 0xFFD700
                else:
                    borderColor = (pulseAlpha << 24) | 0xAA00FF
            else:
                borderColor = (pulseAlpha << 24) | (self.baseColor & 0x00FFFFFF)
            
            self.borderLeft.SetColor(borderColor)
            self.borderRight.SetColor(borderColor)
            
            # Footer
            if dt > 2.0:
                import math
                blink = int(abs(math.sin((dt - 2.0) * 3)) * 180) + 75
                self.footerText.SetText("[ Clicca per chiudere ]")
                self.footerText.SetPackedFontColor((blink << 24) | 0xFFFFFF)
        
        # === FASE 4: FADE OUT ===
        else:
            fadeStart = 3.5
            fadeDuration = duration - fadeStart
            progress = (t - fadeStart) / fadeDuration
            
            fadeAlpha = int(220 * (1.0 - progress))
            self.bg.SetColor((fadeAlpha << 24) | 0x000508)
            
            # Tutto sfuma
            textAlpha = int(255 * (1.0 - progress))
            self.headerText.SetPackedFontColor((textAlpha << 24) | 0x00A8FF)

    def OnMouseLeftButtonUp(self):
        if self.startTime > 0 and (app.GetTime() - self.startTime) > 1.5:
            self.startTime = 0
            self.Hide()

# ==============================================================================
# 6. PARTY CHEST: Effetto rapido per distribuzione party
# ==============================================================================
class PartyChestEffect(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(400, 60)
        self.SetPosition(self.screenWidth/2 - 200, 150)
        self.AddFlag("not_pick")
        
        self.startTime = 0
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(400, 60)
        self.bg.SetColor(0xCC000000)
        self.bg.Show()

        self.border = ui.Bar()
        self.border.SetParent(self)
        self.border.SetPosition(0, 0)
        self.border.SetSize(400, 3)
        self.border.SetColor(0xFFFFD700)
        self.border.Show()

        self.text1 = ui.TextLine()
        self.text1.SetParent(self)
        self.text1.SetPosition(200, 15)
        self.text1.SetHorizontalAlignCenter()
        self.text1.SetText("")
        self.text1.SetPackedFontColor(0xFFFFD700)
        self.text1.SetOutline()
        self.text1.Show()

        self.text2 = ui.TextLine()
        self.text2.SetParent(self)
        self.text2.SetPosition(200, 35)
        self.text2.SetHorizontalAlignCenter()
        self.text2.SetText("")
        self.text2.SetPackedFontColor(0xFF00FF00)
        self.text2.Show()

    def Start(self, chestName, totalGlory, memberCount):
        self.startTime = app.GetTime()
        self.text1.SetText("PARTY: " + chestName.replace("+", " "))
        self.text2.SetText("+" + str(totalGlory) + " Gloria divisa tra " + str(memberCount) + " Hunter")
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if self.startTime == 0:
            return
        elapsed = app.GetTime() - self.startTime
        if elapsed > 3.0:
            self.startTime = 0
            self.Hide()

# ==============================================================================
# GESTIONE ISTANZE
# ==============================================================================
g_gateEntry = None
g_gateVictory = None
g_gateDefeat = None
g_popup = None
g_chestOpen = None
g_partyChest = None

def ShowGateEntry(gateName, colorCode):
    global g_gateEntry
    if g_gateEntry is None: g_gateEntry = GateEntryEffect()
    g_gateEntry.Start(gateName, colorCode)

def ShowGateVictory(gateName, gloria):
    global g_gateVictory
    if g_gateVictory is None: g_gateVictory = GateVictoryEffect()
    g_gateVictory.Start(gateName, gloria)

def ShowGateDefeat(penalty):
    global g_gateDefeat
    if g_gateDefeat is None: g_gateDefeat = GateDefeatEffect()
    g_gateDefeat.Start(penalty)

def ShowChestOpen(chestName, glory, colorCode, itemName="", jackpotGlory=0, jackpotItems=""):
    """Mostra effetto epico apertura baule in stile Solo Leveling"""
    global g_chestOpen
    if g_chestOpen is None: g_chestOpen = ChestOpenEffect()
    g_chestOpen.Start(chestName, glory, colorCode, itemName, jackpotGlory, jackpotItems)

def ShowPartyChest(chestName, totalGlory, memberCount):
    """Mostra notifica rapida party chest"""
    global g_partyChest
    if g_partyChest is None: g_partyChest = PartyChestEffect()
    g_partyChest.Start(chestName, totalGlory, memberCount)

def ShowTrialProgress(pType, cur, req):
    global g_popup
    if g_popup is None: g_popup = TrialProgressPopup()
    g_popup.AddPopup(pType, cur, req)

# ==============================================================================
# 7. GATE SELECTED - Effetto selezione sorteggio Gate
# ==============================================================================
class GateSelectedEffect(ui.Window):
    """Effetto quando il player viene sorteggiato per l'accesso al Gate"""

    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")

        self.startTime = 0
        self.gateName = "Gate"
        self.rankRequired = "E"
        self.hoursLeft = 2
        self.minsLeft = 0

        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        # Sfondo semi-trasparente
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.Show()

        # Banner centrale
        self.banner = ui.Bar()
        self.banner.SetParent(self)
        self.banner.SetSize(500, 180)
        self.banner.SetPosition(self.screenWidth/2 - 250, self.screenHeight/2 - 90)
        self.banner.SetColor(0xEE111122)
        self.banner.Hide()

        # Bordi luminosi
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self.banner)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(500, 4)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.Show()

        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self.banner)
        self.borderBot.SetPosition(0, 176)
        self.borderBot.SetSize(500, 4)
        self.borderBot.SetColor(0xFFFFD700)
        self.borderBot.Show()

        # Icona stella/alert
        self.alertIcon = ui.TextLine()
        self.alertIcon.SetParent(self.banner)
        self.alertIcon.SetPosition(250, 15)
        self.alertIcon.SetHorizontalAlignCenter()
        self.alertIcon.SetText("*")
        self.alertIcon.SetPackedFontColor(0xFFFFD700)
        self.alertIcon.SetOutline()
        self.alertIcon.Show()

        # Titolo principale
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self.banner)
        self.titleText.SetPosition(250, 35)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.Show()

        # Nome Gate
        self.gateText = ui.TextLine()
        self.gateText.SetParent(self.banner)
        self.gateText.SetPosition(250, 65)
        self.gateText.SetHorizontalAlignCenter()
        self.gateText.SetText("")
        self.gateText.SetPackedFontColor(0xFF00FF00)
        self.gateText.SetOutline()
        self.gateText.Show()

        # Rank richiesto
        self.rankText = ui.TextLine()
        self.rankText.SetParent(self.banner)
        self.rankText.SetPosition(250, 95)
        self.rankText.SetHorizontalAlignCenter()
        self.rankText.SetText("")
        self.rankText.SetPackedFontColor(0xFF00FFFF)
        self.rankText.Show()

        # Tempo rimasto
        self.timeText = ui.TextLine()
        self.timeText.SetParent(self.banner)
        self.timeText.SetPosition(250, 120)
        self.timeText.SetHorizontalAlignCenter()
        self.timeText.SetText("")
        self.timeText.SetPackedFontColor(0xFFFF6600)
        self.timeText.Show()

        # Istruzioni
        self.hintText = ui.TextLine()
        self.hintText.SetParent(self.banner)
        self.hintText.SetPosition(250, 150)
        self.hintText.SetHorizontalAlignCenter()
        self.hintText.SetText("")
        self.hintText.SetPackedFontColor(0xFFAAAAAA)
        self.hintText.Show()

        # Particelle decorative
        self.particles = []
        for i in xrange(30):
            p = ui.Bar()
            p.SetParent(self)
            p.SetSize(3, 3)
            p.SetColor(0xFFFFD700)
            p.Hide()
            self.particles.append({"bar": p, "x": 0, "y": 0, "vx": 0, "vy": 0})

    def Start(self, gateName, rankRequired, hoursLeft, minsLeft):
        self.gateName = gateName.replace("+", " ")
        self.rankRequired = rankRequired
        self.hoursLeft = hoursLeft
        self.minsLeft = minsLeft
        self.startTime = app.GetTime()

        # Prepara testi
        self.titleText.SetText("SEI STATO SELEZIONATO!")
        self.gateText.SetText("Gate: " + self.gateName)
        self.rankText.SetText("Rango: " + self.rankRequired + "-Rank")
        self.timeText.SetText("Tempo: " + str(self.hoursLeft) + "h " + str(self.minsLeft) + "m")
        self.hintText.SetText("Apri il Terminale per entrare!")

        # Inizializza particelle
        cx = self.screenWidth / 2
        cy = self.screenHeight / 2
        for p in self.particles:
            angle = app.GetRandom(0, 360) * 3.14159 / 180.0
            speed = app.GetRandom(50, 150)
            p["x"] = cx
            p["y"] = cy
            p["vx"] = math.cos(angle) * speed
            p["vy"] = math.sin(angle) * speed

        self.bg.SetColor(0x00000000)
        self.banner.Hide()
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if self.startTime == 0:
            return

        t = app.GetTime() - self.startTime
        duration = 5.0

        if t > duration:
            self.startTime = 0
            self.Hide()
            return

        # === FASE 1: Fade in sfondo + particelle esplosione (0-1s) ===
        if t < 1.0:
            progress = t / 1.0
            bgAlpha = int(180 * progress)
            self.bg.SetColor((bgAlpha << 24) | 0x000011)

            # Anima particelle in esplosione
            dt = 0.016
            for p in self.particles:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["vy"] += 100 * dt  # gravita

                pAlpha = int(255 * (1.0 - progress))
                p["bar"].SetPosition(int(p["x"]), int(p["y"]))
                p["bar"].SetColor((pAlpha << 24) | 0xFFD700)
                p["bar"].Show()

        # === FASE 2: Banner appare (1-1.5s) ===
        elif t < 1.5:
            for p in self.particles:
                p["bar"].Hide()

            self.bg.SetColor(0xB4000011)
            self.banner.Show()

            # Effetto pulse sul bordo
            pulse = int(127 + 127 * math.sin(t * 10))
            pulseColor = (0xFF << 24) | (pulse << 16) | (pulse << 8) | 0x00
            self.borderTop.SetColor(0xFFFFD700)
            self.borderBot.SetColor(0xFFFFD700)

        # === FASE 3: Testo stabile + pulse icona (1.5-4.5s) ===
        elif t < duration - 0.5:
            # Pulse sull'icona alert
            pulse = 0.7 + 0.3 * math.sin(t * 5)
            iconAlpha = int(255 * pulse)
            self.alertIcon.SetPackedFontColor((iconAlpha << 24) | 0xFFD700)

        # === FASE 4: Fade out (4.5-5s) ===
        else:
            fadeProgress = (t - (duration - 0.5)) / 0.5
            fadeAlpha = int(180 * (1.0 - fadeProgress))
            self.bg.SetColor((fadeAlpha << 24) | 0x000011)

            bannerAlpha = int(238 * (1.0 - fadeProgress))
            self.banner.SetColor((bannerAlpha << 24) | 0x111122)

g_gateSelected = None

def ShowGateSelected(gateName, rankRequired, hoursLeft, minsLeft):
    """Mostra effetto selezione Gate con notifica epica"""
    global g_gateSelected
    if g_gateSelected is None:
        g_gateSelected = GateSelectedEffect()
    g_gateSelected.Start(gateName, rankRequired, hoursLeft, minsLeft)


# ==============================================================================
# RESET ALL GATE EFFECTS - Chiamato su cambio mappa/logout/relog
# ==============================================================================
def ResetAllGateEffects():
    """Resetta e nasconde tutti gli effetti Gate al cambio mappa/logout/relog"""
    global g_gateEntry, g_gateVictory, g_gateDefeat, g_popup, g_chestOpen, g_partyChest, g_gateSelected

    # Reset GateEntry
    if g_gateEntry is not None:
        try:
            g_gateEntry.isActive = False
            g_gateEntry.Hide()
        except:
            pass

    # Reset GateVictory
    if g_gateVictory is not None:
        try:
            g_gateVictory.isActive = False
            g_gateVictory.Hide()
        except:
            pass

    # Reset GateDefeat
    if g_gateDefeat is not None:
        try:
            g_gateDefeat.isActive = False
            g_gateDefeat.Hide()
        except:
            pass

    # Reset Popup
    if g_popup is not None:
        try:
            g_popup.Hide()
        except:
            pass

    # Reset ChestOpen
    if g_chestOpen is not None:
        try:
            g_chestOpen.isActive = False
            g_chestOpen.Hide()
        except:
            pass

    # Reset PartyChest
    if g_partyChest is not None:
        try:
            g_partyChest.isActive = False
            g_partyChest.Hide()
        except:
            pass

    # Reset GateSelected
    if g_gateSelected is not None:
        try:
            g_gateSelected.isActive = False
            g_gateSelected.Hide()
        except:
            pass