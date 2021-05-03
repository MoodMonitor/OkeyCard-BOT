from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, DictProperty
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.metrics import dp, sp, Metrics
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import NoTransition
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from dateutil.relativedelta import *
from kivy.uix.bubble import Bubble
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
import random
import math
from functools import partial
import time
import os
import traceback
from kivy.input.recorder import Recorder

import itertools
from itertools import combinations, chain
import openpyxl
import ast

Builder.load_string("""

<S1>:
    karty: karty
    cz: cz
    n: n
    z: z
    BoxLayout:
        orientation: "vertical"
        padding: app.sz/29,0,0,0
        pos_hint: {"top": 0.96, "left": 0.5}
        size_hint: 1,None
        height: self.minimum_height
        Label:
            size_hint: None,None
            text: "Game number: " + str(root.ilosc)
            height: app.wy/20
        Label:
            size_hint: None,None
            text: "Wins: " + str(root.wygrane)
            height: app.wy/20
  
    BoxLayout:
        orientation: "vertical"
        size_hint: 1, None
        height: self.minimum_height
        padding: app.sz/5,0,app.sz/5,0
        pos_hint: {"top": 0.90, "left": 0.5}
        Label:
            size_hint: 1,None
            height: app.wy/15
            font_size: sp(21)
            text: "Available cards"
        GridLayout: # 5 Kart aktualnych
            id: karty
            cols: 5
            rows: 1
            size_hint: 1, None
            height: self.minimum_height
    BoxLayout:
        orientation: "vertical"
        size_hint: 1, None
        height: self.minimum_height
        padding: app.sz/9,0,app.sz/9,0
        pos_hint: {"top": 0.57, "left": 0.5}
        Label:
            size_hint: 1,None
            height: app.wy/15
            font_size: sp(21)
            text: "Undiscarded cards"
        GridLayout: # 5 Kart aktualnych
            id: cz
            cols: 8
            size_hint: 1, None
            height: self.minimum_height
        GridLayout: # 5 Kart aktualnych
            id: n
            cols: 8
            size_hint: 1, None
            height: self.minimum_height
        GridLayout: # 5 Kart aktualnych
            id: z
            cols: 8
            size_hint: 1, None
            height: self.minimum_height    
    
    Label:
        size_hint: None,None
        pos_hint: {"right": 1.02, "top": 0.20}
        text: "Points"
    Label:
        size_hint: None,None
        pos_hint: {"right": 1.02, "top": 0.15}
        text: str(root.punkty)
    Button:
        pos_hint: {"right": 0.105, "top": 0.11}
        size_hint: None,None
        text: 'Next card'
        on_press: root.Dodaj2(self)
        height: app.wy/10
        width: app.sz/10
    Button:
        size_hint: None,None
        text: "Next set"
        on_press: root.ZACZYNAMY3()
        pos_hint: {"top": 0.955, "right": 0.99} 
        height: app.wy/11  
        width: app.sz/10 
    Button:
        size_hint: None,None
        text: "Results"
        on_press: root.manager.current = "2"
        pos_hint: {"top": 0.84, "right": 0.99} 
        height: app.wy/11  
        width: app.sz/10
    Button:
        size_hint: None,None
        text: "How to Play"
        on_press: root.pp()
        pos_hint: {"top": 0.73, "right": 0.99} 
        height: app.wy/11  
        width: app.sz/9.5 

<S2>:
    wyniki: wyniki
    wyniki2: wyniki2
    Button:
        size_hint: None,None
        text: "Back"
        pos_hint: {"top": 0.94, "right": 0.15}  
        height: app.wy/11  
        width: app.sz/10  
        on_press: root.manager.current = "1"       
   
    GridLayout:
        cols: 2
        StackLayout:
            padding: app.sz/10,0,0,0
            GridLayout:
                id: wyniki
                size_hint: 1,1
                cols: 2
        StackLayout:
            GridLayout:
                id: wyniki2
                size_hint: 1,1
                cols: 2
<Karta@Button>:
    size_hint: None, None
    width: app.sz/8
    height: app.wy/4
    on_press: app.root.get_screen("1").pop(self)

<Kartaa@Button>:
    size_hint: None, None
    width: app.sz/10
    height: app.wy/6

""")



