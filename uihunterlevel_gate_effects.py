# -*- coding: utf-8 -*-
import ui
import wndMgr
import app
import math

# ==============================================================================
# CONFIGURAZIONE E COLORI – SOLO LEVELING DEFINITIVE PALETTE
# ==============================================================================
COLOR_CODES = {
    "RED":        0xFFFF1111,  # Rosso sangue puro
    "BLUE":       0xFF00AAFF,  # Blu azzurro vivace
    "PURPLE":     0xFFBB00FF,  # Viola mistico profondo
    "GOLD":       0xFFFFD700,  # Oro reale
    "GREEN":      0xFF00FF44,  # Verde neon smeraldo
    "ORANGE":     0xFFFF7700,  # Arancione fuoco
    "BLACKWHITE": 0xFFDDDDDD,  # Bianco argentato
    "SYSTEM":     0xFF00CCFF,  # Azzurro sistema vibrante
    "CYAN":       0xFF00FFFF,  # Ciano cristallo
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
        # 1. Sfondo Totale (Abisso digitale assoluto)
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0xFF000000)
        self.bg.Show()

        # 1b. Overlay colorato (tinta cromatica durante l'impatto)
        self.bgOverlay = ui.Bar()
        self.bgOverlay.SetParent(self)
        self.bgOverlay.SetPosition(0, 0)
        self.bgOverlay.SetSize(self.screenWidth, self.screenHeight)
        self.bgOverlay.SetColor(0x00000000)
        self.bgOverlay.AddFlag("not_pick")
        self.bgOverlay.Show()

        # 2. Glow Scanline (morbido, dietro la linea principale)
        self.scanGlow = ui.Bar()
        self.scanGlow.SetParent(self)
        self.scanGlow.SetPosition(0, -4)
        self.scanGlow.SetSize(self.screenWidth, 10)
        self.scanGlow.SetColor(0x2200CCFF)
        self.scanGlow.AddFlag("not_pick")
        self.scanGlow.Hide()

        # 2b. Linea di Scansione principale - 3px per impatto visivo
        self.scanLine = ui.Bar()
        self.scanLine.SetParent(self)
        self.scanLine.SetPosition(0, 0)
        self.scanLine.SetSize(self.screenWidth, 3)
        self.scanLine.SetColor(0xFF00CCFF)
        self.scanLine.Hide()

        # 3. Box Centrale "ALERT" - sfondo abissale blu-nero
        self.alertBox = ui.Bar()
        self.alertBox.SetParent(self)
        self.alertBox.SetSize(600, 150)
        self.alertBox.SetPosition(self.screenWidth/2 - 300, self.screenHeight/2 - 75)
        self.alertBox.SetColor(0xEE020210)
        self.alertBox.Hide()

        # Layer interiore profondita'
        self.alertBgInner = ui.Bar()
        self.alertBgInner.SetParent(self.alertBox)
        self.alertBgInner.SetPosition(6, 3)
        self.alertBgInner.SetSize(588, 144)
        self.alertBgInner.SetColor(0x0C080820)
        self.alertBgInner.AddFlag("not_pick")
        self.alertBgInner.Show()

        # Striscia header superiore (effetto profondita')
        self.alertTopStrip = ui.Bar()
        self.alertTopStrip.SetParent(self.alertBox)
        self.alertTopStrip.SetPosition(6, 3)
        self.alertTopStrip.SetSize(588, 18)
        self.alertTopStrip.SetColor(0x1800A8FF)
        self.alertTopStrip.AddFlag("not_pick")
        self.alertTopStrip.Show()

        # Bordo superiore - 3px (spesso = priorita' visiva massima)
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self.alertBox)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(600, 3)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.Show()

        # Bordo inferiore - 2px (asimmetrico: meno importante)
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self.alertBox)
        self.borderBot.SetPosition(0, 148)
        self.borderBot.SetSize(600, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.Show()

        # Bordo sinistro - 6px (accent bar dominante)
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self.alertBox)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(6, 150)
        self.borderLeft.SetColor(0xFF00CCFF)
        self.borderLeft.Show()

        # Bordo destro - 2px
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self.alertBox)
        self.borderRight.SetPosition(598, 0)
        self.borderRight.SetSize(2, 150)
        self.borderRight.SetColor(0xFF00CCFF)
        self.borderRight.Show()

        # Corner ticks L-bracket (angoli decorativi - stile Solo Leveling)
        self.alertCorners = []
        tickLen = 16
        for (cx, cy, cw, ch) in [
            (6, 3, tickLen, 1),   (6, 3, 1, tickLen),                          # TL H + V
            (600-tickLen-2, 3, tickLen, 1), (598, 3, 1, tickLen),              # TR H + V
            (6, 147, tickLen, 1), (6, 147-tickLen, 1, tickLen),                # BL H + V
            (600-tickLen-2, 147, tickLen, 1), (598, 147-tickLen, 1, tickLen),  # BR H + V
        ]:
            ct = ui.Bar()
            ct.SetParent(self.alertBox)
            ct.SetPosition(cx, cy)
            ct.SetSize(cw, ch)
            ct.SetColor(0xFF00EEFF)
            ct.AddFlag("not_pick")
            ct.Show()
            self.alertCorners.append(ct)

        # Label "[ SYSTEM ALERT ]" nel header
        self.alertHeaderText = ui.TextLine()
        self.alertHeaderText.SetParent(self.alertBox)
        self.alertHeaderText.SetPosition(300, 5)
        self.alertHeaderText.SetHorizontalAlignCenter()
        self.alertHeaderText.SetText("[ SYSTEM ALERT ]")
        self.alertHeaderText.SetPackedFontColor(0xFF80CCFF)
        self.alertHeaderText.SetOutline()
        self.alertHeaderText.Show()

        # Testo Principale (sotto header)
        self.mainText = ui.TextLine()
        self.mainText.SetParent(self.alertBox)
        self.mainText.SetPosition(300, 35)
        self.mainText.SetHorizontalAlignCenter()
        self.mainText.SetText("! SYSTEM ALERT !")
        self.mainText.SetOutline()
        self.mainText.Show()

        # Separatore orizzontale tra main e sub
        self.alertSep = ui.Bar()
        self.alertSep.SetParent(self.alertBox)
        self.alertSep.SetPosition(20, 65)
        self.alertSep.SetSize(560, 1)
        self.alertSep.SetColor(0x3300AAFF)
        self.alertSep.AddFlag("not_pick")
        self.alertSep.Show()

        # Testo Secondario (Nome Gate - typewriter)
        self.subText = ui.TextLine()
        self.subText.SetParent(self.alertBox)
        self.subText.SetPosition(300, 75)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText("")
        self.subText.SetOutline()
        self.subText.Show()

        # Glitch Bars - aumentate a 22 per effetto piu' caotico
        self.glitchBars = []
        for i in xrange(22):
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

        # Colori derivati dal baseColor
        r = (self.baseColor >> 16) & 0xFF
        g = (self.baseColor >> 8) & 0xFF
        b = self.baseColor & 0xFF
        glowCol   = (0x22 << 24) | (r << 16) | (g << 8) | b
        stripCol  = (0x18 << 24) | (r << 16) | (g << 8) | b
        sepCol    = (0x33 << 24) | (r << 16) | (g << 8) | b
        brightR = min(255, r + 60)
        brightG = min(255, g + 60)
        brightB = min(255, b + 60)
        cyanCol = 0xFF000000 | (brightR << 16) | (brightG << 8) | brightB

        # ==========================================
        # HARD RESET DEGLI STATI VISIVI (FIX)
        # ==========================================
        self.bg.SetColor(0xFF000000)
        self.bgOverlay.SetColor(0x00000000)

        # Aggiorna colori elementi cromatici con baseColor
        self.scanGlow.SetColor(glowCol)
        self.scanLine.SetColor(self.baseColor)
        self.alertTopStrip.SetColor(stripCol)
        self.alertSep.SetColor(sepCol)
        for ct in self.alertCorners:
            ct.SetColor(cyanCol)

        # 1. Ripristina dimensioni originali del box
        self.alertBox.SetSize(600, 150)
        self.alertBox.SetPosition(int(self.screenWidth/2 - 300), int(self.screenHeight/2 - 75))

        # 2. Ripristina componenti interni
        self.mainText.Show()
        self.mainText.SetText("! DANGER !")
        self.mainText.SetPackedFontColor(0xFFFF0000)

        self.subText.Show()
        self.subText.SetText("")

        self.alertHeaderText.Show()
        self.borderLeft.SetColor(self.baseColor)
        self.borderRight.SetColor(self.baseColor)
        self.borderTop.SetColor(self.baseColor)
        self.borderBot.SetColor(self.baseColor)
        self.borderLeft.Show()
        self.borderRight.Show()
        self.borderTop.Show()
        self.borderBot.Show()

        # 3. Nascondi container principali per l'inizio animazione
        self.alertBox.Hide()
        self.scanLine.Hide()
        self.scanGlow.Hide()
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
            self.scanGlow.Show()
            yPos = int((t / 1.0) * self.screenHeight)
            self.scanLine.SetPosition(0, yPos)
            self.scanGlow.SetPosition(0, yPos - 4)

            # Glitch casuali piu' intensi
            for b in self.glitchBars:
                if app.GetRandom(0, 100) > 70:
                    w = app.GetRandom(30, 500)
                    x = app.GetRandom(0, self.screenWidth - w)
                    y = app.GetRandom(0, self.screenHeight)
                    b.SetPosition(x, y)
                    b.SetSize(w, app.GetRandom(1, 4))
                    b.SetColor(self.baseColor)
                    b.Show()
                else:
                    b.Hide()

        # FASE 2: ALERT BOX IMPACT (1.0s - 1.2s)
        elif t < 1.2:
            self.scanLine.Hide()
            self.scanGlow.Hide()
            for b in self.glitchBars: b.Hide()

            # Flash del box + overlay colorato
            self.alertBox.Show()
            self.borderLeft.SetColor(self.baseColor)
            self.borderRight.SetColor(self.baseColor)
            self.borderTop.SetColor(self.baseColor)
            self.borderBot.SetColor(self.baseColor)
            self.mainText.SetPackedFontColor(self.baseColor)
            self.mainText.SetText("! DUNGEON DETECTED !")

            # Flash overlay con colore del gate
            r = (self.baseColor >> 16) & 0xFF
            g = (self.baseColor >> 8) & 0xFF
            b = self.baseColor & 0xFF
            flashAlpha = int((1.2 - t) / 0.2 * 28)
            self.bgOverlay.SetColor((flashAlpha << 24) | (r << 16) | (g << 8) | b)

        # FASE 3: TYPEWRITER EFFECT & PULSE (1.2s - 4.0s)
        elif t < 4.0:
            self.alertBox.Show()
            self.bgOverlay.SetColor(0x00000000)

            # Scrittura tipo terminale
            fullStr = "ENTERING: " + self.gateName
            dt = t - 1.2
            charCount = int(dt * 25)
            if charCount > len(fullStr): charCount = len(fullStr)
            self.subText.SetText(fullStr[:charCount])

            # Pulsazione Colore bordi
            pulse = abs(math.sin(t * 6.0))
            r = (self.baseColor >> 16) & 0xFF
            g = (self.baseColor >> 8) & 0xFF
            b = self.baseColor & 0xFF
            mr = int(r * pulse)
            mg = int(g * pulse)
            mb = int(b * pulse)
            col = (0xFF << 24) | (mr << 16) | (mg << 8) | mb

            self.borderLeft.SetColor(col)
            self.borderRight.SetColor(col)
            self.borderTop.SetColor(col)
            self.borderBot.SetColor(col)
            self.subText.SetPackedFontColor(0xFFFFFFFF)

            # Sfondo: aura tech cromatica pulsante
            bgPulse = int(pulse * 80)
            br = int(r * 0.2)
            self.bg.SetColor((bgPulse << 24) | (br << 16))

        # FASE 4: SYSTEM SHUTDOWN (Fade Out) (4.0s - 5.0s)
        elif t < 5.0:
            normT = (t - 4.0)
            currentWidth = int(600 * (1.0 - normT))
            if currentWidth < 0: currentWidth = 0

            self.alertBox.SetSize(currentWidth, 150 if normT < 0.3 else 2)
            self.alertBox.SetPosition(int(self.screenWidth/2 - currentWidth/2), int(self.screenHeight/2 - 75))

            self.mainText.Hide()
            self.subText.Hide()
            self.alertHeaderText.Hide()
            self.borderLeft.Hide()
            self.borderRight.Hide()
            self.borderTop.Hide()
            self.borderBot.Hide()

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
        # Sfondo scuro semi-trasparente
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0xBB000000)
        self.bg.Show()

        # Glow dorato dietro al banner (piu' ampio)
        self.bannerGlow = ui.Bar()
        self.bannerGlow.SetParent(self)
        self.bannerGlow.SetSize(0, 130)
        self.bannerGlow.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 65))
        self.bannerGlow.SetColor(0x22FFD700)
        self.bannerGlow.AddFlag("not_pick")
        self.bannerGlow.Show()

        # Banner principale - core scuro con bordi oro
        self.banner = ui.Bar()
        self.banner.SetParent(self)
        self.banner.SetSize(0, 100)
        self.banner.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 50))
        self.banner.SetColor(0xDD050300)
        self.banner.Show()

        # Banner bordo superiore (3px)
        self.bannerBorderTop = ui.Bar()
        self.bannerBorderTop.SetParent(self.banner)
        self.bannerBorderTop.SetPosition(0, 0)
        self.bannerBorderTop.SetSize(0, 3)
        self.bannerBorderTop.SetColor(0xFFFFD700)
        self.bannerBorderTop.AddFlag("not_pick")
        self.bannerBorderTop.Show()

        # Banner bordo inferiore (2px)
        self.bannerBorderBot = ui.Bar()
        self.bannerBorderBot.SetParent(self.banner)
        self.bannerBorderBot.SetPosition(0, 98)
        self.bannerBorderBot.SetSize(0, 2)
        self.bannerBorderBot.SetColor(0xFFCC8800)
        self.bannerBorderBot.AddFlag("not_pick")
        self.bannerBorderBot.Show()

        # Linea accent sinistra (6px)
        self.bannerAccentL = ui.Bar()
        self.bannerAccentL.SetParent(self.banner)
        self.bannerAccentL.SetPosition(0, 0)
        self.bannerAccentL.SetSize(6, 100)
        self.bannerAccentL.SetColor(0xFFFFD700)
        self.bannerAccentL.AddFlag("not_pick")
        self.bannerAccentL.Show()

        # Separatore decorativo orizzontale nel banner
        self.bannerSep = ui.Bar()
        self.bannerSep.SetParent(self.banner)
        self.bannerSep.SetPosition(20, 50)
        self.bannerSep.SetSize(0, 1)
        self.bannerSep.SetColor(0x44FFD700)
        self.bannerSep.AddFlag("not_pick")
        self.bannerSep.Show()

        # Titolo principale
        self.title = ui.TextLine()
        self.title.SetParent(self)
        self.title.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 22))
        self.title.SetHorizontalAlignCenter()
        self.title.SetText("DUNGEON COMPLETATO")
        self.title.SetPackedFontColor(0xFFFFFFFF)
        self.title.SetOutline()
        self.title.Show()

        # Label header "[ SISTEMA ]"
        self.bannerHeader = ui.TextLine()
        self.bannerHeader.SetParent(self)
        self.bannerHeader.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 40))
        self.bannerHeader.SetHorizontalAlignCenter()
        self.bannerHeader.SetText("[ SISTEMA ]")
        self.bannerHeader.SetPackedFontColor(0xFFCC8800)
        self.bannerHeader.SetOutline()
        self.bannerHeader.Show()

        # Testo ricompensa
        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 + 8))
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFD700)
        self.rewardText.SetOutline()
        self.rewardText.Show()

        # Particelle con colori variati: oro, bianco, ciano
        PARTICLE_COLORS = [0xFFFFD700, 0xFFFFFFFF, 0xFF00EEFF, 0xFFFFAA00, 0xFFFFEE88]
        self.particles = []
        for i in xrange(28):
            p = ui.Bar()
            p.SetParent(self)
            sz = 3 if i % 3 == 0 else 4
            p.SetSize(sz, sz)
            p.SetColor(PARTICLE_COLORS[i % len(PARTICLE_COLORS)])
            p.Hide()
            self.particles.append([p, 0, 0])

    def Start(self, gateName, gloria):
        self.startTime = app.GetTime()
        self.rewardText.SetText("+ %d GLORIA" % gloria)
        self.banner.SetSize(0, 100)
        self.bannerGlow.SetSize(0, 130)
        self.bannerBorderTop.SetSize(0, 3)
        self.bannerBorderBot.SetSize(0, 2)
        self.bannerSep.SetSize(0, 1)
        self.Show()
        self.SetTop()

        for p in self.particles:
            p[0].SetPosition(int(self.screenWidth/2), int(self.screenHeight/2))
            p[0].Show()
            p[1] = app.GetRandom(-12, 12)
            p[2] = app.GetRandom(-14, -2)

    def OnUpdate(self):
        if not self.IsShow(): return
        t = app.GetTime() - self.startTime

        if t < 0.5:
            width = int((t / 0.5) * self.screenWidth)
            halfW = int(width / 2)
            self.banner.SetSize(width, 100)
            self.banner.SetPosition(int(self.screenWidth/2 - halfW), int(self.screenHeight/2 - 50))
            self.bannerGlow.SetSize(width, 130)
            self.bannerGlow.SetPosition(int(self.screenWidth/2 - halfW), int(self.screenHeight/2 - 65))
            self.bannerBorderTop.SetSize(width, 3)
            self.bannerBorderBot.SetSize(width, 2)
            innerW = max(0, width - 40)
            self.bannerSep.SetSize(innerW, 1)
        else:
            self.banner.SetSize(self.screenWidth, 100)
            self.banner.SetPosition(0, int(self.screenHeight/2 - 50))
            self.bannerGlow.SetSize(self.screenWidth, 130)
            self.bannerGlow.SetPosition(0, int(self.screenHeight/2 - 65))
            self.bannerBorderTop.SetSize(self.screenWidth, 3)
            self.bannerBorderBot.SetSize(self.screenWidth, 2)
            self.bannerSep.SetSize(self.screenWidth - 40, 1)

        # Pulsazione glow oro
        if t < 4.0:
            glowAlpha = int(abs(math.sin(t * 3.0)) * 0x40 + 0x10)
            self.bannerGlow.SetColor((glowAlpha << 24) | 0xFFD700)

        if t < 3.0:
            for p in self.particles:
                x, y = p[0].GetLocalPosition()
                x += p[1]
                y += p[2]
                p[2] += 0.4
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
        # Sfondo nero (inizia vuoto, si riempie di rosso sangue)
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.Show()

        # Overlay rosso vignette (bordi piu' scuri al centro piu' chiaro)
        self.bloodOverlay = ui.Bar()
        self.bloodOverlay.SetParent(self)
        self.bloodOverlay.SetPosition(0, 0)
        self.bloodOverlay.SetSize(self.screenWidth, self.screenHeight)
        self.bloodOverlay.SetColor(0x00000000)
        self.bloodOverlay.AddFlag("not_pick")
        self.bloodOverlay.Show()

        # Crack bars - piu' numerose e colorate di rosso/nero
        self.cracks = []
        CRACK_COLORS = [0xFFAA0000, 0xFF880000, 0xFF660000, 0xFF440000, 0xFF220000,
                        0xFFCC0000, 0xFF990000]
        for i in xrange(10):
            c = ui.Bar()
            c.SetParent(self)
            c.SetColor(CRACK_COLORS[i % len(CRACK_COLORS)])
            c.Hide()
            self.cracks.append(c)

        # Label "[ SISTEMA ]"
        self.sysLabel = ui.TextLine()
        self.sysLabel.SetParent(self)
        self.sysLabel.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2 - 28))
        self.sysLabel.SetHorizontalAlignCenter()
        self.sysLabel.SetText("[ SISTEMA ]")
        self.sysLabel.SetPackedFontColor(0xFFAA0000)
        self.sysLabel.SetOutline()
        self.sysLabel.Show()

        # Testo principale sconfitta
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(int(self.screenWidth/2), int(self.screenHeight/2))
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("CRITICAL FAILURE")
        self.text.SetPackedFontColor(0xFF000000)
        self.text.SetOutline()
        self.text.Show()

        # Separatore sotto il testo
        self.defeatSep = ui.Bar()
        self.defeatSep.SetParent(self)
        self.defeatSep.SetPosition(int(self.screenWidth/2) - 120, int(self.screenHeight/2) + 18)
        self.defeatSep.SetSize(240, 1)
        self.defeatSep.SetColor(0x55FF0000)
        self.defeatSep.AddFlag("not_pick")
        self.defeatSep.Show()

    def Start(self, penalty):
        self.startTime = app.GetTime()
        self.text.SetText("SEI MORTO (-%d GLORIA)" % penalty)
        self.text.SetPackedFontColor(0xFF000000)
        self.sysLabel.SetPackedFontColor(0xFFAA0000)

        for c in self.cracks:
            w = app.GetRandom(40, 500)
            h = app.GetRandom(1, 4)
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

        if t < 0.15:
            # Flash bianco accecante
            self.bg.SetColor(0xDDFFFFFF)
            self.bloodOverlay.SetColor(0x00000000)
        elif t < 3.0:
            # Sangue rosso che si intensifica
            redAlpha = min(0x99, int((t - 0.15) / 2.85 * 0x99))
            self.bg.SetColor((redAlpha << 24) | 0x880000)
            self.bloodOverlay.SetColor(0x22880000)
            self.text.SetPackedFontColor(0xFFFFCCCC)
            self.sysLabel.SetPackedFontColor(0xFFFF4444)
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
        # Sfondo scuro profondo
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(self.w, self.h)
        self.bg.SetPosition(0, 0)
        self.bg.SetColor(0xF0020210)
        self.bg.Show()

        # Layer interiore depth
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self.bg)
        self.bgInner.SetPosition(5, 0)
        self.bgInner.SetSize(self.w - 5, self.h)
        self.bgInner.SetColor(0x080808FF)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # Bordo superiore (2px, colore verrà aggiornato da AddPopup)
        self.topBorder = ui.Bar()
        self.topBorder.SetParent(self.bg)
        self.topBorder.SetPosition(0, 0)
        self.topBorder.SetSize(self.w, 2)
        self.topBorder.SetColor(0xFFFFFFFF)
        self.topBorder.AddFlag("not_pick")
        self.topBorder.Show()

        # Bordo destro (1px, dim)
        self.rightBorder = ui.Bar()
        self.rightBorder.SetParent(self.bg)
        self.rightBorder.SetPosition(self.w - 1, 0)
        self.rightBorder.SetSize(1, self.h)
        self.rightBorder.SetColor(0x44FFFFFF)
        self.rightBorder.AddFlag("not_pick")
        self.rightBorder.Show()

        # Bordo inferiore (1px, dim)
        self.botBorder = ui.Bar()
        self.botBorder.SetParent(self.bg)
        self.botBorder.SetPosition(0, self.h - 1)
        self.botBorder.SetSize(self.w, 1)
        self.botBorder.SetColor(0x44FFFFFF)
        self.botBorder.AddFlag("not_pick")
        self.botBorder.Show()

        # Accent bar sinistra (6px, colore del tipo)
        self.sideBar = ui.Bar()
        self.sideBar.SetParent(self.bg)
        self.sideBar.SetSize(5, self.h)
        self.sideBar.SetPosition(0, 0)
        self.sideBar.SetColor(0xFFFFFFFF)
        self.sideBar.Show()

        # Corner ticks TL
        self.cornerTL_H = ui.Bar()
        self.cornerTL_H.SetParent(self.bg)
        self.cornerTL_H.SetPosition(5, 2)
        self.cornerTL_H.SetSize(10, 1)
        self.cornerTL_H.SetColor(0xFFFFFFFF)
        self.cornerTL_H.AddFlag("not_pick")
        self.cornerTL_H.Show()

        self.cornerTL_V = ui.Bar()
        self.cornerTL_V.SetParent(self.bg)
        self.cornerTL_V.SetPosition(5, 2)
        self.cornerTL_V.SetSize(1, 10)
        self.cornerTL_V.SetColor(0xFFFFFFFF)
        self.cornerTL_V.AddFlag("not_pick")
        self.cornerTL_V.Show()

        # Label tipo (piccolo header)
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self.bg)
        self.titleText.SetPosition(20, 7)
        self.titleText.SetText("[ UPDATE ]")
        self.titleText.SetPackedFontColor(0xFF888899)
        self.titleText.Show()

        # Testo progresso (piu' grande, principale)
        self.progText = ui.TextLine()
        self.progText.SetParent(self.bg)
        self.progText.SetPosition(20, 26)
        self.progText.SetText("")
        self.progText.SetPackedFontColor(0xFFFFFFFF)
        self.progText.Show()

    def AddPopup(self, pType, current, required):
        pType = pType.upper()
        colMap = {
            "BOSS":     0xFFFF2222,
            "METIN":    0xFFFFD700,
            "FRACTURE": 0xFFBB00FF,
            "MISSION":  0xFF00FF44,
            "CHEST":    0xFF00AAFF
        }
        barColor = colMap.get(pType, 0xFFCCCCCC)
        self.sideBar.SetColor(barColor)
        self.topBorder.SetColor(barColor)
        self.cornerTL_H.SetColor(barColor)
        self.cornerTL_V.SetColor(barColor)

        self.titleText.SetText("[ " + pType + " ]")
        self.titleText.SetPackedFontColor((0xFF << 24) | (barColor & 0x00FFFFFF))
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
# CHEST SPAWN EFFECT - Notifica spawn baule dopo difesa frattura
# ==============================================================================
g_chestSpawn = None

