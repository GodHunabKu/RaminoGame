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
import autohunt
if autohunt.Attack is not None:
	autohunt.Attack()

import stringCommander
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
import uihunterlevel
import uihunterlevel_gate_trial

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
		self.interface = interfaceModule.Interface()
		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(self.interface)
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()
		constInfo.SetInterfaceInstance(self.interface)

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()

		if app.ENABLE_SKILL_SELECT_FEATURE:
			self.skillSelect = uiselectskill.SkillSelectWindow()
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

		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			if self.wndMount:
				self.wndMount.Hide()

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None
			

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(None)
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
		onPressKeyDict[app.DIK_F5]	= lambda : self.interface.wndBlend.btnUse()
		onPressKeyDict[app.DIK_F6]	= lambda : self.interface.ToggleMarmurShopWindow()
		# onPressKeyDict[app.DIK_F5]	= lambda : self.interface.ToggleSwitchbotWindow()
		#onPressKeyDict[app.DIK_F7]	= lambda : self.interface.OpenLocationWindow() ## MODIFICA: Rimosso conflitto F7
		onPressKeyDict[app.DIK_F8]	= lambda : self.interface.OpenRespWindow()
		onPressKeyDict[app.DIK_F9]	= lambda : self.interface.BuffNPCOpenWindow()

		onPressKeyDict[app.DIK_RETURN]	= lambda : self.ChangeBonus()

		onPressKeyDict[app.DIK_F11]	= lambda : self.interface.ToggleCollectWindow()

		onPressKeyDict[app.DIK_F12] = lambda : self.interface.ToggleCollectionWindow()
		# onPressKeyDict[app.DIK_F12] = lambda : self.interface.OpenEventCalendar()

		if app.ENABLE_NEW_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]	= lambda : self.interface.pet_window_open()
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
		onPressKeyDict[app.DIK_Y]			= self.__PressYKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindow()
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			onPressKeyDict[app.DIK_U]			= lambda : self.interface.TogglePrivateShopPanelWindowCheck()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()
		onPressKeyDict[app.DIK_TAB]			= lambda : self.interface.ToggleMapaSwWindow()

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
		if constInfo.IS_BONUS_CHANGER:
			self.interface.wndChangerWindow.ChangeBonus()
		elif constInfo.IS_ACCE_WINDOW:
			acce.SendRefineRequest()
		elif constInfo.IS_DRAGON_SOUL_OPEN:
			self.interface.wndDragonSoulRefine.PressDoRefineButton()

	def WyszukiwaraOpen(self):
		self.wndShopSearchWindow.OpenWindow()

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
		"""Gestione tasto Y: Apre il Sistema Hunter"""
		if not (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)):
			uihunterlevel.ToggleHunterLevelWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
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
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
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
			self.wndKeyChange.Open()

		def OpenWindow(self, type, state):
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
				self.interface.wndBlend.btnUse()
			elif type == player.KEY_OPEN_MARBLE:
				self.interface.ToggleMarmurShopWindow()
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
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

		self.CheckGameButton()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		else:
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
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()

	if app.ENABLE_AFFECT_FIX:
		def RefreshAffectWindow(self):
			self.affectShower.BINARY_NEW_RefreshAffect()


	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHPTargetBoard(self, vid, iMinHP, iMaxHP):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			
			self.targetBoard.SetHP(iMinHP, iMaxHP)
			self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		# if self.mapNameShower:
		# 	self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME
    
	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chat.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	# def OnPickMoney(self, money):
	# 	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	# 		chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
	# 	else:
	# 		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))
	def OnPickMoney(self, money):
		self.interface.OnPickMoneyNew(money)

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
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
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## OfflineShop
	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def StartOfflineShop(self, vid):
			self.interface.OpenOfflineShopDialog(vid)
			
		def EndOfflineShop(self):
			self.interface.CloseOfflineShopDialog()
			
		def RefreshOfflineShop(self):
			self.interface.RefreshOfflineShopDialog()
        
	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
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
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
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
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
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
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
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
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
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

		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		### INIZIO CODICE AGGIUNTO E MODIFICATO ###
		if key == app.DIK_F7:
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
				if self.wndKeyChange.IsOpen() == 1:
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
		if self.interface.BUILD_OnMouseLeftButtonDown():
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

		if self.interface.BUILD_OnMouseLeftButtonUp():
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
				else:
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

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		# if self.mapNameShower.IsShow():
		# 	self.mapNameShower.Update()

		if app.IsPressed(app.DIK_Z):
			player.PickCloseItem()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()
			
		self.interface.BUILD_OnUpdate()

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

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
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
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################
	
	# EXCHANGE
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)
	# END_OF_EXCHANGE

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
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
		self.interface.ShowGift()


	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

		self.interface.OpenCubeWindow()


		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

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
		self.interface.CloseCubeWindow()

	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
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
		self.interface.AppendQueue(vnum, value)

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
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
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1



				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()


		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0


	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# @fixme003 (+if self.interface:)
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_ShowIcon(self):
		self.interface.CardsShowIcon()
		
	def BINARY_Cards_Open(self, safemode):
		self.interface.OpenCardsWindow(safemode)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
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
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
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
		serverCommandList["HunterAchievements"]  = self.__HunterAchievements
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

		# Chest/Baule System
		serverCommandList["HunterChestOpening"]  = self.__HunterChestOpening
		serverCommandList["HunterChestOpened"]   = self.__HunterChestOpened
		serverCommandList["HunterChestItem"]     = self.__HunterChestItem
		serverCommandList["HunterPartyChest"]    = self.__HunterPartyChest

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
		})
		
		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)


	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetBodyCostumeHidden(self, hidden):
			constInfo.HIDDEN_BODY_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetHairCostumeHidden(self, hidden):
			constInfo.HIDDEN_HAIR_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetAcceCostumeHidden(self, hidden):
			constInfo.HIDDEN_ACCE_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()
				
		def SetStoleCostumeHidden(self, hidden):
			constInfo.HIDDEN_STOLE_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetWeaponCostumeHidden(self, hidden):
			constInfo.HIDDEN_WEAPON_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetAuraCostumeHidden(self, hidden):
			constInfo.HIDDEN_AURA_COSTUME = int(hidden)
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
			self.interface.OnPickPktOsiagNew(pkt_osiag)
			# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PKT_OSIAG_SYSTEM_PICK_PKT_OSIAG % (pkt_osiag))

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
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
			self.interface.OpenOdlamkiWindow()

		def BINARY_OdlamkiItemRefreshWindow(self):
			self.interface.wndOdlamki.ClearWindow()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def __SetBuffNPCSummon(self):
			self.interface.BuffNPC_Summon()
			
		def __SetBuffNPCUnsummon(self):
			self.interface.BuffNPC_Unsummon()
			
		def __SetBuffNPCClear(self):
			self.interface.BuffNPC_Clear()

		def __SetBuffNPCBasicInfo(self, name, sex, intvalue):
			self.interface.BuffNPC_SetBasicInfo(str(name), int(sex), int(intvalue))

		def __SetBuffNPCSkillInfo(self, skill1, skill2, skill3):
			self.interface.BuffNPC_SetSkillInfo(skill1, skill2, skill3)
			
		def __SetBuffNPCSkillSetSkillCooltime(self, slot, timevalue):
			self.interface.BuffNPC_SetSkillCooltime(slot, timevalue)
			
		def __SetBuffNPCCreatePopup(self, type, value0, value1):
			self.interface.BuffNPC_CreatePopup(int(type), int(value0), int(value1))
			
		def BINARY_OpenCreateBuffWindow(self):
			self.interface.BuffNPC_OpenCreateWindow()

	def RefineSuceededMessage(self):
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(True)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
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
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	## PrivateShop
	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	## OfflineShop
	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def __OfflineShop_Open(self):
			self.interface.OpenOfflineShopBuilder()
		
		def BINARY_OfflineShop_Appear(self, vid, text):	
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				self.interface.AppearOfflineShop(vid, text)
			
		def BINARY_OfflineShop_Disappear(self, vid):	
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				self.interface.DisappearOfflineShop(vid)	
				
		def OpenOfflineShopPanel(self, info):
			self.interface.ToggleOfflineShopAdminPanelWindow(info)

		def OpenOfflineShopLogs(self):
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
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
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
			self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
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
		if self.interface.wndMessenger:
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
		self.interface.wndRemoveItem.ClearWindow()

	if app.ENABLE_RESP_SYSTEM:
		def BINARY_SetMobRespData(self, mobVnum, data):
			self.interface.wndResp.SetMobRespData(mobVnum, data)

		def BINARY_SetMobDropData(self, mobVnum, data):
			self.interface.wndResp.SetMobDropData(mobVnum, data)

		def BINARY_SetMapData(self, data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount):
			self.interface.wndResp.SetMapData(data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount)

		def BINARY_RefreshResp(self, id, mobVnum, time, cord):
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
		self.interface.wndItemShop.Open(dataTime)

	def BINARY_ItemShopSetEditorFlag(self, flag):
		self.interface.wndItemShop.SetEditorFlag(flag)

	def BINARY_ItemShopRefresh(self):
		self.interface.wndItemShop.RefreshPage()

	def BINARY_ItemShopUpdateCoins(self):
		self.interface.wndItemShop.UpdateCoins()

	def BINARY_ItemShopShowPopup(self, type, id, category):
		self.interface.wndItemShop.ShowPopup(type, id, category)

	def BINARY_TombolaStart(self, pos, to_pos, to_spin, time):
		self.interface.TombolaStart(pos, to_pos, to_spin, time)

	def BINARY_TombolaSpinningItem(self, pos, vnum, count):
		self.interface.TombolaSetSpinningItem(pos, vnum, count)

	def BINARY_TombolaOpen(self):
		self.interface.TombolaOpen()

	def BINARY_TombolaSetPrice(self, group, price, price_type):
		self.interface.TombolaSetPrice(group, price, price_type)

	def BINARY_TombolaSetItem(self, group, vnum, count, chance):
		self.interface.TombolaSetItem(group, vnum, count, chance)

	def BINARY_TombolaClear(self):
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
			self.targetBoard.DropInfoRefresh(mob_vnum)

		def DropInfoRefresh(self):
			constInfo.dropInfoDict = {}
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
			self.interface.ClearLocationWindow()
			
		def BINARY_ReceiveLocationPos(self, position, index, posx, posy):
			self.interface.UpdateLocationWindowPos(position, index, posx, posy)

		def BINARY_ReceiveLocationName(self, name):
			self.interface.UpdateLocationWindowName(name)

	def __OpenItemShop(self):
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
			self.interface.RefreshServerInfo(channelNumber)
			
	def _mapa(self, id):
		constInfo.id_quest_mapa = int(id)
	
	def GetInputOn(self):
		constInfo.INPUT_IGNORE = 1
		
	def GetInputOff(self):
		constInfo.INPUT_IGNORE = 0

	if app.ENABLE_NEW_PET_SYSTEM:	
		def __pet_info(self, arg):
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
				
			self.interface.pet_refresh()

		def __pet_info_update(self, arg):
			try:
				constInfo.gui_pets["ID"] = int(arg)
			except:
				pass

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			self.interface.RefreshSwitchbotWindow()
			
		def RefreshSwitchbotItem(self, slot):
			self.interface.RefreshSwitchbotItem(slot)

	def PotionsbalcudiaF(self):
		#self.wndItemShop.RequestOpen()
		self.interface.wndBlend.OpenWindow()
		#self.interface.ToggleDungeonInfoWindow()
		
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

		def BINARY_SetMiniMapDungeonInfoTimer(self, status, time):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoTimer(status, time)

	if app.ENABLE_COLLECT_WINDOW:
		def BINARY_UpdateCollectWindow(self, windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.AddData(windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel)
				
		def UpdateTime(self, val, time):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendTime(val, time)

		def UpdateChance(self, val, chance):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendChance(val, chance)

		def __SetCollectWindowQID(self, window, value):
			constInfo.CollectWindowQID[int(window)] = int(value)
			# self.interface.ToggleQuest(str(value))

		def OpenCollectWindow(self):
			self.interface.ToggleCollectWindow()
		
	if constInfo.GIFT_CODE_SYSTEM:
		def __OpenCodeWindow(self):
			self.interface.OpenGiftCodeWindow()

	if app.ENABLE_LRN_BATTLE_PASS:
		def SERVER_BattlePassClearQuest(self):
			self.interface.ClearBattlePassQuest()

		def SERVER_BattlePassClearReward(self):
			self.interface.ClearBattlePassReward()

		def SERVER_BattlePassLevel(self, info):
			info = info.split("#")
			self.interface.AppendBattlePassLevel(int(info[0]), int(info[1]), int(info[2]))

		def BINARY_BattlePassQuest(self, index, group, count, exp):
			self.interface.AppendBattlePassQuest(index, group, count, exp)

		def BINARY_BattlePassQuestData(self, index, count, status):
			self.interface.AppendBattlePassQuestData(index, count, status)

		def BINARY_BattlePassReward(self, level, item_free, count_free, item_premium, count_premium):
			self.interface.AppendBattlePassReward(level, item_free, count_free, item_premium, count_premium)

		def BINARY_BattlePassRewardData(self, level, status_free, status_premium):
			self.interface.AppendBattlePassRewardData(level, status_free, status_premium)

	if app.ENABLE_EVENT_MANAGER:
		def ClearEventManager(self):
			self.interface.ClearEventManager()
		def RefreshEventManager(self):
			self.interface.RefreshEventManager()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
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
			if self.interface.wndMessenger:
				self.interface.wndMessenger.OnLogin(2, name)

		def __Team_Off(self, name):
			if self.interface.wndMessenger:
				self.interface.wndMessenger.OnLogout(2, name)

	def UpdateBotControlItems(self, data):
		vv = data.split('|')
		vv.pop()
		itemArr = [int(i) for i in vv]
		if self.interface:
			self.interface.wndBotControl.UpdateItems(itemArr)
			self.interface.OpenBotControl()

	def UpdateBotControlRealName(self, name):
		if self.interface:
			chat.AppendChat(1, "{}".format(name))
			self.interface.wndBotControl.SetRealItemName(str(name))

	def UpdateBotControlRof(self, rof):
		if self.interface:
			self.interface.wndBotControl.SetROF(int(rof))

	def CloseBotControl(self):
		if self.interface:
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
				}
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd: wnd.SetPlayerData(data)
		except:
			pass

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
							rankList.append({
								"name": parts[0],
								"points": int(parts[1]),
								"value": int(parts[1]),
								"kills": int(parts[2])
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetRankingData(rankType, rankList)
		except:
			pass

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
							rankList.append({
								"name": parts[0],
								"value": int(parts[1]),
								"points": int(parts[2])
							})
						elif len(parts) == 2:
							rankList.append({
								"name": parts[0],
								"value": int(parts[1]),
								"points": int(parts[1])
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetRankingData(rankType, rankList)
		except:
			pass

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
		except:
			pass

	def __HunterAchievements(self, dataStr):
		try:
			achList = []
			if dataStr and dataStr != "EMPTY":
				entries = dataStr.split(";")
				for entry in entries:
					if entry:
						parts = entry.split(",")
						if len(parts) >= 7:
							achList.append({
								"id": int(parts[0]),
								"name": parts[1].replace("+", " "),
								"type": int(parts[2]),
								"requirement": int(parts[3]),
								"progress": int(parts[4]),
								"unlocked": int(parts[5]) == 1,
								"claimed": int(parts[6]) == 1
							})
			wnd = uihunterlevel.GetHunterLevelWindow()
			if wnd: wnd.SetAchievements(achList)
		except:
			pass

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
		except:
			pass

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
		except:
			pass

	def __HunterTimers(self, dataStr):
		try:
			parts = dataStr.split("|")
			if len(parts) >= 2:
				wnd = uihunterlevel.GetHunterLevelWindow()
				if wnd: wnd.SetTimers(parts[0], parts[1])
		except:
			pass

	def __HunterOpenWindow(self):
		uihunterlevel.OpenHunterLevelWindow()

	def __HunterMessage(self, msgStr):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msgStr.replace("+", " "))

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
		except:
			pass

# ==============================================================================
	# HUNTER SYSTEM: AWAKENING HANDLERS (New Features v36)
	# ==============================================================================

	def __HunterSystemSpeak(self, msg):
		"""Il Sistema parla (Messaggio colorato in base al rank)"""
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
		except:
			pass

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
		except:
			pass

	def __HunterEmergencyUpdate(self, count):
		"""Aggiorna contatore Emergency Quest"""
		if self.interface:
			self.interface.HunterEmergencyUpdate(int(count))

	def __HunterEmergencyClose(self, status):
		"""Chiude Emergency Quest (SUCCESS o FAIL)"""
		if self.interface:
			self.interface.HunterEmergencyClose(str(status))

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
		except:
			pass

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
		except:
			pass

	def __HunterBossAlert(self, bossName):
		"""Mostra ALERT a schermo intero quando spawna un BOSS"""
		try:
			if self.interface:
				self.interface.HunterBossAlert(bossName)
		except:
			pass

	def __HunterSystemInit(self):
		"""Mostra effetto inizializzazione sistema al login"""
		try:
			if self.interface:
				self.interface.HunterSystemInit()
		except:
			pass

	def __HunterActivation(self, playerName):
		"""Mostra effetto attivazione Hunter al Lv 30"""
		try:
			if self.interface:
				self.interface.HunterActivation(playerName.replace("+", " "))
		except:
			pass

	def __HunterOvertake(self, data):
		"""Mostra effetto sorpasso in classifica"""
		try:
			parts = data.split("|")
			if len(parts) >= 2:
				overtakenName = parts[0].replace("+", " ")
				newPosition = int(parts[1])
				if self.interface:
					self.interface.HunterOvertake(overtakenName, newPosition)
		except:
			pass

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
		except:
			pass

	def __HunterEventStatus(self, data):
		"""Mostra finestra stato evento"""
		try:
			parts = data.split("|")
			if len(parts) >= 2:
				eventName = parts[0].replace("+", " ")
				duration = int(parts[1])
				eventType = "default"
				desc = ""
				reward = ""
				if len(parts) >= 3:
					eventType = parts[2]
				if len(parts) >= 4:
					desc = parts[3].replace("+", " ")
				if len(parts) >= 5:
					reward = parts[4].replace("+", " ")
				if self.interface:
					self.interface.HunterEventStatus(eventName, duration, eventType, desc, reward)
		except:
			pass

	def __HunterEventClose(self):
		"""Chiude la finestra stato evento"""
		try:
			if self.interface:
				self.interface.HunterEventClose()
		except:
			pass

	# ====================================================================================
	# DAILY MISSIONS & EVENTS HANDLERS
	# ====================================================================================
	
	def __HunterMissionsCount(self, data):
		"""Riceve il numero di missioni giornaliere"""
		try:
			count = int(data)
			if self.interface:
				self.interface.HunterMissionsCount(count)
		except:
			pass
	
	def __HunterMissionData(self, data):
		"""Riceve dati di una missione: id|name|type|progress|target|reward|penalty|status"""
		try:
			parts = data.split("|")
			if len(parts) >= 8:
				# Formato: id|name|type|current|target|reward|penalty|status
				missionData = "%d|%s|%s|%d|%d|%d|%d|%s" % (
					int(parts[0]),
					parts[1].replace("+", " "),
					parts[2],
					int(parts[3]),
					int(parts[4]),
					int(parts[5]),
					int(parts[6]),
					parts[7]
				)
				if self.interface:
					self.interface.HunterMissionData(missionData)
		except:
			pass
	
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
		except:
			pass
	
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
		except:
			pass
	
	def __HunterAllMissionsComplete(self, data):
		"""Tutte le missioni complete - bonus x1.5 + bonus fratture attivato"""
		try:
			parts = data.split("|")
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
		except:
			pass
	
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

	# ============================================================
	def __HunterEventsCount(self, data):
		"""Riceve numero eventi"""
		try:
			count = int(data)
			if self.interface:
				self.interface.HunterEventsCount(count)
		except:
			pass
	
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
		except:
			pass
	
	def __HunterEventBatch(self, data):
		"""Riceve batch di eventi: event1;event2;event3... dove ogni evento e' id~name~start~end~type~reward~status~min_rank~winner_prize"""
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
						"winner_prize": int(parts[8]) if len(parts) > 8 else 200
					}
					if self.interface:
						self.interface.HunterEventData(eventData)
		except:
			pass
	
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
		except:
			pass
	
	def __HunterEventsOpen(self):
		"""Apre pannello eventi"""
		try:
			if self.interface:
				self.interface.HunterEventsOpen()
		except:
			pass

	def __HunterNewDay(self):
		"""E' passata la mezzanotte - resetta cache eventi e aggiorna UI"""
		try:
			if self.interface:
				self.interface.HunterNewDay()
		except:
			pass

	# ============================================================
	# HUNTER SYSTEM - FRACTURE DEFENSE SYSTEM
	# ============================================================

	def __HunterFractureDefenseStart(self, args):
		"""Inizia difesa frattura: fracture_name|duration|rank|totalMobs"""
		try:
			parts = args.split("|")
			if len(parts) >= 4:
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

	def __HunterSpeedKillEnd(self, success):
		"""Termina speed kill: 1=successo, 0=fallito"""
		try:
			isSuccess = int(success)
			if self.interface:
				self.interface.HunterSpeedKillEnd(isSuccess)
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
		        chest_cur|chest_req|daily_cur|daily_req
		Esempio: 2|Prova+del+Cacciatore|C|BLUE|259200|3|5|7|10|2|5|3|5|10|15
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
				
				if self.interface:
					self.interface.HunterTrialStatus(
						trialId, trialName, toRank, colorCode, remainingSeconds,
						bossKills, bossReq, metinKills, metinReq,
						fractureSeals, fractureReq, chestOpens, chestReq,
						dailyMissions, dailyReq
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
						a, b = s.split("/")
						return int(a), int(b)
					return 0, 0
				
				bossKills, bossReq = parseProg(parts[1])
				metinKills, metinReq = parseProg(parts[2])
				fractureSeals, fractureReq = parseProg(parts[3])
				chestOpens, chestReq = parseProg(parts[4])
				dailyMissions, dailyReq = parseProg(parts[5])
				
				if self.interface:
					self.interface.HunterTrialProgress(
						trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions
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
		"""Effetto risveglio livello - usa nuovo sistema hunter_effects"""
		try:
			# args e' un numero (livello)
			level = 5  # default
			try:
				level = int(args)
			except:
				level = 5
			
			import hunter_effects
			hunter_effects.ShowAwakening(level)
		except Exception as e:
			import dbg
			dbg.TraceError("HunterAwakening error: " + str(e))