class S1(Screen):
    punkty = NumericProperty()
    wygrane = NumericProperty()
    ilosc = NumericProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ilosc = 0
        self.wygrane = 0
        self.f = 0
        self.listy = [
            ['4C', '4N', '5N', '1Z', '4Z', '6C', '1N', '8N', '6Z', '7C', '8C', '3C', '1C', '6N', '3Z', '2Z', '8Z', '3N',
             '2C', '2N', '5C', '7Z', '5Z', '7N'],
            ['2N', '3N', '5N', '7N', '6Z', '8Z', '3Z', '4N', '1Z', '4Z', '7C', '2C', '6C', '7Z', '1C', '2Z', '5Z', '5C',
             '1N', '8N', '3C', '8C', '4C', '6N'],
            ['5C', '4N', '5N', '2Z', '3Z', '7Z', '1C', '5Z', '8Z', '1Z', '6Z', '7C', '4Z', '1N', '8C', '6C', '6N', '3N',
             '4C', '3C', '2N', '2C', '7N', '8N'],
            ['4C', '6C', '3N', '6N', '3Z', '4N', '8N', '1N', '1C', '2C', '8Z', '2Z', '3C', '5N', '7C', '6Z', '7Z', '4Z',
             '2N', '5Z', '8C', '5C', '1Z', '7N'],
            ['1C', '2N', '6N', '4Z', '8Z', '2C', '1N', '5N', '5Z', '7Z', '6C', '4C', '2Z', '4N', '3N', '8N', '7N', '3C',
             '1Z', '8C', '3Z', '7C', '5C', '6Z'],
            ['3C', '4C', '7C', '8C', '5Z', '5C', '2N', '1N', '8Z', '4N', '2Z', '1C', '5N', '2C', '1Z', '8N', '3Z', '6Z',
             '6N', '7Z', '7N', '6C', '4Z', '3N'],
            ['6C', '6N', '7N', '8N', '7Z', '8C', '1C', '2Z', '5N', '2N', '2C', '4N', '1Z', '5Z', '1N', '5C', '3N', '8Z',
             '6Z', '4Z', '3C', '4C', '3Z', '7C'],
            ['7C', '8C', '5N', '2Z', '6Z', '1C', '1N', '4N', '3C', '2C', '4Z', '4C', '6C', '7N', '3Z', '5C', '5Z', '7Z',
             '3N', '8Z', '8N', '6N', '1Z', '2N'],
            ['4C', '5C', '1N', '3N', '5Z', '4Z', '3C', '2C', '3Z', '7N', '5N', '8N', '6Z', '8Z', '1C', '4N', '2Z', '8C',
             '2N', '6C', '6N', '7Z', '1Z', '7C'],
            ['1C', '4C', '7N', '1Z', '5Z', '7Z', '6C', '5N', '5C', '6N', '2C', '1N', '8N', '8C', '7C', '6Z', '2N', '3Z',
             '8Z', '4Z', '3C', '4N', '2Z', '3N'],
            ['1C', '2C', '3N', '6N', '1Z', '2Z', '8C', '7C', '7Z', '5Z', '4Z', '2N', '3C', '8N', '4N', '1N', '5C', '4C',
             '5N', '6Z', '6C', '7N', '3Z', '8Z'],
            ['2N', '1Z', '2Z', '5Z', '7Z', '8C', '3N', '4Z', '4N', '4C', '1N', '3C', '7N', '6Z', '6C', '5C', '2C', '7C',
             '1C', '8Z', '5N', '6N', '3Z', '8N'],
            ['5C', '6C', '1N', '1Z', '7Z', '4Z', '7N', '7C', '8N', '2Z', '3N', '4C', '2N', '4N', '3Z', '5Z', '8C', '5N',
             '6Z', '1C', '8Z', '2C', '3C', '6N'],
            ['1C', '4C', '4N', '8N', '4Z', '7N', '8C', '8Z', '2Z', '3C', '6C', '7C', '6Z', '2N', '7Z', '5N', '6N', '1N',
             '2C', '3N', '3Z', '5Z', '1Z', '5C'],
            ['5C', '2N', '3N', '4Z', '8Z', '6N', '4C', '7C', '8N', '5Z', '2C', '7N', '6Z', '1Z', '2Z', '1C', '8C', '7Z',
             '4N', '6C', '1N', '3C', '5N', '3Z'],
            ['1C', '6C', '5N', '1Z', '3Z', '4C', '8N', '6N', '3N', '4Z', '2C', '7Z', '6Z', '5Z', '2Z', '5C', '4N', '7C',
             '2N', '3C', '7N', '1N', '8Z', '8C'],
            ['7C', '2N', '7N', '8N', '5Z', '1N', '1C', '1Z', '3Z', '3C', '5C', '6Z', '4N', '2Z', '5N', '3N', '2C', '4Z',
             '4C', '8C', '8Z', '6N', '6C', '7Z'],
            ['6C', '2N', '4N', '6N', '6Z', '8C', '4C', '2C', '4Z', '3Z', '7C', '8Z', '5C', '3C', '1N', '3N', '7Z', '7N',
             '2Z', '8N', '5Z', '5N', '1Z', '1C'],
            ['2C', '1Z', '4Z', '5Z', '8Z', '6Z', '3C', '7Z', '6C', '2Z', '3Z', '7C', '4N', '8C', '5C', '1N', '2N', '1C',
             '4C', '3N', '6N', '5N', '8N', '7N'],
            ['8C', '4N', '7N', '4Z', '7Z', '6N', '3N', '5Z', '6C', '4C', '7C', '5C', '5N', '2C', '1Z', '8Z', '2Z', '3C',
             '6Z', '3Z', '2N', '1N', '1C', '8N'],
            ['4C', '1N', '5N', '1Z', '6Z', '2N', '7C', '3Z', '5C', '7N', '8C', '4Z', '8Z', '8N', '4N', '1C', '2Z', '6N',
             '6C', '3C', '7Z', '2C', '5Z', '3N'],
            ['2C', '5N', '1Z', '3Z', '5Z', '3C', '8C', '1N', '6C', '4C', '2Z', '2N', '1C', '7C', '7Z', '6Z', '8N', '6N',
             '8Z', '4Z', '3N', '4N', '7N', '5C'],
            ['6C', '7N', '8N', '5Z', '7Z', '4Z', '4N', '3C', '1C', '1Z', '8Z', '8C', '3Z', '5C', '2C', '2N', '3N', '6Z',
             '6N', '1N', '5N', '2Z', '4C', '7C'],
            ['2C', '4C', '7C', '3Z', '7Z', '8N', '8C', '1N', '7N', '2Z', '3N', '6Z', '6C', '1C', '4N', '4Z', '2N', '8Z',
             '3C', '1Z', '5N', '5Z', '5C', '6N'],
            ['2N', '4N', '6N', '8N', '8Z', '7Z', '1N', '1C', '6Z', '3C', '2Z', '5N', '3N', '5Z', '5C', '4Z', '1Z', '7C',
             '8C', '3Z', '2C', '6C', '7N', '4C'],
            ['2N', '5N', '1Z', '5Z', '7Z', '3Z', '8N', '7N', '6C', '6Z', '8C', '1C', '2C', '8Z', '4C', '5C', '3C', '7C',
             '6N', '1N', '4N', '3N', '4Z', '2Z'],
            ['3C', '2Z', '3Z', '7Z', '8Z', '1Z', '5Z', '6Z', '1N', '5C', '7N', '8N', '4N', '4Z', '4C', '8C', '3N', '6C',
             '5N', '7C', '2N', '1C', '6N', '2C'],
            ['1C', '2C', '4C', '8C', '8Z', '3N', '5Z', '8N', '7N', '3Z', '7Z', '1N', '3C', '6Z', '5N', '1Z', '6N', '2N',
             '4Z', '6C', '2Z', '5C', '4N', '7C'],
            ['8C', '7N', '4Z', '5Z', '6Z', '3Z', '6N', '1N', '5N', '8N', '6C', '3N', '4C', '7Z', '7C', '2N', '1Z', '5C',
             '8Z', '4N', '2C', '2Z', '3C', '1C'],
            ['3C', '7C', '8C', '8N', '6Z', '4N', '2C', '1Z', '5Z', '3Z', '1N', '7Z', '2Z', '3N', '8Z', '1C', '6C', '4Z',
             '7N', '6N', '4C', '2N', '5C', '5N'],
            ['5C', '7C', '8C', '3Z', '8Z', '6C', '4Z', '5N', '4N', '8N', '7Z', '3N', '6Z', '1N', '5Z', '1Z', '1C', '4C',
             '2Z', '3C', '2N', '2C', '7N', '6N'],
            ['1C', '2N', '3Z', '7Z', '8Z', '2C', '6C', '5C', '8C', '7C', '7N', '8N', '4C', '2Z', '1Z', '3N', '6N', '3C',
             '1N', '4N', '4Z', '5Z', '6Z', '5N'],
            ['1C', '5C', '6C', '3N', '1Z', '8Z', '4N', '4Z', '8N', '3Z', '2Z', '7C', '5N', '2C', '7Z', '3C', '4C', '2N',
             '5Z', '6Z', '8C', '1N', '6N', '7N'],
            ['8C', '1N', '6N', '5Z', '7Z', '1C', '3N', '1Z', '5C', '3C', '2N', '4N', '7C', '8Z', '4C', '6Z', '4Z', '5N',
             '3Z', '8N', '2C', '6C', '2Z', '7N'],
            ['3C', '5N', '8N', '2Z', '7Z', '5C', '7N', '6Z', '8C', '2N', '7C', '1C', '1Z', '3N', '2C', '6N', '4C', '5Z',
             '4N', '8Z', '6C', '4Z', '3Z', '1N'],
            ['3C', '6C', '7C', '6N', '2Z', '8C', '8Z', '5C', '2C', '1N', '7N', '3Z', '1C', '8N', '4N', '4C', '4Z', '5N',
             '3N', '2N', '6Z', '7Z', '5Z', '1Z'],
            ['7C', '4N', '8N', '2Z', '4Z', '3C', '5N', '3N', '7N', '2C', '1N', '8C', '6C', '7Z', '3Z', '5C', '4C', '6N',
             '6Z', '8Z', '1Z', '1C', '2N', '5Z'],
            ['3C', '2N', '3N', '5N', '4Z', '4N', '5Z', '1C', '1Z', '6C', '6Z', '6N', '1N', '4C', '2C', '8C', '5C', '8Z',
             '7C', '3Z', '8N', '7Z', '2Z', '7N'],
            ['1N', '4N', '5N', '7N', '1Z', '1C', '6C', '2N', '6Z', '8Z', '3N', '3Z', '4Z', '8C', '2C', '2Z', '8N', '7Z',
             '5C', '3C', '7C', '4C', '6N', '5Z'],
            ['8C', '3N', '6N', '8N', '7Z', '6Z', '2N', '1C', '2Z', '7N', '7C', '4C', '1N', '3Z', '4Z', '1Z', '5N', '3C',
             '6C', '4N', '5Z', '2C', '5C', '8Z'],
            ['7C', '6N', '1Z', '3Z', '6Z', '6C', '7N', '2Z', '2N', '5N', '8Z', '3N', '7Z', '3C', '4N', '8N', '4C', '5Z',
             '2C', '4Z', '5C', '8C', '1N', '1C'],
            ['7C', '8C', '6N', '2Z', '4Z', '6Z', '5Z', '1N', '2N', '2C', '4N', '6C', '5N', '8N', '8Z', '3Z', '4C', '7N',
             '5C', '1Z', '1C', '3C', '7Z', '3N'],
            ['6C', '7C', '1N', '4N', '4Z', '5C', '8C', '4C', '5N', '3C', '8Z', '2C', '7N', '1C', '3Z', '3N', '8N', '2Z',
             '6N', '7Z', '2N', '5Z', '6Z', '1Z'],
            ['2C', '4C', '6C', '4N', '3Z', '8N', '2Z', '4Z', '8C', '6N', '1N', '7C', '8Z', '5N', '5Z', '1C', '5C', '3C',
             '3N', '1Z', '7Z', '7N', '6Z', '2N'],
            ['4C', '6C', '8N', '4Z', '5Z', '6Z', '8Z', '2C', '2N', '5N', '6N', '3C', '1C', '3Z', '8C', '1Z', '7Z', '5C',
             '7C', '2Z', '3N', '7N', '4N', '1N'],
            ['3C', '6C', '8C', '1N', '2Z', '7C', '1Z', '5Z', '8N', '5C', '6N', '2C', '1C', '3Z', '2N', '8Z', '6Z', '4Z',
             '4C', '3N', '5N', '7Z', '4N', '7N'],
            ['2C', '5C', '1N', '3N', '6N', '3Z', '7C', '1Z', '8C', '7Z', '6Z', '7N', '3C', '4Z', '5Z', '2N', '1C', '4C',
             '6C', '5N', '4N', '2Z', '8N', '8Z'],
            ['5C', '6N', '1Z', '3Z', '4Z', '2Z', '3C', '4N', '5N', '7N', '1N', '4C', '8C', '2C', '6C', '8N', '5Z', '3N',
             '1C', '7C', '6Z', '2N', '7Z', '8Z'],
            ['6C', '3N', '5N', '8N', '3Z', '7C', '7N', '3C', '8Z', '6N', '1N', '5C', '4N', '4Z', '7Z', '2N', '2Z', '5Z',
             '6Z', '8C', '1Z', '1C', '4C', '2C'],
            ['7C', '7N', '8N', '7Z', '3Z', '1Z', '8C', '4C', '3C', '2C', '4N', '1C', '5C', '8Z', '5N', '5Z', '6C', '6Z',
             '3N', '2N', '6N', '1N', '4Z', '2Z']]
        self.ZACZYNAMY3()


    def on_enter(self, *args):
        pass

    def Dodaj2(self, el):

        try:
            #a = random.choice(list(self.zbior.keys()))
            a = self.list[0]
        except:
            pass

        try:
            self.karty.add_widget(self.zbior[a])
            self.aktualne.append(a)
            #print(self.aktualne)
            del self.zbior[a]
            self.list.remove(self.list[0])
            self.kart+=1
        except:

            try:
                self.karty.remove_widget(self.zbior[a])
            except:
                pass


    def ZACZYNAMY3(self):
        if self.ilosc >=1 and self.f == 0:
            if self.ilosc <= 25:
                self.l = Label(text = "Game number " + str(self.ilosc))
                sm.get_screen("2").wyniki.add_widget(self.l)
                self.l = Label(text = str(self.punkty), size_hint = (None, 1), width = Window.width/35)
                sm.get_screen("2").wyniki.add_widget(self.l)
            else:
                self.l = Label(text = "Game number " + str(self.ilosc))
                sm.get_screen("2").wyniki2.add_widget(self.l)
                self.l = Label(text = str(self.punkty), size_hint = (None, 1), width = Window.width/35)
                sm.get_screen("2").wyniki2.add_widget(self.l)
        if self.ilosc == 50:
            if self.f == 0:
                self.l = Label(text = str("END, check the Results"), pos_hint = {"top": 1}, size_hint = (1,None))
                self.add_widget(self.l)
                self.f = 1
            return
        try:
            if self.punkty >= 400:
                self.wygrane+=1
                self.ilosc+=1
            else:
                self.ilosc+=1
        except:
            pass
        self.karty.clear_widgets()
        self.cz.clear_widgets()
        self.n.clear_widgets()
        self.z.clear_widgets()
        self.Stworz()
        self.automat = {}
        self.licznik = 0
        self.punkty = 0
        self.aktualne = []
        self.list = self.listy[0]
        self.listy.remove(self.listy[0])
        self.Pomoc()
        for i in range(5):
            self.Dodaj2(None)

    def Dodaj(self, el):
        try:
            a = random.choice(list(self.zbior.keys()))
        except:
            pass
        #print(self.zbior[a], a)
        try:
            self.karty.add_widget(self.zbior[a])
            self.aktualne.append(a)
            #print(self.aktualne)
            del self.zbior[a]
        except:
            try:
                self.karty.remove_widget(self.zbior[a])
            except:
                pass


    def pp(self):
        self.content = BoxLayout(orientation = "vertical")
        self.popup = Popup(title='HOW TO PLAY',
                           content=self.content,
                           size_hint=(None, None), size=(Window.width, Window.height/2))
        #self.l = Label ")
        self.l = Label(text = "There are 24 cards, 3 colors(Red, Blue, Green), 8 cards each with numbers from 1 to 8.\n The goal of the game is to score at least 400 points, points can be earned by combining cards: \n 100 points - One by one, cards of same colors (eg. 1R,2R,3R, R - red colour) \n 10 + 10 * the smallest card number - One by one, cards of different colors (eg. 1R,2B,3R = 20 points, R- red, B- blue) \n  10 + 10 * number of card - Three cards of the same number(eg. 8R, 8B, 8Y = 90 poitns, R - red, B - blue, G- green) \n Click the card in Available Cards and select whether you want to add it to the combination or remove it. \n if you make a mistake in adding to the combination, add it again to the combination   " )
        self.b1 = Button(text="Leave", size_hint = (1,None), height = Window.height/24)
        self.content.add_widget(self.l)
        self.content.add_widget(self.b1)
        self.b1.bind(on_press = self.popup.dismiss)
        self.popup.open()


    def pop(self, el):
        self.pom = el
        #print(el)
        self.content = BoxLayout()
        self.popup = Popup(title='ACTION',
                           content=self.content,
                           size_hint=(None, None), size=(Window.width/2.5, Window.height/4))
        self.b1 = Button(text="Add to combination")
        self.b2 = Button(text="Discard")
        self.b1.bind(on_press=self.bind1)
        self.b2.bind(on_press=self.bind2)
        self.content.add_widget(self.b1)
        self.content.add_widget(self.b2)
        self.automat["Dodaj"] = self.b1
        self.automat["Usun"] = self.b2
        self.popup.open()

    def bind1(self, ee):
        el = self.pom
        b = list(el.ids.values())[0]
        if el.opacity == 0.5:
            el.opacity = 1
            self.licznik -= 1
            del self.dodane[str(b)]
            self.popup.dismiss()
            #print(self.dodane)
            return
        el.opacity = 0.5
        self.licznik += 1
        self.dodane[str(b)] = self.pom
        self.popup.dismiss()
        #print(self.dodane)
        if self.licznik == 3:
            self.sprawdz()


    def bind2(self, el):
        b = list(self.pom.ids.values())[0]

        self.pomoc[str(b)].opacity = 0.3
        self.karty.remove_widget(self.pom)
        self.aktualne.remove(b)
        self.popup.dismiss()
        del self.pomoc[str(b)]

    def Stworz(self):
        self.dodane = {}
        self.ogolne = {}
        self.zbior = {}
        #self.zbior["czerwony"] = {}
        for i in range(1,9):
            self.k = Karta()
            self.k.text = str(i)
            self.k.ids = {"A": str(i) + "C"}
            self.k.background_color = (1,0,0,1)
            #self.zbior["czerwony"][str(i)] = self.k
            self.zbior[str(i) + "C"] = self.k
            self.ogolne[str(i) + "C"] = self.k

        #self.zbior["niebieski"] = {}
        for i in range(1,9):
            self.k = Karta()
            self.k.text = str(i)
            self.k.background_color = (0,0,1,1)
            #self.zbior["niebieski"][str(i)] = self.k
            self.k.ids = {"A": str(i) + "N"}
            self.zbior[str(i) + "N"] = self.k
            self.ogolne[str(i) + "N"] = self.k

        #self.zbior["zielony"] = {}
        for i in range(1,9):
            self.k = Karta()
            self.k.text = str(i)
            self.k.background_color = (0,1,0,1)
            #self.zbior["zielony"][str(i)] = self.k
            self.k.ids = {"A": str(i) + "Z"}
            self.zbior[str(i) + "Z"] = self.k
            self.ogolne[str(i) + "Z"] = self.k

    def Pomoc(self):
        self.pomoc = {}
        for i in range(1,9):
            self.k = Kartaa()
            self.k.text = str(i)
            self.k.ids = {"A": str(i) + "C"}
            self.k.background_color = (1,0,0,1)
            #self.zbior["czerwony"][str(i)] = self.k
            self.pomoc[str(i) + "C"] = self.k
            self.cz.add_widget(self.k)

        #self.zbior["niebieski"] = {}
        for i in range(1,9):
            self.k = Kartaa()
            self.k.text = str(i)
            self.k.background_color = (0,0,1,1)
            #self.zbior["niebieski"][str(i)] = self.k
            self.k.ids = {"A": str(i) + "N"}
            self.pomoc[str(i) + "N"] = self.k
            self.n.add_widget(self.k)

        #self.zbior["zielony"] = {}
        for i in range(1,9):
            self.k = Kartaa()
            self.k.text = str(i)
            self.k.background_color = (0,1,0,1)
            #self.zbior["zielony"][str(i)] = self.k
            self.k.ids = {"A": str(i) + "Z"}
            self.pomoc[str(i) + "Z"] = self.k
            self.z.add_widget(self.k)

    def sprawdz(self):
        c = list(self.dodane)
        #print(c[0][1])

        if c[0][0] in c[1] and c[0][0] in c[2]:
            self.punkty = self.punkty + 20 + 10* (int(c[0][0])-1)
            #print(self.punkty)
            for i in c:
                self.karty.remove_widget(self.dodane[str(i)])
                self.pomoc[str(i)].opacity = 0.3
                del self.pomoc[str(i)]
                del self.dodane[str(i)]
                self.aktualne.remove(str(i))
            self.licznik = 0
            #dodaj 20 + 10 * tyle
            #usun co trzeba dodaj co trzeba
            return

        try:
            l = []
            for i in c:
                l.append(int(i[0]))
            ll = sorted(l)
            for i in range(1,len(ll)):
                if ll[i] - ll[i-1] != 1: #sprawdzamy czy jest po kolei
                    for i in c:
                        self.dodane[str(i)].opacity = 1
                        del self.dodane[str(i)]
                    self.licznik = 0
                    return # zmien wtedy wszystko i return

            if c[0][1] in c[1] and c[0][1] in c[2]:
                self.punkty = self.punkty + 100
                for i in c:
                    self.karty.remove_widget(self.dodane[str(i)])
                    self.pomoc[str(i)].opacity = 0.3
                    del self.pomoc[str(i)]
                    del self.dodane[str(i)]
                    self.aktualne.remove(str(i))
                self.licznik = 0
            else:
                self.punkty = self.punkty + 10*ll[0]
                for i in c:
                    self.karty.remove_widget(self.dodane[str(i)])
                    self.pomoc[str(i)].opacity = 0.3
                    del self.pomoc[str(i)]
                    del self.dodane[str(i)]
                    self.aktualne.remove(str(i))
                self.licznik = 0

        except Exception as e:
            traceback.print_exc()
            pass



class S2(Screen):
    wyniki = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Karta(Button):
    pass

class Kartaa(Button):
    pass

class Uruchom(App):

    sz = NumericProperty()
    wy = NumericProperty()

    def build(self):
        self.sz = Window.width
        self.wy = Window.height
        global sm
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(S1(name = "1"))
        sm.add_widget(S2(name = "2"))
        return sm

if __name__ == '__main__':
    Uruchom().run()
    
