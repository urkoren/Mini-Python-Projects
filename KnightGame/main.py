import collections
import tkinter as tk
import pyautogui as pt
from time import sleep
from random import randrange, SystemRandom
from secrets import randbelow
from pyscreeze import Box, Point

Logo = collections.namedtuple('Logo', 'path minConfidence')

LOGOS = {
    'battle'                    : Logo('images/battle.png', 0.85),
    'alliance'                  : Logo('images/alliance_.png', 0.85),
    # 'allianceTabTitle'          : Logo('images/allianceTabTitle.png', 0.), #TODO: missing - add this logo to images
    'questMainButton'           : Logo('images/questButton.png', 0.85),
    'questTabTitle'             : Logo('images/questButton.png', 0.85),
    'inventoryMainButton'       : Logo('images/inventoryButton.png', 0.85),
    'dontJoin'                  : Logo('images/dontjoinatall.png', 0.7), # Keep on low confidence - better safe than sorry
    # 'marchFlag'         : Logo('images/MarchFlag.png', 0.),
    'noneJoined'                : Logo('images/nonjoined.png', 0.9),
    # 'rallying'          : Logo('images/rallying.png', 0.),
    # 'joinRallyGray'     : Logo('images/JoinedSpartois.png', 0.),
    'marchButton'               : Logo('images/marchButton.png', 0.85),
    'goBackArrow'               : Logo('images/goBackArrow.png', 0.85),
    'joinRallyBlue'             : Logo('images/ReadySpartois.png', 0.9),
    'rallyTabTitle'             : Logo('images/rallyTabTitle.png', 0.85),
    'peacefulState'             : Logo('images/none.png', 0.9),
    'rallyTabButton2Blue'       : Logo('images/rallyTabButton2Blue.png', 0.9)
}

