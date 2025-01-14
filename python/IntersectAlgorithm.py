# A Python3 program to find if 2 given line segments intersect or not
# This code is contributed by Ansh Riyal from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
import networkx


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


    def __hash__(self):
        return hash((self.x, self.y))
    # Given three collinear points p, q, r, the function checks if


# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False

# def onSegmentStronger(p,q,r):
#     try:
#         kpr = (r.y-p.y)/(r.x-p.x)
#     except ZeroDivisionError:
#         kpr = (r.y-p.y)/0.001
#     try:
#         kqr = (r.y-q.y)/(r.x-q.x)
#     except ZeroDivisionError:
#         kqr = (r.y-q.y)/0.001
#     try:
#         kqp = (q.y-p.y)/(q.y-p.y)
#     except ZeroDivisionError:
#         kqp = (q.y-p.y)/0.001
#     if kpr == kqr == kqp and onSegment(p, q, r):
#         return True

def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
# adapted by adding line 58~59
def doIntersect(p1, q1, p2, q2):
    if len((p1, q1, p2, q2)) != len(set((p1, q1, p2, q2))):
        return False
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)



    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return 2

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return 2

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return 2

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return 2

    # General case
    if ((o1 != o2) and (o3 != o4)):
        # fix
        # onSegment is weaker than its name
        return 1

    # If none of the cases
    return 0



    # This code is contributed by Ansh Riyal


