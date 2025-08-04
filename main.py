from manim import *
from Utils import *
import numpy as np

def Create_Wave_From_Frequency(axes: Axes, frequency: float, xOffset: float) -> Wave:
    # Create a 3 Beats / Second Wave
    wave: Wave = Wave(axes)
    wave.Set_Up_From_Frequency(frequency, xOffset)
    return wave

def Get_Lines_From_Wave(axes: Axes, wave: Wave) -> VGroup:
    # Convert to scene points
    coords = [axes.coords_to_point(p.x, p.y) for p in wave.points]

    # Connect points with lines
    lines = VGroup()
    for i in range(len(coords) - 1):
        lines.add(Line(coords[i], coords[i + 1], color=YELLOW))

    return lines

class FFT(Scene):
    def construct(self):
        # Create Coordinate system with labels
        axes = Axes(
            x_range=[0, 4.5], 
            y_range=[0, 2], 
            x_length=13, 
            y_length= 1.5,
            axis_config={"include_numbers": True},
        ).move_to([0, 2.5, 0])

        labels = axes.get_axis_labels(
            Text("Time").scale(0.5), Text("Intensity").scale(0.5)
        )

        self.add(axes, labels)

        wave3Hz = Get_Lines_From_Wave(axes, Create_Wave_From_Frequency(axes, 3, -0.25))

        self.play(Create(wave3Hz))

        
        


    


            















class HelloWorld(Scene):
    def construct(self):
        rect1 = Rectangle(height = 0.5, width= 0.5, fill_opacity = 1).shift(LEFT * 5)
        rect2 = Rectangle(height = 0.5, width= 0.5, fill_opacity = 1).move_to([5, 0, 0])

        r1 = Rectangle(height = 0.5, width = 0.5, fill_opacity = 1)
        r2 = Rectangle(height = 0.5, width = 0.5, fill_opacity = 1) 
        r3 = Rectangle(height = 0.5, width = 0.5, fill_opacity = 1) 
        r4 = Rectangle(height = 0.5, width = 0.5, fill_opacity = 1)
        r5 = Rectangle(height = 0.5, width = 0.5, fill_opacity = 1)

        group = VGroup(r1, r2, r3, r4, r5)
        group.arrange()
        group.set_color_by_gradient(RED, ORANGE, YELLOW_C, PURE_GREEN)

        self.play(Write(rect1))
        self.play(Write(rect2))

        group2 = VGroup(rect1, rect2)

        self.play(rect2.animate.next_to(rect1, RIGHT))
        self.play(ReplacementTransform(group2, group))

        s1 = SurroundingRectangle(group, color = WHITE)
        s2 = SurroundingRectangle(s1, color = WHITE)

        self.play(Write(s1), Write(s2, run_time = 1.5))

        t = Text("1 2 3 4 5").next_to(s2, UP, buff = 0.3).scale(1.5)
        self.play(Write(t))

        self.play(Indicate(t[0], colot = RED), Indicate(r1, color = RED, scale_factor= 0.3))
        self.play(Indicate(t[1], colot = RED), Indicate(r2, color = RED, scale_factor= 0.3))
        self.play(Indicate(t[2], colot = RED), Indicate(r3, color = RED, scale_factor= 0.3))
        self.play(Indicate(t[3], colot = RED), Indicate(r4, color = RED, scale_factor= 0.3))
        self.play(Indicate(t[4], colot = RED), Indicate(r5, color = RED, scale_factor= 0.3))

        g3 = VGroup(group, t, s1, s2)

        d = Dot(color = RED)

        self.play(ReplacementTransform(g3, d))
        self.play(d.animate.scale(150))
        self.play(FadeOut(d))

        self.wait(3)