class Clicker:
    def __init__(self, target_png, speed):
        self.target_png = target_png
        self.speed = speed
        pt.FAILSAFE = True

    
    #########################################################################################################################
    #                               Begining of new/improved/modified Functions Section                                     #
    #########################################################################################################################

    # ------------------
    # Boolean Functions:
    # ------------------

    # Returns True when the go back arrow button is visible on screen, otherwise, returns False
    def isGoBackArrowVisible(self) -> bool:
        return bool(self.locateLogoOnScreen(LOGOS['goBackArrow']) != None)

    # Returns True if the main screen is currently Open, otherwise, returns False
    def isMainScreenVisible(self) -> bool:
        return (not self.isGoBackArrowVisible())
    
    # Returns True if the Alliance Tab is currently visible, otherwise, returns False
    def isAllianceTabVisible(self) -> bool:
        #TODO: Implement - tab logo is missing, need to add it to images
        # return bool(
            # self.isGoBackArrowVisible() and
            # self.locateLogoOnScreen([LOGOS['allianceTabTitle']]) != None
        # )
        pass
    
    # Returns True if the Quest tab is currently visible, otherwise, returns False
    def isQuestTabVisible(self) -> bool:
        return bool(
            self.isGoBackArrowVisible() and 
            self.locateLogoOnScreen(LOGOS['questTabTitle']) != None
        )

    # Returns True if the inventory tab is currently visible, otherwise, returns False
    def isInventoryTabVisible(self) -> bool:
        # TODO: Implement - inventory tab title image is missing - add to images
        # return bool(
        #     self.isGoBackArrowVisible() and
        #     self.locateLogoOnScreen(LOGOS['inventoryTabTitle']) != None
        # )
        pass
    
    # Returns True if the rally tab is currently open, otherwise, returns False
    def isRallyTabVisible(self) -> bool:
        return bool(
            self.isGoBackArrowVisible() and
            self.locateLogoOnScreen(LOGOS['rallyTabTitle']) != None
        )

    # Returns true when the "We are in peaceful state" text image is found on screen.
    # When the text is found - it means that there is no rally.
    def isAllianceInPeacefulState(self) -> bool:
        return bool(self.locateLogoOnScreen(LOGOS['peacefulState']) != None)
    
    # Returns True if it is safe to join. Otherwise, returns False
    def isItSafeToClick(self) -> bool:
        return bool(self.locateLogoOnScreen(LOGOS['dontJoin']) == None)

    # Returns True if the specified rally button is currently clicked, or False otherwise
    # when ~checkIfRallyTabVisible~ is set to True, the function also checks if the rally
    # tab is currently visible.
    def isRallyTabButtonClicked(self, buttonNumber: int, checkIfRallyTabVisible: bool = True) -> bool:
        return bool(
            buttonNumber == 2 and 
            ( checkIfRallyTabVisible == False or self.isRallyTabVisible() ) and 
            self.locateLogoOnScreen(LOGOS['rallyTabButton2Blue']) != None
        )

    
    # --------------
    # Get Functions:
    # --------------

    # Returns a random float duration between 0.1 to 2.09 with a maximum percision of 2 ( [0-2].XX )
    def getRandDuration(self) -> float:
        return float(randbelow(2) + round(SystemRandom.uniform(0.1, 1.1), 2))

    # Returns a random coordinates point whithin the specified box argument
    def getRandCoords(self, box: Box) -> Point:
        return Point(
            (box.left + randbelow(box.width)),
            (box.top + randbelow(box.height)) 
        )


    # ------------------
    # Utility Functions:
    # ------------------
    
    # Tries to locate ~logo~ on screen.
    # If the logo is not found - returns None.
    # If the logo is found and returnRandCoords is set to False, returns the logo's box on screen.
    # Otherwise, if it is set to True, returns a random ~Point~ whithin the logo's box.
    def locateLogoOnScreen(self, logo: Logo, returnRandCoords: bool = True) -> (Box | Point | None):
        logoBox = pt.locateOnScreen(image = logo.path, confidence = logo.minConfidence)

        if logoBox == None or not returnRandCoords:
            return logoBox
        
        return self.getRandCoords(logoBox)
    
    # Double clicks with a short delay interval between each click
    def doubleClick(self) -> None:
        pt.click(2, 0.07)

    # Rests for a bit until cops pass to the next neighborhood 
    def goOnLowProfileTheCopsAreComing(self) -> None:
        sleep(randbelow(2) + self.getRandDuration())
        

    # --------------------------
    # Student Program Functions:
    # --------------------------

    # Attempts to find the goBackArrow logo and click it.
    # Returns True upon success, or false if failed to find the logo
    def clickGoBackArrow(self) -> bool:
        goBackArrowCoords = self.locateLogoOnScreen(LOGOS['goBackArrow'])
        
        if goBackArrowCoords == None:
            return False
        
        pt.moveTo(goBackArrowCoords.x, goBackArrowCoords.y, self.getRandDuration(), pt.easeInOutQuad)
        pt.click()
        return True
        
        
    # Attempts to enter the alliance tab.
    # Returns True upon success or False if the tab logo could not be found
    def enterAllianceTab(self) -> bool:
        if not self.isMainScreenVisible():
            return False

        if not self.isItSafeToClick():
            return False
        
        allianceTabCoords = self.locateLogoOnScreen(LOGOS['alliance'])
        
        if allianceTabCoords == None:
            return False
        
        pt.moveTo(allianceTabCoords.x, allianceTabCoords.y, self.getRandDuration(), pt.easeInOutQuad)
        pt.click()
        return True

    # Attempts to enter the inventory tab.
    # Returns true upon success, or False if failed for any reason.
    # Possible failure reasons are:
    # Main screen isn't visible, not safe to click, logo not found
    def enterInventoryTab(self) -> bool:
        if not self.isMainScreenVisible():
            return False
        
        if not self.isItSafeToClick():
            return False
        
        inventoryButtonCoords = self.locateLogoOnScreen(LOGOS['inventoryMainButton'])

        if inventoryButtonCoords == None:
            return False
        
        pt.moveTo(inventoryButtonCoords.x, inventoryButtonCoords.y, self.getRandDuration(), pt.easeInOutQuad)
        pt.click()
        return True
    
    # Attempts to enter the battle tab.
    # Returns True upon success, or False if failed for any reason.
    # Possible failure reasons could be: peaceful state, unsafe to join, logo was not found
    def enterAllianceBattleTab(self) -> bool:
        if self.isAllianceInPeacefulState():
            return False

        if not self.isItSafeToClick():
            return False
        
        battleCoords = self.locateLogoOnScreen(LOGOS['battle'])

        if battleCoords == None:
            return False
        
        pt.moveTo(battleCoords.x, battleCoords.y, self.getRandDuration(), pt.easeInOutQuad)
        pt.click()
        return True

    # Same as enterBattleTab - defined simply for context
    # so that code is easier to read.
    def refreshAllianceBattleTab(self) -> bool:
        return self.enterAllianceBattleTab()

    # Attempts to open the rally tab (within the battle tab).
    # Returns True upon success, or False if failed for any reason.
    # Possible failure reasons could be: unsafe to join, logo not found.
    def openRallyTab(self) -> bool:
        if not self.isItSafeToClick():
            return False
        
        sleep(self.getRandDuration())

        rallyTabCoords = self.locateLogoOnScreen(LOGOS['noneJoined'])
        
        if rallyTabCoords == None:
            return False
        
        pt.moveTo(rallyTabCoords.x, rallyTabCoords.y, self.getDuration())
        self.doubleClick()
        return True

    # Attempts to join a rally by finding and clicking the blue join rally button.
    # Returns True upon success, or False if failed for any reason.
    # Possible failure reasons could be: 
    # unsafe to join, logo not found (either incorrect tab, or button isn't blue)
    def clickJoinRallyButton(self) -> bool:
        if not self.isItSafeToClick():
            return False
        
        joinRallyButtonCoords = self.locateLogoOnScreen(LOGOS['joinRallyBlue'])
        
        if joinRallyButtonCoords == None:
            return False
        
        pt.moveTo(joinRallyButtonCoords.x, joinRallyButtonCoords.y, self.getRandDuration(), pt.easeInOutQuad)
        self.doubleClick()
        return True

    # Attempts to click the rally tab's march button.
    # Returns True upon success, or False if failed for any reason.
    # Possible failure reasons are:
    # not in rally tab, unsafe to join, button 2 is not clicked, logo not found
    def clickRallyTabMarchButton(self) -> bool:
        if not self.isItSafeToClick:
            return False
        
        marchButtonCoords = self.locateLogoOnScreen(LOGOS['marchButton'])
        
        if marchButtonCoords == None:
            return False
        
        pt.moveTo(marchButtonCoords.x, marchButtonCoords.y, self.getRandDuration, pt.easeInOutQuad)
        pt.click()
        return True

    # TODO: Implement below function
    def improvedDrag(self) -> None:
        pass
    
    #########################################################################################################################
    #                                   End of new/improved/modified Functions Section                                      #
    #########################################################################################################################

    
    def battletab(self):
        # check if there is a rally
        if pt.locateOnScreen('images/none.png', confidence=.9) is None:
            # check if you are in battle tab
            if pt.locateOnScreen('images/dontjoinatall.png', confidence=.7) is None:
                if pt.locateOnScreen(self.target_png, confidence=.8) is None:
                    pt.moveTo(randrange(0, 200), randrange(75, 95), randrange(1, 2))
                    pt.click()
                    pt.moveTo(randrange(1600, 1700), randrange(910, 1000), randrange(1, 2))
                    pt.click()
                    pt.moveTo(randrange(150, 280), randrange(380, 450), randrange(1, 2))
                    pt.click()
                    sleep(randrange(1, 3))
                    pt.click()
                    return 0

    def autojoin(self):
        if pt.locateOnScreen('images/dontjoinatall.png', confidence=.7) is None:
            sleep(randrange(1, 3))
            position = pt.locateOnScreen('images/nonjoined.png', confidence=.9)
            # check if there is free sp, no return 0, yes execute and return 1
            if position is None:
                return 0
            else:
                pt.moveTo(position[0] + randrange(1, 100), position[1] + randrange(1, 10), randrange(1, 2))
                pt.click()
                pt.click()
                return 1

    def checkandjoined(self):
        if pt.locateOnScreen('images/dontjoinatall.png', confidence=.7) is None:
            sleep(randrange(1, 3))

            if pt.locateOnScreen('images/ReadySpartois.png' , confidence=.8) == None:
                return

            pt.moveTo(randrange(780, 1140), randrange(890, 990), randrange(1, 2))
            pt.click()
            pt.click()
            sleep(randrange(1, 2))
            pt.moveTo(randrange(1450, 1550), randrange(270, 320), randrange(1, 2))
            pt.click()
            sleep(randrange(1, 2))
            pt.moveTo(randrange(1650, 1750), randrange(890, 980), randrange(1, 2))
            pt.click()

    def drag(self):
        if pt.locateOnScreen('images/dontjoinatall.png', confidence=.7) is None:
            # check if there is a rally
            if pt.locateOnScreen('images/none.png', confidence=.9) is None:
                sleep(randrange(1, 2))
                pt.moveTo(randrange(1250, 1750), randrange(890, 980), randrange(1, 2))
                pt.mouseDown()
                sleep(randrange(1, 2))
                pt.moveTo(randrange(1250, 1750), randrange(590, 780), 1)
                pt.mouseUp()
                sleep(randrange(1))
                pt.mouseUp()


