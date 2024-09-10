from flat import document, shape, rgb, rgba
import random
import os

# Constants
NUM_AVATARS = 23
IMAGE_SIZE = (100, 100)
OUTPUT_DIR = "avatars"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Colors
SKIN_TONES = [rgb(255, 224, 189), rgb(242, 194, 154), rgb(224, 172, 105), rgb(198, 134, 66), rgb(141, 85, 36)]
HAIR_COLORS = [rgb(0, 0, 0), rgb(94, 54, 29), rgb(255, 255, 255), rgb(170, 112, 69), rgb(210, 180, 140)]
CLOTHES_COLORS = [rgb(255, 0, 0), rgb(0, 255, 0), rgb(0, 0, 255), rgb(255, 255, 0), rgb(255, 165, 0), rgb(128, 0, 128)]

# Functions to draw features
def draw_face(pen, x, y, size, color):
    pen.circle(x, y, size).color(color).stroke()

def draw_eyes(pen, x, y, size):
    eye_size = size / 10
    pen.circle(x - eye_size * 2, y - eye_size, eye_size).color(rgb(255, 255, 255)).stroke()
    pen.circle(x + eye_size * 2, y - eye_size, eye_size).color(rgb(255, 255, 255)).stroke()
    pen.circle(x - eye_size * 2, y - eye_size, eye_size / 2).color(rgb(0, 0, 0)).fill()
    pen.circle(x + eye_size * 2, y - eye_size, eye_size / 2).color(rgb(0, 0, 0)).fill()

def draw_mouth(pen, x, y, size):
    pen.line(x - size / 4, y + size / 4, x + size / 4, y + size / 4).color(rgb(0, 0, 0)).stroke()

def draw_hair(pen, x, y, size, color):
    pen.line(x - size / 2, y - size / 2, x + size / 2, y - size / 2).color(color).stroke()

def draw_clothes(pen, x, y, size, color):
    pen.rectangle(x - size / 2, y, size, size).color(color).fill()

def create_avatar(index):
    d = document(IMAGE_SIZE[0], IMAGE_SIZE[1], 'mm')
    page = d.addpage()
    pen = page.place(IMAGE_SIZE[0], IMAGE_SIZE[1])  # Corrected the place method call

    # Randomly select colors and features
    skin_color = random.choice(SKIN_TONES)
    hair_color = random.choice(HAIR_COLORS)
    clothes_color = random.choice(CLOTHES_COLORS)

    # Draw the avatar
    face_x, face_y, face_size = 50, 40, 30
    draw_face(pen, face_x, face_y, face_size, skin_color)
    draw_eyes(pen, face_x, face_y, face_size)
    draw_mouth(pen, face_x, face_y, face_size)
    draw_hair(pen, face_x, face_y - face_size / 2, face_size, hair_color)
    draw_clothes(pen, face_x, face_y + face_size / 2, face_size, clothes_color)

    d.save(os.path.join(OUTPUT_DIR, f"avatar_{index}.svg"))

# Generate and save avatars
for i in range(NUM_AVATARS):
    create_avatar(i)

print(f"Generated {NUM_AVATARS} avatars in the '{OUTPUT_DIR}' directory.")
