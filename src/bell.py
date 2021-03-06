import pygame

import os
import sys

class Bell:
    def __init__(self, bellNumber, location, bellImageFile, width, height, textLocation, font, key=None, backgroundColour=(255, 255, 255)):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        self.font = font
        self.stroke = 'H'

        # Read in bell image and create handstroke and backstroke images from it
        self.width = width
        self.height = height
        self.backgroundColour = backgroundColour
        bell = pygame.image.load(bellImageFile)
        self.handstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.handstrokeBellBlank = self.handstrokeBell.copy()
        self.handstrokeBellBlank.fill(self.backgroundColour)
        self.backstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.backstrokeBell = pygame.transform.rotate(self.backstrokeBell, -90.0)
        self.backstrokeBell = pygame.transform.flip(self.backstrokeBell, True, False)
        self.backstrokeBellBlank = self.backstrokeBell.copy()
        self.backstrokeBellBlank.fill(self.backgroundColour)


        self.x = location[0]
        self.y = location[1]

        self.textX = textLocation[0]
        self.textY = textLocation[1]

        self.bellNumber = bellNumber
        self.bellNumberText = self.font.FONT.render(str(self.bellNumber), True, (0, 0, 0))
        self.bellNumberTextBlank = pygame.Rect(self.textX, self.textY, self.bellNumberText.get_width(), self.bellNumberText.get_height())

        self.key = key

    def fill(self, surface, colour):
        surface.fill(colour)

    def setKey(self, key):
        self.key = key

    def clearKey(self):
        self.key = None

    def updateLocation(self, x, y, textX, textY):
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY

        self.bellNumberTextBlank = pygame.Rect(self.textX, self.textY, self.bellNumberText.get_width(), self.bellNumberText.get_height())

    def draw(self, win, renderNumber=True):
        if self.stroke == 'H':
            win.blit(self.backstrokeBellBlank, (self.x, self.y))
            win.blit(self.handstrokeBell, (self.x, self.y))
        else:
            win.blit(self.handstrokeBellBlank, (self.x, self.y))
            win.blit(self.backstrokeBell, (self.x, self.y))
        if renderNumber:
            pygame.draw.rect(win, self.backgroundColour, self.bellNumberTextBlank, 0)
            win.blit(self.bellNumberText, (self.textX, self.textY))

    def handle_event(self, send):
        send("R:" + self.stroke + str(self.bellNumber))

    def bellRung(self, stroke):
        # Change the bell stroke 
        self.stroke = 'B' if stroke == 'H' else 'H'
        