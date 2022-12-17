import geometry
import math

def test_point_class():
    point1 = geometry.Point(100, 100)
    point2 = geometry.Point(100, 100)
    point4 = geometry.Point(-100, -100)
    point3 = geometry.Point(0, 0)

    assert point1 == point2
    assert point1 != point3 
    assert point3 == point3
    assert point1.dist2(point3) == 20000

    point1.rotate(point3, math.pi)
    assert point1 == point4
    assert point2.is_parallel(point4)
    assert point1.is_parallel(point4)
    assert point3.is_parallel(point4)
    assert (point1 % point2) == point3



def test_line_class():
    point1 = geometry.Point(100, 100)
    point2 = geometry.Point(10, 0)
    line1 = geometry.Line(point1 = point1, point2 = point2)
    line2 = geometry.Line(a = 1, b = 0, c = -10)
    line3 = geometry.Line(a = 1, b = 0, c = -20)

    assert line2.get_parallel_vector() == geometry.Point(0, 1)
    assert not line1.is_parallel(line2)
    assert line1.is_parallel(line1)
    assert line2.is_parallel(line3)
    assert line2 ^ line3 is None
    assert line1 ^ line2 == point2



def test_segment_class():
    seg1 = geometry.Segment(geometry.Point(10, 10), geometry.Point(20, 20))
    seg2 = geometry.Segment(geometry.Point(20, 10), geometry.Point(0, 10))
    seg3 = geometry.Segment(geometry.Point(0, 0), geometry.Point(20, 20))
    
    assert seg1.is_in(geometry.Point(10, 10))
    assert seg2.is_in(geometry.Point(10, 10))
    assert seg1.is_in(geometry.Point(15, 15))
    assert seg1.is_in(geometry.Point(12, 12))

    assert seg1 ^ seg2 is not None
    assert seg1 ^ seg2 == geometry.Point(10, 10)
    assert seg3 ^ seg2 == geometry.Point(10, 10)

    assert seg2.get_up() == 10 and seg2.get_down() == 10
    assert seg1.get_up() == 20 and seg1.get_down() == 10

    assert (geometry.Segment(geometry.Point(994.5936153452441, 67.64679301523503), 
                             geometry.Point (998.4621304329248, 48.024494703967115)) ^
            geometry.Segment(geometry.Point(1200, 50), geometry.Point(50, 50))) is not None



def test_polyline_class():
    polyline = geometry.Polyline([geometry.Point(10, 10), geometry.Point(10, 100), geometry.Point(100, 100)])
    assert polyline.get_segments()[0] == geometry.Segment(geometry.Point(10, 10), geometry.Point(10, 100))
    assert polyline.get_segments()[1] == geometry.Segment(geometry.Point(10, 100), geometry.Point(100, 100))
    assert len(polyline.get_segments()) == 2


def test_rectangle_class():
    rectangle1 = geometry.Rectangle(point1=geometry.Point(10, 10), lenx = 100, leny = 10)
    rectangle2 = geometry.Rectangle(point1=geometry.Point(20, 10), lenx = 200, leny = 10)

    assert len(rectangle1 ^ rectangle2) != 0
    rectangle1.move(10, 20)
    assert rectangle1.point1 == geometry.Point(20, 30)

    
    polyline = geometry.Polyline([geometry.Point(10, 10), geometry.Point(10, 100), geometry.Point(100, 100)])
    assert len(rectangle2.intersect_poly(polyline)) == 0