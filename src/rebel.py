"""
ReBel
author: Samuel M Senior
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import sys

import numpy as np

from log import Log

from client import Network

from font import Font
from titledInputBox import TitledInputBox
from button import Button
from config import Config

from helpScreen import HelpScreen
from menuScreen import MenuScreen
from optionsScreen import OptionsScreen
from ringingScreen import RingingScreen

        
class Rebel(Font, Log):
    def __init__(self, menuWidth, menuHeight, mainWidth, mainHeight, configFile=os.path.join("..", "config", "config.txt")):

        # initialize
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=1)
        pygame.mixer.init()
        pygame.font.init()

        Font.__init__(self)

        self.logFile = os.path.join("..", "log", "log.txt")
        Log.__init__(self, logFile=self.logFile)
        self.clearLog()

        self.reBelClientVersion = "v0.2.15"
        self.log("[INFO] Running ReBel client {}".format(self.reBelClientVersion))

        self.menuWidth = menuWidth
        self.menuHeight = menuHeight

        self.mainWidth = mainWidth
        self.mainHeight = mainHeight

        self.configFile = configFile

        self.win = pygame.display.set_mode((self.menuWidth, self.menuHeight))
        pygame.display.set_caption("ReBel")

        self.config = Config(fileName=self.configFile)

        self.frameRate = self.config.get('frameRate')
        self.log("[INFO] FrameRate set to {}".format(self.frameRate))

        self.network = Network(self.logFile, frameRate=self.frameRate)
        self.helpScreen = HelpScreen(self.win, frameRate=self.frameRate)
        self.menuScreen = MenuScreen(win=self.win, network=self.network, frameRate=self.frameRate,
                                     logFile=self.logFile, config=self.config)
        self.optionsScreen = OptionsScreen(win=self.win, config=self.config, frameRate=self.frameRate)
        self.ringingScreen = RingingScreen(network=self.network, width=self.mainWidth, height=self.mainHeight, frameRate=self.frameRate,
                                           logFile=self.logFile, config=self.config)

        self.screen = 'menuScreen'

    def quit(self):
        self.running = False
        if self.network.connected == True:
            self.network.send("clientDisconnect:Disconnecting")
        self.log("[INFO] Quitting...")
        pygame.quit()
        sys.exit(0)

    def updateScreenSize(self, width, height):
        self.win = pygame.display.set_mode((width, height))

    def run(self):
        self.running = True
        while self.running:
            if self.screen == 'menuScreen':
                self.ringingScreen.initialised = False
                self.updateScreenSize(self.menuWidth, self.menuHeight)
                self.previousScreen = 'menuScreen'
                self.screen = self.menuScreen.display()
                if self.screen == 'quit':
                    self.quit()
            elif self.screen == 'helpScreen':
                self.screen = self.helpScreen.display(win=self.win, source=self.previousScreen)
                if self.screen == 'quit':
                    self.quit()
            elif self.screen == 'optionsScreen':
                self.screen = self.optionsScreen.display(win=self.win, source=self.previousScreen)
                if self.screen == 'quit':
                    self.quit()
                elif self.optionsScreen.bellKeysUpdated:
                    self.ringingScreen.updateBellKeys()
                    self.optionsScreen.bellKeysUpdated = False
            elif self.screen == 'ringingScreen':
                self.updateScreenSize(self.mainWidth, self.mainHeight)
                self.previousScreen = 'ringingScreen'
                self.screen = self.ringingScreen.display()
                if self.screen == 'quit':
                    self.quit()
            else:
                self.quit()
   

if __name__ == "__main__":
    rebel = Rebel(750, 700, 1000, 700)
    rebel.run()
