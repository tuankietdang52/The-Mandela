

class Physic:
    def __init__(self):
        pass

    @staticmethod
    def collide(obj1, obj2) -> bool:
        """
        Please provide obj with x, y, width and height attribute
        :param Any obj1:
        :param Any obj2:
        """

        if (not hasattr(obj1, "x")
                and hasattr(obj1, "y")
                and hasattr(obj1, "width")
                and hasattr(obj1, "height")):

            raise ReferenceError

        if (not hasattr(obj2, "x")
                and hasattr(obj2, "y")
                and hasattr(obj2, "width")
                and hasattr(obj2, "height")):
            raise ReferenceError

        dx = (obj2.x, obj2.x + obj2.width)
        dy = (obj2.y, obj2.y + obj2.height)

        if dx[0] <= obj1.x <= dx[1] and dy[0] <= obj1.y <= dy[1]:
            print(f"Collide with {obj2.oid}")
            return True

        return False
