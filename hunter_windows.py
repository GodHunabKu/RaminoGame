# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - WINDOWS MODULE
#  Finestre principali del sistema Hunter
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import net
import wndMgr
import app
import math

from hunter_core import (
    DraggableMixin,
    SaveWindowPosition, GetWindowPosition, HasSavedPosition,
    COLOR_BG_DARK, COLOR_TEXT_NORMAL, COLOR_TEXT_MUTED,
    COLOR_SCHEMES, DEFAULT_SCHEME, FRACTURE_ID_MAP,
    GetColorScheme, GetColorFromKey, DetectColorFromText,
    FormatTime
)
from hunter_components import (
    SoloLevelingWindow, SystemButton, AnimatedProgressBar
)


# ═══════════════════════════════════════════════════════════════════════════════
#  WHAT-IF CHOICE WINDOW - Scelte narrative delle fratture
# ═══════════════════════════════════════════════════════════════════════════════
class WhatIfChoiceWindow(SoloLevelingWindow, DraggableMixin):
    """Finestra di scelta What-If - Movibile con memoria posizione"""
    
    def __init__(self):
        SoloLevelingWindow.__init__(self, 400, 300)
        self.questionId = ""
        self.buttons = []
        self.textLines = []
        
        # Inizializza drag con memoria posizione
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        self.InitDraggable("WhatIfChoiceWindow", (screenW - 400) // 2, (screenH - 300) // 2)
        
        # Header "SYSTEM"
        self.headerText = ui.TextLine()
        self.headerText.SetParent(self)
        self.headerText.SetPosition(200, 10)
        self.headerText.SetHorizontalAlignCenter()
        self.headerText.SetText("SYSTEM")
        self.headerText.SetOutline()
        self.headerText.AddFlag("not_pick")
        self.headerText.Show()
        
        self.subHeaderText = ui.TextLine()
        self.subHeaderText.SetParent(self)
        self.subHeaderText.SetPosition(200, 30)
        self.subHeaderText.SetHorizontalAlignCenter()
        self.subHeaderText.SetText("Una scelta è richiesta.")
        self.subHeaderText.SetPackedFontColor(COLOR_TEXT_MUTED)
        self.subHeaderText.AddFlag("not_pick")
        self.subHeaderText.Show()

    def Create(self, qid, text, options, colorCode="PURPLE"):
        """Crea la finestra con domanda e opzioni"""
        self.questionId = qid
        
        # Pulizia input
        if colorCode:
            colorCode = colorCode.strip()
        
        # 1. Tenta di mappare l'ID al colore
        mappedColor = FRACTURE_ID_MAP.get(str(qid), None)
        if mappedColor:
            colorCode = mappedColor
            
        # 2. Auto-detect se il colore non è valido
        if not colorCode or colorCode not in COLOR_SCHEMES:
            colorCode = DetectColorFromText(text, "PURPLE")
        
        # 3. Applica schema colori
        scheme = GetColorScheme(colorCode)
        self.SetColorScheme(scheme)
        self.headerText.SetPackedFontColor(scheme.get("title", 0xFFFFFFFF))
        
        # Reset UI
        self.buttons = []
        self.textLines = []
        
        # Parsa testo
        lines = text.replace("+", " ").split("|")
        
        # Calcola layout
        baseY = 60
        lineHeight = 20
        windowWidth = 400
        
        # Crea righe testo
        for line in lines:
            t = ui.TextLine()
            t.SetParent(self)
            t.SetPosition(windowWidth // 2, baseY)
            t.SetHorizontalAlignCenter()
            t.SetText(line)
            t.SetPackedFontColor(COLOR_TEXT_NORMAL)
            t.Show()
            self.textLines.append(t)
            baseY += lineHeight
            
        baseY += 15
        
        # Crea bottoni
        for i, opt in enumerate(options):
            if not opt:
                continue
            
            def make_event(idx):
                return lambda: self.__OnClickOption(idx)
                
            btn = SystemButton(self, 20, baseY, windowWidth - 40, opt.replace("+", " "), scheme, make_event(i + 1))
            self.buttons.append(btn)
            baseY += 40
            
        # Ridimensiona finestra
        totalHeight = baseY + 10
        self.SetSize(windowWidth, totalHeight)
        self.bg.SetSize(windowWidth, totalHeight)
        
        # Aggiorna bordi
        self.borders[1].SetPosition(0, totalHeight - 2)
        self.borders[2].SetSize(2, totalHeight)
        self.borders[3].SetSize(2, totalHeight)
        self.borders[3].SetPosition(windowWidth - 2, 0)
        
        # Centra nello schermo
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        self.SetPosition((screenWidth - windowWidth) // 2, (screenHeight - totalHeight) // 3)
        
        self.Show()
        self.SetTop()
        
    def __OnClickOption(self, val):
        net.SendChatPacket("/hunter_whatif_answer %s %d" % (self.questionId, val))
        self.Close()
        
    def Close(self):
        self.Hide()
        
    def OnKeyDown(self, key):
        if key == app.DIK_ESCAPE:
            if len(self.buttons) >= 3:
                self.__OnClickOption(3)
            else:
                self.Close()
            return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM MESSAGE WINDOW - Messaggi di sistema con coda
# ═══════════════════════════════════════════════════════════════════════════════
class SystemMessageWindow(ui.Window):
    """Messaggio di sistema con colori dinamici e coda messaggi"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(500, 60)
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition((screenWidth - 500) // 2, 280)
        self.AddFlag("not_pick")
        self.AddFlag("float")

        self.currentColor = 0xFF0099FF
        self.messageQueue = []
        self.currentMessage = None
        self.messageDelay = 4.0

        # Sfondo
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(500, 60)
        self.bg.SetColor(COLOR_BG_DARK)
        self.bg.Show()

        # Bordi
        self.borders = []
        color = COLOR_SCHEMES["BLUE"]["border"]
        b1 = ui.Bar(); b1.SetParent(self); b1.SetPosition(0, 0); b1.SetSize(500, 2); b1.SetColor(color); b1.Show()
        self.borders.append(b1)
        b2 = ui.Bar(); b2.SetParent(self); b2.SetPosition(0, 58); b2.SetSize(500, 2); b2.SetColor(color); b2.Show()
        self.borders.append(b2)
        b3 = ui.Bar(); b3.SetParent(self); b3.SetPosition(0, 0); b3.SetSize(2, 60); b3.SetColor(color); b3.Show()
        self.borders.append(b3)
        b4 = ui.Bar(); b4.SetParent(self); b4.SetPosition(498, 0); b4.SetSize(2, 60); b4.SetColor(color); b4.Show()
        self.borders.append(b4)

        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(250, 20)
        self.text.SetHorizontalAlignCenter()
        self.text.SetPackedFontColor(COLOR_SCHEMES["BLUE"]["title"])
        self.text.SetOutline()
        self.text.Show()

        self.endTime = 0

    def __UpdateColors(self, color):
        self.currentColor = color
        for b in self.borders:
            b.SetColor(color)
        self.text.SetPackedFontColor(color)

    def ShowMessage(self, msg, color=None):
        """Aggiungi messaggio alla coda"""
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition((screenWidth - 500) // 2, 280)

        finalColor = self.currentColor
        if color:
            # FIX: Compatibilita' Python 2/3 - usa type() invece di isinstance con long
            if type(color) in (int,) or (hasattr(__builtins__, 'long') and type(color) == long):
                finalColor = color
            elif isinstance(color, str):
                finalColor = GetColorFromKey(color)
            else:
                try:
                    finalColor = int(color)
                except:
                    finalColor = GetColorFromKey(str(color))

        self.messageQueue.append((msg.replace("+", " "), finalColor))

        if not self.currentMessage:
            self.__ShowNextMessage()

    def __ShowNextMessage(self):
        if len(self.messageQueue) > 0:
            msg, color = self.messageQueue.pop(0)
            self.__UpdateColors(color)
            self.text.SetText(msg)
            self.currentMessage = msg
            self.endTime = app.GetTime() + self.messageDelay
            self.Show()
            self.SetTop()
        else:
            self.currentMessage = None

    def SetRankColor(self, colorKey):
        color = GetColorFromKey(colorKey)
        self.__UpdateColors(color)

    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0
            self.currentMessage = None
            self.__ShowNextMessage()

    def ClearQueue(self):
        self.messageQueue = []
        self.Hide()
        self.currentMessage = None
        self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  EMERGENCY QUEST WINDOW - Solo Leveling Style - Missioni a tempo
# ═══════════════════════════════════════════════════════════════════════════════

# Colori per difficolta' Emergency Quest
DIFFICULTY_COLORS = {
    "EASY": {"bg": 0xCC004400, "border": 0xFF00FF00, "text": 0xFF00FF00, "label": "FACILE"},
    "NORMAL": {"bg": 0xCC001144, "border": 0xFF00CCFF, "text": 0xFF00CCFF, "label": "NORMALE"},
    "HARD": {"bg": 0xCC442200, "border": 0xFFFF8800, "text": 0xFFFF8800, "label": "DIFFICILE"},
    "EXTREME": {"bg": 0xCC440000, "border": 0xFFFF0000, "text": 0xFFFF0000, "label": "ESTREMA"},
    "GOD_MODE": {"bg": 0xCC220044, "border": 0xFFFF00FF, "text": 0xFFFF00FF, "label": "DIVINO"}
}

class EmergencyQuestWindow(ui.Window, DraggableMixin):
    """Emergency Quest - Solo Leveling Style - Finestra Espansa con Descrizione"""

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(420, 220)
        screenWidth = wndMgr.GetScreenWidth()
        defaultX = (screenWidth - 420) // 2
        defaultY = 180

        self.InitDraggable("EmergencyQuestWindow", defaultX, defaultY)

        # Variabili di stato
        self.endTime = 0
        self.currentTitle = ""
        self.targetCount = 0
        self.currentProgress = 0
        self.description = ""
        self.difficulty = "NORMAL"
        self.penalty = 0
        self.pulsePhase = 0.0

        # Sfondo principale scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(420, 220)
        self.bg.SetColor(0xEE0A0A14)  # Quasi nero con sfumatura blu scuro
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Inner glow effect (bordo interno luminoso)
        self.innerGlow = ui.Bar()
        self.innerGlow.SetParent(self)
        self.innerGlow.SetPosition(3, 3)
        self.innerGlow.SetSize(414, 214)
        self.innerGlow.SetColor(0x22FFFFFF)
        self.innerGlow.AddFlag("not_pick")
        self.innerGlow.Show()

        # Inner background
        self.innerBg = ui.Bar()
        self.innerBg.SetParent(self)
        self.innerBg.SetPosition(5, 5)
        self.innerBg.SetSize(410, 210)
        self.innerBg.SetColor(0xDD080812)
        self.innerBg.AddFlag("not_pick")
        self.innerBg.Show()

        # Bordi esterni animati (4 lati)
        self.borders = []
        self.borderColor = DIFFICULTY_COLORS["NORMAL"]["border"]
        for y in [0, 218]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(420, 2); b.SetColor(self.borderColor); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, 418]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, 220); b.SetColor(self.borderColor); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)

        # ═══════════ HEADER SECTION ═══════════
        # Linea separatore header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(10, 45)
        self.headerLine.SetSize(400, 1)
        self.headerLine.SetColor(0x66FFFFFF)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # Titolo "EMERGENCY QUEST"
        self.systemLabel = ui.TextLine()
        self.systemLabel.SetParent(self)
        self.systemLabel.SetPosition(210, 8)
        self.systemLabel.SetHorizontalAlignCenter()
        self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
        self.systemLabel.SetPackedFontColor(0xFFFF4444)
        self.systemLabel.SetOutline()
        self.systemLabel.AddFlag("not_pick")
        self.systemLabel.Show()

        # Badge Difficolta'
        self.diffBadgeBg = ui.Bar()
        self.diffBadgeBg.SetParent(self)
        self.diffBadgeBg.SetPosition(10, 25)
        self.diffBadgeBg.SetSize(80, 18)
        self.diffBadgeBg.SetColor(0xCC001144)
        self.diffBadgeBg.AddFlag("not_pick")
        self.diffBadgeBg.Show()

        self.diffBadgeText = ui.TextLine()
        self.diffBadgeText.SetParent(self)
        self.diffBadgeText.SetPosition(50, 27)
        self.diffBadgeText.SetHorizontalAlignCenter()
        self.diffBadgeText.SetText("NORMALE")
        self.diffBadgeText.SetPackedFontColor(0xFF00CCFF)
        self.diffBadgeText.AddFlag("not_pick")
        self.diffBadgeText.Show()

        # Timer grande a destra
        self.timerBg = ui.Bar()
        self.timerBg.SetParent(self)
        self.timerBg.SetPosition(320, 22)
        self.timerBg.SetSize(90, 22)
        self.timerBg.SetColor(0x66000000)
        self.timerBg.AddFlag("not_pick")
        self.timerBg.Show()

        self.timer = ui.TextLine()
        self.timer.SetParent(self)
        self.timer.SetPosition(365, 25)
        self.timer.SetHorizontalAlignCenter()
        self.timer.SetText("00:00")
        self.timer.SetPackedFontColor(0xFFFFD700)
        self.timer.SetOutline()
        self.timer.AddFlag("not_pick")
        self.timer.Show()

        # ═══════════ QUEST INFO SECTION ═══════════
        # Nome Quest
        self.questName = ui.TextLine()
        self.questName.SetParent(self)
        self.questName.SetPosition(210, 52)
        self.questName.SetHorizontalAlignCenter()
        self.questName.SetText("")
        self.questName.SetPackedFontColor(0xFFFFFFFF)
        self.questName.SetOutline()
        self.questName.AddFlag("not_pick")
        self.questName.Show()

        # ═══════════ DESCRIPTION SECTION ═══════════
        self.descBg = ui.Bar()
        self.descBg.SetParent(self)
        self.descBg.SetPosition(10, 72)
        self.descBg.SetSize(400, 60)
        self.descBg.SetColor(0x44000000)
        self.descBg.AddFlag("not_pick")
        self.descBg.Show()

        # Descrizione su piu' linee
        self.descLines = []
        for i in range(3):
            line = ui.TextLine()
            line.SetParent(self)
            line.SetPosition(20, 77 + i * 18)
            line.SetText("")
            line.SetPackedFontColor(0xFFCCCCCC)
            line.AddFlag("not_pick")
            line.Show()
            self.descLines.append(line)

        # ═══════════ PROGRESS SECTION ═══════════
        # Linea separatore progress
        self.progressLine = ui.Bar()
        self.progressLine.SetParent(self)
        self.progressLine.SetPosition(10, 138)
        self.progressLine.SetSize(400, 1)
        self.progressLine.SetColor(0x66FFFFFF)
        self.progressLine.AddFlag("not_pick")
        self.progressLine.Show()

        # Progress Bar Background
        self.progressBg = ui.Bar()
        self.progressBg.SetParent(self)
        self.progressBg.SetPosition(15, 148)
        self.progressBg.SetSize(390, 20)
        self.progressBg.SetColor(0xFF1A1A2E)
        self.progressBg.AddFlag("not_pick")
        self.progressBg.Show()

        # Progress Bar Fill
        self.progressFill = ui.Bar()
        self.progressFill.SetParent(self)
        self.progressFill.SetPosition(15, 148)
        self.progressFill.SetSize(0, 20)
        self.progressFill.SetColor(0xFF00CCFF)
        self.progressFill.AddFlag("not_pick")
        self.progressFill.Show()

        # Progress Text
        self.progressText = ui.TextLine()
        self.progressText.SetParent(self)
        self.progressText.SetPosition(210, 150)
        self.progressText.SetHorizontalAlignCenter()
        self.progressText.SetText("0 / 0")
        self.progressText.SetPackedFontColor(0xFFFFFFFF)
        self.progressText.SetOutline()
        self.progressText.AddFlag("not_pick")
        self.progressText.Show()

        # ═══════════ FOOTER SECTION ═══════════
        # Penalty Warning
        self.penaltyBg = ui.Bar()
        self.penaltyBg.SetParent(self)
        self.penaltyBg.SetPosition(15, 178)
        self.penaltyBg.SetSize(190, 30)
        self.penaltyBg.SetColor(0x44330000)
        self.penaltyBg.AddFlag("not_pick")
        self.penaltyBg.Show()

        self.penaltyLabel = ui.TextLine()
        self.penaltyLabel.SetParent(self)
        self.penaltyLabel.SetPosition(20, 181)
        self.penaltyLabel.SetText("PENALITA' FALLIMENTO:")
        self.penaltyLabel.SetPackedFontColor(0xFFFF6666)
        self.penaltyLabel.AddFlag("not_pick")
        self.penaltyLabel.Show()

        self.penaltyValue = ui.TextLine()
        self.penaltyValue.SetParent(self)
        self.penaltyValue.SetPosition(20, 195)
        self.penaltyValue.SetText("-0 Gloria")
        self.penaltyValue.SetPackedFontColor(0xFFFF4444)
        self.penaltyValue.SetOutline()
        self.penaltyValue.AddFlag("not_pick")
        self.penaltyValue.Show()

        # Status Text (Motivational)
        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(315, 188)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("SORGI, CACCIATORE!")
        self.statusText.SetPackedFontColor(0xFFFFD700)
        self.statusText.SetOutline()
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()

        self.Hide()

    def SetDifficultyTheme(self, difficulty):
        """Imposta tema colori basato sulla difficolta'"""
        if difficulty not in DIFFICULTY_COLORS:
            difficulty = "NORMAL"

        colors = DIFFICULTY_COLORS[difficulty]
        self.borderColor = colors["border"]

        # Aggiorna bordi
        for b in self.borders:
            b.SetColor(colors["border"])

        # Aggiorna badge difficolta'
        self.diffBadgeBg.SetColor(colors["bg"])
        self.diffBadgeText.SetText(colors["label"])
        self.diffBadgeText.SetPackedFontColor(colors["text"])

        # Aggiorna progress bar fill color
        self.progressFill.SetColor(colors["border"])

    def WrapText(self, text, maxCharsPerLine=55):
        """Divide il testo in linee per la descrizione"""
        words = text.split()
        lines = []
        currentLine = ""

        for word in words:
            if len(currentLine) + len(word) + 1 <= maxCharsPerLine:
                if currentLine:
                    currentLine += " " + word
                else:
                    currentLine = word
            else:
                if currentLine:
                    lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        return lines[:3]  # Max 3 linee

    def StartMission(self, title, seconds, vnums, count, description="", difficulty="NORMAL", penalty=0):
        self.currentTitle = title.replace("+", " ")
        self.targetCount = count
        self.currentProgress = 0
        self.description = description.replace("+", " ") if description else "Completa la sfida prima che scada il tempo!"
        self.difficulty = difficulty
        self.penalty = penalty

        # RESET: Resetta il titolo sistema (potrebbe essere rimasto "MISSION FAILED")
        self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
        self.systemLabel.SetPackedFontColor(0xFFFF4444)

        # Imposta tema colori
        self.SetDifficultyTheme(difficulty)

        # Imposta timer
        self.endTime = app.GetTime() + seconds

        # Aggiorna testi
        self.questName.SetText(self.currentTitle)

        # Descrizione su piu' linee
        descLines = self.WrapText(self.description)
        for i, line in enumerate(self.descLines):
            if i < len(descLines):
                line.SetText(descLines[i])
            else:
                line.SetText("")

        # Penalty
        if penalty > 0:
            self.penaltyValue.SetText("-%d Gloria" % penalty)
            self.penaltyBg.Show()
            self.penaltyLabel.Show()
            self.penaltyValue.Show()
        else:
            self.penaltyBg.Hide()
            self.penaltyLabel.Hide()
            self.penaltyValue.Hide()

        # Progress
        self.UpdateProgress(0)

        # Status message basato su difficolta'
        statusMessages = {
            "EASY": "Inizia la caccia!",
            "NORMAL": "Sorgi, Cacciatore!",
            "HARD": "Dimostra il tuo valore!",
            "EXTREME": "Solo i forti sopravvivono!",
            "GOD_MODE": "Diventa il Monarca!"
        }
        self.statusText.SetText(statusMessages.get(difficulty, "Sorgi, Cacciatore!"))
        self.statusText.SetPackedFontColor(0xFFFFD700)  # Reset colore oro

        self.Show()
        self.SetTop()

    def UpdateProgress(self, current):
        self.currentProgress = current
        self.progressText.SetText("%d / %d" % (current, self.targetCount))

        if self.targetCount > 0:
            fillWidth = int((float(current) / float(self.targetCount)) * 390)
            fillWidth = min(fillWidth, 390)
            self.progressFill.SetSize(fillWidth, 20)

    def EndMission(self, status, isEmergency=True):
        if isEmergency:
            if status == "SUCCESS":
                self.systemLabel.SetText("[SYSTEM] MISSION COMPLETE")
                self.systemLabel.SetPackedFontColor(0xFF00FF00)
                self.statusText.SetText("VITTORIA!")
                self.statusText.SetPackedFontColor(0xFF00FF00)
                for b in self.borders:
                    b.SetColor(0xFF00FF00)
            elif status == "FAILED":
                self.systemLabel.SetText("[SYSTEM] MISSION FAILED")
                self.systemLabel.SetPackedFontColor(0xFFFF0000)
                self.statusText.SetText("FALLIMENTO...")
                self.statusText.SetPackedFontColor(0xFFFF0000)
                for b in self.borders:
                    b.SetColor(0xFFFF0000)
        else:
            self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
            self.systemLabel.SetPackedFontColor(0xFFFF4444)

        self.endTime = app.GetTime() + 4.0

    def OnUpdate(self):
        if self.endTime > 0:
            left = self.endTime - app.GetTime()
            if left <= 0:
                self.Hide()
                self.endTime = 0
            else:
                # Formatta timer
                mins = int(left) // 60
                secs = int(left) % 60
                self.timer.SetText("%02d:%02d" % (mins, secs))

                # Effetto pulsante sui bordi quando il tempo sta per scadere
                if left < 10:
                    self.pulsePhase += 0.15
                    alpha = int(128 + 127 * math.sin(self.pulsePhase))
                    pulseColor = (0xFF << 24) | (alpha << 16) | (0x00 << 8) | 0x00
                    for b in self.borders:
                        b.SetColor(pulseColor)

    def OnPressEscapeKey(self):
        # Blocca la chiusura con ESC - la finestra rimane sempre visibile
        return True

    def Close(self):
        # Blocca la chiusura manuale - solo EndMission puo' chiudere
        pass


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENT STATUS WINDOW - Popup evento attivo
# ═══════════════════════════════════════════════════════════════════════════════
class EventStatusWindow(ui.Window, DraggableMixin):
    """Popup Evento Attivo - Finestra Movibile"""

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(220, 60)

        screenWidth = wndMgr.GetScreenWidth()
        defaultX = screenWidth - 230
        defaultY = 140
        
        self.InitDraggable("EventStatusWindow", defaultX, defaultY)
        
        self.endTime = 0
        self.parentWindow = None
        self.eventDesc = ""
        self.eventReward = ""
        self.eventType = "default"
        self.toolTip = None
        
        # Background scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(220, 60)
        self.bg.SetColor(0xDD000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordo colorato
        self.borders = []
        eventColor = 0xFFFFD700
        
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(220, 2); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 58); b.SetSize(220, 2); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(2, 60); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(218, 0); b.SetSize(2, 60); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        
        # Glow effect
        self.glowBar = ui.Bar()
        self.glowBar.SetParent(self)
        self.glowBar.SetPosition(2, 2)
        self.glowBar.SetSize(4, 56)
        self.glowBar.SetColor(0x66FFD700)
        self.glowBar.AddFlag("not_pick")
        self.glowBar.Show()
        
        # Label
        self.labelText = ui.TextLine()
        self.labelText.SetParent(self)
        self.labelText.SetPosition(110, 8)
        self.labelText.SetHorizontalAlignCenter()
        self.labelText.SetText("EVENTO IN CORSO")
        self.labelText.SetPackedFontColor(0xFFFFD700)
        self.labelText.SetOutline()
        self.labelText.AddFlag("not_pick")
        self.labelText.Show()
        
        # Nome evento
        self.eventNameText = ui.TextLine()
        self.eventNameText.SetParent(self)
        self.eventNameText.SetPosition(110, 28)
        self.eventNameText.SetHorizontalAlignCenter()
        self.eventNameText.SetText("")
        self.eventNameText.SetPackedFontColor(0xFFFFD700)
        self.eventNameText.SetOutline()
        self.eventNameText.AddFlag("not_pick")
        self.eventNameText.Show()
        
        # Orario
        self.timeText = ui.TextLine()
        self.timeText.SetParent(self)
        self.timeText.SetPosition(110, 44)
        self.timeText.SetHorizontalAlignCenter()
        self.timeText.SetText("")
        self.timeText.SetPackedFontColor(0xFFAAAAAA)
        self.timeText.AddFlag("not_pick")
        self.timeText.Show()
        
        self.currentEvent = ""
        self.Hide()
    
    def SetEvent(self, eventName, timeInfo=""):
        if not eventName or eventName == "Nessuno" or eventName == "":
            self.currentEvent = ""
            self.Hide()
            return
        
        self.currentEvent = eventName.replace("+", " ")
        self.eventNameText.SetText(self.currentEvent[:25])
        
        if timeInfo:
            self.timeText.SetText(timeInfo)
        else:
            self.timeText.SetText("")
        
        if not HasSavedPosition("EventStatusWindow"):
            screenWidth = wndMgr.GetScreenWidth()
            self.SetPosition(screenWidth - 230, 140)

        self.Show()
        self.SetTop()
    
    def ShowEvent(self, eventName, duration=0, eventType="default", desc="", reward=""):
        if not eventName or eventName == "Nessuno" or eventName == "":
            self.currentEvent = ""
            self.Hide()
            return
        
        self.currentEvent = eventName.replace("+", " ")
        self.eventNameText.SetText(self.currentEvent[:25])
        self.eventType = eventType
        self.eventDesc = desc
        self.eventReward = reward
        
        if duration > 0:
            self.endTime = app.GetTime() + duration
            mins = duration // 60
            secs = duration % 60
            self.timeText.SetText("Tempo: %d:%02d" % (mins, secs))
        else:
            self.endTime = 0
            self.timeText.SetText("")
        
        eventColors = {
            "default": 0xFFFFD700,
            "boss_hunt": 0xFFFF0000,
            "fracture": 0xFF9900FF,
            "glory_rush": 0xFFFFD700,
            "time_trial": 0xFFFFD700,
            "custom": 0xFF00FFFF
        }
        color = eventColors.get(eventType, 0xFFFFD700)
        self.SetEventColor(color)

        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition(screenWidth - 230, 140)

        self.Show()
        self.SetTop()
    
    def SetEventColor(self, color):
        for b in self.borders:
            b.SetColor(color)
        self.glowBar.SetColor((color & 0x00FFFFFF) | 0x66000000)
        self.labelText.SetPackedFontColor(color)
    
    def OnUpdate(self):
        if not self.IsShow():
            return
        
        ct = app.GetTime()
        
        if hasattr(self, 'endTime') and self.endTime > 0:
            remaining = self.endTime - ct
            if remaining <= 0:
                self.Hide()
                self.endTime = 0
                return
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            self.timeText.SetText("Tempo: %d:%02d" % (mins, secs))
        
        # Pulse glow
        alpha = int(abs((ct * 2) % 2 - 1) * 60) + 40
        glowColor = 0x00FF88 | (alpha << 24)
        self.glowBar.SetColor(glowColor)

    def SetParentWindow(self, parent):
        self.parentWindow = parent
    
    def SetEventDetails(self, desc="", reward="", eventType="default"):
        """Imposta dettagli aggiuntivi per tooltip"""
        self.eventDesc = desc
        self.eventReward = reward
        self.eventType = eventType
    
    def OnMouseOverIn(self):
        """Mostra tooltip con dettagli evento"""
        if not self.currentEvent:
            return
        
        try:
            import uiToolTip
            if not self.toolTip:
                self.toolTip = uiToolTip.ToolTip()
                self.toolTip.ClearToolTip()
            
            self.toolTip.ClearToolTip()
            self.toolTip.SetThinBoardSize(200)
            
            # Titolo evento
            self.toolTip.AppendTextLine(self.currentEvent, 0xFFFFD700)
            self.toolTip.AppendSpace(5)
            
            # Tipo evento
            eventTypeNames = {
                "default": "Evento Standard",
                "boss_hunt": "Caccia ai Boss",
                "fracture": "Frattura",
                "glory_rush": "Gloria Rush",
                "time_trial": "Sfida a Tempo",
                "custom": "Evento Speciale"
            }
            typeName = eventTypeNames.get(self.eventType, "Evento")
            self.toolTip.AppendTextLine("Tipo: %s" % typeName, 0xFFAAAAAA)
            
            # Descrizione
            if self.eventDesc:
                self.toolTip.AppendSpace(5)
                self.toolTip.AppendTextLine(self.eventDesc[:40], 0xFFCCCCCC)
            
            # Reward
            if self.eventReward:
                self.toolTip.AppendSpace(5)
                self.toolTip.AppendTextLine("Reward: %s" % self.eventReward, 0xFF00FF00)
            
            # Tempo rimasto
            if hasattr(self, 'endTime') and self.endTime > 0:
                remaining = self.endTime - app.GetTime()
                if remaining > 0:
                    mins = int(remaining) // 60
                    secs = int(remaining) % 60
                    self.toolTip.AppendSpace(5)
                    self.toolTip.AppendTextLine("Tempo: %d:%02d" % (mins, secs), 0xFFFF8800)
            
            self.toolTip.ShowToolTip()
        except:
            pass
    
    def OnMouseOverOut(self):
        """Nasconde tooltip"""
        if self.toolTip:
            self.toolTip.HideToolTip()


# ═══════════════════════════════════════════════════════════════════════════════
#  RIVAL TRACKER WINDOW - Tracker rivale in classifica
# ═══════════════════════════════════════════════════════════════════════════════
class RivalTrackerWindow(ui.Window, DraggableMixin):
    """Tracker Rivale - Finestra Movibile"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(200, 80)
        self.screenWidth = wndMgr.GetScreenWidth()
        
        defaultX = self.screenWidth - 210
        defaultY = 80
        
        self.InitDraggable("RivalTrackerWindow", defaultX, defaultY)
        self.eventWndRef = None
        
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(200, 80)
        self.bg.SetColor(COLOR_BG_DARK)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordi Rossi
        self.borders = []
        color = COLOR_SCHEMES["RED"]["border"]
        for y in [0, 78]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(200, 2); b.SetColor(color); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, 198]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, 80); b.SetColor(color); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(100, 10)
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("RIVALE DI CLASSIFICA")
        self.text.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
        self.text.SetOutline()
        self.text.AddFlag("not_pick")
        self.text.Show()
        
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(100, 30)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(COLOR_TEXT_NORMAL)
        self.nameText.AddFlag("not_pick")
        self.nameText.Show()

        self.descText = ui.TextLine()
        self.descText.SetParent(self)
        self.descText.SetPosition(100, 50)
        self.descText.SetHorizontalAlignCenter()
        self.descText.SetText("Nuovo bersaglio attivo.")
        self.descText.SetPackedFontColor(COLOR_TEXT_MUTED)
        self.descText.AddFlag("not_pick")
        self.descText.Show()
        
        self.endTime = 0
    
    def SetEventWindowRef(self, eventWnd):
        self.eventWndRef = eventWnd
        
    def ShowRival(self, name, diff, label="Gloria", mode="VICINO"):
        if not HasSavedPosition("RivalTrackerWindow"):
            self.screenWidth = wndMgr.GetScreenWidth()
            self.SetPosition(self.screenWidth - 210, 80)
        
        self.nameText.SetText(name.replace("+", " "))
        
        if mode == "SUPERATO":
            self.text.SetText("SEI STATO SUPERATO!")
            self.text.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
            self.descText.SetText("%s ti ha superato di %s pt!" % (name.replace("+", " "), str(diff)))
            self.descText.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
        else:
            self.text.SetText("RIVALE DI CLASSIFICA")
            self.text.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
            self.descText.SetText("Distacco %s: %s pt" % (label, str(diff)))
            self.descText.SetPackedFontColor(COLOR_SCHEMES["ORANGE"]["title"])
        
        self.endTime = app.GetTime() + 30.0
        self.Show()
        self.SetTop()
        
    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  OVERTAKE WINDOW - Sorpasso in classifica
# ═══════════════════════════════════════════════════════════════════════════════
class OvertakeWindow(ui.Window):
    """Effetto quando sorpassi qualcuno in classifica"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(400, 80)
        
        self.defaultY = 80
        self.eventActiveY = 210
        self.SetPosition(self.screenWidth - 410, self.defaultY)
        
        self.AddFlag("not_pick")
        self.AddFlag("float")
        self.AddFlag("attach")
        
        self.eventWndRef = None
        
        # Sfondo
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(400, 80)
        self.bg.SetColor(0xDD111111)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordi
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(400, 3)
        self.borderTop.SetColor(0xFF00FF00)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, 77)
        self.borderBottom.SetSize(400, 3)
        self.borderBottom.SetColor(0xFF00FF00)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()
        
        # Freccia
        self.arrowText = ui.TextLine()
        self.arrowText.SetParent(self)
        self.arrowText.SetPosition(200, 10)
        self.arrowText.SetHorizontalAlignCenter()
        self.arrowText.SetText("^ ^ ^")
        self.arrowText.SetPackedFontColor(0xFF00FF00)
        self.arrowText.SetOutline()
        self.arrowText.Show()
        
        # Testo principale
        self.mainText = ui.TextLine()
        self.mainText.SetParent(self)
        self.mainText.SetPosition(200, 30)
        self.mainText.SetHorizontalAlignCenter()
        self.mainText.SetText("")
        self.mainText.SetPackedFontColor(0xFFFFFFFF)
        self.mainText.SetOutline()
        self.mainText.Show()
        
        # Posizione
        self.posText = ui.TextLine()
        self.posText.SetParent(self)
        self.posText.SetPosition(200, 55)
        self.posText.SetHorizontalAlignCenter()
        self.posText.SetText("")
        self.posText.SetPackedFontColor(0xFFFFD700)
        self.posText.Show()
        
        self.startTime = 0
        self.endTime = 0
        
        self.Hide()
    
    def SetEventWindowRef(self, eventWnd):
        self.eventWndRef = eventWnd
    
    def ShowOvertake(self, overtakenName, newPosition):
        self.mainText.SetText("Hai superato %s!" % overtakenName)
        self.posText.SetText("Nuova Posizione: #%d" % newPosition)
        
        yPos = self.defaultY
        if self.eventWndRef and self.eventWndRef.IsShow():
            yPos = self.eventActiveY
        
        self.SetPosition(self.screenWidth - 410, yPos)
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 4.5
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        elapsed = currentTime - self.startTime
        
        # Lampeggio verde
        cycle = (elapsed * 4) % 2
        if cycle < 1:
            self.borderTop.SetColor(0xFF00FF00)
            self.borderBottom.SetColor(0xFF00FF00)
            self.arrowText.SetPackedFontColor(0xFF00FF00)
        else:
            self.borderTop.SetColor(0xFF00CC00)
            self.borderBottom.SetColor(0xFF00CC00)
            self.arrowText.SetPackedFontColor(0xFF88FF88)


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════
g_whatIfWindow = None
g_systemMsgWindow = None
g_emergencyWindow = None
g_eventWindow = None
g_rivalWindow = None
g_overtakeWindow = None

def GetWhatIfWindow():
    global g_whatIfWindow
    if g_whatIfWindow is None:
        g_whatIfWindow = WhatIfChoiceWindow()
    return g_whatIfWindow

def GetSystemMessageWindow():
    global g_systemMsgWindow
    if g_systemMsgWindow is None:
        g_systemMsgWindow = SystemMessageWindow()
    return g_systemMsgWindow

def GetEmergencyWindow():
    global g_emergencyWindow
    if g_emergencyWindow is None:
        g_emergencyWindow = EmergencyQuestWindow()
    return g_emergencyWindow

def GetEventWindow():
    global g_eventWindow
    if g_eventWindow is None:
        g_eventWindow = EventStatusWindow()
    return g_eventWindow

def GetRivalWindow():
    global g_rivalWindow
    if g_rivalWindow is None:
        g_rivalWindow = RivalTrackerWindow()
    return g_rivalWindow

def GetOvertakeWindow():
    global g_overtakeWindow
    if g_overtakeWindow is None:
        g_overtakeWindow = OvertakeWindow()
    return g_overtakeWindow


# Alias per compatibilità con hunter.py
GetWhatIfChoiceWindow = GetWhatIfWindow
GetEmergencyQuestWindow = GetEmergencyWindow
GetEventStatusWindow = GetEventWindow
GetRivalTrackerWindow = GetRivalWindow


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════
def OpenWhatIfChoice(qid, text, options, colorCode="PURPLE"):
    """Apre la finestra di scelta What-If"""
    GetWhatIfWindow().Create(qid, text, options, colorCode)

def ShowSystemMessage(msgType, arg1="", arg2="", arg3=""):
    """Mostra un messaggio di sistema"""
    GetSystemMessageWindow().ShowMessage(msgType, arg1, arg2, arg3)

def ShowEmergencyQuest(questName, duration):
    """Mostra notifica quest emergenza"""
    GetEmergencyWindow().ShowQuest(questName, duration)

def ShowEventStatus(eventName, timeLeft, reward):
    """Mostra stato evento"""
    GetEventWindow().ShowEvent(eventName, timeLeft, reward)

def ShowRivalTracker(rivalName, rivalGlory, myGlory, position):
    """Mostra tracker rivale"""
    GetRivalWindow().ShowRival(rivalName, rivalGlory, myGlory, position)

def ShowOvertake(overtakenName, newPosition):
    """Mostra notifica sorpasso"""
    GetOvertakeWindow().ShowOvertake(overtakenName, newPosition)
