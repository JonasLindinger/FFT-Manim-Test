from manim import *
from Utils import *
import numpy as np

def Create_Wave_From_Frequency(axes: Axes, frequency: float, xOffset: float) -> Wave:
    # Create a 3 Beats / Second Wave
    wave: Wave = Wave((axes.x_range[1] - axes.x_range[0]))
    wave.Set_Up_From_Frequency(frequency, xOffset)
    return wave

def Get_Lines_From_Points(axes: Axes, points: list, yOffset: float) -> VGroup:
    # Convert to scene points
    coords = [axes.coords_to_point(p.x, p.y + yOffset) for p in points]

    # Connect points with lines
    lines = VGroup()
    for i in range(len(coords) - 1):
        lines.add(Line(coords[i], coords[i + 1], color=YELLOW))

    return lines

def Get_Coors_Of_Point(axes: Axes, point: Point, offset: Point):
    return axes.coords_to_point(point.x + offset.x, point.y + offset.y)

class FFT(Scene):
    def construct(self):
        # --------------------------------------------
        # Create Coordinate system with labels
        # --------------------------------------------
        baseFrequencyAxesPosition: Point = Point(0, 2.5)
        baseFrequencyAxes = Axes(
            x_range=[0, 4.5], 
            y_range=[0, 2], 
            x_length=13, 
            y_length= 1.5,
            axis_config={"include_numbers": True},
        ).move_to([baseFrequencyAxesPosition.x, baseFrequencyAxesPosition.y, 0])

        baseFrequencyAxesLabel = baseFrequencyAxes.get_axis_labels(
            Text("Time").scale(0.5), Text("Intensity").scale(0.5)
        )

        baseFrequencyCoordinateSystem: VGroup = VGroup(baseFrequencyAxes, baseFrequencyAxesLabel)

        self.play(Write(baseFrequencyCoordinateSystem), run_time = 0.5)

        # --------------------------------------------
        # Display base wave
        # --------------------------------------------
        wave: Wave = Wave(baseFrequencyAxes.x_range[1])
        wave.Set_Up_From_Frequency(3, -0.25)

        graph = Get_Lines_From_Points(baseFrequencyAxes, wave.points, 1)

        self.play(Write(graph), run_time=3)

        # --------------------------------------------
        # Circular Wave Coordinate system
        # --------------------------------------------
        circularWaveAxesPosition: Point = Point(-4.5, -1.5)
        circularWaveAxes = Axes(
            x_range=[-1.5, 1.5], 
            y_range=[-1.5, 1.5], 
            x_length=4, 
            y_length= 4,
            axis_config={"include_numbers": True},
        ).move_to([circularWaveAxesPosition.x, circularWaveAxesPosition.y, 0])

        self.play(Write(circularWaveAxes), run_time = 0.5)

        # --------------------------------------------
        # Wrap a copy of the base wave around the origin
        # --------------------------------------------
        wrappingGraph = graph.copy()

        self.add(wrappingGraph)

        cycles_per_second = ValueTracker(0.1)

        yOffset: float = 1
        originGraph = always_redraw(
            lambda:
            Get_Lines_From_Points(circularWaveAxes, wave.Get_Circular_Points(cycles_per_second.get_value(), yOffset), 0)
        )

        cycles_per_second_text_position = Point(-4.5, 1.3)
        cycles_per_second_text = always_redraw(
            lambda:
            Text(str(round(cycles_per_second.get_value(), 2)) + " Cycles per second", font_size=16).move_to([cycles_per_second_text_position.x, cycles_per_second_text_position.y, 0])
        )

        self.play(ReplacementTransform(wrappingGraph, originGraph), Write(cycles_per_second_text), run_time=2)

        # --------------------------------------------
        # Add Center of mass to Graph and do fancy animation
        # --------------------------------------------
        centerOfMass = always_redraw(
            lambda:
            Dot(Get_Coors_Of_Point(circularWaveAxes, wave.Get_Center_of_Mass(cycles_per_second.get_value(), yOffset), Point(0, 0)), radius=0.08, color = RED, fill_opacity = 1)
        )

        self.play(Write(centerOfMass), run_time = 0.5)

        self.wait(4)

        self.play(cycles_per_second.animate.set_value(.5), run_time=3)

        self.wait(2)

        self.play(cycles_per_second.animate.set_value(1.5), run_time=2)

        self.wait(.5)

        self.play(cycles_per_second.animate.set_value(.3), run_time=2)

        self.wait(.5)

        self.play(cycles_per_second.animate.set_value(3), run_time=10)

        self.wait(3)

        self.play(cycles_per_second.animate.set_value(3.5), run_time=.5)

        self.wait(1.5)

        self.play(cycles_per_second.animate.set_value(.1), run_time=5)

        # --------------------------------------------
        # Add Frequency Graph
        # --------------------------------------------
        self.wait(2)

        centerOfMassArrow = always_redraw(
            lambda:
            Arrow(
                start = Get_Coors_Of_Point(circularWaveAxes, Point(0, 0), Point(0, 0)),
                end = centerOfMass.get_center(),
                buff= LARGE_BUFF,
            )
        )

        self.play(Write(centerOfMassArrow))

        frequencyGraphAxesPosition: Point = Point(2, -1.5)
        frequencyGraphAxes = Axes(
            x_range=[0, 6], 
            y_range=[0, 4], 
            x_length = 7.5, 
            y_length = 4,
            axis_config={"include_numbers": True},
        ).move_to([frequencyGraphAxesPosition.x, frequencyGraphAxesPosition.y, 0])

        self.play(Write(frequencyGraphAxes), run_time=.5)

        graph = Get_Lines_From_Points(frequencyGraphAxes, wave.Get_Frequency_Graph_Points(frequencyGraphAxes.x_range[0], frequencyGraphAxes.x_range[1], yOffset), 0)
        graph.set_color(RED)

        self.play(Write(graph), cycles_per_second.animate.set_value(6), run_time=5)

        self.wait(6)

        # --------------------------------------------
        # Shift the Wave down
        # --------------------------------------------
        self.play(cycles_per_second.animate.set_value(.1), run_time=2)

        yOffset = 0
        shiftedOriginGraph = always_redraw(
            lambda:
            Get_Lines_From_Points(circularWaveAxes, wave.Get_Circular_Points(cycles_per_second.get_value(), yOffset), 0)
        )

        shiftedCenterOfMass = always_redraw(
            lambda:
            Dot(Get_Coors_Of_Point(circularWaveAxes, wave.Get_Center_of_Mass(cycles_per_second.get_value(), yOffset), Point(0, 0)), radius=0.08, color = RED, fill_opacity = 1)
        )

        self.play(ReplacementTransform(originGraph, shiftedOriginGraph), ReplacementTransform(centerOfMass, shiftedCenterOfMass), run_time=3)
        self.play(Unwrite(graph), run_time=.5)
        self.play(cycles_per_second.animate.set_value(.1), run_time=5)

        shiftedGraph = Get_Lines_From_Points(frequencyGraphAxes, wave.Get_Frequency_Graph_Points(frequencyGraphAxes.x_range[0], frequencyGraphAxes.x_range[1], yOffset), 0)
        shiftedGraph.set_color(RED)

        self.play(cycles_per_second.animate.set_value(6), Write(shiftedGraph), run_time=5)

        # --------------------------------------------
        # Todo
        # --------------------------------------------
        