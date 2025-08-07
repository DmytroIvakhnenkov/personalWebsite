import sys
from PIL import Image

def main():
    if len(sys.argv) < 2:
        print("Usage: python flip_image.py <input_image_path>")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        image = Image.open(input_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

    output_path = input("Enter output filename (include extension, e.g. output.webp): ").strip()
    if not output_path:
        print("No output filename given, exiting.")
        sys.exit(1)

    try:
        flipped_image.save(output_path)
        print(f"Flipped image saved as '{output_path}'")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
