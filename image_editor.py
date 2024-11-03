#################################################################
# FILE : image_editor.py
# WRITER : HADAS NUKRAI , hadasnuk2_ , 207310855
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A program for picture's editting, using couple of function for
# edit the picture
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
from copy import *
import math
import sys


##############################################################################
#                                  Functions                                 #
##############################################################################

# A function that separate channels, return a picture with separated channels
def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    w = len(image[0])
    h = len(image)
    c = len(image[0][0])
    tencor = [[[0 for _ in range(w)]for _ in range(h)]for _ in range(c)]
    for i in range(c):
        for j in range(h):
            for k in range(w):
                tencor[i][j][k] = copy(image[j][k][i])
    return tencor

# A function that combines the channels. return a colorful picture


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    w = len(channels[0])
    h = len(channels)
    c = len(channels[0][0])
    tencor = [[[0 for _ in range(h)]for _ in range(c)]for _ in range(w)]
    for i in range(w):
        for j in range(c):
            for k in range(h):
                tencor[i][j][k] = copy(channels[k][i][j])
    return tencor

# A function that getting a colorful picture and returning grayscale picture


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    w = len(colored_image[0])
    h = len(colored_image)
    RED = 0.299
    GREEN = 0.587
    BLUE = 0.114
    avarage = 0
    matrix = [[0 for _ in range(w)]for _ in range(h)]
    for i in range(h):
        for j in range(w):
            avarage = colored_image[i][j][0]*RED + \
                colored_image[i][j][1]*GREEN+colored_image[i][j][2]*BLUE
            matrix[i][j] = copy(round(avarage))
    return matrix

# A function that calculate the kernel for blurring the picture


def blur_kernel(size: int) -> Kernel:
    value = 1 / math.pow(size, 2)
    matrix = [[value for _ in range(size)]for _ in range(size)]
    return matrix

