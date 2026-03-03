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
import item
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
#  LINGOTTI YANG - Mappa VNUM -> Valore Yang per preview achievement
# ============================================================================
YANG_INGOTS = {
    80003: 50000,        # Lingotto d'Argento (50k)
    80004: 100000,       # Lingotto d'Argento (100k)
    80005: 500000,       # Lingotto d'Oro (500k)
    80006: 1000000,      # Lingotto d'Oro (1kk)
    80007: 2000000,      # Lingotto d'Oro (2kk)
    80008: 10000000,     # Lingotto d'Oro (10kk)
    80009: 5000000,      # Lingotto d'Argento (5kk)
}

def FormatYang(amount):
    """Formatta la quantita' di Yang in modo leggibile"""
    if amount >= 1000000000:
        return "%.1fB" % (amount / 1000000000.0)
    elif amount >= 1000000:
        return "%.1fkk" % (amount / 1000000.0)
    elif amount >= 1000:
        return "%.0fk" % (amount / 1000.0)
    return str(amount)

# ============================================================================
#  GUIDE TOOLTIP - Testo con hover per spiegazioni dettagliate
# ============================================================================
_g_guideTooltip = None

def _GetGuideTooltip():
    global _g_guideTooltip
    if _g_guideTooltip is None:
        _g_guideTooltip = GuideTooltip()
    return _g_guideTooltip


class GuideTooltip(ui.Window):
    """Tooltip flottante per la guida del terminale Hunter."""

    MAX_WIDTH = 340
    LINE_H = 14
    POOL_SIZE = 30
    BAR_POOL = 6
    HEADER_H = 24

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(self.MAX_WIDTH, 50)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        self.tooltipH = 50
        self.linePool = []
        self.barPool = []
        self.usedLines = 0
        self.usedBars = 0
        self.__BuildFrame()
        self.__BuildPool()
        self.Hide()

    def __BuildFrame(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.MAX_WIDTH, 50)
        self.bg.SetColor(0xF2080812)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(0, 0)
        self.headerBg.SetSize(self.MAX_WIDTH, self.HEADER_H)
        self.headerBg.SetColor(0xCC1a0a2a)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.MAX_WIDTH, 2)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 48)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)
        self.borderBot.SetColor(0xFFFFD700)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()

        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, 50)
        self.borderLeft.SetColor(0xFFFFD700)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, 50)
        self.borderRight.SetColor(0xFFFFD700)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(2, self.HEADER_H)
        self.headerLine.SetSize(self.MAX_WIDTH - 4, 1)
        self.headerLine.SetColor(0xFFFFD700)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.MAX_WIDTH // 2, 4)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(0xFFFFFFFF)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()

    def __BuildPool(self):
        for i in range(self.POOL_SIZE):
            tl = ui.TextLine()
            tl.SetParent(self)
            tl.AddFlag("not_pick")
            tl.Hide()
            self.linePool.append(tl)
        for i in range(self.BAR_POOL):
            b = ui.Bar()
            b.SetParent(self)
            b.AddFlag("not_pick")
            b.Hide()
            self.barPool.append(b)

    def __ResetPool(self):
        for tl in self.linePool:
            tl.Hide()
        for b in self.barPool:
            b.Hide()
        self.usedLines = 0
        self.usedBars = 0

    def __PutLine(self, text, color, x, y, outline=False):
        if self.usedLines < len(self.linePool):
            tl = self.linePool[self.usedLines]
            tl.SetPosition(x, y)
            tl.SetText(text)
            tl.SetPackedFontColor(color)
            if outline:
                tl.SetOutline()
            tl.Show()
            self.usedLines += 1

    def __PutSep(self, y, color=0xFF333355):
        if self.usedBars < len(self.barPool):
            b = self.barPool[self.usedBars]
            b.SetPosition(14, y)
            b.SetSize(self.MAX_WIDTH - 28, 1)
            b.SetColor(color)
            b.Show()
            self.usedBars += 1

    def __DimColor(self, color, factor):
        a = (color >> 24) & 0xFF
        r = int(((color >> 16) & 0xFF) * factor)
        g = int(((color >> 8) & 0xFF) * factor)
        b = int((color & 0xFF) * factor)
        return (a << 24) | (min(255, r) << 16) | (min(255, g) << 8) | min(255, b)

    def ShowTip(self, title, titleColor, lines):
        """Mostra tooltip con titolo e righe descrittive.
        lines = lista di tuple (testo, colore) o stringhe semplici."""
        self.__ResetPool()

        self.titleText.SetText(title)
        self.titleText.SetPackedFontColor(titleColor)
        self.headerBg.SetColor(self.__DimColor(titleColor, 0.15))

        y = self.HEADER_H + 8

        for item in lines:
            if isinstance(item, tuple):
                text, color = item
            else:
                text = item
                color = 0xFFCCCCCC

            if text == "---":
                self.__PutSep(y, self.__DimColor(titleColor, 0.4))
                y += 8
            elif text == "":
                y += 4
            else:
                self.__PutLine(text, color, 14, y)
                y += self.LINE_H

        y += 10

        self.tooltipH = y
        self.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.bg.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.borderLeft.SetSize(2, self.tooltipH)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, self.tooltipH)
        self.borderBot.SetPosition(0, self.tooltipH - 2)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)

        self.borderLeft.SetColor(titleColor)
        self.borderRight.SetColor(self.__DimColor(titleColor, 0.5))
        self.borderTop.SetColor(titleColor)
        self.borderBot.SetColor(self.__DimColor(titleColor, 0.5))
        self.headerLine.SetColor(self.__DimColor(titleColor, 0.6))

        mouseX, mouseY = wndMgr.GetMousePosition()
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()

        px = mouseX + 15
        py = mouseY - self.tooltipH // 2
        if px + self.MAX_WIDTH > screenW:
            px = mouseX - self.MAX_WIDTH - 10
        if py < 5:
            py = 5
        if py + self.tooltipH > screenH - 5:
            py = screenH - self.tooltipH - 5

        self.SetPosition(max(0, px), max(0, py))
        self.Show()
        self.SetTop()

    def HideTip(self):
        self.Hide()


class GuideHoverBar(ui.Bar):
    """Barra invisibile con hover che mostra il GuideTooltip."""
    def __init__(self, title, titleColor, lines):
        ui.Bar.__init__(self)
        self.tipTitle = title
        self.tipTitleColor = titleColor
        self.tipLines = lines

    def OnMouseOverIn(self):
        tip = _GetGuideTooltip()
        tip.ShowTip(self.tipTitle, self.tipTitleColor, self.tipLines)

    def OnMouseOverOut(self):
        tip = _GetGuideTooltip()
        tip.HideTip()


