import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import textTail
import net
import wndMgr
import acce
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime

# UI imports
import ui
import uiCommon
import uiPhaseCurtain
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiMount
import uiPrivateShopBuilder

# Module imports
import mouseModule
import consoleModule
import interfaceModule
import uimarbleshop
if app.ENABLE_SKILL_SELECT_FEATURE:
	import uiskillchoose

import musicInfo
import debugInfo

import stringCommander
import uipresentation
if app.ENABLE_KEYCHANGE_SYSTEM:
	import uiKeyChange
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop

if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import uiPrivateShop

from _weakref import proxy

# ============================================================
# 1. IMPORT HUNTER SYSTEM
# ============================================================
try:
	import uihunterlevel
	import uihunterlevel_gate_trial
	import uimercatogloria
	import uihunterboards
	import uipresentation
	HUNTER_SYSTEM_AVAILABLE = True
except ImportError:
	HUNTER_SYSTEM_AVAILABLE = False
	import dbg
	dbg.TraceError("HUNTER SYSTEM: Failed to import one or more hunter modules")

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0


class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		if app.ENABLE_SKILL_SELECT_FEATURE:
			self.skillSelect = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		# self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = None

		self.stream=stream
		self.__interfaceReady = False
		self.interface = interfaceModule.Interface()

		# NOTE: MakeInterface e ShowDefaultWindows spostati in OnUpdate()
		# per evitare blocco del main loop C++ (handshake timeout)

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.Hide()

		if app.ENABLE_SKILL_SELECT_FEATURE:
			self.skillSelect = uiskillchoose.SkillSelectWindow()
			self.skillSelect.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		# self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()
		self.wndMarbleShop = uimarbleshop.MarbleShopWindow()
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			self.wndMount = uiMount.MountWindow()


		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()
		self.itemDropQuestionDialog = None

		### INIZIO CODICE AGGIUNTO ###
		# Variabili per l'autoclick dello spazio
		self.auto_space_enabled = False
		self.auto_space_last_time = 0
		self.auto_space_delay = 0.4  # Ritardo in secondi (puoi cambiarlo)
		### FINE CODICE AGGIUNTO ###

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = uiKeyChange.KeyChangeWindow(self, self.interface)
			self.ADDKEYBUFFERCONTROL = player.KEY_ADDKEYBUFFERCONTROL
			self.ADDKEYBUFFERALT = player.KEY_ADDKEYBUFFERALT
			self.ADDKEYBUFFERSHIFT = player.KEY_ADDKEYBUFFERSHIFT

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		# MakeInterface spostato in OnUpdate() per non bloccare il main loop C++
		# durante Open(). Cosi' il C++ puo' fare recv/send (rispondere PING)
		# prima che MakeInterface blocchi nel frame successivo.

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		if app.ENABLE_KEYCHANGE_SYSTEM:
			pass
		else:
			self.__BuildKeyDict()
		self.__BuildDebugInfo()

		constInfo.IS_BONUS_CHANGER = False
		constInfo.IS_ACCE_WINDOW = False
		constInfo.IS_DRAGON_SOUL_OPEN = False

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			uiOfflineShopBuilder.Clear()

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE

		if len(constInfo.lastSentenceStack) > 0:
			constInfo.lastSentencePos = 0

		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		if app.ENABLE_SKILL_SELECT_FEATURE and self.skillSelect:
			self.skillSelect.Destroy()
			self.skillSelect = None
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		# self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None
		
		if self.wndMarbleShop:
			self.wndMarbleShop.Hide()
			self.wndMarbleShop = None

		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			if self.wndMount:
				self.wndMount.Hide()
				self.wndMount = None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None
			

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		constInfo.SetInterfaceInstance(None)
		app.HideCursor()
		if app.ENABLE_KEYCHANGE_SYSTEM:
			if self.wndKeyChange:
				self.wndKeyChange.KeyChangeWindowClose(True)
				self.wndKeyChange = None

		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}


		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		onPressKeyDict[app.DIK_F5]	= lambda : self.interface and self.interface.wndBlend and self.interface.wndBlend.btnUse()
		#onPressKeyDict[app.DIK_F6]	= lambda : self.interface.ToggleMarmurShopWindow()
		# onPressKeyDict[app.DIK_F5]	= lambda : self.interface.ToggleSwitchbotWindow()
		#onPressKeyDict[app.DIK_F7]	= lambda : self.interface.OpenLocationWindow() ## MODIFICA: Rimosso conflitto F7
		onPressKeyDict[app.DIK_F8]	= lambda : self.interface and self.interface.OpenRespWindow()
		onPressKeyDict[app.DIK_F9]	= lambda : self.interface and self.interface.BuffNPCOpenWindow()

		onPressKeyDict[app.DIK_RETURN]	= lambda : self.ChangeBonus()

		onPressKeyDict[app.DIK_F11]	= lambda : self.interface and self.interface.ToggleCollectWindow()

		onPressKeyDict[app.DIK_F12] = lambda : self.interface and self.interface.ToggleCollectionWindow()
		# onPressKeyDict[app.DIK_F12] = lambda : self.interface.OpenEventCalendar()

		if app.ENABLE_NEW_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]	= lambda : self.interface and self.interface.pet_window_open()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			onPressKeyDict[app.DIK_K]		= lambda : self.__PressExtendedInventory()

		# if app.ENABLE_ARTEFAKT_SYSTEM:
		# 	onPressKeyDict[app.DIK_U]		= lambda: self.interface.OpenArtefaktWindow()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		# onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey
		# NOTA: Y viene gestito direttamente in OnKeyDown (riga ~1436), questa entry non viene mai raggiunta
		# onPressKeyDict[app.DIK_Y]			= self.__PressYKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface and self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface and self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface and self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface and self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface and self.interface.ToggleDragonSoulWindow()
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			onPressKeyDict[app.DIK_U]			= lambda : self.interface and self.interface.TogglePrivateShopPanelWindowCheck()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface and self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface and self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface and self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface and self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()
		onPressKeyDict[app.DIK_TAB]			= lambda : self.interface and self.interface.ToggleMapaSwWindow()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()


		# CUBE_TEST
		#onPressKeyDict[app.DIK_K]			= lambda : self.interface.OpenCubeWindow()
		# CUBE_TEST_END

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	def ChangeBonus(self):
		if not self.interface:
			return
		if constInfo.IS_BONUS_CHANGER:
			if hasattr(self.interface, 'wndChangerWindow') and self.interface.wndChangerWindow:
				self.interface.wndChangerWindow.ChangeBonus()
		elif constInfo.IS_ACCE_WINDOW:
			acce.SendRefineRequest()
		elif constInfo.IS_DRAGON_SOUL_OPEN:
			if hasattr(self.interface, 'wndDragonSoulRefine') and self.interface.wndDragonSoulRefine:
				self.interface.wndDragonSoulRefine.PressDoRefineButton()

	def WyszukiwaraOpen(self):
		if self.interface and hasattr(self.interface, 'wndOfflineShopSearch') and self.interface.wndOfflineShopSearch:
			self.interface.wndOfflineShopSearch.OpenWindow()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()

	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				#net.SendChatPacket("/user_horse_ride")
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break

	def	__PressHKey(self):
		"""Gestione tasto H: CTRL+H = Cavallo, H = Guida"""
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			if self.interface:
				self.interface.ToggleHelpWindow()

	def	__PressYKey(self):
		"""DEAD CODE - Y viene gestito in OnKeyDown. Tenuto per riferimento."""
		if not (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)):
			uihunterlevel.ToggleHunterLevelWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			if self.interface:
				state = "EMOTICON"
				self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			if self.ShowNameFlag and self.interface:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if not self.interface:
				return
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if localeInfo.IsARABIC():
			if 0 <= localSlotIndex and localSlotIndex < 4:
				player.RequestUseLocalQuickSlot(3-localSlotIndex)
			else:
				player.RequestUseLocalQuickSlot(11-localSlotIndex)
		else:
			player.RequestUseLocalQuickSlot(localSlotIndex)

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def OpenKeyChangeWindow(self):
			if self.wndKeyChange:
				self.wndKeyChange.Open()

		def OpenWindow(self, type, state):
			if not self.interface:
				return
			if type == player.KEY_OPEN_STATE:
				self.interface.ToggleCharacterWindow(state)
			elif type == player.KEY_OPEN_INVENTORY:
				self.interface.ToggleInventoryWindow()
			elif type == player.KEY_OPEN_DDS:
				self.interface.ToggleDragonSoulWindow()
			elif type == player.KEY_OPEN_MINIMAP:
				self.interface.ToggleMiniMap()
			elif type == player.KEY_OPEN_LOGCHAT:
				self.interface.ToggleChatLogWindow()
			elif type == player.KEY_OPEN_GUILD:
				self.interface.ToggleGuildWindow()
			elif type == player.KEY_OPEN_MESSENGER:
				self.interface.ToggleMessenger()
			elif type == player.KEY_OPEN_HELP:
				self.interface.ToggleHelpWindow()
			elif type == player.KEY_TP_MAP:
				self.interface.ToggleMapaSwWindow()
			elif type == player.KEY_OPEN_EXTENDED_INV:
				self.interface.ToggleExtendedInventoryWindow()
			elif type == player.KEY_OPEN_PET:
				self.interface.pet_window_open()
			elif type == player.KEY_OPEN_DOPY:
				if self.interface.wndBlend:
					self.interface.wndBlend.btnUse()
			#elif type == player.KEY_OPEN_MARBLE:
				#self.interface.ToggleMarmurShopWindow()
			#elif type == player.KEY_OPEN_SAVE_LOCATION:
				#self.interface.OpenLocationWindow()
			elif type == player.KEY_OPEN_RESP:
				self.interface.OpenRespWindow()
			elif type == player.KEY_OPEN_BUFF:
				self.interface.BuffNPCOpenWindow()
			elif type == player.KEY_OPEN_MISSION:
				self.interface.ToggleCollectWindow()
			elif type == player.KEY_OPEN_COLLECTION:
				self.interface.ToggleCollectionWindow()
			elif type == player.KEY_RETURN:
				self.ChangeBonus()
			elif type == player.KEY_OPEN_DUNGEONS:
				self.interface.ToggleDungeonInfoWindow()

			elif type == player.KEY_CHANGECHANNEL1:
				net.MoveChannelGame(1)
			elif type == player.KEY_CHANGECHANNEL2:
				net.MoveChannelGame(2)
			elif type == player.KEY_CHANGECHANNEL3:
				net.MoveChannelGame(3)
			elif type == player.KEY_CHANGECHANNEL4:
				net.MoveChannelGame(4)
			elif type == player.KEY_CHANGECHANNEL5:
				net.MoveChannelGame(5)
			elif type == player.KEY_CHANGECHANNEL6:
				net.MoveChannelGame(6)
			#if app.ENABLE_GROWTH_PET_SYSTEM:
			#	if type == player.KEY_OPEN_PET:
			#		self.interface.TogglePetInformationWindow()
			#if app.ENABLE_AUTO_SYSTEM:
			#	if type == player.KEY_OPEN_AUTO:
			#		self.interface.ToggleAutoWindow()
			#if app.ENABLE_MONSTER_CARD:
			#	if type == player.KEY_MONSTER_CARD:
			#		self.interface.ToggleMonsterCardWindow()
			#if app.ENABLE_PARTY_MATCH:
			#	if type == player.KEY_PARTY_MATCH:
			#		self.interface.TogglePartyMatchWindow()
			#if app.ENABLE_DSS_KEY_SELECT:
			#	if type == player.KEY_SELECT_DSS_1:
			#		self.interface.DragonSoulKeySelect(0)
			#	elif type == player.KEY_SELECT_DSS_2:
			#		self.interface.DragonSoulKeySelect(1)

		def ScrollOnOff(self):
			if not self.interface:
				return
			if 0 == interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)
		# net.MoveChannelGame(pageIndex+1)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):
		if not self.interface:
			return
		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if not self.__interfaceReady:
			return
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		if not self.__interfaceReady:
			return
		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

		self.CheckGameButton()

	def RefreshStamina(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		if not self.__interfaceReady:
			return
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		if not self.interface:
			return
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		if not self.interface:
			return
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		if not self.interface:
			return
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type=0):
		if not self.interface:
			return
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		if not self.interface:
			return
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		if not self.interface:
			return
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		if not self.affectShower:
			return
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		if not self.affectShower:
			return
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		if not self.affectShower:
			return
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		try:
			if self.affectShower:
				self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
			if self.interface:
				if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
					self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
				elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
					self.BINARY_DragonSoulGiveQuilification()
		except Exception, e:
			dbg.TraceError("BINARY_NEW_AddAffect error: type=%s pointIdx=%s value=%s dur=%s err=%s" % (str(type), str(pointIdx), str(value), str(duration), str(e)))

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		try:
			if self.affectShower:
				self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
			if self.interface:
				if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
					self.interface.DragonSoulDeactivate()
		except Exception, e:
			dbg.TraceError("BINARY_NEW_RemoveAffect error: type=%s pointIdx=%s err=%s" % (str(type), str(pointIdx), str(e)))

	if app.ENABLE_AFFECT_FIX:
		def RefreshAffectWindow(self):
			if self.affectShower:
				self.affectShower.BINARY_NEW_RefreshAffect()


	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if not self.__interfaceReady:
			return
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if not self.__interfaceReady:
			return
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if not self.__interfaceReady:
			return
		if self.interface:
			self.interface.RefreshCharacter()

	if app.RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			# Auto-stop tutte le modalita' caccia su morte
			try:
				import autohunt
				autohunt.ForceStopAll()
			except:
				pass
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			# Auto-stop tutte le modalita' caccia su morte
			try:
				import autohunt
				autohunt.ForceStopAll()
			except:
				pass
			self.OpenRestartDialog()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			if not self.interface:
				return
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			if not self.interface:
				return
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		if not self.interface:
			return
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		if not self.targetBoard:
			return
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			if self.interface:
				self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		if not self.targetBoard:
			return
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		if not self.targetBoard:
			return
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		if not self.targetBoard:
			return
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHPTargetBoard(self, vid, iMinHP, iMaxHP):
			if not self.targetBoard:
				return
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			
			self.targetBoard.SetHP(iMinHP, iMaxHP)
			self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if not self.targetBoard:
			return
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		if not self.targetBoard:
			return
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		if not self.interface:
			return
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not self.interface:
			return
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not self.interface:
			return
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not self.interface:
			return
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		# if self.mapNameShower:
		# 	self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME
    
	def BINARY_OpenAtlasWindow(self):
		if not self.interface:
			return
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_GM:
			if self.interface:
				self.interface.RegisterGameMasterName(name)
		chat.AppendWhisper(mode, name, line)
		if self.interface:
			self.interface.RecvWhisper(name)

		# Auto-reply whisper se autohunt attivo
		try:
			import autohunt
			autohunt.GetAutoReplyManager().OnWhisper(name)
		except:
			pass

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		if self.interface:
			self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		if self.interface:
			self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		if not self.interface:
			return
		self.interface.RecvWhisper(name)

	# def OnPickMoney(self, money):
	# 	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	# 		chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
	# 	else:
	# 		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))
	def OnPickMoney(self, money):
		if not self.interface:
			return
		self.interface.OnPickMoneyNew(money)

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
			if not self.interface:
				return
			self.interface.OnPickChequeNew(cheque)
			# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_CHEQUE % (cheque))

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnItemShopError(self, type):
		try:
			self.PopupMessage(localeInfo.ITEMSHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		if not self.interface:
			return
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		if not self.interface:
			return
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		if not self.interface:
			return
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		if not self.interface:
			return
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## OfflineShop
	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def StartOfflineShop(self, vid):
			if not self.interface:
				return
			self.interface.OpenOfflineShopDialog(vid)
			
		def EndOfflineShop(self):
			if not self.interface:
				return
			self.interface.CloseOfflineShopDialog()
			
		def RefreshOfflineShop(self):
			if not self.interface:
				return
			self.interface.RefreshOfflineShopDialog()
        
	## Exchange
	def StartExchange(self):
		if not self.interface:
			return
		self.interface.StartExchange()

	def EndExchange(self):
		if not self.interface:
			return
		self.interface.EndExchange()

	def RefreshExchange(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		if not self.interface:
			return
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		if not self.interface:
			return
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		if not self.interface:
			return
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		if not self.interface:
			return
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		if not self.interface:
			return
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		if not self.interface:
			return
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		if not self.interface:
			return
		self.interface.ExitParty()
		if self.targetBoard:
			self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		if not self.interface:
			return
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		if not self.interface:
			return
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		if not self.interface:
			return
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		if not self.interface:
			return
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		if not self.__interfaceReady:
			return
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		if not self.interface:
			return
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		if not self.interface:
			return
		self.interface.ShowClock(second)

	def HideClock(self):
		if not self.interface:
			return
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if not self.interface:
			return
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if self.interface and True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		return
		# print "save screen"

		# # SCREENSHOT_CWDSAVE
		# if SCREENSHOT_CWDSAVE:
		# 	if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
		# 		os.mkdir(os.getcwd()+os.sep+"screenshot")

		# 	(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		# elif SCREENSHOT_DIR:
		# 	(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		# else:
		# 	(succeeded, name) = grp.SaveScreenShot()
		# # END_OF_SCREENSHOT_CWDSAVE

		# if succeeded:
		# 	chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s %s" % (name, localeInfo.SCREENSHOT_SAVE1, localeInfo.SCREENSHOT_SAVE2))
		# else:
		# 	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			player.SetQuickPage(self.quickSlotPageIndex + 1)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		if not self.interface:
			return
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		if not self.interface:
			return
		self.interface.HideMouseImage()

	def StartAttack(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return
		except:
			pass
		player.SetAttackKeyState(True)

	def EndAttack(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return
		except:
			pass
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)
		
	def PickUpItem(self):
		if app.FAST_ITEMS_PICKUP:
			player.PickCloseItemVector()
		else:
			player.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		# =============================================================
		# FIX TASTO Y - HUNTER SYSTEM (METODO DIRETTO)
		# =============================================================
		if key == app.DIK_Y:
			# Se premi CTRL o SHIFT o ALT, ignora (per evitare conflitti con macro o altro)
			if not (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL) or app.IsPressed(app.DIK_LSHIFT)):
				import uihunterlevel
				uihunterlevel.ToggleHunterLevelWindow()
				return True

		# =============================================================
		# FIX F10 — Windows tratta F10 come WM_SYSKEYDOWN (menu di sistema).
		# Intercettiamo qui per evitare che Windows entri in modal menu loop
		# e blocchi il rendering del gioco fino al click.
		# =============================================================
		if key == app.DIK_F10:
			if self.interface:
				if hasattr(app, 'ENABLE_DUNGEON_INFO_SYSTEM') and app.ENABLE_DUNGEON_INFO_SYSTEM:
					self.interface.ToggleDungeonInfoWindow()
			return True

		if key == app.DIK_J:
			if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
				# CTRL+J: Apri Wiki e cerca l'item hoverato nel tooltip
				try:
					wikiVnum = getattr(constInfo, 'WIKI_TOOLTIP_VNUM', 0)
					if wikiVnum and wikiVnum > 0:
						uipresentation.OpenSearchByVnum(wikiVnum)
						return True
				except:
					pass
			elif not app.IsPressed(app.DIK_LSHIFT):
				uipresentation.ToggleWindow()
				return True
		# =============================================================

		if self.interface and self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		### INIZIO CODICE AGGIUNTO E MODIFICATO ###
		if key == app.DIK_F7:
			try:
				import autohunt
				if autohunt.IsAFK360Active():
					chat.AppendChat(chat.CHAT_TYPE_INFO, "[Auto-Spazio] Non disponibile durante AFK 360.")
					return True
			except:
				pass
			self.auto_space_enabled = not self.auto_space_enabled # Inverte lo stato (da True a False e viceversa)
			if self.auto_space_enabled:
				if player.IsDead():
					chat.AppendChat(chat.CHAT_TYPE_INFO, "[Auto-Spazio] Non puoi avviare da morto.")
					self.auto_space_enabled = False
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, "[Auto-Spazio] ATTIVATO (F7 per fermare)")
					self.auto_space_last_time = 0 # Resetta il timer all'avvio
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "[Auto-Spazio] DISATTIVATO")
			return True # Impedisce al tasto di essere processato da altre funzioni
		### FINE CODICE AGGIUNTO E MODIFICATO ###

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			if app.ENABLE_KEYCHANGE_SYSTEM:
				if self.wndKeyChange and self.wndKeyChange.IsOpen() == 1:
					if self.wndKeyChange.IsSelectKeySlot():
						if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LALT + self.ADDKEYBUFFERALT)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						else:
							self.wndKeyChange.ChangeKey(key)
				else:
					player.OnKeyDown(key)
			else:
				self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		if app.ENABLE_KEYCHANGE_SYSTEM:
			player.OnKeyUp(key)
		else:
			try:
				self.onClickKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

	def OnMouseLeftButtonDown(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return True
		except:
			pass
		if self.interface and self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return True
		except:
			pass
		if self.interface and self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				elif player.ITEM_CHEQUE == attachedItemIndex and app.ENABLE_CHEQUE_SYSTEM:
					self.__PutCheque(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				elif self.interface:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						if app.ENABLE_REFINE_RENEWAL:
							constInfo.AUTO_REFINE_TYPE = 2
							constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
							constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
							constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
							constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return
			
			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	if app.ENABLE_CHEQUE_SYSTEM:
		def __PutCheque(self, attachedType, attachedMoney, dstChrID):
			if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
				net.SendExchangeStartPacket(dstChrID)
				net.SendExchangeChequeAddPacket(attachedMoney)
			else:
				self.__DropCheque(attachedType, attachedMoney)

		def __DropCheque(self, attachedType, attachedMoney):
			# PRIVATESHOP_DISABLE_ITEM_DROP - 개 옘젘 열고 잘는  았 아 템 버림 방지
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
			# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			
			if attachedMoney>=1000:
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_CHEQUE_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
				return

			itemDropQuestionDialog = uiCommon.QuestionDialog()
			itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_CHEQUE % (attachedMoney))
			itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
			itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
			itemDropQuestionDialog.Open()
			itemDropQuestionDialog.dropType = attachedType
			itemDropQuestionDialog.dropCount = attachedMoney
			itemDropQuestionDialog.dropNumber = player.ITEM_CHEQUE
			self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or player.SLOT_TYPE_STONE_INVENTORY == dropType or player.SLOT_TYPE_BOX_INVENTORY == dropType or player.SLOT_TYPE_EFSUN_INVENTORY == dropType or player.SLOT_TYPE_CICEK_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				elif app.ENABLE_CHEQUE_SYSTEM and dropNumber == player.ITEM_CHEQUE:
					net.SendGoldChequePacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif app.WJ_SPLIT_INVENTORY_SYSTEM:
					if player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or player.SLOT_TYPE_STONE_INVENTORY == dropType or player.SLOT_TYPE_BOX_INVENTORY == dropType or player.SLOT_TYPE_EFSUN_INVENTORY == dropType or player.SLOT_TYPE_CICEK_INVENTORY == dropType:
						self.__SendDropItemPacket(dropNumber, dropCount, player.SLOT_TYPE_SKILL_BOOK_INVENTORY or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY or player.SLOT_TYPE_STONE_INVENTORY or player.SLOT_TYPE_BOX_INVENTORY or player.SLOT_TYPE_EFSUN_INVENTORY or player.SLOT_TYPE_CICEK_INVENTORY)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return
				
			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	def OnMouseRightButtonDown(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return True
		except:
			pass

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		try:
			import autohunt
			if autohunt.IsAFK360Active():
				return True
		except:
			pass
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		# === DEFERRED MAKEINTERFACE: gira al primo OnUpdate ===
		# A questo punto il C++ ha gia' fatto recv/send (risposto al PING del server)
		# quindi MakeInterface puo' bloccare senza causare disconnessione
		if not self.__interfaceReady:
			try:
				if app.ENABLE_EVENT_MANAGER:
					constInfo.SetInterfaceInstance(self.interface)
				self.interface.MakeInterface()
				self.interface.ShowDefaultWindows()
				constInfo.SetInterfaceInstance(self.interface)

				try:
					import hunter
					hunter.SetGameInterface(self.interface)
				except:
					pass

				if self.targetBoard:
					self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))

				self.__interfaceReady = True

				# === CATCH-UP: i pacchetti di refresh arrivati dal server durante
				# il caricamento sono stati scartati dai guard __interfaceReady.
				# I dati sono ancora nel modulo C++ player, forziamo la UI a rileggerli.
				try:
					self.RefreshInventory()
					self.RefreshEquipment()
					self.RefreshCharacter()
					self.RefreshStatus()
					self.RefreshSkill()
					self.RefreshAlignment()
					self.RefreshStamina()
					self.RefreshQuest()
					self.RefreshMessenger()
					self.CheckGameButton()
				except Exception, e:
					dbg.TraceError("DEFERRED_CATCHUP_WARN: " + str(e))

			except Exception, e:
				dbg.TraceError("CRITICAL: MakeInterface failed: " + str(e))
				import traceback
				traceback.print_exc()
				self.__interfaceReady = True
			return

		app.UpdateGame()

		# if self.mapNameShower.IsShow():
		# 	self.mapNameShower.Update()

		if app.IsPressed(app.DIK_Z):
			player.PickCloseItem()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()
			
		if self.interface:
			self.interface.BUILD_OnUpdate()

		# HUNTER SYSTEM PER-FRAME UPDATES (throttled internamente)
		if HUNTER_SYSTEM_AVAILABLE:
			try:
				uimercatogloria.ScanForOracle()
				uihunterboards.UpdateHunterBoards()
			except Exception, e:
				dbg.TraceError("HUNTER_ONUPDATE_CRASH: " + str(e))

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			uiPrivateShop.UpdateTitleBoard()

		### INIZIO CODICE AGGIUNTO (METODO NUOVO) ###
		if self.auto_space_enabled:
			if player.IsDead():
				self.auto_space_enabled = False
				chat.AppendChat(chat.CHAT_TYPE_INFO, "[Auto-Spazio] Personaggio morto, disattivato.")
			else:
				current_time = app.GetTime()
				if current_time - self.auto_space_last_time > self.auto_space_delay:
					player.SetAttackKeyState(True)
					player.SetAttackKeyState(False)
					self.auto_space_last_time = current_time
		### FINE CODICE AGGIUNTO (METODO NUOVO) ###

	def UpdateDebugInfo(self):
		#
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		showName = self.__IsShowName()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if self.targetBoard and 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not showName:
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if showName:
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			# Chiudi finestre Hunter se aperte (ESC → Close)
			try:
				import uipresentation
				wikiWnd = uipresentation.GetWikiWindow()
				if wikiWnd and wikiWnd.IsShow():
					wikiWnd.Close()
					return True
			except:
				pass

			if HUNTER_SYSTEM_AVAILABLE:
				try:
					hlWnd = uihunterlevel.GetHunterLevelWindow()
					if hlWnd and hlWnd.IsShow():
						hlWnd.Close()
						return True
				except:
					pass

			if self.interface:
				self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if not self.interface:
			return True
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		if self.interface:
			self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################
	
	# EXCHANGE
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if not self.interface:
				return
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)
	# END_OF_EXCHANGE

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if not self.interface:
			return
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if not self.interface:
			return
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    # GIFT command
	def Gift_Show(self):
		if not self.interface:
			return
		self.interface.ShowGift()


	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM
		if not self.interface:
			return

		self.interface.OpenCubeWindow()


		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			if not (hasattr(self.interface, 'wndCube') and self.interface.wndCube):
				return

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		if not self.interface:
			return
		self.interface.CloseCubeWindow()

	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		if not self.interface:
			return
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		if not self.interface:
			return
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		if not self.interface:
			return
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC

		self.cubeInformation[npcVNUM] = []

		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				if self.interface and hasattr(self.interface, 'wndCube') and self.interface.wndCube:
					self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)

			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))

			if 0 < modCount:
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_AddToQueue(self, vnum, value):
		if not self.interface:
			return
		self.interface.AppendQueue(vnum, value)

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		if not self.interface:
			return 0
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0



			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]

				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")

					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							if hasattr(self.interface, 'wndCube') and self.interface.wndCube:
								self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						if hasattr(self.interface, 'wndCube') and self.interface.wndCube:
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1



				itemIndex = itemIndex + 1

			if self.interface and hasattr(self.interface, 'wndCube') and self.interface.wndCube:
				self.interface.wndCube.Refresh()


		except Exception, msg:
			dbg.TraceError(msg)
			return 0


	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# @fixme003 (+if self.interface:)
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		if not self.interface:
			return
		self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		if not self.interface:
			return
		self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		if not self.interface:
			return
		self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_ShowIcon(self):
		if not self.interface:
			return
		self.interface.CardsShowIcon()
		
	def BINARY_Cards_Open(self, safemode):
		if not self.interface:
			return
		self.interface.OpenCardsWindow(safemode)

	def BINARY_DragonSoulGiveQuilification(self):
		if not self.interface:
			return
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		if not self.interface:
			return
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		if not self.interface:
			return
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		if not self.interface:
			return
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		if self.interface and self.interface.bigBoard:
			self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		if self.interface and self.interface.tipBoard:
			self.interface.tipBoard.SetTip(message)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def BINARY_DungeonInfoOpen(self):
			if self.interface:
				self.interface.DungeonInfoOpen()

		def BINARY_DungeonRankingRefresh(self):
			if self.interface:
				self.interface.DungeonRankingRefresh()

		def BINARY_DungeonInfoReload(self, onReset):
			if self.interface:
				self.interface.DungeonInfoReload(onReset)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		if not self.interface:
			return
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		if not self.interface:
			return
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		if not self.interface:
			return
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		if not self.interface:
			return
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		if not self.interface:
			return
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		if not self.interface:
			return
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		if self.interface and hasattr(self.interface, 'wndMiniMap') and self.interface.wndMiniMap:
			self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		if not self.interface:
			return
		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		if hasattr(self.interface, 'wndMiniMap') and self.interface.wndMiniMap:
			self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,
			"Teamler_on"            : self.__Team_On,
			"Teamler_off"            : self.__Team_Off, 

			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,

			#"selectskill_open"	: self.skillSelect.Open,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
			
			##MAPA_TELEPORTACJI
			"get_input_start"		: self.GetInputOn,
			"get_input_end"			: self.GetInputOff,
			"map_gui"				: self._mapa,
			##

		}
		if app.ENABLE_COLLECTIONS_SYSTEM:
			serverCommandList["RECV_Collection"] = self.__RecvCollection
			serverCommandList["RECV_CollectionItem"] = self.__RecvCollectionItem
			serverCommandList["RECV_CollectionBuild"] = self.__RecvCollectionBuild
			serverCommandList["RECV_CollectionRefresh"] = self.__RecvCollectionRefresh
			serverCommandList["RECV_CollectionIncrease"] = self.__RecvCollectionIncrease

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			serverCommandList["BuffNPCSummon"] = self.__SetBuffNPCSummon
			serverCommandList["BuffNPCUnsummon"] = self.__SetBuffNPCUnsummon
			serverCommandList["BuffNPCClear"] = self.__SetBuffNPCClear
			serverCommandList["BuffNPCBasicInfo"] = self.__SetBuffNPCBasicInfo
			serverCommandList["BuffNPCSkillInfo"] = self.__SetBuffNPCSkillInfo
			serverCommandList["BuffNPCSkillCooltime"] = self.__SetBuffNPCSkillSetSkillCooltime
			serverCommandList["BuffNPCCreatePopup"] = self.__SetBuffNPCCreatePopup

		if constInfo.GIFT_CODE_SYSTEM:
			serverCommandList.update({"OpenCodeWindow" : self.__OpenCodeWindow})

		if app.ENABLE_COLLECT_WINDOW:
			serverCommandList.update({"UpdateTime" : self.UpdateTime})
			serverCommandList.update({"UpdateChance" : self.UpdateChance})

		if app.ENABLE_DROP_INFO:
			serverCommandList.update({
				"DropInfoRefresh" : self.DropInfoRefresh,
			})

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList.update({"SetBodyCostumeHidden" : self.SetBodyCostumeHidden })
			serverCommandList.update({"SetHairCostumeHidden" : self.SetHairCostumeHidden })
			serverCommandList.update({"SetAcceCostumeHidden" : self.SetAcceCostumeHidden })
			serverCommandList.update({"SetWeaponCostumeHidden" : self.SetWeaponCostumeHidden })
			serverCommandList.update({"SetAuraCostumeHidden" : self.SetAuraCostumeHidden })
			serverCommandList.update({"SetStoleCostumeHidden" : self.SetStoleCostumeHidden })

		if app.BL_MOVE_CHANNEL:
			serverCommandList["server_info"] = self.__SeverInfo

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			serverCommandList["OpenOfflineShop"] =self.__OfflineShop_Open
			serverCommandList["OpenOfflineShopPanel"] =self.OpenOfflineShopPanel
			serverCommandList["OpenOfflineShopLogs"]=self.OpenOfflineShopLogs
		if app.ENABLE_NEW_PET_SYSTEM:
			serverCommandList["pet_info"] = self.__pet_info
			serverCommandList["pet_info_update"] = self.__pet_info_update

		#if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		#	serverCommandList["MountNPCEXPInfo"] = self.__SetMountNPCEXPInfo
		#	serverCommandList["MountNPCSkillInfo"] = self.__SetMountNPCSkillInfo
		#	serverCommandList["MountNPCClear"] = self.__SetMountClear
		#	serverCommandList["OpenHorseShoe"] =self.OpenHorseShoePanel

		# Hunter Level System
		serverCommandList["HunterPlayerData"]    = self.__HunterPlayerData
		serverCommandList["HunterRankingDaily"]  = self.__HunterRankingDaily
		serverCommandList["HunterRankingWeekly"] = self.__HunterRankingWeekly
		serverCommandList["HunterRankingTotal"]  = self.__HunterRankingTotal

		# GATE & TRIAL HANDLERS (SOLO LEVELING)
		serverCommandList["HunterGateStatus"]    = self.__HunterGateStatus
		serverCommandList["HunterGateEnter"]     = self.__HunterGateEnter
		serverCommandList["HunterGateComplete"]  = self.__HunterGateComplete
		serverCommandList["HunterTrialStart"]    = self.__HunterTrialStart
		serverCommandList["HunterTrialStatus"]   = self.__HunterTrialStatus
		serverCommandList["HunterTrialProgress"] = self.__HunterTrialProgress
		serverCommandList["HunterTrialComplete"] = self.__HunterTrialComplete
		serverCommandList["HunterGateTrialOpen"] = self.__HunterGateTrialOpen
		
		# SUPREMI (World Boss) System
		serverCommandList["HunterSupremoStatus"] = self.__HunterSupremoStatus
		serverCommandList["HunterSupremoSpawn"]  = self.__HunterSupremoSpawn
		serverCommandList["HunterSupremoAwakening"] = self.__HunterSupremoAwakening
		serverCommandList["HunterSupremoChallenge"] = self.__HunterSupremoChallenge
		serverCommandList["HunterSupremoChallengeUpdate"] = self.__HunterSupremoChallengeUpdate
		serverCommandList["HunterSupremoChallengeClose"] = self.__HunterSupremoChallengeClose
		serverCommandList["HunterSupremoVictory"] = self.__HunterSupremoVictory

		# EFFETTI EPICI GATE
		serverCommandList["HunterGateEntry"]          = self.__HunterGateEntry
		serverCommandList["HunterGateVictory"]        = self.__HunterGateVictory
		serverCommandList["HunterGateDefeat"]         = self.__HunterGateDefeat
		serverCommandList["HunterGateSelected"]       = self.__HunterGateSelected
		serverCommandList["HunterTrialProgressPopup"] = self.__HunterTrialProgressPopup

		# Classifiche Dettagliate
		serverCommandList["HunterRankingDailyKills"]  = self.__HunterRankingDailyKills
		serverCommandList["HunterRankingWeeklyKills"] = self.__HunterRankingWeeklyKills
		serverCommandList["HunterRankingTotalKills"]  = self.__HunterRankingTotalKills
		serverCommandList["HunterRankingFractures"] = self.__HunterRankingFractures
		serverCommandList["HunterRankingChests"]    = self.__HunterRankingChests
		serverCommandList["HunterRankingMetins"]    = self.__HunterRankingMetins

		# Dati Generici
		serverCommandList["HunterShopItems"]     = self.__HunterShopItems
		serverCommandList["HunterChestShopItems"] = self.__HunterChestShopItems
		serverCommandList["HunterShopRefresh"]   = self.__HunterShopRefresh
		serverCommandList["HunterAchievements"]  = self.__HunterAchievements
		serverCommandList["HunterAchievementsMore"] = self.__HunterAchievementsMore
		serverCommandList["HunterAchievementClaimed"] = self.__HunterAchievementClaimed
		serverCommandList["HunterCalendar"]      = self.__HunterCalendar
		serverCommandList["HunterActiveEvent"]   = self.__HunterActiveEvent
		serverCommandList["HunterTimers"]        = self.__HunterTimers
		serverCommandList["HunterOpenWindow"]    = self.__HunterOpenWindow
		serverCommandList["HunterMessage"]       = self.__HunterMessage
		serverCommandList["HunterFractures"]     = self.__HunterFractures

		# --- NOVITA' (Aggiungi queste righe) ---
		serverCommandList["HunterSystemSpeak"]      = self.__HunterSystemSpeak
		serverCommandList["HunterEmergency"]        = self.__HunterEmergency
		serverCommandList["HunterEmergencyUpdate"]  = self.__HunterEmergencyUpdate
		serverCommandList["HunterEmergencyClose"]   = self.__HunterEmergencyClose
		serverCommandList["HunterRivalAlert"]      = self.__HunterRivalUpdate
		serverCommandList["HunterWhatIf"]           = self.__HunterWhatIf
		serverCommandList["HunterWelcome"]          = self.__HunterWelcome
		serverCommandList["HunterBossAlert"]        = self.__HunterBossAlert
		serverCommandList["HunterSystemInit"]       = self.__HunterSystemInit
		serverCommandList["HunterAwakening"]        = self.__HunterAwakening
		serverCommandList["HunterActivation"]       = self.__HunterActivation
		serverCommandList["HunterRankUp"]           = self.__HunterRankUp
		serverCommandList["HunterOvertake"]         = self.__HunterOvertake
		serverCommandList["HunterSysMsg"]           = self.__HunterSysMsg
		serverCommandList["HunterEventStatus"]      = self.__HunterEventStatus
		serverCommandList["HunterEventClose"]       = self.__HunterEventClose
		serverCommandList["HunterCloseAll"]         = self.__HunterCloseAll

		# Fracture Defense & Speed Kill System
		serverCommandList["HunterFractureDefenseStart"]    = self.__HunterFractureDefenseStart
		serverCommandList["HunterFractureDefenseTimer"]    = self.__HunterFractureDefenseTimer
		serverCommandList["HunterFractureDefenseComplete"] = self.__HunterFractureDefenseComplete
		serverCommandList["HunterSpeedKillStart"]          = self.__HunterSpeedKillStart
		serverCommandList["HunterSpeedKillTimer"]          = self.__HunterSpeedKillTimer
		serverCommandList["HunterSpeedKillEnd"]            = self.__HunterSpeedKillEnd
		serverCommandList["HunterTip"]                     = self.__HunterTip

		# Daily Missions & Events System
		serverCommandList["HunterMissionsCount"]     = self.__HunterMissionsCount
		serverCommandList["HunterMissionData"]       = self.__HunterMissionData
		serverCommandList["HunterMissionProgress"]   = self.__HunterMissionProgress
		serverCommandList["HunterMissionComplete"]   = self.__HunterMissionComplete
		serverCommandList["HunterAllMissionsComplete"] = self.__HunterAllMissionsComplete
		serverCommandList["HunterMissionsOpen"]      = self.__HunterMissionsOpen
		serverCommandList["HunterEventsCount"]       = self.__HunterEventsCount
		serverCommandList["HunterEventData"]         = self.__HunterEventData
		serverCommandList["HunterEventBatch"]        = self.__HunterEventBatch
		serverCommandList["HunterEventJoined"]       = self.__HunterEventJoined
		serverCommandList["HunterEventsOpen"]        = self.__HunterEventsOpen
		serverCommandList["HunterNewDay"]            = self.__HunterNewDay
		serverCommandList["HunterOpenRankUp"]        = self.__HunterOpenRankUp
		serverCommandList["HunterResetUI"]           = self.__HunterResetUI

		# Chest/Baule System
		serverCommandList["HunterChestOpening"]  = self.__HunterChestOpening
		serverCommandList["HunterChestOpened"]   = self.__HunterChestOpened
		serverCommandList["HunterChestItem"]     = self.__HunterChestItem
		serverCommandList["HunterPartyChest"]    = self.__HunterPartyChest
		serverCommandList["HunterChestSpawn"]    = self.__HunterChestSpawn
		serverCommandList["HunterChestPreview"]  = self.__HunterChestPreview

		# Fracture Portal Preview (nuova UI immersiva)
		serverCommandList["HunterFracturePortal"] = self.__HunterFracturePortal

		# Hunter Floating Boards (clear al cambio mappa/dungeon)
		serverCommandList["HunterMobBoardClear"] = self.__HunterMobBoardClear

		# Handler aggiuntivi (notifiche, effetti, party info)
		serverCommandList["HunterNotification"]        = self.__HunterNotification
		serverCommandList["HunterFirstOfDay"]          = self.__HunterFirstOfDay
		serverCommandList["HunterEventWinner"]         = self.__HunterEventWinner
		serverCommandList["HunterDefenseClose"]        = self.__HunterDefenseClose
		serverCommandList["HunterResonatorReceived"]   = self.__HunterResonatorReceived
		serverCommandList["HunterResonatorTriggered"]  = self.__HunterResonatorTriggered
		serverCommandList["HunterPartyGloryDist"]      = self.__HunterPartyGloryDist
		serverCommandList["HunterPartyMeritGlory"]     = self.__HunterPartyMeritGlory
		serverCommandList["HunterFracturePing"]        = self.__HunterFracturePing
		serverCommandList["HunterSealEffect"]          = self.__HunterSealEffect
		serverCommandList["HunterChaosPossible"]       = self.__HunterChaosPossible
		serverCommandList["HunterMentorActive"]        = self.__HunterMentorActive
		serverCommandList["HunterChaosFracture"]       = self.__HunterChaosFracture
		serverCommandList["HunterChaosFractureComplete"] = self.__HunterChaosFractureComplete

		# Gloria Detail Panel (sostituisce syschat)
		serverCommandList["HunterGloryDetail"]         = self.__HunterGloryDetail

		# Presentazione / Guida Completa UI
		serverCommandList["HunterOpenGuide"]             = self.__HunterOpenGuide

		if app.ENABLE_ODLAMKI_SYSTEM:
			serverCommandList["OpenOdlamki"] = self.OpenOdlamki

		if app.ENABLE_COLLECT_WINDOW:
			serverCommandList["SetCollectWindowQID"] = self.__SetCollectWindowQID
			serverCommandList["OpenCollectWindow"] = self.OpenCollectWindow

		if app.ENABLE_LRN_BATTLE_PASS:
			serverCommandList.update({"SERVER_BattlePassClearReward" 	: self.SERVER_BattlePassClearReward })
			serverCommandList.update({"SERVER_BattlePassClearQuest" 	: self.SERVER_BattlePassClearQuest })
			serverCommandList.update({"SERVER_BattlePassLevel" 			: self.SERVER_BattlePassLevel })

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			serverCommandList["SetPrivateShopPremiumBuild"] = self.SetPrivateShopPremiumBuild

		serverCommandList.update({
			"botcontrol" : self.UpdateBotControlItems,
			"closebotcontrol" : self.CloseBotControl,
			"botcontrolname" : self.UpdateBotControlRealName,
			"botcontrolrof" : self.UpdateBotControlRof,
			"botcontrolnonce" : self.UpdateBotControlNonce,
		})

		# Auto Hunt License & Occupied & Dungeon
		serverCommandList["AUTOHUNT_LICENSE"] = self.__AutoHuntLicense
		serverCommandList["AutoHuntOccupied"] = self.__AutoHuntOccupied
		serverCommandList["AUTOHUNT_DUNGEON"] = self.__AutoHuntDungeon
		
		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)


	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetBodyCostumeHidden(self, hidden):
			constInfo.HIDDEN_BODY_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()

		def SetHairCostumeHidden(self, hidden):
			constInfo.HIDDEN_HAIR_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()

		def SetAcceCostumeHidden(self, hidden):
			constInfo.HIDDEN_ACCE_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()
				
		def SetStoleCostumeHidden(self, hidden):
			constInfo.HIDDEN_STOLE_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()

		def SetWeaponCostumeHidden(self, hidden):
			constInfo.HIDDEN_WEAPON_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()

		def SetAuraCostumeHidden(self, hidden):
			constInfo.HIDDEN_AURA_COSTUME = int(hidden)
			if self.interface:
				self.interface.RefreshVisibleCostume()

	if app.ENABLE_COLLECTIONS_SYSTEM:
		def __RecvCollection(self, collectionIdx, name, isComplete):
			if self.interface and self.interface.wndCollections:
				self.interface.wndCollections.AddCollection(collectionIdx, name, isComplete)
		
		def __RecvCollectionItem(self, collectionIdx, itemIdx, iVnum, iCount, myCount):
			if self.interface and self.interface.wndCollections:
				self.interface.wndCollections.AddItem(collectionIdx, itemIdx, iVnum, iCount, myCount)
				
		def __RecvCollectionBuild(self):
			if self.interface and self.interface.wndCollections:
				self.interface.wndCollections.Build()
		
		def __RecvCollectionRefresh(self, collectionIdx, itemIdx, myCount):
			if self.interface and self.interface.wndCollections:
				self.interface.wndCollections.UpdateValue(collectionIdx, itemIdx, myCount)
		
		def __RecvCollectionIncrease(self, isIncreased):
			if self.interface and self.interface.wndCollections:
				self.interface.wndCollections.SetIncrease(isIncreased)

	if app.ENABLE_PUNKTY_OSIAGNIEC:
		def OnPickPktOsiag(self, pkt_osiag):
			if self.interface:
				self.interface.OnPickPktOsiagNew(pkt_osiag)
			# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PKT_OSIAG_SYSTEM_PICK_PKT_OSIAG % (pkt_osiag))

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except Exception, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except Exception, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		if not self.interface:
			return
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		if not self.interface:
			return
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		if not self.interface:
			return
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		if not self.interface:
			return
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		if not self.interface:
			return
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	#if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		#def __SetMountNPCEXPInfo(self, level, cur_exp, exp):
		#	self.interface.Mount_SetEXPInfo(level, cur_exp, exp)

		#def __SetMountNPCSkillInfo(self, skillpoints, skilldata):
		#	self.interface.MountNPC_SetSkillInfo(int(skillpoints), skilldata)

		#def __SetMountClear(self):
		#	self.interface.MountNPC_Clear()
		
		#def OpenHorseShoePanel(self):
		#	self.interface.ToggleHorseshoePanel()

	if app.ENABLE_ODLAMKI_SYSTEM:
		def OpenOdlamki(self):
			if not self.interface:
				return
			self.interface.OpenOdlamkiWindow()

		def BINARY_OdlamkiItemRefreshWindow(self):
			if self.interface and hasattr(self.interface, 'wndOdlamki') and self.interface.wndOdlamki:
				self.interface.wndOdlamki.ClearWindow()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def __SetBuffNPCSummon(self):
			if not self.interface:
				return
			self.interface.BuffNPC_Summon()
			
		def __SetBuffNPCUnsummon(self):
			if not self.interface:
				return
			self.interface.BuffNPC_Unsummon()
			
		def __SetBuffNPCClear(self):
			if not self.interface:
				return
			self.interface.BuffNPC_Clear()

		def __SetBuffNPCBasicInfo(self, name, sex, intvalue):
			if not self.interface:
				return
			self.interface.BuffNPC_SetBasicInfo(str(name), int(sex), int(intvalue))

		def __SetBuffNPCSkillInfo(self, skill1, skill2, skill3):
			if not self.interface:
				return
			self.interface.BuffNPC_SetSkillInfo(skill1, skill2, skill3)
			
		def __SetBuffNPCSkillSetSkillCooltime(self, slot, timevalue):
			if not self.interface:
				return
			self.interface.BuffNPC_SetSkillCooltime(slot, timevalue)
			
		def __SetBuffNPCCreatePopup(self, type, value0, value1):
			if not self.interface:
				return
			self.interface.BuffNPC_CreatePopup(int(type), int(value0), int(value1))
			
		def BINARY_OpenCreateBuffWindow(self):
			if not self.interface:
				return
			self.interface.BuffNPC_OpenCreateWindow()

	def RefineSuceededMessage(self):
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.ENABLE_REFINE_RENEWAL:
			if self.interface:
				self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.ENABLE_REFINE_RENEWAL:
			if self.interface:
				self.interface.CheckRefineDialog(True)

	def CommandCloseSafebox(self):
		if not self.interface:
			return
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		if self.affectShower:
			self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		if self.affectShower:
			self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		if not self.interface:
			return
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	## PrivateShop
	def __PrivateShop_Open(self):
		if not self.interface:
			return
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		if not self.interface:
			return
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		if not self.interface:
			return
		self.interface.DisappearPrivateShop(vid)

	## OfflineShop
	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def __OfflineShop_Open(self):
			if not self.interface:
				return
			self.interface.OpenOfflineShopBuilder()
		
		def BINARY_OfflineShop_Appear(self, vid, text):	
			if not self.interface:
				return
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				self.interface.AppearOfflineShop(vid, text)
			
		def BINARY_OfflineShop_Disappear(self, vid):	
			if not self.interface:
				return
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				self.interface.DisappearOfflineShop(vid)	
				
		def OpenOfflineShopPanel(self, info):
			if not self.interface:
				return
			self.interface.ToggleOfflineShopAdminPanelWindow(info)

		def OpenOfflineShopLogs(self):
			if not self.interface:
				return
			self.interface.ToggleOfflineShopLogWindow()

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	## XMasBoom
	BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )

	def __XMasBoom_Update(self):
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			if self.interface:
				self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface and self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface and self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface and self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
	# END_OF_WEDDING

	if app.ENABLE_LOADING_PERFORMANCE:
		def OpenWarpShowerWindow(self):
			if self.interface:
				self.interface.OpenWarpShowerWindow()

		def CloseWarpShowerWindow(self):
			if self.interface:
				self.interface.CloseWarpShowerWindow()

	def BINARY_RemoveItemRefreshWindow(self):
		if self.interface and hasattr(self.interface, 'wndRemoveItem') and self.interface.wndRemoveItem:
			self.interface.wndRemoveItem.ClearWindow()

	if app.ENABLE_RESP_SYSTEM:
		def BINARY_SetMobRespData(self, mobVnum, data):
			if self.interface and hasattr(self.interface, 'wndResp') and self.interface.wndResp:
				self.interface.wndResp.SetMobRespData(mobVnum, data)

		def BINARY_SetMobDropData(self, mobVnum, data):
			if self.interface and hasattr(self.interface, 'wndResp') and self.interface.wndResp:
				self.interface.wndResp.SetMobDropData(mobVnum, data)

		def BINARY_SetMapData(self, data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount):
			if self.interface and hasattr(self.interface, 'wndResp') and self.interface.wndResp:
				self.interface.wndResp.SetMapData(data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount)

		def BINARY_RefreshResp(self, id, mobVnum, time, cord):
			if self.interface and hasattr(self.interface, 'wndResp') and self.interface.wndResp:
				self.interface.wndResp.RefreshRest(id, mobVnum, time, cord)

	def SendTitleActiveNow(self, id):
		if self.interface:
			self.interface.ActiveTileNow(id)

	def SendTitleEnable(self, id, val):
		if self.interface:
			self.interface.TitleEnable(id, val)

	def SendOfflineShopLogs(self, id, item, count, price, price2, date, action):
		if self.interface:
			self.interface.OfflineShopLogs(id, item, count, price, price2, date, action)

	def SendAntyExp(self, value):
		constInfo.ANTY_EXP_STATUS = value

	def SendWpadanie(self, value):
		constInfo.WPADANIE_DODATKOWE = value

	if app.WJ_SPLIT_INVENTORY_SYSTEM:
		def __PressExtendedInventory(self):
			if self.interface:
				self.interface.ToggleExtendedInventoryWindow()

	def SendWeeklyPage(self, page, active, season):
		if active == True:
			if self.interface:
				self.interface.SelectPage(page, season)

	def SendWeeklyInfo(self, pos, name, points, empire, job):
		if self.interface:
			self.interface.SendWeeklyInfo(pos, name, points, empire, job)

	def BINARY_ItemShopOpen(self, dataTime):
		if self.interface and hasattr(self.interface, 'wndItemShop') and self.interface.wndItemShop:
			self.interface.wndItemShop.Open(dataTime)

	def BINARY_ItemShopSetEditorFlag(self, flag):
		if self.interface and hasattr(self.interface, 'wndItemShop') and self.interface.wndItemShop:
			self.interface.wndItemShop.SetEditorFlag(flag)

	def BINARY_ItemShopRefresh(self):
		if self.interface and hasattr(self.interface, 'wndItemShop') and self.interface.wndItemShop:
			self.interface.wndItemShop.RefreshPage()

	def BINARY_ItemShopUpdateCoins(self):
		if self.interface and hasattr(self.interface, 'wndItemShop') and self.interface.wndItemShop:
			self.interface.wndItemShop.UpdateCoins()

	def BINARY_ItemShopShowPopup(self, type, id, category):
		if self.interface and hasattr(self.interface, 'wndItemShop') and self.interface.wndItemShop:
			self.interface.wndItemShop.ShowPopup(type, id, category)

	def BINARY_TombolaStart(self, pos, to_pos, to_spin, time):
		if not self.interface:
			return
		self.interface.TombolaStart(pos, to_pos, to_spin, time)

	def BINARY_TombolaSpinningItem(self, pos, vnum, count):
		if not self.interface:
			return
		self.interface.TombolaSetSpinningItem(pos, vnum, count)

	def BINARY_TombolaOpen(self):
		if not self.interface:
			return
		self.interface.TombolaOpen()

	def BINARY_TombolaSetPrice(self, group, price, price_type):
		if not self.interface:
			return
		self.interface.TombolaSetPrice(group, price, price_type)

	def BINARY_TombolaSetItem(self, group, vnum, count, chance):
		if not self.interface:
			return
		self.interface.TombolaSetItem(group, vnum, count, chance)

	def BINARY_TombolaClear(self):
		if not self.interface:
			return
		self.interface.TombolaClear()

 
	if app.ENABLE_DROP_INFO:
		if app.ENABLE_DROP_INFO_PCT:
			def BINARY_DropInfoAppendItem(self, mob_vnum, vnum, min_count, max_count, percentage):
				if not constInfo.dropInfoDict.has_key(mob_vnum):
					constInfo.dropInfoDict[mob_vnum] = []

				constInfo.dropInfoDict[mob_vnum].append({"vnum": [vnum], "min_count": min_count, "max_count": max_count, "percentage": percentage})
		else:
			def BINARY_DropInfoAppendItem(self, mob_vnum, vnum, min_count, max_count):
				if not constInfo.dropInfoDict.has_key(mob_vnum):
					constInfo.dropInfoDict[mob_vnum] = []

				constInfo.dropInfoDict[mob_vnum].append({"vnum": [vnum], "min_count": min_count, "max_count": max_count})
				
		def BINARY_DropInfoRefresh(self, mob_vnum):
			if self.targetBoard:
				self.targetBoard.DropInfoRefresh(mob_vnum)

		def DropInfoRefresh(self):
			constInfo.dropInfoDict = {}
			if self.targetBoard:
				self.targetBoard.DropInfoClear()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAcce(iAct, bWindow)

		def AlertAcce(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")
			# if bWindow:
			# 	self.PopupMessage(localeInfo.ACCE_DEL_SERVEITEM)
			# else:
			# 	self.PopupMessage(localeInfo.ACCE_DEL_ABSORDITEM)

		def SendAcceMaterials(self, id, vnum, count):
			if self.interface:
				self.interface.AcceMaterials(id, vnum, count)

	if app.ENABLE_AURA_SYSTEM:
		def ActAura(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAura(iAct, bWindow)

		def AlertAura(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")

	if app.ENABLE_LRN_LOCATION_SYSTEM:
		def BINARY_ReceiveLocationClear(self):
			if not self.interface:
				return
			self.interface.ClearLocationWindow()
			
		def BINARY_ReceiveLocationPos(self, position, index, posx, posy):
			if not self.interface:
				return
			self.interface.UpdateLocationWindowPos(position, index, posx, posy)

		def BINARY_ReceiveLocationName(self, name):
			if not self.interface:
				return
			self.interface.UpdateLocationWindowName(name)

	def __OpenItemShop(self):
		if not self.interface:
			return
		self.interface.RequestOpenItemShop()

	def ClickEvent(self):
		constInfo.OpcjeButton = 4

	if app.BL_MOVE_CHANNEL:
		def __SeverInfo(self, channelNumber, mapIndex):
			_chNum	= int(channelNumber.strip())
			_mapIdx	= int(mapIndex.strip())
			
			if _chNum == 99 or _mapIdx >= 10000:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 0)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)
				
			net.SetChannelName(_chNum)
			net.SetMapIndex(_mapIdx)
			if self.interface:
				self.interface.RefreshServerInfo(channelNumber)
			
	def _mapa(self, id):
		constInfo.id_quest_mapa = int(id)
	
	def GetInputOn(self):
		constInfo.INPUT_IGNORE = 1
		
	def GetInputOff(self):
		constInfo.INPUT_IGNORE = 0

	if app.ENABLE_NEW_PET_SYSTEM:	
		def __pet_info(self, arg):
			try:
				dat = arg.split("|")
				if dat[0] == "clear":
					constInfo.gui_pets["RACE"] = 0
					constInfo.gui_pets["NAME"] = ""
					return
				elif dat[0] == "state":
					constInfo.gui_pets["EXP"] = int(dat[1])
					constInfo.gui_pets["POINTS"] = int(dat[2])
					return
					
				constInfo.gui_pets["NAME"] = str(dat[0].replace("+", " "))
				constInfo.gui_pets["RACE"] = int(dat[1])
				constInfo.gui_pets["LEVEL"] = int(dat[2])
				constInfo.gui_pets["EXP"] = int(dat[3])
				constInfo.gui_pets["EXP_NEED"] = int(dat[4])
				constInfo.gui_pets["POINTS"] = int(dat[5])
				
				skill_data = dat[6].split("#")
			
				constInfo.gui_pets["SKILLS"] = []
				for skill in skill_data:
					if not len(skill):
						continue
				
					tmp = {}
					t = skill.split("&")
					if len(t) < 2:
						continue
						
					tmp["lv"] = int(t[0])

					tmp["affect"] = []
					for s in t[1].split("@"):
						tmp["affect"].append(s)
					
					constInfo.gui_pets["SKILLS"].append(tmp)
					
				if self.interface:
					self.interface.pet_refresh()
			except Exception, e:
				dbg.TraceError("__pet_info error: %s" % str(e))

		def __pet_info_update(self, arg):
			try:
				constInfo.gui_pets["ID"] = int(arg)
			except:
				pass

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			if not self.interface:
				return
			self.interface.RefreshSwitchbotWindow()
			
		def RefreshSwitchbotItem(self, slot):
			if not self.interface:
				return
			self.interface.RefreshSwitchbotItem(slot)

	def PotionsbalcudiaF(self):
		if self.interface and hasattr(self.interface, 'wndBlend') and self.interface.wndBlend:
			self.interface.wndBlend.OpenWindow()
		
	if app.ENABLE_MINIMAP_DUNGEONINFO:
		def BINARY_SetMiniMapDungeonInfoState(self, state):
			if self.interface:
				self.interface.SetMiniMapDungeonInfo(state)
		
		def BINARY_SetMiniMapDungeonInfoStage(self, cur_stage, max_stage):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoStage(cur_stage, max_stage)
		
		def BINARY_SetMiniMapDungeonInfoGauge(self, gauge_type, value1, value2):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoGauge(gauge_type, value1, value2)
		
		def BINARY_SetMiniMapDungeonInfoNotice(self, notice):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoNotice(notice)

		def BINARY_SetMiniMapDungeonInfoButton(self, status):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoButton(status)
			if status == 1:
				try:
					import autohunt
					if autohunt.wndAttack:
						autohunt.wndAttack.OnDungeonBossKilled()
				except:
					pass

		def BINARY_SetMiniMapDungeonInfoTimer(self, status, time):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoTimer(status, time)

	if app.ENABLE_COLLECT_WINDOW:
		def BINARY_UpdateCollectWindow(self, windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel):
			if self.interface and hasattr(self.interface, 'wndCollectWindow') and self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.AddData(windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel)
				
		def UpdateTime(self, val, time):
			if self.interface and hasattr(self.interface, 'wndCollectWindow') and self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendTime(val, time)

		def UpdateChance(self, val, chance):
			if self.interface and hasattr(self.interface, 'wndCollectWindow') and self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendChance(val, chance)

		def __SetCollectWindowQID(self, window, value):
			constInfo.CollectWindowQID[int(window)] = int(value)
			# self.interface.ToggleQuest(str(value))

		def OpenCollectWindow(self):
			if not self.interface:
				return
			self.interface.ToggleCollectWindow()
		
	if constInfo.GIFT_CODE_SYSTEM:
		def __OpenCodeWindow(self):
			if not self.interface:
				return
			self.interface.OpenGiftCodeWindow()

	if app.ENABLE_LRN_BATTLE_PASS:
		def SERVER_BattlePassClearQuest(self):
			if not self.interface:
				return
			self.interface.ClearBattlePassQuest()

		def SERVER_BattlePassClearReward(self):
			if not self.interface:
				return
			self.interface.ClearBattlePassReward()

		def SERVER_BattlePassLevel(self, info):
			if not self.interface:
				return
			info = info.split("#")
			self.interface.AppendBattlePassLevel(int(info[0]), int(info[1]), int(info[2]))

		def BINARY_BattlePassQuest(self, index, group, count, exp):
			if not self.interface:
				return
			self.interface.AppendBattlePassQuest(index, group, count, exp)

		def BINARY_BattlePassQuestData(self, index, count, status):
			if not self.interface:
				return
			self.interface.AppendBattlePassQuestData(index, count, status)

		def BINARY_BattlePassReward(self, level, item_free, count_free, item_premium, count_premium):
			if not self.interface:
				return
			self.interface.AppendBattlePassReward(level, item_free, count_free, item_premium, count_premium)

		def BINARY_BattlePassRewardData(self, level, status_free, status_premium):
			if not self.interface:
				return
			self.interface.AppendBattlePassRewardData(level, status_free, status_premium)

	if app.ENABLE_EVENT_MANAGER:
		def ClearEventManager(self):
			if not self.interface:
				return
			self.interface.ClearEventManager()
		def RefreshEventManager(self):
			if not self.interface:
				return
			self.interface.RefreshEventManager()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if not self.interface:
				return
			self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			if not self.interface:
				return
			self.interface.AppendEvent(int(dayIndex),int(eventID), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

	if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
		def SendLegendDamageData(self, vid, pos, name, level, race, empire, damage):
			if self.interface:
				self.interface.SendLegendDamageData(vid, pos, name, level, race, empire, damage)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def OpenPrivateShopPanel(self):
			if self.interface:
				self.interface.OpenPrivateShopPanel()
			
		def ClosePrivateShopPanel(self):
			if self.interface:
				self.interface.ClosePrivateShopPanel()
			
		def RefreshPrivateShopWindow(self):
			if self.interface:
				self.interface.RefreshPrivateShopWindow()
			
		def OpenPrivateShopSearch(self, mode):
			if not self.interface:
				return
			self.interface.OpenPrivateShopSearch(mode)
			
		def PrivateShopSearchRefresh(self):
			if self.interface:
				self.interface.PrivateShopSearchRefresh()

		def PrivateShopSearchUpdate(self, index, state):
			if self.interface:
				self.interface.PrivateShopSearchUpdate(index, state)
			
		def AppendMarketItemPrice(self, gold, cheque):
			if self.interface:
				self.interface.AppendMarketItemPrice(gold, cheque)

		def AddPrivateShopTitleBoard(self, vid, text, type):
			if self.interface:
				self.interface.AddPrivateShopTitleBoard(vid, text, type)

		def RemovePrivateShopTitleBoard(self, vid):
			if self.interface:
				self.interface.RemovePrivateShopTitleBoard(vid)

		def SetPrivateShopPremiumBuild(self):
			if self.interface:
				self.interface.SetPrivateShopPremiumBuild()
				
		def PrivateShopStateUpdate(self):
			if self.interface:
				self.interface.PrivateShopStateUpdate()

		def __Team_On(self, name):
			if self.interface and self.interface.wndMessenger:
				self.interface.wndMessenger.OnLogin(2, name)

		def __Team_Off(self, name):
			if self.interface and self.interface.wndMessenger:
				self.interface.wndMessenger.OnLogout(2, name)

	def UpdateBotControlItems(self, data):
		try:
			vv = data.split('|')
			vv.pop()
			itemArr = [int(i) for i in vv]
		except (ValueError, IndexError):
			dbg.TraceError("UpdateBotControlItems: malformed data")
			return
		if self.interface and hasattr(self.interface, 'wndBotControl') and self.interface.wndBotControl:
			self.interface.wndBotControl.UpdateItems(itemArr)
			self.interface.ShowBotControl()

	def UpdateBotControlRealName(self, name):
		if self.interface and hasattr(self.interface, 'wndBotControl') and self.interface.wndBotControl:
			self.interface.wndBotControl.SetRealItemName(str(name))

	def UpdateBotControlRof(self, rof):
		if self.interface and hasattr(self.interface, 'wndBotControl') and self.interface.wndBotControl:
			self.interface.wndBotControl.SetROF(int(rof))

	def UpdateBotControlNonce(self, nonce):
		if self.interface and hasattr(self.interface, 'wndBotControl') and self.interface.wndBotControl:
			self.interface.wndBotControl.SetNonce(int(nonce))

	def CloseBotControl(self):
		if self.interface and hasattr(self.interface, 'wndBotControl') and self.interface.wndBotControl:
			self.interface.wndBotControl.Close()

# ====================================================================================
	# HUNTER LEVEL SYSTEM HANDLERS (FIXED INDENTATION)
	# ====================================================================================

	def __HunterPlayerData(self, dataStr):
		try:
			parts = dataStr.split("|")
			if len(parts) >= 33:  # Updated for detailed stats
				data = {
					"name": parts[0],
					"total_points": int(parts[1]),
					"spendable_points": int(parts[2]),
					"daily_points": int(parts[3]),
					"weekly_points": int(parts[4]),
					"total_kills": int(parts[5]),
					"daily_kills": int(parts[6]),
					"weekly_kills": int(parts[7]),
					"login_streak": int(parts[8]),
					"streak_bonus": int(parts[9]),
					"total_fractures": int(parts[10]),
					"total_chests": int(parts[11]),
					"total_metins": int(parts[12]),
					"pending_daily_reward": int(parts[13]),
					"pending_weekly_reward": int(parts[14]),
					"daily_pos": int(parts[15]),
					"weekly_pos": int(parts[16]),
					# Detailed stats
					"chests_e": int(parts[17]), "chests_d": int(parts[18]), "chests_c": int(parts[19]),
					"chests_b": int(parts[20]), "chests_a": int(parts[21]), "chests_s": int(parts[22]), "chests_n": int(parts[23]),
					"boss_kills_easy": int(parts[24]), "boss_kills_medium": int(parts[25]),
					"boss_kills_hard": int(parts[26]), "boss_kills_elite": int(parts[27]),
					"metin_kills_normal": int(parts[28]), "metin_kills_special": int(parts[29]),
					"defense_wins": int(parts[30]), "defense_losses": int(parts[31]), "elite_kills": int(parts[32]),
					# Rank confermato dal DB (cambia SOLO tramite Prove del Maestro)
					"hunter_rank": parts[33] if len(parts) > 33 else "",
					# Coraggio (0-100) per sistema anti-farm dungeon
					"hunter_courage": int(parts[34]) if len(parts) > 34 else 100,
				}
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd: wnd.SetPlayerData(data)
			elif len(parts) >= 17:  # Fallback for old format
				data = {
					"name": parts[0], "total_points": int(parts[1]), "spendable_points": int(parts[2]),
					"daily_points": int(parts[3]), "weekly_points": int(parts[4]), "total_kills": int(parts[5]),
					"daily_kills": int(parts[6]), "weekly_kills": int(parts[7]), "login_streak": int(parts[8]),
					"streak_bonus": int(parts[9]), "total_fractures": int(parts[10]), "total_chests": int(parts[11]),
					"total_metins": int(parts[12]), "pending_daily_reward": int(parts[13]), "pending_weekly_reward": int(parts[14]),
					"daily_pos": int(parts[15]), "weekly_pos": int(parts[16]),
					# Defaults for detailed stats
					"chests_e": 0, "chests_d": 0, "chests_c": 0, "chests_b": 0, "chests_a": 0, "chests_s": 0, "chests_n": 0,
					"boss_kills_easy": 0, "boss_kills_medium": 0, "boss_kills_hard": 0, "boss_kills_elite": 0,
					"metin_kills_normal": 0, "metin_kills_special": 0, "defense_wins": 0, "defense_losses": 0, "elite_kills": 0,
					"hunter_rank": "",
					"hunter_courage": 100,
				}
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd: wnd.SetPlayerData(data)
		except Exception as e:
			import dbg
			dbg.TraceError("HUNTER DATA ERROR: " + str(e))

	def __HunterRankingDaily(self, dataStr): self.__ParseHunterRankingData(dataStr, "daily")
	def __HunterRankingWeekly(self, dataStr): self.__ParseHunterRankingData(dataStr, "weekly")
	def __HunterRankingTotal(self, dataStr): self.__ParseHunterRankingData(dataStr, "total")

	def __ParseHunterRankingData(self, dataStr, rankType):
		try:
			rankList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 3:
							d = {
								"name": parts[0],
								"points": int(parts[1]),
								"value": int(parts[1]),
								"kills": int(parts[2])
							}
							# FIX 03/03: Rank confermato dal server (4o campo)
							if len(parts) >= 4 and parts[3]:
								d["rank"] = parts[3]
							rankList.append(d)
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetRankingData(rankType, rankList)
		except Exception as e:
			import dbg
			dbg.TraceError("__ParseHunterRankingData error: " + str(e))

	def __HunterRankingDailyKills(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "daily_kills")
	def __HunterRankingWeeklyKills(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "weekly_kills")
	def __HunterRankingTotalKills(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "total_kills")
	def __HunterRankingFractures(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "fractures")
	def __HunterRankingChests(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "chests")
	def __HunterRankingMetins(self, dataStr): self.__ParseHunterRankingSimple(dataStr, "metins")

	def __ParseHunterRankingSimple(self, dataStr, rankType):
		try:
			rankList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 3:
							d = {
								"name": parts[0],
								"value": int(parts[1]),
								"points": int(parts[2])
							}
							# FIX 03/03: Rank confermato dal server (4o campo)
							if len(parts) >= 4 and parts[3]:
								d["rank"] = parts[3]
							rankList.append(d)
						elif len(parts) == 2:
							rankList.append({
								"name": parts[0],
								"value": int(parts[1]),
								"points": int(parts[1])
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetRankingData(rankType, rankList)
		except Exception as e:
			import dbg
			dbg.TraceError("__ParseHunterRankingSimple error: " + str(e))

	def __HunterShopItems(self, dataStr):
		try:
			shopList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 5:
							shopList.append({
								"id": int(parts[0]),
								"vnum": int(parts[1]),
								"count": int(parts[2]),
								"price": int(parts[3]),
								"name": parts[4].replace("+", " ")
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetShopItems(shopList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterShopItems error: " + str(e))

	def __HunterShopRefresh(self):
		"""Richiede refresh dati shop dopo acquisto"""
		try:
			net.SendChatPacket("/hunter_shop")
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterShopRefresh error: " + str(e))

	def __HunterChestShopItems(self, dataStr):
		"""Parser per dati Shop Scrigni: id,vnum,count,price,name,tier;..."""
		try:
			chestList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 6:
							chestList.append({
								"id": int(parts[0]),
								"vnum": int(parts[1]),
								"count": int(parts[2]),
								"price": int(parts[3]),
								"name": parts[4].replace("+", " "),
								"tier": int(parts[5])
							})
						elif len(parts) >= 5:
							chestList.append({
								"id": int(parts[0]),
								"vnum": int(parts[1]),
								"count": int(parts[2]),
								"price": int(parts[3]),
								"name": parts[4].replace("+", " "),
								"tier": 1
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetChestShopItems(chestList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterChestShopItems error: " + str(e))

	def __HunterAchievements(self, dataStr):
		try:
			achList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						# Formato: id,name,type,req,prg,unl,clm,rvnum,rcount,ryang,rycount
						if len(parts) >= 7:
							ach = {
								"id": int(parts[0]),
								"name": parts[1].replace("+", " "),
								"type": int(parts[2]),
								"requirement": int(parts[3]),
								"progress": int(parts[4]),
								"unlocked": int(parts[5]) == 1,
								"claimed": int(parts[6]) == 1
							}
							# Nuovi campi ricompensa (opzionali per retrocompatibilita')
							if len(parts) >= 11:
								ach["reward_vnum"] = int(parts[7])
								ach["reward_count"] = int(parts[8])
								ach["reward_yang_vnum"] = int(parts[9])
								ach["reward_yang_count"] = int(parts[10])
							achList.append(ach)
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetAchievements(achList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterAchievements error: " + str(e))

	def __HunterAchievementsMore(self, dataStr):
		"""FIX 04/03/2026: Pacchetto aggiuntivo achievements - append ai dati esistenti"""
		try:
			if not dataStr or dataStr == "EMPTY":
				return
			moreList = []
			entries = dataStr.split(";")
			for entry in entries:
				if entry:
					parts = entry.split(",")
					if len(parts) >= 7:
						ach = {
							"id": int(parts[0]),
							"name": parts[1].replace("+", " "),
							"type": int(parts[2]),
							"requirement": int(parts[3]),
							"progress": int(parts[4]),
							"unlocked": int(parts[5]) == 1,
							"claimed": int(parts[6]) == 1
						}
						if len(parts) >= 11:
							ach["reward_vnum"] = int(parts[7])
							ach["reward_count"] = int(parts[8])
							ach["reward_yang_vnum"] = int(parts[9])
							ach["reward_yang_count"] = int(parts[10])
						moreList.append(ach)
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.AppendAchievements(moreList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterAchievementsMore error: " + str(e))

	def __HunterAchievementClaimed(self, achId):
		"""Chiamato quando un achievement viene riscosso - richiede refresh UI e aggiorna pagina"""
		try:
			# Richiede tutti i dati aggiornati
			net.SendChatPacket("/hunter_request_data")
			# Forza refresh della pagina achievements nella UI
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd and wnd.IsShow():
				wnd.RefreshCurrentPage()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterAchievementClaimed error: " + str(e))

	def __HunterEventStatus_legacy(self, dataStr):
		"""LEGACY: Vecchio handler 2-field, mantenuto per backward compat"""
		try:
			wnd = uihunterlevel.GetHunterLevelWindow()
			if not wnd: return
			if dataStr == "NONE":
				wnd.SetActiveEvent(None, None)
			else:
				parts = dataStr.split("|")
				if len(parts) >= 2:
					wnd.SetActiveEvent(parts[0].replace("+", " "), parts[1].replace("+", " "))
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventStatus_legacy error: " + str(e))

	def __HunterCalendar(self, dataStr):
		try:
			calList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 4:
							calList.append({
								"day_index": int(parts[0]),
								"event_name": parts[1].replace("+", " "),
								"start_hour": int(parts[2]),
								"end_hour": int(parts[3])
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetCalendarEvents(calList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterCalendar error: " + str(e))

	def __HunterActiveEvent(self, dataStr):
		try:
			wnd = uihunterlevel.GetHunterLevelWindow()
			if not wnd: return
			if dataStr == "NONE":
				wnd.SetActiveEvent(None, None)
			else:
				parts = dataStr.split("|")
				if len(parts) >= 2:
					wnd.SetActiveEvent(parts[0].replace("+", " "), parts[1].replace("+", " "))
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterActiveEvent error: " + str(e))

	def __HunterTimers(self, dataStr):
		try:
			parts = dataStr.split("|")
			if len(parts) >= 2:
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd: wnd.SetTimers(parts[0], parts[1])
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterTimers error: " + str(e))

	def __HunterOpenWindow(self):
		try:
			uihunterlevel.OpenHunterLevelWindow()
		except:
			pass

	def __HunterOpenGuide(self):
		try:
			uipresentation.OpenHunterGuide()
		except:
			pass

	def __HunterMessage(self, msgStr):
		try:
			chat.AppendChat(chat.CHAT_TYPE_INFO, msgStr.replace("+", " "))
		except:
			pass

	def __HunterFractures(self, dataStr):
		try:
			fractureList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 2:
							fractureList.append({
								"name": parts[0].replace("+", " "),
								"req_points": int(parts[1])
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetFractures(fractureList)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterFractures error: " + str(e))

# ==============================================================================
	# HUNTER SYSTEM: AWAKENING HANDLERS (New Features v36)
	# ==============================================================================

	def __HunterSystemSpeak(self, msg):
		"""Il Sistema parla (Messaggio colorato in base al rank)"""
		try:
			if self.interface:
				# Nuovo formato: "rank_key|messaggio" per colorare con il rank del player
				if "|" in msg:
					parts = msg.split("|", 1)
					rank_key = parts[0].strip()  # FIX: strip() whitespace per lookup corretto
					actual_msg = parts[1] if len(parts) > 1 else ""
					self.interface.HunterSystemSpeak(actual_msg, rank_key)
				else:
					# Retrocompatibilita: vecchio formato senza rank
					self.interface.HunterSystemSpeak(msg, "E")
		except:
			pass

	def __HunterWelcome(self, data):
		"""Mostra benvenuto epico basato sul rank"""
		try:
			parts = data.split("|")
			if len(parts) >= 3:
				rank_key = parts[0].strip()  # FIX: strip() whitespace per lookup corretto
				name = parts[1].replace("+", " ")
				points = int(parts[2])
				if self.interface:
					self.interface.HunterWelcome(rank_key, name, points)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterWelcome error: " + str(e))

	def __HunterEmergency(self, data):
		"""Attiva missione Emergency Quest con parametri estesi"""
		try:
			parts = data.split("|")
			if len(parts) >= 4:
				title = parts[0].replace("+", " ")
				seconds = int(parts[1])
				vnums = parts[2]  # Può essere "0" o "8052,8053" per multi-vnum
				count = int(parts[3])
				description = ""
				difficulty = "NORMAL"
				penalty = 0

				# Parametri opzionali: description, difficulty, penalty
				if len(parts) >= 5:
					description = parts[4].replace("+", " ")
				if len(parts) >= 6:
					difficulty = parts[5]
				if len(parts) >= 7:
					try:
						penalty = int(parts[6])
					except:
						penalty = 0

				if self.interface:
					self.interface.HunterEmergency(title, seconds, vnums, count, description, difficulty, penalty)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEmergency error: " + str(e))

	def __HunterEmergencyUpdate(self, count):
		"""Aggiorna contatore Emergency Quest"""
		try:
			if self.interface:
				self.interface.HunterEmergencyUpdate(int(count))
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEmergencyUpdate error: " + str(e))

	def __HunterEmergencyClose(self, status):
		"""Chiude Emergency Quest (SUCCESS o FAIL)"""
		try:
			if self.interface:
				self.interface.HunterEmergencyClose(str(status))
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEmergencyClose error: " + str(e))

	def __HunterRivalUpdate(self, data):
		"""Mostra notifica rivale rilevato o superamento"""
		try:
			parts = data.split("|")
			if len(parts) >= 2:
				name = parts[0].replace("+", " ")
				points = int(parts[1])
				label = "Gloria"
				mode = "VICINO"
				if len(parts) >= 3:
					label = parts[2].replace("+", " ")
				if len(parts) >= 4:
					mode = parts[3]
				
				if self.interface:
					self.interface.HunterRivalUpdate(name, points, label, mode)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterRivalUpdate error: " + str(e))

	def __HunterWhatIf(self, data):
		"""Apre finestra delle scelte narrative con gestione Colori Fratture"""
		try:
			parts = data.split("|")
			if len(parts) >= 4:
				qid = parts[0]
				text = parts[1]
				o1 = parts[2]
				o2 = parts[3]
				o3 = ""
				color = "PURPLE" # Default

				# Gestione dinamica degli argomenti opzionali
				if len(parts) == 5:
					# Se il 5° è un colore conosciuto
					if parts[4] in ["GREEN", "BLUE", "ORANGE", "RED", "GOLD", "PURPLE", "BLACKWHITE"]:
						color = parts[4]
					else:
						o3 = parts[4]
				elif len(parts) >= 6:
					# Se ci sono 6+ argomenti, il 5° è opt3 e il 6° è il colore
					o3 = parts[4]
					color = parts[5]

				if self.interface:
					self.interface.HunterWhatIf(qid, text, o1, o2, o3, color)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterWhatIf error: " + str(e))

	def __HunterBossAlert(self, bossName):
		"""Mostra ALERT a schermo intero quando spawna un BOSS"""
		try:
			if self.interface:
				self.interface.HunterBossAlert(bossName)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterBossAlert error: " + str(e))

	def __HunterResetUI(self):
		"""Resetta tutte le posizioni delle finestre Hunter alle posizioni default"""
		try:
			from hunter_core import ResetAllWindowPositions
			ResetAllWindowPositions()
			# Mostra messaggio di conferma
			if self.interface:
				self.interface.HunterSystemSpeak("Posizioni finestre resettate! Riavvia il client per applicare.", "BLUE")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterResetUI error: " + str(e))

	def __HunterSystemInit(self):
		"""Mostra effetto inizializzazione sistema al login"""
		try:
			if self.interface:
				self.interface.HunterSystemInit()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterSystemInit error: " + str(e))

	def __HunterActivation(self, playerName):
		"""Mostra effetto attivazione Hunter al Lv 30"""
		try:
			if self.interface:
				self.interface.HunterActivation(playerName.replace("+", " "))
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterActivation error: " + str(e))

	def __HunterOvertake(self, data):
		"""Mostra effetto sorpasso in classifica"""
		try:
			parts = data.split("|")
			if len(parts) >= 2:
				overtakenName = parts[0].replace("+", " ")
				newPosition = int(parts[1])
				if self.interface:
					self.interface.HunterOvertake(overtakenName, newPosition)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterOvertake error: " + str(e))

	def __HunterSysMsg(self, data):
		"""Mostra messaggio di sistema con colore rank"""
		try:
			parts = data.split("|")
			if len(parts) >= 1:
				msg = parts[0].replace("+", " ")
				color = "PURPLE"  # Default
				if len(parts) >= 2:
					color = parts[1]
				if self.interface:
					self.interface.HunterSysMsg(msg, color)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterSysMsg error: " + str(e))

	def __HunterEventStatus(self, data):
		"""Mostra finestra stato evento"""
		try:
			if data == "NONE":
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd:
					wnd.SetActiveEvent(None, None)
				return
			parts = data.split("|")
			if len(parts) >= 2:
				eventName = parts[0].replace("+", " ")
				duration = int(parts[1])
				eventType = "default"
				desc = ""
				reward = ""
				minRank = "E"
				winnerPrize = 0
				if len(parts) >= 3:
					eventType = parts[2]
				if len(parts) >= 4:
					desc = parts[3].replace("+", " ")
				if len(parts) >= 5:
					reward = parts[4].replace("+", " ")
				if len(parts) >= 6:
					minRank = parts[5]
				if len(parts) >= 7:
					winnerPrize = int(parts[6])
				if self.interface:
					self.interface.HunterEventStatus(eventName, duration, eventType, desc, reward, minRank, winnerPrize)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventStatus error: " + str(e))

	def __HunterEventClose(self):
		"""Chiude la finestra stato evento"""
		try:
			if self.interface:
				self.interface.HunterEventClose()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventClose error: " + str(e))

	def __HunterCloseAll(self):
		"""Chiude tutte le finestre Hunter - usato per reset completo"""
		try:
			if self.interface:
				self.interface.HunterCloseAll()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterCloseAll error: " + str(e))

	# ====================================================================================
	# DAILY MISSIONS & EVENTS HANDLERS
	# ====================================================================================
	
	def __HunterMissionsCount(self, data):
		"""Riceve il numero di missioni giornaliere"""
		try:
			count = int(data)
			if self.interface:
				self.interface.HunterMissionsCount(count)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMissionsCount error: " + str(e))
	
	def __HunterMissionData(self, data):
		"""Riceve dati di una missione: id|name|type|progress|target|reward|penalty|status|target_vnum"""
		try:
			parts = data.split("|")
			if len(parts) >= 8:
				# Formato: id|name|type|current|target|reward|penalty|status|target_vnum
				targetVnum = 0
				if len(parts) >= 9:
					targetVnum = int(parts[8])
				missionData = "%d|%s|%s|%d|%d|%d|%d|%s|%d" % (
					int(parts[0]),
					parts[1].replace("+", " "),
					parts[2],
					int(parts[3]),
					int(parts[4]),
					int(parts[5]),
					int(parts[6]),
					parts[7],
					targetVnum
				)
				if self.interface:
					self.interface.HunterMissionData(missionData)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMissionData error: " + str(e))
	
	def __HunterMissionProgress(self, data):
		"""Aggiorna progresso missione: id|current|target"""
		try:
			parts = data.split("|")
			if len(parts) >= 3:
				missionId = int(parts[0])
				current = int(parts[1])
				target = int(parts[2])
				if self.interface:
					self.interface.HunterMissionProgress(missionId, current, target)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMissionProgress error: " + str(e))
	
	def __HunterMissionComplete(self, data):
		"""Missione completata: id|name|reward"""
		try:
			parts = data.split("|")
			if len(parts) >= 3:
				missionId = int(parts[0])
				name = parts[1].replace("+", " ")
				reward = int(parts[2])
				if self.interface:
					self.interface.HunterMissionComplete(missionId, name, reward)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMissionComplete error: " + str(e))
	
	def __HunterAllMissionsComplete(self, data):
		"""Tutte le missioni complete - bonus x1.5 + bonus fratture attivato"""
		try:
			parts = data.split("|")
			if len(parts) < 1 or not parts[0]:
				return
			bonus = int(parts[0])
			hasFractureBonus = len(parts) > 1 and parts[1] == "FRACTURE_BONUS_ACTIVE"
			
			if self.interface:
				self.interface.HunterAllMissionsComplete(bonus, hasFractureBonus)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterAllMissionsComplete error: " + str(e))
	
	def __HunterMissionsOpen(self):
		"""Apre pannello missioni"""
		try:
			if self.interface:
				self.interface.HunterMissionsOpen()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMissionsOpen error: " + str(e))
	
	def __HunterOpenRankUp(self):
		"""Apre pannello Rank Up dalla finestra Trial"""
		try:
			if self.interface:
				self.interface.HunterOpenRankUp()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterOpenRankUp error: " + str(e))

	# ============================================================
	# CHEST/BAULE HANDLERS
	# ============================================================
	def __HunterChestOpening(self, data):
		"""Effetto visivo pre-apertura baule: vid"""
		try:
			vid = int(data)
			# Suono apertura baule
			import snd
			snd.PlaySound("sound/ui/drop.wav")
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterChestOpening error: " + str(e))

	def __HunterChestOpened(self, data):
		"""Mostra effetto EPICO apertura baule: vnum|glory|name|color|itemName|jackpotGlory|jackpotItems"""
		try:
			parts = data.split("|")
			if len(parts) >= 4:
				vnum = int(parts[0])
				glory = int(parts[1])
				name = parts[2].replace("+", " ")
				color = parts[3] if len(parts) > 3 else "GOLD"
				itemName = parts[4].replace("+", " ") if len(parts) > 4 and parts[4] else ""
				jackpotGlory = int(parts[5]) if len(parts) > 5 and parts[5] else 0
				jackpotItems = parts[6].replace("+", " ") if len(parts) > 6 and parts[6] else ""
				
				# EFFETTO EPICO!
				import uihunterlevel_gate_effects
				uihunterlevel_gate_effects.ShowChestOpen(name, glory, color, itemName, jackpotGlory, jackpotItems)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterChestOpened error: " + str(e))

	def __HunterChestItem(self, data):
		"""Item bonus dal baule - gestito gia' in ChestOpened"""
		pass  # L'item viene mostrato nell'effetto principale

	def __HunterPartyChest(self, data):
		"""Notifica party chest: name|total_glory|member_count"""
		try:
			parts = data.split("|")
			if len(parts) >= 3:
				name = parts[0].replace("+", " ")
				total_glory = int(parts[1])
				member_count = int(parts[2])

				# Effetto party rapido
				import uihunterlevel_gate_effects
				uihunterlevel_gate_effects.ShowPartyChest(name, total_glory, member_count)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterPartyChest error: " + str(e))

	def __HunterChestSpawn(self, data):
		"""Notifica spawn baule dopo difesa frattura: name|color|rank"""
		try:
			parts = data.split("|")
			if len(parts) >= 2:
				name = parts[0].replace("+", " ")
				color = parts[1] if len(parts) > 1 else "GOLD"
				rank = parts[2] if len(parts) > 2 else "E"
				
				# Mostra effetto epico spawn baule
				import uihunterlevel_gate_effects
				uihunterlevel_gate_effects.ShowChestSpawn(name, color, rank)
				
				# Suono speciale per spawn baule
				import snd
				snd.PlaySound("sound/ui/make_soket.wav")
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterChestSpawn error: " + str(e))

	def __HunterChestPreview(self, data):
		"""Anteprima contenuto scrigno: NAME|TIER|GMIN|GMAX|IVNUM|IQTY|ICHANCE|LOOTDATA"""
		try:
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd:
				wnd.ShowChestPreview(data)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterChestPreview error: " + str(e))

	def __HunterFracturePortal(self, data):
		"""
		Mostra la finestra preview frattura immersiva.
		Format: name|rank|color|vnum|req_glory|req_power_rank|can_enter|can_force|player_glory|party_power_rank|seal_bonus|rewards
		"""
		try:
			import hunter
			hunter.ShowFracturePortalFromCmd(data)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterFracturePortal error: " + str(e))

	def __HunterMobBoardClear(self, data=""):
		"""Rimuove tutte le hunter floating board (cambio mappa, dungeon)"""
		try:
			uihunterboards.ClearAllHunterBoards()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterMobBoardClear error: " + str(e))

	# ============================================================
	def __HunterEventsCount(self, data):
		"""Riceve numero eventi"""
		try:
			count = int(data)
			if self.interface:
				self.interface.HunterEventsCount(count)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventsCount error: " + str(e))
	
	def __HunterEventData(self, data):
		"""Riceve dati evento: id|name|start_time|end_time|type|reward|status|desc|color|min_rank"""
		try:
			parts = data.split("|")
			if len(parts) >= 7:
				# Formato completo da hunter_scheduled_events
				eventData = {
					"id": int(parts[0]),
					"name": parts[1].replace("+", " "),
					"start_time": parts[2],
					"end_time": parts[3],
					"type": parts[4],
					"reward": parts[5].replace("+", " "),
					"status": parts[6],
					"desc": parts[7].replace("+", " ") if len(parts) > 7 else "",
					"color": parts[8] if len(parts) > 8 else "GOLD",
					"min_rank": parts[9] if len(parts) > 9 else "E"
				}
				if self.interface:
					self.interface.HunterEventData(eventData)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventData error: " + str(e))
	
	def __HunterEventBatch(self, data):
		"""Riceve batch di eventi: event1;event2;event3... dove ogni evento e' id~name~start~end~type~reward~status~min_rank~winner_prize~winner_name~winner_rank~is_registered~player_won"""
		try:
			events = data.split(";")
			for eventStr in events:
				parts = eventStr.split("~")
				if len(parts) >= 7:
					eventData = {
						"id": int(parts[0]),
						"name": parts[1].replace("+", " "),
						"start_time": parts[2],
						"end_time": parts[3],
						"type": parts[4],
						"reward": parts[5].replace("+", " "),
						"status": parts[6],
						"desc": "",
						"color": "GOLD",
						"min_rank": parts[7] if len(parts) > 7 else "E",
						"winner_prize": int(parts[8]) if len(parts) > 8 else 200,
						"winner_name": parts[9].replace("+", " ") if len(parts) > 9 else "",
						"winner_rank": parts[10] if len(parts) > 10 else "",
						"is_registered": int(parts[11]) if len(parts) > 11 else 0,
						"player_won": int(parts[12]) if len(parts) > 12 else 0
					}
					if self.interface:
						self.interface.HunterEventData(eventData)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventBatch error: " + str(e))
	
	def __HunterEventJoined(self, data):
		"""Conferma partecipazione evento: id|name|glory"""
		try:
			parts = data.split("|")
			if len(parts) >= 3:
				eventId = int(parts[0])
				name = parts[1].replace("+", " ")
				glory = int(parts[2])
				if self.interface:
					self.interface.HunterEventJoined(eventId, name, glory)
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventJoined error: " + str(e))
	
	def __HunterEventsOpen(self):
		"""Apre pannello eventi"""
		try:
			if self.interface:
				self.interface.HunterEventsOpen()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterEventsOpen error: " + str(e))

	def __HunterNewDay(self):
		"""E' passata la mezzanotte - resetta cache eventi e aggiorna UI"""
		try:
			if self.interface:
				self.interface.HunterNewDay()
		except Exception as e:
			import dbg
			dbg.TraceError("__HunterNewDay error: " + str(e))

	# ============================================================
	# HUNTER SYSTEM - FRACTURE DEFENSE SYSTEM
	# ============================================================

	def __HunterFractureDefenseStart(self, args):
		"""Inizia difesa frattura: fracture_name|duration|rank|totalMobs[|centerX|centerY|radius]"""
		try:
			parts = args.split("|")
			if len(parts) >= 7:
				# Nuovo formato con coordinate zona difesa
				fractureName = parts[0].replace("+", " ")
				duration = int(parts[1])
				rank = parts[2].strip()
				totalMobs = int(parts[3])
				# Le coordinate sono gia in formato world (moltiplicate x100 in Lua)
				centerX = int(parts[4])
				centerY = int(parts[5])
				radius = int(parts[6])
				if self.interface:
					self.interface.HunterFractureDefenseStart(fractureName, duration, rank, totalMobs, centerX, centerY, radius)
			elif len(parts) >= 4:
				fractureName = parts[0].replace("+", " ")
				duration = int(parts[1])
				rank = parts[2].strip()
				totalMobs = int(parts[3])
				if self.interface:
					self.interface.HunterFractureDefenseStart(fractureName, duration, rank, totalMobs)
			elif len(parts) >= 3:
				# Retrocompatibilita' con vecchio formato
				fractureName = parts[0].replace("+", " ")
				duration = int(parts[1])
				rank = parts[2].strip()
				if self.interface:
					self.interface.HunterFractureDefenseStart(fractureName, duration, rank, 0)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterFractureDefenseStart error: " + str(e))

	def __HunterFractureDefenseTimer(self, args):
		"""Aggiorna progresso difesa: killed|required|wave"""
		try:
			parts = args.split("|")
			if len(parts) >= 3:
				killed = int(parts[0])
				required = int(parts[1])
				wave = int(parts[2])
				if self.interface:
					self.interface.HunterFractureDefenseUpdate(killed, required, wave)
			elif len(parts) == 1:
				# Retrocompatibilita' con vecchio formato (solo timer)
				remainingSeconds = int(parts[0])
				if self.interface:
					self.interface.HunterFractureDefenseTimer(remainingSeconds)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterFractureDefenseTimer error: " + str(e))

	def __HunterFractureDefenseComplete(self, args):
		"""Completa difesa frattura: success|message"""
		try:
			parts = args.split("|")
			if len(parts) >= 2:
				success = int(parts[0])
				message = parts[1].replace("+", " ")
				if self.interface:
					self.interface.HunterFractureDefenseComplete(success, message)
			elif len(parts) == 1:
				success = int(parts[0])
				if self.interface:
					self.interface.HunterFractureDefenseComplete(success, "")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterFractureDefenseComplete error: " + str(e))

	# ============================================================
	# HUNTER SYSTEM - SPEED KILL SYSTEM
	# ============================================================

	def __HunterSpeedKillStart(self, args):
		"""Inizia speed kill: mob_type|duration|color"""
		try:
			parts = args.split("|")
			if len(parts) >= 3:
				mobType = parts[0]  # BOSS or SUPER METIN
				duration = int(parts[1])
				color = parts[2]
				if self.interface:
					self.interface.HunterSpeedKillStart(mobType, duration, color)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSpeedKillStart error: " + str(e))

	def __HunterSpeedKillTimer(self, remaining):
		"""Aggiorna timer speed kill"""
		try:
			remainingSeconds = int(remaining)
			if self.interface:
				self.interface.HunterSpeedKillTimer(remainingSeconds)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSpeedKillTimer error: " + str(e))

	def __HunterSpeedKillEnd(self, args):
		"""Termina speed kill: success|bonus (es: 1|300 o 0|0)"""
		try:
			parts = args.split("|")
			isSuccess = int(parts[0]) if len(parts) > 0 else 0
			bonusGlory = int(parts[1]) if len(parts) > 1 else 0
			if self.interface:
				self.interface.HunterSpeedKillEnd(isSuccess, bonusGlory)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSpeedKillEnd error: " + str(e))

	def __HunterTip(self, tipText):
		"""Mostra un tip nella finestra Hunter Tips"""
		try:
			if self.interface:
				self.interface.HunterShowTip(tipText.replace("+", " "))
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTip error: " + str(e))

	# ============================================================
	# HUNTER SYSTEM - GATE DUNGEON HANDLERS
	# ============================================================
	
	def __HunterGateStatus(self, args):
		"""
		Riceve: gate_id|gate_name|remaining_seconds|color_code
		Esempio: 3|Gate+Abissale|7200|ORANGE
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 4:
				gateId = int(parts[0])
				gateName = parts[1].replace("+", " ")
				remainingSeconds = int(parts[2])
				colorCode = parts[3]
				
				if self.interface:
					self.interface.HunterGateStatus(gateId, gateName, remainingSeconds, colorCode)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateStatus error: " + str(e))

	def __HunterSupremoStatus(self, args):
		"""
		Riceve: access_id|supremo_name|remaining_seconds|rank
		Esempio: 5|Signore+dell'Abisso|7200|B
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 4:
				accessId = int(parts[0])
				supremoName = parts[1].replace("+", " ")
				remainingSeconds = int(parts[2])
				rank = parts[3]
				
				if self.interface:
					self.interface.HunterSupremoStatus(accessId, supremoName, remainingSeconds, rank)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoStatus error: " + str(e))

	def __HunterSupremoSpawn(self, args):
		"""
		Riceve: supremo_name|rank|summoner_name
		Esempio: Signore+dell'Abisso|B|NomeGiocatore
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 3:
				supremoName = parts[0].replace("+", " ")
				rank = parts[1]
				summonerName = parts[2].replace("+", " ")
				
				if self.interface:
					self.interface.HunterSupremoSpawn(supremoName, rank, summonerName)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoSpawn error: " + str(e))

	def __HunterGateEnter(self, args):
		"""
		Riceve: gate_id|duration_minutes
		Esempio: 3|25
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 2:
				gateId = int(parts[0])
				duration = int(parts[1])
				
				if self.interface:
					self.interface.HunterGateEnter(gateId, duration)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateEnter error: " + str(e))

	def __HunterGateComplete(self, args):
		"""
		Riceve: success(0/1)|gloria_change
		Esempio: 1|800 (completato, +800 gloria)
		Esempio: 0|400 (fallito, -400 gloria)
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 2:
				success = int(parts[0]) == 1
				gloriaChange = int(parts[1])
				
				if self.interface:
					self.interface.HunterGateComplete(success, gloriaChange)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateComplete error: " + str(e))

	# ============================================================
	# HUNTER SYSTEM - RANK TRIAL (JOB CHANGE) HANDLERS
	# ============================================================

	def __HunterTrialStart(self, args):
		"""
		Riceve: trial_id|trial_name|to_rank|color_code
		Esempio: 2|Prova+del+Cacciatore|C|BLUE
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 4:
				trialId = int(parts[0])
				trialName = parts[1].replace("+", " ")
				toRank = parts[2]
				colorCode = parts[3]
				
				if self.interface:
					self.interface.HunterTrialStart(trialId, trialName, toRank, colorCode)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTrialStart error: " + str(e))

	def __HunterTrialStatus(self, args):
		"""
		Riceve: trial_id|trial_name|to_rank|color_code|remaining_seconds|
		        boss_cur|boss_req|metin_cur|metin_req|fracture_cur|fracture_req|
		        chest_cur|chest_req|daily_cur|daily_req|from_rank(opzionale)
		Esempio: 2|Prova+del+Cacciatore|C|BLUE|259200|3|5|7|10|2|5|3|5|10|15|B
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 15:
				trialId = int(parts[0])
				trialName = parts[1].replace("+", " ")
				toRank = parts[2]
				colorCode = parts[3]
				remainingSeconds = int(parts[4]) if parts[4] != "-1" else -1
				
				bossKills = int(parts[5])
				bossReq = int(parts[6])
				metinKills = int(parts[7])
				metinReq = int(parts[8])
				fractureSeals = int(parts[9])
				fractureReq = int(parts[10])
				chestOpens = int(parts[11])
				chestReq = int(parts[12])
				dailyMissions = int(parts[13])
				dailyReq = int(parts[14])
				
				# FIX: Leggi from_rank (16° campo) se presente
				fromRank = parts[15] if len(parts) >= 16 and parts[15] else toRank
				
				# Leggi nomi target (campi 17°-20°) se presenti
				bossNames = parts[16].replace("+", " ") if len(parts) >= 17 and parts[16] else ""
				metinNames = parts[17].replace("+", " ") if len(parts) >= 18 and parts[17] else ""
				fractureNames = parts[18].replace("+", " ") if len(parts) >= 19 and parts[18] else ""
				chestNames = parts[19].replace("+", " ") if len(parts) >= 20 and parts[19] else ""
				
				if self.interface:
					self.interface.HunterTrialStatus(
						trialId, trialName, toRank, colorCode, remainingSeconds,
						bossKills, bossReq, metinKills, metinReq,
						fractureSeals, fractureReq, chestOpens, chestReq,
						dailyMissions, dailyReq, fromRank,
						bossNames, metinNames, fractureNames, chestNames
					)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTrialStatus error: " + str(e))

	def __HunterTrialProgress(self, args):
		"""
		Riceve: trial_id|boss_cur/boss_req|metin_cur/metin_req|fracture_cur/fracture_req|
		        chest_cur/chest_req|daily_cur/daily_req
		Esempio: 2|4/5|8/10|3/5|4/5|12/15
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 6:
				trialId = int(parts[0])
				
				def parseProg(s):
					if "/" in s:
						a, b = s.split("/", 1)
						return int(a), int(b)
					return 0, 0
				
				bossKills, bossReq = parseProg(parts[1])
				metinKills, metinReq = parseProg(parts[2])
				fractureSeals, fractureReq = parseProg(parts[3])
				chestOpens, chestReq = parseProg(parts[4])
				dailyMissions, dailyReq = parseProg(parts[5])
				
				if self.interface:
					# FIX: Passa anche i req values per aggiornare UI anche se la finestra
					# non ha mai ricevuto un HunterTrialStatus completo
					self.interface.HunterTrialProgress(
						trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions,
						bossReq, metinReq, fractureReq, chestReq, dailyReq
					)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTrialProgress error: " + str(e))

	def __HunterTrialComplete(self, args):
		"""
		Riceve: new_rank|gloria_reward|trial_name
		Esempio: C|1000|Prova+del+Cacciatore
		"""
		try:
			parts = args.split("|")
			if len(parts) >= 3:
				newRank = parts[0]
				gloriaReward = int(parts[1])
				trialName = parts[2].replace("+", " ")
				
				if self.interface:
					self.interface.HunterTrialComplete(newRank, gloriaReward, trialName)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTrialComplete error: " + str(e))

	def __HunterGateTrialOpen(self):
		"""Apre la finestra principale del sistema Hunter Gate/Trial"""
		try:
			if self.interface:
				self.interface.HunterGateTrialOpen()
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateTrialOpen error: " + str(e))

	# ============================================================
	# HUNTER SYSTEM - EFFETTI EPICI
	# ============================================================

	def __HunterGateEntry(self, args):
		import chat
		try:
			parts = args.split("|")
			gateName = parts[0].replace("+", " ") if len(parts) > 0 else "Gate"
			colorCode = parts[1] if len(parts) > 1 else "RED"
			
			# Importa il file che hai appena creato
			import uihunterlevel_gate_effects
			uihunterlevel_gate_effects.ShowGateEntry(gateName, colorCode)
			
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateEntry error: " + str(e))

	def __HunterGateVictory(self, args):
		"""Effetto vittoria Gate - Esplosione gloriosa dorata"""
		try:
			parts = args.split("|")
			gateName = parts[0].replace("+", " ") if len(parts) > 0 else "Gate"
			gloria = int(parts[1]) if len(parts) > 1 else 500
			
			import uihunterlevel_gate_effects
			uihunterlevel_gate_effects.ShowGateVictory(gateName, gloria)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateVictory error: " + str(e))

	def __HunterGateDefeat(self, args):
		"""Effetto sconfitta Gate - Schermo frantumato"""
		try:
			penalty = int(args) if args else 250
			
			import uihunterlevel_gate_effects
			uihunterlevel_gate_effects.ShowGateDefeat(penalty)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateDefeat error: " + str(e))

	def __HunterGateSelected(self, args):
		"""Effetto selezione Gate - mostra notifica + apre finestra Gate"""
		try:
			parts = args.split("|")
			gateName = parts[0].replace("+", " ") if len(parts) > 0 else "Gate"
			rankRequired = parts[1] if len(parts) > 1 else "E"
			hoursLeft = int(parts[2]) if len(parts) > 2 else 2
			minsLeft = int(parts[3]) if len(parts) > 3 else 0

			import uihunterlevel_gate_effects
			uihunterlevel_gate_effects.ShowGateSelected(gateName, rankRequired, hoursLeft, minsLeft)

			# Apri anche la finestra Gate/Trial dopo un breve delay
			if self.interface and hasattr(self.interface, 'wndHunterLevel'):
				hunterWnd = self.interface.wndHunterLevel
				if hunterWnd:
					hunterWnd.Show()
					# Seleziona tab Trial/Gate se disponibile
					if hasattr(hunterWnd, 'OpenGateTab'):
						hunterWnd.OpenGateTab()
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGateSelected error: " + str(e))

	def __HunterTrialProgressPopup(self, args):
		"""Popup progresso Trial"""
		try:
			parts = args.split("|")
			progressType = parts[0] if len(parts) > 0 else "boss"
			current = int(parts[1]) if len(parts) > 1 else 0
			required = int(parts[2]) if len(parts) > 2 else 0

			import uihunterlevel_gate_effects
			uihunterlevel_gate_effects.ShowTrialProgress(progressType, current, required)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterTrialProgressPopup error: " + str(e))

	def __HunterRankUp(self, args):
		"""Effetto promozione Rank"""
		try:
			parts = args.split("|")
			oldRank = parts[0] if len(parts) > 0 else "E"
			newRank = parts[1] if len(parts) > 1 else "D"
			
			# Usa l'interfaccia per chiamare la finestra corretta
			if self.interface:
				self.interface.HunterRankUp(oldRank, newRank)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterRankUp error: " + str(e))

	def __HunterAwakening(self, args):
		"""Effetto risveglio livello - args e' il nome del player"""
		try:
			playerName = args.replace("+", " ") if args else ""
			if self.interface:
				self.interface.HunterAwakening(playerName)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterAwakening error: " + str(e))

	# ============================================================
	# SUPREMO SYSTEM - UI HANDLERS
	# ============================================================

	def __HunterSupremoAwakening(self, args):
		"""Mostra UI epica quando un Supremo viene risvegliato"""
		try:
			parts = args.split("|")
			summonerName = parts[0].replace("+", " ") if len(parts) > 0 else "???"
			supremoName = parts[1].replace("+", " ") if len(parts) > 1 else "Supremo"
			rank = parts[2] if len(parts) > 2 else "E"
			
			if self.interface:
				self.interface.HunterSupremoAwakening(summonerName, supremoName, rank)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoAwakening error: " + str(e))

	def __HunterSupremoChallenge(self, args):
		"""Avvia UI sfida Supremo"""
		try:
			parts = args.split("|")
			summonerName = parts[0].replace("+", " ") if len(parts) > 0 else "???"
			supremoName = parts[1].replace("+", " ") if len(parts) > 1 else "Supremo"
			vnum = int(parts[2]) if len(parts) > 2 else 0
			rank = parts[3] if len(parts) > 3 else "E"
			duration = int(parts[4]) if len(parts) > 4 else 600
			reward = int(parts[5]) if len(parts) > 5 else 500
			penalty = int(parts[6]) if len(parts) > 6 else 500
			spawnX = int(parts[7]) if len(parts) > 7 else 0
			spawnY = int(parts[8]) if len(parts) > 8 else 0
			maxDistance = int(parts[9]) if len(parts) > 9 else 2000
			
			if self.interface:
				self.interface.HunterSupremoChallenge(summonerName, supremoName, vnum, rank, duration, reward, penalty, spawnX, spawnY, maxDistance)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoChallenge error: " + str(e))

	def __HunterSupremoChallengeUpdate(self, args):
		"""Aggiorna UI sfida Supremo (tempo e distanza)"""
		try:
			parts = args.split("|")
			timeLeft = int(parts[0]) if len(parts) > 0 else 0
			distance = int(parts[1]) if len(parts) > 1 else 0
			status = parts[2] if len(parts) > 2 else "FIGHTING"
			
			if self.interface:
				self.interface.HunterSupremoChallengeUpdate(timeLeft, distance, status)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoChallengeUpdate error: " + str(e))

	def __HunterSupremoChallengeClose(self, args):
		"""Chiude UI sfida Supremo con risultato"""
		try:
			parts = args.split("|")
			result = parts[0] if len(parts) > 0 else "TIMEOUT"
			gloriaChange = parts[1] if len(parts) > 1 else "0"
			message = parts[2].replace("+", " ") if len(parts) > 2 else ""
			
			if self.interface:
				self.interface.HunterSupremoChallengeClose(result, gloriaChange, message)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoChallengeClose error: " + str(e))

	def __HunterSupremoVictory(self, args):
		"""Mostra effetto vittoria Supremo"""
		try:
			parts = args.split("|")
			supremoName = parts[0].replace("+", " ") if len(parts) > 0 else "Supremo"
			rank = parts[1] if len(parts) > 1 else "E"
			gloriaReward = parts[2] if len(parts) > 2 else "500"
			
			if self.interface:
				self.interface.HunterSupremoVictory(supremoName, rank, gloriaReward)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSupremoVictory error: " + str(e))

	# ============================================================
	# HANDLER NOTIFICHE E UTILITY MANCANTI
	# ============================================================

	def __HunterNotification(self, args):
		"""Mostra notifica popup (achievement, rank, system, event)"""
		try:
			parts = args.split("|")
			notifType = parts[0] if len(parts) > 0 else "system"
			message = parts[1].replace("+", " ") if len(parts) > 1 else ""
			if self.interface:
				self.interface.HunterNotification(notifType, message)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterNotification error: " + str(e))

	def __HunterFirstOfDay(self, args):
		"""Notifica bonus primo del giorno"""
		try:
			parts = args.split("|")
			activityType = parts[0] if len(parts) > 0 else "generic"
			bonusGlory = parts[1] if len(parts) > 1 else "0"
			bonusPercent = parts[2] if len(parts) > 2 else "0"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cff00FF00[FIRST OF DAY]|r Bonus " + activityType + ": +" + bonusGlory + " Gloria (+" + bonusPercent + "%)")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterFirstOfDay error: " + str(e))

	def __HunterEventWinner(self, args):
		"""Annuncio vincitore evento"""
		try:
			parts = args.split("|")
			winnerName = parts[0].replace("+", " ") if len(parts) > 0 else "???"
			gloryPrize = parts[1] if len(parts) > 1 else "0"
			eventName = parts[2].replace("+", " ") if len(parts) > 2 else "Evento"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFD700[EVENTO]|r " + winnerName + " ha vinto " + eventName + "! (+" + gloryPrize + " Gloria)")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterEventWinner error: " + str(e))

	def __HunterDefenseClose(self, args):
		"""Chiude UI difesa frattura"""
		try:
			import hunter_windows
			defenseWnd = hunter_windows.GetFractureDefenseWindow()
			if defenseWnd and defenseWnd.IsShow():
				defenseWnd.Close()
		except Exception as e:
			import dbg
			dbg.TraceError("HunterDefenseClose error: " + str(e))

	def __HunterResonatorReceived(self, args):
		"""Notifica gloria ricevuta via risonatore"""
		try:
			parts = args.split("|")
			glory = parts[0] if len(parts) > 0 else "0"
			sharePercent = parts[1] if len(parts) > 1 else "0"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cff00BFFF[RISONATORE]|r Hai ricevuto +" + glory + " Gloria (" + sharePercent + "% condivisione)")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterResonatorReceived error: " + str(e))

	def __HunterResonatorTriggered(self, args):
		"""Notifica risonatore attivato per il party"""
		try:
			parts = args.split("|")
			boostedGlory = parts[0] if len(parts) > 0 else "0"
			memberCount = parts[1] if len(parts) > 1 else "0"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cff00BFFF[RISONATORE]|r Gloria condivisa: " + boostedGlory + " tra " + memberCount + " membri")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterResonatorTriggered error: " + str(e))

	def __HunterPartyGloryDist(self, args):
		"""Notifica distribuzione gloria party"""
		try:
			parts = args.split("|")
			totalGlory = parts[0] if len(parts) > 0 else "0"
			memberCount = parts[1] if len(parts) > 1 else "0"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFD700[PARTY]|r Gloria distribuita: " + totalGlory + " tra " + memberCount + " membri")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterPartyGloryDist error: " + str(e))

	def __HunterPartyMeritGlory(self, args):
		"""Notifica gloria merito party"""
		try:
			parts = args.split("|")
			totalGlory = parts[0] if len(parts) > 0 else "0"
			memberCount = parts[1] if len(parts) > 1 else "0"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFD700[PARTY]|r Gloria per merito: " + totalGlory + " tra " + memberCount + " membri")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterPartyMeritGlory error: " + str(e))

	def __HunterFracturePing(self, args):
		"""Ping frattura sulla minimappa"""
		try:
			parts = args.split("|")
			x = int(parts[0]) if len(parts) > 0 else 0
			y = int(parts[1]) if len(parts) > 1 else 0
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFF6600[FRATTURA]|r Rilevata alle coordinate (" + str(x) + ", " + str(y) + ")")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterFracturePing error: " + str(e))

	def __HunterSealEffect(self, args):
		"""Effetto visivo sigillo frattura"""
		try:
			fcolor = args.replace("+", " ") if args else "PURPLE"
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffAA00FF[SIGILLO]|r Frattura sigillata!")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterSealEffect error: " + str(e))

	def __HunterChaosPossible(self, args):
		"""Indicatore Frattura Corrotta possibile. Formato: HighestRank|FractureRank (es. A|E)"""
		try:
			parts = args.split("|")
			if len(parts) >= 2:
				highestRank = parts[0]
				fractureRank = parts[1]
				if self.interface:
					try:
						self.interface.SetChaosPossible(highestRank, fractureRank)
					except:
						pass
		except Exception as e:
			import dbg
			dbg.TraceError("HunterChaosPossible error: " + str(e))

	def __HunterMentorActive(self, args):
		"""Notifica: Mentore (B+ rank) presente. Formato: HighestRank (es. A)"""
		pass  # Notifica gia' gestita via syschat server-side

	def __HunterChaosFracture(self, args):
		"""Frattura Corrotta rilevata. Formato: FractureRank|ChaosRank|ChaosTier"""
		pass  # Effetto visivo futuro; messaggi chaos gia' via syschat

	def __HunterChaosFractureComplete(self, args):
		"""Frattura Corrotta completata. Formato: ChaosRank"""
		pass  # Notifica gia' gestita via syschat server-side

	def __HunterGloryDetail(self, rawArgs):
		"""Riceve il dettaglio Gloria dal server e lo mostra nella UI pannello.
		   Formato: CONTEXT|TYPE|NAME|BASE|mod1;val1;add1~mod2;val2;add2~...|FINAL
		   Esempio: KILLER|BOSS|Nemere|500|Primo+del+Giorno!;+50%;+250~Bonus+Serie;+7%;+52|3208
		   NOTA: Solo i nomi hanno spazi codificati come +. I valori (es. +50%) contengono + letterali.
		"""
		import dbg
		dbg.TraceError("[GLORY_DETAIL] Received rawArgs: " + str(rawArgs))
		try:
			parts = rawArgs.split("|")
			if len(parts) < 6:
				dbg.TraceError("[GLORY_DETAIL] ERROR: parts < 6, got " + str(len(parts)))
				return
			context    = parts[0].strip()
			sourceType = parts[1].strip()
			sourceName = parts[2].strip().replace("+", " ")  # Solo nome: + = spazio
			baseGlory  = int(parts[3].strip())
			modsRaw    = parts[4].strip()
			finalGlory = int(parts[5].strip())

			modifiers = []
			if modsRaw and modsRaw != "NONE":
				for token in modsRaw.split("~"):
					sub = token.split(";")
					if len(sub) >= 3:
						modName = sub[0].replace("+", " ")  # Nome mod: + = spazio
						modVal  = sub[1]                     # Valore: +50% resta intatto
						modAdd  = int(sub[2])
						modifiers.append((modName, modVal, modAdd))
					elif len(sub) == 2:
						modifiers.append((sub[0].replace("+", " "), sub[1], 0))

			dbg.TraceError("[GLORY_DETAIL] Parsed: ctx=" + context + " type=" + sourceType + " name=" + sourceName + " base=" + str(baseGlory) + " mods=" + str(len(modifiers)) + " final=" + str(finalGlory))
			dbg.TraceError("[GLORY_DETAIL] interface=" + str(self.interface is not None))

			if self.interface:
				self.interface.HunterGloryDetail(context, sourceType, sourceName, baseGlory, modifiers, finalGlory)
				dbg.TraceError("[GLORY_DETAIL] Called interface.HunterGloryDetail OK")
		except Exception as e:
			import dbg
			dbg.TraceError("HunterGloryDetail error: " + str(e))

	def __AutoHuntLicense(self, args):
		"""Server risponde: AUTOHUNT_LICENSE OK / FAIL ALREADY_ACTIVE / RELEASED"""
		try:
			import autohunt
			if autohunt.wndAttack:
				autohunt.wndAttack.OnServerLicenseResponse(args)
		except:
			pass

	def __AutoHuntOccupied(self, vid_str):
		try:
			vid = int(vid_str)
			import autohunt
			if autohunt.wndAttack:
				autohunt.wndAttack.OnOccupied(vid)
		except:
			pass

	def __AutoHuntDungeon(self, args):
		"""Server risponde: AUTOHUNT_DUNGEON OK/FAIL [reason]"""
		try:
			import autohunt
			if autohunt.wndAttack:
				autohunt.wndAttack.OnServerDungeonResponse(args)
		except:
			pass
