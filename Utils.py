from math import *
from manim import *

def Get_Distance(p1: Point, p2: Point) -> float:
        return sqrt(pow(p2.x - p1.x, 2) + pow(p2.y  - p1.y, 2))

class Point:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

class CircularPointData:
    def __init__(self, cycles_per_second: float, yOffset: float, points: list):
        self.cycles_per_second: float = cycles_per_second
        self.yOffset: float = yOffset
        self.points: list = points

class CenterOfMassPointData:
    def __init__(self, cycles_per_second: float, yOffset: float, point: Point):
        self.cycles_per_second: float = cycles_per_second
        self.yOffset: float = yOffset
        self.point: Point = point

class FrequencyGraphPointData:
    def __init__(self, xMin: float, xMax: float, yOffset: float, points: list):
        self.xMin: float = xMin
        self.xMax: float = xMax
        self.yOffset: float = yOffset
        self.points = points

class Wave:
    def __init__(self, end: float):
        self.amplitude: float = 1
        self.step: float = 0.01
        self.end: float = end
        self.set_up: bool = False
        self.points: list = []
        self.pointsDic = {}

        # Cach
        self.calculatedCircularPointData: list = []
        self.centerOfMassPointData: list = []
        self.frequencyGraphPointData: list = []
    
    def Set_Up_From_Frequency(self, frequency: float, xOffset: float) -> None:
        x: float = 0

        while (x <= self.end):
            y: float = self.amplitude * sin(2 * pi * frequency * (x + xOffset))
            self.points.append(Point(x, y))
            self.pointsDic[x] = y

            x += self.step

        self.set_up = True

    def Set_Up_From_Points(self, points: list) -> None:
        self.points = points

        for point in self.points:
            self.pointsDic[point.x] = point.y

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
    
    def Get_Circular_Points(self, cycles_per_second: float, yOffset: int) -> list:
        # Check cach
        for pointData in self.calculatedCircularPointData:
            if pointData.cycles_per_second == cycles_per_second and pointData.yOffset == yOffset:
                return pointData.points

        length = len(self.points)

        newPoints: list = []
        for i in range(length):
            point: Point = self.points[i]

            angle = TAU * cycles_per_second * point.x

            x: float = cos(angle) * (point.y + yOffset)
            y: float = sin(-angle) * (point.y + yOffset)

            newPoints.append(Point(x, y))

        # Save in cach
        self.calculatedCircularPointData.append(CircularPointData(cycles_per_second, yOffset, newPoints))

        return newPoints
    
    def Get_Center_of_Mass(self, cycles_per_second: float, yOffset: float) -> Point:
        # Check cach
        for pointData in self.centerOfMassPointData:
            if pointData.cycles_per_second == cycles_per_second and pointData.yOffset == yOffset:
                return pointData.point

        points: list = self.Get_Circular_Points(cycles_per_second, yOffset)
        length: int = len(self.points)

        totalX: float = 0
        totalY: float = 0

        for point in points:
            totalX += point.x
            totalY += point.y

        x: float = totalX / length
        y: float = totalY / length

        point: Point = Point(x, y)

        # Save in cach
        self.centerOfMassPointData.append(CenterOfMassPointData(cycles_per_second, yOffset, point))

        return point
    
    def Get_Frequency_Graph_Points(self, xMin: float, xMax: float, yOffset: float):
        # Check cach
        for pointData in self.frequencyGraphPointData:
            if pointData.xMin == xMin and pointData.xMax == xMax and pointData.yOffset == yOffset:
                return pointData.points
        
        center: Point = Point(0, 0)
        multiplier: float = abs(xMin + xMax)

        x: float = xMin
        points: list = []
        while x < xMax:
            center_of_mass: Point = self.Get_Center_of_Mass(x, yOffset)
            y: float = abs(Get_Distance(center, center_of_mass))

            points.append(Point(x, y * multiplier))

            x += self.step

        # Save in Cach
        self.frequencyGraphPointData.append(FrequencyGraphPointData(xMin, xMax, yOffset, points))

        return points