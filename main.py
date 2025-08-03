from manim import *

class HelloWorld(Scene):
    def construct(self):
        # ANIMATIONS
        t = Text("hello").shift(UP)
        t2 = Text("hello").shift(DOWN)
        self.play(Write(t), Write(t2))
        self.wait(3)