def ShowChestSpawn(chestName, colorCode, rank):
    """Mostra effetto epico spawn baule dopo difesa frattura"""
    global g_chestSpawn
    if g_chestSpawn is None: g_chestSpawn = ChestSpawnEffect()
    g_chestSpawn.Start(chestName, colorCode, rank)

class ChestSpawnEffect(ui.Window):
    """Effetto notifica spawn baule in stile Solo Leveling"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(450, 100)
        self.SetPosition(self.screenWidth/2 - 225, 200)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        
        self.startTime = 0
        self.chestName = "Baule"
        self.colorCode = "GOLD"
        self.rank = "E"
        
        self.__BuildUI()
        self.Hide()
    
    def __BuildUI(self):
        # Sfondo principale
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(450, 100)
        self.bg.SetColor(0xDD0A0A12)
        self.bg.Show()
        
        # Bordo superiore
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(450, 3)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.Show()
        
        # Bordo inferiore
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, 97)
        self.borderBottom.SetSize(450, 3)
        self.borderBottom.SetColor(0xFFFFD700)
        self.borderBottom.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(225, 15)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("[ T E S O R O  R I L E V A T O ]")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        # Nome baule
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(225, 40)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(0xFF00FF00)
        self.nameText.SetOutline()
        self.nameText.Show()
        
        # Messaggio
        self.msgText = ui.TextLine()
        self.msgText.SetParent(self)
        self.msgText.SetPosition(225, 65)
        self.msgText.SetHorizontalAlignCenter()
        self.msgText.SetText("Cliccalo per ottenere la ricompensa!")
        self.msgText.SetPackedFontColor(0xFFAAAAAA)
        self.msgText.SetOutline()
        self.msgText.Show()
    
    def Start(self, chestName, colorCode, rank):
        self.chestName = chestName.replace("+", " ")
        self.colorCode = colorCode
        self.rank = rank
        self.startTime = app.GetTime()
        
        # Imposta colore in base al rank
        color = GetColor(colorCode)
        self.nameText.SetText(self.chestName + " [" + rank + "-Rank]")
        self.nameText.SetPackedFontColor(color)
        self.borderTop.SetColor(color)
        self.borderBottom.SetColor(color)
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.startTime == 0:
            return
        
        elapsed = app.GetTime() - self.startTime
        
        # Lampeggio bordi
        import math
        pulse = 0.5 + 0.5 * math.sin(elapsed * 4)
        pulseAlpha = int(180 + 75 * pulse)
        color = GetColor(self.colorCode)
        pulseColor = (pulseAlpha << 24) | (color & 0x00FFFFFF)
        self.borderTop.SetColor(pulseColor)
        self.borderBottom.SetColor(pulseColor)
        
        # Nascondi dopo 5 secondi
        if elapsed > 5.0:
            self.startTime = 0
            self.Hide()

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