# Define the list of passwords
passwords = ['pass']

start = Clicker('images/Battle.png', speed=.001)

# Create the main window
window = tk.Tk()
window.title("Login")
window.geometry("300x200")

# Define the main function
def main():
    while True:
        start.battletab()
        if start.autojoin() != 0:
            start.checkandjoined()
            pt.moveTo(randrange(150, 280), randrange(380, 450), randrange(1, 2))
            pt.click()
            sleep(randrange(1, 3))
            pt.click()
        start.battletab()
        start.drag()
        if start.autojoin() != 0:
            start.checkandjoined()
            pt.moveTo(randrange(150, 280), randrange(380, 450), randrange(1, 2))
            pt.click()
            sleep(randrange(1, 3))
            pt.click()
        start.battletab()
        start.drag()
        start.drag()
        if start.autojoin() != 0:
            start.checkandjoined()

# Define the login function
def login():
    # Get the username and password from the input fields
    username = username_input.get()
    password = password_input.get()

    # Check if the entered password matches any of the passwords in the list
    if password in passwords:
        # Show a welcome message
        welcome_label.config(text="Welcome, " + username + "!")

        # Close the login window after a delay
        window.after(2000, window.destroy)

        # Call the main function
        main()

    else:
        # Show an error message and clear the password input field
        error_label.config(text="Invalid password. Please try again.")
        password_input.delete(0, tk.END)


# Create the username input label and input field
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_input = tk.Entry(window)
username_input.pack()

# Create the password input label and input field
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_input = tk.Entry(window, show="*")
password_input.pack()

# Create the login button
login_button = tk.Button(window, text="Login", command=login)
login_button.pack()

# Create the welcome and error labels
welcome_label = tk.Label(window, text="")
welcome_label.pack()
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

# Run the main loop
window.mainloop()
