import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as color
import extcolors
from PIL import Image
import os

matplotlib.use('Agg')

def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # convert RGB to HEX code
    df_color_up = [color.rgb2hex((int(i.split(", ")[0].replace("(", ""))/255,
                           int(i.split(", ")[1])/255,
                           int(i.split(", ")[2].replace(")", ""))/255)) for i in df_rgb]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
    return df


def exact_color(input_image, resize, tolerance, zoom):
    # background
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)

    # resize
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((output_width, hsize), Image.ANTIALIAS)
        resize_name =  input_image
        img.save(resize_name)
    else:
        resize_name = input_image

    # crate dataframe
    img_url = resize_name
    colors_x = extcolors.extract_from_path(img_url, tolerance=tolerance, limit=13)
    df_color = color_to_df(colors_x)

    # annotate text
    list_color = list(df_color['c_code'])
    fig, (ax) = plt.subplots(1, figsize=(160, 120), dpi=10)

    # color palette
    x_posi, y_posi, y_posi2 = 160, -170, -170
    for c in list_color:
        if list_color.index(c) <= 5:
            y_posi += 180
            rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor=c)
            ax.add_patch(rect)
            ax.text(x=x_posi + 400, y=y_posi + 100, s=c, fontdict={'fontsize': 190})
        else:
            y_posi2 += 180
            rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor=c)
            ax.add_artist(rect)
            ax.text(x=x_posi + 1400, y=y_posi2 + 100, s=c, fontdict={'fontsize': 190})

    fig.set_facecolor('white')
    ax.axis('off')
    bg = plt.imread('bg.png')
    plt.imshow(bg)
    plt.show()
    fig.savefig("static/uploads/palette_result.png")
