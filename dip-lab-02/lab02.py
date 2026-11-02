"""Digital Image Processing Lab 02 — image inspection and basic transformations.

Usage:
    python lab02.py input_image.jpg
    python lab02.py input_image.png

Choose your own color image of at least 300 x 300 pixels.
"""

from pathlib import Path
import sys

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input_image.jpg")
if not IMAGE_PATH.is_absolute():
    IMAGE_PATH = PROJECT_DIR / IMAGE_PATH


def save_figure(fig, filename):
    path = PROJECT_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight")
    print(f"Saved figure: {path.name}")


# Step 2: Load and validate the personally selected image.
image = cv.imread(str(IMAGE_PATH), cv.IMREAD_COLOR)
if image is None:
    raise FileNotFoundError(
        f"Could not load '{IMAGE_PATH}'. Put your JPG/PNG in the project folder "
        "and run: python lab02.py your_image.jpg"
    )

height, width, channels = image.shape
if height < 300 or width < 300:
    raise ValueError(f"Image must be at least 300 x 300 pixels; got {width} x {height}.")

print("\n=== Step 2: Image Loading ===")
print("Input image:", IMAGE_PATH.name)
print("Image shape (height, width, channels):", image.shape)
print("Image data type:", image.dtype)

# Step 3: Inspect image properties and pixels (OpenCV stores BGR).
print("\n=== Step 3: Image Inspection ===")
print("Height:", height)
print("Width:", width)
print("Number of channels:", channels)
print("Top-left pixel [row=0, column=0] (BGR):", image[0, 0].tolist())
center_row, center_col = height // 2, width // 2
print(f"Center pixel [row={center_row}, column={center_col}] (BGR):", image[center_row, center_col].tolist())
print("Global minimum intensity:", int(image.min()))
print("Global maximum intensity:", int(image.max()))
for channel_index, channel_name in enumerate(("Blue", "Green", "Red")):
    channel = image[:, :, channel_index]
    print(f"{channel_name} channel minimum: {int(channel.min())}; maximum: {int(channel.max())}")

# Step 4: Convert BGR to RGB and split color channels.
rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
red, green, blue = cv.split(rgb)
center_rgb = rgb[center_row, center_col]
center_hex = "#{:02X}{:02X}{:02X}".format(*(int(v) for v in center_rgb))
print("\n=== Step 4: Color Channels ===")
print("Center pixel (RGB):", center_rgb.tolist())
print("Center pixel HEX:", center_hex)

fig_channels, axes = plt.subplots(2, 3, figsize=(13, 8))
views = [
    (rgb, "RGB (correct colors)", None),
    (red, "Red channel", "gray"),
    (green, "Green channel", "gray"),
    (blue, "Blue channel", "gray"),
    (gray, "Grayscale", "gray"),
    (image, "BGR displayed as RGB (incorrect colors)", None),
]
for ax, (data, title, cmap) in zip(axes.flat, views):
    ax.imshow(data, cmap=cmap, vmin=0 if cmap else None, vmax=255 if cmap else None)
    ax.set_title(title, fontsize=11)
    ax.axis("off")
fig_channels.suptitle("Color Conversion and Channel Separation", fontsize=15)
fig_channels.tight_layout()
save_figure(fig_channels, "color_channels.png")

# Step 5: Exact 100x100 crop, resize to 200x200, convert back to BGR and save.
y_start = (height - 100) // 2
x_start = (width - 100) // 2
crop_rgb = rgb[y_start:y_start + 100, x_start:x_start + 100]
resized_rgb = cv.resize(crop_rgb, (200, 200), interpolation=cv.INTER_LINEAR)
print("\n=== Step 5: Crop, Resize, and Save ===")
print(f"Crop coordinates: rows {y_start}:{y_start + 100}, columns {x_start}:{x_start + 100}")
print("Crop shape:", crop_rgb.shape)
print("Resized crop shape:", resized_rgb.shape)
resized_bgr = cv.cvtColor(resized_rgb, cv.COLOR_RGB2BGR)
saved = cv.imwrite(str(PROJECT_DIR / "resized_crop.png"), resized_bgr)
print("cv.imwrite() saved resized_crop.png successfully:", saved)
if not saved:
    raise OSError("Could not save resized_crop.png")

