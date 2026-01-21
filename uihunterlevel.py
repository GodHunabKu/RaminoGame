# -*- coding: utf-8 -*-
# ============================================================================
#  HUNTER TERMINAL - SOLO LEVELING EDITION v4.0
#  Interfaccia completamente dinamica con colori basati sul Rank
#  Design ispirato a Solo Leveling - Temi scuri con accenti neon
# ============================================================================

import ui
import net
import app
import wndMgr
import grp
from weakref import proxy

# Import moduli Hunter System
import hunter_windows
import hunter_effects
import hunter_missions

# Funzione T() - restituisce direttamente il testo (no multilingua)
def T(key, default=None, replacements=None):
    text = default if default else key
    if replacements and isinstance(replacements, dict):
        for k, v in replacements.items():
            text = text.replace("{" + str(k) + "}", str(v))
    return text

# Import CENTRALIZZATO da hunter_core.py - NO DUPLICAZIONI
from hunter_core import (
    RANK_THEMES,
    RANK_COLORS,
    COLOR_SCHEMES,
    GetRankKey,
    GetRankTheme,
    GetRankProgress,
    FormatNumber,
    FormatTime,
    DraggableMixin,
    WINDOW_POSITIONS,
    SaveWindowPosition,
    GetWindowPosition,
)

# Import SoloLevelingButton da hunter_components.py
from hunter_components import SoloLevelingButton

# ============================================================================
#  CONFIGURAZIONE DIMENSIONI TERMINALE
# ============================================================================
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 540  # Leggermente piu' alto per effetti
CONTENT_HEIGHT = 310
HEADER_HEIGHT = 100
TAB_HEIGHT = 30
FOOTER_HEIGHT = 38

# ============================================================================
#  COLORI SPECIALI
# ============================================================================
GOLD_COLOR = 0xFFFFD700
SILVER_COLOR = 0xFFC0C0C0
BRONZE_COLOR = 0xFFCD7F32

