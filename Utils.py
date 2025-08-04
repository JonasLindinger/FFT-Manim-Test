from math import *
from manim import *

class Point:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

class Wave:
    def __init__(self, axes: Axes):
        self.amplitude: float = 1
        self.step: float = 0.01
        self.end: float = (axes.x_range[1] - axes.x_range[0])
        self.set_up: bool = False
        self.points: list = []
    
    def Set_Up_From_Frequency(self, frequency: float, xOffset: float) -> None:
        x: float = 0

        while (x <= self.end):
            y: float = self.amplitude * sin(2 * pi * frequency * (x + xOffset))
            self.points.append(Point(x, y))

            x += self.step

        self.set_up = True

    def Set_Up_From_Points(self, points: list) -> None:
        self.points = points

        self.set_up = True

    def Combine(waves: list):
        match(len(waves)):
            case 0:
                raise RuntimeError("List has a length of 0!")
            case 1:
                return waves[0]
            
        # Combine waves
        points: list = []
        firstWave = waves[0]

        i = 0
        for point in firstWave:
            x: float = point.x
            combinedY: float = 0

            for wave in waves:
                combinedY += wave.points[i]

            points.append(Point(x, combinedY))

            i += 1

        newWave = Wave()
        newWave.Set_Up_From_Points(points)

        return newWave