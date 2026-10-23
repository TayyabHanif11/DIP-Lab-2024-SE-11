# Digital Image Processing - Lab 01
# Python Fundamentals

# Exercise 1: Variables and Data Types
# ========================================

print("\n--- Exercise 1: Variables and Data Types ---")

width = 640
height = 480
image_name = "sample.png"
is_color = True

print("Width:", width, "| Type:", type(width))
print("Height:", height, "| Type:", type(height))
print("Image Name:", image_name, "| Type:", type(image_name))
print("Is Color:", is_color, "| Type:", type(is_color))

total_pixels = width * height
print("Total Pixels:", total_pixels)


# Exercise 2: if, elif, and else
# ========================================

print("\n--- Exercise 2: Conditions ---")

intensities = [-1, 0, 127, 128, 255, 256]

for intensity in intensities:
    if intensity < 0 or intensity > 255:
        label = "Invalid"
    elif intensity >= 128:
        label = "Bright pixel"
    else:
        label = "Dark pixel"

    print("Intensity:", intensity, "->", label)


# Exercise 3: for and while Loops
# ========================================

print("\n--- Exercise 3: Loops ---")

pixels = [20, 130, 255]

for pixel in pixels:
    if pixel >= 128:
        print(pixel, "-> Bright pixel")
    else:
        print(pixel, "-> Dark pixel")

print("While Loop:")

counter = 0
while counter < 3:
    print(counter)
    counter += 1


# Exercise 4: Functions
# ========================================

print("\n--- Exercise 4: Functions ---")

def is_bright(pixel, threshold=128):
    return pixel >= threshold

print("is_bright(127):", is_bright(127))
print("is_bright(128):", is_bright(128))
print("is_bright(200, 210):", is_bright(200, 210))


# Exercise 5: Lists and Tuples
# ========================================

print("\n--- Exercise 5: Lists and Tuples ---")

pixels = [0, 128, 255]

print("First Pixel:", pixels[0])

pixels[1] = 150
pixels.append(64)

print("Updated Pixels:", pixels)
print("List Length:", len(pixels))

size = (640, 480)
width, height = size

print("Width:", width)
print("Height:", height)

# Lists are mutable, so their items can be changed.
# Tuples are immutable, so their items cannot be changed.


# Exercise 6: Dictionaries and Sets
# ========================================

print("\n--- Exercise 6: Dictionaries and Sets ---")

image = {"width": 640, "height": 480}

image["mode"] = "RGB"

print("Image Width:", image["width"])
print("Image Mode:", image["mode"])

labels = ["cat", "dog", "cat", "bird"]

unique_labels = set(labels)

print("Unique Labels:", unique_labels)
print("Number of Unique Labels:", len(unique_labels))