# ============================================================================
#  HUNTER TERMINAL WINDOW
# ============================================================================
class HunterLevelWindow(ui.ScriptWindow):
    def OpenGateTrialWindow(self):
        # Mostra la finestra di stato della trial (Gate/Trial)
        try:
            import uihunterlevel_gate_trial
            wnd = uihunterlevel_gate_trial.GetTrialStatusWindow()
            wnd.Show()
        except Exception as e:
            import dbg
            dbg.TraceError("OpenGateTrialWindow error: " + str(e))

    def UpdateGateStatus(self, gateId, gateName, remainingSeconds, colorCode):
        """Aggiorna la UI con lo stato del Gate"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode)
        except Exception as e:
            import dbg
            dbg.TraceError("UpdateGateStatus error: " + str(e))

    def HideGateTimer(self):
        """Nasconde il timer del Gate"""
        try:
            import uihunterlevel_gate_trial
            # Resetta lo stato del gate (nessun accesso)
            uihunterlevel_gate_trial.UpdateGateStatus(0, "", 0, "GRAY")
        except Exception as e:
            import dbg
            dbg.TraceError("HideGateTimer error: " + str(e))

    def OnGateComplete(self, success, gloriaChange):
        """Mostra il risultato del completamento Gate"""
        try:
            import uihunterlevel_gate_trial
            # Mostra messaggio sistema
            if success:
                uihunterlevel_gate_trial.ShowSystemMessage("GREEN", "Gate completato! +" + str(gloriaChange) + " Gloria")
            else:
                uihunterlevel_gate_trial.ShowSystemMessage("RED", "Gate fallito! -" + str(gloriaChange) + " Gloria")
            # Resetta lo stato del gate
            uihunterlevel_gate_trial.UpdateGateStatus(0, "", 0, "GRAY")
        except Exception as e:
            import dbg
            dbg.TraceError("OnGateComplete error: " + str(e))

    def OnTrialStart(self, trialId, trialName, toRank, colorCode):
        """Mostra l'inizio di una nuova Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.ShowSystemMessage(colorCode, "Nuova Trial iniziata: " + trialName + " - Obiettivo Rank " + toRank)
            # Apri automaticamente la finestra Gate/Trial
            uihunterlevel_gate_trial.OpenGateTrialWindow()
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialStart error: " + str(e))

    def OnTrialStatus(self, trialId, trialName, toRank, colorCode, remainingSeconds,
                      bossKills, bossReq, metinKills, metinReq,
                      fractureSeals, fractureReq, chestOpens, chestReq,
                      dailyMissions, dailyReq):
        """Aggiorna lo stato della Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.UpdateTrialStatus(
                trialId, trialName, toRank, colorCode, remainingSeconds,
                bossKills, bossReq, metinKills, metinReq,
                fractureSeals, fractureReq, chestOpens, chestReq,
                dailyMissions, dailyReq
            )
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialStatus error: " + str(e))

    def OnTrialProgress(self, trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions):
        """Aggiorna il progresso della Trial"""
        try:
            import uihunterlevel_gate_trial
            wnd = uihunterlevel_gate_trial.GetTrialStatusWindow()
            if wnd and wnd.trialData:
                # Aggiorna solo i valori di progresso mantenendo i requisiti
                wnd.progressBars["boss"].SetProgress(bossKills, wnd.trialData["progress"]["boss"][1])
                wnd.progressBars["metin"].SetProgress(metinKills, wnd.trialData["progress"]["metin"][1])
                wnd.progressBars["fracture"].SetProgress(fractureSeals, wnd.trialData["progress"]["fracture"][1])
                wnd.progressBars["chest"].SetProgress(chestOpens, wnd.trialData["progress"]["chest"][1])
                wnd.progressBars["mission"].SetProgress(dailyMissions, wnd.trialData["progress"]["mission"][1])
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialProgress error: " + str(e))

    def OnTrialComplete(self, newRank, gloriaReward, trialName):
        """Mostra il completamento della Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.ShowSystemMessage("GOLD", "Trial completata! Sei ora Rank " + newRank + "! +" + str(gloriaReward) + " Gloria")
            # Resetta la Trial
            uihunterlevel_gate_trial.UpdateTrialStatus(0, "", "", "GRAY", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialComplete error: " + str(e))
    
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.isLoaded = False
        self.isDestroyed = False
        
        self.currentRankKey = "E"
        self.theme = RANK_THEMES["E"]
        
        self.systemMsgWnd = None
        self.emergencyWnd = None
        self.whatIfWnd = None
        self.rivalWnd = None
        
        self.dailyResetSeconds = 0
        self.weeklyResetSeconds = 0
        self.lastUpdateTime = 0
        self.timerUpdateAccum = 0.0
        
        self.currentTab = 0
        self.currentRankingView = "daily_points"

        # Auto-apertura per progresso missioni
        self.autoOpenedForMission = False
        self.autoCloseTimer = 0.0

        self.bgElements = []
        self.headerElements = []
        self.tabButtons = []
        self.contentElements = []
        self.footerElements = []
        self.totalContentHeight = 0
        
        self.baseWindow = None
        self.contentPanel = None
        self.scrollBar = None
        
        self.playerData = {
            "name": "-",
            "total_points": 0,
            "spendable_points": 0,
            "daily_points": 0,
            "weekly_points": 0,
            "total_kills": 0,
            "daily_kills": 0,
            "weekly_kills": 0,
            "login_streak": 0,
            "streak_bonus": 0,
            "total_fractures": 0,
            "total_chests": 0,
            "total_metins": 0,
            "pending_daily_reward": 0,
            "pending_weekly_reward": 0,
            "daily_pos": 0,
            "weekly_pos": 0,
            # Detailed stats
            "chests_e": 0, "chests_d": 0, "chests_c": 0, "chests_b": 0,
            "chests_a": 0, "chests_s": 0, "chests_n": 0,
            "boss_kills_easy": 0, "boss_kills_medium": 0, "boss_kills_hard": 0, "boss_kills_elite": 0,
            "metin_kills_normal": 0, "metin_kills_special": 0,
            "defense_wins": 0, "defense_losses": 0, "elite_kills": 0
        }
        
        self.rankingData = {
            "daily": [], "weekly": [], "total": [],
            "daily_points": [], "weekly_points": [], "total_points": [],
            "daily_kills": [], "weekly_kills": [], "total_kills": [],
            "fractures": [], "chests": [], "metins": []
        }
        self.shopData = []
        self.achievementsData = []
        self.calendarData = []
        self.activeEvent = ("Nessuno", "")
        
        # ============================================================
        # DAILY MISSIONS DATA
        # ============================================================
        self.missionsData = []
        self.missionsCount = 0
        self.eventsData = []
        self.eventsCount = 0
        self.missionsWnd = None
        self.eventsWnd = None
        self.missionProgressWnd = None
        self.missionCompleteWnd = None
        self.allMissionsCompleteWnd = None
        
        # Fracture Bonus System
        self.fractureBonusActive = False
        self.bonusIndicatorText = ""

        # Windows dal modulo hunter_windows
        self.systemMsgWnd = hunter_windows.GetSystemMessageWindow()
        self.emergencyWnd = hunter_windows.GetEmergencyQuestWindow()
        self.whatIfWnd = hunter_windows.GetWhatIfChoiceWindow()
        self.rivalWnd = hunter_windows.GetRivalTrackerWindow()
        self.eventWnd = hunter_windows.GetEventStatusWindow()
        self.overtakeWnd = hunter_windows.GetOvertakeWindow()
        
        # Windows dal modulo hunter_effects
        self.bossAlertWnd = hunter_effects.GetBossAlertWindow()
        self.systemInitWnd = hunter_effects.GetSystemInitWindow()
        self.awakeningWnd = hunter_effects.GetAwakeningEffect()
        self.rankUpWnd = hunter_effects.GetRankUpEffect()
        
        # Daily Missions Windows dal modulo hunter_missions
        self.missionsWnd = hunter_missions.GetDailyMissionsWindow()
        self.eventsWnd = hunter_missions.GetEventsScheduleWindow()
        self.missionProgressWnd = hunter_missions.GetMissionProgressPopup()
        self.missionCompleteWnd = hunter_missions.GetMissionCompleteWindow()
        self.allMissionsCompleteWnd = hunter_missions.GetAllMissionsCompleteWindow()
        
        # Nota: HunterActivationWindow e' stata rimossa (era duplicato di SystemInitWindow)
        self.activationWnd = self.systemInitWnd
        
        # Collega OvertakeWindow a EventStatusWindow per gestione posizione dinamica
        if self.overtakeWnd and self.eventWnd:
            self.overtakeWnd.SetEventWindowRef(self.eventWnd)
        # Collega RivalTrackerWindow a EventStatusWindow per gestione posizione dinamica
        if self.rivalWnd and self.eventWnd:
            self.rivalWnd.SetEventWindowRef(self.eventWnd)
        # Collega EventStatusWindow al terminale per aprire la guida
        if self.eventWnd:
            self.eventWnd.SetParentWindow(self)
        
    def __del__(self):
        ui.ScriptWindow.__del__(self)
        
    def Destroy(self):
        if self.isDestroyed:
            return
        self.isDestroyed = True
        self.Hide()
        self.__ClearAll()
        
        for wnd in [self.systemMsgWnd, self.emergencyWnd, self.whatIfWnd, self.rivalWnd, self.eventWnd]:
            if wnd:
                wnd.Hide()
        self.systemMsgWnd = None
        self.emergencyWnd = None
        self.whatIfWnd = None
        self.rivalWnd = None
        self.eventWnd = None
        
        self.ClearDictionary()
        self.isLoaded = False
        
    def Close(self):
        self.Hide()
        
    def LoadWindow(self):
        if self.isLoaded:
            return True
        try:
            ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/hunterlevel.py")
            self.baseWindow = self.GetChild("BaseWindow")
            # Disabilita mouse pick sul baseWindow per permettere il drag della finestra principale
            if self.baseWindow and hasattr(self.baseWindow, 'AddFlag'):
                self.baseWindow.AddFlag("not_pick")
            self.__BuildInterface()
        except:
            import dbg
            dbg.TraceError("HunterLevelWindow.LoadWindow() failed")
            return False
        
        self.isLoaded = True
        self.isDestroyed = False
        return True
    
    def __ClearAll(self):
        """Pulizia rigorosa anti-memory leak - pattern consistente con hunter_effects.py"""
        # Pulizia bgElements
        for i in range(len(self.bgElements)):
            try:
                if self.bgElements[i]:
                    if hasattr(self.bgElements[i], 'SetEvent'):
                        self.bgElements[i].SetEvent(None)
                    self.bgElements[i].Hide()
                    self.bgElements[i] = None
            except:
                pass
        del self.bgElements[:]
        self.bgElements = []

        # Pulizia headerElements
        for i in range(len(self.headerElements)):
            try:
                if self.headerElements[i]:
                    if hasattr(self.headerElements[i], 'SetEvent'):
                        self.headerElements[i].SetEvent(None)
                    self.headerElements[i].Hide()
                    self.headerElements[i] = None
            except:
                pass
        del self.headerElements[:]
        self.headerElements = []

        # Pulizia contentElements
        for i in range(len(self.contentElements)):
            try:
                if self.contentElements[i]:
                    if hasattr(self.contentElements[i], 'SetEvent'):
                        self.contentElements[i].SetEvent(None)
                    self.contentElements[i].Hide()
                    self.contentElements[i] = None
            except:
                pass
        del self.contentElements[:]
        self.contentElements = []

        # Pulizia footerElements
        for i in range(len(self.footerElements)):
            try:
                if self.footerElements[i]:
                    if hasattr(self.footerElements[i], 'SetEvent'):
                        self.footerElements[i].SetEvent(None)
                    self.footerElements[i].Hide()
                    self.footerElements[i] = None
            except:
                pass
        del self.footerElements[:]
        self.footerElements = []

        # Pulizia tabButtons
        for i in range(len(self.tabButtons)):
            try:
                if self.tabButtons[i]:
                    self.tabButtons[i].SetEvent(None)
                    self.tabButtons[i].Hide()
                    self.tabButtons[i] = None
            except:
                pass
        del self.tabButtons[:]
        self.tabButtons = []

    def __UpdateTheme(self):
        newKey = GetRankKey(self.playerData["total_points"])
        if newKey != self.currentRankKey:
            self.currentRankKey = newKey
            self.theme = RANK_THEMES[newKey]
            self.__BuildInterface()
            self.__UpdateSpecialWindowsTheme()
    
    def __UpdateSpecialWindowsTheme(self):
        # REMOVED: Non aggiornare il colore del SystemMessageWindow con il tema
        # I messaggi devono mantenere il colore del loro rank specifico (E,D,C,B,A,S,N)
        # altrimenti quando il player cambia rank, tutti i messaggi cambiano colore!
        pass
    
    def __BuildInterface(self):
        self.__ClearAll()
        self.theme = RANK_THEMES[self.currentRankKey]
        
        self.__CreateBackground()
        self.__CreateHeader()
        self.__CreateTabs()
        self.__CreateContentArea()
        self.__CreateFooter()
        self.__OnClickTab(self.currentTab)
    
    # ========================================================================
    #  BACKGROUND
    # ========================================================================
    def _DisableMousePick(self, widget):
        """Aggiunge il flag not_pick a un widget per permettere drag della finestra"""
        if hasattr(widget, 'AddFlag'):
            try:
                widget.AddFlag("not_pick")
            except:
                pass
        return widget
    
    def __CreateBackground(self):
        t = self.theme

        # Glow esterno finestra principale (layer piu' grande per effetto "alone")
        glowFrame = ui.Bar()
        glowFrame.SetParent(self.baseWindow)
        glowFrame.SetPosition(-2, -2)
        glowFrame.SetSize(WINDOW_WIDTH + 4, WINDOW_HEIGHT + 4)
        glowFrame.SetColor(t["glow"])
        glowFrame.Show()
        self._DisableMousePick(glowFrame)
        self.bgElements.append(glowFrame)

        # Background principale
        bg = ui.Bar()
        bg.SetParent(self.baseWindow)
        bg.SetPosition(0, 0)
        bg.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        bg.SetColor(t["bg_dark"])
        bg.Show()
        self._DisableMousePick(bg)
        self.bgElements.append(bg)

        # Bordi neon della finestra
        for (x, y, w, h) in [(0, 0, WINDOW_WIDTH, 3), (0, WINDOW_HEIGHT - 3, WINDOW_WIDTH, 3),
                             (0, 0, 3, WINDOW_HEIGHT), (WINDOW_WIDTH - 3, 0, 3, WINDOW_HEIGHT)]:
            border = ui.Bar()
            border.SetParent(self.baseWindow)
            border.SetPosition(x, y)
            border.SetSize(w, h)
            border.SetColor(t["border"])
            border.Show()
            self._DisableMousePick(border)
            self.bgElements.append(border)

        # Angoli decorativi ESTERNI - Solo Leveling Style
        cornerLen = 25
        cornerColor = t.get("pulse_color", t["accent"])

        # Top-Left
        self.__CreateCorner(0, 0, cornerLen, cornerColor, "TL")
        # Top-Right
        self.__CreateCorner(WINDOW_WIDTH - cornerLen, 0, cornerLen, cornerColor, "TR")
        # Bottom-Left
        self.__CreateCorner(0, WINDOW_HEIGHT - cornerLen, cornerLen, cornerColor, "BL")
        # Bottom-Right
        self.__CreateCorner(WINDOW_WIDTH - cornerLen, WINDOW_HEIGHT - cornerLen, cornerLen, cornerColor, "BR")

        closeBtn = SoloLevelingButton()
        closeBtn.Create(self.baseWindow, WINDOW_WIDTH - 35, 8, 25, 20, "X", t)
        closeBtn.SetEvent(ui.__mem_func__(self.Close))
        self.bgElements.append(closeBtn)

    def __CreateCorner(self, x, y, size, color, position):
        """Crea angolo decorativo in stile Solo Leveling"""
        t = self.theme

        if position == "TL":
            h = ui.Bar()
            h.SetParent(self.baseWindow)
            h.SetPosition(x, y)
            h.SetSize(size, 3)
            h.SetColor(color)
            h.Show()
            self._DisableMousePick(h)
            self.bgElements.append(h)

            v = ui.Bar()
            v.SetParent(self.baseWindow)
            v.SetPosition(x, y)
            v.SetSize(3, size)
            v.SetColor(color)
            v.Show()
            self._DisableMousePick(v)
            self.bgElements.append(v)

        elif position == "TR":
            h = ui.Bar()
            h.SetParent(self.baseWindow)
            h.SetPosition(x, y)
            h.SetSize(size, 3)
            h.SetColor(color)
            h.Show()
            self._DisableMousePick(h)
            self.bgElements.append(h)

            v = ui.Bar()
            v.SetParent(self.baseWindow)
            v.SetPosition(x + size - 3, y)
            v.SetSize(3, size)
            v.SetColor(color)
            v.Show()
            self._DisableMousePick(v)
            self.bgElements.append(v)

        elif position == "BL":
            h = ui.Bar()
            h.SetParent(self.baseWindow)
            h.SetPosition(x, y + size - 3)
            h.SetSize(size, 3)
            h.SetColor(color)
            h.Show()
            self._DisableMousePick(h)
            self.bgElements.append(h)

            v = ui.Bar()
            v.SetParent(self.baseWindow)
            v.SetPosition(x, y)
            v.SetSize(3, size)
            v.SetColor(color)
            v.Show()
            self._DisableMousePick(v)
            self.bgElements.append(v)

        elif position == "BR":
            h = ui.Bar()
            h.SetParent(self.baseWindow)
            h.SetPosition(x, y + size - 3)
            h.SetSize(size, 3)
            h.SetColor(color)
            h.Show()
            self._DisableMousePick(h)
            self.bgElements.append(h)

            v = ui.Bar()
            v.SetParent(self.baseWindow)
            v.SetPosition(x + size - 3, y)
            v.SetSize(3, size)
            v.SetColor(color)
            v.Show()
            self._DisableMousePick(v)
            self.bgElements.append(v)
    
    # ========================================================================
    #  HEADER
    # ========================================================================
    def __CreateHeader(self):
        t = self.theme

        # Glow esterno (layer piu' grande)
        glowOuter = ui.Bar()
        glowOuter.SetParent(self.baseWindow)
        glowOuter.SetPosition(8, 8)
        glowOuter.SetSize(WINDOW_WIDTH - 16, HEADER_HEIGHT + 4)
        glowOuter.SetColor(t["glow"])
        glowOuter.Show()
        self._DisableMousePick(glowOuter)
        self.headerElements.append(glowOuter)

        # Background header
        headerBg = ui.Bar()
        headerBg.SetParent(self.baseWindow)
        headerBg.SetPosition(10, 10)
        headerBg.SetSize(WINDOW_WIDTH - 20, HEADER_HEIGHT)
        headerBg.SetColor(t["bg_medium"])
        headerBg.Show()
        self._DisableMousePick(headerBg)
        self.headerElements.append(headerBg)

        # Bordi neon header (top, bottom, left, right)
        glowTop = ui.Bar()
        glowTop.SetParent(self.baseWindow)
        glowTop.SetPosition(10, 10)
        glowTop.SetSize(WINDOW_WIDTH - 20, 2)
        glowTop.SetColor(t["glow_strong"])
        glowTop.Show()
        self._DisableMousePick(glowTop)
        self.headerElements.append(glowTop)

        glowBottom = ui.Bar()
        glowBottom.SetParent(self.baseWindow)
        glowBottom.SetPosition(10, HEADER_HEIGHT + 8)
        glowBottom.SetSize(WINDOW_WIDTH - 20, 2)
        glowBottom.SetColor(t["glow_strong"])
        glowBottom.Show()
        self._DisableMousePick(glowBottom)
        self.headerElements.append(glowBottom)

        # Angoli decorativi - SOLO LEVELING STYLE
        cornerSize = 12
        cornerColor = t.get("pulse_color", t["accent"])

        # Top-Left corner
        cTL1 = ui.Bar()
        cTL1.SetParent(self.baseWindow)
        cTL1.SetPosition(10, 10)
        cTL1.SetSize(cornerSize, 3)
        cTL1.SetColor(cornerColor)
        cTL1.Show()
        self._DisableMousePick(cTL1)
        self.headerElements.append(cTL1)

        cTL2 = ui.Bar()
        cTL2.SetParent(self.baseWindow)
        cTL2.SetPosition(10, 10)
        cTL2.SetSize(3, cornerSize)
        cTL2.SetColor(cornerColor)
        cTL2.Show()
        self._DisableMousePick(cTL2)
        self.headerElements.append(cTL2)

        # Top-Right corner
        cTR1 = ui.Bar()
        cTR1.SetParent(self.baseWindow)
        cTR1.SetPosition(WINDOW_WIDTH - 10 - cornerSize, 10)
        cTR1.SetSize(cornerSize, 3)
        cTR1.SetColor(cornerColor)
        cTR1.Show()
        self._DisableMousePick(cTR1)
        self.headerElements.append(cTR1)

        cTR2 = ui.Bar()
        cTR2.SetParent(self.baseWindow)
        cTR2.SetPosition(WINDOW_WIDTH - 13, 10)
        cTR2.SetSize(3, cornerSize)
        cTR2.SetColor(cornerColor)
        cTR2.Show()
        self._DisableMousePick(cTR2)
        self.headerElements.append(cTR2)

        # Bottom-Left corner
        cBL1 = ui.Bar()
        cBL1.SetParent(self.baseWindow)
        cBL1.SetPosition(10, HEADER_HEIGHT + 7)
        cBL1.SetSize(cornerSize, 3)
        cBL1.SetColor(cornerColor)
        cBL1.Show()
        self._DisableMousePick(cBL1)
        self.headerElements.append(cBL1)

        cBL2 = ui.Bar()
        cBL2.SetParent(self.baseWindow)
        cBL2.SetPosition(10, HEADER_HEIGHT + 10 - cornerSize)
        cBL2.SetSize(3, cornerSize)
        cBL2.SetColor(cornerColor)
        cBL2.Show()
        self._DisableMousePick(cBL2)
        self.headerElements.append(cBL2)

        # Bottom-Right corner
        cBR1 = ui.Bar()
        cBR1.SetParent(self.baseWindow)
        cBR1.SetPosition(WINDOW_WIDTH - 10 - cornerSize, HEADER_HEIGHT + 7)
        cBR1.SetSize(cornerSize, 3)
        cBR1.SetColor(cornerColor)
        cBR1.Show()
        self._DisableMousePick(cBR1)
        self.headerElements.append(cBR1)

        cBR2 = ui.Bar()
        cBR2.SetParent(self.baseWindow)
        cBR2.SetPosition(WINDOW_WIDTH - 13, HEADER_HEIGHT + 10 - cornerSize)
        cBR2.SetSize(3, cornerSize)
        cBR2.SetColor(cornerColor)
        cBR2.Show()
        self._DisableMousePick(cBR2)
        self.headerElements.append(cBR2)

        self.__UpdateHeaderContent()
    
    def __UpdateHeaderContent(self):
        # Mantieni i primi 12 elementi (glow, bg, bordi, angoli decorativi)
        baseElements = 12
        for e in self.headerElements[baseElements:]:
            try:
                e.Hide()
            except:
                pass
        self.headerElements = self.headerElements[:baseElements]
        
        t = self.theme
        pts = self.playerData["total_points"]
        progress = GetRankProgress(pts)
        
        self.__HText("Cacciatore:", 20, 18, t["text_muted"])
        self.__HText(str(self.playerData["name"]), 95, 18, t["accent"])
        
        self.__HText("Gloria:", 250, 18, t["text_muted"])
        self.__HText(FormatNumber(pts), 305, 18, GOLD_COLOR)
        self.__HText("Oggi:", 400, 18, t["text_muted"])
        self.__HText("+" + FormatNumber(self.playerData["daily_points"]), 440, 18, 0xFF00FF88)
        
        rankText = "[%s] %s - %s" % (self.currentRankKey, t["name"], t["title"])
        self.__HText(rankText, 20, 40, t["accent"])
        
        self.__HText("Spendibili:", 250, 40, t["text_muted"])
        self.__HText(FormatNumber(self.playerData["spendable_points"]), 305, 40, 0xFFFFA500)
        
        streak = self.playerData["login_streak"]
        bonus = self.playerData["streak_bonus"]
        
        # Calcola bonus streak client-side se il server non lo manda
        if streak > 0 and bonus == 0:
            if streak >= 30:
                bonus = 20
            elif streak >= 7:
                bonus = 10
            elif streak >= 3:
                bonus = 5
        
        if streak > 0:
            self.__HText("Streak: %dg (+%d%%)" % (streak, bonus), 400, 40, 0xFF00FF88)
        
        barX, barY = 20, 65
        barW, barH = 320, 14
        
        barBg = ui.Bar()
        barBg.SetParent(self.baseWindow)
        barBg.SetPosition(barX, barY)
        barBg.SetSize(barW, barH)
        barBg.SetColor(0xFF111111)
        barBg.Show()
        self._DisableMousePick(barBg)
        self.headerElements.append(barBg)
        
        fillW = max(1, int(barW * progress / 100))
        barFill = ui.Bar()
        barFill.SetParent(self.baseWindow)
        barFill.SetPosition(barX, barY)
        barFill.SetSize(fillW, barH)
        barFill.SetColor(t["bar_fill"])
        barFill.Show()
        self._DisableMousePick(barFill)
        self.headerElements.append(barFill)
        
        self.__HText("%d%%" % int(progress), 350, 63, t["accent"])
        
        nextKey = self.__GetNextRankKey()
        if nextKey:
            nextTheme = RANK_THEMES[nextKey]
            self.__HText("Prossimo:", 400, 63, t["text_muted"])
            self.__HText(nextTheme["name"], 460, 63, nextTheme["accent"])
        else:
            self.__HText("RANK MASSIMO!", 400, 63, GOLD_COLOR)
    
    def __HText(self, text, x, y, color):
        t = ui.TextLine()
        t.SetParent(self.baseWindow)
        t.SetPosition(x, y)
        t.SetText(str(text))
        t.SetPackedFontColor(color)
        t.Show()
        self._DisableMousePick(t)
        self.headerElements.append(t)
    
    def __GetNextRankKey(self):
        order = ["E", "D", "C", "B", "A", "S", "N"]
        idx = order.index(self.currentRankKey)
        if idx < len(order) - 1:
            return order[idx + 1]
        return None
    
    # ========================================================================
    #  TABS - Bottoni custom Solo Leveling
    # ========================================================================
    def __CreateTabs(self):
        t = self.theme
        # Usa traduzioni dal DB - fallback a italiano se non disponibili
        tabNames = [
            T("UI_TAB_STATS", "Stats"),
            T("UI_TAB_RANK", "Rank"),
            T("UI_TAB_SHOP", "Shop"),
            T("UI_TAB_ACHIEV", "Achiev"),
            T("UI_TAB_EVENTS", "Eventi"),
            T("UI_TAB_GUIDE", "Guida")
        ]
        tabY = HEADER_HEIGHT + 20
        tabW = 75
        startX = 15

        for i, name in enumerate(tabNames):
            btn = SoloLevelingButton()
            btn.Create(self.baseWindow, startX + (i * (tabW + 5)), tabY, tabW, 24, name, t)
            btn.SetEvent(ui.__mem_func__(self.__OnClickTab), i)
            self.tabButtons.append(btn)
    
    def __OnClickTab(self, idx):
        t = self.theme
        for i, btn in enumerate(self.tabButtons):
            if i == idx:
                btn.Down()
            else:
                btn.SetUp()

        # Se il player cambia tab manualmente, disabilita auto-close
        # (significa che vuole esplorare e tenere la finestra aperta)
        if self.currentTab != idx and self.autoOpenedForMission:
            self.autoOpenedForMission = False
            self.autoCloseTimer = 0.0

        self.currentTab = idx
        self.__LoadTabContent(idx)
    
    # ========================================================================
    #  CONTENT AREA
    # ========================================================================
    def __CreateContentArea(self):
        t = self.theme
        contentY = HEADER_HEIGHT + TAB_HEIGHT + 30
        contentH = CONTENT_HEIGHT
        
        contentBg = ui.Bar()
        contentBg.SetParent(self.baseWindow)
        contentBg.SetPosition(10, contentY)
        contentBg.SetSize(WINDOW_WIDTH - 20, contentH)
        contentBg.SetColor(t["bg_light"])
        contentBg.Show()
        self._DisableMousePick(contentBg)
        self.bgElements.append(contentBg)
        
        self.contentPanel = ui.Window()
        self.contentPanel.SetParent(self.baseWindow)
        self.contentPanel.SetPosition(15, contentY + 5)
        self.contentPanel.SetSize(WINDOW_WIDTH - 50, contentH - 10)
        self.contentPanel.Show()
        self._DisableMousePick(self.contentPanel)
        
        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self.baseWindow)
        self.scrollBar.SetPosition(WINDOW_WIDTH - 30, contentY + 10)
        self.scrollBar.SetScrollBarSize(contentH - 20)
        self.scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
        self._DisableMousePick(self.scrollBar)
        self.scrollBar.Hide()
    
    def __ClearContent(self):
        for e in self.contentElements:
            try:
                if hasattr(e, 'SetEvent'):
                    e.SetEvent(None)
                e.Hide()
            except:
                pass
        self.contentElements = []
        self.totalContentHeight = 0
        if self.scrollBar:
            self.scrollBar.Hide()
            self.scrollBar.SetPos(0)
    
    def __LoadTabContent(self, idx):
        self.__ClearContent()
        
        if idx == 0:
            self.__LoadStats()
        elif idx == 1:
            self.__LoadRanking(self.currentRankingView)
        elif idx == 2:
            self.__LoadShop()
        elif idx == 3:
            self.__LoadAchievements()
        elif idx == 4:
            self.__LoadEvents()
        elif idx == 5:
            self.__LoadGuide()
        
        self.__SavePositions()
        self.__UpdateScroll()
    
    def __SavePositions(self):
        for e in self.contentElements:
            try:
                if not hasattr(e, '_oy'):
                    e._oy = e.GetLocalPosition()[1]
            except:
                pass
    
    def __UpdateScroll(self):
        if not self.contentPanel or not self.scrollBar:
            return
        maxY = 0
        for e in self.contentElements:
            try:
                y = e._oy if hasattr(e, '_oy') else e.GetLocalPosition()[1]
                h = e.GetHeight() if hasattr(e, 'GetHeight') else 20
                maxY = max(maxY, y + h)
            except:
                pass
        self.totalContentHeight = maxY
        if maxY > CONTENT_HEIGHT - 10:
            self.scrollBar.Show()
            self.scrollBar.SetPos(0)
        else:
            self.scrollBar.Hide()
    
    def __OnScroll(self):
        if not self.scrollBar:
            return
        try:
            pos = self.scrollBar.GetPos()
        except:
            pos = 0
        scrollH = max(0, self.totalContentHeight - (CONTENT_HEIGHT - 10))
        off = -int(pos * scrollH)
        for e in self.contentElements:
            try:
                if not hasattr(e, '_oy'):
                    e._oy = e.GetLocalPosition()[1]
                x = e.GetLocalPosition()[0]
                ny = e._oy + off
                e.SetPosition(x, ny)
                if ny < -30 or ny > CONTENT_HEIGHT:
                    e.Hide()
                else:
                    e.Show()
            except:
                pass
    
    # ========================================================================
    #  FOOTER
    # ========================================================================
    def __CreateFooter(self):
        t = self.theme
        footerY = WINDOW_HEIGHT - FOOTER_HEIGHT - 10

        footerBg = ui.Bar()
        footerBg.SetParent(self.baseWindow)
        footerBg.SetPosition(10, footerY)
        footerBg.SetSize(WINDOW_WIDTH - 20, FOOTER_HEIGHT)
        footerBg.SetColor(t["bg_medium"])
        footerBg.Show()
        self._DisableMousePick(footerBg)
        self.footerElements.append(footerBg)

        self.__FText("Reset Daily:", 20, footerY + 10, t["text_muted"])
        self.dailyTimerLabel = self.__FText("--:--:--", 100, footerY + 10, t["text_value"])

        self.__FText("Reset Weekly:", 200, footerY + 10, t["text_muted"])
        self.weeklyTimerLabel = self.__FText("--", 290, footerY + 10, t["text_value"])

    def __FText(self, text, x, y, color):
        t = ui.TextLine()
        t.SetParent(self.baseWindow)
        t.SetPosition(x, y)
        t.SetText(str(text))
        t.SetPackedFontColor(color)
        t.Show()
        self._DisableMousePick(t)
        self.footerElements.append(t)
        return t

    # ========================================================================
    # ========================================================================
    #  CONTENT HELPERS
    # ========================================================================
    def __CText(self, txt, x, y, col):
        t = ui.TextLine()
        t.SetParent(self.contentPanel)
        t.SetPosition(x, y)
        t.SetText(str(txt))
        t.SetPackedFontColor(col)
        t.Show()
        self._DisableMousePick(t)
        self.contentElements.append(t)
        return t
    
    def __CBar(self, x, y, w, h, col):
        b = ui.Bar()
        b.SetParent(self.contentPanel)
        b.SetPosition(x, y)
        b.SetSize(w, h)
        b.SetColor(col)
        b.Show()
        self._DisableMousePick(b)
        self.contentElements.append(b)
        return b
    
    def __CSep(self, x, y):
        self.__CBar(x, y, 430, 1, self.theme["border"])
    
    def __CProgressBar(self, x, y, w, h, pct, col):
        self.__CBar(x, y, w, h, 0xFF111111)
        fw = max(1, int(w * pct / 100))
        self.__CBar(x, y, fw, h, col)
    
    def __CButton(self, x, y, text, callback, arg=None):
        btn = SoloLevelingButton()
        btn.Create(self.contentPanel, x, y, 80, 22, text, self.theme)
        if arg is not None:
            btn.SetEvent(callback, arg)
        else:
            btn.SetEvent(callback)
        self.contentElements.append(btn)
        return btn
    
    # ========================================================================
    #  TAB CONTENTS
    # ========================================================================
    def __LoadStats(self):
        t = self.theme
        y = 5

        # ============================================================
        # HEADER - RISVEGLIATO STATUS
        # ============================================================
        self.__CText(T("STATS_TITLE", ">>> STATO RISVEGLIATO <<<"), 5, y, t["accent"])
        y += 25

        # ============================================================
        # RANK BADGE + INFO
        # ============================================================
        self.__CBar(5, y, 420, 55, t["bg_dark"])

        # Badge visivo del rango (a sinistra)
        self.__CBar(15, y + 8, 40, 40, t["accent"])
        self.__CText(self.currentRankKey, 27, y + 17, 0xFF000000)

        # Nome rango e titolo
        self.__CText(t["name"], 65, y + 8, t["accent"])
        self.__CText(t["title"], 65, y + 23, t["text_muted"])

        # Posizione in classifica (se presente)
        daily_pos = self.playerData.get("daily_pos", 0)
        weekly_pos = self.playerData.get("weekly_pos", 0)
        if daily_pos > 0:
            self.__CText(T("RANK_POSITION", "Classifica:"), 250, y + 8, t["text_muted"])
            self.__CText("#%d oggi | #%d settimana" % (daily_pos, weekly_pos if weekly_pos > 0 else 999), 250, y + 23, GOLD_COLOR)

        y += 60

        # ============================================================
        # PROGRESSO VERSO PROSSIMO RANK
        # ============================================================
        progress = GetRankProgress(self.playerData["total_points"])
        total_glory = self.playerData["total_points"]

        # Calcola distanza dal prossimo rango
        rank_thresholds = [
            ("N", 1500000), ("S", 500000), ("A", 150000),
            ("B", 50000), ("C", 10000), ("D", 2000), ("E", 0)
        ]
        next_rank_name = None
        next_rank_glory = None
        for rk, threshold in rank_thresholds:
            if total_glory < threshold:
                next_rank_name = rk
                next_rank_glory = threshold
                break

        self.__CBar(5, y, 420, 45, t["bg_dark"])
        self.__CText(T("STATS_PROGRESS", "PROGRESSO RISVEGLIO:"), 15, y + 5, t["accent"])
        self.__CProgressBar(15, y + 22, 340, 14, progress, t["bar_fill"])
        self.__CText("%d%%" % int(progress), 365, y + 21, t["accent"])

        if next_rank_name and next_rank_glory:
            missing = next_rank_glory - total_glory
            next_theme = RANK_THEMES[next_rank_name]
            self.__CText(T("NEXT_RANK", "Prossimo: [%s] %s" % (next_rank_name, next_theme["name"])), 15, y + 38, next_theme["accent"])
            self.__CText(T("MISSING_GLORY", "(-" + FormatNumber(missing) + " Gloria)"), 280, y + 38, 0xFFFFAA55)
        else:
            self.__CText(T("MAX_RANK", ">>> HAI RAGGIUNTO IL RANGO MASSIMO <<<"), 15, y + 38, 0xFFFFD700)

        y += 50

        # ============================================================
        # STREAK BONUS (se attivo)
        # ============================================================
        streak = self.playerData.get("login_streak", 0)
        streak_bonus = self.playerData.get("streak_bonus", 0)
        if streak > 0:
            streak_color = 0xFF00FF88 if streak >= 30 else 0xFFFFAA55 if streak >= 7 else 0xFF00AAFF
            self.__CBar(5, y, 420, 25, 0x33FFAA00)

            streak_icon = "[***]" if streak >= 30 else "[**]" if streak >= 7 else "[*]"
            # streak_bonus arriva già come percentuale (12, non 0.12)
            self.__CText(T("STREAK", "%s SERIE CONSECUTIVA: %d giorni | Bonus: +%d%%" % (streak_icon, streak, int(streak_bonus))), 15, y + 6, streak_color)
            y += 30

        # ============================================================
        # PREMI DISPONIBILI
        # ============================================================
        if self.playerData.get("pending_daily_reward", 0) > 0 or self.playerData.get("pending_weekly_reward", 0) > 0:
            self.__CBar(5, y, 420, 30, 0x4400FF00)
            self.__CText(T("STATS_REWARDS_AVAILABLE", "[!] PREMI DA RISCUOTERE [!]"), 15, y + 8, 0xFF00FF88)
            self.__CButton(340, y + 3, T("BTN_CLAIM", "Ritira"), ui.__mem_func__(self.__OnSmartClaim))
            y += 40

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # POWER LEVEL (in stile Solo Leveling)
        # ============================================================
        # Calcola un "livello di potere" basato su gloria + kills
        power_level = int((total_glory / 1000) + (self.playerData["total_kills"] / 10))
        power_rank = "SSS" if power_level > 5000 else "SS" if power_level > 2000 else "S" if power_level > 1000 else "A" if power_level > 500 else "B" if power_level > 200 else "C" if power_level > 100 else "D"

        self.__CText(T("POWER_LEVEL", "LIVELLO DI POTERE"), 5, y, t["accent"])
        y += 22
        self.__CBar(5, y, 420, 35, 0x22440000)
        self.__CText(T("POWER_VALUE", "Rango: %s | Potere: %s" % (power_rank, FormatNumber(power_level))), 15, y + 3, GOLD_COLOR)

        # Calcola bonus totale giornaliero (rank bonus + streak)
        # streak_bonus arriva già come percentuale (12, non 0.12)
        rank_bonuses = {"N": 1.12, "S": 1.10, "A": 1.07, "B": 1.05, "C": 1.03, "D": 1.01, "E": 1.0}
        rank_bonus = rank_bonuses.get(self.currentRankKey, 1.0)
        rank_bonus_pct = (rank_bonus - 1.0) * 100  # Converti rank_bonus a percentuale
        total_daily_bonus = rank_bonus_pct + streak_bonus  # Somma due percentuali

        if total_daily_bonus > 0:
            self.__CText(T("DAILY_BONUS", "Bonus Giornaliero Totale: +%.1f%% (Rango: +%.0f%% | Streak: +%.0f%%)" % (total_daily_bonus, rank_bonus_pct, streak_bonus)), 15, y + 18, 0xFFFFAA55)
        y += 40

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # STATISTICHE COMBATTIMENTO
        # ============================================================
        self.__CText(T("STATS_COMBAT", "[ STATISTICHE COMBATTIMENTO ]"), 5, y, t["accent"])
        y += 25

        self.__CText(T("STATS_TODAY", "OGGI"), 100, y, 0xFF00AAFF)
        self.__CText(T("STATS_TOTAL", "TOTALE"), 300, y, GOLD_COLOR)
        y += 20

        self.__CText(T("STATS_KILLS", "Uccisioni:"), 15, y, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["daily_kills"]), 120, y, 0xFF00FF88)
        self.__CText(FormatNumber(self.playerData["total_kills"]), 320, y, t["text_value"])
        y += 20

        self.__CText(T("STATS_GLORY", "Gloria:"), 15, y, t["text_muted"])
        self.__CText("+" + FormatNumber(self.playerData["daily_points"]), 120, y, GOLD_COLOR)
        self.__CText(FormatNumber(self.playerData["total_points"]), 320, y, GOLD_COLOR)
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # ECONOMIA - CRISTALLI GLORIA
        # ============================================================
        self.__CText(T("STATS_ECONOMY", "[ CRISTALLI GLORIA ]"), 5, y, 0xFFFFA500)
        y += 22
        self.__CText(T("STATS_SPENDABLE", "Spendibili:"), 15, y, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["spendable_points"]) + " CR", 120, y, 0xFFFFA500)

        # Mostra percentuale di gloria spesa
        if total_glory > 0:
            spent_glory = total_glory - self.playerData["spendable_points"]
            spent_percent = int((spent_glory * 100.0) / total_glory)
            self.__CText(T("SPENT_PERCENT", "(Spesa: %d%%)" % spent_percent), 280, y, t["text_muted"])
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # RECORD PERSONALI
        # ============================================================
        self.__CText(T("STATS_RECORDS", "[ RECORD PERSONALI ]"), 5, y, t["accent"])
        y += 22
        self.__CText(T("STATS_FRACTURES", "Fratture: %d" % self.playerData["total_fractures"]), 15, y, t["accent"])
        self.__CText("Metin: %d" % self.playerData["total_metins"], 160, y, 0xFFFFA500)
        self.__CText(T("STATS_CHESTS", "Bauli: %d" % self.playerData["total_chests"]), 300, y, GOLD_COLOR)
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # BAULI PER GRADO
        # ============================================================
        self.__CText(T("STATS_CHESTS_BY_GRADE", "[ BAULI PER GRADO ]"), 5, y, 0xFFFFD700)
        y += 22

        # Riga 1: E, D, C, B
        chest_colors = {"E": 0xFF00FF00, "D": 0xFF0088FF, "C": 0xFFFF8800, "B": 0xFFFF0000,
                       "A": 0xFFFFD700, "S": 0xFFAA00FF, "N": 0xFFFFFFFF}
        self.__CText("E: %d" % self.playerData.get("chests_e", 0), 15, y, chest_colors["E"])
        self.__CText("D: %d" % self.playerData.get("chests_d", 0), 80, y, chest_colors["D"])
        self.__CText("C: %d" % self.playerData.get("chests_c", 0), 145, y, chest_colors["C"])
        self.__CText("B: %d" % self.playerData.get("chests_b", 0), 210, y, chest_colors["B"])
        y += 20

        # Riga 2: A, S, N
        self.__CText("A: %d" % self.playerData.get("chests_a", 0), 15, y, chest_colors["A"])
        self.__CText("S: %d" % self.playerData.get("chests_s", 0), 80, y, chest_colors["S"])
        self.__CText("N: %d" % self.playerData.get("chests_n", 0), 145, y, chest_colors["N"])
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # BOSS & ELITE
        # ============================================================
        self.__CText(T("STATS_BOSS_KILLS", "[ BOSS ELIMINATI ]"), 5, y, 0xFFFF0000)
        y += 22

        total_boss = (self.playerData.get("boss_kills_easy", 0) + self.playerData.get("boss_kills_medium", 0) +
                     self.playerData.get("boss_kills_hard", 0) + self.playerData.get("boss_kills_elite", 0))
        self.__CText("Totale Boss: %d" % total_boss, 15, y, 0xFFFFAA55)
        y += 20

        self.__CText("Facili: %d" % self.playerData.get("boss_kills_easy", 0), 15, y, 0xFF00FF88)
        self.__CText("Medi: %d" % self.playerData.get("boss_kills_medium", 0), 110, y, 0xFF00AAFF)
        self.__CText("Difficili: %d" % self.playerData.get("boss_kills_hard", 0), 205, y, 0xFFFF8800)
        self.__CText("Elite: %d" % self.playerData.get("boss_kills_elite", 0), 320, y, 0xFFFF00FF)
        y += 20

        self.__CText(T("STATS_ELITE_TOTAL", "Elite Totali: %d" % self.playerData.get("elite_kills", 0)), 15, y, 0xFFFFD700)
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # METIN & DEFENSE
        # ============================================================
        self.__CText(T("STATS_METIN_DEFENSE", "[ METIN & DIFESE ]"), 5, y, 0xFF00AAFF)
        y += 22

        # Metin
        metin_normal = self.playerData.get("metin_kills_normal", 0)
        metin_special = self.playerData.get("metin_kills_special", 0)
        self.__CText("Metin Normali: %d" % metin_normal, 15, y, t["text_value"])
        self.__CText("Metin Speciali: %d" % metin_special, 200, y, 0xFFFF8800)
        y += 20

        # Defense Win Rate
        defense_wins = self.playerData.get("defense_wins", 0)
        defense_losses = self.playerData.get("defense_losses", 0)
        defense_total = defense_wins + defense_losses
        if defense_total > 0:
            win_rate = int((defense_wins * 100.0) / defense_total)
            win_color = 0xFF00FF88 if win_rate >= 70 else 0xFFFFAA55 if win_rate >= 50 else 0xFFFF4444
            self.__CText("Difese: %d Vinte | %d Perse | Win Rate: %d%%" % (defense_wins, defense_losses, win_rate), 15, y, win_color)
        else:
            self.__CText("Difese: Nessuna difesa completata", 15, y, t["text_muted"])
    
    def __LoadShop(self):
        t = self.theme
        y = 5

        self.__CText(T("SHOP_TITLE", "[ MERCANTE HUNTER ]"), 150, y, t["accent"])
        y += 28

        self.__CText(T("SHOP_GLORY_AVAILABLE", "Gloria disponibile:"), 15, y, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["spendable_points"]), 150, y, 0xFFFFA500)
        y += 25

        self.__CSep(5, y)
        y += 15

        if not self.shopData:
            self.__CText(T("SHOP_EMPTY", "Negozio vuoto."), 160, y + 40, t["text_muted"])
            return

        for item in self.shopData:
            name = item.get("name", "Item").replace("+", " ")
            price = item.get("price", 0)
            count = item.get("count", 1)
            itemId = item.get("id", 0)
            canBuy = self.playerData["spendable_points"] >= price

            bgCol = t["bg_dark"] if canBuy else 0x22440000
            self.__CBar(5, y, 420, 35, bgCol)

            displayName = "%s x%d" % (name, count) if count > 1 else name
            self.__CText(displayName, 15, y + 3, t["text_value"] if canBuy else t["text_muted"])

            self.__CText(T("SHOP_PRICE", "Prezzo:"), 15, y + 18, t["text_muted"])
            priceCol = 0xFFFFA500 if canBuy else 0xFFFF4444
            self.__CText(FormatNumber(price) + " " + T("GLORY", "Gloria"), 70, y + 18, priceCol)

            if canBuy:
                self.__CButton(340, y + 5, T("BTN_BUY", "Acquista"), ui.__mem_func__(self.__OnBuy), itemId)

            y += 42
    
    def __LoadRanking(self, rType):
        t = self.theme
        self.currentRankingView = rType
        y = 5

        # =====================================================
        # TITOLO
        # =====================================================
        self.__CText(T("RANK_TITLE", "SALA DELLE LEGGENDE"), 150, y, t["accent"])
        y += 22

        # =====================================================
        # RIGA 1: PERIODO (Daily / Weekly / Total)
        # =====================================================
        self.__CText(T("RANK_PERIOD", "Periodo:"), 5, y + 3, t["text_muted"])
        periods = [(T("RANK_TODAY", "Oggi"), "daily"), (T("RANK_WEEK", "Settimana"), "weekly"), (T("RANK_ALWAYS", "Sempre"), "total")]
        pX = 70
        for pLabel, pKey in periods:
            # Determina se questo periodo è attivo
            if pKey == "daily" and ("daily" in rType):
                isActive = True
            elif pKey == "weekly" and ("weekly" in rType):
                isActive = True
            elif pKey == "total" and ("total" in rType or rType in ["fractures", "chests", "metins"]):
                isActive = True
            else:
                isActive = False
            
            # Costruisce il tipo corretto
            if "kills" in rType:
                targetType = pKey + "_kills"
            elif "points" in rType or rType in ["daily", "weekly", "total"]:
                targetType = pKey + "_points"
            else:
                targetType = rType  # fractures, chests, metins
            
            btn = self.__CButton(pX, y, pLabel, ui.__mem_func__(self.__OnRankPeriod), targetType)
            if isActive:
                btn.Down()
            pX += 85
        y += 28
        
        # =====================================================
        # RIGA 2: CATEGORIA (Gloria / Kills / Fratture / etc)
        # =====================================================
        self.__CText(T("RANK_TYPE", "Tipo:"), 5, y + 3, t["text_muted"])
        categories = [(T("GLORY", "Gloria"), "points"), ("Kills", "kills"), (T("FRACTURES", "Fratture"), "fractures"), (T("CHESTS", "Bauli"), "chests"), ("Metin", "metins")]
        catX = 55
        for catLabel, catKey in categories:
            # Determina il tipo target
            if catKey in ["fractures", "chests", "metins"]:
                targetType = catKey
                isActive = (rType == catKey)
            else:
                # Mantieni il periodo corrente
                if "daily" in rType:
                    targetType = "daily_" + catKey
                elif "weekly" in rType:
                    targetType = "weekly_" + catKey
                else:
                    targetType = "total_" + catKey
                isActive = (catKey in rType)
            
            btn = self.__CButton(catX, y, catLabel, ui.__mem_func__(self.__OnRankSub), targetType)
            if isActive:
                btn.Down()
            catX += 82
        y += 28
        
        self.__CSep(5, y)
        y += 8
        
        # =====================================================
        # LA TUA POSIZIONE
        # =====================================================
        myPos = self.playerData.get("daily_pos", 0) if "daily" in rType else self.playerData.get("weekly_pos", 0)
        myPts = self.playerData.get("total_points", 0)
        myRank = GetRankKey(myPts)
        myTheme = RANK_THEMES[myRank]
        
        self.__CBar(5, y, 420, 24, t["bg_dark"])
        self.__CText(T("RANK_YOU", "TU:"), 12, y + 5, t["text_muted"])
        
        # Badge rank
        self.__CBar(40, y + 3, 20, 16, myTheme["accent"])
        self.__CText(myRank, 45, y + 4, 0xFF000000)
        
        self.__CText(str(self.playerData.get("name", "-")), 68, y + 5, t["accent"])
        
        if myPos > 0:
            self.__CText("#%d" % myPos, 200, y + 5, GOLD_COLOR)
        
        self.__CText(FormatNumber(myPts) + " " + T("GLORY", "Gloria"), 280, y + 5, t["text_value"])
        y += 28
        
        self.__CSep(5, y)
        y += 8
        
        # =====================================================
        # CLASSIFICA TOP 10
        # =====================================================
        data = self.rankingData.get(rType, [])
        if not data:
            # Fallback
            if "points" in rType:
                data = self.rankingData.get("daily_points", self.rankingData.get("daily", []))
            elif "kills" in rType:
                data = self.rankingData.get("daily_kills", [])
        
        if not data:
            self.__CText(T("RANK_NO_DATA", "Nessun dato disponibile."), 130, y + 30, t["text_muted"])
            self.__CText(T("RANK_PLAY_TO_CLIMB", "Gioca per scalare la classifica!"), 120, y + 50, t["text_muted"])
            return

        # Header colonne
        self.__CText("#", 12, y, t["text_muted"])
        self.__CText("Rk", 35, y, t["text_muted"])
        self.__CText(T("RANK_HUNTER", "Cacciatore"), 65, y, t["text_muted"])
        self.__CText(T("RANK_VALUE", "Valore"), 350, y, t["text_muted"])
        y += 16
        
        # =====================================================
        # MOSTRA TUTTI I 10 GIOCATORI
        # =====================================================
        for i in range(min(10, len(data))):
            e = data[i]
            val = e.get("value", e.get("points", 0))
            playerName = e.get("name", "-").replace("+", " ")
            
            # Calcola rank del giocatore dalla gloria
            playerGloria = e.get("points", val) if "kills" not in rType else e.get("points", 0)
            playerRankKey = GetRankKey(playerGloria)
            playerTheme = RANK_THEMES[playerRankKey]
            
            # TOP 3 - Design Premium con medaglie
            if i < 3:
                if i == 0:
                    medalCol, bgCol = GOLD_COLOR, 0x44FFD700
                elif i == 1:
                    medalCol, bgCol = SILVER_COLOR, 0x33C0C0C0
                else:
                    medalCol, bgCol = BRONZE_COLOR, 0x33CD7F32
                
                # Background con bordo colorato
                self.__CBar(5, y, 420, 26, bgCol)
                self.__CBar(5, y, 3, 26, medalCol)
                
                # Posizione
                self.__CText(str(i + 1), 14, y + 5, medalCol)
                
                # Rank badge
                self.__CBar(32, y + 4, 20, 16, playerTheme["accent"])
                self.__CText(playerRankKey, 37, y + 5, 0xFF000000)
                
                # Nome giocatore
                self.__CText(playerName[:20], 58, y + 5, medalCol)
                
                # Valore
                self.__CText(FormatNumber(val), 350, y + 5, t["text_value"])
                
                y += 28
            
            # POSIZIONI 4-10 - Design compatto
            else:
                # Alternanza sfondo
                if i % 2 == 1:
                    self.__CBar(5, y, 420, 20, 0x15FFFFFF)
                
                # Posizione
                self.__CText(str(i + 1), 14, y + 2, t["text_value"])
                
                # Mini rank badge
                self.__CBar(32, y + 1, 18, 14, playerTheme["accent"])
                self.__CText(playerRankKey, 36, y + 1, 0xFF000000)
                
                # Nome
                self.__CText(playerName[:18], 56, y + 2, t["text_value"])
                
                # Valore
                self.__CText(FormatNumber(val), 350, y + 2, t["accent"])
                
                y += 21
    
    def __OnRankPeriod(self, rType):
        """Cambia periodo mantenendo la categoria"""
        self.__ClearContent()
        self.__LoadRanking(rType)
        self.__SavePositions()
        self.__UpdateScroll()
    
    def __LoadAchievements(self):
        t = self.theme
        y = 5

        self.__CText(T("ACHIEV_TITLE", "TRAGUARDI"), 5, y, t["accent"])
        y += 30

        if not self.achievementsData:
            self.__CText(T("ACHIEV_NONE", "Nessun traguardo."), 150, y + 40, t["text_muted"])
            return

        for a in self.achievementsData:
            unlocked = a.get("unlocked", False)
            claimed = a.get("claimed", False)

            bgCol = 0x22888888 if claimed else (0x2200FF00 if unlocked else t["bg_dark"])
            self.__CBar(5, y, 420, 38, bgCol)

            col = 0xFF00FF88 if unlocked else t["text_muted"]
            self.__CText(a.get("name", "").replace("+", " "), 15, y + 3, col)

            prg = a.get("progress", 0)
            req = a.get("requirement", 1)
            pct = min(100, (float(prg) / float(req)) * 100) if req > 0 else 0

            self.__CProgressBar(15, y + 22, 200, 8, pct, col)
            self.__CText("%d / %d" % (min(prg, req), req), 225, y + 19, t["text_value"])

            if unlocked and not claimed:
                btnText = T("BTN_CLAIM_REWARD", "Riscuoti")
            elif claimed:
                btnText = T("BTN_DONE", "Fatto")
            else:
                btnText = T("BTN_VIEW", "Vedi")
            self.__CButton(340, y + 5, btnText, ui.__mem_func__(self.__OnClaim), a.get("id", 0))
            y += 45
    
    def __LoadEvents(self, skipRequest=False):
        """Tab Eventi - MISSIONI GIORNALIERE + Eventi Calendario"""
        t = self.theme
        y = 5

        # HEADER TAB - Spiega che contiene MISSIONI + EVENTI
        self.__CBar(5, y, 420, 40, 0x33FFD700)
        self.__CText(T("EVENTS_HEADER", "MISSIONI & EVENTI"), 160, y + 3, GOLD_COLOR)
        self.__CText(T("EVENTS_CONTAINS", "Questa schermata contiene:"), 125, y + 18, t["text_value"])
        self.__CText(T("EVENTS_DESC", "Missioni Giornaliere + Eventi Programmati 24H"), 65, y + 28, t["text_muted"])
        y += 48

        # Se non abbiamo dati eventi E non stiamo refreshando dopo averli ricevuti
        if not self.eventsData and not skipRequest:
            net.SendChatPacket("/hunter_events_silent")  # Richiedi eventi senza aprire popup

        # =====================================================
        # SEZIONE MISSIONI GIORNALIERE
        # =====================================================
        self.__CBar(5, y, 420, 28, t["bg_dark"])
        self.__CText(T("DAILY_MISSIONS_TITLE", "MISSIONI GIORNALIERE (Reset: 00:05)"), 15, y + 6, 0xFF00CCFF)
        self.__CButton(310, y + 2, T("BTN_OPEN_DETAILS", "Apri Dettagli"), ui.__mem_func__(self.__OnOpenMissions))
        y += 35

        # Tooltip missioni
        self.__CBar(5, y, 420, 30, 0x33444444)
        self.__CText(T("MISSION_AUTO_OPEN", "Il Terminale si apre automaticamente quando fai progresso!"), 30, y + 2, 0xFF88FF88)
        self.__CText(T("MISSION_BONUS_TIP", "Completa TUTTE E 3 per bonus x1.5 Gloria!"), 70, y + 16, GOLD_COLOR)
        y += 35

        # Info missioni disponibili
        missionCount = len(self.missionsData)
        completedCount = sum(1 for m in self.missionsData if m.get("status") == "completed")
        
        if missionCount > 0:
            # Box stato missioni
            self.__CBar(5, y, 420, 85, 0x22000044)
            
            self.__CText(T("MISSION_STATUS", "Stato:") + " %d/%d %s" % (completedCount, missionCount, T("COMPLETE", "complete")), 15, y + 5, t["text_value"])
            
            # Mini preview delle 3 missioni
            for i, m in enumerate(self.missionsData[:3]):
                my = y + 22 + i * 18
                name = m.get("name", "???").replace("+", " ")[:25]
                current = m.get("current", 0)
                target = m.get("target", 1)
                status = m.get("status", "active")
                
                if status == "completed":
                    self.__CText("[OK]", 15, my, 0xFF00FF00)
                else:
                    self.__CText("[...]", 15, my, 0xFFAAAAAA)
                
                self.__CText(name, 50, my, t["text_value"] if status != "completed" else 0xFF888888)
                self.__CText("%d/%d" % (current, target), 280, my, t["accent"])
            
            # Info bonus
            if completedCount == missionCount and missionCount == 3:
                self.__CBar(5, y + 73, 420, 12, 0x4400FF00)
                self.__CText(T("BONUS_ACTIVE", "BONUS x1.5 ATTIVO!"), 180, y + 73, 0xFF00FF00)
            
            y += 92
        else:
            self.__CBar(5, y, 420, 35, 0x22440000)
            self.__CText(T("NO_MISSION_TODAY", "Nessuna missione assegnata oggi."), 80, y + 10, t["text_muted"])
            self.__CText(T("MISSION_ON_LOGIN", "Le missioni vengono assegnate al login."), 75, y + 22, 0xFF888888)
            y += 42

        # Info box bonus/penalita
        self.__CBar(5, y, 205, 35, 0x2200FF00)
        self.__CText(T("ALL_COMPLETE", "Tutte complete:"), 12, y + 4, 0xFF00FF00)
        self.__CText(T("BONUS_50_GLORY", "+50% Gloria Bonus!"), 12, y + 18, 0xFF88FF88)

        self.__CBar(220, y, 205, 35, 0x22FF0000)
        self.__CText(T("NOT_COMPLETE", "Non complete:"), 227, y + 4, 0xFFFF4444)
        self.__CText(T("PENALTY_GLORY", "Penalita' Gloria"), 227, y + 18, 0xFFFF8888)
        y += 42
        
        self.__CSep(5, y)
        y += 15
        
        # =====================================================
        # SEZIONE EVENTI CALENDARIO
        # =====================================================
        self.__CBar(5, y, 420, 28, t["bg_dark"])
        self.__CText(T("EVENTS_TODAY", "EVENTI DEL GIORNO"), 15, y + 6, 0xFFFFAA00)
        self.__CButton(310, y + 2, T("BTN_OPEN_EVENTS", "Apri Eventi"), ui.__mem_func__(self.__OnOpenEvents))
        y += 35

        # Evento in corso?
        ev = self.activeEvent[0] if self.activeEvent[0] != "Nessuno" else None
        if ev:
            self.__CBar(5, y, 420, 40, 0x4400FF00)
            self.__CText(T("EVENT_IN_PROGRESS", "EVENTO IN CORSO!"), 15, y + 5, GOLD_COLOR)
            self.__CText(ev.replace("+", " "), 15, y + 22, GOLD_COLOR)
            y += 48
        else:
            self.__CBar(5, y, 420, 25, 0x22000000)
            self.__CText(T("NO_ACTIVE_EVENT", "Nessun evento attivo al momento"), 120, y + 5, t["text_muted"])
            y += 32

        # Eventi di Oggi (usa eventsData popolato dal server)
        self.__CText(T("SCHEDULED_EVENTS_TODAY", "Eventi Programmati Oggi:"), 5, y, t["accent"])
        y += 20

        if not self.eventsData:
            self.__CText(T("NO_SCHEDULED_EVENT", "Nessun evento programmato oggi."), 120, y + 10, t["text_muted"])
            y += 30
        else:
            # Header
            self.__CBar(5, y, 420, 18, t["bg_dark"])
            self.__CText(T("COL_STATUS", "Stato"), 15, y + 2, t["text_muted"])
            self.__CText(T("COL_EVENT", "Evento"), 60, y + 2, t["text_muted"])
            self.__CText(T("COL_TIME", "Orario"), 280, y + 2, t["text_muted"])
            self.__CText("Rank", 380, y + 2, t["text_muted"])
            y += 20
            
            # Mostra max 8 eventi nel terminale
            for i, e in enumerate(self.eventsData[:8]):
                eventName = e.get("name", "").replace("+", " ")[:22]
                startTime = e.get("start_time", "00:00")
                endTime = e.get("end_time", "00:00")
                status = e.get("status", "upcoming")
                minRank = e.get("min_rank", "E")
                
                if i % 2 == 0:
                    self.__CBar(5, y - 1, 420, 18, 0x11FFFFFF)
                
                # Indicatore stato
                if status == "active":
                    self.__CText("[ON]", 15, y, 0xFF00FF00)
                elif status == "ended":
                    self.__CText("[--]", 15, y, 0xFF666666)
                else:
                    self.__CText("[..]", 15, y, 0xFFAAAA00)
                
                # Nome evento (colore in base a status)
                nameColor = t["text_value"]
                if status == "active":
                    nameColor = GOLD_COLOR
                elif status == "ended":
                    nameColor = 0xFF888888
                self.__CText(eventName, 60, y, nameColor)
                
                # Orario
                self.__CText("%s-%s" % (startTime, endTime), 280, y, t["accent"])
                
                # Rank minimo
                self.__CText(minRank, 390, y, t["text_muted"])
                y += 19
            
            # Se ci sono piu' di 8 eventi, mostra quanti altri
            if len(self.eventsData) > 8:
                self.__CText(T("MORE_EVENTS", "... e altri {COUNT} eventi (clicca 'Apri Eventi')", {"COUNT": len(self.eventsData) - 8}), 100, y, t["text_muted"])
                y += 19

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # INFO RESET
        # =====================================================
        self.__CBar(5, y, 420, 40, t["bg_dark"])
        self.__CText(T("RESET_TIMES", "ORARI RESET:"), 180, y + 4, t["accent"])
        self.__CText(T("RESET_MISSIONS", "Missioni: Ogni giorno alle 00:05"), 50, y + 20, 0xFFAAAAAA)
        self.__CText(T("RESET_EVENTS", "Eventi: In base al calendario"), 230, y + 20, 0xFFAAAAAA)
    
    def __OnOpenMissions(self):
        """Apre direttamente la finestra popup delle missioni giornaliere"""
        self.OpenMissionsPanel()
    
    def __OnOpenEvents(self):
        """Apre direttamente la finestra popup degli eventi programmati"""
        self.OpenEventsPanel()
    
    def __LoadGuide(self):
        t = self.theme
        y = 5
        self.currentGuideTab = getattr(self, 'currentGuideTab', 0)

        # =====================================================
        # HEADER - TITOLO E TABS
        # =====================================================
        self.__CText(T("GUIDE_TITLE", "GUIDA COMPLETA HUNTER SYSTEM"), 100, y, GOLD_COLOR)
        y += 25

        # Tab buttons per sottosezioni - con traduzioni
        guideTabs = [
            (T("GUIDE_TAB_RANKS", "Ranghi"), 0),
            (T("GUIDE_TAB_GLORY", "Gloria"), 1),
            (T("GUIDE_TAB_MISSIONS", "Missioni"), 2),
            (T("GUIDE_TAB_EVENTS", "Eventi"), 3),
            (T("GUIDE_TAB_SHOP", "Shop"), 4),
            (T("GUIDE_TAB_FAQ", "FAQ"), 5)
        ]
        tabX = 5
        for tabName, tabIdx in guideTabs:
            btn = self.__CButton(tabX, y, tabName, ui.__mem_func__(self.__OnGuideTab), tabIdx)
            if self.currentGuideTab == tabIdx:
                btn.Down()
            tabX += 70
        y += 30
        
        self.__CSep(5, y)
        y += 10
        
        # =====================================================
        # CONTENUTO IN BASE AL TAB SELEZIONATO
        # =====================================================
        if self.currentGuideTab == 0:
            y = self.__LoadGuideRanks(y)
        elif self.currentGuideTab == 1:
            y = self.__LoadGuideGlory(y)
        elif self.currentGuideTab == 2:
            y = self.__LoadGuideMissions(y)
        elif self.currentGuideTab == 3:
            y = self.__LoadGuideEvents(y)
        elif self.currentGuideTab == 4:
            y = self.__LoadGuideShop(y)
        else:
            y = self.__LoadGuideFAQ(y)
    
    def __OnGuideTab(self, tabIdx):
        self.currentGuideTab = tabIdx
        self.__ClearContent()
        self.__LoadGuide()
        self.__SavePositions()
        self.__UpdateScroll()
    
    def __LoadGuideRanks(self, y):
        """Guida completa ai ranghi"""
        t = self.theme

        self.__CText(T("GUIDE_RANKS_TITLE", "SISTEMA DEI RANGHI"), 160, y, t["accent"])
        y += 22

        self.__CText(T("GUIDE_RANKS_DESC1", "Il tuo Rango determina il tuo prestigio e i contenuti"), 30, y, t["text_muted"])
        y += 16
        self.__CText(T("GUIDE_RANKS_DESC2", "a cui puoi accedere. Accumula Gloria per salire!"), 50, y, t["text_muted"])
        y += 25
        
        # Lista ranghi con dettagli
        rankDetails = [
            ("E", T("RANK_E_NAME", "Risvegliato"), "0", "2.000", T("RANK_E_DESC", "Hai appena scoperto i tuoi poteri.")),
            ("D", T("RANK_D_NAME", "Apprendista"), "2.000", "10.000", T("RANK_D_DESC", "Inizi a padroneggiare le basi.")),
            ("C", T("RANK_C_NAME", "Cacciatore"), "10.000", "50.000", T("RANK_C_DESC", "Sei un vero Cacciatore ora.")),
            ("B", T("RANK_B_NAME", "Veterano"), "50.000", "150.000", T("RANK_B_DESC", "I mostri tremano al tuo passaggio.")),
            ("A", T("RANK_A_NAME", "Maestro"), "150.000", "500.000", T("RANK_A_DESC", "Solo i migliori arrivano qui.")),
            ("S", T("RANK_S_NAME", "Leggenda"), "500.000", "1.500.000", T("RANK_S_DESC", "Il tuo nome e' conosciuto ovunque.")),
            ("N", T("RANK_N_NAME", "Monarca Nazionale"), "1.500.000", "MAX", T("RANK_N_DESC", "Hai raggiunto l'apice del potere!")),
        ]

        for key, title, minPts, maxPts, desc in rankDetails:
            rt = RANK_THEMES[key]

            # Box rank
            self.__CBar(5, y, 420, 45, rt["bg_dark"])
            self.__CBar(5, y, 5, 45, rt["accent"])

            # Badge e titolo
            self.__CBar(15, y + 5, 25, 18, rt["accent"])
            self.__CText(key, 22, y + 6, 0xFF000000)
            self.__CText(title, 50, y + 5, rt["accent"])

            # Range punti
            self.__CText("%s - %s %s" % (minPts, maxPts, T("GLORY", "Gloria")), 200, y + 5, rt["text_value"])
            
            # Descrizione
            self.__CText(desc, 15, y + 27, rt["text_muted"])
            
            y += 50
        
        return y
    
    def __LoadGuideGlory(self, y):
        """Guida su come guadagnare Gloria"""
        t = self.theme

        # =====================================================
        # GLORIA
        # =====================================================
        self.__CText(T("GUIDE_GLORY_TITLE", "COME GUADAGNARE GLORIA"), 140, y, GOLD_COLOR)
        y += 25

        # IMPORTANTE: Spiegazione mostri normali NON danno Gloria
        self.__CBar(5, y, 420, 55, 0x44FF0000)
        self.__CText(T("WARNING", "ATTENZIONE!"), 180, y + 5, 0xFFFF0000)
        self.__CText(T("GLORY_WARNING1", "I mostri, metin e boss NORMALI NON danno Gloria!"), 30, y + 22, 0xFFFFAAAA)
        self.__CText(T("GLORY_WARNING2", "Ottieni Gloria SOLO da:"), 140, y + 37, 0xFFFFFFFF)
        y += 62

        gloryMethods = [
            (T("GLORY_METHOD_FRACTURES", "Fratture Dimensionali"), "+50-500", T("GLORY_METHOD_FRACTURES_DESC", "Boss/Metin DENTRO le fratture (base pts)")),
            (T("GLORY_METHOD_MISSIONS", "Missioni Giornaliere"), "+50-3000", T("GLORY_METHOD_MISSIONS_DESC", "3 missioni al giorno (reward scala col Rank)")),
            (T("GLORY_METHOD_EMERGENCY", "Emergency Quest"), "+150-1200", T("GLORY_METHOD_EMERGENCY_DESC", "40% chance dopo ~500 kill normali")),
            (T("GLORY_METHOD_EVENTS", "Eventi Programmati"), "+100-2000", T("GLORY_METHOD_EVENTS_DESC", "Glory Rush, Metin Frenzy, Boss Massacre...")),
            (T("GLORY_METHOD_STREAK", "Streak Login"), "+5/10/20%", T("GLORY_METHOD_STREAK_DESC", "3gg=+5%, 7gg=+10%, 30gg=+20% Gloria")),
            (T("GLORY_METHOD_CHESTS", "Bauli Hunter"), "+20-100", T("GLORY_METHOD_CHESTS_DESC", "Bauli spawn nelle mappe normali")),
            (T("GLORY_METHOD_SPEEDKILL", "Speed Kill Bonus"), "x2 reward", T("GLORY_METHOD_SPEEDKILL_DESC", "Boss 60s, Metin 300s = doppia Gloria")),
        ]

        for method, reward, desc in gloryMethods:
            self.__CBar(5, y, 420, 35, t["bg_dark"])
            self.__CText(method, 15, y + 3, t["text_value"])
            self.__CText(reward, 200, y + 3, 0xFF00FF00)
            self.__CText(desc, 15, y + 18, t["text_muted"])
            y += 38

        y += 15
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # GLORIA SPENDIBILE
        # =====================================================
        self.__CText(T("GLORY_SPENDABLE_TITLE", "GLORIA SPENDIBILE (SHOP)"), 130, y, 0xFFFFA500)
        y += 25

        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("GLORY_SPLIT_INFO", "La Gloria e' divisa in due contatori:"), 115, y + 5, t["text_value"])
        self.__CText(T("GLORY_TOTAL_INFO", "- Gloria Totale: determina il tuo RANK (non scende mai)"), 30, y + 22, GOLD_COLOR)
        self.__CText(T("GLORY_SPEND_INFO", "- Gloria Spendibile: usala nello SHOP senza perdere rank!"), 15, y + 38, 0xFF00FF00)
        self.__CText(T("GLORY_BOTH_INFO", "Ogni Gloria guadagnata incrementa ENTRAMBI i contatori!"), 35, y + 58, t["text_muted"])
        y += 90

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # GLORIA IN PARTY
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x3300FFFF)
        self.__CText(T("GLORY_PARTY_TITLE", "GLORIA IN PARTY"), 160, y + 5, 0xFF00FFFF)
        y += 38

        self.__CBar(5, y, 420, 75, t["bg_dark"])
        self.__CText(T("GLORY_PARTY_INFO1", "Quando giochi in GRUPPO (party), la Gloria va a"), 70, y + 5, t["text_value"])
        self.__CText(T("GLORY_PARTY_INFO2", "CHI COMPIE L'AZIONE!"), 145, y + 20, GOLD_COLOR)
        self.__CText(T("GLORY_PARTY_INFO3", "Bauli: chi apre | Boss/Metin: chi uccide | Fratture: chi conquista"), 15, y + 37, 0xFF00FF00)
        self.__CText(T("GLORY_PARTY_INFO4", "Il Power Rank serve per FORZARE fratture, non per dividere Gloria."), 20, y + 55, t["text_muted"])
        y += 83

        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 20

        partySteps = [
            T("PARTY_STEP_1", "1. Boss/Metin ucciso = Gloria va al KILLER"),
            T("PARTY_STEP_2", "2. Baule aperto = Gloria va a CHI APRE"),
            T("PARTY_STEP_3", "3. Frattura conquistata = Gloria va al CONQUISTATORE"),
            T("PARTY_STEP_4", "4. Si applicano i bonus personali (Streak, Focus, Evento...)"),
            T("PARTY_STEP_5", "5. Si applicano i malus personali (Trial -50%)"),
            T("PARTY_STEP_6", "6. Gloria finale assegnata!"),
        ]

        for step in partySteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 16
        y += 10

        # Info importante
        self.__CBar(5, y, 420, 70, 0x33FFD700)
        self.__CText(T("POWER_RANK_TITLE", "POWER RANK - A COSA SERVE?"), 130, y + 5, GOLD_COLOR)
        self.__CText(T("POWER_RANK_INFO1", "Il Power Rank del party serve per FORZARE fratture!"), 50, y + 22, t["text_value"])
        self.__CText(T("POWER_RANK_INFO2", "Fratture B/A/S/N richiedono tot Power Rank per entrare"), 45, y + 38, t["text_value"])
        self.__CText(T("POWER_RANK_INFO3", "se non hai abbastanza Gloria personale."), 100, y + 52, t["text_muted"])
        y += 80

        # Bonus/Malus personali
        self.__CBar(5, y, 420, 85, t["bg_dark"])
        self.__CText(T("BONUS_MALUS_TITLE", "BONUS/MALUS PERSONALI:"), 145, y + 5, t["accent"])
        self.__CText(T("BONUS_STREAK", "+ Streak Login: +5%/+10%/+20% (3/7/30 giorni)"), 15, y + 22, 0xFF00FF00)
        self.__CText(T("BONUS_FOCUS", "+ Focus Hunter: +20% (item consumabile)"), 15, y + 36, 0xFF00FF00)
        self.__CText(T("BONUS_FRACTURE", "+ Fracture Bonus: +50% (missioni 3/3 complete)"), 15, y + 50, 0xFF00FF00)
        self.__CText(T("MALUS_TRIAL", "- Trial Attivo: -50% (fino a completamento prova)"), 15, y + 66, 0xFFFF6666)
        y += 95

        # =====================================================
        # DETTAGLIO GLORIA - SYSCHAT
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33AAAAFF)
        self.__CText(T("GLORY_DETAIL_TITLE", "DETTAGLIO GLORIA IN CHAT"), 140, y + 5, 0xFFAAAAFF)
        y += 38

        self.__CBar(5, y, 420, 100, t["bg_dark"])
        self.__CText(T("GLORY_DETAIL_INFO", "Quando uccidi Boss, Metin o apri Bauli, vedrai in chat:"), 40, y + 5, t["text_value"])
        self.__CText("========== DETTAGLIO GLORIA =========", 80, y + 22, 0xFF888888)
        self.__CText("BOSS: Nome Del Boss", 100, y + 36, t["text_value"])
        self.__CText(T("GLORY_BASE", "Gloria Base:") + " 500", 100, y + 50, t["text_muted"])
        self.__CText("Streak Bonus (+10%): +50", 100, y + 64, 0xFF00FF00)
        self.__CText(">>> TOTALE: +550 Gloria <<<", 100, y + 78, GOLD_COLOR)
        y += 110

        self.__CText(T("GLORY_DETAIL_TIP", "Cosi' puoi verificare TUTTI i bonus/malus applicati!"), 55, y, 0xFF00CCFF)
        y += 25

        return y
    
    def __LoadGuideMissions(self, y):
        """Guida alle missioni giornaliere"""
        t = self.theme

        self.__CText(T("GUIDE_MISSIONS_TITLE", "MISSIONI GIORNALIERE"), 150, y, t["accent"])
        y += 25

        # Pulsante per aprire le missioni
        self.__CBar(5, y, 420, 35, 0x3300CCFF)
        self.__CText(T("WANT_SEE_MISSIONS", "Vuoi vedere le tue missioni attuali?"), 100, y + 3, t["text_value"])
        self.__CButton(150, y + 18, T("BTN_OPEN_DAILY_MISSIONS", "APRI MISSIONI GIORNALIERE"), ui.__mem_func__(self.__OnOpenMissions))
        y += 45

        # Intro
        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("MISSIONS_INTRO1", "Ogni giorno alle 00:05 ricevi 3 nuove missioni."), 50, y + 5, t["text_value"])
        self.__CText(T("MISSIONS_INTRO2", "Le missioni sono basate sul tuo Rank attuale."), 60, y + 20, t["text_muted"])

        self.__CText(T("WHERE_TO_SEE", "DOVE VEDERLE:"), 170, y + 40, 0xFFFFAA00)
        self.__CText(T("MISSIONS_HOW1", "1. Scrivi /hunter_missions in chat"), 80, y + 55, 0xFF00CCFF)
        self.__CText(T("MISSIONS_HOW2", "2. Premi N > Tab Eventi > Apri Dettagli"), 75, y + 68, 0xFF00CCFF)
        y += 90

        # Tipi di missioni (quelli effettivi nel DB)
        self.__CText(T("MISSION_TYPES_TITLE", "TIPI DI MISSIONI:"), 5, y, t["accent"])
        y += 22

        missionTypes = [
            ("kill_mob", T("MISSION_TYPE_KILL_MOB", "Uccidi Mostri"), T("MISSION_TYPE_KILL_MOB_DESC", "Elimina un certo numero di mob (vnum specifico o qualsiasi)")),
            ("kill_boss", T("MISSION_TYPE_KILL_BOSS", "Caccia al Boss"), T("MISSION_TYPE_KILL_BOSS_DESC", "Sconfiggi boss nel mondo di gioco")),
            ("kill_metin", T("MISSION_TYPE_KILL_METIN", "Distruggi Metin"), T("MISSION_TYPE_KILL_METIN_DESC", "Distruggi pietre metin nelle mappe")),
            ("seal_fracture", T("MISSION_TYPE_SEAL_FRACTURE", "Sigilla Frattura"), T("MISSION_TYPE_SEAL_FRACTURE_DESC", "Chiudi le fratture dimensionali (rank A+)")),
        ]

        for mType, name, desc in missionTypes:
            self.__CBar(5, y, 420, 32, t["bg_dark"])
            self.__CText("- %s" % name, 15, y + 3, t["text_value"])
            self.__CText(desc, 20, y + 17, t["text_muted"])
            y += 34

        y += 10
        self.__CSep(5, y)
        y += 15

        # Come funziona
        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        steps = [
            T("MISSION_STEP_1", "1. Al login ricevi automaticamente 3 missioni"),
            T("MISSION_STEP_2", "2. Uccidi mob/boss/metin per fare progresso"),
            T("MISSION_STEP_3", "3. Un popup ti mostra il progresso (3 secondi)"),
            T("MISSION_STEP_4", "4. Al completamento ricevi Gloria + effetto verde"),
            T("MISSION_STEP_5", "5. Se completi TUTTE E 3: Bonus x1.5 + effetto oro!"),
        ]

        for step in steps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 15

        # Penalita
        self.__CBar(5, y, 420, 70, 0x33FF0000)
        self.__CText(T("PENALTY_SYSTEM", "SISTEMA PENALITA'"), 160, y + 5, 0xFFFF4444)
        self.__CText(T("PENALTY_INFO1", "Missioni NON completate entro mezzanotte:"), 90, y + 22, t["text_value"])
        self.__CText(T("PENALTY_INFO2", "= Perdi Gloria TOTALE (non spendibile)!"), 85, y + 38, 0xFFFF6666)
        self.__CText(T("PENALTY_INFO3", "La missione viene segnata come 'failed' nel DB."), 60, y + 53, t["text_muted"])
        y += 80

        # Bonus completamento
        self.__CBar(5, y, 420, 80, 0x3300FF00)
        self.__CText(T("BONUS_ALL_COMPLETE_TITLE", "BONUS TUTTE COMPLETE"), 155, y + 5, 0xFF00FF00)
        self.__CText(T("BONUS_ALL_COMPLETE_INFO", "Completa tutte e 3 le missioni:"), 130, y + 22, 0xFF88FF88)
        self.__CText(T("BONUS_ALL_1", "1. +50% Gloria extra (sulla somma ricompense missioni)"), 30, y + 37, t["text_value"])
        self.__CText(T("BONUS_ALL_2", "2. BONUS FRATTURE: +50% Gloria da Boss/Metin fratture!"), 15, y + 52, 0xFFFFD700)
        self.__CText(T("BONUS_ALL_3", "Il bonus e' visibile nel syschat dettagliato."), 80, y + 67, t["text_muted"])
        y += 90

        y += 15
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # EMERGENCY QUEST - Sezione dedicata
        # =====================================================
        self.__CBar(5, y, 420, 35, 0x33FF6600)
        self.__CText(T("EMERGENCY_QUEST_TITLE", "EMERGENCY QUEST"), 160, y + 5, 0xFFFF6600)
        self.__CText(T("EMERGENCY_QUEST_SUBTITLE", "MISSIONI SPECIALI A TEMPO - PREMI MASSIMI!"), 80, y + 22, 0xFFFFAA00)
        y += 43

        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        emergencySteps = [
            T("EMERG_STEP_1", "1. Spawn RANDOM dopo aver ucciso ~500 mob normali"),
            T("EMERG_STEP_2", "2. 40% chance Emergency, 60% chance Frattura"),
            T("EMERG_STEP_3", "3. Tempo limitato: 60-180 secondi per completare!"),
            T("EMERG_STEP_4", "4. Obiettivi: 30-250 kill a seconda della difficolta'"),
            T("EMERG_STEP_5", "5. Premi: 150-1200 Gloria + item bonus"),
            T("EMERG_STEP_6", "6. Se fallisci, non c'e' penalita' (solo opportunita' persa)"),
        ]

        for step in emergencySteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 10

        # Difficoltà Emergency
        self.__CText(T("DIFFICULTY_LEVELS", "LIVELLI DI DIFFICOLTA':"), 5, y, t["accent"])
        y += 22

        emergencyLevels = [
            ("EASY", 0xFF00FF00, T("EMERG_EASY_REQ", "30 kill in 60s"), "+150 Gloria"),
            ("NORMAL", 0xFF00CCFF, T("EMERG_NORMAL_REQ", "2-3 Boss/Metin in 120-150s"), "+350-400 Gloria"),
            ("HARD", 0xFFFFAA00, T("EMERG_HARD_REQ", "60 kill/60s o 5 Metin/180s"), "+300-500 Gloria"),
            ("EXTREME", 0xFFFF6600, T("EMERG_EXTREME_REQ", "120 kill/90s o 3 Boss/180s"), "+600-1000 Gloria"),
            ("GOD_MODE", 0xFFFF0000, T("EMERG_GODMODE_REQ", "250 kill in 180s"), "+1200 Gloria"),
        ]

        for diff, color, req, reward in emergencyLevels:
            self.__CBar(5, y, 420, 22, t["bg_dark"])
            self.__CBar(5, y, 4, 22, color)
            self.__CText(diff, 15, y + 3, color)
            self.__CText(req, 150, y + 3, t["text_value"])
            self.__CText(reward, 290, y + 3, 0xFF00FF00)
            y += 24

        y += 10

        # Speed Kill bonus per Emergency
        self.__CBar(5, y, 420, 50, 0x3300FFFF)
        self.__CText(T("SPEEDKILL_BONUS_TITLE", "SPEED KILL BONUS"), 165, y + 5, 0xFF00FFFF)
        self.__CText(T("SPEEDKILL_BOSS", "Boss: Uccidi entro 60 secondi = x2 Punti Gloria!"), 50, y + 22, t["text_value"])
        self.__CText(T("SPEEDKILL_METIN", "Metin: Distruggi entro 300 secondi = x2 Punti Gloria!"), 40, y + 36, t["text_value"])
        y += 60

        y += 15
        self.__CSep(5, y)
        y += 15

        # Ricompense per rank
        self.__CText(T("REWARDS_BY_RANK", "RICOMPENSE PER RANK:"), 5, y, t["accent"])
        y += 22

        rankRewards = [
            ("E", "15-50", "5-15"),
            ("D", "40-100", "12-30"),
            ("C", "80-200", "25-60"),
            ("B", "150-400", "45-120"),
            ("A", "300-800", "90-240"),
            ("S", "600-1500", "180-450"),
            ("N", "1200-3000", "350-900"),
        ]

        self.__CText("Rank    Reward Gloria    " + T("PENALTY", "Penalita'"), 60, y, t["text_muted"])
        y += 18

        for rank, reward, penalty in rankRewards:
            color = RANK_COLORS.get(rank, t["text_value"])
            self.__CText("%s" % rank, 80, y, color)
            self.__CText("%s" % reward, 140, y, 0xFF00FF00)
            self.__CText("%s" % penalty, 260, y, 0xFFFF6666)
            y += 16

        y += 15

        return y
    
    def __LoadGuideEvents(self, y):
        """Guida agli eventi programmati - Sistema 24H"""
        t = self.theme

        self.__CText(T("GUIDE_EVENTS_TITLE", "EVENTI PROGRAMMATI 24H"), 145, y, t["accent"])
        y += 25

        # Pulsante per aprire gli eventi
        self.__CBar(5, y, 420, 35, 0x33FFD700)
        self.__CText(T("WANT_SEE_EVENTS", "Vuoi vedere gli eventi di oggi?"), 120, y + 3, t["text_value"])
        self.__CButton(150, y + 18, T("BTN_OPEN_TODAY_EVENTS", "APRI EVENTI DEL GIORNO"), ui.__mem_func__(self.__OnOpenEvents))
        y += 45

        # Intro
        self.__CBar(5, y, 420, 55, t["bg_dark"])
        self.__CText(T("EVENTS_INTRO1", "Gli eventi si attivano automaticamente ad orari"), 70, y + 5, t["text_muted"])
        self.__CText(T("EVENTS_INTRO2", "prestabiliti. L'iscrizione e' AUTOMATICA!"), 100, y + 20, t["text_muted"])
        self.__CText(T("EVENTS_INTRO3", "Clicca 'Apri Eventi' per vedere quelli di oggi!"), 65, y + 37, 0xFF00CCFF)
        y += 65

        # =====================================================
        # ISCRIZIONE AUTOMATICA - IMPORTANTE!
        # =====================================================
        self.__CBar(5, y, 420, 80, 0x3300FF00)
        self.__CText(T("AUTO_REGISTRATION", "ISCRIZIONE AUTOMATICA"), 155, y + 5, 0xFF00FF00)
        self.__CText(T("AUTO_REG_INFO1", "NON devi cliccare nessun pulsante!"), 110, y + 22, t["text_value"])
        self.__CText(T("AUTO_REG_INFO2", "Conquista fratture, uccidi boss, metin o mob"), 70, y + 38, t["text_value"])
        self.__CText(T("AUTO_REG_INFO3", "per iscriverti automaticamente all'evento!"), 80, y + 54, t["text_value"])
        self.__CText(T("AUTO_REG_INFO4", "Vedrai: [EVENTO] Sei iscritto all'estrazione finale!"), 50, y + 70, 0xFFFFD700)
        y += 90

        # Tipi di eventi
        self.__CText(T("EVENT_TYPES_TITLE", "TIPI DI EVENTO:"), 5, y, t["accent"])
        y += 22

        eventTypes = [
            ("GLORY RUSH", 0xFFFFD700, T("EVENT_DESC_GLORY_RUSH", "Gloria x2 per ogni kill! Sorteggio finale.")),
            (T("EVENT_FRACTURE_EVENING", "FRATTURA SERA"), 0xFF9900FF, T("EVENT_DESC_FRACTURE_EVENING", "PRIMO a conquistare frattura VINCE!")),
            (T("EVENT_BOSS_HUNT", "CACCIA BOSS"), 0xFFFF0000, T("EVENT_DESC_BOSS_HUNT", "PRIMO a uccidere un boss VINCE!")),
            ("RIFT HUNT", 0xFF9900FF, T("EVENT_DESC_RIFT_HUNT", "Fratture +50% spawn. Sorteggio finale.")),
            ("BOSS MASSACRE", 0xFFFF6600, T("EVENT_DESC_BOSS_MASSACRE", "Boss Gloria +50%. Sorteggio finale.")),
            ("METIN FRENZY", 0xFFFF6600, T("EVENT_DESC_METIN_FRENZY", "Metin Bonus +50%. Sorteggio finale.")),
            ("DOUBLE SPAWN", 0xFF00FF00, T("EVENT_DESC_DOUBLE_SPAWN", "Spawn Elite x2. Sorteggio finale.")),
        ]

        for name, color, desc in eventTypes:
            self.__CBar(5, y, 420, 22, t["bg_dark"])
            self.__CBar(5, y, 4, 22, color)
            self.__CText(name, 15, y + 3, color)
            self.__CText(desc, 140, y + 3, t["text_muted"])
            y += 24

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # EVENTI "PRIMO VINCE"
        # =====================================================
        self.__CBar(5, y, 420, 95, 0x33FF4444)
        self.__CText(T("FIRST_WINS_TITLE", "EVENTI 'PRIMO VINCE'"), 160, y + 5, 0xFFFF4444)
        self.__CText(T("FIRST_RIFT_TITLE", "FRATTURA DELLA SERA (first_rift):"), 15, y + 22, 0xFFFFD700)
        self.__CText(T("FIRST_RIFT_DESC", "Il PRIMO giocatore che conquista una frattura VINCE!"), 25, y + 38, t["text_value"])
        self.__CText(T("FIRST_BOSS_TITLE", "CACCIA AL BOSS (first_boss):"), 15, y + 55, 0xFFFFD700)
        self.__CText(T("FIRST_BOSS_DESC", "Il PRIMO giocatore che uccide un boss VINCE!"), 25, y + 71, t["text_value"])
        self.__CText(T("FIRST_PRIZE_INFO", "Premio immediato + annuncio globale!"), 80, y + 87, 0xFF00FF00)
        y += 105

        # Come funziona
        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        steps = [
            T("EVENT_STEP_1", "1. Gli eventi si attivano automaticamente"),
            T("EVENT_STEP_2", "2. Fai azioni che danno Gloria = sei ISCRITTO!"),
            T("EVENT_STEP_3", "3. Nella lista eventi vedrai [ISCRITTO] in verde"),
            T("EVENT_STEP_4", "4. Per GLORY RUSH: sorteggio casuale a fine evento"),
            T("EVENT_STEP_5", "5. Per PRIMO VINCE: chi fa l'azione per primo vince!"),
            T("EVENT_STEP_6", "6. Il vincitore riceve il PREMIO FINALE!"),
        ]

        for step in steps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 15

        # Box informativo PREMI
        self.__CBar(5, y, 420, 70, 0x33FFD700)
        self.__CText(T("EVENT_PRIZES_TITLE", "PREMI EVENTO"), 180, y + 5, GOLD_COLOR)
        self.__CText(T("EVENT_PRIZE_PARTICIPATION", "Partecipazione: +50 Gloria base (varia per evento)"), 60, y + 22, t["text_value"])
        self.__CText(T("EVENT_PRIZE_WINNER", "Sorteggio/Primo: +200-500 Gloria BONUS!"), 80, y + 38, 0xFF00FF00)
        self.__CText(T("EVENT_PRIZE_CHECK", "Controlla la lista eventi per vedere i premi esatti!"), 55, y + 54, t["text_muted"])
        y += 80


        # =============================
        # EVENTI PROGRAMMATI DETTAGLIATI
        # =============================
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CText(T("SCHEDULED_EVENTS_LIST", "LISTA COMPLETA EVENTI PROGRAMMATI"), 70, y + 5, GOLD_COLOR)
        y += 38

        # allScheduledEvents deve essere una lista di dict con chiavi:
        # event_name, event_type, event_desc, start_hour, start_minute, duration_minutes, days_active, min_rank, reward_glory_base, reward_glory_winner, color_scheme, priority
        global allScheduledEvents
        if 'allScheduledEvents' in globals() and allScheduledEvents:
            # Header
            self.__CBar(5, y, 420, 22, t["bg_dark"])
            self.__CText(T("COL_TIME", "Orario"), 10, y + 3, t["text_muted"])
            self.__CText(T("COL_EVENT_NAME", "Nome Evento"), 70, y + 3, t["text_muted"])
            self.__CText(T("COL_TYPE", "Tipo"), 220, y + 3, t["text_muted"])
            self.__CText("Rank", 280, y + 3, t["text_muted"])
            self.__CText(T("COL_PRIZE", "Premio"), 330, y + 3, t["text_muted"])
            y += 22
            for ev in allScheduledEvents:
                # Orario
                start = "%02d:%02d" % (ev.get("start_hour",0), ev.get("start_minute",0))
                durata = ev.get("duration_minutes", 0)
                giorni = ev.get("days_active", "1,2,3,4,5,6,7")
                giorni_txt = T("ALL_DAYS", "Tutti") if giorni == "1,2,3,4,5,6,7" else giorni
                # Colore
                color_map = {"GOLD":0xFFFFD700, "PURPLE":0xFF9900FF, "RED":0xFFFF0000, "ORANGE":0xFFFF6600}
                bar_col = color_map.get(ev.get("color_scheme","GOLD"), 0xFFCCCCCC)
                self.__CBar(5, y, 420, 22, bar_col)
                # Nome evento
                self.__CText("%s-%dm" % (start, durata), 10, y + 3, t["text_value"])
                self.__CText(ev.get("event_name","?"), 70, y + 3, GOLD_COLOR)
                self.__CText(ev.get("event_type","?"), 220, y + 3, t["accent"])
                self.__CText(ev.get("min_rank","E"), 280, y + 3, t["text_value"])
                self.__CText("%d/%d" % (ev.get("reward_glory_base",0), ev.get("reward_glory_winner",0)), 330, y + 3, 0xFF00FF00)
                y += 22
                # Descrizione
                self.__CText(ev.get("event_desc",""), 20, y, t["text_muted"])
                y += 18
                # Giorni attivi
                self.__CText(T("DAYS", "Giorni:") + " %s | " + T("PRIORITY", "Priorità:") + " %s" % (giorni_txt, str(ev.get("priority",5))), 20, y, t["text_muted"])
                y += 18
                y += 2
        else:
            self.__CText(T("NO_SCHEDULED_EVENTS", "Nessun evento programmato trovato."), 60, y + 5, t["text_muted"])
            y += 28

        y += 10
        self.__CSep(5, y)
        y += 15
        # ...existing code...

        # =====================================================
        # FRATTURE DIMENSIONALI
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x339900FF)
        self.__CText(T("FRACTURES_TITLE", "FRATTURE DIMENSIONALI"), 145, y + 5, 0xFF9900FF)
        self.__CText(T("FRACTURES_SUBTITLE", "Portali con mob potenti - Alta ricompensa!"), 75, y + 20, t["text_muted"])
        y += 38

        self.__CText(T("HOW_THEY_WORK", "COME FUNZIONANO:"), 5, y, t["accent"])
        y += 22

        fractureSteps = [
            T("FRACT_STEP_1", "1. Dopo ~500 kill normali: 65% chance spawna una Frattura"),
            T("FRACT_STEP_2", "2. Clicca sulla Frattura per tentare di aprirla"),
            T("FRACT_STEP_3", "3. Se non hai Gloria: usa il POWER RANK del Party!"),
            T("FRACT_STEP_4", "4. Difendi la Frattura dalle ondate di mob nemici"),
            T("FRACT_STEP_5", "5. Vinci la difesa = sblocchi il portale per 5 minuti"),
            T("FRACT_STEP_6", "6. Tocca il portale per evocare Boss/Metin Elite!"),
        ]

        for step in fractureSteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18
        y += 10

        self.__CText(T("FRACTURE_RANKS_TITLE", "RANK FRATTURE (da DB):"), 5, y, t["accent"])
        y += 22

        self.__CBar(5, y, 420, 55, t["bg_dark"])
        self.__CText(T("FRACTURE_REQ_INFO", "Ogni Frattura ha un requisito di Gloria Totale!"), 75, y + 5, GOLD_COLOR)
        self.__CText("E-Rank: 0 | D: 2K | C: 10K | B: 50K | A: 150K | S: 500K | N: 1.5M", 15, y + 22, t["text_value"])
        self.__CText("Spawn chance: E=35% | D=25% | C=15% | B=10% | A=8% | S=5% | N=2%", 15, y + 38, t["text_muted"])
        y += 60

        # Power Rank System
        y += 5
        self.__CBar(5, y, 420, 115, 0x33FF6600)
        self.__CText(T("FORCE_WITHOUT_GLORY", "FORZARE SENZA GLORIA"), 155, y + 5, 0xFFFF6600)
        self.__CText(T("FORCE_INFO", "Non hai la Gloria richiesta? Puoi forzare!"), 65, y + 22, t["text_value"])
        y += 40

        self.__CText(T("FRACTURES_EDC", "FRATTURE E / D / C:"), 5, y, 0xFF00FF00)
        self.__CText(T("FRACTURES_EDC_REQ", "Party di 4+ membri vicini"), 155, y, t["text_value"])
        y += 18

        self.__CText(T("FRACTURES_BASN", "FRATTURE B / A / S / N:"), 5, y, 0xFFFFAA00)
        self.__CText(T("FRACTURES_BASN_REQ", "Sistema POWER RANK"), 175, y, t["text_value"])
        y += 18

        self.__CText(T("POWER_RANK_SUM", "Il Power Rank e' la somma della forza di tutti i membri"), 40, y, t["text_muted"])
        y += 25

        # Power Rank Values
        self.__CBar(5, y, 420, 45, t["bg_dark"])
        self.__CText(T("POWER_RANK_VALUES", "VALORE POWER RANK PER GRADO HUNTER:"), 90, y + 5, t["accent"])
        self.__CText("E=1 | D=5 | C=15 | B=40 | A=80 | S=150 | N=250 " + T("POINTS", "punti"), 55, y + 25, t["text_value"])
        y += 55

        # Power Rank Requirements
        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("POWER_RANK_REQ", "REQUISITI POWER RANK FRATTURE:"), 110, y + 5, 0xFFFFAA00)
        self.__CText("B-Rank: 100 PR (es: 3 B = 120, o 1 A + 1 B = 120)", 45, y + 22, t["text_value"])
        self.__CText("A-Rank: 200 PR (es: 2 A + 1 B = 200, o 1 S + 1 B = 190)", 30, y + 38, t["text_value"])
        self.__CText("S-Rank: 350 PR (es: 1 N + 1 S = 400, o 3 S = 450)", 45, y + 52, t["text_value"])
        self.__CText("N-Rank: 500 PR (es: 2 N = 500, o 1 N + 2 S = 550)", 45, y + 66, t["text_value"])
        y += 90

        self.__CBar(5, y, 420, 45, 0x33FFD700)
        self.__CText(T("WARNING", "ATTENZIONE!"), 180, y + 5, GOLD_COLOR)
        self.__CText(T("FRACTURE_WARNING1", "Aprire una frattura rivela la tua posizione a TUTTI!"), 50, y + 22, 0xFFFF6666)
        self.__CText(T("FRACTURE_WARNING2", "Altri player possono rubarti il Boss! Preparati a difenderlo."), 35, y + 34, t["text_value"])
        y += 55

        return y
    
    def __LoadGuideShop(self, y):
        """Guida allo shop Hunter"""
        t = self.theme

        self.__CText(T("GUIDE_SHOP_TITLE", "MERCANTE HUNTER"), 165, y, 0xFFFFA500)
        y += 25

        # Intro
        self.__CText(T("SHOP_GUIDE_INTRO", "Usa la tua Gloria Spendibile per acquistare oggetti!"), 60, y, t["text_muted"])
        y += 25

        # Come funziona la Gloria Spendibile
        self.__CBar(5, y, 420, 65, t["bg_dark"])
        self.__CText(T("SPENDABLE_GLORY_TITLE", "GLORIA SPENDIBILE:"), 155, y + 5, 0xFFFFA500)
        self.__CText(T("SHOP_INFO1", "Ogni Gloria guadagnata e' anche Gloria Spendibile."), 55, y + 22, t["text_value"])
        self.__CText(T("SHOP_INFO2", "Puoi spenderla nello Shop senza perdere il Rank!"), 60, y + 36, t["text_value"])
        self.__CText(T("SHOP_INFO3", "La Gloria Totale determina il Rank, quella Spendibile lo Shop."), 25, y + 50, t["text_muted"])
        y += 75

        # Categorie shop
        self.__CText(T("SHOP_CATEGORIES_TITLE", "CATEGORIE DISPONIBILI:"), 5, y, t["accent"])
        y += 22

        categories = [
            (T("SHOP_CAT_CONSUMABLES", "Consumabili"), T("SHOP_CAT_CONSUMABLES_DESC", "Pozioni, buff temporanei, boost EXP")),
            (T("SHOP_CAT_EQUIPMENT", "Equipaggiamento"), T("SHOP_CAT_EQUIPMENT_DESC", "Armi e armature esclusive Hunter")),
            (T("SHOP_CAT_COSMETICS", "Cosmetici"), T("SHOP_CAT_COSMETICS_DESC", "Titoli, aure, effetti visivi")),
            (T("SHOP_CAT_MATERIALS", "Materiali"), T("SHOP_CAT_MATERIALS_DESC", "Pietre, upgrade, crafting")),
            (T("SHOP_CAT_SPECIAL", "Speciali"), T("SHOP_CAT_SPECIAL_DESC", "Item rari a rotazione settimanale")),
        ]

        for cat, desc in categories:
            self.__CBar(5, y, 420, 26, t["bg_dark"])
            self.__CText(cat, 15, y + 5, 0xFFFFA500)
            self.__CText(desc, 130, y + 5, t["text_muted"])
            y += 28

        y += 15
        self.__CSep(5, y)
        y += 15

        # Consigli
        self.__CText(T("SHOP_TIPS_TITLE", "CONSIGLI ACQUISTI:"), 5, y, t["accent"])
        y += 22

        tips = [
            T("SHOP_TIP_1", "- Non sprecare Gloria Spendibile su consumabili comuni"),
            T("SHOP_TIP_2", "- Gli item speciali cambiano ogni settimana"),
            T("SHOP_TIP_3", "- Risparmia per equipaggiamento di alto rank"),
            T("SHOP_TIP_4", "- I cosmetici sono permanenti, buon investimento!"),
        ]

        for tip in tips:
            self.__CText(tip, 15, y, t["text_value"])
            y += 18

        return y
    
    def __LoadGuideFAQ(self, y):
        """FAQ e domande frequenti"""
        t = self.theme

        self.__CText(T("FAQ_TITLE", "DOMANDE FREQUENTI (FAQ)"), 130, y, t["accent"])
        y += 25

        faqs = [
            (T("FAQ_Q1", "Come attivo il sistema Hunter?"),
             T("FAQ_A1", "Raggiungi il livello 30 per attivare il sistema automaticamente.")),

            (T("FAQ_Q2", "Come vedo le mie missioni?"),
             T("FAQ_A2", "Usa /hunter_missions oppure premi N > Tab Eventi > Apri Dettagli.")),

            (T("FAQ_Q3", "I mostri normali danno Gloria?"),
             T("FAQ_A3", "NO! Solo Fratture, Missioni, Emergency Quest ed Eventi danno Gloria!")),

            (T("FAQ_Q4", "Perche' perdo Gloria?"),
             T("FAQ_A4", "Missioni non completate: perdi Gloria TOTALE (non spendibile).")),

            (T("FAQ_Q5", "Cos'e' il Bonus x1.5?"),
             T("FAQ_A5", "Completi 3 missioni = +50% Gloria missioni + 50% bonus fratture!")),

            (T("FAQ_Q6", "Come salgo di Rank?"),
             T("FAQ_A6", "Accumula Gloria! E->D: 2000, D->C: 10000, C->B: 50000, etc.")),

            (T("FAQ_Q7", "Posso perdere il mio Rank?"),
             T("FAQ_A7", "No, il Rank e' permanente. La Gloria puo' scendere ma non il Rank.")),

            (T("FAQ_Q8", "Come partecipo agli eventi?"),
             T("FAQ_A8", "Usa /hunter_events per vedere gli eventi, poi clicca 'Partecipa'.")),

            (T("FAQ_Q9", "Cosa sono le Fratture?"),
             T("FAQ_A9", "Portali dimensionali con Boss/Metin Elite. Gloria scala col rank!")),

            (T("FAQ_Q10", "Quando si resettano le missioni?"),
             T("FAQ_A10", "Alle 00:05. Missioni incomplete = penalita' su Gloria TOTALE!")),

            (T("FAQ_Q11", "Come funziona lo streak bonus?"),
             T("FAQ_A11", "Accessi consecutivi: 3 giorni=+5%, 7 giorni=+10%, 30 giorni=+20%!")),

            (T("FAQ_Q12", "Cos'e' l'Emergency Quest?"),
             T("FAQ_A12", "Missioni speciali dopo ~500 kill! 40% chance, tempo limitato.")),

            (T("FAQ_Q13", "Come ottengo Speed Kill Bonus?"),
             T("FAQ_A13", "Boss: uccidi in 60s. Metin: distruggi in 300s = x2 Gloria!")),

            (T("FAQ_Q14", "Perche' il Terminale si apre da solo?"),
             T("FAQ_A14", "Quando fai progresso missioni si apre automaticamente per 5 secondi!")),

            (T("FAQ_Q15", "Cosa succede se non completo le missioni?"),
             T("FAQ_A15", "Perdi Gloria TOTALE (non spendibile). Missione segnata come 'failed'.")),

            (T("FAQ_Q16", "Le missioni si perdono se cambio mappa?"),
             T("FAQ_A16", "NO! Le missioni persistono anche cambiando mappa o riloggando.")),

            (T("FAQ_Q17", "Come funziona il sistema Rival?"),
             T("FAQ_A17", "Se qualcuno ti supera in classifica, ricevi una notifica!")),

            (T("FAQ_Q18", "Cosa sono i Bauli Dimensionali?"),
             T("FAQ_A18", "Spawn random nelle fratture. Danno item rari + Gloria bonus!")),

            (T("FAQ_Q19", "Posso aprire Fratture da E-Rank?"),
             T("FAQ_A19", "SI! Tutti possono aprirle, ma rank A+ hanno fratture esclusive.")),

            (T("FAQ_Q20", "Cos'e' la Prova d'Esame?"),
             T("FAQ_A20", "Trial per rank-up: -50% Gloria finche' non completi gli obiettivi!")),

            (T("FAQ_Q21", "Perche' guadagno meno Gloria del solito?"),
             T("FAQ_A21", "Prova d'Esame attiva? Guarda il syschat dettagliato con tutti i bonus/malus!")),

            (T("FAQ_Q22", "Come funziona la Gloria in party?"),
             T("FAQ_A22", "Va a CHI FA L'AZIONE: killer, chi apre bauli, chi conquista fratture!")),

            (T("FAQ_Q23", "Come vedo il calcolo dettagliato Gloria?"),
             T("FAQ_A23", "Ogni kill Boss/Metin/Baule mostra syschat con tutti i bonus e malus!")),

            (T("FAQ_Q24", "Cos'e' il Power Rank?"),
             T("FAQ_A24", "La somma della forza del party: E=1, D=5, C=15, B=40, A=80, S=150, N=250.")),

            (T("FAQ_Q25", "Come forzo fratture B/A/S/N senza Gloria?"),
             T("FAQ_A25", "Servono tot Power Rank: B=100, A=200, S=350, N=500. Fai party con rank alti!")),

            (T("FAQ_Q26", "Cosa sono i Quick Access nel Trial?"),
             T("FAQ_A26", "Pulsanti rapidi per aprire RankUp/Gate e Missioni/Eventi senza uscire!")),

            (T("FAQ_Q27", "Cos'e' il Fracture Bonus +50%?"),
             T("FAQ_A27", "3/3 missioni = +50% Gloria da Boss/Metin delle fratture! Visibile nel dettaglio.")),
        ]

        for q, a in faqs:
            # Domanda
            self.__CBar(5, y, 420, 18, t["bg_dark"])
            self.__CText(T("QUESTION_PREFIX", "D:") + " " + q, 10, y + 2, GOLD_COLOR)
            y += 20

            # Risposta
            self.__CText(T("ANSWER_PREFIX", "R:") + " " + a, 10, y, t["text_value"])
            y += 22

        y += 15
        self.__CSep(5, y)
        y += 15

        # Comandi utili
        self.__CBar(5, y, 420, 115, t["bg_dark"])
        self.__CText(T("COMMANDS_TITLE", "COMANDI E SCORCIATOIE:"), 155, y + 5, t["accent"])
        y += 22

        commands = [
            (T("CMD_KEY_N", "Tasto N"), T("CMD_KEY_N_DESC", "Apre/Chiude il Terminale Hunter")),
            ("/hunter_missions", T("CMD_MISSIONS_DESC", "Apre pannello missioni giornaliere")),
            ("/hunter_events", T("CMD_EVENTS_DESC", "Mostra eventi programmati di oggi")),
            ("/hunter_join_event [id]", T("CMD_JOIN_DESC", "Partecipa all'evento con ID specificato")),
            ("/hunter_buy [id]", T("CMD_BUY_DESC", "Acquista item dallo shop con Gloria")),
            ("/hunter_claim [id]", T("CMD_CLAIM_DESC", "Riscuoti ricompensa achievement")),
            ("/hunter_smart_claim", T("CMD_SMART_CLAIM_DESC", "Riscuoti tutte le ricompense disponibili")),
        ]

        for cmd, desc in commands:
            self.__CText(cmd, 15, y, 0xFF00CCFF)
            self.__CText(desc, 180, y, t["text_muted"])
            y += 18

        y += 20

        # Consigli finali
        self.__CBar(5, y, 420, 145, 0x33FFD700)
        self.__CText("CONSIGLI PER NUOVI HUNTER:", 130, y + 5, GOLD_COLOR)
        self.__CText("1. Completa SEMPRE le 3 missioni giornaliere (evita penalty)", 15, y + 22, t["text_value"])
        self.__CText("2. Emergency Quest dopo ~500 kill = opportunita' MASSIMA!", 15, y + 36, t["text_value"])
        self.__CText("3. Speed Kill Boss (60s) e Metin (300s) = DOPPI PUNTI!", 15, y + 50, t["text_value"])
        self.__CText("4. Accedi ogni giorno per streak bonus (3gg/7gg/30gg)", 15, y + 64, t["text_value"])
        self.__CText("5. Weekend = eventi speciali con Gloria x2/x3!", 15, y + 78, t["text_value"])
        self.__CText("6. Fratture danno PIU' Gloria dei mob normali (200-2000)", 15, y + 92, t["text_value"])
        self.__CText("7. In PARTY la Gloria va a chi fa l'azione (killer/opener)!", 15, y + 106, 0xFF00FFFF)
        self.__CText("8. Usa Quick Access nel Trial per Rank Up e Missioni!", 15, y + 120, 0xFF00FFFF)
        y += 155

        return y
    
    # ========================================================================
    #  CALLBACKS
    # ========================================================================
    def __OnRankSub(self, rType):
        self.__ClearContent()
        self.__LoadRanking(rType)
        self.__SavePositions()
        self.__UpdateScroll()
    
    def __OnBuy(self, iid):
        net.SendChatPacket("/hunter_buy %d" % iid)
    
    def __OnClaim(self, aid):
        net.SendChatPacket("/hunter_claim %d" % aid)
    
    def __OnSmartClaim(self):
        net.SendChatPacket("/hunter_smart_claim")
    
    # ========================================================================
    #  PUBLIC METHODS
    # ========================================================================

    def ShowSystemMessage(self, msg, rankKey="E"):
        """Mostra messaggio del Sistema con colore basato sul rank o color scheme"""
        if self.systemMsgWnd:
            # Prima prova RANK_COLORS (E,D,C,B,A,S,N)
            color = RANK_COLORS.get(rankKey, None)
            if color is None:
                # Poi prova COLOR_SCHEMES (RED, GOLD, GREEN, BLUE, ORANGE, PURPLE)
                scheme = COLOR_SCHEMES.get(rankKey.upper() if rankKey else "", None)
                if scheme:
                    color = scheme["border"]
                else:
                    color = 0xFF808080  # Grigio default
            self.systemMsgWnd.ShowMessage(msg, color)
            # REMOVED: SetRankColor() era ridondante e causava override del colore
    
    def ShowWelcomeMessage(self, rankKey, name, points):
        """Mostra il messaggio di benvenuto epico basato sul rank"""
        
        RANK_TITLES = {
            "E": "[E-RANK] RISVEGLIATO",
            "D": "[D-RANK] APPRENDISTA", 
            "C": "[C-RANK] CACCIATORE",
            "B": "[B-RANK] VETERANO",
            "A": "* [A-RANK] MAESTRO *",
            "S": "** [S-RANK] LEGGENDA **",
            "N": "*** [NATIONAL] MONARCA ***",
        }
        
        RANK_MESSAGES = {
            "E": "Il Sistema ti osserva. Dimostra il tuo valore.",
            "D": "Bentornato, Cacciatore. Il Sistema ti riconosce.",
            "C": "Il Sistema saluta un guerriero esperto.",
            "B": "Bentornato, Veterano. Il Sistema ti onora.",
            "A": "Il Sistema si inchina al tuo potere.",
            "S": "ATTENZIONE: Cacciatore S-Rank rilevato.",
            "N": "!! ALLERTA MASSIMA !! MONARCA NAZIONALE ONLINE !!",
        }
        
        color = RANK_COLORS.get(rankKey, 0xFF808080)
        title = RANK_TITLES.get(rankKey, "[E-RANK]")
        message = RANK_MESSAGES.get(rankKey, "Bentornato.")
        
        # Mostra il messaggio con il colore del rank
        if self.systemMsgWnd:
            fullMsg = title + " - " + message
            self.systemMsgWnd.ShowMessage(fullMsg, color)
    
    def StartEmergencyQuest(self, title, seconds, vnums, count, description="", difficulty="NORMAL", penalty=0):
        if self.emergencyWnd:
            self.emergencyWnd.StartMission(title, seconds, vnums, count, description, difficulty, penalty)
    
    def UpdateEmergencyCount(self, current):
        if self.emergencyWnd:
            self.emergencyWnd.UpdateProgress(current)
    
    def EndEmergencyQuest(self, success):
        if self.emergencyWnd:
            status = "SUCCESS" if success else "FAILED"
            self.emergencyWnd.EndMission(status)
    
    def UpdateRival(self, name, points, label="Gloria", mode="VICINO"):
        if self.rivalWnd:
            self.rivalWnd.ShowRival(name, points, label, mode)
    
    def OpenWhatIf(self, qid, questionText, opt1, opt2, opt3, colorCode="PURPLE"):
        if self.whatIfWnd:
            self.whatIfWnd.Create(qid, questionText, [opt1, opt2, opt3], colorCode)
    
    def ShowBossAlert(self, bossName):
        """Mostra ALERT a schermo intero quando spawna un BOSS"""
        if self.bossAlertWnd:
            self.bossAlertWnd.ShowAlert(bossName)
    
    def ShowSystemInit(self):
        """Mostra effetto di inizializzazione sistema al login"""
        if self.systemInitWnd:
            self.systemInitWnd.StartLoading()
    
    def ShowAwakening(self, level):
        """Mostra effetto awakening per un livello specifico"""
        # level puo' essere int o stringa (retrocompatibilita)
        try:
            lvl = int(level)
        except:
            lvl = 5  # Default se viene passato un nome (vecchio sistema)
        
        if self.awakeningWnd:
            self.awakeningWnd.Start(lvl)
    
    def ShowHunterActivation(self, playerName):
        """Mostra effetto attivazione Hunter al Lv 30 - usa Awakening Lv30"""
        if self.awakeningWnd:
            self.awakeningWnd.Start(30)
    
    def ShowRankUp(self, oldRank, newRank):
        """Mostra effetto salita di rank"""
        if self.rankUpWnd:
            self.rankUpWnd.Start(oldRank, newRank)
    
    def ShowOvertake(self, overtakenName, newPosition):
        """Mostra effetto sorpasso in classifica"""
        if self.overtakeWnd:
            self.overtakeWnd.ShowOvertake(overtakenName, newPosition)
    
    def ShowEventStatus(self, eventName, duration, eventType="default", desc="", reward=""):
        """Mostra finestra stato evento"""
        if self.eventWnd:
            self.eventWnd.ShowEvent(eventName, duration, eventType, desc, reward)
    
    def CloseEventStatus(self):
        """Chiude la finestra stato evento"""
        if self.eventWnd:
            self.eventWnd.Hide()
    
    # ========================================================================
    #  DAILY MISSIONS SYSTEM
    # ========================================================================
    def SetMissionsCount(self, count):
        """Prepara per ricevere dati missioni"""
        self.missionsCount = int(count)
        self.missionsData = []
    
    def AddMissionData(self, missionData):
        """Aggiunge dati di una missione"""
        # formato: id|name|type|current|target|reward|penalty|status
        try:
            parts = missionData.split("|")
            if len(parts) >= 8:
                mission = {
                    "id": int(parts[0]),
                    "name": parts[1],
                    "type": parts[2],
                    "current": int(parts[3]),
                    "target": int(parts[4]),
                    "reward": int(parts[5]),
                    "penalty": int(parts[6]),
                    "status": parts[7]  # active, completed, failed
                }
                self.missionsData.append(mission)
                
                # Quando abbiamo ricevuto tutti i dati, aggiorna UI
                if len(self.missionsData) >= self.missionsCount:
                    if self.missionsWnd:
                        self.missionsWnd.SetMissions(self.missionsData, self.theme)
        except:
            import dbg
            dbg.TraceError("AddMissionData parse error: " + str(missionData))
    
    def UpdateMissionProgress(self, missionId, current, target):
        """Aggiorna progresso di una missione specifica"""
        missionId = int(missionId)
        current = int(current)
        target = int(target)

        # Aggiorna nei dati locali
        for m in self.missionsData:
            if m["id"] == missionId:
                m["current"] = current
                m["target"] = target
                break

        # Mostra popup progresso (3 sec)
        if self.missionProgressWnd:
            # Trova nome missione
            missionName = "Missione #%d" % missionId
            for m in self.missionsData:
                if m["id"] == missionId:
                    missionName = m["name"]
                    break
            self.missionProgressWnd.ShowProgress(missionName, current, target, self.theme)

        # AUTO-APERTURA: Apri la finestra Daily Missions (non il terminale)
        if self.missionsWnd:
            if not self.missionsWnd.IsShow():
                self.missionsWnd.Open()
                self.missionsWnd.autoCloseTimer = 5.0  # Chiudi dopo 5 secondi
            else:
                # Se già aperta, resetta il timer
                self.missionsWnd.autoCloseTimer = 5.0
            
            # Aggiorna i dati nella finestra
            self.missionsWnd.UpdateProgress(missionId, current, target)
    
    def OnMissionComplete(self, missionId, name, reward):
        """Notifica completamento missione"""
        missionId = int(missionId)
        reward = int(reward)
        
        # Aggiorna status locale
        for m in self.missionsData:
            if m["id"] == missionId:
                m["status"] = "completed"
                break
        
        # Mostra effetto completamento
        if self.missionCompleteWnd:
            self.missionCompleteWnd.ShowComplete(name, reward, self.theme)
        
        # Aggiorna finestra missioni se aperta
        if self.missionsWnd and self.missionsWnd.IsShow():
            self.missionsWnd.SetMissionComplete(missionId)
    
    def OnAllMissionsComplete(self, bonus, hasFractureBonus=False):
        """Notifica tutte le missioni complete - bonus x1.5 per le fratture"""
        bonus = int(bonus)
        if self.allMissionsCompleteWnd:
            self.allMissionsCompleteWnd.ShowBonus(bonus, self.theme, hasFractureBonus)
        
        # Se il bonus fratture è attivo, mostra indicatore
        if hasFractureBonus:
            # Aggiorna il titolo o aggiunge visual indicator
            if self.theme == "awakening":
                self.bonusIndicatorText = "BONUS FRATTURE ATTIVO +50%"
            else:
                self.bonusIndicatorText = "BONUS SEAL +50%"
            self.fractureBonusActive = True
    
    def OpenMissionsPanel(self):
        """Apre pannello missioni giornaliere"""
        if self.missionsWnd:
            self.missionsWnd.Open(self.missionsData, self.theme)
    
    def OpenRankUpPanel(self):
        """Apre pannello Rank Up - mostra finestra principale con tab RankUp"""
        try:
            # Apre la finestra principale Hunter
            self.Show()
            self.SetTop()
            # Imposta la tab su RankUp se esiste
            if hasattr(self, 'tabButtons') and self.tabButtons:
                # Cerca la tab RankUp/Rank
                for tabName, btn in self.tabButtons.items():
                    if "rank" in tabName.lower():
                        self.__OnTabClick(tabName)
                        break
        except Exception as e:
            import dbg
            dbg.TraceError("OpenRankUpPanel error: " + str(e))
    
    # ========================================================================
    #  EVENTS SCHEDULE SYSTEM
    # ========================================================================
    def SetEventsCount(self, count):
        """Prepara per ricevere dati eventi"""
        self.eventsCount = int(count)
        self.eventsData = []
    
    def AddEventData(self, eventData):
        """Aggiunge dati di un evento"""
        # Ora riceve direttamente un dizionario da game.py
        try:
            if isinstance(eventData, dict):
                # Nuovo formato dizionario
                event = {
                    "id": eventData.get("id", 0),
                    "name": eventData.get("name", "Evento"),
                    "start_time": eventData.get("start_time", "00:00"),
                    "end_time": eventData.get("end_time", "00:00"),
                    "type": eventData.get("type", "glory_rush"),
                    "reward": eventData.get("reward", "+50 Gloria"),
                    "status": eventData.get("status", "upcoming"),
                    "desc": eventData.get("desc", ""),
                    "color": eventData.get("color", "GOLD"),
                    "min_rank": eventData.get("min_rank", "E"),
                    "winner_prize": eventData.get("winner_prize", 200)
                }
            else:
                # Fallback vecchio formato stringa
                parts = eventData.split("|")
                if len(parts) >= 7:
                    event = {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "start_time": parts[2],
                        "end_time": parts[3],
                        "type": parts[4],
                        "reward": parts[5],
                        "status": parts[6],
                        "desc": parts[7] if len(parts) > 7 else "",
                        "color": parts[8] if len(parts) > 8 else "GOLD",
                        "min_rank": parts[9] if len(parts) > 9 else "E",
                        "winner_prize": int(parts[10]) if len(parts) > 10 else 200
                    }
                else:
                    return
                    
            self.eventsData.append(event)
            
            # Quando abbiamo tutti i dati, aggiorna UI
            if len(self.eventsData) >= self.eventsCount:
                # Aggiorna finestra eventi popup se esiste
                if self.eventsWnd:
                    self.eventsWnd.SetEvents(self.eventsData, self.theme)
                # Se siamo nel tab Eventi (4), refresha il contenuto del terminale
                if self.currentTab == 4:
                    self.__ClearContent()
                    self.__LoadEvents(skipRequest=True)  # Non richiedere di nuovo dal server
                    self.__SavePositions()
                    self.__UpdateScroll()
        except Exception as e:
            import dbg
            dbg.TraceError("AddEventData parse error: " + str(eventData) + " - " + str(e))
    
    def OnEventJoined(self, eventId, name, glory):
        """Conferma partecipazione ad evento"""
        eventId = int(eventId)
        glory = int(glory)
        
        # Aggiorna status locale
        for e in self.eventsData:
            if e["id"] == eventId:
                e["status"] = "joined"
                break
        
        # Mostra conferma
        if self.systemMsgWnd:
            self.systemMsgWnd.ShowMessage("Iscritto a: %s (+%d Gloria)" % (name, glory), "GREEN")
        
        # Aggiorna finestra eventi
        if self.eventsWnd and self.eventsWnd.IsShow():
            self.eventsWnd.SetEventJoined(eventId)
    
    def OpenEventsPanel(self):
        """Apre pannello eventi programmati"""
        if self.eventsWnd:
            self.eventsWnd.Open(self.eventsData, self.theme)

    def OnNewDay(self):
        """E' passata la mezzanotte - resetta cache eventi e aggiorna UI"""
        import chat
        
        # Pulisci cache eventi vecchi
        self.eventsData = []
        self.eventsCount = 0
        
        # Chiudi popup eventi se aperto (mostrera' dati vecchi)
        if self.eventsWnd and self.eventsWnd.IsShow():
            self.eventsWnd.Hide()
        
        # Notifica player
        chat.AppendChat(chat.CHAT_TYPE_INFO, "|cff00FFFF[HUNTER]|r Nuovo giorno! Lista eventi aggiornata.")
        
        # Se siamo nel tab eventi, forza refresh
        if self.currentTab == 4:
            self.__ClearContent()
            self.__LoadEvents(skipRequest=False)  # Richiedi nuovi dati
            self.__SavePositions()
            self.__UpdateScroll()

    # ========================================================================
    #  DATA SETTERS
    # ========================================================================
    def SetPlayerData(self, d):
        self.playerData.update(d)
        self.__UpdateTheme()
        self.__UpdateHeaderContent()
        if self.currentTab == 0:
            self.__ClearContent()
            self.__LoadStats()
            self.__SavePositions()
            self.__UpdateScroll()
    
    def SetRankingData(self, rt, d):
        self.rankingData[rt] = d
        if rt == "daily":
            self.rankingData["daily_points"] = d
        elif rt == "weekly":
            self.rankingData["weekly_points"] = d
        elif rt == "total":
            self.rankingData["total_points"] = d
    
    def SetShopItems(self, d):
        self.shopData = d
    
    def SetAchievements(self, d):
        self.achievementsData = d
    
    def SetCalendarEvents(self, d):
        self.calendarData = d
    
    def SetActiveEvent(self, n, desc):
        self.activeEvent = (n if n else "Nessuno", desc)
        # Mostra/nasconde il popup evento
        if self.eventWnd:
            self.eventWnd.SetEvent(n, desc)
    
    def SetTimers(self, ds, ws):
        try:
            self.dailyResetSeconds = int(ds)
            self.weeklyResetSeconds = int(ws)
        except:
            pass
    
    def SetFractures(self, d):
        pass
    
    # ========================================================================
    #  UPDATE
    # ========================================================================
    def OnUpdate(self):
        if not self.isLoaded or self.isDestroyed:
            return
        
        if self.systemMsgWnd:
            self.systemMsgWnd.OnUpdate()
        if self.emergencyWnd:
            self.emergencyWnd.OnUpdate()
        if self.rivalWnd:
            self.rivalWnd.OnUpdate()
        if self.eventWnd:
            self.eventWnd.OnUpdate()
        
        ct = app.GetTime()
        dt = ct - self.lastUpdateTime
        self.lastUpdateTime = ct
        self.timerUpdateAccum += dt

        # Auto-close timer per finestra missioni
        if self.autoCloseTimer > 0.0:
            self.autoCloseTimer -= dt
            if self.autoCloseTimer <= 0.0:
                self.autoCloseTimer = 0.0
                # Chiudi solo se è stata aperta automaticamente e player non ha interagito
                if self.autoOpenedForMission:
                    self.Close()
                    self.autoOpenedForMission = False

        if self.timerUpdateAccum >= 1.0:
            self.timerUpdateAccum = 0.0
            if self.dailyResetSeconds > 0:
                self.dailyResetSeconds -= 1
            if self.weeklyResetSeconds > 0:
                self.weeklyResetSeconds -= 1
            self.__UpdateTimers()
    
    def __UpdateTimers(self):
        if hasattr(self, 'dailyTimerLabel') and self.dailyTimerLabel:
            d = max(0, int(self.dailyResetSeconds))
            self.dailyTimerLabel.SetText("%02d:%02d:%02d" % (d // 3600, (d % 3600) // 60, d % 60))
        if hasattr(self, 'weeklyTimerLabel') and self.weeklyTimerLabel:
            w = max(0, int(self.weeklyResetSeconds))
            self.weeklyTimerLabel.SetText("%dg %02d:%02d" % (w // 86400, (w % 86400) // 3600, (w % 3600) // 60))
    
    def Open(self):
        if not self.isLoaded:
            if not self.LoadWindow():
                return
        self.__UpdateTheme()
        self.SetCenterPosition()
        self.SetTop()
        self.Show()

        # Se il player apre manualmente mentre c'è un timer auto-close, disabilitalo
        # Questo evita che la finestra si chiuda se il player vuole tenerla aperta
        if self.IsShow() and self.autoCloseTimer > 0.0:
            self.autoOpenedForMission = False
            self.autoCloseTimer = 0.0
    
    def OnPressEscapeKey(self):
        self.Close()
        return True

    # ========================================================================
    #  SPEED KILL SYSTEM - Metodi richiesti per Speed Kill Timer
    # ========================================================================
    def StartSpeedKill(self, mobType, duration, color):
        """Avvia speed kill timer"""
        import chat
        minutes = duration / 60
        chat.AppendChat(chat.CHAT_TYPE_INFO, "[SPEED KILL] %s - Uccidi entro %d:%02d per GLORIA x2!" % (mobType, minutes, duration % 60))

    def UpdateSpeedKillTimer(self, remainingSeconds):
        """Aggiorna timer (chiamato ogni secondo)"""
        # Non stampiamo nulla per non spammare la chat
        pass

    def EndSpeedKill(self, isSuccess):
        """Termina speed kill"""
        import chat
        if isSuccess == 1 or isSuccess == "1":
            chat.AppendChat(chat.CHAT_TYPE_INFO, "[SPEED KILL SUCCESS] GLORIA x2!")
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "[SPEED KILL FAILED] Gloria normale")

    # ========================================================================
    #  FRACTURE DEFENSE SYSTEM - Metodi richiesti per difesa fratture
    # ========================================================================
    def StartFractureDefense(self, fractureName, duration, color):
        """Avvia difesa frattura"""
        import chat
        minutes = duration / 60
        chat.AppendChat(chat.CHAT_TYPE_INFO, "[DIFESA FRATTURA] %s - Difendi per %d:%02d!" % (fractureName, minutes, duration % 60))

    def UpdateFractureDefenseTimer(self, remainingSeconds):
        """Aggiorna timer difesa (chiamato ogni secondo)"""
        # Non stampiamo nulla per non spammare la chat
        pass

    def CompleteFractureDefense(self, success, message):
        """Termina difesa frattura"""
        import chat
        if success == 1 or success == "1":
            chat.AppendChat(chat.CHAT_TYPE_INFO, "[DIFESA RIUSCITA] %s" % message)
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "[DIFESA FALLITA] %s" % message)

# ============================================================================
#  WINDOW MANAGER
# ============================================================================
_wndManager = None

def SetWindowManager(w):
    global _wndManager
    _wndManager = proxy(w) if w else None

def GetHunterLevelWindow():
    global _wndManager
    try:
        return _wndManager
    except:
        return None

def OpenHunterLevelWindow():
    w = GetHunterLevelWindow()
    if w:
        w.Open()

def CloseHunterLevelWindow():
    w = GetHunterLevelWindow()
    if w:
        w.Close()

def ToggleHunterLevelWindow():
    w = GetHunterLevelWindow()
    if w:
        if w.IsShow():
            w.Close()
        else:
            w.Open()
