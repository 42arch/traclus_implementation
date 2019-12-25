from distance_functions import determine_longer_and_shorter_lines
from geometry import LineSegment

line_a = LineSegment.from_tuples((0, 0), (2, 0))
line_b = LineSegment.from_tuples((0, 0), (0, 3))
print(line_a.as_dict())
print(line_b.as_dict())

longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
print('长线段', longer_line.as_dict())
print('短线段', shorter_line.as_dict())