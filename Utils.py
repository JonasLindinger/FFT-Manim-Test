from math import *
from manim import *

class Point:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

class Wave:
    def __init__(self, end: float):
        self.amplitude: float = 1
        self.step: float = 0.01
        self.end: float = end
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
        for point in firstWave.points:
            x: float = point.x
            combinedY: float = 0

            for wave in waves:
                combinedY += wave.points[i].y

            points.append(Point(x, combinedY))

            i += 1

        newWave = Wave(0)
        newWave.Set_Up_From_Points(points)

        return newWave
    
    def Get_Circular_Points(self, cycles_per_second: float) -> list:
        length = len(self.points)

        newPoints: list = []
        for i in range(length):
            point: Point = self.points[i]

            angle = TAU * cycles_per_second * point.x

            x: float = cos(angle) * point.y
            y: float = sin(angle) * point.y

            newPoints.append(Point(x, y))

        return newPoints
    
    def Get_Center_of_Mass(self, cycles_per_second: float) -> Point:
        points: list = self.Get_Circular_Points(cycles_per_second)
        length: int = len(self.points)

        totalX: float = 0
        totalY: float = 0

        for point in points:
            totalX += point.x
            totalY += point.y

        x: float = totalX / length
        y: float = totalY / length

        return Point(x, y)