# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - WINDOWS MODULE
#  Finestre principali del sistema Hunter
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import net
import wndMgr
import app

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
#  EMERGENCY QUEST WINDOW - Missioni a tempo
# ═══════════════════════════════════════════════════════════════════════════════
class EmergencyQuestWindow(ui.Window, DraggableMixin):
    """Emergency Quest (Red Box) - Finestra Movibile"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(300, 100)
        screenWidth = wndMgr.GetScreenWidth()
        defaultX = (screenWidth - 300) // 2
        defaultY = 220
        
        self.InitDraggable("EmergencyQuestWindow", defaultX, defaultY)
        
        # Sfondo Rosso Scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(300, 100)
        self.bg.SetColor(0xCC330000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordi Rossi
        self.borders = []
        color = COLOR_SCHEMES["RED"]["border"]
        for y in [0, 98]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(300, 2); b.SetColor(color); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, 298]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, 100); b.SetColor(color); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        
        self.title = ui.TextLine()
        self.title.SetParent(self)
        self.title.SetPosition(150, 10)
        self.title.SetHorizontalAlignCenter()
        self.title.SetText("! EMERGENCY QUEST !")
        self.title.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
        self.title.SetOutline()
        self.title.AddFlag("not_pick")
        self.title.Show()
        
        self.questName = ui.TextLine()
        self.questName.SetParent(self)
        self.questName.SetPosition(150, 35)
        self.questName.SetHorizontalAlignCenter()
        self.questName.SetText("")
        self.questName.SetPackedFontColor(COLOR_TEXT_NORMAL)
        self.questName.AddFlag("not_pick")
        self.questName.Show()
        
        self.timer = ui.TextLine()
        self.timer.SetParent(self)
        self.timer.SetPosition(150, 60)
        self.timer.SetHorizontalAlignCenter()
        self.timer.SetPackedFontColor(COLOR_SCHEMES["GOLD"]["title"])
        self.timer.SetOutline()
        self.timer.AddFlag("not_pick")
        self.timer.Show()
        
        self.endTime = 0
        self.currentTitle = ""
        self.targetCount = 0
        
    def StartMission(self, title, seconds, mobVnum, count):
        self.currentTitle = title.replace("+", " ")
        self.targetCount = count
        self.UpdateProgress(0)
        self.endTime = app.GetTime() + seconds
        self.Show()
        self.SetTop()
        self.title.SetText("IL DESTINO SI DECIDE ORA!")
        self.title.SetPackedFontColor(COLOR_SCHEMES["GOLD"]["title"])
        
    def UpdateProgress(self, current):
        if self.targetCount > 0:
            self.questName.SetText("%s [%d/%d]" % (self.currentTitle, current, self.targetCount))
        else:
            self.questName.SetText(self.currentTitle)
        
    def EndMission(self, status, isEmergency=True):
        if isEmergency:
            if status == "SUCCESS":
                self.title.SetText("MISSION COMPLETE")
                self.title.SetPackedFontColor(COLOR_SCHEMES["GREEN"]["title"])
            elif status == "FAILED":
                self.title.SetText("MISSION FAILED")
                self.title.SetPackedFontColor(COLOR_SCHEMES["RED"]["title"])
        else:
            self.title.SetText("IL DESTINO SI DECIDE ORA!")
            self.title.SetPackedFontColor(COLOR_SCHEMES["GOLD"]["title"])
        self.endTime = app.GetTime() + 3.0

    def OnUpdate(self):
        if self.endTime > 0:
            left = self.endTime - app.GetTime()
            if left <= 0:
                self.Hide()
                self.endTime = 0
            else:
                self.timer.SetText(FormatTime(left))


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
