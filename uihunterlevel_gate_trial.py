# -*- coding: utf-8 -*-
# ============================================================
# HUNTER SYSTEM - GATE/TRIAL STATUS WINDOW
# ============================================================
# Finestra principale per visualizzare:
# - Stato Gate Dungeon (accesso, timer, info)
# - Stato Trial (progresso, obiettivi, tempo)
# - Barre di progresso animate
# - Colori per rank
# ============================================================

import ui
import wndMgr
import app
import math

# ============================================================
# COLORI
# ============================================================
RANK_COLORS = {
    "E": 0xFF808080,
    "D": 0xFF00FF00,
    "C": 0xFF00FFFF,
    "B": 0xFF0066FF,
    "A": 0xFFAA00FF,
    "S": 0xFFFF6600,
    "N": 0xFFFF0000,
}

COLOR_CODES = {
    "GREEN": 0xFF00FF00,
    "BLUE": 0xFF0099FF,
    "CYAN": 0xFF00FFFF,
    "ORANGE": 0xFFFF6600,
    "RED": 0xFFFF0000,
    "GOLD": 0xFFFFD700,
    "PURPLE": 0xFF9900FF,
    "WHITE": 0xFFFFFFFF,
    "GRAY": 0xFF808080,
    "BLACKWHITE": 0xFFFFFFFF,  # Bianco/Nero - N-Rank special
}

def GetRankColor(rank):
    return RANK_COLORS.get(rank, 0xFFFFFFFF)

def GetColorCode(code):
    return COLOR_CODES.get(code, RANK_COLORS.get(code, 0xFFFFFFFF))


