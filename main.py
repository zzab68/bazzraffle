###############################################################################
#                            RUN MAIN                                         #
###############################################################################

# setup
import warnings
warnings.filterwarnings("ignore")
import math
import random
import kivy
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.image import Image
from kivymd.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from functools import partial

# Global variables in Python, similar to public/private static final.
# SHUFFLE_DURATION_COUNTER x SHUFFLE_ANIMATION_GAP = Total Shuffle Time, in Seconds.
SHUFFLE_ANIMATION_GAP =  0.1 # how long between the number shuffled on screen, in Seconds.
SHUFFLE_DURATION_COUNTER = 20 # How many times the shuffle occurs.

# Load the KV file
Builder.load_file('components.kv')

# screens
class IntroScreen(Screen):
    start_raffle_number = 0
    finish_raffle_number = 0
    max_numbers = 0
    finish_number_length = 0
    def start_raffle(self, *args):
        # First up, perform all error checking on the Raffle numbers before progressing.
        # Start abd Finish Raffle numbers must be greater than 1 and finish_raffle_number > start_raffle_number.
        if not self.ids.start_number.text:
            #print(" ERROR = start_number Text box is empty.")
            Factory.NumberEntryError().open()
            return
        else:
            #print(" start_number Text box contains content.")
            IntroScreen.start_raffle_number = int(self.ids.start_number.text)
            if IntroScreen.start_raffle_number <1:
                #print("ERROR = start_number is less than 1.")
                Factory.NumberEntryError().open()
                return  # This exits the my_kivy_method function
        if not self.ids.finish_number.text:
            #print(" ERROR = finish_raffle_number Text box is empty.")
            Factory.NumberEntryError().open()
            return
        else:
            #print(" finish_number Text box contains content.")
            IntroScreen.finish_raffle_number = int(self.ids.finish_number.text)
            if IntroScreen.finish_raffle_number <1:
                #print("ERROR = finish_integer is less than 1.")
                Factory.NumberEntryError().open()
                return  # This exits the my_kivy_method function
        if IntroScreen.start_raffle_number >= IntroScreen.finish_raffle_number :
            #print("ERROR = FINISHING NUMBER must be greater than STARTING NUMBER.")
            Factory.NumberEntryError().open()
            return  # This exits the my_kivy_method function
        else:
            # The max_number must include start and finish number.
            IntroScreen.max_numbers = IntroScreen.finish_raffle_number  - IntroScreen.start_raffle_number + 1
            # This sets big number display digit length equal to finish numbers digit length.
            IntroScreen.finish_number_length = int(math.log10(IntroScreen.finish_raffle_number)) + 1
            """
            print(f'STARTING NUMBER is {IntroScreen.start_raffle_number}') 
            print(f'FINISHING NUMBER is {IntroScreen.finish_raffle_number}') 
            print(f'MAX RAFFLE NUMBERS is {IntroScreen.max_numbers}') 
            print(f'IntroScreen.finish_number_length is {IntroScreen.finish_number_length}') 
            """
            formatted_number = str('0').zfill(IntroScreen.finish_number_length)
            # The next line sets the big RAFFLE number to zeros with digit length equal to finish numbers digit length.
            self.manager.get_screen('main_screen').ids.displayed_raffle_number.text =  f"{formatted_number}"
            self.manager.get_screen('main_screen').ids.pick_winner_button.disabled = False
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'main_screen' # change screens here due to logic; the kv file can't do logic for transitions.

    def reset_nums(self):
        self.ids.start_number.text = ''
        self.ids.finish_number.text = ''

class MainScreen(Screen):
    # Initialize an empty list to store raffle numbers
    unique_raffle_numbers = []  
    unique_raffle_numbers.clear()  
    count = 0
        
    # This method updates the BIG SHUFFLED RANDOM number Label displayed_raffle_number.
    def update_main_raffle_number(self):
        formatted_finish_number = str(self.new_random_number).zfill(IntroScreen.finish_number_length)
        self.ids.displayed_raffle_number.text = f"{formatted_finish_number}"
        #print(f"new_random_number inside update_main_raffle_number = {formatted_finish_number} ")
        self.ids.drawn_raffle_list.text = f"{self.unique_raffle_numbers}"
        
    # This method updates the list of drawn raffle numbers with the new number.
    def update_raffle_list_display(self):
        self.ids.drawn_raffle_list.text = f"{self.unique_raffle_numbers}"
        
    def clear_Raffle_array(self):
        self.unique_raffle_numbers = []
        self.unique_raffle_numbers.clear()
        self.ids.pick_winner_button.disabled = False
     
    def start_animation(self):
        self.count = 0
        self.event = Clock.schedule_interval(self.animate_text, SHUFFLE_ANIMATION_GAP)
        # Schedule the stop event after the shuffle duration. 
        #Clock.schedule_once(self.stop_animation, SHUFFLE_DURATION_TIME)   
        
    def animate_text(self, dt):
        """Called every 0.1 seconds to add a new character."""
        self.count += 1
        fake_random_number = str(random.randint(IntroScreen.start_raffle_number, IntroScreen.finish_raffle_number))
        formatted_fake_number = str(fake_random_number).zfill(IntroScreen.finish_number_length)
        #formatted_finish_number = str(self.new_random_number).zfill(IntroScreen.finish_number_length)
        self.ids.displayed_raffle_number.text = f"{formatted_fake_number}"
        #self.ids.displayed_raffle_number.text = f"{formatted_finish_number}"
        #print(f" Fake random number = {fake_random_number}")
        #print(f" formatted_fake_number = {formatted_fake_number}")
        if len(self.unique_raffle_numbers) < IntroScreen.max_numbers:
            if self.count >= SHUFFLE_DURATION_COUNTER:
                self.update_main_raffle_number()
                #self.update_raffle_list_display()
                self.ids.pick_winner_button.disabled = False
                self.event.cancel() # Stop the interval
                #self.stop_animation(dt) # Stop the interval
        else:
            #self.count = 0
            self.update_main_raffle_number()
            #self.update_raffle_list_display()
            self.ids.pick_winner_button.disabled = False
            #print(f"IntroScreen.max_numbers Maximum Number = {IntroScreen.max_numbers} in animate_text.")
            #Factory.RaffleFull().open()
            self.event.cancel() # Stop the interval

    # Generate a new random unique raffle number and add it to the unique_raffle_numbers list. 
    def generate_and_add_number(self):
        self.ids.pick_winner_button.disabled = True
        if len(self.unique_raffle_numbers) < IntroScreen.max_numbers:
            while True:  # Simulates a do-while loop
                self.new_random_number = random.randint(IntroScreen.start_raffle_number, IntroScreen.finish_raffle_number)
                #print(f"Random Number generated = {self.new_random_number} ")
                if self.new_random_number not in self.unique_raffle_numbers:
                    self.unique_raffle_numbers.append(self.new_random_number)
                    break  # Exit the loop once a unique raffle number is found and added
        else:
            #print(f"Maximum Number of {IntroScreen.max_numbers} in generate_and_add_number.")
            # If we have exhausted all possible raffle numbers in the range, disply Popup and Disable PICK A WINNER button.
            Factory.RaffleFull().open()
            self.ids.pick_winner_button.disabled = True
            
class MyScreenManager(ScreenManager):
    pass

class bazzRaffle(App):
    def build(self):
        sm = MyScreenManager()
        Window.clearcolor = (1, 1, 1, 1) 
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(MainScreen(name='main'))
        return sm

########################## Run ##########################
if __name__ == '__main__':
    bazzRaffle().run()
