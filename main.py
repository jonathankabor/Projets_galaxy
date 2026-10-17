from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')


from kivy.properties import Clock
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Line, Color
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import platform





class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    V_NB_LINES = 10
    V_LINES_SPACING = 0.25   # pourcentage of the width
    vertical_lines = []
    
    H_NB_LINES = 8
    H_LINES_SPACING = 0.1   # pourcentage of the width
    horizontal_lines = []
    
    SPEED = 4
    current_offset_y = 0
    
    SPEED_X = 3
    current_speed_x = 0
    current_offset_x = 0
    
    
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
       
       
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
        
    def is_desktop(self):
        platforms = ['linux', 'win', 'macosx']
        if platform in platforms:
            return True
        return False
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = -self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = self.SPEED_X
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        return True
    
    def on_parent(self, widget, parent):
        print("ON PARENT W: " + str(self.width) + " H: " + str(self.height))
        
        
    def on_size(self, *args):
        #self.update_vertical_lines()
        #self.update_horizontal_lines()
        # print("ON SIZE W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height / 0.75
        pass

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
        
    def transform_2D(self, x, y):
        return int(x), int(y)
        
    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y
                
        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 4)
            
            
        offset_x = diff_x * factor_y
            
            
        tr_x = self.perspective_point_x + offset_x
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y 
        return int(tr_x), int(tr_y)


    def on_perspective_point_x(self, widget, value):
        # print("PX: " + str(value))
        pass

    def on_perspective_point_y(self, widget, value):
        # print("PY: " + str(value))
        pass
    
    
    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            # V_NB_LINES = 7
            # V_LINES_SPACING = 0.1   
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())
            
            
    def update_vertical_lines(self):
        start_index = -int(self.V_NB_LINES / 2)+1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i + start_index)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i - start_index].points = [x1, y1, x2, y2]
            
        
        
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            # H_NB_LINES = 7
            # H_LINES_SPACING = 0.2   
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())
                    
                    
    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES / 2)+1
        end_index = start_index + self.V_NB_LINES - 1
                
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index - 1)
        spacing_y = self.H_LINES_SPACING * self.height
        for i in range(0, self.H_NB_LINES):
            line_y = i*spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
    
    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
        
    def on_touch_up(self, touch):
        self.current_speed_x = 0
        
        
    def update(self, dt):
        # print("dt : " + str(dt * 60))
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED * time_factor
        self.current_offset_x += self.current_speed_x * time_factor

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            
            
    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.width * self.V_LINES_SPACING
        offset = index - 0.5 
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

class GalaxyApp(App):
    pass


GalaxyApp().run()