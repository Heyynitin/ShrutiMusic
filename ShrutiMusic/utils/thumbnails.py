import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

async def gen_thumb(thumbnail, title, duration, views):

    if len(title) > 40:
        title = title[:37] + "..."

    response = requests.get(thumbnail)
    img = Image.open(BytesIO(response.content)).convert("RGB")

    # Background blur
    background = img.resize((1280,720))
    background = background.filter(ImageFilter.GaussianBlur(25))

    # Center thumbnail
    small = img.resize((420,320))
    background.paste(small,(430,180))

    draw = ImageDraw.Draw(background)

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",60)
        small_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",35)
        watermark_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf",28)
    except:
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        watermark_font = ImageFont.load_default()

    # Title
    draw.text((200,540),f"{title}",fill="white",font=title_font)

    # Duration
    draw.text((200,620),f"Duration : {duration}",fill="white",font=small_font)

    # Views
    draw.text((200,670),f"Views : {views}",fill="white",font=small_font)

    # Watermark
    draw.text((1080,690),"Eryx Music",fill="white",font=watermark_font)

    final = "final.png"
    background.save(final)

    return final