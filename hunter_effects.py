# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - FULLSCREEN EFFECTS
#  Effetti epici a schermo intero stile Solo Leveling
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import wndMgr
import app
import math

from hunter_core import (
    AWAKENING_CONFIG, RANK_COLORS, RANK_NAMES, RANK_TITLES, RANK_QUOTES,
    COLOR_SCHEMES, GetAwakeningConfig, IsAwakeningLevel
)


# ═══════════════════════════════════════════════════════════════════════════════
#  BOSS ALERT - Alert a schermo intero quando spawna un boss
# ═══════════════════════════════════════════════════════════════════════════════
class BossAlertWindow(ui.Window):
    """Alert a schermo intero stile Solo Leveling - Boss Detection"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        self.AddFlag("attach")
        
        self.barHeight = 120
        self.barY = (self.screenHeight - self.barHeight) // 2
        
        # Layer 1: Glow esterno
        self.glowOuter = ui.Bar()
        self.glowOuter.SetParent(self)
        self.glowOuter.SetPosition(0, self.barY - 30)
        self.glowOuter.SetSize(self.screenWidth, self.barHeight + 60)
        self.glowOuter.SetColor(0x15FF0000)
        self.glowOuter.AddFlag("not_pick")
        self.glowOuter.Show()
        
        # Layer 2: Glow medio
        self.glowMiddle = ui.Bar()
        self.glowMiddle.SetParent(self)
        self.glowMiddle.SetPosition(0, self.barY - 15)
        self.glowMiddle.SetSize(self.screenWidth, self.barHeight + 30)
        self.glowMiddle.SetColor(0x25FF0000)
        self.glowMiddle.AddFlag("not_pick")
        self.glowMiddle.Show()
        
        # Layer 3: Barra principale
        self.mainBar = ui.Bar()
        self.mainBar.SetParent(self)
        self.mainBar.SetPosition(0, self.barY)
        self.mainBar.SetSize(self.screenWidth, self.barHeight)
        self.mainBar.SetColor(0x88FF0000)
        self.mainBar.AddFlag("not_pick")
        self.mainBar.Show()
        
        # Linee NEON
        self.neonTop = ui.Bar()
        self.neonTop.SetParent(self)
        self.neonTop.SetPosition(0, self.barY - 3)
        self.neonTop.SetSize(self.screenWidth, 6)
        self.neonTop.SetColor(0xFFFF0000)
        self.neonTop.AddFlag("not_pick")
        self.neonTop.Show()
        
        self.neonTopGlow = ui.Bar()
        self.neonTopGlow.SetParent(self)
        self.neonTopGlow.SetPosition(0, self.barY - 8)
        self.neonTopGlow.SetSize(self.screenWidth, 5)
        self.neonTopGlow.SetColor(0x66FF4444)
        self.neonTopGlow.AddFlag("not_pick")
        self.neonTopGlow.Show()
        
        self.neonBottom = ui.Bar()
        self.neonBottom.SetParent(self)
        self.neonBottom.SetPosition(0, self.barY + self.barHeight - 3)
        self.neonBottom.SetSize(self.screenWidth, 6)
        self.neonBottom.SetColor(0xFFFF0000)
        self.neonBottom.AddFlag("not_pick")
        self.neonBottom.Show()
        
        self.neonBottomGlow = ui.Bar()
        self.neonBottomGlow.SetParent(self)
        self.neonBottomGlow.SetPosition(0, self.barY + self.barHeight + 3)
        self.neonBottomGlow.SetSize(self.screenWidth, 5)
        self.neonBottomGlow.SetColor(0x66FF4444)
        self.neonBottomGlow.AddFlag("not_pick")
        self.neonBottomGlow.Show()
        
        # Testi
        self.alertText = ui.TextLine()
        self.alertText.SetParent(self)
        self.alertText.SetPosition(self.screenWidth // 2, self.barY + 25)
        self.alertText.SetHorizontalAlignCenter()
        self.alertText.SetText("! ! !  A L E R T  ! ! !")
        self.alertText.SetPackedFontColor(0xFFFFFFFF)
        self.alertText.SetOutline()
        self.alertText.Show()
        
        self.subText = ui.TextLine()
        self.subText.SetParent(self)
        self.subText.SetPosition(self.screenWidth // 2, self.barY + 55)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText("B O S S   D E T E C T E D")
        self.subText.SetPackedFontColor(0xFFFF4444)
        self.subText.SetOutline()
        self.subText.Show()
        
        self.bossName = ui.TextLine()
        self.bossName.SetParent(self)
        self.bossName.SetPosition(self.screenWidth // 2, self.barY + 80)
        self.bossName.SetHorizontalAlignCenter()
        self.bossName.SetText("")
        self.bossName.SetPackedFontColor(0xFFFFD700)
        self.bossName.SetOutline()
        self.bossName.Show()
        
        # Angoli decorativi
        self.__BuildCorners()
        
        self.endTime = 0
        self.isFlashing = False
        
        self.Hide()
    
    def __BuildCorners(self):
        """Crea angoli decorativi stile Solo Leveling"""
        goldColor = 0xFFFFD700
        
        # Top-Left
        self.cornerTL = ui.Bar()
        self.cornerTL.SetParent(self); self.cornerTL.SetPosition(50, self.barY - 3)
        self.cornerTL.SetSize(80, 6); self.cornerTL.SetColor(goldColor)
        self.cornerTL.AddFlag("not_pick"); self.cornerTL.Show()
        
        self.cornerTLv = ui.Bar()
        self.cornerTLv.SetParent(self); self.cornerTLv.SetPosition(50, self.barY - 3)
        self.cornerTLv.SetSize(6, 40); self.cornerTLv.SetColor(goldColor)
        self.cornerTLv.AddFlag("not_pick"); self.cornerTLv.Show()
        
        # Top-Right
        self.cornerTR = ui.Bar()
        self.cornerTR.SetParent(self); self.cornerTR.SetPosition(self.screenWidth - 130, self.barY - 3)
        self.cornerTR.SetSize(80, 6); self.cornerTR.SetColor(goldColor)
        self.cornerTR.AddFlag("not_pick"); self.cornerTR.Show()
        
        self.cornerTRv = ui.Bar()
        self.cornerTRv.SetParent(self); self.cornerTRv.SetPosition(self.screenWidth - 56, self.barY - 3)
        self.cornerTRv.SetSize(6, 40); self.cornerTRv.SetColor(goldColor)
        self.cornerTRv.AddFlag("not_pick"); self.cornerTRv.Show()
        
        # Bottom-Left
        self.cornerBL = ui.Bar()
        self.cornerBL.SetParent(self); self.cornerBL.SetPosition(50, self.barY + self.barHeight - 3)
        self.cornerBL.SetSize(80, 6); self.cornerBL.SetColor(goldColor)
        self.cornerBL.AddFlag("not_pick"); self.cornerBL.Show()
        
        self.cornerBLv = ui.Bar()
        self.cornerBLv.SetParent(self); self.cornerBLv.SetPosition(50, self.barY + self.barHeight - 37)
        self.cornerBLv.SetSize(6, 40); self.cornerBLv.SetColor(goldColor)
        self.cornerBLv.AddFlag("not_pick"); self.cornerBLv.Show()
        
        # Bottom-Right
        self.cornerBR = ui.Bar()
        self.cornerBR.SetParent(self); self.cornerBR.SetPosition(self.screenWidth - 130, self.barY + self.barHeight - 3)
        self.cornerBR.SetSize(80, 6); self.cornerBR.SetColor(goldColor)
        self.cornerBR.AddFlag("not_pick"); self.cornerBR.Show()
        
        self.cornerBRv = ui.Bar()
        self.cornerBRv.SetParent(self); self.cornerBRv.SetPosition(self.screenWidth - 56, self.barY + self.barHeight - 37)
        self.cornerBRv.SetSize(6, 40); self.cornerBRv.SetColor(goldColor)
        self.cornerBRv.AddFlag("not_pick"); self.cornerBRv.Show()
    
    def Destroy(self):
        """Pulizia memoria - Distrugge tutti gli oggetti UI figli"""
        self.glowOuter = None
        self.glowMiddle = None
        self.mainBar = None
        self.neonTop = None
        self.neonTopGlow = None
        self.neonBottom = None
        self.neonBottomGlow = None
        self.alertText = None
        self.subText = None
        self.bossName = None
        self.cornerTL = None
        self.cornerTLv = None
        self.cornerTR = None
        self.cornerTRv = None
        self.cornerBL = None
        self.cornerBLv = None
        self.cornerBR = None
        self.cornerBRv = None
        self.ClearDictionary()
    
    def __del__(self):
        self.Destroy()
    
    def ShowAlert(self, bossName=""):
        if bossName:
            self.bossName.SetText("[ " + bossName.replace("+", " ") + " ]")
        else:
            self.bossName.SetText("")
        
        self.endTime = app.GetTime() + 5.0
        self.isFlashing = True
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if not self.isFlashing:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.isFlashing = False
            return
        
        # Animazione flash
        cycle = (currentTime * 7) % 2
        
        if cycle < 1:
            # FASE ACCESA
            self.mainBar.SetColor(0xAAFF0000)
            self.glowOuter.SetColor(0x30FF0000)
            self.glowMiddle.SetColor(0x50FF0000)
            self.neonTop.SetColor(0xFFFF0000)
            self.neonBottom.SetColor(0xFFFF0000)
            self.alertText.SetPackedFontColor(0xFFFFFFFF)
            self.subText.SetPackedFontColor(0xFFFF0000)
        else:
            # FASE SPENTA
            self.mainBar.SetColor(0x55880000)
            self.glowOuter.SetColor(0x10880000)
            self.glowMiddle.SetColor(0x20880000)
            self.neonTop.SetColor(0xAACC0000)
            self.neonBottom.SetColor(0xAACC0000)
            self.alertText.SetPackedFontColor(0xAAFFAAAA)
            self.subText.SetPackedFontColor(0xAABB0000)
        
        # Pulsazione angoli
        goldPulse = int(abs((currentTime * 3) % 2 - 1) * 100) + 155
        goldColor = 0x00FFD700 | (goldPulse << 24)
        
        self.cornerTL.SetColor(goldColor)
        self.cornerTLv.SetColor(goldColor)
        self.cornerTR.SetColor(goldColor)
        self.cornerTRv.SetColor(goldColor)
        self.cornerBL.SetColor(goldColor)
        self.cornerBLv.SetColor(goldColor)
        self.cornerBR.SetColor(goldColor)
        self.cornerBRv.SetColor(goldColor)


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM INIT WINDOW - Caricamento sistema al login
# ═══════════════════════════════════════════════════════════════════════════════
class SystemInitWindow(ui.Window):
    """Effetto di inizializzazione sistema stile Solo Leveling"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        self.AddFlag("attach")
        
        # Sfondo semi-trasparente
        self.bgOverlay = ui.Bar()
        self.bgOverlay.SetParent(self)
        self.bgOverlay.SetPosition(0, 0)
        self.bgOverlay.SetSize(self.screenWidth, self.screenHeight)
        self.bgOverlay.SetColor(0x99000000)
        self.bgOverlay.AddFlag("not_pick")
        self.bgOverlay.SetTop()  # FIX: Mantiene sopra effetti skill e nomi mob
        self.bgOverlay.Show()
        
        # Box centrale
        boxWidth = 500
        boxHeight = 150
        boxX = (self.screenWidth - boxWidth) // 2
        boxY = (self.screenHeight - boxHeight) // 2
        
        self.boxBorder = ui.Bar()
        self.boxBorder.SetParent(self)
        self.boxBorder.SetPosition(boxX - 2, boxY - 2)
        self.boxBorder.SetSize(boxWidth + 4, boxHeight + 4)
        self.boxBorder.SetColor(0xFF0099FF)
        self.boxBorder.AddFlag("not_pick")
        self.boxBorder.Show()
        
        self.boxBg = ui.Bar()
        self.boxBg.SetParent(self)
        self.boxBg.SetPosition(boxX, boxY)
        self.boxBg.SetSize(boxWidth, boxHeight)
        self.boxBg.SetColor(0xEE111111)
        self.boxBg.AddFlag("not_pick")
        self.boxBg.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.screenWidth // 2, boxY + 20)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("[ S Y S T E M ]")
        self.titleText.SetPackedFontColor(0xFF0099FF)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        self.msgText = ui.TextLine()
        self.msgText.SetParent(self)
        self.msgText.SetPosition(self.screenWidth // 2, boxY + 50)
        self.msgText.SetHorizontalAlignCenter()
        self.msgText.SetText("I N I T I A L I Z I N G . . .")
        self.msgText.SetPackedFontColor(0xFFFFFFFF)
        self.msgText.SetOutline()
        self.msgText.Show()
        
        # Barra di caricamento
        barWidth = 400
        barHeight = 20
        barX = (self.screenWidth - barWidth) // 2
        barY = boxY + 85
        
        self.barBg = ui.Bar()
        self.barBg.SetParent(self)
        self.barBg.SetPosition(barX, barY)
        self.barBg.SetSize(barWidth, barHeight)
        self.barBg.SetColor(0xFF222222)
        self.barBg.AddFlag("not_pick")
        self.barBg.Show()
        
        self.barProgress = ui.Bar()
        self.barProgress.SetParent(self)
        self.barProgress.SetPosition(barX + 2, barY + 2)
        self.barProgress.SetSize(0, barHeight - 4)
        self.barProgress.SetColor(0xFF0099FF)
        self.barProgress.AddFlag("not_pick")
        self.barProgress.Show()
        
        self.percentText = ui.TextLine()
        self.percentText.SetParent(self)
        self.percentText.SetPosition(self.screenWidth // 2, barY + 25)
        self.percentText.SetHorizontalAlignCenter()
        self.percentText.SetText("0%")
        self.percentText.SetPackedFontColor(0xFF00FFFF)
        self.percentText.Show()
        
        self.subText = ui.TextLine()
        self.subText.SetParent(self)
        self.subText.SetPosition(self.screenWidth // 2, boxY + 120)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText("Hunter Terminal is loading...")
        self.subText.SetPackedFontColor(0xFF888888)
        self.subText.Show()
        
        self.barMaxWidth = barWidth - 4
        self.startTime = 0
        self.duration = 3.0
        self.endTime = 0
        self.onComplete = None
        self.completed = False
        
        self.Hide()
    
    def Destroy(self):
        """Pulizia memoria - Distrugge tutti gli oggetti UI figli"""
        self.bgOverlay = None
        self.boxBorder = None
        self.boxBg = None
        self.titleText = None
        self.msgText = None
        self.barBg = None
        self.barProgress = None
        self.percentText = None
        self.subText = None
        self.onComplete = None
        self.ClearDictionary()
    
    def __del__(self):
        self.Destroy()
    
    def StartLoading(self, callback=None):
        self.startTime = app.GetTime()
        self.endTime = self.startTime + self.duration + 1.5
        self.onComplete = callback
        self.completed = False
        self.msgText.SetText("I N I T I A L I Z I N G . . .")
        self.msgText.SetPackedFontColor(0xFFFFFFFF)
        self.barProgress.SetSize(0, 16)
        self.percentText.SetText("0%")
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            if self.onComplete:
                self.onComplete()
            return
        
        elapsed = currentTime - self.startTime
        progress = min(elapsed / self.duration, 1.0)
        
        newWidth = int(self.barMaxWidth * progress)
        self.barProgress.SetSize(newWidth, 16)
        
        percent = int(progress * 100)
        self.percentText.SetText("%d%%" % percent)
        
        # Lampeggio bordo
        cycle = (currentTime * 4) % 2
        if cycle < 1:
            self.boxBorder.SetColor(0xFF0099FF)
        else:
            self.boxBorder.SetColor(0xFF00CCFF)
        
        # Completato
        if progress >= 1.0 and not self.completed:
            self.completed = True
            self.msgText.SetText("S Y S T E M   R E A D Y")
            self.msgText.SetPackedFontColor(0xFF00FF00)
            self.boxBorder.SetColor(0xFF00FF00)


# ═══════════════════════════════════════════════════════════════════════════════
#  AWAKENING EFFECT - Risveglio a livelli speciali
# ═══════════════════════════════════════════════════════════════════════════════
class AwakeningEffect(ui.Window):
    """Effetto awakening epico per livelli speciali"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.startTime = 0
        self.duration = 5.0
        self.level = 5
        self.config = None
        self.glitchTimer = 0
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        # Background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Flash
        self.flash = ui.Bar()
        self.flash.SetParent(self)
        self.flash.SetPosition(0, 0)
        self.flash.SetSize(self.screenWidth, self.screenHeight)
        self.flash.SetColor(0x00FFFFFF)
        self.flash.AddFlag("not_pick")
        self.flash.Show()

        # Scan lines
        self.scanLines = []
        for i in range(5):
            line = ui.Bar()
            line.SetParent(self)
            line.SetSize(self.screenWidth, 2)
            line.SetPosition(0, 0)
            line.SetColor(0x00FFFFFF)
            line.AddFlag("not_pick")
            line.Show()
            self.scanLines.append(line)

        # Anelli energia
        self.rings = []
        for i in range(5):
            ring = ui.Bar()
            ring.SetParent(self)
            ring.SetSize(10, 10)
            ring.SetPosition(self.screenWidth // 2 - 5, self.screenHeight // 2 - 5)
            ring.SetColor(0x00FFFFFF)
            ring.AddFlag("not_pick")
            ring.Show()
            self.rings.append(ring)

        # Barre laterali
        self.leftBar = ui.Bar()
        self.leftBar.SetParent(self)
        self.leftBar.SetPosition(50, 0)
        self.leftBar.SetSize(3, 0)
        self.leftBar.SetColor(0x00FFFFFF)
        self.leftBar.AddFlag("not_pick")
        self.leftBar.Show()

        self.rightBar = ui.Bar()
        self.rightBar.SetParent(self)
        self.rightBar.SetPosition(self.screenWidth - 53, 0)
        self.rightBar.SetSize(3, 0)
        self.rightBar.SetColor(0x00FFFFFF)
        self.rightBar.AddFlag("not_pick")
        self.rightBar.Show()

        # Barre orizzontali
        self.topBar = ui.Bar()
        self.topBar.SetParent(self)
        self.topBar.SetPosition(0, 80)
        self.topBar.SetSize(0, 2)
        self.topBar.SetColor(0x00FFFFFF)
        self.topBar.AddFlag("not_pick")
        self.topBar.Show()

        self.bottomBar = ui.Bar()
        self.bottomBar.SetParent(self)
        self.bottomBar.SetPosition(0, self.screenHeight - 82)
        self.bottomBar.SetSize(0, 2)
        self.bottomBar.SetColor(0x00FFFFFF)
        self.bottomBar.AddFlag("not_pick")
        self.bottomBar.Show()

        # Testi
        self.levelText = ui.TextLine()
        self.levelText.SetParent(self)
        self.levelText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 - 100)
        self.levelText.SetHorizontalAlignCenter()
        self.levelText.SetText("")
        self.levelText.SetPackedFontColor(0x00FFFFFF)
        self.levelText.SetOutline()
        self.levelText.Show()

        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 - 50)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(0x00FFFFFF)
        self.nameText.SetOutline()
        self.nameText.Show()

        self.subtitleText = ui.TextLine()
        self.subtitleText.SetParent(self)
        self.subtitleText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 - 20)
        self.subtitleText.SetHorizontalAlignCenter()
        self.subtitleText.SetText("")
        self.subtitleText.SetPackedFontColor(0x00888888)
        self.subtitleText.SetOutline()
        self.subtitleText.Show()

        self.quoteText = ui.TextLine()
        self.quoteText.SetParent(self)
        self.quoteText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 + 30)
        self.quoteText.SetHorizontalAlignCenter()
        self.quoteText.SetText("")
        self.quoteText.SetPackedFontColor(0x00AAAAAA)
        self.quoteText.SetOutline()
        self.quoteText.Show()

        self.tipText = ui.TextLine()
        self.tipText.SetParent(self)
        self.tipText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 + 80)
        self.tipText.SetHorizontalAlignCenter()
        self.tipText.SetText("")
        self.tipText.SetPackedFontColor(0x00FFFF00)
        self.tipText.SetOutline()
        self.tipText.Show()

        # Corner text
        self.cornerTL = ui.TextLine()
        self.cornerTL.SetParent(self)
        self.cornerTL.SetPosition(60, 90)
        self.cornerTL.SetText("")
        self.cornerTL.SetPackedFontColor(0x00FFFFFF)
        self.cornerTL.Show()

        self.cornerTR = ui.TextLine()
        self.cornerTR.SetParent(self)
        self.cornerTR.SetPosition(self.screenWidth - 150, 90)
        self.cornerTR.SetText("")
        self.cornerTR.SetPackedFontColor(0x00FFFFFF)
        self.cornerTR.Show()

        self.cornerBL = ui.TextLine()
        self.cornerBL.SetParent(self)
        self.cornerBL.SetPosition(60, self.screenHeight - 110)
        self.cornerBL.SetText("")
        self.cornerBL.SetPackedFontColor(0x00FFFFFF)
        self.cornerBL.Show()

        self.cornerBR = ui.TextLine()
        self.cornerBR.SetParent(self)
        self.cornerBR.SetPosition(self.screenWidth - 180, self.screenHeight - 110)
        self.cornerBR.SetText("")
        self.cornerBR.SetPackedFontColor(0x00FFFFFF)
        self.cornerBR.Show()

    def Destroy(self):
        """Pulizia memoria - Distrugge tutti gli oggetti UI figli"""
        # FIX MEMORY LEAK: Prima nascondi e pulisci ogni elemento della lista
        if self.scanLines:
            for i in range(len(self.scanLines)):
                if self.scanLines[i]:
                    self.scanLines[i].Hide()
                    self.scanLines[i] = None
            del self.scanLines[:]
        self.scanLines = []

        if self.rings:
            for i in range(len(self.rings)):
                if self.rings[i]:
                    self.rings[i].Hide()
                    self.rings[i] = None
            del self.rings[:]
        self.rings = []

        # Pulizia altri elementi
        if self.bg:
            self.bg.Hide()
        self.bg = None
        if self.flash:
            self.flash.Hide()
        self.flash = None
        if self.leftBar:
            self.leftBar.Hide()
        self.leftBar = None
        if self.rightBar:
            self.rightBar.Hide()
        self.rightBar = None
        if self.topBar:
            self.topBar.Hide()
        self.topBar = None
        if self.bottomBar:
            self.bottomBar.Hide()
        self.bottomBar = None
        if self.levelText:
            self.levelText.Hide()
        self.levelText = None
        if self.nameText:
            self.nameText.Hide()
        self.nameText = None
        if self.subtitleText:
            self.subtitleText.Hide()
        self.subtitleText = None
        if self.quoteText:
            self.quoteText.Hide()
        self.quoteText = None
        if self.tipText:
            self.tipText.Hide()
        self.tipText = None
        if self.cornerTL:
            self.cornerTL.Hide()
        self.cornerTL = None
        if self.cornerTR:
            self.cornerTR.Hide()
        self.cornerTR = None
        if self.cornerBL:
            self.cornerBL.Hide()
        self.cornerBL = None
        if self.cornerBR:
            self.cornerBR.Hide()
        self.cornerBR = None
        self.config = None
        self.ClearDictionary()
    
    def __del__(self):
        self.Destroy()

    def Start(self, level):
        self.level = level
        self.config = GetAwakeningConfig(level)
        if not self.config:
            self.config = {
                "name": "LEVEL UP",
                "subtitle": "Continua a crescere",
                "quote": '"Il potere non ha limiti."',
                "color": 0xFFFFFFFF,
                "duration": 4.0,
                "effect": "default",
            }
        
        self.duration = self.config.get("duration", 5.0)
        self.startTime = app.GetTime()
        self.glitchTimer = 0

        self.levelText.SetText("L E V E L  " + str(level))
        self.nameText.SetText(self.config.get("name", ""))
        self.subtitleText.SetText(self.config.get("subtitle", ""))
        self.quoteText.SetText(self.config.get("quote", ""))
        self.tipText.SetText(self.config.get("tip", ""))

        self.cornerTL.SetText("[SYSTEM]")
        self.cornerTR.SetText("HUNTER NETWORK")
        self.cornerBL.SetText("STATUS: AWAKENING")
        self.cornerBR.SetText("LV." + str(level) + " CONFIRMED")

        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.IsShow():
            return

        elapsed = app.GetTime() - self.startTime
        color = self.config.get("color", 0xFFFFFFFF)
        secondaryColor = self.config.get("secondary_color", color)
        effect = self.config.get("effect", "default")

        # FASE 1: Flash iniziale (0 - 0.5s)
        if elapsed < 0.5:
            flashIntensity = 1.0 - (elapsed / 0.5)
            if effect == "monarch":
                self.flash.SetColor((int(flashIntensity * 200) << 24) | 0xFF0000)
            elif effect == "centennial":
                self.flash.SetColor((int(flashIntensity * 220) << 24) | 0xFFD700)
            else:
                self.flash.SetColor((int(flashIntensity * 150) << 24) | (color & 0xFFFFFF))
            self.bg.SetColor((int(elapsed / 0.5 * 230) << 24) | 0x000000)

        # FASE 2: Scan lines + UI build (0.3 - 1.5s)
        if elapsed >= 0.3 and elapsed < 1.5:
            self.flash.SetColor(0x00000000)
            
            for i, line in enumerate(self.scanLines):
                lineStart = 0.3 + i * 0.15
                if elapsed >= lineStart:
                    lineProgress = min(1.0, (elapsed - lineStart) / 0.5)
                    yPos = int(lineProgress * self.screenHeight)
                    line.SetPosition(0, yPos)
                    alpha = int((1.0 - lineProgress) * 100)
                    line.SetColor((alpha << 24) | (color & 0xFFFFFF))

            barProgress = min(1.0, (elapsed - 0.3) / 0.8)
            barHeight = int(barProgress * self.screenHeight)
            self.leftBar.SetSize(3, barHeight)
            self.rightBar.SetSize(3, barHeight)
            self.leftBar.SetColor((int(barProgress * 150) << 24) | (color & 0xFFFFFF))
            self.rightBar.SetColor((int(barProgress * 150) << 24) | (color & 0xFFFFFF))

            hBarProgress = min(1.0, (elapsed - 0.5) / 0.6)
            hBarWidth = int(hBarProgress * self.screenWidth)
            self.topBar.SetSize(hBarWidth, 2)
            self.bottomBar.SetSize(hBarWidth, 2)
            self.topBar.SetPosition((self.screenWidth - hBarWidth) // 2, 80)
            self.bottomBar.SetPosition((self.screenWidth - hBarWidth) // 2, self.screenHeight - 82)
            self.topBar.SetColor((int(hBarProgress * 120) << 24) | (color & 0xFFFFFF))
            self.bottomBar.SetColor((int(hBarProgress * 120) << 24) | (color & 0xFFFFFF))

        # FASE 3: Anelli energia (0.8 - 2.5s)
        if elapsed >= 0.8 and elapsed < 2.5:
            for i, ring in enumerate(self.rings):
                ringStart = 0.8 + i * 0.25
                if elapsed >= ringStart:
                    ringProgress = min(1.0, (elapsed - ringStart) / 0.8)
                    ringSize = int(50 + ringProgress * 280)
                    if effect == "monarch":
                        ringSize = int(80 + ringProgress * 400)
                    
                    ring.SetSize(ringSize, ringSize)
                    ring.SetPosition(
                        self.screenWidth // 2 - ringSize // 2,
                        self.screenHeight // 2 - ringSize // 2
                    )
                    alpha = int((1 - ringProgress) * 180)
                    ring.SetColor((alpha << 24) | (color & 0xFFFFFF))

        # FASE 4: Testi (1.0 - fine)
        if elapsed >= 1.0:
            textFadeIn = min(1.0, (elapsed - 1.0) / 0.6)
            textAlpha = int(textFadeIn * 255)

            glitchOffset = 0
            if effect in ["system_boot", "terminal_unlock", "monarch"]:
                self.glitchTimer += 1
                if self.glitchTimer % 8 < 2:
                    glitchOffset = (self.glitchTimer % 5) - 2

            self.levelText.SetPosition(self.screenWidth // 2 + glitchOffset, self.screenHeight // 2 - 100)
            self.levelText.SetPackedFontColor((textAlpha << 24) | 0xFFFFFF)

            self.nameText.SetPosition(self.screenWidth // 2 - glitchOffset, self.screenHeight // 2 - 50)
            self.nameText.SetPackedFontColor((textAlpha << 24) | (color & 0xFFFFFF))

            subtitleAlpha = int(min(1.0, max(0, (elapsed - 1.3) / 0.5)) * 200)
            self.subtitleText.SetPackedFontColor((subtitleAlpha << 24) | 0x888888)

            if elapsed >= 1.8:
                quoteAlpha = int(min(1.0, (elapsed - 1.8) / 0.5) * 255)
                if effect == "monarch":
                    self.quoteText.SetPackedFontColor((quoteAlpha << 24) | 0xFF0000)
                else:
                    self.quoteText.SetPackedFontColor((quoteAlpha << 24) | 0xCCCCCC)

            if elapsed >= 2.5 and self.config.get("tip"):
                tipAlpha = int(min(1.0, (elapsed - 2.5) / 0.5) * 255)
                pulse = abs(math.sin(elapsed * 3)) * 0.3 + 0.7
                tipAlpha = int(tipAlpha * pulse)
                self.tipText.SetPackedFontColor((tipAlpha << 24) | 0xFFFF00)

            cornerAlpha = int(textFadeIn * 100)
            self.cornerTL.SetPackedFontColor((cornerAlpha << 24) | (color & 0xFFFFFF))
            self.cornerTR.SetPackedFontColor((cornerAlpha << 24) | (color & 0xFFFFFF))
            self.cornerBL.SetPackedFontColor((cornerAlpha << 24) | (color & 0xFFFFFF))
            self.cornerBR.SetPackedFontColor((cornerAlpha << 24) | (color & 0xFFFFFF))

        # FASE 5: Fade out
        if elapsed >= self.duration - 1.5:
            fadeOut = (elapsed - (self.duration - 1.5)) / 1.5
            alpha = int((1 - fadeOut) * 255)
            bgAlpha = int((1 - fadeOut) * 230)

            self.bg.SetColor((bgAlpha << 24) | 0x000000)
            self.levelText.SetPackedFontColor((alpha << 24) | 0xFFFFFF)
            self.nameText.SetPackedFontColor((alpha << 24) | (color & 0xFFFFFF))

        # Fine animazione
        if elapsed >= self.duration:
            self.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  RANK UP EFFECT - Promozione di rango
# ═══════════════════════════════════════════════════════════════════════════════
class RankUpEffect(ui.Window):
    """Effetto promozione rank stile Solo Leveling"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(self.screenWidth, self.screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        self.startTime = 0
        self.oldRank = "E"
        self.newRank = "D"
        self.duration = 7.0
        self.glitchTimer = 0
        self.__BuildUI()
        self.Hide()

    def __BuildUI(self):
        # Background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.screenWidth, self.screenHeight)
        self.bg.SetColor(0x00000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Flash
        self.flash = ui.Bar()
        self.flash.SetParent(self)
        self.flash.SetPosition(0, 0)
        self.flash.SetSize(self.screenWidth, self.screenHeight)
        self.flash.SetColor(0x00FFFFFF)
        self.flash.AddFlag("not_pick")
        self.flash.Show()

        # Linee decorative
        self.lineTop = ui.Bar()
        self.lineTop.SetParent(self)
        self.lineTop.SetPosition(0, 100)
        self.lineTop.SetSize(0, 3)
        self.lineTop.SetColor(0x00FFFFFF)
        self.lineTop.AddFlag("not_pick")
        self.lineTop.Show()

        self.lineBottom = ui.Bar()
        self.lineBottom.SetParent(self)
        self.lineBottom.SetPosition(0, self.screenHeight - 103)
        self.lineBottom.SetSize(0, 3)
        self.lineBottom.SetColor(0x00FFFFFF)
        self.lineBottom.AddFlag("not_pick")
        self.lineBottom.Show()

        # Anelli
        self.rings = []
        for i in range(7):
            ring = ui.Bar()
            ring.SetParent(self)
            ring.SetSize(10, 10)
            ring.SetPosition(self.screenWidth // 2 - 5, self.screenHeight // 2 - 5)
            ring.SetColor(0x00FFFFFF)
            ring.AddFlag("not_pick")
            ring.Show()
            self.rings.append(ring)

        # Testi
        self.systemText = ui.TextLine()
        self.systemText.SetParent(self)
        self.systemText.SetPosition(self.screenWidth // 2, 120)
        self.systemText.SetHorizontalAlignCenter()
        self.systemText.SetText("")
        self.systemText.SetPackedFontColor(0x00FFFFFF)
        self.systemText.SetOutline()
        self.systemText.Show()

        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 - 120)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(0x00FFD700)
        self.titleText.SetOutline()
        self.titleText.Show()

        self.oldRankText = ui.TextLine()
        self.oldRankText.SetParent(self)
        self.oldRankText.SetPosition(self.screenWidth // 2 - 120, self.screenHeight // 2 - 30)
        self.oldRankText.SetHorizontalAlignCenter()
        self.oldRankText.SetText("")
        self.oldRankText.SetPackedFontColor(0x00FFFFFF)
        self.oldRankText.SetOutline()
        self.oldRankText.Show()

        self.arrowText = ui.TextLine()
        self.arrowText.SetParent(self)
        self.arrowText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 - 30)
        self.arrowText.SetHorizontalAlignCenter()
        self.arrowText.SetText("")
        self.arrowText.SetPackedFontColor(0x00FFD700)
        self.arrowText.SetOutline()
        self.arrowText.Show()

        self.newRankText = ui.TextLine()
        self.newRankText.SetParent(self)
        self.newRankText.SetPosition(self.screenWidth // 2 + 120, self.screenHeight // 2 - 30)
        self.newRankText.SetHorizontalAlignCenter()
        self.newRankText.SetText("")
        self.newRankText.SetPackedFontColor(0x00FFFFFF)
        self.newRankText.SetOutline()
        self.newRankText.Show()

        self.rankNameText = ui.TextLine()
        self.rankNameText.SetParent(self)
        self.rankNameText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 + 30)
        self.rankNameText.SetHorizontalAlignCenter()
        self.rankNameText.SetText("")
        self.rankNameText.SetPackedFontColor(0x00FFFFFF)
        self.rankNameText.SetOutline()
        self.rankNameText.Show()

        self.titleEarnedText = ui.TextLine()
        self.titleEarnedText.SetParent(self)
        self.titleEarnedText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 + 60)
        self.titleEarnedText.SetHorizontalAlignCenter()
        self.titleEarnedText.SetText("")
        self.titleEarnedText.SetPackedFontColor(0x00888888)
        self.titleEarnedText.SetOutline()
        self.titleEarnedText.Show()

        self.quoteText = ui.TextLine()
        self.quoteText.SetParent(self)
        self.quoteText.SetPosition(self.screenWidth // 2, self.screenHeight // 2 + 110)
        self.quoteText.SetHorizontalAlignCenter()
        self.quoteText.SetText("")
        self.quoteText.SetPackedFontColor(0x00AAAAAA)
        self.quoteText.SetOutline()
        self.quoteText.Show()

    def Destroy(self):
        """Pulizia memoria - Distrugge tutti gli oggetti UI figli"""
        # FIX MEMORY LEAK: Prima nascondi e pulisci ogni elemento della lista
        if self.rings:
            for i in range(len(self.rings)):
                if self.rings[i]:
                    self.rings[i].Hide()
                    self.rings[i] = None
            del self.rings[:]
        self.rings = []

        # Pulizia altri elementi
        if self.bg:
            self.bg.Hide()
        self.bg = None
        if self.flash:
            self.flash.Hide()
        self.flash = None
        if self.lineTop:
            self.lineTop.Hide()
        self.lineTop = None
        if self.lineBottom:
            self.lineBottom.Hide()
        self.lineBottom = None
        if self.systemText:
            self.systemText.Hide()
        self.systemText = None
        if self.titleText:
            self.titleText.Hide()
        self.titleText = None
        if self.oldRankText:
            self.oldRankText.Hide()
        self.oldRankText = None
        if self.arrowText:
            self.arrowText.Hide()
        self.arrowText = None
        if self.newRankText:
            self.newRankText.Hide()
        self.newRankText = None
        if self.rankNameText:
            self.rankNameText.Hide()
        self.rankNameText = None
        if self.titleEarnedText:
            self.titleEarnedText.Hide()
        self.titleEarnedText = None
        if self.quoteText:
            self.quoteText.Hide()
        self.quoteText = None
        self.ClearDictionary()
    
    def __del__(self):
        self.Destroy()

    def Start(self, oldRank, newRank):
        self.oldRank = oldRank
        self.newRank = newRank
        self.startTime = app.GetTime()
        self.glitchTimer = 0

        if newRank == "N":
            self.duration = 12.0
        elif newRank == "S":
            self.duration = 10.0
        elif newRank in ["A", "B"]:
            self.duration = 8.0
        else:
            self.duration = 7.0

        self.systemText.SetText("[SYSTEM NOTIFICATION]")
        self.titleText.SetText("R A N K   U P !")
        self.oldRankText.SetText(oldRank + "-RANK")
        self.arrowText.SetText(">>> ")
        self.newRankText.SetText(newRank + "-RANK")
        self.rankNameText.SetText(RANK_NAMES.get(newRank, "HUNTER"))
        self.titleEarnedText.SetText("Titolo: " + RANK_TITLES.get(newRank, ""))
        self.quoteText.SetText(RANK_QUOTES.get(newRank, ""))

        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.IsShow():
            return

        elapsed = app.GetTime() - self.startTime
        newColor = RANK_COLORS.get(self.newRank, 0xFFFFFFFF)
        oldColor = RANK_COLORS.get(self.oldRank, 0xFF808080)
        self.glitchTimer += 1

        isMonarch = self.newRank == "N"
        isLegendary = self.newRank in ["S", "N"]

        # FASE 1: Flash
        if elapsed < 0.8:
            flashProgress = elapsed / 0.8
            if isMonarch:
                self.flash.SetColor((int((1 - flashProgress) * 255) << 24) | 0xFF0000)
            else:
                self.flash.SetColor((int((1 - flashProgress) * 200) << 24) | 0xFFFFFF)
            self.bg.SetColor((int(flashProgress * 230) << 24) | 0x000000)
        else:
            self.flash.SetColor(0x00000000)

        # FASE 2: Linee
        if elapsed >= 0.5 and elapsed < 1.5:
            lineProgress = min(1.0, (elapsed - 0.5) / 0.5)
            lineWidth = int(lineProgress * self.screenWidth)
            self.lineTop.SetSize(lineWidth, 3)
            self.lineBottom.SetSize(lineWidth, 3)
            self.lineTop.SetPosition((self.screenWidth - lineWidth) // 2, 100)
            self.lineBottom.SetPosition((self.screenWidth - lineWidth) // 2, self.screenHeight - 103)
            self.lineTop.SetColor((int(lineProgress * 150) << 24) | (newColor & 0xFFFFFF))
            self.lineBottom.SetColor((int(lineProgress * 150) << 24) | (newColor & 0xFFFFFF))

        # FASE 3: Anelli
        if elapsed >= 1.0 and elapsed < 3.5:
            for i, ring in enumerate(self.rings):
                ringStart = 1.0 + i * 0.2
                if elapsed >= ringStart:
                    ringProgress = min(1.0, (elapsed - ringStart) / 1.0)
                    ringSize = int(60 + ringProgress * 350)
                    if isMonarch:
                        ringSize = int(100 + ringProgress * 500)
                    
                    ring.SetSize(ringSize, ringSize)
                    ring.SetPosition(
                        self.screenWidth // 2 - ringSize // 2,
                        self.screenHeight // 2 - ringSize // 2
                    )
                    alpha = int((1 - ringProgress) * 150)
                    ring.SetColor((alpha << 24) | (newColor & 0xFFFFFF))

        # FASE 4: Testi
        if elapsed >= 1.2:
            sysAlpha = int(min(1.0, (elapsed - 1.2) / 0.3) * 150)
            self.systemText.SetPackedFontColor((sysAlpha << 24) | (newColor & 0xFFFFFF))

        if elapsed >= 1.5:
            titleAlpha = int(min(1.0, (elapsed - 1.5) / 0.4) * 255)
            pulse = abs(math.sin(elapsed * 2)) * 0.2 + 0.8
            titleAlpha = int(titleAlpha * pulse)
            self.titleText.SetPackedFontColor((titleAlpha << 24) | 0xFFD700)

        if elapsed >= 2.0:
            rankAlpha = int(min(1.0, (elapsed - 2.0) / 0.5) * 255)
            self.oldRankText.SetPackedFontColor((rankAlpha << 24) | (oldColor & 0xFFFFFF))
            self.arrowText.SetPackedFontColor((rankAlpha << 24) | 0xFFD700)
            
            arrowPulse = abs(math.sin(elapsed * 4))
            self.arrowText.SetPosition(
                self.screenWidth // 2 + int(arrowPulse * 10),
                self.screenHeight // 2 - 30
            )

        if elapsed >= 2.5:
            newRankAlpha = int(min(1.0, (elapsed - 2.5) / 0.5) * 255)
            self.newRankText.SetPackedFontColor((newRankAlpha << 24) | (newColor & 0xFFFFFF))

        if elapsed >= 3.0:
            nameAlpha = int(min(1.0, (elapsed - 3.0) / 0.5) * 255)
            self.rankNameText.SetPackedFontColor((nameAlpha << 24) | (newColor & 0xFFFFFF))

        if elapsed >= 3.5:
            titleEarnedAlpha = int(min(1.0, (elapsed - 3.5) / 0.5) * 200)
            self.titleEarnedText.SetPackedFontColor((titleEarnedAlpha << 24) | 0x888888)

        if elapsed >= 4.0:
            quoteAlpha = int(min(1.0, (elapsed - 4.0) / 0.5) * 255)
            if isMonarch:
                self.quoteText.SetPackedFontColor((quoteAlpha << 24) | 0xFF0000)
            else:
                self.quoteText.SetPackedFontColor((quoteAlpha << 24) | 0xCCCCCC)

        # FASE 5: Fade out
        if elapsed >= self.duration - 2.0:
            fadeOut = (elapsed - (self.duration - 2.0)) / 2.0
            alpha = int((1 - fadeOut) * 255)
            bgAlpha = int((1 - fadeOut) * 230)
            self.bg.SetColor((bgAlpha << 24) | 0x000000)

        if elapsed >= self.duration:
            self.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════
g_bossAlertWindow = None
g_systemInitWindow = None
g_awakeningEffect = None
g_rankUpEffect = None

def GetBossAlertWindow():
    global g_bossAlertWindow
    if g_bossAlertWindow is None:
        g_bossAlertWindow = BossAlertWindow()
    return g_bossAlertWindow

def GetSystemInitWindow():
    global g_systemInitWindow
    if g_systemInitWindow is None:
        g_systemInitWindow = SystemInitWindow()
    return g_systemInitWindow

def GetAwakeningEffect():
    global g_awakeningEffect
    if g_awakeningEffect is None:
        g_awakeningEffect = AwakeningEffect()
    return g_awakeningEffect

def GetRankUpEffect():
    global g_rankUpEffect
    if g_rankUpEffect is None:
        g_rankUpEffect = RankUpEffect()
    return g_rankUpEffect


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════
def ShowBossAlert(bossName=""):
    """Mostra alert boss"""
    GetBossAlertWindow().ShowAlert(bossName)

def ShowSystemInit(callback=None):
    """Mostra schermata inizializzazione"""
    GetSystemInitWindow().StartLoading(callback)

def ShowAwakening(level):
    """Mostra effetto awakening per un livello"""
    GetAwakeningEffect().Start(level)

def ShowRankUp(oldRank, newRank):
    """Mostra effetto rank up"""
    GetRankUpEffect().Start(oldRank, newRank)

def CheckAndShowAwakening(level):
    """Controlla se il livello ha un awakening e lo mostra"""
    if IsAwakeningLevel(level):
        ShowAwakening(level)
        return True
    return False
