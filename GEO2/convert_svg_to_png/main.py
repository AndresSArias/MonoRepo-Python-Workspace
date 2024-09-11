from PIL import Image, ImageDraw
import svgwrite

def create_svg(filename):
    dwg = svgwrite.Drawing(filename, profile='tiny')
    dwg.add(dwg.circle(center=(50, 50), r=40, stroke=svgwrite.rgb(10, 10, 16, '%'), fill='red'))
    dwg.save()

def convert_svg_to_png(svg_filename, png_filename):
    image = Image.new("RGB", (100, 100), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([20, 20, 80, 80], fill="blue", outline="black")
    image.save(png_filename)



def main():
    svg_filename = "static/SVG_logo.svg"
    png_filename = "static/PNG_logo.png"

    create_svg(svg_filename)
    convert_svg_to_png(svg_filename, png_filename)

if __name__ == "__main__":
    print("Bienvenido al convertidor de SVG to PNG")
    main()
    print("Conversión exitosa")