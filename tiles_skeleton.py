import numpy as np
import cv2


TILE_SIZE = 32
OFS = 50

MARKET = """
##################
##..............##
#R..HA..ME..IB..P#
#R..HA..ME..IB..P#
#R..HA..ME..IB..P#
#Y..HA..ME..IB..P#
#Y..HA..ME..IB..P#
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split("\n")]
        self.xsize = len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros(
            (self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()
    
    def extract_tile(self, row, col):
        y = (row-1)*32
        x = (col-1)*32
        return self.tiles[y:y+32, x:x+32]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(1,1)
        elif char == "G":
            return self.extract_tile(8,4)
        elif char == "C":
            return self.extract_tile(3,9)
        elif char == "B":
            return self.extract_tile(1,5)
        elif char == "E":
            return self.extract_tile(8,12)
        elif char == "A":
            return self.extract_tile(7,14)
        elif char == "R":
            return self.extract_tile(4,9)
        elif char == "Y":
            return self.extract_tile(5,9)
        elif char == "P":
            return self.extract_tile(6,5)
        elif char == "I":
            return self.extract_tile(5,14)
        elif char == "M":
            return self.extract_tile(4,14)
        elif char == "H":
            return self.extract_tile(7,4)
        else:
            return self.extract_tile(1,3)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile(tile)
                self.image[
                    y * TILE_SIZE : (y + 1) * TILE_SIZE,
                    x * TILE_SIZE : (x + 1) * TILE_SIZE,
                ] = bm

    def draw(self, frame, offset=OFS):
        """
        draws the image into a frame
        offset pixels from the top left corner
        """
        frame[
            OFS : OFS + self.image.shape[0], OFS : OFS + self.image.shape[1]
        ] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)

class Customer:

    def __init__(self, terrain_map, image, x, y):

        self.terrain_map = terrain_map
        self.image = image
        self.x = x # the column
        self.y = y # the row
    
    def __repr__(self):
        return f'the customer is now at {self.x} and {self.y}!'

    def draw(self, frame):
        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
        frame[ypos:ypos+TILE_SIZE, xpos:xpos+TILE_SIZE] = self.image
        # overlay the Customer image / sprite onto the frame
    
    def move(self, direction):
        newx = self.x
        newy = self.y
        if direction == 'up':
            newy -= 1
        if direction == 'down':
            newy += 1
        if direction == 'left':
            newx -= 1
        if direction == 'right':
            newx += 1
        if self.terrain_map.contents[newy][newx] == '.':
            self.x = newx
            self.y = newy


if __name__ == "__main__":

    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    market = SupermarketMap(MARKET, tiles)
    cust_image = market.extract_tile(5,1)
    cust1 = Customer(market, cust_image, 14, 10)

    while True: # this script will run forever
        frame = background.copy()
        market.draw(frame) # it draws in to the supermarket
        cust1.draw(frame)

        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == "q":
            break
        if key == 'w':
            cust1.move('up')
        if key == 'a':
            cust1.move('left')
        if key == 'd':
            cust1.move('right')
        if key == 'z':
            cust1.move('down')


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