# A function that blurring the image by returning a new image calculate with kernel


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    m = len(kernel)//2
    matrix = [[0 for _ in range(len(image[0]))]for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            sum = 0
            for a in range(len(kernel)):
                for b in range(len(kernel[0])):
                    if i-m+a < 0 or j-m+b < 0 or i-m+a >= len(image) or j-m+b >= len(image[0]):
                        sum += float(kernel[a][b])*float(image[i][j])
                    else:
                        sum += float(kernel[a][b])*float(image[i-m+a][j-m+b])
            if sum > 255:
                sum = 255
            if sum < 0:
                sum = 0
            matrix[i][j] = round(sum)
    return matrix

# A function that calculate the new pixel for the image, after resize, by bilinear_interpolation


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    a = image[math.floor(y)][math.floor(x)]
    # In case the y coordinat is 0, add 1
    if math.ceil(y) == 0:
        new_y = math.ceil(y)+1
        b = image[new_y][math.floor(x)]
    else:
        new_y = math.ceil(y)
        b = image[new_y][math.floor(x)]
    if math.floor(x) == 0:
        # In case the x coordinat is 0, add 1
        new_x = math.floor(x)+1
        c = image[math.floor(y)][new_x]
    else:
        new_x = math.ceil(x)
        c = image[math.floor(y)][new_x]
    if math.ceil(y) == 0 and math.ceil(x) == 0:
        # In case the x and y coordinat is 0, add 1
        d = image[math.ceil(y)+1][math.ceil(x)+1]
    elif math.ceil(y) == 0 and math.ceil(x) != 0:
        d = image[math.ceil(y)+1][math.ceil(x)]
    elif math.ceil(y) != 0 and math.ceil(x) == 0:
        d = image[math.ceil(y)][math.ceil(x)+1]
    else:
        d = image[math.ceil(y)][math.ceil(x)]
    delta_x = abs(math.floor(x)-x)
    delta_y = abs(math.floor(y)-y)
    pixel = round(float(a)*(1-delta_x)*(1-delta_y)+float(b)*delta_y *
                  (1-delta_x)+float(c)*delta_x*(1-delta_y)+float(d)*delta_x*delta_y)
    return pixel

# A function that calculate the pixels of the image with new sizes


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    new_image = [[0 for _ in range(new_width)]for _ in range(new_height)]
    for i in range(new_height):
        for j in range(new_width):
            if i == 0 and j == 0:
                new_image[i][j] = copy(image[0][0])
            elif i == new_height-1 and j == 0:
                new_image[i][j] = copy(image[len(image)-1][0])
            elif i == 0 and j == new_width-1:
                new_image[i][j] = copy(image[0][len(image[0])-1])
            elif i == new_height-1 and j == new_width-1:
                new_image[i][j] = copy(image[len(image)-1][len(image[0])-1])
            else:
                y = (i/(new_height-1))*(len(image)-1)
                x = (j/(new_width-1))*(len(image[0])-1)
                new_image[i][j] = bilinear_interpolation(image, y, x)
    return new_image

# A function that rotate the picture to the side the user input


def rotate_90(image: Image, direction: str) -> Image:
    rotate_pic = [[0 for _ in range(len(image))]for _ in range(len(image[0]))]
    col = len(image)-1
    if direction == 'R':
        for i in range(len(image)):
            for j in range(len(image[0])):
                rotate_pic[j][col] = copy(image[i][j])
            col -= 1
    elif direction == 'L':
        for i in range(len(image)):
            row = len(rotate_pic)-1
            for j in range(len(image[0])):
                rotate_pic[row][i] = copy(image[i][j])
                row -= 1
    return rotate_pic

# A function that getting a black and white image and returning grayscale image with the same sizes


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    new_image = [[0 for _ in range(len(image[0]))] for _ in range(len(image))]
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    r = block_size//2
    for i in range(len(image)):
        for j in range(len(image[0])):
            sum = 0
            for a in range(block_size):
                for b in range(block_size):
                    if i-r+a < 0 or j-r+b < 0 or i-r+a >= len(image) or j-r+b >= len(image[0]):
                        sum += blurred_image[i][j]
                    else:
                        sum += blurred_image[i-r+a][j-r+b]
            threshold = ((sum-blurred_image[i][j]) //
                         (block_size*block_size-1)) - c
            if threshold > blurred_image[i][j]:
                new_image[i][j] = 0
            elif threshold < blurred_image[i][j]:
                new_image[i][j] = 255
    return new_image

# A function that calculate the quanize on the image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    new_image = [[0 for _ in range(len(image[0]))] for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            new_image[i][j] = round(math.floor(image[i][j]*N/256)*255/(N-1))
    return new_image

# A function that calculate the quanize on colored image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    new_image = [[[0 for _ in range(len(image[0][0]))] for _ in range(
        len(image[0]))]for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(len(image[0][0])):
                new_image[i][j][k] = round(math.floor(
                    image[i][j][k]*N/256)*255/(N-1))
    return new_image

# A function that checking if the RGB2grayscale's input is corect


def RGB2grayscale_main(image, message):
    if type(image[0][0]) == int:
        print("The image is already grayscale")
    else:
        image = RGB2grayscale(image)
    return image

# A function that checking if the kernel's input is corect


def blur_main(image, message):
    kernel_size = input("Please enter a kernel's size")
    k = []
    for c in kernel_size:
        k.append(c)
    count, num = helper_method(0, len(kernel_size), k)
    if count == len(kernel_size) and int(num) % 2 == 1 and kernel_size.find('.') == -1 and int(num) > 0:
        if type(image[0][0]) == int:
            image = apply_kernel(
                image, blur_kernel(int(kernel_size)))
        else:
            list1 = []
            image = separate_channels(image)
            for list in image:
                list1.append(apply_kernel(
                    list, (blur_kernel(int(kernel_size)))))
            image = combine_channels(list1)
    else:
        print("The value isn't corect {}".format(MESSAGE))
    return image

