import cairosvg

def convert_svg_to_png(svg_file, png_file):
    """
    Convierte un archivo SVG a PNG.
    
    :param svg_file: Ruta del archivo SVG de entrada.
    :param png_file: Ruta del archivo PNG de salida.
    """
    try:
        cairosvg.svg2png(url=svg_file, write_to=png_file)
        print(f"Conversión exitosa: {png_file}")
    except Exception as e:
        print(f"Error durante la conversión: {e}")



def main():
    # Ruta del archivo SVG de entrada
    svg_file = "static/SVG_logo.svg"

    # Ruta del archivo PNG de salida
    png_file = "static/PNG_logo.png"

    # Llamar a la función de conversión
    convert_svg_to_png(svg_file, png_file)

if __name__ == "__main__":
    print("Bienvenido al convertidor de SVG to PNG")
    main()
    print("Conversión exitosa")