fig_crop, axes_crop = plt.subplots(1, 3, figsize=(13, 4.5))
for ax, data, title in zip(
    axes_crop,
    (rgb, crop_rgb, resized_rgb),
    ("Original RGB", "100 x 100 crop", "200 x 200 resized crop"),
):
    ax.imshow(data)
    ax.set_title(title)
    ax.axis("off")
fig_crop.tight_layout()
save_figure(fig_crop, "crop_resize_comparison.png")

# Step 6: Grayscale histogram (256 bins over [0, 256)).
flat_gray = gray.ravel()
fig_hist, ax_hist = plt.subplots(figsize=(9, 5))
ax_hist.hist(flat_gray, bins=256, range=(0, 256), color="#475569")
ax_hist.set_title("Grayscale Intensity Histogram")
ax_hist.set_xlabel("Pixel intensity (0–255)")
ax_hist.set_ylabel("Pixel frequency")
ax_hist.set_xlim(0, 256)
fig_hist.tight_layout()
save_figure(fig_hist, "grayscale_histogram.png")

mean_intensity = float(np.mean(gray))
dark_pct = float(np.mean(gray < 85) * 100)
mid_pct = float(np.mean((gray >= 85) & (gray < 171)) * 100)
bright_pct = float(np.mean(gray >= 171) * 100)
if dark_pct > 50:
    assessment = "mainly dark"
elif bright_pct > 50:
    assessment = "mainly bright"
else:
    assessment = "balanced or mixed in brightness"
print("\n=== Step 6: Histogram Interpretation ===")
print(f"Mean grayscale intensity: {mean_intensity:.2f} / 255")
print(f"Dark (0–84): {dark_pct:.1f}% | Midtone (85–170): {mid_pct:.1f}% | Bright (171–255): {bright_pct:.1f}%")
print(f"Interpretation: The image is {assessment} based on its grayscale intensity distribution.")
print("A histogram shows how frequently intensities occur, but not their spatial positions.")

# Step 7: 8-bit gradient and 1-, 2-, and 4-bit quantization.
gradient = np.tile(np.arange(256, dtype=np.uint8), (60, 1))


def quantize_to_bits(arr, bits):
    levels = 2 ** bits
    indices = (arr.astype(np.uint16) * levels) // 256
    return ((indices * 255) // (levels - 1)).astype(np.uint8)


gradient_1 = quantize_to_bits(gradient, 1)
gradient_2 = quantize_to_bits(gradient, 2)
gradient_4 = quantize_to_bits(gradient, 4)
print("\n=== Step 7: Bit Depth ===")
for label, grad in (("8-bit", gradient), ("1-bit", gradient_1), ("2-bit", gradient_2), ("4-bit", gradient_4)):
    print(f"{label} unique intensity count:", len(np.unique(grad)))
print("Resolution is the number of pixels (width x height); bit depth is the number of bits used to represent each pixel intensity.")

fig_bits, axes_bits = plt.subplots(4, 1, figsize=(11, 6))
for ax, grad, title in zip(
    axes_bits,
    (gradient, gradient_1, gradient_2, gradient_4),
    ("8-bit: 256 levels", "1-bit: 2 levels", "2-bit: 4 levels", "4-bit: 16 levels"),
):
    ax.imshow(grad, cmap="gray", vmin=0, vmax=255, aspect="auto")
    ax.set_title(title, loc="left")
    ax.axis("off")
fig_bits.suptitle("Grayscale Bit-Depth Comparison")
fig_bits.tight_layout()
save_figure(fig_bits, "bit_depth_comparison.png")

print("\nLAB 02 COMPLETED SUCCESSFULLY. Close the figure windows to return to the terminal.")
plt.show()