# A helper method that checking if the given string contain numbers


def helper_method(s, param, list1):
    count = 0
    num = ''
    numbers = '0123456789'
    for i in range(s, param):
        for j in numbers:
            if list1[i] == j:
                count += 1
                num += str(j)
                break
    return count, num

# A function that checking if the resize's value is corect


def resize_main(image):
    values = input("Please enter two numbers with the sign ',' between them")
    index1 = values.find(',')
    if index1 != -1:
        count, num1 = helper_method(0, index1, values)
        count1, num2 = helper_method(index1+1, len(values), values)
        if count1 == index1 and count == len(values)-index1-1 and int(num1) > 1 and int(num2) > 1:
            if type(image[0][0]) == int:
                image = resize(image, int(num1), int(num2))
            else:
                image = separate_channels(image)
                list1 = []
                for l in image:
                    list1.append(resize(l, int(num1), int(num2)))
                image = combine_channels(list1)
        else:
            print("The numbers aren't corect {}".format(MESSAGE))
    return image

# A function that checking if the rotate's side input is corect


def rotate_main(image, message):
    side = input("Please enter which side to rotate the image, R/L")
    if side == 'R' or side == 'L':
        image = rotate_90(image, side)
    else:
        print(
            "The value isn't corect or the format isn't corect {}".format(MESSAGE))
    return image

# A function that checking if the edges's input is corect


def edges_main(image, message):
    edges = input("Please enter three numbers with ',' between them")
    text = ("The numbers aren't corect or the format isn't corect {}".format(MESSAGE))
    index = ''
    count = 0
    for i in range(len(edges)):
        if edges[i] == ',':
            index += str(i)
            count += 1
    if count == 2:
        a, num1 = helper_method(0, int(index[0]), edges)
        b, num2 = helper_method(
            int(index[0])+1, int(index[1]), edges)
        c, num3 = helper_method(
            int(index[1])+1, len(edges), edges)
        if a == int(index[0]) and b == int(index[1])-int(index[0])-1 and c == int(len(edges)-int(index[1])-1):
            if type(image[0][0]) == list:
                image = get_edges(RGB2grayscale(image),
                                  int(num1), int(num2), int(num3))
            else:
                image = get_edges(
                    image, int(num1), int(num2), int(num3))
        else:
            print(text)
    else:
        print(text)
    return image


# A function that checking if the number of shades is corect


def quantzie_main(image, message):
    shades = input("Please enter the number of shades you want")
    list1 = []
    for i in range(len(shades)):
        list1.append(shades[i])
    count, b = helper_method(0, len(list1), list1)
    if count == len(shades) and int(shades) > 1:
        if type(image[0][0]) == list:
            image = separate_channels(image)
            image = quantize_colored_image(image, int(shades))
            image = combine_channels(image)
        else:
            images = quantize(image, shades)
    else:
        print("The number of shades isnt corect {}".format(MESSAGE))
    return image


if __name__ == '__main__':
    args = sys.argv
    image = load_image(args[1])
    MESSAGE = ("Please choose from the next functions:\n1. RGB2grayscale\n2. blurring image\n3. resize\n4. rotate 90\n5. edges\n6. quantize\n7. show the image\n8. exit")
    user_input = 0
    while user_input != 8:
        user_input = input(MESSAGE)
        if user_input == '1':
            image = RGB2grayscale_main(image, MESSAGE)
        elif user_input == '2':
            image = blur_main(image, MESSAGE)
        elif user_input == '3':
            image = resize_main(image)
        elif user_input == '4':
            image = rotate_main(image, MESSAGE)
        elif user_input == '5':
            image = edges_main(image, MESSAGE)
        elif user_input == '6':
            image = quantzie_main(image, MESSAGE)
        elif user_input == '7':
            show_image(image)
        elif user_input == '8':
            break
    save_image(image, "./edited.png")