class ShopIconHoverBar(ui.Bar):
    """Barra hover invisibile sopra icone shop - mostra tooltip item al passaggio mouse."""
    def __init__(self, vnum):
        ui.Bar.__init__(self)
        self.vnum = int(vnum)

    def OnMouseOverIn(self):
        tip = _GetGuideTooltip()
        try:
            item.SelectItem(self.vnum)
            name = item.GetItemName()
            desc = item.GetItemDescription()
            lines = []
            if desc and len(desc) > 1:
                lines.append(desc)
            lines.append("---")
            lines.append(("VNUM: %d" % self.vnum, 0xFF666688))
        except:
            name = "Item #%d" % self.vnum
            lines = []
        tip.ShowTip(name, 0xFF00FFFF, lines)

    def OnMouseOverOut(self):
        tip = _GetGuideTooltip()
        tip.HideTip()


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
                      dailyMissions, dailyReq, fromRank=None,
                      bossNames="", metinNames="", fractureNames="", chestNames=""):
        """Aggiorna lo stato della Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.UpdateTrialStatus(
                trialId, trialName, toRank, colorCode, remainingSeconds,
                bossKills, bossReq, metinKills, metinReq,
                fractureSeals, fractureReq, chestOpens, chestReq,
                dailyMissions, dailyReq, fromRank,
                bossNames, metinNames, fractureNames, chestNames
            )
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialStatus error: " + str(e))

    def OnTrialProgress(self, trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions,
                         bossReq=0, metinReq=0, fractureReq=0, chestReq=0, dailyReq=0):
        """Aggiorna il progresso della Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.UpdateTrialProgress(
                trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions,
                bossReq, metinReq, fractureReq, chestReq, dailyReq
            )
        except Exception as e:
            import dbg
            dbg.TraceError("OnTrialProgress error: " + str(e))

    def OnTrialComplete(self, newRank, gloriaReward, trialName):
        """Mostra il completamento della Trial"""
        try:
            import uihunterlevel_gate_trial
            uihunterlevel_gate_trial.ShowSystemMessage("GOLD", "Trial completata! Sei ora Rank " + newRank + "! +" + str(gloriaReward) + " Gloria")
            # Resetta la Trial - passa newRank come fromRank per aggiornare il rank corrente
            uihunterlevel_gate_trial.UpdateTrialStatus(0, "", newRank, "GRAY", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, newRank)
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
            "defense_wins": 0, "defense_losses": 0, "elite_kills": 0,
            "hunter_rank": "",
            "hunter_courage": 100
        }
        
        self.rankingData = {
            "daily": [], "weekly": [], "total": [],
            "daily_points": [], "weekly_points": [], "total_points": [],
            "daily_kills": [], "weekly_kills": [], "total_kills": [],
            "fractures": [], "chests": [], "metins": []
        }
        self.shopData = []
        self.chestShopData = []
        self.shopMode = "selector"  # "selector", "normal", "chests"
        self.fractureData = []
        self.achievementsData = []
        self.lastAchievementsRequest = 0  # Cooldown anti-spam per auto-request achievements
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
        
        # Supremo System Windows
        self.supremoAwakeningWnd = hunter_windows.GetSupremoAwakeningWindow()
        self.supremoChallengeWnd = hunter_windows.GetSupremoChallengeWindow()
        self.supremoVictoryWnd = hunter_windows.GetSupremoVictoryWindow()
        self.gloryDetailWnd = hunter_windows.GetGloryDetailWindow()
        
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
        
        for wnd in [self.systemMsgWnd, self.emergencyWnd, self.whatIfWnd, self.rivalWnd, self.eventWnd,
                    self.supremoAwakeningWnd, self.supremoChallengeWnd, self.supremoVictoryWnd,
                    self.bossAlertWnd, self.systemInitWnd, self.awakeningWnd,
                    self.rankUpWnd, self.overtakeWnd, self.missionsWnd]:
            if wnd:
                try:
                    wnd.Hide()
                except:
                    pass
        self.systemMsgWnd = None
        self.emergencyWnd = None
        self.whatIfWnd = None
        self.rivalWnd = None
        self.eventWnd = None
        self.supremoAwakeningWnd = None
        self.supremoChallengeWnd = None
        self.supremoVictoryWnd = None
        self.bossAlertWnd = None
        self.systemInitWnd = None
        self.awakeningWnd = None
        self.rankUpWnd = None
        self.overtakeWnd = None
        self.missionsWnd = None
        
        self.ClearDictionary()
        self.isLoaded = False
        
    def Close(self):
        # Nascondi tooltip guida se visibile
        try:
            tip = _GetGuideTooltip()
            tip.HideTip()
        except:
            pass
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
        # Nascondi tooltip guida se visibile
        try:
            tip = _GetGuideTooltip()
            tip.HideTip()
        except:
            pass

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
                    # Pulisci riferimenti GuideHoverBar per GC
                    if hasattr(self.contentElements[i], 'tipLines'):
                        self.contentElements[i].tipLines = None
                        self.contentElements[i].tipTitle = None
                        self.contentElements[i].tipTitleColor = None
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
        # FIX: Usa il rank confermato dal server (Prove del Maestro), NON calcolato dai punti
        confirmedRank = self.playerData.get("hunter_rank", "")
        if confirmedRank and confirmedRank in RANK_THEMES:
            newKey = confirmedRank
        else:
            # Fallback per compatibilita' con vecchio formato senza hunter_rank
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
        self.__CreateCloseButton()  # ULTIMO: Z-order sopra tutto
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

        # Background principale – profondo quasi-nero
        bg = ui.Bar()
        bg.SetParent(self.baseWindow)
        bg.SetPosition(0, 0)
        bg.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        bg.SetColor(t["bg_dark"])
        bg.Show()
        self._DisableMousePick(bg)
        self.bgElements.append(bg)

        # Inner background layer (profondità + texture)
        bgInner = ui.Bar()
        bgInner.SetParent(self.baseWindow)
        bgInner.SetPosition(3, 3)
        bgInner.SetSize(WINDOW_WIDTH - 6, WINDOW_HEIGHT - 6)
        bgInner.SetColor(t["bg_medium"])
        bgInner.Show()
        self._DisableMousePick(bgInner)
        self.bgElements.append(bgInner)

        # Top highlight (gradiente cima)
        topHL = ui.Bar()
        topHL.SetParent(self.baseWindow)
        topHL.SetPosition(4, 4)
        topHL.SetSize(WINDOW_WIDTH - 8, 3)
        topHL.SetColor(0x0CFFFFFF)
        topHL.Show()
        self._DisableMousePick(topHL)
        self.bgElements.append(topHL)

        # Bordi neon principali – Top 3px, Left 3px (più visibili), Bottom/Right 2px (asimmetria elegante)
        borderColor = t["border"]
        borderDim = 0xFF000000 | (((borderColor >> 16) & 0xFF) * 2 // 3 << 16) | (((borderColor >> 8) & 0xFF) * 2 // 3 << 8) | ((borderColor & 0xFF) * 2 // 3)
        for (x, y, w, h, col) in [
            (0, 0, WINDOW_WIDTH, 3, borderColor),         # Top
            (0, WINDOW_HEIGHT - 2, WINDOW_WIDTH, 2, borderDim),  # Bottom
            (0, 0, 3, WINDOW_HEIGHT, borderColor),         # Left
            (WINDOW_WIDTH - 2, 0, 2, WINDOW_HEIGHT, borderDim),  # Right
        ]:
            border = ui.Bar()
            border.SetParent(self.baseWindow)
            border.SetPosition(x, y)
            border.SetSize(w, h)
            border.SetColor(col)
            border.Show()
            self._DisableMousePick(border)
            self.bgElements.append(border)

        # Angoli decorativi DOPPI – stile Solo Leveling definitivo
        cornerLen = 30
        cornerColor = t.get("accent", t["border"])
        cornerColorDim = 0xFF000000 | (((cornerColor >> 16) & 0xFF) // 2 << 16) | (((cornerColor >> 8) & 0xFF) // 2 << 8) | ((cornerColor & 0xFF) // 2)

        # Outer corners (brillanti)
        self.__CreateCorner(0, 0, cornerLen, cornerColor, "TL")
        self.__CreateCorner(WINDOW_WIDTH - cornerLen, 0, cornerLen, cornerColor, "TR")
        self.__CreateCorner(0, WINDOW_HEIGHT - cornerLen, cornerLen, cornerColor, "BL")
        self.__CreateCorner(WINDOW_WIDTH - cornerLen, WINDOW_HEIGHT - cornerLen, cornerLen, cornerColor, "BR")
        # Inner corners (attenuati - doppio bracket)
        innerLen = 14
        innerOffset = 6
        self.__CreateCorner(innerOffset, innerOffset, innerLen, cornerColorDim, "TL")
        self.__CreateCorner(WINDOW_WIDTH - innerLen - innerOffset, innerOffset, innerLen, cornerColorDim, "TR")
        self.__CreateCorner(innerOffset, WINDOW_HEIGHT - innerLen - innerOffset, innerLen, cornerColorDim, "BL")
        self.__CreateCorner(WINDOW_WIDTH - innerLen - innerOffset, WINDOW_HEIGHT - innerLen - innerOffset, innerLen, cornerColorDim, "BR")

        # FIX: Close button con colori espliciti ad alto contrasto (visibile su ogni tema)
        # NOTA: Creato in __CreateCloseButton() per z-order corretto (dopo header/tabs)

    def __CreateCloseButton(self):
        """Crea il bottone X di chiusura – più elaborato e visibile"""
        closeWnd = ui.Window()
        closeWnd.SetParent(self.baseWindow)
        closeWnd.SetPosition(WINDOW_WIDTH - 34, 5)
        closeWnd.SetSize(26, 22)
        closeWnd.Show()

        # BG con sfumatura rosso scuro
        closeBg = ui.Bar()
        closeBg.SetParent(closeWnd)
        closeBg.SetPosition(0, 0)
        closeBg.SetSize(26, 22)
        closeBg.SetColor(0xDD1A0000)
        closeBg.AddFlag("not_pick")
        closeBg.Show()

        # Bordo superiore rosso brillante (2px)
        closeBorderT = ui.Bar()
        closeBorderT.SetParent(closeWnd)
        closeBorderT.SetPosition(0, 0)
        closeBorderT.SetSize(26, 2)
        closeBorderT.SetColor(0xFFFF3333)
        closeBorderT.AddFlag("not_pick")
        closeBorderT.Show()

        # Bordo inferiore (1px attenuato)
        closeBorderB = ui.Bar()
        closeBorderB.SetParent(closeWnd)
        closeBorderB.SetPosition(0, 21)
        closeBorderB.SetSize(26, 1)
        closeBorderB.SetColor(0x66FF3333)
        closeBorderB.AddFlag("not_pick")
        closeBorderB.Show()

        # Bordi laterali
        closeBorderL = ui.Bar()
        closeBorderL.SetParent(closeWnd)
        closeBorderL.SetPosition(0, 0)
        closeBorderL.SetSize(1, 22)
        closeBorderL.SetColor(0x88FF3333)
        closeBorderL.AddFlag("not_pick")
        closeBorderL.Show()

        closeBorderR = ui.Bar()
        closeBorderR.SetParent(closeWnd)
        closeBorderR.SetPosition(25, 0)
        closeBorderR.SetSize(1, 22)
        closeBorderR.SetColor(0x88FF3333)
        closeBorderR.AddFlag("not_pick")
        closeBorderR.Show()

        # Testo X centrato
        closeText = ui.TextLine()
        closeText.SetParent(closeWnd)
        closeText.SetPosition(13, 3)
        closeText.SetHorizontalAlignCenter()
        closeText.SetText("X")
        closeText.SetPackedFontColor(0xFFFF5555)
        closeText.SetOutline()
        closeText.Show()

        closeWnd.OnMouseLeftButtonUp = lambda: self.Close()
        self.closeWnd = closeWnd
        self.closeBg = closeBg
        self.closeText = closeText
        self.bgElements.append(closeWnd)

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

        # Glow esterno ampio (alone luminoso attorno all'header)
        glowOuter = ui.Bar()
        glowOuter.SetParent(self.baseWindow)
        glowOuter.SetPosition(6, 6)
        glowOuter.SetSize(WINDOW_WIDTH - 12, HEADER_HEIGHT + 8)
        glowOuter.SetColor(t["glow"])
        glowOuter.Show()
        self._DisableMousePick(glowOuter)
        self.headerElements.append(glowOuter)

        # Background header – più scuro, quasi piatto
        headerBg = ui.Bar()
        headerBg.SetParent(self.baseWindow)
        headerBg.SetPosition(10, 10)
        headerBg.SetSize(WINDOW_WIDTH - 20, HEADER_HEIGHT)
        headerBg.SetColor(t["bg_dark"])
        headerBg.Show()
        self._DisableMousePick(headerBg)
        self.headerElements.append(headerBg)

        # Inner header (gradiente interno simulato – layer più chiaro in cima)
        headerBgTop = ui.Bar()
        headerBgTop.SetParent(self.baseWindow)
        headerBgTop.SetPosition(12, 12)
        headerBgTop.SetSize(WINDOW_WIDTH - 24, HEADER_HEIGHT // 3)
        headerBgTop.SetColor(0x0CFFFFFF)
        headerBgTop.Show()
        self._DisableMousePick(headerBgTop)
        self.headerElements.append(headerBgTop)

        # Left accent bar nell'header (barra neon sx – iconica)
        headerAccent = ui.Bar()
        headerAccent.SetParent(self.baseWindow)
        headerAccent.SetPosition(10, 10)
        headerAccent.SetSize(4, HEADER_HEIGHT)
        headerAccent.SetColor(t["border"])
        headerAccent.Show()
        self._DisableMousePick(headerAccent)
        self.headerElements.append(headerAccent)

        # Bordi neon header superiore (2px brillante) e inferiore (2px attenuato)
        glowTop = ui.Bar()
        glowTop.SetParent(self.baseWindow)
        glowTop.SetPosition(10, 10)
        glowTop.SetSize(WINDOW_WIDTH - 20, 2)
        glowTop.SetColor(t["border"])
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

        # Angoli decorativi – DOPPIO BRACKET
        cornerSize = 16
        cornerColor = t.get("accent", t["border"])

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
        # Mantieni i primi 16 elementi (glow, bg, innerBg, accent, bordi, angoli decorativi)
        baseElements = 16
        for e in self.headerElements[baseElements:]:
            try:
                e.Hide()
            except:
                pass
        self.headerElements = self.headerElements[:baseElements]
        
        t = self.theme
        pts = self.playerData["total_points"]
        
        # FIX: Calcola progresso header basandosi sul rank confermato
        confirmedRank = self.playerData.get("hunter_rank", "")
        if not confirmedRank or confirmedRank not in RANK_THEMES:
            confirmedRank = GetRankKey(pts)
        rank_current_thr = {"E": 0, "D": 2000, "C": 10000, "B": 50000, "A": 150000, "S": 500000, "N": 1500000}
        rank_next_thr = {"E": 2000, "D": 10000, "C": 50000, "B": 150000, "A": 500000, "S": 1500000, "N": None}
        cur_thr = rank_current_thr.get(confirmedRank, 0)
        nxt_thr = rank_next_thr.get(confirmedRank, None)
        if nxt_thr and nxt_thr > cur_thr:
            progress = min(100.0, max(0.0, float(pts - cur_thr) / float(nxt_thr - cur_thr) * 100))
        elif confirmedRank == "N":
            progress = 100.0
        else:
            progress = 0.0
        
        # ── Riga 1: Nome + Gloria + Daily ──
        self.__HText("CACCIATORE", 20, 15, t["text_muted"])
        self.__HText(str(self.playerData["name"]), 100, 15, t["accent_bright"] if "accent_bright" in t else t["accent"])

        self.__HText("GLORIA", 250, 15, t["text_muted"])
        self.__HText(FormatNumber(pts), 300, 15, GOLD_COLOR)

        self.__HText("+Oggi", 400, 15, t["text_muted"])
        self.__HText(FormatNumber(self.playerData["daily_points"]), 440, 15, 0xFF44FF88)

        # Separatore orizzontale sottile
        sepH = ui.Bar()
        sepH.SetParent(self.baseWindow)
        sepH.SetPosition(16, 33)
        sepH.SetSize(WINDOW_WIDTH - 32, 1)
        sepH.SetColor(0x20FFFFFF)
        sepH.Show()
        self._DisableMousePick(sepH)
        self.headerElements.append(sepH)

        # ── Riga 2: Rank + Spendibili + Streak ──
        rankText = "[%s] %s" % (self.currentRankKey, t["title"])
        self.__HText(rankText, 20, 38, t["accent"])

        self.__HText("Spendibili", 250, 38, t["text_muted"])
        self.__HText(FormatNumber(self.playerData["spendable_points"]), 318, 38, 0xFFFFAA44)

        streak = self.playerData["login_streak"]
        bonus = self.playerData["streak_bonus"]
        if streak > 0 and bonus == 0:
            if streak >= 30: bonus = 20
            elif streak >= 7: bonus = 10
            elif streak >= 3: bonus = 5
        if streak > 0:
            self.__HText("Streak %dg +%d%%" % (streak, bonus), 400, 38, 0xFF44FF88)

        # ── Barra Progresso Rank – più elaborata ──
        barX, barY = 16, 62
        barW, barH = 300, 14

        # BG barra (sfondo scuro con bordo sottile)
        barBg = ui.Bar()
        barBg.SetParent(self.baseWindow)
        barBg.SetPosition(barX, barY)
        barBg.SetSize(barW, barH)
        barBg.SetColor(0xFF060610)
        barBg.Show()
        self._DisableMousePick(barBg)
        self.headerElements.append(barBg)

        # Bordi barra (top/left brillanti)
        barBorderT = ui.Bar(); barBorderT.SetParent(self.baseWindow); barBorderT.SetPosition(barX, barY); barBorderT.SetSize(barW, 1); barBorderT.SetColor(0xFF333355); barBorderT.Show(); self._DisableMousePick(barBorderT); self.headerElements.append(barBorderT)
        barBorderL = ui.Bar(); barBorderL.SetParent(self.baseWindow); barBorderL.SetPosition(barX, barY); barBorderL.SetSize(1, barH); barBorderL.SetColor(0xFF333355); barBorderL.Show(); self._DisableMousePick(barBorderL); self.headerElements.append(barBorderL)

        # Fill barra progresso
        fillW = max(1, int(barW * progress / 100))
        barFill = ui.Bar()
        barFill.SetParent(self.baseWindow)
        barFill.SetPosition(barX, barY)
        barFill.SetSize(fillW, barH)
        barFill.SetColor(t["bar_fill"])
        barFill.Show()
        self._DisableMousePick(barFill)
        self.headerElements.append(barFill)

        # Highlight fill (effetto brillantezza cima)
        if fillW > 4:
            barHL = ui.Bar(); barHL.SetParent(self.baseWindow); barHL.SetPosition(barX, barY); barHL.SetSize(fillW, 2); barHL.SetColor(0x25FFFFFF); barHL.Show(); self._DisableMousePick(barHL); self.headerElements.append(barHL)

        # Testo % progresso e prossimo rank
        self.__HText("%d%%" % int(progress), barX + barW + 6, 61, t["accent"])

        nextKey = self.__GetNextRankKey()
        if nextKey:
            nextTheme = RANK_THEMES[nextKey]
            self.__HText("->", barX + barW + 38, 61, t["text_muted"])
            self.__HText(nextTheme["name"], barX + barW + 52, 61, nextTheme.get("accent", 0xFFFFFFFF))
        else:
            self.__HText("MONARCA", barX + barW + 6, 61, GOLD_COLOR)

        # Separatore finale header
        sepH2 = ui.Bar()
        sepH2.SetParent(self.baseWindow)
        sepH2.SetPosition(16, 82)
        sepH2.SetSize(WINDOW_WIDTH - 32, 1)
        sepH2.SetColor(t["glow_strong"] if "glow_strong" in t else 0x30FFFFFF)
        sepH2.Show()
        self._DisableMousePick(sepH2)
        self.headerElements.append(sepH2)
    
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

        # Reset shop mode quando si esce dalla tab shop
        if self.currentTab == 2 and idx != 2:
            self.shopMode = "selector"

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
        # Nascondi il tooltip guida se visibile (previene tooltip orfano su schermo)
        try:
            tip = _GetGuideTooltip()
            tip.HideTip()
        except:
            pass

        for e in self.contentElements:
            try:
                if hasattr(e, 'SetEvent'):
                    e.SetEvent(None)
                # Pulisci riferimenti GuideHoverBar per GC
                if hasattr(e, 'tipLines'):
                    e.tipLines = None
                    e.tipTitle = None
                    e.tipTitleColor = None
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
        
        try:
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
        except:
            import dbg
            dbg.TraceError("__LoadTabContent: exception in tab=%d" % idx)
        
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
                oy = e._oy if hasattr(e, '_oy') else e.GetLocalPosition()[1]
                # Usa GetHeight se disponibile, altrimenti fallback 20px
                # Per TextLine: GetHeight potrebbe non esistere, quindi fallback
                h = 20
                try:
                    h = e.GetHeight()
                    if h <= 0:
                        h = 20
                except:
                    h = 20
                maxY = max(maxY, oy + h)
            except:
                pass
        self.totalContentHeight = maxY
        if maxY > CONTENT_HEIGHT - 10:
            self.scrollBar.Show()
            self.scrollBar.SetPos(0)
        else:
            self.scrollBar.Hide()
        # Clip iniziale diretto: nascondi tutto cio' che esce dall'area visibile
        for e in self.contentElements:
            try:
                oy = e._oy if hasattr(e, '_oy') else e.GetLocalPosition()[1]
                if oy < -30 or oy > CONTENT_HEIGHT:
                    e.Hide()
            except:
                pass
    
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
        t.SetPosition(int(x), int(y))
        t.SetText(str(txt))
        t.SetPackedFontColor(col)
        t._oy = int(y)  # Salva posizione originale subito
        if y >= -30 and y <= CONTENT_HEIGHT:
            t.Show()
        self._DisableMousePick(t)
        self.contentElements.append(t)
        return t
    
    def __CBar(self, x, y, w, h, col):
        b = ui.Bar()
        b.SetParent(self.contentPanel)
        b.SetPosition(int(x), int(y))
        b.SetSize(int(w), int(h))
        b.SetColor(col)
        b._oy = int(y)  # Salva posizione originale subito
        if y >= -30 and y <= CONTENT_HEIGHT:
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

    def __CTextTip(self, txt, x, y, col, tipTitle, tipColor, tipLines, w=420, h=18):
        """Crea un testo con area hover che mostra un tooltip dettagliato.
        tipLines = lista di stringhe o tuple (testo, colore). Usa '---' per separatore."""
        inView = (y >= -30 and y <= CONTENT_HEIGHT)
        # Testo visibile
        t = ui.TextLine()
        t.SetParent(self.contentPanel)
        t.SetPosition(int(x), int(y))
        t.SetText(str(txt))
        t.SetPackedFontColor(col)
        t.AddFlag("not_pick")
        t._oy = int(y)
        if inView:
            t.Show()
        self.contentElements.append(t)

        # Icona [?] a destra del testo come indicatore
        qMark = ui.TextLine()
        qMark.SetParent(self.contentPanel)
        qMark.SetPosition(int(x + len(str(txt)) * 6 + 8), int(y))
        qMark.SetText("[?]")
        qMark.SetPackedFontColor(0xFF888888)
        qMark.AddFlag("not_pick")
        qMark._oy = int(y)
        if inView:
            qMark.Show()
        self.contentElements.append(qMark)

        # Area hover trasparente sopra il testo
        hoverBar = GuideHoverBar(tipTitle, tipColor, tipLines)
        hoverBar.SetParent(self.contentPanel)
        hoverBar.SetPosition(int(x), int(y))
        hoverBar.SetSize(int(w), int(h))
        hoverBar.SetColor(0x00000000)  # Trasparente
        hoverBar._oy = int(y)
        if inView:
            hoverBar.Show()
        self.contentElements.append(hoverBar)

        return t
    
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
        # PROGRESSO VERSO PROSSIMO RANK (basato su rank confermato, non dai punti)
        # ============================================================
        total_glory = self.playerData["total_points"]
        
        # FIX: Calcola progresso basandosi sul rank confermato dal server
        confirmedRank = self.playerData.get("hunter_rank", "")
        if not confirmedRank or confirmedRank not in RANK_THEMES:
            confirmedRank = GetRankKey(total_glory)
        
        # Soglia della prossima prova basata sul rank confermato
        rank_next_trial = {
            "E": ("D", 2000), "D": ("C", 10000), "C": ("B", 50000),
            "B": ("A", 150000), "A": ("S", 500000), "S": ("N", 1500000), "N": (None, None)
        }
        next_rank_name, next_rank_glory = rank_next_trial.get(confirmedRank, (None, None))
        
        # Calcola progresso dalla soglia attuale alla prossima
        rank_current_threshold = {"E": 0, "D": 2000, "C": 10000, "B": 50000, "A": 150000, "S": 500000, "N": 1500000}
        current_threshold = rank_current_threshold.get(confirmedRank, 0)
        
        if next_rank_glory and next_rank_glory > current_threshold:
            progress = min(100.0, max(0.0, float(total_glory - current_threshold) / float(next_rank_glory - current_threshold) * 100))
        elif confirmedRank == "N":
            progress = 100.0
        else:
            progress = 0.0

        self.__CBar(5, y, 420, 45, t["bg_dark"])
        self.__CText(T("STATS_PROGRESS", "PROGRESSO RISVEGLIO:"), 15, y + 5, t["accent"])
        self.__CProgressBar(15, y + 22, 340, 14, progress, t["bar_fill"])
        self.__CText("%d%%" % int(progress), 365, y + 21, t["accent"])

        if next_rank_name and next_rank_glory:
            missing = next_rank_glory - total_glory
            next_theme = RANK_THEMES[next_rank_name]
            if missing > 0:
                self.__CText(T("NEXT_RANK", "Prova [%s]: %s Gloria richiesti" % (next_rank_name, FormatNumber(next_rank_glory))), 15, y + 38, next_theme["accent"])
                self.__CText(T("MISSING_GLORY", "(-" + FormatNumber(missing) + " Gloria)"), 280, y + 38, 0xFFFFAA55)
            else:
                # Ha abbastanza Gloria ma non ha fatto la prova
                self.__CText(T("TRIAL_READY", "Prova [%s] disponibile! Parla col Maestro!" % next_rank_name), 15, y + 38, 0xFFFFD700)
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
        # POWER RANK (valori reali del server, usati per le fratture)
        # ============================================================
        # Power Rank REALI: devono corrispondere a POWER_RANK_VALUES nel server
        # E=1, D=5, C=15, B=40, A=80, S=150, N=250
        power_rank_values = {"E": 1, "D": 5, "C": 15, "B": 40, "A": 80, "S": 150, "N": 250}
        power_level = power_rank_values.get(self.currentRankKey, 1)
        power_rank = self.currentRankKey or "E"

        self.__CText(T("POWER_LEVEL", "LIVELLO DI POTERE"), 5, y, t["accent"])
        y += 22
        self.__CBar(5, y, 420, 35, 0x22440000)
        self.__CText(T("POWER_VALUE", "Rango: %s | Potere: %s" % (power_rank, FormatNumber(power_level))), 15, y + 3, GOLD_COLOR)

        # Calcola bonus totale giornaliero (rank bonus + streak)
        # streak_bonus arriva già come percentuale (12, non 0.12)
        # Bonus Gloria da DB: E=0%, D=2%, C=4%, B=6%, A=9%, S=13%, N=18%
        rank_bonuses = {"N": 1.18, "S": 1.13, "A": 1.09, "B": 1.06, "C": 1.04, "D": 1.02, "E": 1.0}
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
        y += 28

        self.__CSep(5, y)
        y += 15

        # ============================================================
        # CORAGGIO (anti-farm dungeon)
        # ============================================================
        courage = self.playerData.get("hunter_courage", 100)
        if courage <= 0:
            courage_color = 0xFFFF4444  # Rosso - bloccato
            courage_label = "BLOCCATO"
        elif courage <= 20:
            courage_color = 0xFFFF8800  # Arancione - basso
            courage_label = "BASSO"
        elif courage <= 50:
            courage_color = 0xFFFFAA55  # Giallo - medio
            courage_label = "MEDIO"
        else:
            courage_color = 0xFF00FF88  # Verde - ok
            courage_label = "OK"

        self.__CText(T("STATS_COURAGE", "[ CORAGGIO ]"), 5, y, 0xFFFF6666)
        y += 22
        self.__CBar(5, y, 420, 30, 0x22440000)
        self.__CText(T("COURAGE_VALUE", "Coraggio: %d%%" % courage), 15, y + 7, courage_color)
        self.__CProgressBar(160, y + 9, 200, 12, courage, courage_color)
        self.__CText(courage_label, 370, y + 7, courage_color)
    
    def __GetItemIcon(self, vnum):
        """Carica icona item dal vnum. Ritorna path o None."""
        try:
            item.SelectItem(int(vnum))
            iconPath = item.GetIconImageFileName()
            if iconPath and len(iconPath) > 4:
                return iconPath
        except:
            pass
        return None

    def __CreateShopIcon(self, x, y, vnum, withTooltip=True):
        """Crea un ImageBox con l'icona dell'item nel contentPanel, con tooltip hover opzionale."""
        iconPath = self.__GetItemIcon(vnum)
        if not iconPath:
            # Fallback: quadrato colorato con "?"
            self.__CBar(x, y, 32, 32, 0xFF222244)
            self.__CText("?", x + 12, y + 8, 0xFF888888)
            return
        try:
            img = ui.ImageBox()
            img.SetParent(self.contentPanel)
            img.SetPosition(int(x), int(y))
            img.AddFlag("not_pick")
            img.LoadImage(iconPath)
            img._oy = int(y)
            if y >= -30 and y <= CONTENT_HEIGHT:
                img.Show()
            self.contentElements.append(img)
            # Hover tooltip per icona
            if withTooltip:
                hoverBar = ShopIconHoverBar(vnum)
                hoverBar.SetParent(self.contentPanel)
                hoverBar.SetPosition(int(x), int(y))
                hoverBar.SetSize(32, 32)
                hoverBar.SetColor(0x00000000)
                hoverBar._oy = int(y)
                if y >= -30 and y <= CONTENT_HEIGHT:
                    hoverBar.Show()
                self.contentElements.append(hoverBar)
        except:
            self.__CBar(x, y, 32, 32, 0xFF222244)
            self.__CText("?", x + 12, y + 8, 0xFF888888)

    def __LoadShop(self):
        """Router: mostra il selettore o la sotto-sezione shop attiva."""
        if self.shopMode == "normal":
            self.__LoadShopNormal()
        elif self.shopMode == "chests":
            self.__LoadShopChests()
        else:
            self.__LoadShopSelector()

    def __LoadShopSelector(self):
        """Pagina di selezione con 2 pulsanti: Mercante Hunter e Scrigni Hunter."""
        t = self.theme
        y = 5

        # === HEADER ===
        self.__CBar(5, y, 420, 28, 0xFF080812)
        self.__CBar(5, y, 420, 2, t["accent"])
        self.__CText(T("SHOP_SELECT_TITLE", "EMPORIO HUNTER"), 155, y + 6, t["accent"])
        y += 35

        # Gloria disponibile
        self.__CBar(5, y, 420, 24, t["bg_dark"])
        self.__CText(T("SHOP_GLORY_AVAILABLE", "Gloria Spendibile:"), 15, y + 5, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["spendable_points"]), 160, y + 5, 0xFFFFA500)
        self.__CText(T("GLORY", "Gloria"), 160 + len(FormatNumber(self.playerData["spendable_points"])) * 7 + 5, y + 5, 0xFFCC8800)
        y += 32

        self.__CSep(5, y)
        y += 15

        # Testo introduttivo
        self.__CText("Scegli quale sezione dello shop visitare:", 60, y, t["text_muted"])
        y += 25

        # ============================================================
        # CARD 1: MERCANTE HUNTER (shop normale)
        # ============================================================
        cardH = 80
        self.__CBar(20, y, 390, cardH, 0xFF0d0d1a)
        self.__CBar(20, y, 4, cardH, 0xFF00BFFF)  # Bordo sinistro cyan
        self.__CBar(20, y, 390, 2, 0xFF00BFFF)     # Bordo superiore cyan
        self.__CBar(20, y + cardH - 2, 390, 2, 0xFF003344)
        # Icona decorativa
        self.__CBar(35, y + 15, 50, 50, 0xFF0a1520)
        self.__CText("[M]", 50, y + 30, 0xFF00BFFF)
        # Titolo e descrizione
        self.__CText("MERCANTE HUNTER", 100, y + 15, 0xFF00DDFF)
        self.__CText("Equipaggiamento, potenziamenti e materiali", 100, y + 35, 0xFF7799AA)
        self.__CText("%d oggetti disponibili" % len(self.shopData), 100, y + 52, 0xFF556677)
        # Bottone
        btn1 = SoloLevelingButton()
        btn1.Create(self.contentPanel, 310, y + 28, 85, 24, "Entra", t)
        btn1.SetEvent(ui.__mem_func__(self.__OnShopSelectNormal))
        btn1._oy = int(y + 28)
        self.contentElements.append(btn1)
        y += cardH + 12

        # ============================================================
        # CARD 2: SCRIGNI HUNTER (chest shop - piu' appariscente)
        # ============================================================
        cardH = 80
        self.__CBar(20, y, 390, cardH, 0xFF120a1e)
        self.__CBar(20, y, 4, cardH, 0xFFCC44FF)  # Bordo sinistro viola
        self.__CBar(20, y, 390, 2, 0xFFCC44FF)     # Bordo superiore viola
        self.__CBar(20, y + cardH - 2, 390, 2, 0xFF331144)
        # Icona decorativa
        self.__CBar(35, y + 15, 50, 50, 0xFF1a0a28)
        self.__CText("[S]", 50, y + 30, 0xFFCC44FF)
        # Titolo e descrizione
        self.__CText("SCRIGNI HUNTER", 100, y + 15, 0xFFDD66FF)
        self.__CText("Bauli speciali, materiali rari e tesori", 100, y + 35, 0xFF9966AA)
        chestCount = len(self.chestShopData)
        self.__CText("%d scrigni disponibili" % chestCount, 100, y + 52, 0xFF776688)
        # Etichetta NUOVO se ci sono scrigni
        if chestCount > 0:
            self.__CBar(350, y + 8, 50, 16, 0xFFCC44FF)
            self.__CText("NUOVO!", 354, y + 9, 0xFF000000)
        # Bottone
        btn2 = SoloLevelingButton()
        btn2.Create(self.contentPanel, 310, y + 28, 85, 24, "Entra", t)
        btn2.SetEvent(ui.__mem_func__(self.__OnShopSelectChests))
        btn2._oy = int(y + 28)
        self.contentElements.append(btn2)
        y += cardH + 12

        # Nota in basso
        self.__CText("Passa il mouse sulle icone per vedere i dettagli", 80, y + 5, 0xFF444455)

    def __OnShopSelectNormal(self):
        self.shopMode = "normal"
        self.__ClearContent()
        self.__LoadShopNormal()
        self.__SavePositions()
        self.__UpdateScroll()

    def __OnShopSelectChests(self):
        self.shopMode = "chests"
        self.__ClearContent()
        self.__LoadShopChests()
        self.__SavePositions()
        self.__UpdateScroll()

    def __OnShopBack(self):
        self.shopMode = "selector"
        self.__ClearContent()
        self.__LoadShopSelector()
        self.__SavePositions()
        self.__UpdateScroll()

    def __LoadShopNormal(self):
        """Shop normale - logica originale del Mercante Hunter."""
        t = self.theme
        y = 5

        # Header + bottone indietro
        self.__CBar(5, y, 420, 28, 0xFF080812)
        self.__CBar(5, y, 420, 2, t["accent"])
        self.__CText(T("SHOP_TITLE", "MERCANTE HUNTER"), 150, y + 6, t["accent"])
        backBtn = SoloLevelingButton()
        backBtn.Create(self.contentPanel, 10, y + 3, 60, 22, "< Indietro", t)
        backBtn.SetEvent(ui.__mem_func__(self.__OnShopBack))
        backBtn._oy = int(y + 3)
        self.contentElements.append(backBtn)
        y += 32

        # Gloria disponibile con badge
        self.__CBar(5, y, 420, 24, t["bg_dark"])
        self.__CText(T("SHOP_GLORY_AVAILABLE", "Gloria Spendibile:"), 15, y + 5, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["spendable_points"]), 160, y + 5, 0xFFFFA500)
        self.__CText(T("GLORY", "Gloria"), 160 + len(FormatNumber(self.playerData["spendable_points"])) * 7 + 5, y + 5, 0xFFCC8800)
        y += 30

        self.__CSep(5, y)
        y += 10

        if not self.shopData:
            self.__CBar(5, y + 20, 420, 60, 0xFF0a0a14)
            self.__CText(T("SHOP_EMPTY", "Negozio vuoto."), 160, y + 40, t["text_muted"])
            self.__CText(T("SHOP_EMPTY_SUB", "Torna piu' tardi!"), 160, y + 58, 0xFF555555)
            return

        # Genera varianti x1/x10/x100 client-side da item base
        GLORIA_CAP = 1500000
        BULK_DISCOUNT = {1: 1.0, 10: 0.95, 100: 0.90}
        BULK_COLORS = {1: 0xFFCCCCCC, 10: 0xFF00CCFF, 100: 0xFFFF6600}

        for shopItem in self.shopData:
            itemId = shopItem.get("id", 0)
            vnum = shopItem.get("vnum", 0)
            basePrice = shopItem.get("price", 0)
            baseCount = shopItem.get("count", 1)
            name = shopItem.get("name", "Item").replace("+", " ")

            # Calcola varianti disponibili
            variants = []
            for mult in (1, 10, 100):
                bulkPrice = int(basePrice * mult * BULK_DISCOUNT[mult])
                if bulkPrice > GLORIA_CAP:
                    continue
                variants.append({"mult": mult, "count": baseCount * mult, "price": bulkPrice})

            # Card container
            numVariants = len(variants)
            cardH = 38 + numVariants * 22
            self.__CBar(5, y, 420, cardH, 0xFF0d0d1a)
            self.__CBar(5, y, 3, cardH, t["accent"])
            self.__CBar(5, y + cardH - 1, 420, 1, 0xFF1a1a2e)

            # Icona item (32x32) con tooltip
            self.__CreateShopIcon(14, y + 4, vnum)

            # Nome item + VNUM
            self.__CText(name[:28], 54, y + 4, t["text_value"])
            self.__CText("#%d" % vnum, 54, y + 19, 0xFF444466)

            # Righe varianti (x1, x10, x100)
            vy = y + 38
            for var in variants:
                mult = var["mult"]
                vCount = var["count"]
                vPrice = var["price"]
                canBuy = self.playerData["spendable_points"] >= vPrice

                qLabel = "x%d" % vCount
                qColor = BULK_COLORS.get(mult, 0xFFCCCCCC)

                # Sfondo riga
                rowBg = 0xFF0a0a14 if canBuy else 0xFF0a0008
                self.__CBar(54, vy, 370, 20, rowBg)

                # Quantita'
                self.__CText(qLabel, 58, vy + 2, qColor)

                # Prezzo
                priceCol = 0xFFFFA500 if canBuy else 0xFFFF4444
                self.__CText(FormatNumber(vPrice) + " Gloria", 100, vy + 2, priceCol)

                # Sconto (se x10 o x100)
                if mult > 1:
                    discount = int(round((1.0 - BULK_DISCOUNT[mult]) * 100))
                    self.__CText("-%d%%" % discount, 230, vy + 2, 0xFF00FF00)

                # Bottone compra — callback diretto per quantita'
                if canBuy:
                    if mult == 1:
                        self.__CButton(340, vy - 1, T("BTN_BUY", "Acquista"), ui.__mem_func__(self.__OnBuy), itemId)
                    elif mult == 10:
                        self.__CButton(340, vy - 1, T("BTN_BUY", "Acquista"), ui.__mem_func__(self.__OnBuy10), itemId)
                    elif mult == 100:
                        self.__CButton(340, vy - 1, T("BTN_BUY", "Acquista"), ui.__mem_func__(self.__OnBuy100), itemId)
                else:
                    self.__CText(T("SHOP_NO_FUNDS", "Gloria insufficiente"), 270, vy + 2, 0xFFFF4444)

                vy += 22

            y += cardH + 6

    def __LoadShopChests(self):
        """Shop Scrigni Hunter - sezione dedicata ai bauli."""
        t = self.theme
        y = 5

        # === HEADER ===
        self.__CBar(5, y, 420, 28, 0xFF0e0618)
        self.__CBar(5, y, 420, 2, 0xFFCC44FF)  # Viola
        self.__CText("SCRIGNI HUNTER", 155, y + 6, 0xFFDD66FF)
        backBtn = SoloLevelingButton()
        backBtn.Create(self.contentPanel, 10, y + 3, 60, 22, "< Indietro", t)
        backBtn.SetEvent(ui.__mem_func__(self.__OnShopBack))
        backBtn._oy = int(y + 3)
        self.contentElements.append(backBtn)
        y += 32

        # Gloria disponibile
        self.__CBar(5, y, 420, 24, 0xFF0a0614)
        self.__CText("Gloria Spendibile:", 15, y + 5, t["text_muted"])
        self.__CText(FormatNumber(self.playerData["spendable_points"]), 160, y + 5, 0xFFFFA500)
        self.__CText("Gloria", 160 + len(FormatNumber(self.playerData["spendable_points"])) * 7 + 5, y + 5, 0xFFCC8800)
        y += 30

        # Barra decorativa viola
        self.__CBar(5, y, 420, 1, 0xFFCC44FF)
        y += 8

        # Sottotitolo
        self.__CText("Sblocca tesori nascosti e materiali rari!", 80, y, 0xFF9966BB)
        y += 22

        if not self.chestShopData:
            self.__CBar(5, y + 10, 420, 70, 0xFF0e0618)
            self.__CBar(5, y + 10, 420, 2, 0xFF331144)
            self.__CText("Nessuno scrigno disponibile.", 120, y + 30, 0xFF776688)
            self.__CText("Torna piu' tardi, Cacciatore!", 120, y + 50, 0xFF554466)
            return

        # Tier config: colori per tier badge
        TIER_COLORS = {
            1: (0xFFC0C0C0, "T1", 0xFF888888),  # Argento
            2: (0xFF00CCFF, "T2", 0xFF0088AA),    # Cyan
            3: (0xFFCC44FF, "T3", 0xFF8822AA),    # Viola
            4: (0xFFFFD700, "T4", 0xFFCC9900),    # Oro
        }

        GLORIA_CAP = 1500000
        BULK_DISCOUNT = {1: 1.0, 10: 0.95, 100: 0.90}
        MULT_COLORS = {1: 0xFFCCCCCC, 10: 0xFF00CCFF, 100: 0xFFFF6600}

        for chestItem in self.chestShopData:
            itemId = chestItem.get("id", 0)
            vnum = chestItem.get("vnum", 0)
            basePrice = chestItem.get("price", 0)
            baseCount = chestItem.get("count", 1)
            name = chestItem.get("name", "Scrigno").replace("+", " ")
            tier = chestItem.get("tier", 1)

            tierCol, tierLabel, tierBorder = TIER_COLORS.get(tier, TIER_COLORS[1])

            # Calcola varianti
            variants = []
            for mult in (1, 10, 100):
                bulkPrice = int(basePrice * mult * BULK_DISCOUNT[mult])
                if bulkPrice > GLORIA_CAP:
                    continue
                variants.append({"mult": mult, "count": baseCount * mult, "price": bulkPrice})

            numVariants = len(variants)
            cardH = 42 + numVariants * 22

            # Card con bordo tier
            self.__CBar(5, y, 420, cardH, 0xFF0e0618)
            self.__CBar(5, y, 4, cardH, tierCol)                     # Bordo sinistro tier
            self.__CBar(5, y, 420, 1, tierBorder)                    # Linea top
            self.__CBar(5, y + cardH - 1, 420, 1, 0xFF1a0a2e)       # Linea bottom

            # Tier badge
            self.__CBar(375, y + 4, 40, 16, tierCol)
            self.__CText(tierLabel, 387, y + 5, 0xFF000000)

            # Icona item (32x32) con tooltip
            self.__CreateShopIcon(14, y + 6, vnum)

            # Nome scrigno
            self.__CText(name[:30], 54, y + 6, tierCol)
            self.__CText("#%d" % vnum, 54, y + 22, 0xFF443355)

            # Righe varianti (x1, x10, x100)
            vy = y + 42
            for var in variants:
                mult = var["mult"]
                vCount = var["count"]
                vPrice = var["price"]
                canBuy = self.playerData["spendable_points"] >= vPrice

                qLabel = "x%d" % vCount
                qColor = MULT_COLORS.get(mult, 0xFFCCCCCC)

                # Sfondo riga
                rowBg = 0xFF0a0614 if canBuy else 0xFF0a0008
                self.__CBar(54, vy, 370, 20, rowBg)

                # Quantita'
                self.__CText(qLabel, 58, vy + 2, qColor)

                # Prezzo
                priceCol = 0xFFFFA500 if canBuy else 0xFFFF4444
                self.__CText(FormatNumber(vPrice) + " Gloria", 100, vy + 2, priceCol)

                # Sconto
                if mult > 1:
                    discount = int(round((1.0 - BULK_DISCOUNT[mult]) * 100))
                    self.__CText("-%d%%" % discount, 230, vy + 2, 0xFF00FF00)

                # Bottone compra
                if canBuy:
                    if mult == 1:
                        self.__CButton(340, vy - 1, "Acquista", ui.__mem_func__(self.__OnBuyChest), itemId)
                    elif mult == 10:
                        self.__CButton(340, vy - 1, "Acquista", ui.__mem_func__(self.__OnBuyChest10), itemId)
                    elif mult == 100:
                        self.__CButton(340, vy - 1, "Acquista", ui.__mem_func__(self.__OnBuyChest100), itemId)
                else:
                    self.__CText("Gloria insufficiente", 270, vy + 2, 0xFFFF4444)

                vy += 22

            y += cardH + 6
    
    def __LoadRanking(self, rType):
        t = self.theme
        self.currentRankingView = rType
        y = 5

        # =====================================================
        # Determina categoria e periodo corrente
        # =====================================================
        catLabels = {
            "points": "GLORIA", "kills": "UCCISIONI",
            "fractures": "FRATTURE", "chests": "BAULI", "metins": "METIN"
        }
        catIcons = {
            "points": "[G]", "kills": "[K]",
            "fractures": "[F]", "chests": "[B]", "metins": "[M]"
        }
        catColors = {
            "points": GOLD_COLOR, "kills": 0xFFFF4444,
            "fractures": 0xFFCC44FF, "chests": 0xFF00BFFF, "metins": 0xFFFF8C00
        }
        currentCat = "points"
        for ck in catLabels:
            if ck in rType or rType == ck:
                currentCat = ck
                break
        
        periodLabels = {"daily": "OGGI", "weekly": "SETTIMANA", "total": "SEMPRE"}
        currentPeriod = "total"
        for pk in periodLabels:
            if pk in rType:
                currentPeriod = pk
                break
        if rType in ["fractures", "chests", "metins"]:
            currentPeriod = "total"
        
        activeCatColor = catColors.get(currentCat, GOLD_COLOR)

        # =====================================================
        # HEADER - Titolo con accent della categoria
        # =====================================================
        self.__CBar(5, y, 420, 30, 0xFF080812)
        self.__CBar(5, y, 420, 2, activeCatColor)
        self.__CBar(5, y + 28, 420, 2, 0x44000000)
        self.__CText("CLASSIFICA CACCIATORI", 120, y + 8, t["accent"])
        y += 34

        # =====================================================
        # RIGA CATEGORIE (5 bottoni)
        # =====================================================
        categories = [
            ("Gloria", "points"),
            ("Uccisioni", "kills"),
            ("Fratture", "fractures"),
            ("Bauli", "chests"),
            ("Metin", "metins"),
        ]
        catX = 5
        catBtnW = 80
        for catLabel, catKey in categories:
            if catKey in ["fractures", "chests", "metins"]:
                targetType = catKey
                isActive = (rType == catKey)
            else:
                targetType = currentPeriod + "_" + catKey
                isActive = (currentCat == catKey)
            
            btn = self.__CButton(catX, y, catLabel, ui.__mem_func__(self.__OnRankSub), targetType)
            if isActive:
                btn.Down()
            catX += catBtnW + 4
        y += 26

        # =====================================================
        # RIGA PERIODO (solo per Gloria e Uccisioni)
        # =====================================================
        if currentCat in ["points", "kills"]:
            periods = [
                ("Oggi", "daily"),
                ("Settimana", "weekly"),
                ("Sempre", "total"),
            ]
            pX = 5
            for pLabel, pKey in periods:
                if currentCat == "kills":
                    targetType = pKey + "_kills"
                else:
                    targetType = pKey + "_points"
                isActive = (currentPeriod == pKey)
                btn = self.__CButton(pX, y, pLabel, ui.__mem_func__(self.__OnRankPeriod), targetType)
                if isActive:
                    btn.Down()
                pX += 85
            y += 26
        
        y += 2

        # =====================================================
        #  LA TUA POSIZIONE - Card premium a due righe
        # =====================================================
        if "daily" in rType:
            myPos = self.playerData.get("daily_pos", 0)
        elif "weekly" in rType:
            myPos = self.playerData.get("weekly_pos", 0)
        else:
            myPos = self.playerData.get("daily_pos", 0)
        
        myPts = self.playerData.get("total_points", 0)
        confirmedRank = self.playerData.get("hunter_rank", "")
        myRank = confirmedRank if (confirmedRank and confirmedRank in RANK_THEMES) else GetRankKey(myPts)
        myTheme = RANK_THEMES[myRank]
        
        cardH = 44
        # Sfondo scuro con glow del rank
        self.__CBar(5, y, 420, cardH, 0xFF0A0A16)
        # Bordo laterale con colore rank (4px)
        self.__CBar(5, y, 4, cardH, myTheme["accent"])
        # Bordo superiore sottile
        self.__CBar(5, y, 420, 1, myTheme["border"])
        # Bordo inferiore sottile
        self.__CBar(5, y + cardH - 1, 420, 1, myTheme["border"])
        # Glow interno laterale (effetto luce dal bordo)
        self.__CBar(9, y + 1, 30, cardH - 2, myTheme["glow"])
        
        # Badge rank grande
        badgeW, badgeH = 28, 22
        badgeX, badgeY = 16, y + 11
        self.__CBar(badgeX, badgeY, badgeW, badgeH, myTheme["accent"])
        self.__CBar(badgeX, badgeY, badgeW, 1, 0x55FFFFFF)  # highlight top
        self.__CText(myRank, badgeX + 8, badgeY + 4, 0xFF000000)
        
        # Nome + rank title
        nameX = 52
        playerName = str(self.playerData.get("name", "-"))
        self.__CText(playerName, nameX, y + 6, 0xFFFFFFFF)
        self.__CText(myTheme.get("name", ""), nameX, y + 21, myTheme["accent"])
        
        # Posizione prominente
        posX = 200
        if myPos > 0:
            posLabel = "#%d" % myPos
            if myPos == 1:
                posColor = GOLD_COLOR
                posDesc = "1* POSTO!"
            elif myPos == 2:
                posColor = SILVER_COLOR
                posDesc = "2* Posto"
            elif myPos == 3:
                posColor = BRONZE_COLOR
                posDesc = "3* Posto"
            elif myPos <= 10:
                posColor = 0xFF88BBFF
                posDesc = "Top 10"
            else:
                posColor = t["text_value"]
                posDesc = ""
            self.__CText(posLabel, posX, y + 6, posColor)
            if posDesc:
                self.__CText(posDesc, posX, y + 21, posColor)
        else:
            self.__CText("---", posX, y + 6, t["text_muted"])
            self.__CText("Non classificato", posX, y + 21, t["text_muted"])
        
        # Valore con label categoria + daily gain
        valX = 310
        myVal = myPts
        valUnit = "Gloria"
        if currentCat == "kills":
            myVal = self.playerData.get("daily_kills", 0) if currentPeriod == "daily" else self.playerData.get("total_kills", 0)
            valUnit = "Uccisioni"
        elif currentCat == "fractures":
            myVal = self.playerData.get("total_fractures", 0)
            valUnit = "Fratture"
        elif currentCat == "chests":
            myVal = self.playerData.get("total_chests", 0)
            valUnit = "Bauli"
        elif currentCat == "metins":
            myVal = self.playerData.get("total_metins", 0)
            valUnit = "Metin"
        
        self.__CText(FormatNumber(myVal), valX, y + 4, GOLD_COLOR)
        self.__CText(valUnit, valX, y + 19, t["text_muted"])
        
        # Guadagno giornaliero (solo per gloria)
        if currentCat == "points":
            dailyGain = self.playerData.get("daily_points", 0)
            if dailyGain > 0:
                self.__CText("+%s oggi" % FormatNumber(dailyGain), valX + 70, y + 4, 0xFF00FF88)
        
        y += cardH + 4
        
        # =====================================================
        # CLASSIFICA TOP 10
        # =====================================================
        data = self.rankingData.get(rType, [])
        if not data:
            if "points" in rType:
                data = self.rankingData.get("daily_points", self.rankingData.get("daily", []))
            elif "kills" in rType:
                data = self.rankingData.get("daily_kills", [])
        
        if not data:
            self.__CBar(5, y + 8, 420, 60, 0x15FFFFFF)
            self.__CText("Nessun dato ancora.", 140, y + 18, t["text_muted"])
            self.__CText("Caccia per scalare la classifica!", 110, y + 38, t["accent"])
            return

        # Header colonne
        valHeader = catLabels.get(currentCat, "Valore")
        self.__CBar(5, y, 420, 18, 0x22FFFFFF)
        self.__CText("#", 14, y + 2, t["text_muted"])
        self.__CText("Rk", 38, y + 2, t["text_muted"])
        self.__CText("Cacciatore", 68, y + 2, t["text_muted"])
        self.__CText(valHeader, 330, y + 2, t["text_muted"])
        y += 20
        
        # =====================================================
        # TOP 3 - Design Premium con medaglie e barra valore
        # =====================================================
        maxVal = 1
        if len(data) > 0:
            maxVal = max(1, data[0].get("value", data[0].get("points", 1)))
        
        for i in range(min(10, len(data))):
            e = data[i]
            val = e.get("value", e.get("points", 0))
            playerName = e.get("name", "-").replace("+", " ")
            
            playerGloria = e.get("points", val) if "kills" not in rType else e.get("points", 0)
            # FIX 03/03: Usa il rank CONFERMATO dal server (se presente), non quello calcolato dalla gloria
            confirmedPlayerRank = e.get("rank", "")
            if confirmedPlayerRank and confirmedPlayerRank in RANK_THEMES:
                playerRankKey = confirmedPlayerRank
            else:
                playerRankKey = GetRankKey(playerGloria)
            playerTheme = RANK_THEMES[playerRankKey]
            
            if i < 3:
                # ─── TOP 3: Card premium ───
                if i == 0:
                    medalCol = GOLD_COLOR
                    bgCol = 0x44FFD700
                    rowH = 32
                elif i == 1:
                    medalCol = SILVER_COLOR
                    bgCol = 0x33C0C0C0
                    rowH = 28
                else:
                    medalCol = BRONZE_COLOR
                    bgCol = 0x33CD7F32
                    rowH = 28
                
                # Sfondo con bordo laterale
                self.__CBar(5, y, 420, rowH, bgCol)
                self.__CBar(5, y, 3, rowH, medalCol)
                
                # Glow leggero
                self.__CBar(8, y + 1, 20, rowH - 2, 0x22FFFFFF)
                
                # Posizione (numero grande per #1)
                posY = y + (rowH - 14) // 2
                if i == 0:
                    self.__CText("#1", 12, posY, medalCol)
                elif i == 1:
                    self.__CText("#2", 12, posY, medalCol)
                else:
                    self.__CText("#3", 12, posY, medalCol)
                
                # Rank badge
                bx = 36
                self.__CBar(bx, posY - 1, 24, 18, playerTheme["accent"])
                self.__CBar(bx, posY - 1, 24, 1, 0x55FFFFFF)
                self.__CText(playerRankKey, bx + 7, posY, 0xFF000000)
                
                # Nome giocatore con colore medaglia
                self.__CText(playerName[:22], 68, posY, medalCol)
                
                # Barra valore proporzionale (background)
                barX, barW = 240, 100
                barPct = min(100, int(val * 100 / maxVal)) if maxVal > 0 else 0
                fillW = max(2, int(barW * barPct / 100))
                self.__CBar(barX, posY + 2, barW, 10, 0x33000000)
                self.__CBar(barX, posY + 2, fillW, 10, medalCol)
                
                # Valore numerico a destra
                self.__CText(FormatNumber(val), barX + barW + 8, posY, 0xFFFFFFFF)
                
                y += rowH + 2
            
            else:
                # ─── POSIZIONI 4-10: Design pulito ───
                rowH = 22
                # Alternanza sfondo
                if i % 2 == 0:
                    self.__CBar(5, y, 420, rowH, 0x11FFFFFF)
                
                # Posizione
                self.__CText(str(i + 1), 14, y + 4, t["text_value"])
                
                # Mini rank badge
                self.__CBar(34, y + 3, 20, 16, playerTheme["accent"])
                self.__CText(playerRankKey, 39, y + 4, 0xFF000000)
                
                # Nome
                self.__CText(playerName[:20], 62, y + 4, t["text_value"])
                
                # Mini barra proporzionale
                barX, barW = 250, 70
                barPct = min(100, int(val * 100 / maxVal)) if maxVal > 0 else 0
                fillW = max(1, int(barW * barPct / 100))
                self.__CBar(barX, y + 6, barW, 8, 0x22000000)
                self.__CBar(barX, y + 6, fillW, 8, t["border"])
                
                # Valore
                self.__CText(FormatNumber(val), barX + barW + 8, y + 4, t["accent"])
                
                y += rowH + 1
    
    def __OnRankPeriod(self, rType):
        """Cambia periodo mantenendo la categoria"""
        self.__ClearContent()
        self.__LoadRanking(rType)
        self.__SavePositions()
        self.__UpdateScroll()
    
    def __LoadAchievements(self):
        """
        TAB ACHIEVEMENT - Solo Leveling Style con categorie e paginazione
        Organizzato per categorie: COMBAT, GLORY, FRACTURE, CHEST, METIN, BOSS, MISSION, TRIAL, STREAK, RANK
        """
        t = self.theme
        y = 5
        
        # Categorie con nomi e colori Solo Leveling style
        CATEGORIES = [
            ("COMBAT", "COMBATTIMENTO", 0xFFFF4444, 1),
            ("GLORY", "GLORIA", 0xFFFFD700, 2),
            ("FRACTURE", "FRATTURE", 0xFF8B00FF, 3),
            ("CHEST", "BAULI", 0xFF00BFFF, 4),
            ("METIN", "METIN", 0xFFFF8C00, 5),
            ("BOSS", "BOSS", 0xFFDC143C, 6),
            ("MISSION", "MISSIONI", 0xFF00FF88, 7),
            ("TRIAL", "PROVE", 0xFFFF00FF, 8),
            ("STREAK", "COSTANZA", 0xFF00FFFF, 9),
            ("RANK", "RANGO", 0xFFFFFFFF, 10),
        ]
        
        # Header principale
        self.__CBar(5, y, 420, 35, 0xFF0A0A15)
        self.__CText("TRAGUARDI HUNTER", 130, y + 3, 0xFFFFD700)
        
        # Statistiche rapide
        if self.achievementsData:
            total = len(self.achievementsData)
            unlocked = sum(1 for a in self.achievementsData if a.get("unlocked", False))
            claimed = sum(1 for a in self.achievementsData if a.get("claimed", False))
            unclaimed = unlocked - claimed
            self.__CText("Completati: %d/%d" % (unlocked, total), 15, y + 18, 0xFF88FF88)
            if unclaimed > 0:
                self.__CText("DA RISCUOTERE: %d" % unclaimed, 280, y + 18, 0xFFFF4444)
        y += 42
        
        if not self.achievementsData:
            # FIX 02/03/2026: Auto-request achievements se dati mancanti
            # Causa: send_all_data() invia 18 cmdchat in rapida successione al login.
            # send_achievements e' il #13 nella coda — il buffer TCP puo' perdere
            # i pacchetti piu' tardivi. Questo auto-retry richiede SOLO gli achievements.
            now = app.GetTime()
            if now - self.lastAchievementsRequest > 5.0:
                self.lastAchievementsRequest = now
                try:
                    net.SendChatPacket("/hunter_request_achievements")
                except:
                    pass
            self.__CBar(5, y, 420, 60, 0x22440000)
            self.__CText("Nessun traguardo disponibile.", 130, y + 10, t["text_muted"])
            self.__CText("Caricamento in corso...", 150, y + 30, 0xFF888888)
            return
        
        # Organizza achievement per categoria (type)
        achByCategory = {}
        for a in self.achievementsData:
            aType = a.get("type", 1)
            if aType not in achByCategory:
                achByCategory[aType] = []
            achByCategory[aType].append(a)
        
        # Mostra ogni categoria
        for catKey, catName, catColor, catType in CATEGORIES:
            achievements = achByCategory.get(catType, [])
            if not achievements:
                continue
            
            # Conta statistiche categoria
            catTotal = len(achievements)
            catUnlocked = sum(1 for a in achievements if a.get("unlocked", False))
            catClaimed = sum(1 for a in achievements if a.get("claimed", False))
            catUnclaimed = catUnlocked - catClaimed
            
            # Header categoria
            self.__CBar(5, y, 420, 26, 0xFF151520)
            # Barra laterale colorata
            self.__CBar(5, y, 4, 26, catColor)
            
            # Nome categoria e conteggio
            self.__CText(catName, 15, y + 5, catColor)
            self.__CText("%d/%d" % (catUnlocked, catTotal), 370, y + 5, 0xFF888888)
            
            # Indicatore achievement da riscuotere
            if catUnclaimed > 0:
                self.__CBar(320, y + 4, 40, 18, 0x44FF0000)
                self.__CText("!%d" % catUnclaimed, 332, y + 5, 0xFFFF4444)
            y += 30
            
            # Mostra solo i primi 3 achievement non completati + tutti quelli sbloccati non riscossi
            # Questo limita il rendering a ~5-8 per categoria
            toShow = []
            
            # Prima: achievement sbloccati ma NON riscossi (priorità!)
            for a in achievements:
                if a.get("unlocked", False) and not a.get("claimed", False):
                    toShow.append(a)
            
            # Poi: prossimi achievement da sbloccare (max 2)
            notUnlocked = [a for a in achievements if not a.get("unlocked", False)]
            notUnlocked.sort(key=lambda x: x.get("requirement", 0))
            toShow.extend(notUnlocked[:2])
            
            # Rimuovi duplicati mantenendo ordine
            seen = set()
            uniqueShow = []
            for a in toShow:
                aid = a.get("id", 0)
                if aid not in seen:
                    seen.add(aid)
                    uniqueShow.append(a)
            
            # Se tutto completato, mostra gli ultimi 2 completati
            if not uniqueShow:
                completed = [a for a in achievements if a.get("claimed", False)]
                completed.sort(key=lambda x: x.get("requirement", 0), reverse=True)
                uniqueShow = completed[:2]
            
            # Renderizza achievement (max 5 per categoria)
            for a in uniqueShow[:5]:
                unlocked = a.get("unlocked", False)
                claimed = a.get("claimed", False)
                
                # Colore sfondo basato su stato
                if claimed:
                    bgCol = 0x22333333  # Grigio - completato
                elif unlocked:
                    bgCol = 0x3300FF44  # Verde - da riscuotere!
                else:
                    bgCol = 0x22000011  # Scuro - in corso
                
                self.__CBar(10, y, 410, 50, bgCol)  # Piu' alto per ricompense
                
                # Barra progresso sottile sul lato
                prg = a.get("progress", 0)
                req = a.get("requirement", 1)
                pct = min(100, (float(prg) / float(req)) * 100) if req > 0 else 0
                pctWidth = int(4 * pct / 100)
                if pctWidth > 0:
                    self.__CBar(10, y, pctWidth, 50, catColor if not claimed else 0xFF444444)
                
                # Nome achievement
                nameCol = 0xFF888888 if claimed else (0xFFFFFFFF if unlocked else 0xFFAAAAAA)
                name = a.get("name", "???").replace("+", " ")
                if len(name) > 28:
                    name = name[:25] + "..."
                self.__CText(name, 20, y + 3, nameCol)
                
                # Progresso
                progText = "%d/%d" % (min(prg, req), req)
                progCol = 0xFF00FF00 if unlocked else 0xFF888888
                self.__CText(progText, 20, y + 18, progCol)
                
                # Barra progresso mini
                self.__CProgressBar(100, y + 22, 120, 6, pct, catColor if not claimed else 0xFF444444)
                
                # Ricompense (riga sotto)
                rewardText = ""
                rvnum = a.get("reward_vnum", 0)
                rcount = a.get("reward_count", 1)
                ryang = a.get("reward_yang_vnum", 0)
                rycount = a.get("reward_yang_count", 1)
                
                if rvnum > 0:
                    rewardText = "Item x%d" % rcount
                if ryang > 0:
                    # Calcola yang totale dal lingotto
                    yangValue = YANG_INGOTS.get(ryang, 0) * rycount
                    if yangValue > 0:
                        yangStr = FormatYang(yangValue)
                        if rewardText:
                            rewardText += " + " + yangStr + " Yang"
                        else:
                            rewardText = yangStr + " Yang"
                
                if rewardText and not claimed:
                    self.__CText("Premio: " + rewardText, 20, y + 34, 0xFFFFD700)
                elif claimed:
                    self.__CText("Ritirato", 20, y + 34, 0xFF666666)
                
                # Pulsante azione
                if unlocked and not claimed:
                    # RISCUOTI - evidenziato
                    self.__CButton(320, y + 12, "RISCUOTI", ui.__mem_func__(self.__OnClaim), a.get("id", 0))
                elif claimed:
                    self.__CText("[OK]", 350, y + 16, 0xFF00AA00)
                else:
                    # Mostra percentuale
                    self.__CText("%d%%" % int(pct), 355, y + 16, 0xFF666666)
                
                y += 54  # Piu' spazio per le ricompense
            
            # Se ci sono altri achievement nascosti
            hidden = len(achievements) - len(uniqueShow)
            if hidden > 0:
                self.__CText("... e altri %d traguardi" % hidden, 150, y, 0xFF555555)
                y += 18
            
            y += 8  # Spazio tra categorie
    
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
        self.__CText(T("DAILY_MISSIONS_TITLE", "MISSIONI GIORNALIERE (Reset: 00:00)"), 15, y + 6, 0xFF00CCFF)
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
        self.__CText(T("RESET_MISSIONS", "Missioni: Ogni giorno alle 00:00"), 50, y + 20, 0xFFAAAAAA)
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
            (T("GUIDE_TAB_FAQ", "FAQ"), 5),
            (T("GUIDE_TAB_FRACTURES", "Fratture"), 6),
            (T("GUIDE_TAB_TRIAL", "Prove"), 7),
            (T("GUIDE_TAB_ITEMS", "Items"), 8),
            (T("GUIDE_TAB_ONLINE", "Online"), 9),
            (T("GUIDE_TAB_SUPREMO", "Supremo"), 10),
            (T("GUIDE_TAB_KARMA", "Karma"), 11),
        ]
        tabX = 5
        idx = 0
        for tabName, tabIdx in guideTabs:
            # Layout su tre righe (4 per riga)
            row = idx / 4
            col = idx % 4
            currentY = y + (row * 26)
            currentX = 5 + (col * 105)

            btn = self.__CButton(currentX, currentY, tabName, ui.__mem_func__(self.__OnGuideTab), tabIdx)
            if self.currentGuideTab == tabIdx:
                btn.Down()
            idx += 1
            
        y += 112 # Spazio per quattro righe (12 tab)
        
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
        elif self.currentGuideTab == 5:
            y = self.__LoadGuideFAQ(y)
        elif self.currentGuideTab == 6:
            y = self.__LoadGuideFractures(y)
        elif self.currentGuideTab == 7:
            y = self.__LoadGuideTrial(y)
        elif self.currentGuideTab == 8:
            y = self.__LoadGuideItems(y)
        elif self.currentGuideTab == 9:
            y = self.__LoadGuideOnline(y)
        elif self.currentGuideTab == 10:
            y = self.__LoadGuideSupremo(y)
        elif self.currentGuideTab == 11:
            y = self.__LoadGuideKarma(y)
    
    def __OnGuideTab(self, tabIdx):
        self.currentGuideTab = tabIdx
        self.__ClearContent()
        try:
            self.__LoadGuide()
        except:
            pass
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

            # Nome con tooltip
            tipLines = {
                "E": [("Bonus Gloria: +0%", 0xFF00FF00), ("Power Rank: 1", 0xFFFFD700), "---", ("Fratture facili, 3 ondate di difesa.", 0xFFCCCCCC), ("Cap Online: 1.500 Gloria/giorno.", 0xFF888888)],
                "D": [("Bonus Gloria: +2%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +10%", 0xFFFF6600), ("Bonus HP: +2.500", 0xFF00CCFF), ("Power Rank: 5", 0xFFFFD700), "---", ("Fratture D: 4 ondate di difesa.", 0xFFCCCCCC), ("Cap Online: 2.000 Gloria/giorno.", 0xFF888888)],
                "C": [("Bonus Gloria: +4%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +15%", 0xFFFF6600), ("Bonus HP: +5.000", 0xFF00CCFF), ("Power Rank: 15", 0xFFFFD700), "---", ("Sblocchi il Calibratore Fratture.", 0xFFCCCCCC), ("Fratture C: 4 ondate + Elite.", 0xFFCCCCCC), ("Cap Online: 2.500 Gloria/giorno.", 0xFF888888)],
                "B": [("Bonus Gloria: +6%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +25%", 0xFFFF6600), ("Bonus HP: +10.000", 0xFF00CCFF), ("Power Rank: 40", 0xFFFFD700), "---", ("Fratture B: 6 ondate + MiniBoss.", 0xFFCCCCCC), ("Se fallisci la difesa, frattura distrutta!", 0xFFFF6666), ("Cap Online: 3.000 Gloria/giorno.", 0xFF888888)],
                "A": [("Bonus Gloria: +9%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +35%", 0xFFFF6600), ("Bonus HP: +15.000", 0xFF00CCFF), ("Bonus Danni Finali: +3%", 0xFFFF4444), ("Power Rank: 80", 0xFFFFD700), "---", ("Sblocchi il Frammento di Monarca.", 0xFFCCCCCC), ("Fratture A: 9 ondate + Boss.", 0xFFCCCCCC), ("Cap Online: 4.000 Gloria/giorno.", 0xFF888888)],
                "S": [("Bonus Gloria: +13%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +50%", 0xFFFF6600), ("Bonus HP: +20.000", 0xFF00CCFF), ("Bonus Danni Finali: +5%", 0xFFFF4444), ("Power Rank: 150", 0xFFFFD700), "---", ("Contenuti TOP del gioco.", 0xFFCCCCCC), ("Fratture S: 12 ondate + Boss Finale!", 0xFFFF6666), ("Cap Online: 5.000 Gloria/giorno.", 0xFF888888)],
                "N": [("Bonus Gloria: +18%", 0xFF00FF00), ("Forte Mezziuomini/Mostri: +75%", 0xFFFF6600), ("Bonus HP: +30.000", 0xFF00CCFF), ("Bonus Danni Finali: +10%", 0xFFFF4444), ("Power Rank: 250", 0xFFFFD700), "---", ("Il rank piu' alto del gioco!", GOLD_COLOR), ("Fratture N: 15 ondate, estremamente difficili.", 0xFFFF4444), ("Cap Online: 6.000 Gloria/giorno.", 0xFF888888)],
            }
            self.__CTextTip(title, 50, y + 5, rt["accent"],
                key + "-RANK: " + title, rt["accent"], tipLines.get(key, []))

            # Range punti
            self.__CText("%s - %s %s" % (minPts, maxPts, T("GLORY", "Gloria")), 200, y + 5, rt["text_value"])
            
            # Descrizione
            self.__CText(desc, 15, y + 27, rt["text_muted"])
            
            y += 50

        # =====================================================
        # BONUS DI RANK (da tooltip)
        # =====================================================
        y += 10
        self.__CSep(5, y)
        y += 15

        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CTextTip(T("RANK_BONUS_TITLE", "BONUS PASSIVI PER RANK"), 130, y + 5, GOLD_COLOR,
            "Bonus di Rank", GOLD_COLOR, [
                ("Ogni Rank fornisce bonus PASSIVI permanenti!", 0xFFCCCCCC),
                "---",
                ("Bonus Gloria: % extra su TUTTA la Gloria.", 0xFF00FF00),
                ("Forte Mezziuomini/Mostri: danno extra.", 0xFFFF6600),
                ("Bonus HP: vita extra permanente.", 0xFF00CCFF),
                ("Bonus Danni Finali: solo da A-Rank!", 0xFFFF4444),
                ("Power Rank: necessario per fratture alte.", 0xFFFFD700),
            ], 260, 16)
        y += 38

        # Header tabella
        self.__CBar(5, y, 420, 22, 0x44FFFFFF)
        self.__CText("Rank", 10, y + 3, 0xFFFFFFFF)
        self.__CText("Gloria", 55, y + 3, 0xFFFFFFFF)
        self.__CText("Forte M/M", 110, y + 3, 0xFFFFFFFF)
        self.__CText("Bonus HP", 195, y + 3, 0xFFFFFFFF)
        self.__CText("Danni", 280, y + 3, 0xFFFFFFFF)
        self.__CText("PWR", 335, y + 3, 0xFFFFFFFF)
        y += 24

        rankBonuses = [
            ("E", "+0%",  "-",     "-",       "-",   "1",   0xFF888888),
            ("D", "+2%",  "+10%",  "+2.500",  "-",   "5",   0xFF00FF00),
            ("C", "+4%",  "+15%",  "+5.000",  "-",   "15",  0xFF0088FF),
            ("B", "+6%",  "+25%",  "+10.000", "-",   "40",  0xFFFF8800),
            ("A", "+9%",  "+35%",  "+15.000", "+3%", "80",  0xFFFF0000),
            ("S", "+13%", "+50%",  "+20.000", "+5%", "150", 0xFFFF00FF),
            ("N", "+18%", "+75%",  "+30.000", "+10%","250", 0xFFFFD700),
        ]

        for rank, gloria, forte, hp, danni, pwr, color in rankBonuses:
            self.__CBar(5, y, 420, 20, t["bg_dark"])
            self.__CBar(5, y, 4, 20, color)
            self.__CText(rank, 15, y + 2, color)
            self.__CText(gloria, 55, y + 2, 0xFF00FF00)
            self.__CText(forte, 115, y + 2, 0xFFFF6600)
            self.__CText(hp, 195, y + 2, 0xFF00CCFF)
            self.__CText(danni, 280, y + 2, 0xFFFF4444 if danni != "-" else t["text_muted"])
            self.__CText(pwr, 340, y + 2, 0xFFFFD700)
            y += 22

        y += 8
        self.__CText(T("RANK_BONUS_NOTE1", "Bonus Danni Finali disponibile solo da A-Rank in su!"), 50, y, 0xFFFF4444)
        y += 16
        self.__CText(T("RANK_BONUS_NOTE2", "I bonus si applicano AUTOMATICAMENTE quando sali di Rank."), 30, y, t["text_muted"])
        y += 20

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
            (T("GLORY_METHOD_FRACTURES", "Fratture Dimensionali"), "+50-2000", T("GLORY_METHOD_FRACTURES_DESC", "Boss/Metin Elite (base pts da DB)")),
            (T("GLORY_METHOD_MISSIONS", "Missioni Giornaliere"), "+50-3000", T("GLORY_METHOD_MISSIONS_DESC", "3 missioni al giorno (reward scala col Rank)")),
            (T("GLORY_METHOD_EMERGENCY", "Emergency Quest"), "+150-1200", T("GLORY_METHOD_EMERGENCY_DESC", "10% chance dopo ~9000 kill normali")),
            (T("GLORY_METHOD_EVENTS", "Eventi Programmati"), "+100-2000", T("GLORY_METHOD_EVENTS_DESC", "Glory Rush, Metin Frenzy, Boss Massacre...")),
            (T("GLORY_METHOD_STREAK", "Streak Login"), "+3/7/12%", T("GLORY_METHOD_STREAK_DESC", "3gg=+3%, 7gg=+7%, 30gg=+12% Gloria")),
            (T("GLORY_METHOD_CHESTS", "Bauli Hunter"), "+20-100", T("GLORY_METHOD_CHESTS_DESC", "Bauli spawn nelle mappe normali")),
            (T("GLORY_METHOD_SPEEDKILL", "Speed Kill Bonus"), "+80/+200", T("GLORY_METHOD_SPEEDKILL_DESC", "Boss 60s = +200, Metin 5min = +80 Gloria")),
        ]

        gloryTips = {
            T("GLORY_METHOD_FRACTURES", "Fratture Dimensionali"): [
                ("Le fratture spawnano dopo ~9000 kill normali.", 0xFFCCCCCC),
                ("Dentro trovi Boss, Super Metin o Bauli.", 0xFFCCCCCC),
                "---",
                ("Entrare = piu' Gloria (difesa + portale).", 0xFF00FF00),
                ("Sigillare = Gloria base senza combattere.", 0xFFFFAA00),
                ("Ricompense: E=500-1500 fino a N=20000-50000", 0xFFFFD700),
            ],
            T("GLORY_METHOD_MISSIONS", "Missioni Giornaliere"): [
                ("3 missioni al giorno, reset a mezzanotte.", 0xFFCCCCCC),
                ("Tipi: kill mob, metin, boss, raccolta.", 0xFFCCCCCC),
                "---",
                ("NOVITA': PROGRESSO CONDIVISO!", 0xFF00FF00),
                ("Se sei in gruppo o vicino a un player", 0xFF00FF00),
                ("che completa una missione, il progresso", 0xFF00FF00),
                ("viene condiviso anche a te!", 0xFF00FF00),
                "---",
                ("Bonus +50% se completi tutte e 3!", 0xFFFFD700),
                ("Penalita' se non le completi entro 00:00.", 0xFFFF6666),
            ],
            T("GLORY_METHOD_EMERGENCY", "Emergency Quest"): [
                ("Spawn random dopo ~9000 kill mob normali.", 0xFFCCCCCC),
                ("10% chance Emergency, 90% Frattura.", 0xFFCCCCCC),
                "---",
                ("5 livelli: EASY, NORMAL, HARD, EXTREME, GOD", 0xFFFFAA00),
                ("Tempo limitato: 60-180 secondi!", 0xFFFF6666),
                ("GOD MODE: 250 kill in 180s = +1200 Gloria!", 0xFFFFD700),
            ],
            T("GLORY_METHOD_EVENTS", "Eventi Programmati"): [
                ("Eventi automatici ogni giorno dal DB.", 0xFFCCCCCC),
                ("Iscrizione AUTOMATICA, basta essere online.", 0xFF00FF00),
                "---",
                ("Tipi: Glory Rush, Metin Frenzy,", 0xFFCCCCCC),
                ("Boss Massacre, PvP Tournament,", 0xFFCCCCCC),
                ("Fracture Storm, King of Kill, Treasure Hunt.", 0xFFCCCCCC),
                "---",
                ("'Primo vince' = primo a completare vince!", 0xFFFFD700),
            ],
            T("GLORY_METHOD_STREAK", "Streak Login"): [
                ("Accedi ogni giorno consecutivamente!", 0xFFCCCCCC),
                "---",
                ("3 giorni = +3% Gloria bonus", 0xFF00FF00),
                ("7 giorni = +7% Gloria bonus", 0xFF00FF00),
                ("30 giorni = +12% Gloria bonus", 0xFFFFD700),
                "---",
                ("Si applica a TUTTE le fonti di Gloria.", 0xFFCCCCCC),
                ("Visibile nel dettaglio syschat.", 0xFF888888),
            ],
            T("GLORY_METHOD_CHESTS", "Bauli Hunter"): [
                ("Spawnano nelle mappe normali o da portali.", 0xFFCCCCCC),
                ("Contengono Gloria + item casuali.", 0xFFCCCCCC),
                "---",
                ("Chiave Dimensionale: +50% Gloria bauli!", 0xFF00FF00),
                ("Chiave: +30% chance item raro!", 0xFF00FF00),
                ("Jackpot possibile = premi extra!", 0xFFFFD700),
            ],
            T("GLORY_METHOD_SPEEDKILL", "Speed Kill Bonus"): [
                ("Uccidi il target velocemente per bonus!", 0xFFCCCCCC),
                "---",
                ("Boss: entro 60 secondi = +200 Gloria!", 0xFF00FF00),
                ("Metin: entro 5 minuti = +80 Gloria!", 0xFF00FF00),
                "---",
                ("Il timer parte quando COLPISCI il mob.", 0xFF888888),
                ("Bonus cumulativo con altri bonus!", 0xFFFFD700),
            ],
        }

        for method, reward, desc in gloryMethods:
            self.__CBar(5, y, 420, 35, t["bg_dark"])
            tips = gloryTips.get(method, [])
            if tips:
                self.__CTextTip(method, 15, y + 3, t["text_value"], str(method), 0xFF00CCFF, tips, 180, 16)
            else:
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
        self.__CText(T("GLORY_PARTY_INFO1", "Quando giochi in GRUPPO (party):"), 130, y + 5, t["text_value"])
        self.__CText(T("GLORY_PARTY_INFO2", "KILLER = 100% Gloria | PARTY = 50% consolazione"), 60, y + 20, GOLD_COLOR)
        self.__CText(T("GLORY_PARTY_INFO3", "La consolazione 50% e' divisa per Power Rank (min 5% a testa)"), 15, y + 37, 0xFF00FF00)
        self.__CText(T("GLORY_PARTY_INFO4", "Risonatore attivo: +20% Gloria distribuita a tutto il party!"), 20, y + 55, 0xFF00FFFF)
        y += 83

        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 20

        partySteps = [
            T("PARTY_STEP_1", "1. Kill Elite = Killer riceve 100% Gloria"),
            T("PARTY_STEP_2", "2. Party vicini ricevono 50% consolazione"),
            T("PARTY_STEP_3", "3. La consolazione e' divisa per Power Rank (min 5% a testa)"),
            T("PARTY_STEP_4", "4. Bauli: Gloria solo a chi apre, party 50% consolazione"),
            T("PARTY_STEP_5", "5. Si applicano Bonus/Malus personali di ciascun membro"),
            T("PARTY_STEP_6", "6. Con Risonatore: +20% Gloria distribuita a TUTTI!"),
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
        self.__CBar(5, y, 420, 155, t["bg_dark"])
        self.__CText(T("BONUS_MALUS_TITLE", "BONUS/MALUS GLORIA (tutti cumulativi):"), 110, y + 5, t["accent"])
        self.__CText(T("BONUS_FIRST", "+ Primo del Giorno: +50% (primo boss/metin/baule/frattura)"), 15, y + 22, 0xFF00FF00)
        self.__CText(T("BONUS_STREAK", "+ Streak Login: +3%/+7%/+12% (3/7/30 giorni)"), 15, y + 36, 0xFF00FF00)
        self.__CText(T("BONUS_RANK", "+ Bonus Rank: +2% a +18% (automatico per rank)"), 15, y + 50, 0xFF00FF00)
        self.__CText(T("BONUS_FOCUS", "+ Focus Hunter: +20% (item consumabile)"), 15, y + 64, 0xFF00FF00)
        self.__CText(T("BONUS_FRACTURE", "+ Fracture Bonus: +50% (missioni 3/3 complete)"), 15, y + 78, 0xFF00FF00)
        self.__CText(T("BONUS_MENTOR", "+ Mentore: +25% (B+ rank in frattura E/D/C)"), 15, y + 92, 0xFF00FF00)
        self.__CText(T("BONUS_EVENT", "+ Evento Attivo: x2/x3/x4 (durante Glory Rush)"), 15, y + 106, 0xFF00FF00)
        self.__CText(T("MALUS_TRIAL", "- Trial Attivo: -25% per rank di differenza (max -100%)"), 15, y + 122, 0xFFFF6666)
        self.__CText(T("MALUS_EMERGENCY", "- Emergency Attiva: -80% Gloria durante la quest!"), 15, y + 136, 0xFFFF6666)
        y += 165

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
        self.__CText("Streak Bonus (+7%): +35", 100, y + 64, 0xFF00FF00)
        self.__CText(">>> TOTALE: +535 Gloria <<<", 100, y + 78, GOLD_COLOR)
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
        self.__CText(T("MISSIONS_INTRO1", "Ogni giorno alle 00:00 ricevi 3 nuove missioni."), 50, y + 5, t["text_value"])
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

        missionTips = {
            "kill_mob": [
                ("Uccidi mob specifici o qualsiasi mob.", 0xFFCCCCCC),
                ("Il VNUM del mob viene dal DB.", 0xFF888888),
                "---",
                ("PROGRESSO CONDIVISO!", 0xFF00FF00),
                ("Se un amico vicino uccide lo stesso mob,", 0xFF00FF00),
                ("il tuo progresso avanza anche!", 0xFF00FF00),
                "---",
                ("Reward: 15-3000 Gloria in base al rank.", 0xFFFFD700),
            ],
            "kill_boss": [
                ("Boss di mappa o Boss in fratture.", 0xFFCCCCCC),
                ("Qualsiasi boss conta, anche mondo aperto!", 0xFFCCCCCC),
                "---",
                ("PROGRESSO CONDIVISO in party!", 0xFF00FF00),
                ("Speed Kill su boss = bonus extra!", 0xFFFFD700),
            ],
            "kill_metin": [
                ("Metin di mappa o Metin in fratture.", 0xFFCCCCCC),
                ("Anche Super Metin contano!", 0xFFCCCCCC),
                "---",
                ("PROGRESSO CONDIVISO!", 0xFF00FF00),
                ("Speed Kill Metin (5 min) = +80 Gloria.", 0xFFFFD700),
            ],
            "seal_fracture": [
                ("Devi SIGILLARE una frattura.", 0xFFCCCCCC),
                ("NON entrare: basta sigillare.", 0xFFCCCCCC),
                "---",
                ("Disponibile da A-Rank in su.", 0xFFFF6666),
                ("Max 3 sigilli/giorno!", 0xFFFF6666),
            ],
        }

        for mType, name, desc in missionTypes:
            self.__CBar(5, y, 420, 32, t["bg_dark"])
            tips = missionTips.get(mType, [])
            if tips:
                self.__CTextTip("- %s" % name, 15, y + 3, t["text_value"],
                    name, 0xFF00CCFF, tips, 200, 14)
            else:
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
        self.__CTextTip(T("PENALTY_SYSTEM", "SISTEMA PENALITA'"), 160, y + 5, 0xFFFF4444,
            "Penalita' Missioni", 0xFFFF4444, [
                ("Se NON completi le missioni entro 00:00:", 0xFFCCCCCC),
                "---",
                ("Perdi Gloria TOTALE (non spendibile)!", 0xFFFF6666),
                ("La perdita scala col rank: E=5, N=900.", 0xFFFF6666),
                "---",
                ("La missione e' segnata 'failed' nel DB.", 0xFF888888),
                ("Ma non perdi MAI rank per questo.", 0xFF00FF00),
            ], 200, 16)
        self.__CText(T("PENALTY_INFO1", "Missioni NON completate entro mezzanotte:"), 90, y + 22, t["text_value"])
        self.__CText(T("PENALTY_INFO2", "= Perdi Gloria TOTALE (non spendibile)!"), 85, y + 38, 0xFFFF6666)
        self.__CText(T("PENALTY_INFO3", "La missione viene segnata come 'failed' nel DB."), 60, y + 53, t["text_muted"])
        y += 80

        # Bonus completamento
        self.__CBar(5, y, 420, 80, 0x3300FF00)
        self.__CTextTip(T("BONUS_ALL_COMPLETE_TITLE", "BONUS TUTTE COMPLETE"), 155, y + 5, 0xFF00FF00,
            "Bonus Completamento 3/3", 0xFF00FF00, [
                ("Completa tutte e 3 le missioni giornaliere!", 0xFFCCCCCC),
                "---",
                ("+50% Gloria extra (somma missioni)", 0xFF00FF00),
                ("+50% Gloria dai Boss/Metin fratture!", 0xFFFFD700),
                "---",
                ("Il bonus fratture dura 24h.", 0xFFCCCCCC),
                ("Visibile nel syschat dettagliato.", 0xFF888888),
                ("SUPER POTENTE: combinato con Focus = +70%!", 0xFFFF00FF),
            ], 200, 16)
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
        self.__CTextTip(T("EMERGENCY_QUEST_TITLE", "EMERGENCY QUEST"), 160, y + 5, 0xFFFF6600,
            "Emergency Quest", 0xFFFF6600, [
                ("Missioni speciali a TEMPO!", 0xFFCCCCCC),
                "---",
                ("Spawn dopo ~9000 kill (10% chance).", 0xFFCCCCCC),
                ("Anti-farm: +150 soglia dopo 5/g, +500 dopo 15/g", 0xFF888888),
                ("5 livelli: EASY -> GOD MODE", 0xFFFFAA00),
                "---",
                ("GOD MODE: 250 kill in 180s!", 0xFFFF0000),
                ("Reward: fino a +1200 Gloria!", 0xFFFFD700),
                "---",
                ("MALUS ATTIVO: Gloria -80% durante la quest!", 0xFFFF4444),
                ("Se fallisci: penalita' 50% del reward!", 0xFFFF6666),
                ("Usa Segnale di Emergenza per forzarla!", 0xFF00FF00),
            ], 260, 16)
        self.__CText(T("EMERGENCY_QUEST_SUBTITLE", "MISSIONI SPECIALI A TEMPO - PREMI MASSIMI!"), 80, y + 22, 0xFFFFAA00)
        y += 43

        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        emergencySteps = [
            T("EMERG_STEP_1", "1. Spawn RANDOM dopo aver ucciso ~9000 mob normali"),
            T("EMERG_STEP_2", "2. 10% chance Emergency, 90% chance Frattura"),
            T("EMERG_STEP_3", "3. Tempo limitato: 60-180 secondi per completare!"),
            T("EMERG_STEP_4", "4. Obiettivi: 30-250 kill a seconda della difficolta'"),
            T("EMERG_STEP_5", "5. Premi: 150-1200 Gloria + item bonus"),
            T("EMERG_STEP_6", "6. Se fallisci: penalita' Gloria (50% del reward)!"),
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
        self.__CText(T("SPEEDKILL_BOSS", "Boss: Uccidi entro 60 secondi = +200 Gloria Bonus!"), 50, y + 22, t["text_value"])
        self.__CText(T("SPEEDKILL_METIN", "Metin: Distruggi entro 5 minuti = +80 Gloria Bonus!"), 50, y + 36, t["text_value"])
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
                self.__CText((T("DAYS", "Giorni:") + " %s | " + T("PRIORITY", "Priorità:") + " %s") % (giorni_txt, str(ev.get("priority",5))), 20, y, t["text_muted"])
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
            T("FRACT_STEP_1", "1. Dopo ~9000 kill normali: 90% chance spawna una Frattura"),
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
        self.__CText("Spawn chance da DB (piu' rara = rank alto). Max +1 rank sopra il tuo.", 15, y + 38, t["text_muted"])
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
             T("FAQ_A1", "Al livello 5 il Sistema ti nota. Al livello 30 diventi Hunter ufficiale!")),

            (T("FAQ_Q2", "Come vedo le mie missioni?"),
             T("FAQ_A2", "Usa /hunter_missions oppure premi N > Tab Eventi > Apri Dettagli.")),

            (T("FAQ_Q3", "I mostri normali danno Gloria?"),
             T("FAQ_A3", "NO! Solo Boss/Metin/Bauli Elite, Missioni, Emergency ed Eventi danno Gloria!")),

            (T("FAQ_Q4", "Perche' perdo Gloria?"),
             T("FAQ_A4", "Missioni non completate: perdi Gloria TOTALE (non spendibile).")),

            (T("FAQ_Q5", "Cos'e' il Bonus x1.5?"),
             T("FAQ_A5", "Completi 3 missioni = +50% Gloria missioni + 50% bonus fratture!")),

            (T("FAQ_Q6", "Come salgo di Rank?"),
             T("FAQ_A6", "Accumula Gloria e completa le Prove. Per avanzare, parla con il Traditore Balso!")),

            (T("FAQ_Q7", "Posso perdere il mio Rank?"),
             T("FAQ_A7", "No, il Rank e' permanente. La Gloria puo' scendere ma non il Rank.")),

            (T("FAQ_Q8", "Come partecipo agli eventi?"),
             T("FAQ_A8", "Usa /hunter_events per vedere gli eventi. L'iscrizione e' AUTOMATICA!")),

            (T("FAQ_Q9", "Cosa sono le Fratture?"),
             T("FAQ_A9", "Portali dimensionali con Boss/Metin Elite. Gloria scala col rank!")),

            (T("FAQ_Q10", "Quando si resettano le missioni?"),
             T("FAQ_A10", "Alle 00:00. Missioni incomplete = penalita' su Gloria TOTALE!")),

            (T("FAQ_Q11", "Come funziona lo streak bonus?"),
             T("FAQ_A11", "Accessi consecutivi: 3 giorni=+3%, 7 giorni=+7%, 30 giorni=+12%!")),

            (T("FAQ_Q12", "Cos'e' l'Emergency Quest?"),
             T("FAQ_A12", "Missioni speciali dopo ~9000 kill! 10% chance, tempo limitato.")),

            (T("FAQ_Q13", "Come ottengo Speed Kill Bonus?"),
             T("FAQ_A13", "Boss: uccidi in 60s = +200 Gloria! Metin: in 300s = +80 Gloria bonus!")),

            (T("FAQ_Q14", "Perche' il Terminale si apre da solo?"),
             T("FAQ_A14", "Quando fai progresso missioni si apre automaticamente per 5 secondi!")),

            (T("FAQ_Q15", "Cosa succede se non completo le missioni?"),
             T("FAQ_A15", "Perdi Gloria TOTALE (non spendibile). Missione segnata come 'failed'.")),

            (T("FAQ_Q16", "Le missioni si perdono se cambio mappa?"),
             T("FAQ_A16", "NO! Le missioni persistono anche cambiando mappa o riloggando.")),

            (T("FAQ_Q17", "Come funziona il sistema Rival?"),
             T("FAQ_A17", "Se qualcuno ti supera in classifica, ricevi una notifica!")),

            (T("FAQ_Q18", "Cosa sono i Bauli Dimensionali?"),
             T("FAQ_A18", "Spawn nelle mappe e fratture. Danno item rari + Gloria bonus!")),

            (T("FAQ_Q19", "Posso aprire Fratture da E-Rank?"),
             T("FAQ_A19", "SI! Tutti possono aprirle. Vedi fratture del tuo rank e max +1 sopra.")),

            (T("FAQ_Q20", "Cos'e' la Prova d'Esame?"),
             T("FAQ_A20", "Trial per rank-up: -25% Gloria per rank di differenza (max -100%)!")),

            (T("FAQ_Q21", "Perche' guadagno meno Gloria del solito?"),
             T("FAQ_A21", "Prova d'Esame attiva? Guarda il syschat dettagliato con tutti i bonus/malus!")),

            (T("FAQ_Q22", "Come funziona la Gloria in party?"),
             T("FAQ_A22", "Killer riceve 100%, party vicini 50% consolazione divisa per Power Rank (min 5% a testa)!")),

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

            (T("FAQ_Q28", "Cos'e' il Risonatore di Gruppo?"),
             T("FAQ_A28", "Item consumabile: +20% Gloria distribuita a TUTTI i membri del party al prossimo kill!")),

            (T("FAQ_Q29", "Cos'e' il Focus Hunter?"),
             T("FAQ_A29", "Item consumabile: +20% Gloria al prossimo kill Elite (Boss/Metin). Consumato all'uso.")),

            (T("FAQ_Q30", "Cos'e' la Chiave Dimensionale?"),
             T("FAQ_A30", "+50% Gloria dai Bauli e +30% chance Item Raro. Si consuma all'apertura del Baule.")),

            (T("FAQ_Q31", "Cos'e' il Sigillo di Conquista?"),
             T("FAQ_A31", "Salta la fase di difesa della frattura: si apre subito! Consumato all'uso.")),

            (T("FAQ_Q32", "Come funziona il Calibratore?"),
             T("FAQ_A32", "La prossima frattura che spawna sara' minimo C-Rank. Filtra E e D. Si consuma allo spawn.")),

            (T("FAQ_Q33", "Come funzionano i Reward Online?"),
             T("FAQ_A33", "Ogni ~30 min ricevi Gloria auto. Milestone ogni 1/2/4/8h. Cap giornaliero per Rank.")),

            (T("FAQ_Q34", "Cos'e' la Super Metin Ownership?"),
             T("FAQ_A34", "Chi spawna la Super Metin e' l'Owner: il premio finale va a LUI. Scade dopo 5 min.")),

            (T("FAQ_Q35", "Come funziona la Partecipazione?"),
             T("FAQ_A35", "Party members vicini ricevono 50% Gloria consolazione. Non-party vicini: 15%. Super Metin: +10%/helper (max +50%).")),


            (T("FAQ_Q36", "Cosa sono gli Achievement?"),
             T("FAQ_A36", "Traguardi auto-tracciati (kill, Gloria, fratture...). Riscuoti con /hunter_claim o /hunter_smart_claim!")),

            (T("FAQ_Q37", "Cos'e' il Jackpot dei Bauli?"),
             T("FAQ_A37", "Chance casuale di ottenere item rari extra + Gloria bonus all'apertura. Chiave Dimensionale ne aumenta %.")),

            (T("FAQ_Q38", "Cos'e' il Sistema Rivale?"),
             T("FAQ_A38", "Se superi un altro Hunter in classifica, lui riceve un alert! Stimola la competizione.")),

            (T("FAQ_Q39", "Le ondate di difesa quante sono?"),
             T("FAQ_A39", "Da DB: E=3, D=4, C=4+Elite, B=6+MiniBoss, A=9+Boss, S=12+BossFinale, N=15.")),

            (T("FAQ_Q40", "Cosa succede se fallisco la difesa?"),
             T("FAQ_A40", "Perdi Coraggio (5%-45%) + Gloria (E=-25,D=-50,C=-100,B=-200,A=-400,S=-800,N=-1500). B+: distrutta!")),

            (T("FAQ_Q41", "Cos'e' lo Scanner di Fratture?"),
             T("FAQ_A41", "Item VNUM 50160: forza lo spawn immediato di una frattura vicino a te! CD 30 min.")),

            (T("FAQ_Q42", "Cos'e' lo Stabilizzatore di Rango?"),
             T("FAQ_A42", "Item VNUM 50161: SCEGLI TU quale rank di frattura evocare tramite menu! CD 30 min.")),

            (T("FAQ_Q43", "Cos'e' il Segnale di Emergenza?"),
             T("FAQ_A43", "Item VNUM 50165: forza la prossima Emergency Quest (salta la casualita' del 10%). CD 10 min.")),

            (T("FAQ_Q44", "Cos'e' il Frammento di Monarca?"),
             T("FAQ_A44", "Item VNUM 50168: evoca Frattura S-Rank + Focus gratis! Richiede A-Rank minimo. CD 1 ora.")),

            (T("FAQ_Q45", "Cosa spawna dal portale della frattura?"),
             T("FAQ_A45", "Casuale: BOSS, SUPER METIN o BAULE (+JACKPOT raro). Probabilita' da DB (hunter_quest_spawn_types).")),

            (T("FAQ_Q46", "Dove appaiono le fratture?"),
             T("FAQ_A46", "Vicino a te (+3,+3) in QUALSIASI mappa tranne dungeon. La posizione e' annunciata a TUTTI!")),

            (T("FAQ_Q47", "Quanta Gloria danno le fratture?"),
             T("FAQ_A47", "E=500-1500, D=1000-3000, C=2000-5000, B=4000-8000, A=6000-12000, S=10000-20000, N=20000-50000.")),

            (T("FAQ_Q48", "Cos'e' il Pity System?"),
             T("FAQ_A48", "Se fallisci la difesa, la prossima volta hai meno mob + tempo extra! Si resetta quando vinci.")),

            (T("FAQ_Q49", "Posso usare item durante la difesa?"),
             T("FAQ_A49", "Si! Usa il Sigillo di Conquista PRIMA di entrare per saltare la difesa. Gli altri item funzionano normali.")),

            (T("FAQ_Q50", "Cos'e' il Supremo?"),
             T("FAQ_A50", "Un WORLD BOSS! Vieni selezionato, evochi il boss, tutti possono attaccarlo. Dettagli nel tab 'Supremo'.")),

            (T("FAQ_Q51", "Cos'e' il Karma?"),
             T("FAQ_A51", "Il Karma segue la tua Gloria: piu' Gloria = piu' Karma. Si vede nell'allineamento. Dettagli nel tab 'Karma'.")),

            (T("FAQ_Q52", "Come apro la Wiki?"),
             T("FAQ_A52", "CTRL+J o /wiki! Cerca mob, item, NPC, drop. Su qualsiasi item compare il suggerimento CTRL+J.")),

            (T("FAQ_Q53", "Come recupero il Coraggio?"),
             T("FAQ_A53", "ENTRA nelle fratture (+10%) e completa la difesa (+15% a +50%). Sigillare NON recupera!")),
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
            (T("CMD_KEY_J", "CTRL+J"), T("CMD_KEY_J_DESC", "Apre la Wiki Encyclopedia (cerca mob/item)")),
            ("/hunter_missions", T("CMD_MISSIONS_DESC", "Apre pannello missioni giornaliere")),
            ("/hunter_events", T("CMD_EVENTS_DESC", "Mostra eventi programmati di oggi")),
            ("/hunter_join_event [id]", T("CMD_JOIN_DESC", "Partecipa all'evento con ID specificato")),
            ("/hunter_buy [id]", T("CMD_BUY_DESC", "Acquista item dallo shop con Gloria")),
            ("/hunter_claim [id]", T("CMD_CLAIM_DESC", "Riscuoti ricompensa achievement")),
            ("/hunter_smart_claim", T("CMD_SMART_CLAIM_DESC", "Riscuoti tutte le ricompense disponibili")),
            ("/wiki", T("CMD_WIKI_DESC", "Apre la Wiki Encyclopedia")),
        ]

        for cmd, desc in commands:
            self.__CText(cmd, 15, y, 0xFF00CCFF)
            self.__CText(desc, 180, y, t["text_muted"])
            y += 18

        y += 20

        # Consigli finali
        self.__CBar(5, y, 420, 205, 0x33FFD700)
        self.__CText("CONSIGLI PER NUOVI HUNTER:", 130, y + 5, GOLD_COLOR)
        self.__CText("1. Completa SEMPRE le 3 missioni giornaliere (evita penalty)", 15, y + 22, t["text_value"])
        self.__CText("2. Emergency Quest dopo ~9000 kill = 10% chance!", 15, y + 36, t["text_value"])
        self.__CText("3. Speed Kill Boss (60s) = +200, Metin (300s) = +80 Gloria!", 15, y + 50, t["text_value"])
        self.__CText("4. Accedi ogni giorno per streak bonus (3gg/7gg/30gg)", 15, y + 64, t["text_value"])
        self.__CText("5. Weekend = eventi speciali con Gloria x2/x3/x4!", 15, y + 78, t["text_value"])
        self.__CText("6. Boss/Metin Elite danno Gloria (base_points in DB)", 15, y + 92, t["text_value"])
        self.__CText("7. In PARTY la Gloria e' divisa per Power Rank (meritocrazia)!", 15, y + 106, 0xFF00FFFF)
        self.__CText("8. Usa Quick Access nel Trial per Rank Up e Missioni!", 15, y + 120, 0xFF00FFFF)
        self.__CText("9. Resta ONLINE: ogni ~30 min = Gloria gratis + Milestone!", 15, y + 134, 0xFF00FF00)
        self.__CText("10. Completa la Prova del Maestro subito per evitare il malus!", 15, y + 148, 0xFFFF6666)
        self.__CText("11. Usa il Risonatore in party per +20% Gloria a tutti!", 15, y + 162, 0xFF00FFFF)
        self.__CText("12. Chiave Dimensionale = +50% bauli + +30% item rari!", 15, y + 176, 0xFF00FFFF)
        self.__CText("13. /hunter_smart_claim riscuoti tutti gli achievement!", 15, y + 190, 0xFF00FF00)
        self.__CText("14. CTRL+J (o /wiki) = Wiki Encyclopedia con TUTTI i mob e item!", 15, y + 204, 0xFF9900FF)
        self.__CText("15. Il Karma segue la Gloria: piu' Gloria = allineamento alto!", 15, y + 218, 0xFF00FF00)
        y += 243

        return y

    def __LoadGuideFractures(self, y):
        """Dettagli su Fratture e Coraggio"""
        t = self.theme
        
        self.__CText(T("GUIDE_FRACTURE_TITLE", "GUIDA: FRATTURE E CORAGGIO"), 100, y, t["accent"])
        y += 25
        
        self.__CText(T("GUIDE_FRACTURE_SUB", "|cffFF4444[IMPORTANTE] ENTRARE VS SIGILLARE|r"), 15, y, 0xFFFFFFFF)
        y += 20
        
        # Sezione 1: Entrare
        self.__CBar(5, y, 420, 75, 0x33FF4444)
        self.__CTextTip(T("F_OPT_ENTER", "1. ENTRARE (Rischio Alto)"), 15, y + 5, t["title"],
            "ENTRARE nella Frattura", 0xFFFF4444, [
                ("Rischio ALTO ma ricompense MASSIME!", 0xFFFF6666),
                "---",
                ("1. Parti le ondate di difesa (3-15 wave)", 0xFFCCCCCC),
                ("2. Uccidi tutti i mob nel tempo limite", 0xFFCCCCCC),
                ("3. Se vinci: portale si apre 5 min", 0xFF00FF00),
                ("4. Dal portale: Boss/SuperMetin/Baule", 0xFF9900FF),
                "---",
                ("Coraggio: guadagni +15% (E) a +50% (N)", 0xFF00FF00),
                ("Gloria: da 500 (E) a 50.000 (N)!", 0xFFFFD700),
                ("NOVITA': Se fallisci -> Pity System!", 0xFF00FFFF),
                ("  5 sconfitte -> -50% mob + 30s extra.", 0xFF00FFFF),
            ], 300, 18)
        self.__CText("- Affronti mob e boss all'interno della frattura.", 20, y+25, 0xFFCCCCCC)
        self.__CText("- RICOMPENSE: Massime (Item, Exp, molta Gloria).", 20, y+38, 0xFF00FF88)
        self.__CText("- EFFETTO: Aumenta il CORAGGIO (+15% a +50% in base al Rank).", 20, y+51, GOLD_COLOR)
        y += 85
        
        # Sezione 2: Sigillare
        self.__CBar(5, y, 420, 75, 0x334444FF)
        self.__CTextTip(T("F_OPT_SEAL", "2. SIGILLARE (Rischio Zero)"), 15, y + 5, 0xFF8888FF,
            "SIGILLARE la Frattura", 0xFF8888FF, [
                ("Rischio ZERO, veloce ma meno Gloria.", 0xFF8888FF),
                "---",
                ("Avvicinati alla frattura e scegli Sigilla.", 0xFFCCCCCC),
                ("Nessun combattimento richiesto.", 0xFFCCCCCC),
                "---",
                ("Gloria: E=50, D=100, C=200, B=350", 0xFFFFAA00),
                ("         A=500, S=1000, N=2000", 0xFFFFAA00),
                "---",
                ("Coraggio: PERDI da 0% (E) a -100% (N)", 0xFFFF6666),
                ("Richiede Coraggio: E=0, D=15, C=30, B=50%", 0xFFFFAA00),
                ("  A=70%, S=85%, N=100% per sigillare!", 0xFFFFAA00),
                ("Max 3 sigilli al giorno.", 0xFF888888),
                ("Ideale per fratture troppo difficili.", 0xFF888888),
            ], 300, 18)
        self.__CText("- Chiudi lo strappo dall'esterno. Niente combattimento.", 20, y+25, 0xFFCCCCCC)
        self.__CText("- RICOMPENSE: Gloria dinamica (E=50, D=100...N=2000).", 20, y+38, 0xFFFFAA55)
        self.__CText("- EFFETTO: Riduce il CORAGGIO (0% a -100% in base al Rank). Max 3/giorno", 20, y+51, 0xFFFF4444)
        y += 85
        
        # Sezione 3: Coraggio
        self.__CText("IL SISTEMA DEL CORAGGIO", 130, y, GOLD_COLOR)
        y += 20
        self.__CText("Il Coraggio rappresenta il tuo valore come Hunter (0% - 100%).", 15, y, 0xFFFFFFFF)
        y += 15
        self.__CText("Se usi troppo spesso 'Sigilla' (via facile), il Coraggio scende.", 15, y, 0xFFCCCCCC)
        y += 15
        self.__CText("Se il Coraggio e' sotto il 50%, ricevi PENALITA' GLORIA.", 15, y, 0xFFFF4444)
        y += 20

        # Come RECUPERARE il Coraggio
        self.__CBar(5, y, 420, 90, 0x3300FF00)
        self.__CBar(5, y, 5, 90, 0xFF00FF00)
        self.__CText("COME RECUPERARE CORAGGIO:", 140, y + 5, 0xFF00FF88)
        self.__CText("1. ENTRA in una Frattura (nuova): +10% fisso", 20, y + 22, 0xFF00FF00)
        self.__CText("2. COMPLETA la difesa con successo:", 20, y + 38, 0xFF00FF00)
        self.__CText("   E=+15% | D=+18% | C=+20% | B=+25% | A=+30% | S=+40% | N=+50%", 20, y + 52, GOLD_COLOR)
        self.__CText("NON si recupera sigillando! Solo COMBATTENDO!", 20, y + 70, 0xFFFF6666)
        y += 100

        # Come si PERDE il Coraggio
        self.__CBar(5, y, 420, 80, 0x33FF0000)
        self.__CBar(5, y, 5, 80, 0xFFFF0000)
        self.__CText("COME SI PERDE CORAGGIO:", 150, y + 5, 0xFFFF4444)
        self.__CText("- Sigillare fratture: E=0% | D=-15% | C=-30% | B=-50% | A=-70% | S=-85% | N=-100%", 15, y + 22, 0xFFFF6666)
        self.__CText("- Fallire una difesa: E=-5% | D=-10% | C=-15% | B=-20% | A=-25% | S=-35% | N=-45%", 15, y + 38, 0xFFFF6666)
        self.__CText("- Uccidere un boss finale di Dungeon: -1% (silenzioso)", 15, y + 55, 0xFFFFAA00)
        y += 90

        # Effetti del Coraggio 
        self.__CBar(5, y, 420, 75, 0x33FFD700)
        self.__CText("EFFETTI DEL CORAGGIO:", 160, y + 5, GOLD_COLOR)
        self.__CText("- Sotto 50%: Penalita' Gloria su tutto!", 20, y + 22, 0xFFFF6666)
        self.__CText("- A 0%: NON puoi entrare in NESSUN Dungeon!", 20, y + 38, 0xFFFF0000)
        self.__CText("- Sigillare richiede Coraggio: D=15%, C=30%, B=50%, A=70%, S=85%, N=100%", 15, y + 55, 0xFFFFAA00)
        y += 85

        self.__CText("Il ciclo: Sigilla (perdi) -> Entra e combatti (recuperi) -> Ripeti!", 40, y, 0xFF00FFFF)
        y += 25

        # Sezione 4: Ondate di Difesa
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x33FF6600)
        self.__CText("ONDATE DI DIFESA (prima di entrare)", 120, y + 5, 0xFFFF6600)
        y += 38

        self.__CBar(5, y, 420, 95, t["bg_dark"])
        self.__CText("Prima di entrare nella frattura, devi DIFENDERE il portale!", 20, y + 5, 0xFFFFFFFF)
        self.__CText("Le ondate dipendono dal Rank della frattura (da DB):", 30, y + 22, 0xFFCCCCCC)
        self.__CText("E=3 ondate | D=4 ondate | C=4+Elite | B=6+MiniBoss", 45, y + 40, t["text_value"])
        self.__CText("A=9+Boss | S=12+Boss Finale | N=15 (dal DB)", 55, y + 55, t["text_value"])
        self.__CText("Ogni ondata ha timer: se scade, mob extra spawneranno!", 40, y + 73, 0xFFFF4444)
        self.__CText("Timer: E/D/C=60s | B=90s | A=120s | S=150s | N=180s", 70, y + 88, 0xFF888888)
        y += 105

        # Sezione 5: Difesa Fallita vs Riuscita
        self.__CBar(5, y, 420, 80, 0x33FF0000)
        self.__CBar(5, y, 5, 80, 0xFFFF0000)
        self.__CText("DIFESA FALLITA:", 170, y + 5, 0xFFFF4444)
        self.__CText("- Perdi Coraggio: -5% (E) fino a -45% (N) in base al rank", 20, y + 22, 0xFFFF6666)
        self.__CText("- Perdi Gloria: E=-25 D=-50 C=-100 B=-200 A=-400 S=-800 N=-1500", 15, y + 38, 0xFFFF6666)
        self.__CText("- Rank B e superiori: la frattura viene DISTRUTTA!", 20, y + 55, 0xFFFF0000)
        y += 90

        self.__CBar(5, y, 420, 65, 0x3300FF00)
        self.__CBar(5, y, 5, 65, 0xFF00FF00)
        self.__CText("DIFESA RIUSCITA:", 170, y + 5, 0xFF00FF88)
        self.__CText("- Guadagni Coraggio: +15% (E) fino a +50% (N)!", 20, y + 22, 0xFF00FF00)
        self.__CText("- Accesso al portale per ENTRARE nella frattura!", 20, y + 38, 0xFF00FF00)
        self.__CText("- Piu' alto il rank, piu' coraggio guadagni!", 20, y + 52, t["text_muted"])
        y += 75

        # =====================================================
        # Sezione 6: COSA SUCCEDE DENTRO IL PORTALE
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x339900FF)
        self.__CTextTip("COSA SPAWNA DAL PORTALE?", 140, y + 5, 0xFF9900FF,
            "Portale Frattura", 0xFF9900FF, [
                ("Dopo la difesa, il portale resta 5 minuti.", 0xFFCCCCCC),
                ("Toccalo per spawnavne il contenuto:", 0xFFCCCCCC),
                "---",
                ("BOSS (1 solo) - Alta Gloria, drop rari", 0xFFFF4444),
                ("SUPER METIN - Tu sei Owner! Premio tuo!", 0xFFFF6600),
                ("BAULE - Item + Gloria + chance Jackpot!", GOLD_COLOR),
                ("JACKPOT - Premio raro extra!", 0xFFFF00FF),
                "---",
                ("Le % vengono dalla tabella DB.", 0xFF888888),
                ("Usa Chiave Dimensionale per +50% bauli!", 0xFF00FF00),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 90, t["bg_dark"])
        self.__CText("Quando tocchi il portale, il sistema sceglie a CASO:", 40, y + 5, 0xFFFFFFFF)
        self.__CText("- BOSS: Mostri potenti con alta Gloria (1 solo)", 20, y + 22, 0xFFFF4444)
        self.__CText("- SUPER METIN: Tu sei Owner! Premio va a te!", 20, y + 36, 0xFFFF6600)
        self.__CText("- BAULE: Baule del Tesoro con item e Gloria bonus!", 20, y + 50, GOLD_COLOR)
        self.__CText("- JACKPOT: Premio raro extra (chance bassa)!", 20, y + 64, 0xFFFF00FF)
        self.__CText("Le probabilita' sono dal DB (hunter_quest_spawn_types).", 30, y + 80, t["text_muted"])
        y += 100

        # Dettaglio: Cosa spawna dipende dal rank
        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText("I Boss/Metin che spawnano dipendono da:", 80, y + 5, 0xFFFFFFFF)
        self.__CText("1. RANK della Frattura: frattura B = mob rank B o inferiori", 15, y + 22, t["text_value"])
        self.__CText("2. TUO LIVELLO: mob filtrati per il tuo level range", 15, y + 36, t["text_value"])
        self.__CText("3. POOL DB: dalla tabella hunter_quest_spawns (nomi, vnum)", 15, y + 50, t["text_value"])
        self.__CText("Non sai cosa uscira' finche' non tocchi il portale!", 50, y + 66, 0xFFFF6600)
        y += 88

        # =====================================================
        # Sezione 7: RICOMPENSE PER RANK FRATTURA
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CTextTip("RICOMPENSE FRATTURE PER RANK", 120, y + 5, GOLD_COLOR,
            "Ricompense Fratture", GOLD_COLOR, [
                ("La Gloria indicata e' un RANGE.", 0xFFCCCCCC),
                ("Il valore esatto dipende da:", 0xFFCCCCCC),
                "---",
                ("1. Tipo di portale (Boss/SuperMetin/Baule)", 0xFF00CCFF),
                ("2. Speed Kill bonus (+80/+200)", 0xFF00FF00),
                ("3. Focus del Cacciatore (+20%)", 0xFF00FF00),
                ("4. Bonus missioni complete (+50%)", 0xFFFFD700),
                ("5. Streak Login (+3/7/12%)", 0xFFFFD700),
                "---",
                ("I bonus si SOMMANO tra loro!", 0xFFFF00FF),
            ], 260, 16)
        y += 38

        fractureRewards = [
            ("E", "500 - 1.500", "Oggetti Comuni + EXP Base", 0xFF888888),
            ("D", "1.000 - 3.000", "Equip Verde + EXP Buona", 0xFF00FF00),
            ("C", "2.000 - 5.000", "Equip Blu + Drop Rari", 0xFF0088FF),
            ("B", "4.000 - 8.000", "Equip Viola + Materiali Speciali", 0xFFFF8800),
            ("A", "6.000 - 12.000", "Equip Oro + Cristalli Rari", 0xFFFF0000),
            ("S", "10.000 - 20.000", "Equip Leggendario + Frammenti Supremi", 0xFFFF00FF),
            ("N", "20.000 - 50.000", "Equip Mitico + Essenza del Monarca", 0xFFFFD700),
        ]

        for rank, gloria, items, color in fractureRewards:
            self.__CBar(5, y, 420, 32, t["bg_dark"])
            self.__CBar(5, y, 4, 32, color)
            self.__CText(rank, 15, y + 3, color)
            self.__CText(gloria + " Gloria", 35, y + 3, 0xFF00FF00)
            self.__CText(items, 160, y + 3, t["text_muted"])
            y += 34

        y += 10

        # =====================================================
        # Sezione 7b: BOTTINO DEI BAULI (Loot Table)
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CTextTip("BOTTINO DEI BAULI", 155, y + 5, GOLD_COLOR,
            "Loot Table Bauli", GOLD_COLOR, [
                ("Ogni baule contiene 1 premio casuale.", 0xFFCCCCCC),
                ("Il Rank della frattura determina il pool!", 0xFFCCCCCC),
                "---",
                ("Fratture di rank alto sbloccano premi rari.", 0xFF00FF00),
                ("Usa Chiave Dimensionale per +50% bauli!", 0xFF00CCFF),
                "---",
                ("Rarita': Comune > Raro > Ultra Raro > LEGGENDARIO", 0xFFFFD700),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 35, t["bg_dark"])
        self.__CText("Ogni baule contiene 1 premio casuale dal pool del Rank.", 30, y + 3, 0xFFFFFFFF)
        self.__CText("Fratture piu' alte = premi piu' potenti e rari!", 55, y + 18, 0xFFFFAA55)
        y += 42

        # --- E-RANK e superiori ---
        self.__CBar(5, y, 420, 18, 0x33888888)
        self.__CText("--- DISPONIBILI DA E-RANK ---", 120, y + 1, 0xFF888888)
        y += 22
        chestLootE = [
            ("Jackpot Gloria Minore", "86-259 Gloria", 0xFF00FF00, ""),
            ("Buono 100 Gloria x2", "", 0xFFFFA500, ""),
            ("Pergamena Certificato Trofei", "", 0xFFCCCCCC, ""),
            ("Pozione Saggezza", "", 0xFFCCCCCC, ""),
            ("Metallo UP 100%", "", 0xFFFF00FF, "LEGGENDARIO"),
        ]
        for name, extra, color, rarity in chestLootE:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00FF88)
            if rarity:
                self.__CText(rarity, 340, y, 0xFFFF00FF)
            y += 16
        y += 8

        # --- D-RANK e superiori ---
        self.__CBar(5, y, 420, 18, 0x3300FF00)
        self.__CText("--- DISPONIBILI DA D-RANK ---", 120, y + 1, 0xFF00FF00)
        y += 22
        chestLootD = [
            ("Scanner di Fratture", "Item Hunter", 0xFF0088FF, ""),
            ("Certificato Cavalcatura", "", 0xFFCCCCCC, ""),
            ("Certificato Cucciolo Pet", "", 0xFFCCCCCC, ""),
            ("Forziere Raffinamenti", "", 0xFFCCCCCC, ""),
        ]
        for name, extra, color, rarity in chestLootD:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00AAFF)
            if rarity:
                self.__CText(rarity, 340, y, 0xFFFF00FF)
            y += 16
        y += 8

        # --- C-RANK e superiori ---
        self.__CBar(5, y, 420, 18, 0x330088FF)
        self.__CText("--- DISPONIBILI DA C-RANK ---", 120, y + 1, 0xFF0088FF)
        y += 22
        chestLootC = [
            ("Jackpot Gloria", "172-518 Gloria", 0xFF00FF00, ""),
            ("Focus del Cacciatore", "Item Hunter", 0xFF0088FF, ""),
            ("Buono 500 Gloria", "", 0xFFFFA500, ""),
            ("Anello Caccia", "", 0xFFFFAA55, ""),
            ("Ritorna Dungeon 15g", "", 0xFFFFAA55, ""),
            ("Scrigno Costumi", "", 0xFFFF8800, "Raro"),
            ("Scrigno Incanta Costumi", "", 0xFFFF8800, "Raro"),
            ("Anello EXP 30g / Guanto 30g", "", 0xFFFF8800, "Ultra Raro"),
            ("Accodamento 30g", "", 0xFFFF8800, "Ultra Raro"),
            ("Forziere Trofei", "", 0xFFFF00FF, "LEGGENDARIO"),
        ]
        for name, extra, color, rarity in chestLootC:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00FF88)
            if rarity:
                rarCol = 0xFFFF8800 if rarity == "Raro" else 0xFFFF4444 if rarity == "Ultra Raro" else 0xFFFF00FF
                self.__CText(rarity, 340, y, rarCol)
            y += 16
        y += 8

        # --- B-RANK e superiori ---
        self.__CBar(5, y, 420, 18, 0x33FF8800)
        self.__CText("--- DISPONIBILI DA B-RANK ---", 120, y + 1, 0xFFFF8800)
        y += 22
        chestLootB = [
            ("Chiave Dimensionale", "Item Hunter", 0xFFFF8800, "Raro"),
            ("Calibratore Fratture", "Item Hunter", 0xFFFF8800, ""),
        ]
        for name, extra, color, rarity in chestLootB:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00AAFF)
            if rarity:
                self.__CText(rarity, 340, y, 0xFFFF8800)
            y += 16
        y += 8

        # --- A-RANK e superiori ---
        self.__CBar(5, y, 420, 18, 0x33FF0000)
        self.__CText("--- DISPONIBILI DA A-RANK ---", 120, y + 1, 0xFFFF0000)
        y += 22
        chestLootA = [
            ("Jackpot Gloria Maggiore", "345-864 Gloria", 0xFF00FF00, ""),
            ("Stabilizzatore di Rango", "Item Hunter", 0xFFFF0000, "Raro"),
            ("Segnale di Emergenza", "Item Hunter", 0xFFFF0000, "Raro"),
            ("Buono 1000 Gloria", "", 0xFFFFA500, ""),
        ]
        for name, extra, color, rarity in chestLootA:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00FF88)
            if rarity:
                self.__CText(rarity, 340, y, 0xFFFF4444)
            y += 16
        y += 8

        # --- S-RANK ---
        self.__CBar(5, y, 420, 18, 0x33FF00FF)
        self.__CText("--- DISPONIBILI DA S-RANK ---", 120, y + 1, 0xFFFF00FF)
        y += 22
        chestLootS = [
            ("Sigillo di Conquista", "Item Hunter", 0xFFFF00FF, "Ultra Raro"),
            ("Risonatore di Gruppo", "Item Hunter", 0xFFFF00FF, "Ultra Raro"),
        ]
        for name, extra, color, rarity in chestLootS:
            self.__CText(name, 15, y, color)
            if extra:
                self.__CText(extra, 230, y, 0xFF00AAFF)
            if rarity:
                self.__CText(rarity, 340, y, 0xFFFF4444)
            y += 16
        y += 8

        # --- N-RANK (MASSIMO) ---
        self.__CBar(5, y, 420, 18, 0x33FFD700)
        self.__CText("--- ESCLUSIVI N-RANK ---", 140, y + 1, 0xFFFFD700)
        y += 22
        chestLootN = [
            ("MEGA JACKPOT GLORIA", "691-1728 Gloria!", 0xFFFFD700, "LEGGENDARIO"),
            ("Frammento di Monarca", "Item Hunter SUPREMO", 0xFFFFD700, "LEGGENDARIO"),
        ]
        for name, extra, color, rarity in chestLootN:
            self.__CBar(5, y, 420, 20, 0x22FFD700)
            self.__CText(name, 15, y + 2, color)
            if extra:
                self.__CText(extra, 230, y + 2, 0xFFFF00FF)
            if rarity:
                self.__CText(rarity, 340, y + 2, 0xFFFF00FF)
            y += 22
        y += 10

        # Nota finale
        self.__CBar(5, y, 420, 22, 0x22FFFFFF)
        self.__CText("I premi di rank superiore si AGGIUNGONO al pool di quelli inferiori!", 15, y + 3, 0xFFFFAA55)
        y += 30

        # =====================================================
        # Sezione 8: DOVE APPAIONO LE FRATTURE
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x3300CCFF)
        self.__CText("DOVE APPAIONO LE FRATTURE?", 130, y + 5, 0xFF00CCFF)
        y += 38

        self.__CBar(5, y, 420, 95, t["bg_dark"])
        self.__CText("Le fratture spawnano VICINO A TE dopo ~9000 kill normali.", 25, y + 5, 0xFFFFFFFF)
        self.__CText("90% chance frattura, 10% chance Emergency Quest.", 55, y + 22, t["text_value"])
        self.__CText("Appaiono in QUALSIASI mappa TRANNE i dungeon!", 50, y + 38, t["text_value"])
        self.__CText("Rank MAX: il tuo Rank attuale +1 (es: se sei C, max D).", 30, y + 54, t["text_value"])
        self.__CText("La posizione E' ANNUNCIATA A TUTTI con notice globale!", 35, y + 70, 0xFFFF4444)
        self.__CText("Es: 'Player ha risvegliato: Boss X [B-Rank] | Mappa CH1'", 25, y + 84, t["text_muted"])
        y += 105

        # =====================================================
        # Sezione 9: FLUSSO COMPLETO FRATTURA (Passo per Passo)
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x33FF6600)
        self.__CText("FLUSSO COMPLETO (Passo per Passo)", 110, y + 5, 0xFFFF6600)
        y += 38

        fullFlow = [
            ("1.", "Uccidi ~9000 mob normali in qualsiasi mappa", 0xFFCCCCCC),
            ("2.", "FRATTURA appare vicino a te (90%) o Emergency (10%)", 0xFFCCCCCC),
            ("3.", "Clicca sulla Frattura: vedi rank, ricompense, requisiti", 0xFFCCCCCC),
            ("4.", "Scegli: ENTRARE (difesa) o SIGILLARE (gloria base)", 0xFFCCCCCC),
            ("5.", "Se ENTRI: parti le ondate di difesa (3-15 wave)", 0xFFFF6600),
            ("6.", "Uccidi TUTTI i mob delle ondate nel tempo limite", 0xFFFF6600),
            ("7.", "Difesa vinta = portale si apre per 5 minuti!", 0xFF00FF00),
            ("8.", "Tocca il portale = spawna Boss/SuperMetin/Baule", 0xFF9900FF),
            ("9.", "Uccidi il Boss = Gloria base + Speed Kill + Bonus vari", GOLD_COLOR),
            ("10.", "Se SuperMetin: tu sei l'Owner, premio va a TE", 0xFF00FFFF),
            ("11.", "Annuncio GLOBALE a tutto il server con posizione!", 0xFFFF4444),
        ]

        for num, desc, color in fullFlow:
            self.__CText(num, 15, y, 0xFFFFAA00)
            self.__CText(desc, 35, y, color)
            y += 17

        y += 10

        # =====================================================
        # Sezione 10: PITY SYSTEM
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x3300FF00)
        self.__CTextTip("PITY SYSTEM (Aiuto Difesa)", 145, y + 5, 0xFF00FF00,
            "Pity System", 0xFF00FF00, [
                ("Un sistema che ti aiuta se fallisci!", 0xFFCCCCCC),
                "---",
                ("Ogni fallimento:", 0xFFFFAA00),
                ("  - Riduce i mob nelle ondate", 0xFF00FF00),
                ("  - Aggiunge tempo extra al timer", 0xFF00FF00),
                "---",
                ("Si resetta quando VINCI una difesa.", 0xFFFF6666),
                ("Funziona per ogni rank separatamente.", 0xFF888888),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 65, t["bg_dark"])
        self.__CText("Se fallisci una difesa, il sistema ti aiuta la prossima volta!", 15, y + 5, 0xFF00FF00)
        self.__CText("- Riduzione mob da uccidere nelle ondate", 20, y + 22, t["text_value"])
        self.__CText("- Tempo extra per completare la difesa", 20, y + 36, t["text_value"])
        self.__CText("Il Pity si resetta quando vinci una difesa.", 40, y + 52, t["text_muted"])
        y += 75

        # =====================================================
        # Sezione 11: CONSIGLI TATTICI PER RANK
        # =====================================================
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CText("CONSIGLI TATTICI PER RANK", 140, y + 5, GOLD_COLOR)
        y += 38

        tactics = [
            ("E", "Attacco Frontale consigliato.", 0xFF888888),
            ("D", "Attenzione ai gruppi numerosi.", 0xFF00FF00),
            ("C", "Priorita' ai nemici Elite prima!", 0xFF0088FF),
            ("B", "Prepara Pozioni e Buff prima di entrare.", 0xFFFF8800),
            ("A", "Richiesto Equipaggiamento vs Mostri.", 0xFFFF0000),
            ("S", "COORDINAZIONE PARTY ESSENZIALE. Pericolo Estremo!", 0xFFFF00FF),
            ("N", "??? SOPRAVVIVI AD OGNI COSTO.", 0xFFFFD700),
        ]

        for rank, hint, color in tactics:
            self.__CBar(5, y, 420, 22, t["bg_dark"])
            self.__CBar(5, y, 4, 22, color)
            self.__CText(rank + "-Rank:", 15, y + 3, color)
            self.__CText(hint, 80, y + 3, t["text_value"])
            y += 24
        
        return y
    
    def __LoadGuideTrial(self, y):
        """Guida al sistema Prove d'Esame (Trial / Rank-Up)"""
        t = self.theme

        self.__CText(T("GUIDE_TRIAL_TITLE", "PROVE D'ESAME (RANK-UP)"), 130, y, t["accent"])
        y += 25

        # Intro
        self.__CBar(5, y, 420, 80, 0x33FFD700)
        self.__CText(T("TRIAL_INTRO1", "Per SALIRE DI RANK non basta la Gloria!"), 90, y + 5, GOLD_COLOR)
        self.__CText(T("TRIAL_INTRO2", "Devi completare la PROVA D'ESAME del rank successivo."), 40, y + 22, t["text_value"])
        self.__CText(T("TRIAL_INTRO3", "Parla con il NPC 'Traditore Balso' per iniziarla."), 55, y + 38, t["text_value"])
        self.__CText(T("TRIAL_INTRO4", "Finche' la Prova non e' superata, hai un MALUS su tutta la Gloria!"), 20, y + 55, 0xFFFF6666)
        y += 90

        # Come funziona
        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        trialSteps = [
            T("TRIAL_STEP_1", "1. Accumula Gloria sufficiente per il rank successivo"),
            T("TRIAL_STEP_2", "2. Parla con il Traditore Balso (NPC Maestro)"),
            T("TRIAL_STEP_3", "3. Accetta la Prova: obiettivi di kill Boss, Metin, Fratture..."),
            T("TRIAL_STEP_4", "4. Completa tutti gli obiettivi (progresso nel terminale)"),
            T("TRIAL_STEP_5", "5. Torna dal Maestro per confermare il Rank-Up!"),
            T("TRIAL_STEP_6", "6. Rank-Up confermato = malus rimosso, Gloria piena!"),
        ]

        for step in trialSteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 10
        self.__CSep(5, y)
        y += 15

        # Malus spiegato
        self.__CBar(5, y, 420, 85, 0x33FF0000)
        self.__CTextTip(T("TRIAL_PENALTY_TITLE", "MALUS PROVA NON COMPLETATA"), 130, y + 5, 0xFFFF4444,
            "Malus Trial", 0xFFFF4444, [
                ("Se hai Gloria per un rank superiore", 0xFFCCCCCC),
                ("MA la Prova non e' stata completata:", 0xFFCCCCCC),
                "---",
                ("-25% Gloria per OGNI rank di gap!", 0xFFFF6666),
                ("Max -100% = non guadagni NULLA!", 0xFFFF0000),
                "---",
                ("Esempio: Gloria=C, Trial=E", 0xFFFFAA00),
                ("  2 rank gap = -50% su TUTTA la Gloria!", 0xFFFFAA00),
                "---",
                ("Si applica a kill, online, missioni.", 0xFFCCCCCC),
                ("NON si applica ai premi degli Eventi.", 0xFF00FF00),
            ], 260, 16)
        self.__CText(T("TRIAL_PENALTY_INFO1", "Se hai la Gloria per un rank superiore MA la Prova non e' fatta:"), 15, y + 22, t["text_value"])
        self.__CText(T("TRIAL_PENALTY_INFO2", "-25% Gloria per ogni rank di differenza (max -100%)"), 50, y + 38, 0xFFFF6666)
        self.__CText(T("TRIAL_PENALTY_EXAMPLE1", "Es: Gloria=A ma Trial=E -> 4 rank di gap -> -100% Gloria!"), 30, y + 55, t["text_muted"])
        self.__CText(T("TRIAL_PENALTY_EXAMPLE2", "Es: Gloria=C ma Trial=D -> 1 rank di gap -> -25% Gloria"), 35, y + 70, t["text_muted"])
        y += 95

        # Cosa influenza il malus
        self.__CBar(5, y, 420, 65, t["bg_dark"])
        self.__CText(T("TRIAL_AFFECTS_TITLE", "IL MALUS SI APPLICA A:"), 150, y + 5, 0xFFFFAA00)
        self.__CText(T("TRIAL_AFFECTS_1", "- Kill Elite (Boss, Metin, Super Metin, Bauli)"), 20, y + 22, t["text_value"])
        self.__CText(T("TRIAL_AFFECTS_2", "- Reward Tempo Online e Milestone"), 20, y + 36, t["text_value"])
        self.__CText(T("TRIAL_AFFECTS_3", "- TUTTO tranne i premi degli Eventi"), 20, y + 50, t["text_value"])
        y += 75

        # Obiettivi Trial
        self.__CBar(5, y, 420, 55, 0x3300CCFF)
        self.__CText(T("TRIAL_OBJECTIVES_TITLE", "TIPI DI OBIETTIVO PROVA:"), 140, y + 5, 0xFF00CCFF)
        self.__CText(T("TRIAL_OBJ_1", "- Uccidi tot Boss specifici (vnum dal DB)"), 20, y + 22, t["text_value"])
        self.__CText(T("TRIAL_OBJ_2", "- Distruggi tot Metin specifici (vnum dal DB)"), 20, y + 36, t["text_value"])
        self.__CText(T("TRIAL_OBJ_3", "- Sigilla tot Fratture | Apri tot Bauli"), 20, y + 50, t["text_value"])
        y += 65

        # Super Metin Ownership
        y += 10
        self.__CBar(5, y, 420, 30, 0x33FF6600)
        self.__CTextTip(T("SUPER_METIN_TITLE", "SUPER METIN - SISTEMA OWNERSHIP"), 110, y + 5, 0xFFFF6600,
            "Super Metin Ownership", 0xFFFF6600, [
                ("Le Super Metin spawnano dai portali frattura.", 0xFFCCCCCC),
                "---",
                ("Chi evoca la frattura = OWNER!", 0xFF00FF00),
                ("Se un ALTRO player la uccide:", 0xFFCCCCCC),
                ("  - Owner riceve il 100% della Gloria", 0xFF00FF00),
                ("  - Killer riceve 15% partecipazione (extra)", 0xFFFF6666),
                "---",
                ("Ownership dura 5 minuti (= Speed Kill).", 0xFFCCCCCC),
                ("Party dell'owner = flusso normale.", 0xFF00CCFF),
                ("Bonus +10% per Hunter vicino (max +50%)!", 0xFFFFD700),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 95, t["bg_dark"])
        self.__CText(T("SM_INFO_1", "Quando evochi una Super Metin da una frattura, SEI L'OWNER."), 15, y + 5, t["text_value"])
        self.__CText(T("SM_INFO_2", "Se un altro player la uccide, TU ricevi il 100% della Gloria!"), 15, y + 20, GOLD_COLOR)
        self.__CText(T("SM_INFO_3", "Il killer riceve 15% Gloria extra (partecipazione)."), 15, y + 35, t["text_muted"])
        self.__CText(T("SM_INFO_4", "Ownership scade dopo 5 minuti (= timer Speed Kill)."), 15, y + 50, t["text_muted"])
        self.__CText(T("SM_INFO_5", "Membri del TUO party mantengono il flusso normale."), 15, y + 65, 0xFF00FF00)
        self.__CText(T("SM_INFO_6", "Bonus Gruppo: +10% per ogni Hunter vicino (max +50%)!"), 15, y + 80, 0xFF00FFFF)
        y += 105

        return y
    
    def __LoadGuideItems(self, y):
        """Guida agli Item Consumabili Hunter"""
        t = self.theme

        self.__CText(T("GUIDE_ITEMS_TITLE", "ITEM CONSUMABILI HUNTER"), 130, y, 0xFFFFA500)
        y += 25

        self.__CText(T("ITEMS_INTRO", "Item speciali che potenziano le tue azioni Hunter!"), 70, y, t["text_muted"])
        y += 25

        # =====================================================
        # RISONATORE DI GRUPPO
        # =====================================================
        self.__CBar(5, y, 420, 85, 0x3300FFFF)
        self.__CBar(5, y, 5, 85, 0xFF00FFFF)
        self.__CTextTip(T("ITEM_RESONATOR_TITLE", "RISONATORE DI GRUPPO"), 120, y + 5, 0xFF00FFFF,
            "Risonatore di Gruppo", 0xFF00FFFF, [
                ("VNUM: 50166 | Cooldown: 5 minuti", 0xFF888888),
                "---",
                ("+20% Gloria al prossimo kill Elite.", 0xFF00FF00),
                ("La Gloria viene distribuita al party", 0xFFCCCCCC),
                ("per meritocrazia (Power Rank).", 0xFFCCCCCC),
                "---",
                ("Ogni membro riceve min 5% in base al rank.", 0xFFCCCCCC),
                ("Consumato al primo kill Elite.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_RESONATOR_DESC1", "Attiva la RISONANZA: +20% Gloria al prossimo kill Elite!"), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_RESONATOR_DESC2", "La Gloria viene poi DISTRIBUITA al party per meritocrazia."), 15, y + 36, t["text_value"])
        self.__CText(T("ITEM_RESONATOR_DESC3", "Ogni membro riceve la sua % basata sul Power Rank (min 5%)."), 15, y + 50, t["text_muted"])
        self.__CText(T("ITEM_RESONATOR_DESC4", "Consumato al primo kill Elite. Si compra nello Shop Hunter."), 15, y + 66, 0xFF00FF00)
        y += 95

        # =====================================================
        # FOCUS HUNTER
        # =====================================================
        self.__CBar(5, y, 420, 65, 0x3300FF00)
        self.__CBar(5, y, 5, 65, 0xFF00FF00)
        self.__CTextTip(T("ITEM_FOCUS_TITLE", "FOCUS DEL CACCIATORE"), 130, y + 5, 0xFF00FF00,
            "Focus del Cacciatore", 0xFF00FF00, [
                ("VNUM: 50162 | Cooldown: 5 minuti", 0xFF888888),
                "---",
                ("+20% Gloria al prossimo kill Elite.", 0xFF00FF00),
                ("Funziona su Boss, Metin, Super Metin.", 0xFFCCCCCC),
                ("In party: il bonus si applica al TUO share.", 0xFFCCCCCC),
                "---",
                ("Consumato al primo kill.", 0xFFFF6666),
                ("Visibile in syschat: 'Focus Hunter +20%'", 0xFF888888),
            ], 200, 16)
        self.__CText(T("ITEM_FOCUS_DESC1", "+20% Gloria al prossimo kill Elite (Boss/Metin)."), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_FOCUS_DESC2", "Consumato al primo kill. Funziona anche in party."), 15, y + 36, t["text_muted"])
        self.__CText(T("ITEM_FOCUS_DESC3", "Visibile nel syschat: 'Focus Hunter +20%'."), 15, y + 50, t["text_muted"])
        y += 75

        # =====================================================
        # CHIAVE DIMENSIONALE
        # =====================================================
        self.__CBar(5, y, 420, 75, 0x339900FF)
        self.__CBar(5, y, 5, 75, 0xFF9900FF)
        self.__CTextTip(T("ITEM_KEY_TITLE", "CHIAVE DIMENSIONALE"), 135, y + 5, 0xFF9900FF,
            "Chiave Dimensionale", 0xFF9900FF, [
                ("VNUM: 50163 | Cooldown: 5 minuti", 0xFF888888),
                "---",
                ("+50% Gloria da Bauli frattura!", 0xFF00FF00),
                ("+30% chance Item Raro!", 0xFF00FF00),
                ("Aumenta anche la chance di Jackpot.", 0xFFFFD700),
                "---",
                ("Usala PRIMA di aprire il Baule.", 0xFFCCCCCC),
                ("Consumata all'apertura del Baule.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_KEY_DESC1", "+50% Gloria dai Bauli + +30% chance Item Raro!"), 15, y + 22, GOLD_COLOR)
        self.__CText(T("ITEM_KEY_DESC2", "Usala PRIMA di aprire un Baule per massimizzare i premi."), 15, y + 38, t["text_value"])
        self.__CText(T("ITEM_KEY_DESC3", "Aumenta anche la chance di Jackpot!"), 15, y + 52, t["text_muted"])
        y += 85

        # =====================================================
        # SIGILLO DI CONQUISTA
        # =====================================================
        self.__CBar(5, y, 420, 75, 0x33FFD700)
        self.__CBar(5, y, 5, 75, 0xFFFFD700)
        self.__CTextTip(T("ITEM_SEAL_TITLE", "SIGILLO DI CONQUISTA"), 135, y + 5, GOLD_COLOR,
            "Sigillo di Conquista", GOLD_COLOR, [
                ("VNUM: 50164 | Cooldown: 30 minuti", 0xFF888888),
                "---",
                ("SALTA completamente la fase di difesa!", 0xFF00FF00),
                ("La frattura si apre subito al portale.", 0xFFCCCCCC),
                "---",
                ("Ideale per fratture alte quando sei solo.", 0xFFCCCCCC),
                ("Consumato quando entri nella frattura.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_SEAL_DESC1", "SALTA la fase di difesa! La frattura si apre SUBITO."), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_SEAL_DESC2", "Nessuna ondata da combattere, vai diretto al portale!"), 15, y + 38, t["text_value"])
        self.__CText(T("ITEM_SEAL_DESC3", "Ideale per fratture alte quando sei solo. Si consuma all'uso."), 15, y + 52, t["text_muted"])
        y += 85

        # =====================================================
        # CALIBRATORE
        # =====================================================
        self.__CBar(5, y, 420, 80, 0x33FF6600)
        self.__CBar(5, y, 5, 80, 0xFFFF6600)
        self.__CTextTip(T("ITEM_CALIBRATOR_TITLE", "CALIBRATORE FRATTURE"), 130, y + 5, 0xFFFF6600,
            "Calibratore Fratture", 0xFFFF6600, [
                ("VNUM: 50167 | Cooldown: 30 minuti", 0xFF888888),
                "---",
                ("La prossima frattura sara' ALMENO C-Rank!", 0xFF00FF00),
                ("Filtra via E-Rank e D-Rank.", 0xFFCCCCCC),
                "---",
                ("REQUISITO: Devi essere C-Rank minimo!", 0xFFFF4444),
                ("Consumato allo spawn della frattura.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_CALIBRATOR_DESC1", "La prossima Frattura che spawna sara' ALMENO C-Rank!"), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_CALIBRATOR_DESC2", "Filtra via fratture E e D. Si consuma allo spawn."), 15, y + 36, t["text_muted"])
        self.__CText(T("ITEM_CALIBRATOR_DESC3", "Utile per cercare fratture di alto valore!"), 15, y + 50, t["text_muted"])
        self.__CText(T("ITEM_CALIBRATOR_REQ", "REQUISITO: Devi essere almeno C-Rank per usarlo!"), 15, y + 64, 0xFFFF4444)
        y += 90

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # SCANNER DI FRATTURE
        # =====================================================
        self.__CText(T("ITEMS_EXTRA_TITLE", "ALTRI ITEM SPECIALI"), 155, y, 0xFFFFA500)
        y += 25

        self.__CBar(5, y, 420, 80, 0x330088FF)
        self.__CBar(5, y, 5, 80, 0xFF0088FF)
        self.__CTextTip(T("ITEM_SCANNER_TITLE", "SCANNER DI FRATTURE"), 135, y + 5, 0xFF0088FF,
            "Scanner di Fratture", 0xFF0088FF, [
                ("VNUM: 50160 | Cooldown: 30 minuti", 0xFF888888),
                "---",
                ("Forza lo spawn IMMEDIATO di una frattura!", 0xFF00FF00),
                ("Appare vicino a te (+3,+3 dalla tua pos).", 0xFFCCCCCC),
                "---",
                ("Il rank segue le regole normali:", 0xFFCCCCCC),
                ("tuo rank attuale + max 1 sopra.", 0xFFCCCCCC),
                ("Non funziona nei dungeon.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_SCANNER_DESC1", "Forza lo SPAWN IMMEDIATO di una frattura vicino a te!"), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_SCANNER_DESC2", "Il rank segue le regole normali (tuo rank + max 1 sopra)."), 15, y + 36, t["text_muted"])
        self.__CText(T("ITEM_SCANNER_DESC3", "Cooldown: 30 minuti. Non funziona nei dungeon."), 15, y + 50, t["text_muted"])
        self.__CText(T("ITEM_SCANNER_DESC4", "Usa questo quando vuoi una frattura SUBITO!"), 15, y + 64, 0xFF00FF00)
        y += 90

        # =====================================================
        # STABILIZZATORE DI RANGO
        # =====================================================
        self.__CBar(5, y, 420, 80, 0x33FFD700)
        self.__CBar(5, y, 5, 80, 0xFFFFD700)
        self.__CTextTip(T("ITEM_STABILIZER_TITLE", "STABILIZZATORE DI RANGO"), 125, y + 5, GOLD_COLOR,
            "Stabilizzatore di Rango", GOLD_COLOR, [
                ("VNUM: 50161 | Cooldown: 30 minuti", 0xFF888888),
                "---",
                ("SCEGLI il rank della prossima frattura!", 0xFF00FF00),
                ("Menu con tutti i rank disponibili.", 0xFFCCCCCC),
                "---",
                ("Esempio: vuoi materiali B-Rank?", 0xFFCCCCCC),
                ("Usa lo Stabilizzatore e seleziona B!", 0xFFCCCCCC),
                "---",
                ("Puoi scegliere SOLO rank <= al tuo.", 0xFFFF6666),
                ("Consumato allo spawn della frattura.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_STABILIZER_DESC1", "SCEGLI TU quale rank di frattura evocare!"), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_STABILIZER_DESC2", "Menu con tutte le fratture disponibili per il tuo rank."), 15, y + 36, t["text_value"])
        self.__CText(T("ITEM_STABILIZER_DESC3", "Cooldown: 30 minuti. Scelta diretta del rank!"), 15, y + 50, t["text_muted"])
        self.__CText(T("ITEM_STABILIZER_DESC4", "Ideale per mirare un rank specifico (es: B per materiali)."), 15, y + 64, 0xFF00FF00)
        y += 90

        # =====================================================
        # SEGNALE D'EMERGENZA
        # =====================================================
        self.__CBar(5, y, 420, 65, 0x33FF4444)
        self.__CBar(5, y, 5, 65, 0xFFFF4444)
        self.__CTextTip(T("ITEM_SIGNAL_TITLE", "SEGNALE DI EMERGENZA"), 135, y + 5, 0xFFFF4444,
            "Segnale di Emergenza", 0xFFFF4444, [
                ("VNUM: 50165 | Cooldown: 10 minuti", 0xFF888888),
                "---",
                ("GARANTISCE la prossima Emergency Quest!", 0xFF00FF00),
                ("Salta la percentuale casuale (10%).", 0xFFCCCCCC),
                "---",
                ("La Emergency puo' essere EASY-GOD.", 0xFFCCCCCC),
                ("GOD = 250 kill in 180s = +1200 Gloria!", 0xFFFFD700),
                "---",
                ("Si consuma alla prima Emergency.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_SIGNAL_DESC1", "Forza l'attivazione di una EMERGENCY QUEST bonus!"), 15, y + 22, t["text_value"])
        self.__CText(T("ITEM_SIGNAL_DESC2", "La prossima Emergency sara' garantita (salta % casualita')."), 15, y + 36, t["text_muted"])
        self.__CText(T("ITEM_SIGNAL_DESC3", "Cooldown: 10 minuti. Si consuma alla prima Emergency."), 15, y + 50, t["text_muted"])
        y += 75

        # =====================================================
        # FRAMMENTO DI MONARCA
        # =====================================================
        self.__CBar(5, y, 420, 80, 0x33FF00FF)
        self.__CBar(5, y, 5, 80, 0xFFFF00FF)
        self.__CTextTip(T("ITEM_MONARCH_TITLE", "FRAMMENTO DI MONARCA"), 130, y + 5, 0xFFFF00FF,
            "Frammento di Monarca", 0xFFFF00FF, [
                ("VNUM: 50168 | Cooldown: 1 ORA", 0xFF888888),
                "---",
                ("Evoca frattura S-RANK garantita!", GOLD_COLOR),
                ("Attiva anche il Focus gratis (+20%)!", 0xFF00FF00),
                "---",
                ("REQUISITO: Devi essere A-Rank minimo!", 0xFFFF4444),
                ("L'item PIU' POTENTE del gioco!", 0xFFFF00FF),
                ("Consumato all'uso.", 0xFFFF6666),
            ], 200, 16)
        self.__CText(T("ITEM_MONARCH_DESC1", "Evoca una FRATTURA S-RANK + attiva il Focus gratis!"), 15, y + 22, GOLD_COLOR)
        self.__CText(T("ITEM_MONARCH_DESC2", "REQUISITO: Devi essere almeno A-Rank per usarlo!"), 15, y + 36, 0xFFFF4444)
        self.__CText(T("ITEM_MONARCH_DESC3", "Sceglie casualmente tra le fratture S-Rank disponibili nel DB."), 15, y + 50, t["text_muted"])
        self.__CText(T("ITEM_MONARCH_DESC4", "Cooldown: 1 ora. L'item piu' potente del gioco!"), 15, y + 64, t["text_muted"])
        y += 90

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # RIEPILOGO ITEM & VNUM
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CText("RIEPILOGO ITEM HUNTER (VNUM)", 120, y + 5, GOLD_COLOR)
        y += 38

        itemSummary = [
            ("50160", "Scanner di Fratture", "Spawna frattura subito"),
            ("50161", "Stabilizzatore Rango", "Scegli rank frattura"),
            ("50162", "Focus del Cacciatore", "+20% Gloria kill"),
            ("50163", "Chiave Dimensionale", "+50% bauli +30% item"),
            ("50164", "Sigillo di Conquista", "Salta difesa frattura"),
            ("50165", "Segnale di Emergenza", "Forza Emergency Quest"),
            ("50166", "Risonatore di Gruppo", "+20% Gloria party"),
            ("50167", "Calibratore Fratture", "Frattura C+ garantita"),
            ("50168", "Frammento di Monarca", "S-Rank + Focus (A+ req)"),
        ]

        for vnum, name, effect in itemSummary:
            self.__CBar(5, y, 420, 20, t["bg_dark"])
            self.__CText(vnum, 10, y + 2, t["text_muted"])
            self.__CText(name, 55, y + 2, t["text_value"])
            self.__CText(effect, 250, y + 2, 0xFF00FF00)
            y += 22

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # SISTEMA JACKPOT BAULI
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CTextTip(T("JACKPOT_TITLE", "SISTEMA JACKPOT BAULI"), 140, y + 5, GOLD_COLOR,
            "Jackpot Bauli", GOLD_COLOR, [
                ("Ogni Baule ha una chance di JACKPOT!", 0xFFCCCCCC),
                "---",
                ("Jackpot = Item rari EXTRA + Gloria bonus!", 0xFF00FF00),
                ("La % viene dalla tabella DB.", 0xFF888888),
                "---",
                ("Chiave Dimensionale AUMENTA la chance!", 0xFFFFD700),
                ("I premi Jackpot ruotano periodicamente.", 0xFFCCCCCC),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 75, t["bg_dark"])
        self.__CText(T("JACKPOT_INFO_1", "Ogni Baule ha una % di dare un JACKPOT!"), 90, y + 5, GOLD_COLOR)
        self.__CText(T("JACKPOT_INFO_2", "Jackpot = Item rari extra + Gloria bonus dal DB."), 65, y + 22, t["text_value"])
        self.__CText(T("JACKPOT_INFO_3", "La Chiave Dimensionale aumenta la chance di Jackpot."), 55, y + 38, t["text_value"])
        self.__CText(T("JACKPOT_INFO_4", "I Jackpot disponibili ruotano (dalla tabella hunter_chest_loot)."), 35, y + 55, t["text_muted"])
        y += 85

        # =====================================================
        # PARTECIPAZIONE VICINI
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x3300CCFF)
        self.__CTextTip(T("PARTICIPATION_TITLE", "PARTECIPAZIONE HUNTER VICINI"), 110, y + 5, 0xFF00CCFF,
            "Partecipazione Vicini", 0xFF00CCFF, [
                ("Quando un Elite muore, gli Hunter vicini:", 0xFFCCCCCC),
                "---",
                ("PARTY: 50% Gloria consolazione!", 0xFF00FF00),
                ("NON-PARTY: 15% Gloria base!", 0xFF00FF00),
                ("Progresso Missioni e Trial condiviso!", 0xFF00FF00),
                "---",
                ("Requisiti:", 0xFFFFAA00),
                ("  - Stessa mappa + vicinanza", 0xFFCCCCCC),
                ("  - Bauli/Fratture: solo progresso, NO Gloria", 0xFFFF6666),
                "---",
                ("Super Metin: +10%/Hunter (max +50%)!", 0xFFFFD700),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("PART_INFO_1", "Quando un Elite (Boss/SM) viene ucciso, Hunter VICINI ricevono:"), 15, y + 5, t["text_value"])
        self.__CText(T("PART_INFO_2", "- PARTY: 50% Gloria consolazione al killer"), 20, y + 22, 0xFF00FF00)
        self.__CText(T("PART_INFO_3", "- NON-PARTY vicini: 15% Gloria base + progresso"), 20, y + 36, 0xFF00FF00)
        self.__CText(T("PART_INFO_4", "- Bauli/Fratture: solo progresso missioni, NO Gloria!"), 20, y + 52, 0xFFFF6666)
        self.__CText(T("PART_INFO_5", "Super Metin: +10% per ogni Hunter vicino (max +50%)!"), 20, y + 66, 0xFFFFD700)
        y += 90

        return y
    
    def __LoadGuideOnline(self, y):
        """Guida al sistema Reward Tempo Online"""
        t = self.theme

        self.__CText(T("GUIDE_ONLINE_TITLE", "REWARD TEMPO ONLINE"), 145, y, 0xFF00FFFF)
        y += 25

        # Intro
        self.__CBar(5, y, 420, 55, 0x3300FFFF)
        self.__CText(T("ONLINE_INTRO1", "Ricevi Gloria AUTOMATICAMENTE restando online!"), 75, y + 5, 0xFF00FFFF)
        self.__CText(T("ONLINE_INTRO2", "Il sistema ti premia ogni ~30 minuti con Gloria bonus."), 45, y + 22, t["text_value"])
        self.__CText(T("ONLINE_INTRO3", "Piu' resti online, piu' guadagni (con tetto giornaliero)."), 45, y + 38, t["text_muted"])
        y += 65

        # Come funziona
        self.__CText(T("HOW_IT_WORKS", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        onlineSteps = [
            T("ONLINE_STEP_1", "1. Ogni ~30 min ricevi Gloria base automatica"),
            T("ONLINE_STEP_2", "2. Bonus Rank: il tuo Rank aumenta la % di Gloria"),
            T("ONLINE_STEP_3", "3. LUCKY GACHA: 5% chance di moltiplicatore x3!"),
            T("ONLINE_STEP_4", "4. Cap giornaliero basato sul Rank (E=1500, D=2000...N=6000)"),
            T("ONLINE_STEP_5", "5. Sessioni consecutive danno un contatore 'Streak Online'"),
        ]

        for step in onlineSteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 15
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # MILESTONE
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33FF6600)
        self.__CTextTip(T("MILESTONE_TITLE", "MILESTONE GIORNALIERE"), 145, y + 5, 0xFFFF6600,
            "Milestone Online", 0xFFFF6600, [
                ("Premi extra per tempo cumulativo online!", 0xFFCCCCCC),
                "---",
                ("1h = Premio base + Item", 0xFF00FF00),
                ("2h = Premio medio + Item migliore", 0xFF00FF00),
                ("4h = Premio alto + Item raro!", 0xFFFFAA00),
                ("8h = Premio MASSIMO + Item speciale!", 0xFFFFD700),
                "---",
                ("Anche multi-sessione (puoi disconnetterti).", 0xFFCCCCCC),
                ("Reset a mezzanotte.", 0xFF888888),
            ], 260, 16)
        y += 38

        self.__CText(T("MILESTONE_DESC", "Premi extra per tempo cumulativo online (anche multi-sessione):"), 20, y, t["text_value"])
        y += 20

        milestones = [
            ("1 ORA", T("MILESTONE_1H", "Gloria + Item bonus (configurato da DB)")),
            ("2 ORE", T("MILESTONE_2H", "Gloria + Item bonus (premio piu' alto)")),
            ("4 ORE", T("MILESTONE_4H", "Gloria + Item bonus (premio raro!)")),
            ("8 ORE", T("MILESTONE_8H", "Gloria + Item SPECIALE (premio massimo!)")),
        ]

        for time, desc in milestones:
            self.__CBar(5, y, 420, 22, t["bg_dark"])
            self.__CBar(5, y, 4, 22, 0xFFFF6600)
            self.__CText(time, 15, y + 3, 0xFFFF6600)
            self.__CText(desc, 90, y + 3, t["text_value"])
            y += 24

        y += 10

        # Cap giornaliero
        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("ONLINE_CAP_TITLE", "CAP GIORNALIERO PER RANK:"), 140, y + 5, 0xFFFFAA00)
        self.__CText("E: 1.500 | D: 2.000 | C: 2.500 | B: 3.000", 60, y + 22, t["text_value"])
        self.__CText("A: 4.000 | S: 5.000 | N: 6.000 " + T("GLORY", "Gloria"), 60, y + 38, t["text_value"])
        self.__CText(T("ONLINE_CAP_INFO", "Rank piu' alto = piu' Gloria possibile al giorno!"), 80, y + 55, t["text_muted"])
        y += 90

        # Malus Trial
        self.__CBar(5, y, 420, 45, 0x33FF0000)
        self.__CText(T("ONLINE_MALUS_TITLE", "IMPORTANTE:"), 180, y + 5, 0xFFFF4444)
        self.__CText(T("ONLINE_MALUS_INFO", "Il MALUS Prova d'Esame si applica anche ai reward online!"), 25, y + 22, t["text_value"])
        self.__CText(T("ONLINE_MALUS_INFO2", "Completa la Prova del Maestro per ricevere i premi pieni."), 35, y + 36, t["text_muted"])
        y += 55

        y += 10
        self.__CSep(5, y)
        y += 15

        # =====================================================
        # SISTEMA ACHIEVEMENT
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33FFD700)
        self.__CTextTip(T("ACHIEVEMENT_TITLE", "TRAGUARDI (ACHIEVEMENTS)"), 130, y + 5, GOLD_COLOR,
            "Achievement Hunter", GOLD_COLOR, [
                ("Traguardi che tracciano i tuoi progressi!", 0xFFCCCCCC),
                "---",
                ("Tipi: Kill, Boss, Metin, Fratture, Gloria", 0xFFCCCCCC),
                ("Progresso: AUTOMATICO (non devi fare nulla)", 0xFF00FF00),
                "---",
                ("Riscuoti: /hunter_claim [ID]", 0xFF00CCFF),
                ("Riscuoti TUTTI: /hunter_smart_claim", 0xFF00CCFF),
                "---",
                ("Premi: Gloria + Item esclusivi!", 0xFFFFD700),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText(T("ACH_INFO_1", "Completa traguardi per sbloccare ricompense!"), 80, y + 5, t["text_value"])
        self.__CText(T("ACH_INFO_2", "Tipi: Kill totali, Boss uccisi, Metin, Fratture, Gloria..."), 30, y + 22, t["text_value"])
        self.__CText(T("ACH_INFO_3", "Progresso automatico. Riscuoti con /hunter_claim [id]"), 40, y + 38, 0xFF00FF00)
        self.__CText(T("ACH_INFO_4", "oppure /hunter_smart_claim per riscuotere TUTTI!"), 60, y + 52, 0xFF00FF00)
        self.__CText(T("ACH_INFO_5", "Vedi i tuoi traguardi nel Tab 'Achiev' del Terminale."), 50, y + 68, t["text_muted"])
        y += 90

        # =====================================================
        # SISTEMA RIVALE
        # =====================================================
        self.__CBar(5, y, 420, 30, 0x33FF4444)
        self.__CTextTip(T("RIVAL_TITLE", "SISTEMA RIVALE"), 170, y + 5, 0xFFFF4444,
            "Sistema Rivale", 0xFFFF4444, [
                ("Competizione tra Hunter in classifica!", 0xFFCCCCCC),
                "---",
                ("Se qualcuno ti supera in ranking:", 0xFFFFAA00),
                ("  Ricevi un ALERT immediato!", 0xFFFF6666),
                "---",
                ("Classifiche monitorate:", 0xFFCCCCCC),
                ("  - Gloria Giornaliera", 0xFF00CCFF),
                ("  - Gloria Settimanale", 0xFF00CCFF),
                ("  - Metin distrutti", 0xFF00CCFF),
                ("  - Fratture completate", 0xFF00CCFF),
                "---",
                ("Stimola la competizione sana!", 0xFF00FF00),
            ], 260, 16)
        y += 38

        self.__CBar(5, y, 420, 65, t["bg_dark"])
        self.__CText(T("RIVAL_INFO_1", "Se SUPERI un altro Hunter in classifica:"), 80, y + 5, t["text_value"])
        self.__CText(T("RIVAL_INFO_2", "- Riceve un ALERT: 'Sei stato superato da [Nome]!'"), 20, y + 22, 0xFFFF6666)
        self.__CText(T("RIVAL_INFO_3", "- Funziona su: Gloria Giornaliera, Settimanale, Metin, Fratture"), 15, y + 38, t["text_muted"])
        self.__CText(T("RIVAL_INFO_4", "- Stimola la competizione tra Hunter!"), 20, y + 52, 0xFF00FF00)
        y += 75

        return y

    def __LoadGuideSupremo(self, y):
        """Guida al sistema Supremo (World Boss)"""
        t = self.theme

        self.__CText(T("GUIDE_SUPREMO_TITLE", "SUPREMO (WORLD BOSS)"), 130, y, 0xFFFF4444)
        y += 25

        # Intro
        self.__CBar(5, y, 420, 80, 0x33FF0000)
        self.__CText(T("SUP_INTRO1", "Il Supremo e' un BOSS MONDIALE che appare sulla mappa!"), 30, y + 5, 0xFFFF6666)
        self.__CText(T("SUP_INTRO2", "Vieni SELEZIONATO dal sistema per evocarlo."), 60, y + 22, t["text_value"])
        self.__CText(T("SUP_INTRO3", "TUTTI i giocatori possono attaccarlo e rubartelo!"), 40, y + 38, 0xFFFFAA00)
        self.__CText(T("SUP_INTRO4", "Ricompense ENORMI ma altrettanto RISCHIOSE."), 55, y + 55, GOLD_COLOR)
        y += 90

        # Come funziona
        self.__CText(T("SUP_HOW_TITLE", "COME FUNZIONA:"), 5, y, t["accent"])
        y += 22

        supSteps = [
            T("SUP_STEP1", "1. Il sistema ti SELEZIONA (casuale) e ricevi un invito"),
            T("SUP_STEP2", "2. Hai 2 ORE per accettare (poi l'invito scade)"),
            T("SUP_STEP3", "3. Parla con il NPC 'Guardiano dei Supremi' in Capitale"),
            T("SUP_STEP4", "4. Scegli 'Evoca il Supremo!' - il boss spawna VICINO A TE"),
            T("SUP_STEP5", "5. Hai 10 MINUTI per ucciderlo (timer visibile)"),
            T("SUP_STEP6", "6. NON allontanarti troppo o ricevi penalita'!"),
        ]

        for step in supSteps:
            self.__CText(step, 15, y, t["text_value"])
            y += 18

        y += 10
        self.__CSep(5, y)
        y += 15

        # Fasi UI
        self.__CBar(5, y, 420, 80, 0x33FF6600)
        self.__CText("LE 3 FASI DEL SUPREMO:", 150, y + 5, 0xFFFF6600)
        self.__CText("1. AWAKENING: Annuncio globale a TUTTI! 'Un Supremo si e' risvegliato!'", 15, y + 22, 0xFFFF4444)
        self.__CText("2. CHALLENGE: UI dedicata con timer, vita boss, distanza massima", 15, y + 40, 0xFFFFAA00)
        self.__CText("3. VICTORY: Celebrazione + ricompensa Gloria al killer/party!", 15, y + 58, 0xFF00FF00)
        y += 90

        # Ricompense
        self.__CBar(5, y, 420, 30, 0x3300FF00)
        self.__CText("RICOMPENSE GLORIA PER RANK:", 140, y + 5, 0xFF00FF88)
        y += 38

        self.__CBar(5, y, 420, 55, t["bg_dark"])
        self.__CText("E=500 | D=750 | C=1.000 | B=1.500 Gloria", 60, y + 8, GOLD_COLOR)
        self.__CText("A=2.000 | S=3.000 | N=5.000 Gloria", 80, y + 26, GOLD_COLOR)
        self.__CText("Il boss scala col TUO rank! Non serve rank minimo.", 55, y + 42, t["text_muted"])
        y += 65

        # Penalita'
        self.__CSep(5, y)
        y += 15
        self.__CBar(5, y, 420, 110, 0x33FF0000)
        self.__CBar(5, y, 5, 110, 0xFFFF0000)
        self.__CText("PENALITA' E RISCHI:", 160, y + 5, 0xFFFF4444)
        self.__CText("- TIMEOUT: boss non ucciso in 10 min = -Gloria (scala col rank)", 15, y + 25, 0xFFFF6666)
        self.__CText("  Moltiplicatore: E=1x D=1.2x C=1.5x B=2x A=2.5x S=3x N=4x", 15, y + 40, t["text_muted"])
        self.__CText("- RUBATO: un altro player lo uccide = TU perdi Gloria, lui prende 10%", 15, y + 58, 0xFFFF6666)
        self.__CText("- ABBANDONO: ti allontani troppo = -500 Gloria!", 15, y + 75, 0xFFFF6666)
        self.__CText("- RIFIUTO: parli col NPC senza invito = -250 Gloria (CD 5 min)", 15, y + 92, 0xFFFFAA00)
        y += 120

        # Party
        self.__CBar(5, y, 420, 55, 0x3300CCFF)
        self.__CText("SUPREMO IN PARTY:", 170, y + 5, 0xFF00CCFF)
        self.__CText("I membri del tuo party possono aiutarti! Fino a 8 persone.", 30, y + 22, t["text_value"])
        self.__CText("Tutti ricevono la UI di sfida e il tracciamento.", 45, y + 38, t["text_muted"])
        y += 65

        # Cooldown
        self.__CBar(5, y, 420, 35, t["bg_dark"])
        self.__CText("COOLDOWN: 5 minuti tra uno spawn e l'altro (globale, per il server).", 25, y + 8, 0xFFFFAA00)
        y += 45

        return y

    def __LoadGuideKarma(self, y):
        """Guida al sistema Karma"""
        t = self.theme

        self.__CText(T("GUIDE_KARMA_TITLE", "SISTEMA KARMA (ALLINEAMENTO)"), 100, y, 0xFF00FF00)
        y += 25

        # Intro
        self.__CBar(5, y, 420, 65, 0x3300FF00)
        self.__CText("Il Karma rappresenta la tua reputazione come Hunter.", 40, y + 5, 0xFFFFFFFF)
        self.__CText("Segue AUTOMATICAMENTE la tua Gloria: piu' Gloria = piu' Karma.", 20, y + 22, 0xFF00FF00)
        self.__CText("Si vede come ALLINEAMENTO nel pannello personaggio.", 40, y + 42, t["text_value"])
        y += 75

        # Formula
        self.__CText("COME SI CALCOLA:", 5, y, t["accent"])
        y += 22

        self.__CBar(5, y, 420, 45, t["bg_dark"])
        self.__CText("Karma = Gloria / 10  (fino al cap del tuo Rank)", 60, y + 5, GOLD_COLOR)
        self.__CText("Esempio: 5.000 Gloria con Rank D (cap 9.999) = Karma 500", 30, y + 25, t["text_muted"])
        y += 55

        # Cap per rank
        self.__CSep(5, y)
        y += 15
        self.__CText("CAP KARMA PER RANK:", 5, y, t["accent"])
        y += 22

        self.__CBar(5, y, 420, 80, t["bg_dark"])
        self.__CText("E: max 1.999 Gloria contata    (Karma max: 199)", 20, y + 5, t["text_value"])
        self.__CText("D: max 9.999                   (Karma max: 999)", 20, y + 19, t["text_value"])
        self.__CText("C: max 49.999                  (Karma max: 4.999)", 20, y + 33, t["text_value"])
        self.__CText("B: max 149.999                 (Karma max: 14.999)", 20, y + 47, 0xFFFFAA00)
        self.__CText("A: max 499.999 | S: max 1.499.999 | N: illimitato", 20, y + 63, GOLD_COLOR)
        y += 90

        # Come si guadagna/perde
        self.__CBar(5, y, 420, 55, 0x3300FF00)
        self.__CBar(5, y, 5, 55, 0xFF00FF00)
        self.__CText("COME SALE IL KARMA:", 170, y + 5, 0xFF00FF88)
        self.__CText("Qualsiasi azione che ti da' Gloria: kill, missioni, eventi, online...", 15, y + 22, t["text_value"])
        self.__CText("Il Karma si sincronizza automaticamente (ogni ~30 secondi).", 25, y + 38, t["text_muted"])
        y += 65

        self.__CBar(5, y, 420, 45, 0x33FF0000)
        self.__CBar(5, y, 5, 45, 0xFFFF0000)
        self.__CText("COME SCENDE IL KARMA:", 160, y + 5, 0xFFFF4444)
        self.__CText("Perdi Gloria (difesa fallita, missioni incomplete) = Karma si abbassa.", 15, y + 22, 0xFFFF6666)
        y += 55

        # Salire di rank = piu' karma
        self.__CBar(5, y, 420, 45, 0x33FFD700)
        self.__CText("CONSIGLIO: Sali di Rank per SBLOCCARE il cap Karma!", 55, y + 5, GOLD_COLOR)
        self.__CText("A Rank E il cap e' basso. Fai il Rank-Up per crescere!", 55, y + 25, t["text_value"])
        y += 55

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

    def __OnBuy10(self, iid):
        net.SendChatPacket("/hunter_buy %d" % (iid + 10000))

    def __OnBuy100(self, iid):
        net.SendChatPacket("/hunter_buy %d" % (iid + 20000))

    def __OnBuyChest(self, iid):
        net.SendChatPacket("/hunter_chest_buy %d" % iid)

    def __OnBuyChest10(self, iid):
        net.SendChatPacket("/hunter_chest_buy %d" % (iid + 10000))

    def __OnBuyChest100(self, iid):
        net.SendChatPacket("/hunter_chest_buy %d" % (iid + 20000))
    
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

    def ShowGloryDetail(self, context, sourceType, sourceName, baseGlory, modifiers, finalGlory):
        """Mostra il pannello dettaglio Gloria a sinistra dello schermo.
           Sostituisce le vecchie linee syschat di dettaglio."""
        if self.gloryDetailWnd:
            self.gloryDetailWnd.ShowDetail(context, sourceType, sourceName, baseGlory, modifiers, finalGlory)

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
    
    def ShowEventStatus(self, eventName, duration, eventType="default", desc="", reward="", minRank="E", winnerPrize=0):
        """Mostra finestra stato evento"""
        if self.eventWnd:
            self.eventWnd.ShowEvent(eventName, duration, eventType, desc, reward, minRank, winnerPrize)
    
    def CloseEventStatus(self):
        """Chiude la finestra stato evento"""
        if self.eventWnd:
            self.eventWnd.Hide()
    
    # ========================================================================
    #  SUPREMO SYSTEM - UI DEDICATE
    # ========================================================================
    def ShowSupremoAwakening(self, summonerName, supremoName, rank):
        """Mostra announcement globale stile Solo Leveling quando un Supremo viene risvegliato"""
        if self.supremoAwakeningWnd:
            self.supremoAwakeningWnd.ShowAwakening(summonerName, supremoName, rank)
    
    def StartSupremoChallenge(self, summonerName, supremoName, vnum, rank, duration, reward, penalty, spawnX, spawnY, maxDistance):
        """Avvia la UI sfida Supremo dedicata"""
        if self.supremoChallengeWnd:
            self.supremoChallengeWnd.StartChallenge(summonerName, supremoName, vnum, rank, int(duration), int(reward), int(penalty), int(spawnX), int(spawnY), int(maxDistance))
    
    def UpdateSupremoChallenge(self, timeLeft, distance, status):
        """Aggiorna la UI sfida Supremo con tempo e distanza"""
        if self.supremoChallengeWnd:
            self.supremoChallengeWnd.UpdateChallenge(int(timeLeft), int(distance), status)
    
    def CloseSupremoChallenge(self, result, gloriaChange, message):
        """Chiude la UI sfida Supremo con risultato"""
        if self.supremoChallengeWnd:
            self.supremoChallengeWnd.EndChallenge(result, int(gloriaChange), message)
    
    def ShowSupremoVictory(self, supremoName, rank, gloriaReward):
        """Mostra effetto vittoria Supremo epico"""
        if self.supremoVictoryWnd:
            self.supremoVictoryWnd.ShowVictory(supremoName, rank, int(gloriaReward))
    
    # ========================================================================
    #  DAILY MISSIONS SYSTEM
    # ========================================================================
    def SetMissionsCount(self, count):
        """Prepara per ricevere dati missioni"""
        self.missionsCount = int(count)
        self.missionsData = []
    
    def AddMissionData(self, missionData):
        """Aggiunge dati di una missione"""
        # formato: id|name|type|current|target|reward|penalty|status|target_vnum
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
                    "status": parts[7],  # active, completed, failed
                    "target_vnum": int(parts[8]) if len(parts) >= 9 else 0
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
            if self.currentRankKey in ("S", "N"):
                self.bonusIndicatorText = "BONUS FRATTURE ATTIVO +50%"
            else:
                self.bonusIndicatorText = "BONUS SEAL +50%"
            self.fractureBonusActive = True
    
    def OpenMissionsPanel(self):
        """Apre pannello missioni giornaliere"""
        if self.missionsWnd:
            self.missionsWnd.Open(self.missionsData, self.theme)
    
    def OpenRankUpPanel(self):
        """Apre pannello Rank Up - mostra finestra principale con tab Ranking"""
        try:
            self.Show()
            self.SetTop()
            # Tab index 1 = Ranking
            self.__OnClickTab(1)
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
        """E' passata la mezzanotte - resetta cache eventi e dati giornalieri"""
        import chat

        # Pulisci cache eventi vecchi
        self.eventsData = []
        self.eventsCount = 0

        # RESET DATI GIORNALIERI DEL PLAYER
        self.playerData["daily_points"] = 0
        self.playerData["daily_kills"] = 0
        self.playerData["daily_pos"] = 0
        self.playerData["pending_daily_reward"] = 0

        # RESET CLASSIFICHE GIORNALIERE
        self.rankingData["daily"] = []
        self.rankingData["daily_points"] = []
        self.rankingData["daily_kills"] = []

        # Chiudi popup eventi se aperto (mostrera' dati vecchi)
        if self.eventsWnd and self.eventsWnd.IsShow():
            self.eventsWnd.Hide()

        # Notifica player
        chat.AppendChat(chat.CHAT_TYPE_INFO, "|cff00FFFF[HUNTER]|r Nuovo giorno! Classifiche giornaliere resettate.")

        # Aggiorna header con i nuovi dati (0 punti daily)
        self.__UpdateHeaderContent()

        # Se siamo nel tab statistiche o classifiche, forza refresh
        if self.currentTab == 0:
            self.__ClearContent()
            self.__LoadStats()
            self.__SavePositions()
            self.__UpdateScroll()
        elif self.currentTab == 1:
            self.__ClearContent()
            self.__LoadRanking(self.currentRankingView)
            self.__SavePositions()
            self.__UpdateScroll()
        elif self.currentTab == 4:
            self.__ClearContent()
            self.__LoadEvents(skipRequest=False)
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
        # AUTO-REFRESH: Aggiorna la tab ranking se visibile
        if self.IsShow() and self.currentTab == 1:
            try:
                self.__ClearContent()
                self.__LoadRanking(self.currentRankingView)
                self.__SavePositions()
                self.__UpdateScroll()
            except:
                pass
    
    def SetShopItems(self, d):
        self.shopData = d
        # AUTO-REFRESH: Aggiorna solo se nella tab shop (selector o normal, NON chests)
        if self.IsShow() and self.currentTab == 2 and self.shopMode != "chests":
            try:
                self.__ClearContent()
                self.__LoadShop()
                self.__SavePositions()
                self.__UpdateScroll()
            except:
                pass

    def SetChestShopItems(self, d):
        self.chestShopData = d
        # AUTO-REFRESH: Aggiorna se la tab shop (scrigni) e' visibile
        if self.IsShow() and self.currentTab == 2 and self.shopMode == "chests":
            try:
                self.__ClearContent()
                self.__LoadShopChests()
                self.__SavePositions()
                self.__UpdateScroll()
            except:
                pass
    
    def SetAchievements(self, d):
        self.achievementsData = d
        # Se la tab achievements è aperta, aggiorna automaticamente
        if self.IsShow() and self.currentTab == 3:
            self.__LoadTabContent(3)
    
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
        self.fractureData = d
    
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
    
    def RefreshCurrentPage(self):
        """Ricarica la pagina corrente (utile dopo claim achievement)"""
        if self.isLoaded and self.IsShow():
            self.__LoadTabContent(self.currentTab)
    
    def OnPressEscapeKey(self):
        self.Close()
        return True

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
        # I dati vengono gia' inviati al login da send_all_data() e send_trial_status()
        # Non serve richiedere nuovamente (evita errore 'direttiva non esiste')
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
            # I dati vengono gia' inviati al login da send_all_data() e send_trial_status()
            # Non serve richiedere nuovamente (evita errore 'direttiva non esiste')
            w.Open()
