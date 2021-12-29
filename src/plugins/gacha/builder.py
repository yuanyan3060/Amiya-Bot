from PIL import Image, ImageDraw
from src.config import pathConfig
from ..util.image import read_pil_img


async def create_gacha_image(result: list):
    image = await read_pil_img(pathConfig.images / 'gacha/bg.png')
    draw = ImageDraw.ImageDraw(image)

    x = 78
    for item in result:
        if item is None:
            x += 82
            continue

        rarity = pathConfig.images / f"gacha/{item['rarity']}.png"
        if rarity.exists():
            img = await read_pil_img(rarity)
            img.convert('RGBA')
            image.paste(img, box=(x, 0), mask=img)

        portraits = pathConfig.images/f"portraits/{item['portraits']}_1.png"
        if not portraits.exists():
            if 'temp_portraits' in item and item['temp_portraits']:
                portraits = item['temp_portraits']

        if os.path.exists(portraits):
            img = Image.open(portraits).convert('RGBA')

            radio = 252 / img.size[1]

            width = int(img.size[0] * radio)
            height = int(img.size[1] * radio)

            step = int((width - 82) / 2)
            crop = (step, 0, width - step, height)

            img = img.resize(size=(width, height))
            img = img.crop(crop)
            image.paste(img, box=(x, 112), mask=img)

        draw.rectangle((x + 10, 321, x + 70, 381), fill='white')
        class_img = 'resource/images/class/%s.png' % item['class']
        if os.path.exists(class_img):
            img = Image.open(class_img).convert('RGBA')
            img = img.resize(size=(59, 59))
            image.paste(img, box=(x + 11, 322), mask=img)

        x += 82

    icon = Image.open(logo_file_white)
    icon = icon.resize(size=(30, 30))
    image.paste(icon, box=(image.size[0] - 30, 0), mask=icon)

    path = '%s/Gacha' % temp_dir
    make_folder(path)

    name = '%s.png' % datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    path = '%s/%s' % (path, name)

    x, y = image.size
    image = image.resize((int(x * 0.8), int(y * 0.8)), Image.ANTIALIAS)
    image.save(path, quality=80)

    return path
