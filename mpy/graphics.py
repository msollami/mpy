# TODO separate out graphics and images...

import PIL
from PIL import Image
import os
import pudb
from math import sqrt, ceil, floor
import sys

def get_basename(filename):
    """Strip path and extension. Return basename."""
    return os.path.splitext(os.path.basename(filename))[0]

# def image_type(img):
#     if type(img)

def ImageDimensions(img):
    return img.size

def ImageCrop(img_path, xmin=0, xmax=None, ymin=0, ymax=None, show=False, save=False):
    """
    ImageCrop[image, size] crops image based on the size specification size.

    ymin is the top!

    Not supported:
        ImageCrop[image] crops image by removing borders of uniform color.
        ImageCrop[image, size, spec] crops image by removing pixels from sides specified by spec.
    """
    original = Image.open(img_path)

    width, height = original.size   # Get dimensions
    if not xmax:
        xmax = width
    if not ymax:
        ymax = height

    cropped = original.crop((xmin, ymin, xmax, ymax))

    if show:
        original.show()
        cropped.show()

    save_path = img_path[:-4]+"_crop_"+"-".join(map(str,[xmin,xmax,ymin,ymax]))+img_path[-4:]

    if save:
        cropped.convert('RGB').save(save_path)


def ImagePartition(filename, number_tiles, directory=os.getcwd(), save=True):
    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
    Kwargs:
       save (bool): Whether or not to save tiles to disk.
    Returns:
        Tuple of :class:`Tile` instances.
    """

    def validate_image(image, number_tiles):
        """Basic sanity checks prior to performing a split."""
        TILE_LIMIT = 99 * 99

        try:
            number_tiles = int(number_tiles)
        except:
            raise ValueError('number_tiles could not be cast to integer.')

        if number_tiles > TILE_LIMIT or number_tiles < 2:
            raise ValueError('Number of tiles must be between 2 and {} (you \
                              asked for {}).'.format(TILE_LIMIT, number_tiles))

    def calc_columns_rows(n):
        """
        Calculates the number of columns and rows required to divide an image
        into n square parts.
        Returns:
            Ruple of integers in the format (num_columns, num_rows)
        """
        num_columns = int(ceil(sqrt(n)))
        num_rows = int(ceil(n / float(num_columns)))
        return (num_columns, num_rows)

    def save(image, filename=None, format='png'):
        if not filename:
            filename = self.generate_filename(format=format)
        image.save(filename, format)

    def generate_filename(col, row, directory=os.getcwd(), prefix='tile', format='png', path=True):
        """Construct and return a filename for this tile."""
        filename = prefix + '_{col:02d}_{row:02d}.{ext}'.format(
                      col=col, row=row, ext=format)
        if not path:
            return filename

        return os.path.join(directory, filename)

    def save_tiles(tiles, prefix='', directory=os.getcwd(), format='png'):
        """
        Write image files to disk. Create specified folder(s) if they
           don't exist. Return list of :class:`Tile` instance.
        Args:
           tiles (list):  List, tuple or set of :class:`Tile` objects to save.
           prefix (str):  Filename prefix of saved tiles.
        Kwargs:
           directory (str):  Directory to save tiles. Created if non-existant.
        Returns:
            Tuple of :class:`Tile` instances.
        """
        # Causes problems in CLI script.
        # if not os.path.exists(directory):
        #   os.makedirs(directory)

        for tile in tiles:
            [image, number, [row, col], coords] = tile
            save(image, filename=generate_filename(row, col,
                prefix=prefix, directory=directory, format=format))

        return tuple(tiles)

    # main method
    im = Image.open(filename)
    validate_image(im, number_tiles)

    im_w, im_h = im.size
    print im_w, im_h
    columns, rows = calc_columns_rows(number_tiles)
    extras = (columns * rows) - number_tiles
    tile_h = int(min(floor(im_w / columns),floor(im_h / rows)))
    tile_w = tile_h
    print "(tile_w, tile_h) = ", (tile_w, tile_h)
    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = [image, number, position, coords]
            tiles.append(tile)
            number += 1

    if not directory:
        directory = os.path.dirname(filename)
    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=directory)

    return tuple(tiles)

def Show(img):
    """
        help
    """
    import cv2

    t = type(img)
    if isinstance(img,str): #TODO replace with switch
        cv2.namedWindow('iPython Image Preview')
        i = cv2.imread(img) #TODO replace with Import
        cv2.imshow('iPython Image Preview', )
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif isinstance(img,PIL.Image.Image):
        img.show('iPython Image Preview')
    elif isinstance(img.cv2.Image):
        cv2.namedWindow('iPython Image Preview')
        cv2.imshow('iPython Image Preview', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("image unreadable")

def ImageResize(img, size):
    import PIL
    return img.resize(size, PIL.Image.BILINEAR)

def makeImage(arr):
    res = Failed
    if len(arr) == 3:
        rgb = np.dstack((arr[0],arr[1],arr[2]))#(r,g,b)
        img = Image.fromarray(rgb, 'RGB')
    else:
        print("image unreadable")

    return res

import glob
fns = glob.glob('/data/products/images/*.jpg')
for i, f in enumerate(fns):
    print '\x1b[2K\r', i, f
    try:
        ImagePartition(f,4,'/data/products/crops/')
    except:
        print "can't read image: ", i, f
