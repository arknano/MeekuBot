from itertools import chain
from wand.image import Image

with Image(filename='cover2.png', ) as cover, Image(filename='template.png') as template, Image(filename='template_over.png') as template_over:
    cover.sample(width=cover.width * 5, height=cover.height * 5)
    w, h = cover.size
    cover.virtual_pixel = 'transparent'
    source_points = (
        (0, 0),
        (w, 0),
        (0, h),
        (w, h)

    )
    destination_points = (
        (208, 375),
        (630, 375),
        (208, 644),
        (630, 644)

    )
    destination_points2 = (
        (83, 201),
        (147, 182),
        (99, 286),
        (163, 270)

    )
    order = chain.from_iterable(zip(source_points, destination_points))
    arguments = list(chain.from_iterable(order))



    print(cover.width)
    print(cover.height)
    cover.distort('perspective', arguments)

    # Overlay cover onto template and save
    template.composite(cover,left=0,top=0)
    template.composite(template_over,left=0,top=0)
    template.save(filename='result.png')