from PIL import Image, ImageDraw, ImageFont

# Define the logo parameters
width, height = 200, 200
background_color = (255, 255, 255, 0)  # Transparent background

# Create an image with a transparent background
image = Image.new('RGBA', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Define the gradient colors
color1 = (102, 51, 153)  # #663399
color2 = (255, 64, 0)    # #ff4000

# Draw the gradient
for i in range(height):
    r = int(color1[0] + (color2[0] - color1[0]) * i / height)
    g = int(color1[1] + (color2[1] - color1[1]) * i / height)
    b = int(color1[2] + (color2[2] - color1[2]) * i / height)
    draw.line([(0, i), (width, i)], fill=(r, g, b))

# Load a font
try:
    font = ImageFont.truetype("arial.ttf", 150)
except IOError:
    font = ImageFont.load_default()

# Calculate the position for centering the text
text = "W"
text_width, text_height = font.font.getsize(text)
text_width = text_width[0] * 20
text_height = text_height[1] * 20
print(text_width, text_height)
print(width, height)
x = (width - text_width) / 2
y = (height - text_height) / 2

# Draw the text with the gradient fill
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

# Save the image in different formats
image.save('logo.png')
image.convert("RGB").save('logo.jpg')
image.save('logo.ico', format='ICO')

print("Saved logo.png, logo.jpg, and logo.ico")
