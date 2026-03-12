import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO


async def gen_thumb(thumbnail, title, *args):

    duration = "Unknown"
    views = "Unknown"
    userid = "User"

    if len(args) >= 1:
        userid = str(args[0])
    if len(args) >= 3:
        duration = str(args[2])
    if len(args) >= 4:
        views = str(args[3])

    if len(title) > 45:
        title = title[:42] + "..."

    try:
        response = requests.get(thumbnail)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    except:
        img = Image.new("RGB", (1280,720), "black")

    # Background Blur
    background = img.resize((1280,720))
    background = background.filter(ImageFilter.GaussianBlur(30))

    draw = ImageDraw.Draw(background)

    # Thumbnail
    thumb = img.resize((350,350))
    background.paste(thumb,(120,180))

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",55)
        info_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",35)
        watermark_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",28)
    except:
        title_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        watermark_font = ImageFont.load_default()

    # Title
    draw.text((520,220),title,fill="white",font=title_font)

    # Duration
    draw.text((520,340),f"Duration : {duration}",fill="white",font=info_font)

    # Views
    draw.text((520,400),f"Views : {views}",fill="white",font=info_font)

    # Requested
    draw.text((520,460),f"Requested By : {userid}",fill="white",font=info_font)

    # Progress Bar
    draw.rectangle((520,520,1080,540),fill=(80,80,80))
    draw.rectangle((520,520,760,540),fill=(30,215,96))

    # Watermark
    draw.text((1080,680),"Eryx Music",fill="white",font=watermark_font)

    final = "final.png"
    background.save(final)

    return final