# ============================================================
# ANIMATED PROGRESS BAR
# ============================================================
class AnimatedProgressBar(ui.Window):
    """Barra di progresso animata con effetto glow"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.width = 200
        self.height = 20
        self.progress = 0.0
        self.targetProgress = 0.0
        self.color = 0xFF00FF00
        self.glowPhase = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.width, self.height)
        self.bg.SetColor(0xFF1a1a1a)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Border
        self.border = ui.Bar()
        self.border.SetParent(self)
        self.border.SetPosition(0, 0)
        self.border.SetSize(self.width, 2)
        self.border.SetColor(0xFF333333)
        self.border.AddFlag("not_pick")
        self.border.Show()
        
        # Progress fill
        self.fill = ui.Bar()
        self.fill.SetParent(self)
        self.fill.SetPosition(2, 2)
        self.fill.SetSize(0, self.height - 4)
        self.fill.SetColor(self.color)
        self.fill.AddFlag("not_pick")
        self.fill.Show()
        
        # Glow overlay
        self.glow = ui.Bar()
        self.glow.SetParent(self)
        self.glow.SetPosition(2, 2)
        self.glow.SetSize(0, self.height - 4)
        self.glow.SetColor(0x00FFFFFF)
        self.glow.AddFlag("not_pick")
        self.glow.Show()
        
        # Text
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(self.width // 2, 2)
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("")
        self.text.SetPackedFontColor(0xFFFFFFFF)
        self.text.SetOutline()
        self.text.Show()
    
    def SetSize(self, w, h):
        ui.Window.SetSize(self, w, h)
        self.width = w
        self.height = h
        self.bg.SetSize(w, h)
        self.border.SetSize(w, 2)
        self.text.SetPosition(w // 2, 2)
        self.__UpdateFill()
    
    def SetProgress(self, current, maximum):
        if maximum > 0:
            self.targetProgress = min(1.0, float(current) / float(maximum))
        else:
            self.targetProgress = 0.0
        self.text.SetText(str(int(current)) + " / " + str(int(maximum)))
    
    def SetProgressNoText(self, current, maximum):
        """Imposta progresso senza mostrare il testo"""
        if maximum > 0:
            self.targetProgress = min(1.0, float(current) / float(maximum))
        else:
            self.targetProgress = 0.0
    
    def HideText(self):
        """Nasconde il testo della barra"""
        self.text.Hide()
    
    def ShowText(self):
        """Mostra il testo della barra"""
        self.text.Show()
    
    def SetColor(self, color):
        self.color = color
        self.fill.SetColor(color)
    
    def __UpdateFill(self):
        fillWidth = int((self.width - 4) * self.progress)
        self.fill.SetSize(max(0, fillWidth), self.height - 4)
        self.glow.SetSize(max(0, fillWidth), self.height - 4)
    
    def OnUpdate(self):
        # Smooth animation
        if abs(self.progress - self.targetProgress) > 0.001:
            self.progress += (self.targetProgress - self.progress) * 0.1
            self.__UpdateFill()
        
        # Glow effect
        self.glowPhase += 0.05
        glowAlpha = int((math.sin(self.glowPhase) * 0.5 + 0.5) * 50)
        self.glow.SetColor((glowAlpha << 24) | 0xFFFFFF)


# ============================================================
# SISTEMA MEMORIA POSIZIONI (Importato da uihunterlevel_whatif)
# ============================================================
try:
    from uihunterlevel_whatif import SaveWindowPosition, GetWindowPosition, HasSavedPosition
except:
    # Fallback se non disponibile
    _WINDOW_POSITIONS = {}
    def SaveWindowPosition(name, x, y):
        _WINDOW_POSITIONS[name] = (x, y)
    def GetWindowPosition(name, dx, dy):
        return _WINDOW_POSITIONS.get(name, (dx, dy))
    def HasSavedPosition(name):
        return name in _WINDOW_POSITIONS


# ============================================================
# TRIAL STATUS WINDOW - Finestra Stato Trial con memoria posizione
# ============================================================
class TrialStatusWindow(ui.Window):
    """Finestra principale per visualizzare lo stato della Trial - Movibile con memoria"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        
        self.windowWidth = 400
        self.windowHeight = 545  # Aumentato per i pulsanti Quick Access
        
        self.SetSize(self.windowWidth, self.windowHeight)
        
        # Posizione default al centro
        defaultX = (self.screenWidth - self.windowWidth) // 2
        defaultY = (self.screenHeight - self.windowHeight) // 2
        
        # Recupera posizione salvata o usa default
        savedX, savedY = GetWindowPosition("TrialStatusWindow", defaultX, defaultY)
        self.SetPosition(savedX, savedY)
        
        # Flag per drag
        self.AddFlag("movable")
        self.AddFlag("float")
        
        # Variabili per drag
        self.isDragging = False
        self.dragOffsetX = 0
        self.dragOffsetY = 0
        
        # Dati
        self.gateData = None
        self.trialData = None
        self.lastUpdateTime = 0
        
        self.__BuildUI()
        self.Hide()
    
    def OnMouseLeftButtonDown(self):
        self.isDragging = True
        mouseX, mouseY = wndMgr.GetMousePosition()
        winX, winY = self.GetGlobalPosition()
        self.dragOffsetX = mouseX - winX
        self.dragOffsetY = mouseY - winY
        return True
    
    def OnMouseLeftButtonUp(self):
        if self.isDragging:
            self.isDragging = False
            # Salva la nuova posizione
            x, y = self.GetGlobalPosition()
            SaveWindowPosition("TrialStatusWindow", x, y)
        return True
    
    def OnMouseDrag(self, x, y):
        if self.isDragging:
            mouseX, mouseY = wndMgr.GetMousePosition()
            newX = mouseX - self.dragOffsetX
            newY = mouseY - self.dragOffsetY
            
            # Limita alla schermata
            newX = max(0, min(newX, self.screenWidth - self.windowWidth))
            newY = max(0, min(newY, self.screenHeight - self.windowHeight))
            
            self.SetPosition(newX, newY)
        return True
    
    def __BuildUI(self):
        # ===== BACKGROUND =====
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.windowWidth, self.windowHeight)
        self.bg.SetColor(0xEE0a0a0a)
        self.bg.Show()
        
        # Border top
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.windowWidth, 3)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.Show()
        
        # Border bottom
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, self.windowHeight - 3)
        self.borderBot.SetSize(self.windowWidth, 3)
        self.borderBot.SetColor(0xFFFFD700)
        self.borderBot.Show()
        
        # ===== HEADER =====
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.windowWidth // 2, 15)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("HUNTER SYSTEM")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        self.subtitleText = ui.TextLine()
        self.subtitleText.SetParent(self)
        self.subtitleText.SetPosition(self.windowWidth // 2, 35)
        self.subtitleText.SetHorizontalAlignCenter()
        self.subtitleText.SetText("Gate Dungeon & Rank Trial")
        self.subtitleText.SetPackedFontColor(0xFF808080)
        self.subtitleText.SetOutline()
        self.subtitleText.Show()
        
        # Divider
        self.divider1 = ui.Bar()
        self.divider1.SetParent(self)
        self.divider1.SetPosition(20, 55)
        self.divider1.SetSize(self.windowWidth - 40, 1)
        self.divider1.SetColor(0xFF333333)
        self.divider1.Show()
        
        # ===== GATE SECTION =====
        self.gateSectionTitle = ui.TextLine()
        self.gateSectionTitle.SetParent(self)
        self.gateSectionTitle.SetPosition(20, 65)
        self.gateSectionTitle.SetText("[ GATE DUNGEON ]")
        self.gateSectionTitle.SetPackedFontColor(0xFFFF6600)
        self.gateSectionTitle.SetOutline()
        self.gateSectionTitle.Show()
        
        self.gateStatusText = ui.TextLine()
        self.gateStatusText.SetParent(self)
        self.gateStatusText.SetPosition(30, 90)
        self.gateStatusText.SetText("Stato: Nessun accesso")
        self.gateStatusText.SetPackedFontColor(0xFF808080)
        self.gateStatusText.Show()
        
        self.gateNameText = ui.TextLine()
        self.gateNameText.SetParent(self)
        self.gateNameText.SetPosition(30, 110)
        self.gateNameText.SetText("")
        self.gateNameText.SetPackedFontColor(0xFFFFFFFF)
        self.gateNameText.Show()
        
        self.gateTimerLabel = ui.TextLine()
        self.gateTimerLabel.SetParent(self)
        self.gateTimerLabel.SetPosition(30, 130)
        self.gateTimerLabel.SetText("Tempo rimasto:")
        self.gateTimerLabel.SetPackedFontColor(0xFF808080)
        self.gateTimerLabel.Show()
        
        self.gateTimerText = ui.TextLine()
        self.gateTimerText.SetParent(self)
        self.gateTimerText.SetPosition(130, 130)
        self.gateTimerText.SetText("--:--:--")
        self.gateTimerText.SetPackedFontColor(0xFFFFD700)
        self.gateTimerText.SetOutline()
        self.gateTimerText.Show()
        
        # Gate progress bar (solo barra, senza testo)
        self.gateProgressBar = AnimatedProgressBar()
        self.gateProgressBar.SetParent(self)
        self.gateProgressBar.SetPosition(30, 150)
        self.gateProgressBar.SetSize(340, 16)
        self.gateProgressBar.SetColor(0xFFFF6600)
        self.gateProgressBar.HideText()  # Nasconde il testo nella barra
        self.gateProgressBar.Show()
        
        # Divider
        self.divider2 = ui.Bar()
        self.divider2.SetParent(self)
        self.divider2.SetPosition(20, 175)
        self.divider2.SetSize(self.windowWidth - 40, 1)
        self.divider2.SetColor(0xFF333333)
        self.divider2.Show()
        
        # ===== TRIAL SECTION =====
        self.trialSectionTitle = ui.TextLine()
        self.trialSectionTitle.SetParent(self)
        self.trialSectionTitle.SetPosition(20, 185)
        self.trialSectionTitle.SetText("[ RANK TRIAL ]")
        self.trialSectionTitle.SetPackedFontColor(0xFFAA00FF)
        self.trialSectionTitle.SetOutline()
        self.trialSectionTitle.Show()
        
        self.trialStatusText = ui.TextLine()
        self.trialStatusText.SetParent(self)
        self.trialStatusText.SetPosition(30, 210)
        self.trialStatusText.SetText("Stato: Nessuna prova attiva")
        self.trialStatusText.SetPackedFontColor(0xFF808080)
        self.trialStatusText.Show()
        
        self.trialNameText = ui.TextLine()
        self.trialNameText.SetParent(self)
        self.trialNameText.SetPosition(30, 230)
        self.trialNameText.SetText("")
        self.trialNameText.SetPackedFontColor(0xFFFFFFFF)
        self.trialNameText.Show()
        
        self.trialRankText = ui.TextLine()
        self.trialRankText.SetParent(self)
        self.trialRankText.SetPosition(30, 250)
        self.trialRankText.SetText("")
        self.trialRankText.SetPackedFontColor(0xFFFFD700)
        self.trialRankText.Show()
        
        self.trialTimerText = ui.TextLine()
        self.trialTimerText.SetParent(self)
        self.trialTimerText.SetPosition(30, 270)
        self.trialTimerText.SetText("")
        self.trialTimerText.SetPackedFontColor(0xFFFF8800)
        self.trialTimerText.Show()
        
        # ===== PROGRESS BARS =====
        self.progressBars = {}
        self.progressLabels = {}
        
        progressTypes = [
            ("boss", "Boss", 0xFFFF0000),
            ("metin", "Metin", 0xFF00FFFF),
            ("fracture", "Fratture", 0xFF9900FF),
            ("chest", "Bauli", 0xFFFFD700),
            ("mission", "Missioni", 0xFF00FF00),
        ]
        
        yOffset = 295
        for pType, pName, pColor in progressTypes:
            # Label
            label = ui.TextLine()
            label.SetParent(self)
            label.SetPosition(30, yOffset)
            label.SetText(pName + ":")
            label.SetPackedFontColor(0xFFAAAAAA)
            label.Show()
            self.progressLabels[pType] = label
            
            # Progress bar
            bar = AnimatedProgressBar()
            bar.SetParent(self)
            bar.SetPosition(100, yOffset - 2)
            bar.SetSize(270, 18)
            bar.SetColor(pColor)
            bar.SetProgress(0, 0)
            bar.Show()
            self.progressBars[pType] = bar
            
            yOffset += 30
        
        # ===== QUICK ACCESS BUTTONS =====
        self.divider3 = ui.Bar()
        self.divider3.SetParent(self)
        self.divider3.SetPosition(20, yOffset + 5)
        self.divider3.SetSize(self.windowWidth - 40, 1)
        self.divider3.SetColor(0xFF333333)
        self.divider3.Show()
        
        yOffset += 15
        
        self.quickAccessTitle = ui.TextLine()
        self.quickAccessTitle.SetParent(self)
        self.quickAccessTitle.SetPosition(self.windowWidth // 2, yOffset)
        self.quickAccessTitle.SetHorizontalAlignCenter()
        self.quickAccessTitle.SetText("[ ACCESSO RAPIDO ]")
        self.quickAccessTitle.SetPackedFontColor(0xFFFFD700)
        self.quickAccessTitle.SetOutline()
        self.quickAccessTitle.Show()
        
        yOffset += 25
        
        # Pulsante Rank Up + Gate Access
        self.btnRankGate = ui.Button()
        self.btnRankGate.SetParent(self)
        self.btnRankGate.SetPosition(30, yOffset)
        self.btnRankGate.SetText("")
        self.btnRankGate.SetEvent(self.__OnClickRankGate)
        self.btnRankGate.Show()
        
        self.btnRankGateBg = ui.Bar()
        self.btnRankGateBg.SetParent(self)
        self.btnRankGateBg.SetPosition(30, yOffset)
        self.btnRankGateBg.SetSize(165, 35)
        self.btnRankGateBg.SetColor(0xFF1a1a3a)
        self.btnRankGateBg.AddFlag("not_pick")
        self.btnRankGateBg.Show()
        
        self.btnRankGateIcon = ui.TextLine()
        self.btnRankGateIcon.SetParent(self)
        self.btnRankGateIcon.SetPosition(40, yOffset + 5)
        self.btnRankGateIcon.SetText("[R]")
        self.btnRankGateIcon.SetPackedFontColor(0xFFAA00FF)
        self.btnRankGateIcon.SetOutline()
        self.btnRankGateIcon.AddFlag("not_pick")
        self.btnRankGateIcon.Show()
        
        self.btnRankGateText = ui.TextLine()
        self.btnRankGateText.SetParent(self)
        self.btnRankGateText.SetPosition(70, yOffset + 5)
        self.btnRankGateText.SetText("Rank Up")
        self.btnRankGateText.SetPackedFontColor(0xFFFFFFFF)
        self.btnRankGateText.AddFlag("not_pick")
        self.btnRankGateText.Show()
        
        self.btnRankGateText2 = ui.TextLine()
        self.btnRankGateText2.SetParent(self)
        self.btnRankGateText2.SetPosition(70, yOffset + 18)
        self.btnRankGateText2.SetText("& Gate Access")
        self.btnRankGateText2.SetPackedFontColor(0xFF808080)
        self.btnRankGateText2.AddFlag("not_pick")
        self.btnRankGateText2.Show()
        
        # Invisible button overlay for Rank/Gate
        self.btnRankGateOverlay = ui.Button()
        self.btnRankGateOverlay.SetParent(self)
        self.btnRankGateOverlay.SetPosition(30, yOffset)
        self.btnRankGateOverlay.SetSize(165, 35)
        self.btnRankGateOverlay.SetEvent(self.__OnClickRankGate)
        self.btnRankGateOverlay.Show()
        
        # Pulsante Missioni + Eventi
        self.btnMissionsEvents = ui.Button()
        self.btnMissionsEvents.SetParent(self)
        self.btnMissionsEvents.SetPosition(205, yOffset)
        self.btnMissionsEvents.SetText("")
        self.btnMissionsEvents.SetEvent(self.__OnClickMissionsEvents)
        self.btnMissionsEvents.Show()
        
        self.btnMissionsEventsBg = ui.Bar()
        self.btnMissionsEventsBg.SetParent(self)
        self.btnMissionsEventsBg.SetPosition(205, yOffset)
        self.btnMissionsEventsBg.SetSize(165, 35)
        self.btnMissionsEventsBg.SetColor(0xFF1a3a1a)
        self.btnMissionsEventsBg.AddFlag("not_pick")
        self.btnMissionsEventsBg.Show()
        
        self.btnMissionsEventsIcon = ui.TextLine()
        self.btnMissionsEventsIcon.SetParent(self)
        self.btnMissionsEventsIcon.SetPosition(215, yOffset + 5)
        self.btnMissionsEventsIcon.SetText("[M]")
        self.btnMissionsEventsIcon.SetPackedFontColor(0xFF00FF00)
        self.btnMissionsEventsIcon.SetOutline()
        self.btnMissionsEventsIcon.AddFlag("not_pick")
        self.btnMissionsEventsIcon.Show()
        
        self.btnMissionsEventsText = ui.TextLine()
        self.btnMissionsEventsText.SetParent(self)
        self.btnMissionsEventsText.SetPosition(245, yOffset + 5)
        self.btnMissionsEventsText.SetText("Missioni")
        self.btnMissionsEventsText.SetPackedFontColor(0xFFFFFFFF)
        self.btnMissionsEventsText.AddFlag("not_pick")
        self.btnMissionsEventsText.Show()
        
        self.btnMissionsEventsText2 = ui.TextLine()
        self.btnMissionsEventsText2.SetParent(self)
        self.btnMissionsEventsText2.SetPosition(245, yOffset + 18)
        self.btnMissionsEventsText2.SetText("& Eventi")
        self.btnMissionsEventsText2.SetPackedFontColor(0xFF808080)
        self.btnMissionsEventsText2.AddFlag("not_pick")
        self.btnMissionsEventsText2.Show()
        
        # Invisible button overlay for Missions/Events
        self.btnMissionsEventsOverlay = ui.Button()
        self.btnMissionsEventsOverlay.SetParent(self)
        self.btnMissionsEventsOverlay.SetPosition(205, yOffset)
        self.btnMissionsEventsOverlay.SetSize(165, 35)
        self.btnMissionsEventsOverlay.SetEvent(self.__OnClickMissionsEvents)
        self.btnMissionsEventsOverlay.Show()
        
        # ===== CLOSE BUTTON =====
        self.closeBtn = ui.Button()
        self.closeBtn.SetParent(self)
        self.closeBtn.SetPosition(self.windowWidth - 30, 10)
        self.closeBtn.SetText("X")
        self.closeBtn.SetEvent(self.Close)
        self.closeBtn.Show()
        
        # ===== FOOTER =====
        self.footerText = ui.TextLine()
        self.footerText.SetParent(self)
        self.footerText.SetPosition(self.windowWidth // 2, self.windowHeight - 25)
        self.footerText.SetHorizontalAlignCenter()
        self.footerText.SetText("Solo Leveling Hunter System")
        self.footerText.SetPackedFontColor(0xFF555555)
        self.footerText.Show()
        
        # Disabilita mouse pick su tutti i widget per permettere drag della finestra
        widgetsToDisable = [
            self.bg, self.borderTop, self.borderBot, self.divider1, self.divider2, self.divider3,
            self.titleText, self.subtitleText,
            self.gateSectionTitle, self.gateStatusText, self.gateNameText, 
            self.gateTimerLabel, self.gateTimerText, self.gateProgressBar,
            self.trialSectionTitle, self.trialStatusText, self.trialNameText, 
            self.trialRankText, self.trialTimerText,
            self.quickAccessTitle,
            self.footerText
        ]
        for widget in widgetsToDisable:
            if widget and hasattr(widget, 'AddFlag'):
                try:
                    widget.AddFlag("not_pick")
                except:
                    pass
        
        # Disabilita mouse pick sui label e bar delle progress bar
        for pType in self.progressLabels:
            if self.progressLabels[pType]:
                try:
                    self.progressLabels[pType].AddFlag("not_pick")
                except:
                    pass
        for pType in self.progressBars:
            if self.progressBars[pType]:
                try:
                    self.progressBars[pType].AddFlag("not_pick")
                except:
                    pass
    
    def Show(self):
        ui.Window.Show(self)
        self.SetTop()
    
    def Close(self):
        self.Hide()
    
    def OnPressEscapeKey(self):
        self.Close()
        return True
    
    def __OnClickRankGate(self):
        """Apre la finestra RankUp e Gate Access"""
        try:
            import net
            # Richiede al server di aprire RankUp tramite quest
            net.SendQuestInputStringPacket("/hunter_open_rankup")
        except Exception as e:
            import dbg
            dbg.TraceError("__OnClickRankGate error: " + str(e))
    
    def __OnClickMissionsEvents(self):
        """Apre entrambe le finestre Missioni ed Eventi"""
        try:
            import net
            # Richiede al server di inviare i dati missioni e aprire le finestre
            net.SendQuestInputStringPacket("/hunter_open_missions_events")
        except Exception as e:
            import dbg
            dbg.TraceError("__OnClickMissionsEvents error: " + str(e))
    
    def UpdateGateStatus(self, gateId, gateName, remainingSeconds, colorCode):
        """Aggiorna lo stato del Gate"""
        self.gateData = {
            "id": gateId,
            "name": gateName.replace("+", " "),
            "remaining": remainingSeconds,
            "color": colorCode,
            "startRemaining": remainingSeconds
        }
        
        if gateId > 0 and remainingSeconds > 0:
            self.gateStatusText.SetText("Stato: ACCESSO DISPONIBILE")
            self.gateStatusText.SetPackedFontColor(0xFF00FF00)
            self.gateNameText.SetText("Gate: " + self.gateData["name"])
            self.gateNameText.SetPackedFontColor(GetColorCode(colorCode))
            self.gateTimerText.SetText(self.__FormatTime(remainingSeconds))
            # Aggiorna barra (2 ore = 7200 secondi max)
            self.gateProgressBar.SetProgressNoText(remainingSeconds, 7200)
            self.gateProgressBar.SetColor(GetColorCode(colorCode))
        else:
            self.gateStatusText.SetText("Stato: Nessun accesso")
            self.gateStatusText.SetPackedFontColor(0xFF808080)
            self.gateNameText.SetText("")
            self.gateTimerText.SetText("--:--:--")
            self.gateProgressBar.SetProgressNoText(0, 1)
    
    def UpdateTrialStatus(self, trialId, trialName, toRank, colorCode, remaining,
                          bossKills, reqBoss, metinKills, reqMetin,
                          fractureSeals, reqFracture, chestOpens, reqChest,
                          dailyMissions, reqMissions):
        """Aggiorna lo stato della Trial"""
        
        trialName = trialName.replace("+", " ") if trialName else ""
        
        self.trialData = {
            "id": trialId,
            "name": trialName,
            "toRank": toRank,
            "color": colorCode,
            "remaining": remaining,
            "progress": {
                "boss": (bossKills, reqBoss),
                "metin": (metinKills, reqMetin),
                "fracture": (fractureSeals, reqFracture),
                "chest": (chestOpens, reqChest),
                "mission": (dailyMissions, reqMissions),
            }
        }
        
        if trialId > 0:
            self.trialStatusText.SetText("Stato: PROVA IN CORSO")
            self.trialStatusText.SetPackedFontColor(0xFF00FFFF)
            self.trialNameText.SetText("Prova: " + trialName)
            self.trialNameText.SetPackedFontColor(GetColorCode(colorCode))
            self.trialRankText.SetText("Obiettivo: " + toRank + "-RANK")
            self.trialRankText.SetPackedFontColor(GetRankColor(toRank))
            
            if remaining and remaining > 0:
                self.trialTimerText.SetText("Tempo: " + self.__FormatTime(remaining))
            else:
                self.trialTimerText.SetText("Tempo: Illimitato")
            
            # Aggiorna barre
            self.progressBars["boss"].SetProgress(bossKills, reqBoss)
            self.progressBars["metin"].SetProgress(metinKills, reqMetin)
            self.progressBars["fracture"].SetProgress(fractureSeals, reqFracture)
            self.progressBars["chest"].SetProgress(chestOpens, reqChest)
            self.progressBars["mission"].SetProgress(dailyMissions, reqMissions)
        else:
            self.trialStatusText.SetText("Stato: Nessuna prova attiva")
            self.trialStatusText.SetPackedFontColor(0xFF808080)
            self.trialNameText.SetText("")
            self.trialRankText.SetText("")
            self.trialTimerText.SetText("")
            
            for bar in self.progressBars.values():
                bar.SetProgress(0, 0)
    
    def __FormatTime(self, seconds):
        if not seconds or seconds <= 0:
            return "Scaduto"
        
        if seconds >= 86400:
            d = seconds // 86400
            h = (seconds % 86400) // 3600
            return str(d) + "g " + str(h) + "h"
        
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return "%02d:%02d:%02d" % (h, m, s)
    
    def OnUpdate(self):
        # Usa tempo reale invece di frame counter per precisione
        currentTime = app.GetTime()
        
        # Aggiorna ogni secondo reale
        if currentTime - self.lastUpdateTime >= 1.0:
            self.lastUpdateTime = currentTime
            
            if self.gateData and self.gateData.get("remaining", 0) > 0:
                self.gateData["remaining"] -= 1
                self.gateTimerText.SetText(self.__FormatTime(self.gateData["remaining"]))
                self.gateProgressBar.SetProgressNoText(self.gateData["remaining"], 7200)
            
            if self.trialData and self.trialData.get("remaining") and self.trialData["remaining"] > 0:
                self.trialData["remaining"] -= 1
                self.trialTimerText.SetText("Tempo: " + self.__FormatTime(self.trialData["remaining"]))


# ============================================================
# SYSTEM SPEAK WINDOW - Messaggi Sistema Animati
# ============================================================
class SystemSpeakWindow(ui.Window):
    """Finestra per messaggi del Sistema Hunter con animazione"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        
        self.SetSize(600, 80)
        self.SetPosition(
            (self.screenWidth - 600) // 2,
            150
        )
        self.AddFlag("not_pick")
        
        self.messageQueue = []
        self.currentMessage = None
        self.startTime = 0
        self.duration = 3.0
        
        self.__BuildUI()
        self.Hide()
    
    def __BuildUI(self):
        # Background con gradiente
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(600, 80)
        self.bg.SetColor(0xDD000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Border superiore
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(600, 3)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        # Border inferiore
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 77)
        self.borderBot.SetSize(600, 3)
        self.borderBot.SetColor(0xFFFFD700)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()
        
        # Icona Sistema
        self.iconText = ui.TextLine()
        self.iconText.SetParent(self)
        self.iconText.SetPosition(20, 25)
        self.iconText.SetText("[SISTEMA]")
        self.iconText.SetPackedFontColor(0xFFFFD700)
        self.iconText.SetOutline()
        self.iconText.Show()
        
        # Messaggio principale
        self.messageText = ui.TextLine()
        self.messageText.SetParent(self)
        self.messageText.SetPosition(300, 35)
        self.messageText.SetHorizontalAlignCenter()
        self.messageText.SetText("")
        self.messageText.SetPackedFontColor(0xFFFFFFFF)
        self.messageText.SetOutline()
        self.messageText.Show()
    
    def AddMessage(self, colorCode, message):
        """Aggiunge un messaggio alla coda"""
        message = message.replace("+", " ")
        color = GetColorCode(colorCode) if colorCode else 0xFFFFFFFF
        
        self.messageQueue.append({
            "color": color,
            "colorCode": colorCode,
            "message": message
        })
        
        if not self.IsShow():
            self.__ShowNext()
    
    def __ShowNext(self):
        if not self.messageQueue:
            self.Hide()
            return
        
        self.currentMessage = self.messageQueue.pop(0)
        self.startTime = app.GetTime()
        
        self.messageText.SetText(self.currentMessage["message"])
        self.messageText.SetPackedFontColor(self.currentMessage["color"])
        self.borderTop.SetColor(self.currentMessage["color"])
        self.borderBot.SetColor(self.currentMessage["color"])
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if not self.IsShow():
            return
        
        elapsed = app.GetTime() - self.startTime
        
        # Fade in (0-0.3s)
        if elapsed < 0.3:
            alpha = int(elapsed / 0.3 * 0xDD)
            self.bg.SetColor((alpha << 24) | 0x000000)
        
        # Fade out (2.5-3s)
        elif elapsed > 2.5:
            fadeProgress = (elapsed - 2.5) / 0.5
            alpha = int((1 - fadeProgress) * 0xDD)
            self.bg.SetColor((alpha << 24) | 0x000000)
            
            textAlpha = int((1 - fadeProgress) * 255)
            self.messageText.SetPackedFontColor((textAlpha << 24) | (self.currentMessage["color"] & 0xFFFFFF))
        
        if elapsed >= self.duration:
            self.__ShowNext()


# ============================================================
# GLOBAL INSTANCES
# ============================================================
g_trialStatusWindow = None
g_systemSpeakWindow = None

def GetTrialStatusWindow():
    global g_trialStatusWindow
    if g_trialStatusWindow is None:
        g_trialStatusWindow = TrialStatusWindow()
    return g_trialStatusWindow

def GetSystemSpeakWindow():
    global g_systemSpeakWindow
    if g_systemSpeakWindow is None:
        g_systemSpeakWindow = SystemSpeakWindow()
    return g_systemSpeakWindow

# ============================================================
# API FUNCTIONS
# ============================================================

def OpenGateTrialWindow():
    """Apre la finestra Gate/Trial"""
    wnd = GetTrialStatusWindow()
    wnd.Show()

def CloseGateTrialWindow():
    """Chiude la finestra Gate/Trial"""
    wnd = GetTrialStatusWindow()
    wnd.Close()

def UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode):
    """Aggiorna lo stato del Gate"""
    wnd = GetTrialStatusWindow()
    wnd.UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode)

def UpdateTrialStatus(trialId, trialName, toRank, colorCode, remaining,
                      bossKills, reqBoss, metinKills, reqMetin,
                      fractureSeals, reqFracture, chestOpens, reqChest,
                      dailyMissions, reqMissions):
    """Aggiorna lo stato della Trial"""
    wnd = GetTrialStatusWindow()
    wnd.UpdateTrialStatus(trialId, trialName, toRank, colorCode, remaining,
                          bossKills, reqBoss, metinKills, reqMetin,
                          fractureSeals, reqFracture, chestOpens, reqChest,
                          dailyMissions, reqMissions)

def ShowSystemMessage(colorCode, message):
    """Mostra un messaggio del Sistema"""
    wnd = GetSystemSpeakWindow()
    wnd.AddMessage(colorCode, message)
