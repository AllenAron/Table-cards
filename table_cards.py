from PIL import Image, ImageDraw, ImageFont # type: ignore

# Load your card template
TEMPLATE_PATH = "local/bordslappar.png"
OUTPUT_FOLDER = "local/output_cards/"
FONT_PATH = "arial.ttf"  # Update with the path to your desired font

# Font sizes
NAME_FONT_SIZE = 90
TITLE_FONT_SIZE = 50

# Paper sizes (mm)
A4_PAPER_WIDTH = 297
A4_PAPER_HEIGHT = 420
CARD_WIDTH = 70

# Resolution (pixels/mm)
RESOLUTION = 30


def create_card(name, title, output_path):
    # Open the template
    template = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(template)
    image_width, image_height = template.size
    center = [image_width // 2, image_height // 2]
    
    # Load fonts
    name_font = ImageFont.truetype(FONT_PATH, NAME_FONT_SIZE)
    title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)

    # Measure text width and height for centering
    name_width = draw.textlength(name, font=name_font)
    name_height = NAME_FONT_SIZE
    title_width = draw.textlength(title, font=title_font)
    title_height = TITLE_FONT_SIZE

    k = 0
    while name_width > image_width:
        name_font = ImageFont.truetype(FONT_PATH, NAME_FONT_SIZE - k*20)
        name_width = draw.textlength(name, font=name_font)
        k += 1

    k = 0
    while title_width > image_width:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE - k*20)
        title_width = draw.textlength(title, font=title_font)
        k += 1

    # Add text to the card
    # Adjust the positions (x, y) as needed for your template
    name_position = ((image_width - name_width) // 2, (image_height - name_height) // 2 - image_height // 20)
    title_position = ((image_width - title_width) // 2, (image_height + title_height) // 2)# + image_height // 20)

    draw.text(name_position, name, font=name_font, fill="black")
    draw.text(title_position, title, font=title_font, fill="gray")

    # Save the output
    template.save(output_path)
    return template

def create_print(cards_list):
    image_width, image_height = cards_list[0].size
    card_height_width_ratio = image_height / image_width

    ## Resolution (pixels/mm)
    resolution = image_width // CARD_WIDTH

    nbr_cards_horizontal = A4_PAPER_WIDTH // CARD_WIDTH
    nbr_cards_vertical = int(A4_PAPER_HEIGHT // (CARD_WIDTH*card_height_width_ratio))

    A4_image_width = A4_PAPER_WIDTH*resolution
    A4_image_height = A4_PAPER_HEIGHT*resolution

    A4_image = Image.new(mode='RGB', size=(A4_image_width, A4_image_height))

    i = 0
    for r in range(nbr_cards_vertical):
        for c in range(nbr_cards_horizontal):
            if i > len(cards_list) - 1:
                break
            A4_image.paste(cards_list[i], (c * A4_image_width // nbr_cards_horizontal, r * A4_image_height // nbr_cards_vertical))
            i += 1

    A4_image.save('local/output_cards/print.pdf')

def main(csv_file):
    cards_list = []
    with open(csv_file, newline='', encoding='UTF-8-SIG') as f:
        for line in f.readlines():
            line = line[:-2]
            name, title = line.split(',')
            cards_list.append(create_card(name, title, f"{OUTPUT_FOLDER}{name.replace(' ', '_')}.png"))
    create_print(cards_list)

main('local/table_cards.csv')