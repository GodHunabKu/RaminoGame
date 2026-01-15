# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - MISSIONS & EVENTS
#  Sistema missioni giornaliere ed eventi stile Solo Leveling
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import wndMgr
import app

from hunter_core import DraggableMixin, WINDOW_POSITIONS, COLOR_SCHEMES, FormatNumber

# Funzione T() - restituisce direttamente il testo (no multilingua)
def T(key, default=None):
    return default if default else key


# ═══════════════════════════════════════════════════════════════════════════════
#  DAILY MISSIONS WINDOW - Finestra principale missioni
# ═══════════════════════════════════════════════════════════════════════════════
class DailyMissionsWindow(ui.Window, DraggableMixin):
    """Finestra missioni giornaliere - Trascinabile"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(340, 340)  # Aumentato per info bonus/malus
        
        # Inizializza drag con memoria posizione
        self.InitDraggable("DailyMissionsWindow", 200, 150)
        
        self.missions = []
        self.missionSlots = []
        self.progressBars = []
        self.theme = None
        self.lastUpdateTime = 0
        self.autoCloseTimer = 0.0
        self.resetTime = "05:00"  # Orario reset missioni
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background principale
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(340, 340)
        self.bgBar.SetColor(0xEE0A0A0A)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi cyan
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(340, 2)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 338)
        self.borderBot.SetSize(340, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()
        
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, 340)
        self.borderLeft.SetColor(0xFF00CCFF)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()
        
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(338, 0)
        self.borderRight.SetSize(2, 340)
        self.borderRight.SetColor(0xFF00CCFF)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(170, 10)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("DAILY_MISSIONS_TITLE", "< MISSIONI GIORNALIERE >"))
        self.titleText.SetPackedFontColor(0xFF00FFFF)
        self.titleText.Show()
        
        # Linea separatore
        self.sepLine = ui.Bar()
        self.sepLine.SetParent(self)
        self.sepLine.SetPosition(10, 35)
        self.sepLine.SetSize(320, 1)
        self.sepLine.SetColor(0xFF00CCFF)
        self.sepLine.AddFlag("not_pick")
        self.sepLine.Show()
        
        # Crea 3 slot per le missioni
        for i in range(3):
            slot = self.__CreateMissionSlot(i)
            self.missionSlots.append(slot)
        
        # ====== SEZIONE INFO BONUS/MALUS ======
        # Separatore
        self.sepLine2 = ui.Bar()
        self.sepLine2.SetParent(self)
        self.sepLine2.SetPosition(10, 235)
        self.sepLine2.SetSize(320, 1)
        self.sepLine2.SetColor(0xFF00CCFF)
        self.sepLine2.AddFlag("not_pick")
        self.sepLine2.Show()
        
        # Titolo BONUS
        self.bonusTitle = ui.TextLine()
        self.bonusTitle.SetParent(self)
        self.bonusTitle.SetPosition(20, 245)
        self.bonusTitle.SetText(T("BONUS", "BONUS"))
        self.bonusTitle.SetPackedFontColor(0xFF00FF00)
        self.bonusTitle.Show()
        
        self.bonusDesc = ui.TextLine()
        self.bonusDesc.SetParent(self)
        self.bonusDesc.SetPosition(70, 245)
        self.bonusDesc.SetText("Completa tutte: Gloria x1.5 fino al reset!")
        self.bonusDesc.SetPackedFontColor(0xFFFFD700)
        self.bonusDesc.Show()
        
        # Titolo MALUS
        self.malusTitle = ui.TextLine()
        self.malusTitle.SetParent(self)
        self.malusTitle.SetPosition(20, 265)
        self.malusTitle.SetText(T("MALUS", "MALUS"))
        self.malusTitle.SetPackedFontColor(0xFFFF4444)
        self.malusTitle.Show()
        
        self.malusDesc = ui.TextLine()
        self.malusDesc.SetParent(self)
        self.malusDesc.SetPosition(70, 265)
        self.malusDesc.SetText(T("MALUS_DESC", "Non completare: -Gloria (vedi penalita)"))
        self.malusDesc.SetPackedFontColor(0xFFAAAAAA)
        self.malusDesc.Show()
        
        # Info Reset
        self.resetInfo = ui.TextLine()
        self.resetInfo.SetParent(self)
        self.resetInfo.SetPosition(170, 290)
        self.resetInfo.SetHorizontalAlignCenter()
        self.resetInfo.SetText(T("RESET_INFO", "Reset giornaliero alle 05:00"))
        self.resetInfo.SetPackedFontColor(0xFF888888)
        self.resetInfo.Show()
        
        # Avviso bonus attivo (nascosto di default)
        self.bonusActiveText = ui.TextLine()
        self.bonusActiveText.SetParent(self)
        self.bonusActiveText.SetPosition(170, 310)
        self.bonusActiveText.SetHorizontalAlignCenter()
        self.bonusActiveText.SetText("")
        self.bonusActiveText.SetPackedFontColor(0xFF00FF00)
        self.bonusActiveText.Show()
        
        # Pulsante chiudi (tasto X)
        self.closeBtn = ui.Button()
        self.closeBtn.SetParent(self)
        self.closeBtn.SetPosition(310, 8)
        self.closeBtn.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
        self.closeBtn.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
        self.closeBtn.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
        self.closeBtn.SetEvent(self.Close)
        self.closeBtn.Show()
        
        self.Hide()
    
    def __CreateMissionSlot(self, index):
        """Crea uno slot missione"""
        slot = {}
        
        # yBase parte da y=45 e ogni slot e' alto 65 px
        yBase = 45 + index * 65
        
        # Numero slot con sfondo
        numBg = ui.Bar()
        numBg.SetParent(self)
        numBg.SetPosition(15, yBase + 8)
        numBg.SetSize(45, 45)
        numBg.SetColor(0xFF003366)
        numBg.AddFlag("not_pick")
        numBg.Show()
        slot["numBg"] = numBg
        
        numText = ui.TextLine()
        numText.SetParent(self)
        numText.SetPosition(37, yBase + 22)
        numText.SetHorizontalAlignCenter()
        numText.SetText(str(index + 1))
        numText.SetPackedFontColor(0xFF00FFFF)
        numText.Show()
        slot["numText"] = numText
        
        # Nome missione
        nameText = ui.TextLine()
        nameText.SetParent(self)
        nameText.SetPosition(75, yBase + 8)
        nameText.SetText(T("WAITING", "In attesa..."))
        nameText.SetPackedFontColor(0xFFFFFFFF)
        nameText.Show()
        slot["nameText"] = nameText
        
        # Progresso text
        progressText = ui.TextLine()
        progressText.SetParent(self)
        progressText.SetPosition(75, yBase + 28)
        progressText.SetText("0 / 0")
        progressText.SetPackedFontColor(0xFFAAAAAA)
        progressText.Show()
        slot["progressText"] = progressText
        
        # Progress bar background
        barBg = ui.Bar()
        barBg.SetParent(self)
        barBg.SetPosition(75, yBase + 48)
        barBg.SetSize(200, 12)
        barBg.SetColor(0x44000000)
        barBg.AddFlag("not_pick")
        barBg.Show()
        slot["barBg"] = barBg
        
        # Progress bar fill
        barFill = ui.Bar()
        barFill.SetParent(self)
        barFill.SetPosition(75, yBase + 48)
        barFill.SetSize(0, 12)
        barFill.SetColor(0xFF00CCFF)
        barFill.AddFlag("not_pick")
        barFill.Show()
        slot["barFill"] = barFill
        self.progressBars.append(barFill)
        
        # Reward text
        rewardText = ui.TextLine()
        rewardText.SetParent(self)
        rewardText.SetPosition(285, yBase + 12)
        rewardText.SetText("+0")
        rewardText.SetPackedFontColor(0xFFFFD700)
        rewardText.Show()
        slot["rewardText"] = rewardText
        
        # Penalty text (malus)
        penaltyText = ui.TextLine()
        penaltyText.SetParent(self)
        penaltyText.SetPosition(285, yBase + 28)
        penaltyText.SetText("")
        penaltyText.SetPackedFontColor(0xFFFF4444)
        penaltyText.Show()
        slot["penaltyText"] = penaltyText
        
        # Status icon/text
        statusText = ui.TextLine()
        statusText.SetParent(self)
        statusText.SetPosition(285, yBase + 44)
        statusText.SetText("")
        statusText.SetPackedFontColor(0xFF00FF00)
        statusText.Show()
        slot["statusText"] = statusText
        
        return slot
    
    def SetMissions(self, missions, theme):
        """Imposta i dati delle missioni"""
        self.missions = missions
        self.theme = theme
        self.__UpdateSlots()
        self.__CheckAllComplete()  # Controlla bonus all'apertura
    
    def __UpdateSlots(self):
        """Aggiorna gli slot con i dati delle missioni"""
        for i, slot in enumerate(self.missionSlots):
            if i < len(self.missions):
                m = self.missions[i]
                slot["nameText"].SetText(m["name"][:35])
                slot["progressText"].SetText("%d / %d" % (m["current"], m["target"]))
                slot["rewardText"].SetText("+%d" % m["reward"])
                
                # Mostra penalita (malus) se presente
                penalty = m.get("penalty", 0)
                if penalty > 0:
                    slot["penaltyText"].SetText("-%d" % penalty)
                else:
                    slot["penaltyText"].SetText("")
                
                # Progress bar
                pct = float(m["current"]) / float(m["target"]) if m["target"] > 0 else 0
                pct = min(1.0, pct)
                slot["barFill"].SetSize(int(200 * pct), 12)
                
                # Status
                if m["status"] == "completed":
                    slot["statusText"].SetText("[OK]")
                    slot["statusText"].SetPackedFontColor(0xFF00FF00)
                    slot["barFill"].SetColor(0xFF00FF00)
                    slot["penaltyText"].SetText("")  # Nascondi penalty se completata
                elif m["status"] == "failed":
                    slot["statusText"].SetText("[X]")
                    slot["statusText"].SetPackedFontColor(0xFFFF0000)
                    slot["barFill"].SetColor(0xFFFF0000)
                else:
                    slot["statusText"].SetText("")
                    slot["barFill"].SetColor(self.theme["accent"] if self.theme else 0xFF00CCFF)
            else:
                slot["nameText"].SetText(T("NO_MISSION", "Nessuna missione"))
                slot["progressText"].SetText("")
                slot["rewardText"].SetText("")
                slot["penaltyText"].SetText("")
                slot["statusText"].SetText("")
                slot["barFill"].SetSize(0, 12)
    
    def UpdateProgress(self, missionId, current, target):
        """Aggiorna progresso di una missione"""
        for i, m in enumerate(self.missions):
            if m["id"] == missionId:
                m["current"] = current
                m["target"] = target
                if i < len(self.missionSlots):
                    slot = self.missionSlots[i]
                    slot["progressText"].SetText("%d / %d" % (current, target))
                    pct = float(current) / float(target) if target > 0 else 0
                    pct = min(1.0, pct)
                    slot["barFill"].SetSize(int(200 * pct), 12)
                break
    
    def SetMissionComplete(self, missionId):
        """Marca una missione come completata"""
        for i, m in enumerate(self.missions):
            if m["id"] == missionId:
                m["status"] = "completed"
                if i < len(self.missionSlots):
                    slot = self.missionSlots[i]
                    slot["statusText"].SetText("[OK]")
                    slot["statusText"].SetPackedFontColor(0xFF00FF00)
                    slot["barFill"].SetColor(0xFF00FF00)
                    slot["barFill"].SetSize(200, 12)
                break
        
        # Controlla se tutte complete
        self.__CheckAllComplete()
    
    def __CheckAllComplete(self):
        """Controlla se tutte le missioni sono complete e mostra bonus"""
        if not self.missions:
            return
        
        allComplete = all(m.get("status") == "completed" for m in self.missions)
        if allComplete:
            self.SetBonusActive(True)
        else:
            self.SetBonusActive(False)
    
    def SetBonusActive(self, active):
        """Mostra/nasconde l'avviso bonus attivo"""
        if active:
            self.bonusActiveText.SetText(T("BONUS_GLORY_ACTIVE", ">>> BONUS GLORIA x1.5 ATTIVO! <<<"))
            self.bonusActiveText.SetPackedFontColor(0xFF00FF00)
            self.bonusDesc.SetText(T("BONUS_ACTIVE_DESC", "ATTIVO! Gloria x1.5 fino alle 05:00!"))
            self.bonusDesc.SetPackedFontColor(0xFF00FF00)
        else:
            self.bonusActiveText.SetText("")
            self.bonusDesc.SetText(T("BONUS_DESC", "Completa tutte: Gloria x1.5 fino al reset!"))
            self.bonusDesc.SetPackedFontColor(0xFFFFD700)
    
    def Open(self, missions=None, theme=None):
        """Apre la finestra, opzionalmente con nuovi dati"""
        if missions is not None:
            self.SetMissions(missions, theme)
        self.lastUpdateTime = app.GetTime()
        self.SetTop()
        self.Show()
    
    def OnPressEscapeKey(self):
        self.autoCloseTimer = 0.0
        self.Hide()
        return True
    
    def Close(self):
        self.autoCloseTimer = 0.0
        self.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION PROGRESS POPUP - Popup progresso (3 secondi)
