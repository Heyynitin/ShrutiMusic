import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO


async def gen_thumb(thumbnail, title, userid, theme, ctitle, duration, views):

    if len(title) > 45:
        title = title[:42] + "..."

    try:
        response = requests.get(thumbnail)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    except:
        img = Image.new("RGB", (1280, 720), "black")

    # ===== Background Blur =====
    background = img.resize((1280, 720))
    background = background.filter(ImageFilter.GaussianBlur(35))

    # ===== Dark Overlay =====
    overlay = Image.new("RGBA", background.size, (0, 0, 0, 120))
    background = Image.alpha_composite(background.convert("RGBA"), overlay)

    # ===== Thumbnail Card =====
    thumb = img.resize((360, 360))
    background.paste(thumb, (120, 180))

    draw = ImageDraw.Draw(background)

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 55)
        info_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 35)
        watermark_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        watermark_font = ImageFont.load_default()

    # ===== Song Title =====
    draw.text((540, 220), title, fill="white", font=title_font)

    # ===== Duration =====
    draw.text((540, 340), f"Duration : {duration}", fill="white", font=info_font)

    # ===== Views =====
    draw.text((540, 400), f"Views : {views}", fill="white", font=info_font)

    # ===== Requested =====
    draw.text((540, 460), f"Requested By : {userid}", fill="white", font=info_font)

    # ===== Fake Spotify Progress Bar =====
    bar_x1 = 540
    bar_y1 = 520
    bar_x2 = 1100
    bar_y2 = 540

    draw.rectangle((bar_x1, bar_y1, bar_x2, bar_y2), fill=(80, 80, 80))
    draw.rectangle((bar_x1, bar_y1, bar_x1 + 250, bar_y2), fill=(30, 215, 96))

    # ===== Watermark =====
    draw.text((1080, 680), "Eryx Music", fill="white", font=watermark_font)

    final = "final.png"
    background.convert("RGB").save(final)

    return final