# ═══════════════════════════════════════════════════════════════════════════════
class MissionProgressPopup(ui.Window):
    """Popup che appare per 3 sec quando si fa progresso"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(250, 50)
        
        self.endTime = 0
        self.theme = None
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition(screenWidth // 2 - 125, 350)
        
        # Background
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(250, 50)
        self.bgBar.SetColor(0xDD0A0A0A)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(250, 2)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 48)
        self.borderBot.SetSize(250, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(125, 8)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("MISSION", "MISSIONE"))
        self.titleText.SetPackedFontColor(0xFF00FFFF)
        self.titleText.Show()
        
        # Progresso
        self.progressText = ui.TextLine()
        self.progressText.SetParent(self)
        self.progressText.SetPosition(125, 28)
        self.progressText.SetHorizontalAlignCenter()
        self.progressText.SetText("0 / 0")
        self.progressText.SetPackedFontColor(0xFFFFFFFF)
        self.progressText.Show()
        
        self.Hide()
    
    def ShowProgress(self, missionName, current, target, theme=None):
        """Mostra popup con progresso"""
        self.theme = theme
        
        # Nome troncato
        name = missionName[:25] + "..." if len(missionName) > 25 else missionName
        self.titleText.SetText(name)
        self.progressText.SetText("%d / %d" % (current, target))
        
        # Colori tema
        if theme:
            self.borderTop.SetColor(theme.get("accent", 0xFF00CCFF))
            self.borderBot.SetColor(theme.get("accent", 0xFF00CCFF))
            self.titleText.SetPackedFontColor(theme.get("text_title", 0xFF00FFFF))
        
        self.endTime = app.GetTime() + 3.0
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION COMPLETE WINDOW - Effetto completamento
# ═══════════════════════════════════════════════════════════════════════════════
class MissionCompleteWindow(ui.Window):
    """Finestra effetto completamento missione"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        self.SetSize(screenWidth, screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        
        self.endTime = 0
        self.startTime = 0
        self.theme = None
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        # Flash overlay
        self.flashOverlay = ui.Bar()
        self.flashOverlay.SetParent(self)
        self.flashOverlay.SetPosition(0, 0)
        self.flashOverlay.SetSize(screenWidth, screenHeight)
        self.flashOverlay.SetColor(0x0000FF00)
        self.flashOverlay.AddFlag("not_pick")
        self.flashOverlay.Show()
        
        # Box centrale
        boxWidth = 400
        boxHeight = 120
        boxX = (screenWidth - boxWidth) // 2
        boxY = (screenHeight - boxHeight) // 2 - 50
        
        self.boxBg = ui.Bar()
        self.boxBg.SetParent(self)
        self.boxBg.SetPosition(boxX, boxY)
        self.boxBg.SetSize(boxWidth, boxHeight)
        self.boxBg.SetColor(0xEE0A0A0A)
        self.boxBg.AddFlag("not_pick")
        self.boxBg.Show()
        
        # Bordi box
        self.boxBorderTop = ui.Bar()
        self.boxBorderTop.SetParent(self)
        self.boxBorderTop.SetPosition(boxX, boxY)
        self.boxBorderTop.SetSize(boxWidth, 3)
        self.boxBorderTop.SetColor(0xFF00FF00)
        self.boxBorderTop.AddFlag("not_pick")
        self.boxBorderTop.Show()
        
        self.boxBorderBot = ui.Bar()
        self.boxBorderBot.SetParent(self)
        self.boxBorderBot.SetPosition(boxX, boxY + boxHeight - 3)
        self.boxBorderBot.SetSize(boxWidth, 3)
        self.boxBorderBot.SetColor(0xFF00FF00)
        self.boxBorderBot.AddFlag("not_pick")
        self.boxBorderBot.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(screenWidth // 2, boxY + 20)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("MISSION_COMPLETED_TITLE", "< MISSIONE COMPLETATA >"))
        self.titleText.SetPackedFontColor(0xFF00FF00)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        # Nome missione
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(screenWidth // 2, boxY + 50)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(0xFFFFFFFF)
        self.nameText.SetOutline()
        self.nameText.Show()
        
        # Reward
        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(screenWidth // 2, boxY + 80)
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFD700)
        self.rewardText.SetOutline()
        self.rewardText.Show()
        
        self.Hide()
    
    def ShowComplete(self, missionName, reward, theme=None):
        """Mostra effetto completamento"""
        self.theme = theme
        self.nameText.SetText(missionName)
        self.rewardText.SetText("+%d %s" % (reward, T("GLORY", "GLORIA")))
        
        if theme:
            self.boxBorderTop.SetColor(theme.get("accent", 0xFF00FF00))
            self.boxBorderBot.SetColor(theme.get("accent", 0xFF00FF00))
            self.titleText.SetPackedFontColor(theme.get("text_title", 0xFF00FF00))
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 3.5
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        elapsed = currentTime - self.startTime
        
        # Flash iniziale (0.5 sec)
        if elapsed < 0.5:
            alpha = int((1.0 - elapsed / 0.5) * 80)
            self.flashOverlay.SetColor((alpha << 24) | 0x00FF00)
        else:
            self.flashOverlay.SetColor(0x00000000)
        
        # Lampeggio bordi
        cycle = (elapsed * 3) % 2
        if cycle < 1:
            c = 0xFF00FF00
        else:
            c = 0xFF00CC00
        self.boxBorderTop.SetColor(c)
        self.boxBorderBot.SetColor(c)


# ═══════════════════════════════════════════════════════════════════════════════
#  ALL MISSIONS COMPLETE WINDOW - Bonus x1.5
# ═══════════════════════════════════════════════════════════════════════════════
class AllMissionsCompleteWindow(ui.Window):
    """Effetto speciale quando si completano tutte e 3 le missioni"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        self.SetSize(screenWidth, screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        
        self.endTime = 0
        self.startTime = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        # Flash overlay dorato
        self.flashOverlay = ui.Bar()
        self.flashOverlay.SetParent(self)
        self.flashOverlay.SetPosition(0, 0)
        self.flashOverlay.SetSize(screenWidth, screenHeight)
        self.flashOverlay.SetColor(0x00FFD700)
        self.flashOverlay.AddFlag("not_pick")
        self.flashOverlay.Show()
        
        # Box centrale grande
        boxWidth = 450
        boxHeight = 150
        boxX = (screenWidth - boxWidth) // 2
        boxY = (screenHeight - boxHeight) // 2 - 50
        
        self.boxBg = ui.Bar()
        self.boxBg.SetParent(self)
        self.boxBg.SetPosition(boxX, boxY)
        self.boxBg.SetSize(boxWidth, boxHeight)
        self.boxBg.SetColor(0xEE0A0A0A)
        self.boxBg.AddFlag("not_pick")
        self.boxBg.Show()
        
        # Bordi oro
        self.boxBorderTop = ui.Bar()
        self.boxBorderTop.SetParent(self)
        self.boxBorderTop.SetPosition(boxX, boxY)
        self.boxBorderTop.SetSize(boxWidth, 4)
        self.boxBorderTop.SetColor(0xFFFFD700)
        self.boxBorderTop.AddFlag("not_pick")
        self.boxBorderTop.Show()
        
        self.boxBorderBot = ui.Bar()
        self.boxBorderBot.SetParent(self)
        self.boxBorderBot.SetPosition(boxX, boxY + boxHeight - 4)
        self.boxBorderBot.SetSize(boxWidth, 4)
        self.boxBorderBot.SetColor(0xFFFFD700)
        self.boxBorderBot.AddFlag("not_pick")
        self.boxBorderBot.Show()
        
        # Titolo speciale
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(screenWidth // 2, boxY + 20)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("ALL_MISSIONS_COMPLETE_TITLE", "=== TUTTE LE MISSIONI COMPLETE ==="))
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        # Bonus text
        self.bonusText = ui.TextLine()
        self.bonusText.SetParent(self)
        self.bonusText.SetPosition(screenWidth // 2, boxY + 55)
        self.bonusText.SetHorizontalAlignCenter()
        self.bonusText.SetText("BONUS COMPLETAMENTO x1.5")
        self.bonusText.SetPackedFontColor(0xFFFFAA00)
        self.bonusText.SetOutline()
        self.bonusText.Show()
        
        # Reward
        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(screenWidth // 2, boxY + 90)
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFFFFF)
        self.rewardText.SetOutline()
        self.rewardText.Show()
        
        # Sub text
        self.subText = ui.TextLine()
        self.subText.SetParent(self)
        self.subText.SetPosition(screenWidth // 2, boxY + 115)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText(T("GREAT_WORK_HUNTER", "Ottimo lavoro, Cacciatore!"))
        self.subText.SetPackedFontColor(0xFFAAAAAA)
        self.subText.Show()
        
        self.Hide()
    
    def ShowBonus(self, bonusGlory, theme=None, hasFractureBonus=False):
        """Mostra effetto bonus completamento totale"""
        self.rewardText.SetText("+%d %s" % (bonusGlory, T("GLORY_BONUS", "GLORIA BONUS")))
        
        if hasFractureBonus:
            self.bonusText.SetText(T("FRACTURE_BONUS_50", "BONUS FRATTURE +50% PER IL RESTO DEL GIORNO!"))
            self.bonusText.SetPackedFontColor(0xFF00FF00)
        else:
            self.bonusText.SetText(T("COMPLETION_BONUS", "BONUS COMPLETAMENTO x1.5"))
            self.bonusText.SetPackedFontColor(0xFFFFAA00)
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 5.0
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        elapsed = currentTime - self.startTime
        
        # Flash iniziale dorato (0.8 sec)
        if elapsed < 0.8:
            alpha = int((1.0 - elapsed / 0.8) * 100)
            self.flashOverlay.SetColor((alpha << 24) | 0xFFD700)
        else:
            self.flashOverlay.SetColor(0x00000000)
        
        # Lampeggio bordi oro
        cycle = (elapsed * 2.5) % 2
        if cycle < 1:
            self.boxBorderTop.SetColor(0xFFFFD700)
            self.boxBorderBot.SetColor(0xFFFFD700)
            self.titleText.SetPackedFontColor(0xFFFFD700)
        else:
            self.boxBorderTop.SetColor(0xFFFFAA00)
            self.boxBorderBot.SetColor(0xFFFFAA00)
            self.titleText.SetPackedFontColor(0xFFFFEE55)


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENT SLOT HOVER AREA - Tooltip dettagli evento
# ═══════════════════════════════════════════════════════════════════════════════
class EventSlotHoverArea(ui.Window):
    """Area hover per mostrare tooltip dettagli evento"""
    
    EVENT_TYPE_DESC = {
        "glory_rush": ("Gloria x2 per ogni kill!", "Sorteggio finale tra tutti i partecipanti."),
        "first_rift": ("Primo a conquistare una frattura VINCE!", "Non c'e' sorteggio - vince il piu' veloce!"),
        "first_boss": ("Primo a uccidere un boss VINCE!", "Non c'e' sorteggio - vince il piu' veloce!"),
        "boss_massacre": ("Gloria da boss +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "rift_hunt": ("Spawn fratture aumentato +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "super_metin": ("Gloria da metin +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "metin_frenzy": ("Bonus metin aumentato!", "Sorteggio finale tra tutti i partecipanti."),
        "treasure_race": ("Caccia ai tesori speciali!", "Chi trova piu' tesori vince."),
        "double_spawn": ("Spawn Elite x2!", "Sorteggio finale tra tutti i partecipanti."),
        "pvp_tournament": ("Torneo PvP!", "Partecipa e combatti!"),
        "survival": ("Sopravvivenza!", "Resisti piu' a lungo possibile."),
    }
    
    def __init__(self):
        ui.Window.__init__(self)
        self.eventData = None
        self.toolTip = None
        self.AddFlag("float")
    
    def SetEventData(self, eventData):
        """Imposta i dati dell'evento per il tooltip"""
        self.eventData = eventData
    
    def OnMouseOverIn(self):
        """Mostra tooltip con dettagli evento"""
        if not self.eventData:
            return
        
        try:
            import uiToolTip
            if not self.toolTip:
                self.toolTip = uiToolTip.ToolTip()
            
            self.toolTip.ClearToolTip()
            
            # Titolo con nome evento
            ename = self.eventData.get("name", "Evento")
            etype = self.eventData.get("type", "glory_rush")
            self.toolTip.SetTitle(ename)
            self.toolTip.AppendSpace(5)
            
            # Tipo evento
            typeColors = {
                "glory_rush": 0xFFFFD700,
                "first_rift": 0xFF9932CC,
                "first_boss": 0xFFFF4444,
                "boss_massacre": 0xFFFF6600,
                "rift_hunt": 0xFF9932CC,
                "super_metin": 0xFFFF8800,
                "metin_frenzy": 0xFFFF8800,
                "double_spawn": 0xFFFF4444,
            }
            typeColor = typeColors.get(etype, 0xFFFFFFFF)
            self.toolTip.AppendTextLine("Tipo: %s" % etype.replace("_", " ").upper(), typeColor)
            self.toolTip.AppendSpace(5)
            
            # Descrizione evento
            desc1, desc2 = self.EVENT_TYPE_DESC.get(etype, ("Evento speciale!", "Partecipa per vincere!"))
            self.toolTip.AppendTextLine(desc1, 0xFF00FF00)
            self.toolTip.AppendTextLine(desc2, 0xFFAAAAAA)
            self.toolTip.AppendSpace(5)
            
            # Orari
            self.toolTip.AppendTextLine("--------------------------------", 0xFF444444)
            startTime = self.eventData.get("start_time", "--:--")
            endTime = self.eventData.get("end_time", "--:--")
            self.toolTip.AppendTextLine("Orario: %s - %s" % (startTime, endTime), 0xFFFFAA00)
            
            # Requisiti
            minRank = self.eventData.get("min_rank", "E")
            self.toolTip.AppendTextLine("Rank minimo: %s" % minRank, 0xFFCCCCCC)
            self.toolTip.AppendSpace(5)
            
            # Premi
            self.toolTip.AppendTextLine("--------------------------------", 0xFF444444)
            self.toolTip.AppendTextLine("[PREMI]", 0xFFFFD700)
            reward = self.eventData.get("reward", "+50 Gloria")
            self.toolTip.AppendTextLine("Partecipazione: %s" % reward, 0xFF88FF88)
            winnerPrize = self.eventData.get("winner_prize", 200)
            self.toolTip.AppendTextLine("Vincitore: +%d Gloria!" % winnerPrize, 0xFF00FF00)
            self.toolTip.AppendSpace(5)
            
            # Status
            status = self.eventData.get("status", "pending")
            if status == "joined":
                self.toolTip.AppendTextLine("[SEI ISCRITTO!]", 0xFF00FF00)
            elif status == "active":
                self.toolTip.AppendTextLine("[EVENTO IN CORSO]", 0xFFFFAA00)
                self.toolTip.AppendTextLine("Gioca per iscriverti!", 0xFFCCCCCC)
            elif status == "ended":
                self.toolTip.AppendTextLine("[TERMINATO]", 0xFF888888)
            else:
                self.toolTip.AppendTextLine("[NON ANCORA INIZIATO]", 0xFFAAAAAA)
            
            self.toolTip.AppendSpace(3)
            self.toolTip.Show()
        except:
            pass
    
    def OnMouseOverOut(self):
        """Nasconde tooltip"""
        if self.toolTip:
            self.toolTip.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENTS SCHEDULE WINDOW - Finestra eventi programmati
# ═══════════════════════════════════════════════════════════════════════════════
class EventsScheduleWindow(ui.Window, DraggableMixin):
    """Finestra per visualizzare gli eventi del giorno - Movibile"""
    
    SLOT_HEIGHT = 58
    VISIBLE_SLOTS = 6
    MAX_SLOTS = 50
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(420, 480)
        
        # Inizializza drag con memoria posizione
        self.InitDraggable("EventsScheduleWindow", 100, 80)
        
        self.events = []
        self.eventSlots = []
        self.theme = None
        self.scrollPos = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background principale
        self.bgMain = ui.Bar()
        self.bgMain.SetParent(self)
        self.bgMain.SetPosition(0, 0)
        self.bgMain.SetSize(420, 480)
        self.bgMain.SetColor(0xEE0A0A0A)
        self.bgMain.AddFlag("not_pick")
        self.bgMain.Show()
        
        # Bordi arancioni
        self.borders = []
        for i, (x, y, w, h) in enumerate([
            (0, 0, 420, 2),   # top
            (0, 478, 420, 2), # bottom
            (0, 0, 2, 480),   # left
            (418, 0, 2, 480)  # right
        ]):
            b = ui.Bar()
            b.SetParent(self)
            b.SetPosition(x, y)
            b.SetSize(w, h)
            b.SetColor(0xFFFF6600)
            b.AddFlag("not_pick")
            b.Show()
            self.borders.append(b)
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(200, 12)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("TODAY_EVENTS_TITLE", "< EVENTI DI OGGI >"))
        self.titleText.SetPackedFontColor(0xFFFFAA00)
        self.titleText.Show()
        
        # Linea separatore titolo
        self.sepLine = ui.Bar()
        self.sepLine.SetParent(self)
        self.sepLine.SetPosition(10, 38)
        self.sepLine.SetSize(398, 1)
        self.sepLine.SetColor(0xFFFF6600)
        self.sepLine.AddFlag("not_pick")
        self.sepLine.Show()
        
        # Messaggio se non ci sono eventi
        self.noEventsText = ui.TextLine()
        self.noEventsText.SetParent(self)
        self.noEventsText.SetPosition(200, 180)
        self.noEventsText.SetHorizontalAlignCenter()
        self.noEventsText.SetText(T("NO_EVENTS_TODAY", "Nessun evento programmato oggi"))
        self.noEventsText.SetPackedFontColor(0xFF888888)
        self.noEventsText.Hide()
        
        # Area scrollabile
        listAreaHeight = self.VISIBLE_SLOTS * self.SLOT_HEIGHT
        
        # Background area lista
        self.listBg = ui.Bar()
        self.listBg.SetParent(self)
        self.listBg.SetPosition(8, 45)
        self.listBg.SetSize(385, listAreaHeight)
        self.listBg.SetColor(0x22000000)
        self.listBg.AddFlag("not_pick")
        self.listBg.Show()
        
        # ScrollBar
        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetPosition(395, 45)
        self.scrollBar.SetScrollBarSize(listAreaHeight)
        self.scrollBar.SetScrollEvent(self.__OnScroll)
        self.scrollBar.Hide()
        
        # Crea solo gli slot visibili
        for i in range(self.VISIBLE_SLOTS):
            slot = self.__CreateEventSlot(i)
            self.eventSlots.append(slot)
        
        # Sezione INFO
        infoY = 400
        
        self.sepInfo = ui.Bar()
        self.sepInfo.SetParent(self)
        self.sepInfo.SetPosition(10, infoY)
        self.sepInfo.SetSize(398, 1)
        self.sepInfo.SetColor(0xFFFF6600)
        self.sepInfo.AddFlag("not_pick")
        self.sepInfo.Show()
        
        self.infoBox = ui.Bar()
        self.infoBox.SetParent(self)
        self.infoBox.SetPosition(10, infoY + 8)
        self.infoBox.SetSize(398, 62)
        self.infoBox.SetColor(0x33FF6600)
        self.infoBox.AddFlag("not_pick")
        self.infoBox.Show()
        
        self.infoTitle = ui.TextLine()
        self.infoTitle.SetParent(self)
        self.infoTitle.SetPosition(210, infoY + 12)
        self.infoTitle.SetHorizontalAlignCenter()
        self.infoTitle.SetText(T("AUTO_REGISTRATION", "ISCRIZIONE AUTOMATICA"))
        self.infoTitle.SetPackedFontColor(0xFFFFAA00)
        self.infoTitle.Show()
        
        self.infoLine1 = ui.TextLine()
        self.infoLine1.SetParent(self)
        self.infoLine1.SetPosition(210, infoY + 28)
        self.infoLine1.SetHorizontalAlignCenter()
        self.infoLine1.SetText(T("AUTO_REG_INFO1", "Conquista fratture, uccidi boss o metinpietra"))
        self.infoLine1.SetPackedFontColor(0xFFCCCCCC)
        self.infoLine1.Show()
        
        self.infoLine2 = ui.TextLine()
        self.infoLine2.SetParent(self)
        self.infoLine2.SetPosition(210, infoY + 44)
        self.infoLine2.SetHorizontalAlignCenter()
        self.infoLine2.SetText(T("AUTO_REG_INFO2", "per iscriverti automaticamente e partecipare!"))
        self.infoLine2.SetPackedFontColor(0xFF88FF88)
        self.infoLine2.Show()
        
        # Pulsante chiudi
        self.closeBtn = ui.Button()
        self.closeBtn.SetParent(self)
        self.closeBtn.SetPosition(380, 8)
        self.closeBtn.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
        self.closeBtn.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
        self.closeBtn.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
        self.closeBtn.SetEvent(self.Hide)
        self.closeBtn.Show()
        
        self.Hide()
    
    def __CreateEventSlot(self, index):
        """Crea uno slot evento"""
        slot = {}
        
        yBase = 48 + index * self.SLOT_HEIGHT
        
        # Background slot
        slotBg = ui.Bar()
        slotBg.SetParent(self)
        slotBg.SetPosition(12, yBase)
        slotBg.SetSize(375, self.SLOT_HEIGHT - 4)
        slotBg.SetColor(0x44222222)
        slotBg.AddFlag("not_pick")
        slotBg.Show()
        slot["bg"] = slotBg
        
        # Indicatore tipo (colore laterale)
        typeBar = ui.Bar()
        typeBar.SetParent(self)
        typeBar.SetPosition(12, yBase)
        typeBar.SetSize(4, self.SLOT_HEIGHT - 4)
        typeBar.SetColor(0xFFFF6600)
        typeBar.AddFlag("not_pick")
        typeBar.Show()
        slot["typeBar"] = typeBar
        
        # Nome evento
        nameText = ui.TextLine()
        nameText.SetParent(self)
        nameText.SetPosition(22, yBase + 5)
        nameText.SetText("Evento")
        nameText.SetPackedFontColor(0xFFFFFFFF)
        nameText.Show()
        slot["nameText"] = nameText
        
        # Orario
        timeText = ui.TextLine()
        timeText.SetParent(self)
        timeText.SetPosition(22, yBase + 22)
        timeText.SetText("--:-- - --:--")
        timeText.SetPackedFontColor(0xFFAAAAAA)
        timeText.Show()
        slot["timeText"] = timeText
        
        # Reward
        rewardText = ui.TextLine()
        rewardText.SetParent(self)
        rewardText.SetPosition(22, yBase + 38)
        rewardText.SetText("+0")
        rewardText.SetPackedFontColor(0xFFFFD700)
        rewardText.Show()
        slot["rewardText"] = rewardText
        
        # Status text
        statusText = ui.TextLine()
        statusText.SetParent(self)
        statusText.SetPosition(320, yBase + 20)
        statusText.SetText("")
        statusText.SetPackedFontColor(0xFF00FF00)
        statusText.Show()
        slot["statusText"] = statusText
        
        # Hover area
        hoverArea = EventSlotHoverArea()
        hoverArea.SetParent(self)
        hoverArea.SetPosition(12, yBase)
        hoverArea.SetSize(375, self.SLOT_HEIGHT - 4)
        hoverArea.Show()
        slot["hoverArea"] = hoverArea
        
        return slot
    
    def __OnScroll(self):
        """Callback quando si scrolla"""
        scrollPos = self.scrollBar.GetPos()
        maxScroll = max(0, len(self.events) - self.VISIBLE_SLOTS)
        self.scrollPos = int(scrollPos * maxScroll + 0.5)
        self.__UpdateSlotPositions()
    
    def __UpdateSlotPositions(self):
        """Aggiorna posizione e visibilita degli slot in base allo scroll"""
        for slotIdx, slot in enumerate(self.eventSlots):
            eventIdx = self.scrollPos + slotIdx
            
            if eventIdx < len(self.events):
                event = self.events[eventIdx]
                self.__UpdateSlotWithEvent(slot, event)
                slot["bg"].Show()
                slot["typeBar"].Show()
                slot["nameText"].Show()
                slot["timeText"].Show()
                slot["rewardText"].Show()
                slot["statusText"].Show()
                slot["hoverArea"].SetEventData(event)
                slot["hoverArea"].Show()
            else:
                slot["bg"].Hide()
                slot["typeBar"].Hide()
                slot["nameText"].Hide()
                slot["timeText"].Hide()
                slot["rewardText"].Hide()
                slot["statusText"].Hide()
                slot["hoverArea"].Hide()
    
    def __UpdateSlotWithEvent(self, slot, event):
        """Aggiorna uno slot con i dati di un evento"""
        typeColors = {
            "glory_rush": 0xFFFFD700,
            "first_rift": 0xFF9932CC,
            "first_boss": 0xFFFF4444,
            "boss_massacre": 0xFFFF6600,
            "rift_hunt": 0xFF9932CC,
            "super_metin": 0xFFFF8800,
            "metin_frenzy": 0xFFFF8800,
            "double_spawn": 0xFFFF4444,
        }
        
        etype = event.get("type", "glory_rush")
        typeColor = typeColors.get(etype, 0xFFFF6600)
        
        slot["typeBar"].SetColor(typeColor)
        slot["nameText"].SetText(event.get("name", "Evento")[:40])
        slot["timeText"].SetText("%s - %s" % (event.get("start_time", "--:--"), event.get("end_time", "--:--")))
        slot["rewardText"].SetText("+%s" % event.get("reward", "0"))
        
        status = event.get("status", "pending")
        if status == "joined":
            slot["statusText"].SetText("[ISCRITTO]")
            slot["statusText"].SetPackedFontColor(0xFF00FF00)
            slot["bg"].SetColor(0x44003300)
        elif status == "active":
            slot["statusText"].SetText("[IN CORSO]")
            slot["statusText"].SetPackedFontColor(0xFFFFAA00)
            slot["bg"].SetColor(0x44332200)
        elif status == "ended":
            slot["statusText"].SetText("[TERMINATO]")
            slot["statusText"].SetPackedFontColor(0xFF888888)
            slot["bg"].SetColor(0x44222222)
        else:
            slot["statusText"].SetText("")
            slot["bg"].SetColor(0x44222222)
    
    def SetEvents(self, events, theme=None):
        """Imposta la lista eventi"""
        self.events = events if events else []
        self.theme = theme
        self.scrollPos = 0
        
        # Mostra/nascondi scrollbar
        if len(self.events) > self.VISIBLE_SLOTS:
            self.scrollBar.Show()
        else:
            self.scrollBar.Hide()
        
        # Mostra messaggio se nessun evento
        if len(self.events) == 0:
            self.noEventsText.Show()
        else:
            self.noEventsText.Hide()
        
        self.__UpdateSlotPositions()
    
    def Open(self, events=None, theme=None):
        """Apre la finestra"""
        if events is not None:
            self.SetEvents(events, theme)
        self.SetTop()
        self.Show()
    
    def OnPressEscapeKey(self):
        self.Hide()
        return True


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════
g_dailyMissionsWindow = None
g_missionProgressPopup = None
g_missionCompleteWindow = None
g_allMissionsCompleteWindow = None
g_eventsScheduleWindow = None

def GetDailyMissionsWindow():
    global g_dailyMissionsWindow
    if g_dailyMissionsWindow is None:
        g_dailyMissionsWindow = DailyMissionsWindow()
    return g_dailyMissionsWindow

def GetMissionProgressPopup():
    global g_missionProgressPopup
    if g_missionProgressPopup is None:
        g_missionProgressPopup = MissionProgressPopup()
    return g_missionProgressPopup

def GetMissionCompleteWindow():
    global g_missionCompleteWindow
    if g_missionCompleteWindow is None:
        g_missionCompleteWindow = MissionCompleteWindow()
    return g_missionCompleteWindow

def GetAllMissionsCompleteWindow():
    global g_allMissionsCompleteWindow
    if g_allMissionsCompleteWindow is None:
        g_allMissionsCompleteWindow = AllMissionsCompleteWindow()
    return g_allMissionsCompleteWindow

def GetEventsScheduleWindow():
    global g_eventsScheduleWindow
    if g_eventsScheduleWindow is None:
        g_eventsScheduleWindow = EventsScheduleWindow()
    return g_eventsScheduleWindow


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════
def OpenDailyMissions(missions=None, theme=None):
    """Apre finestra missioni giornaliere"""
    GetDailyMissionsWindow().Open(missions, theme)

def ShowMissionProgress(missionName, current, target, theme=None):
    """Mostra popup progresso missione"""
    GetMissionProgressPopup().ShowProgress(missionName, current, target, theme)

def ShowMissionComplete(missionName, reward, theme=None):
    """Mostra effetto missione completata"""
    GetMissionCompleteWindow().ShowComplete(missionName, reward, theme)

def ShowAllMissionsComplete(bonusGlory, theme=None, hasFractureBonus=False):
    """Mostra effetto tutte missioni completate"""
    GetAllMissionsCompleteWindow().ShowBonus(bonusGlory, theme, hasFractureBonus)

def OpenEventsSchedule(events=None, theme=None):
    """Apre finestra eventi"""
    GetEventsScheduleWindow().Open(events, theme)
