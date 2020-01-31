#!/usr/bin/env python3

import lxml as l
import lxml.etree as et
from argparse import ArgumentParser
import sys

def elem(tag, **kwargs):
    attribs = {}
    for k,v in kwargs.items():
        attribs[k.replace("_", "-")] = str(v)
    return et.Element(tag, attrib=attribs)

def render_board(
    cell_size = 2.0,
    cell_border = .5,
    outer_border = .75,
    board_rows = 9,
    board_columns = 12,
    stroke = .05,
    corner_radius_ratio = .15,
    text_scale=.4,
    text_pad=.2, #height of text relative to cell
    font="04b"
):
    board_height = board_rows * cell_size \
                    + (board_rows - 1) * cell_border \
                    + outer_border * 2
    board_width = board_columns * cell_size \
                    + (board_columns - 1) * cell_border \
                    + outer_border * 2

    corner_radius = cell_size * corner_radius_ratio

    document_height = board_height * 3 + 2 * outer_border

    style="fill: none; stroke: black; stroke-width: {stroke}".format(**locals())

    def piece_outlines(shape_style=style):
        pieces = elem("g")
        for row in range(board_rows):
            for col in range(board_columns):
                pieces.append(elem("rect",
                    x=col*cell_size+col*cell_border,
                    y=row*cell_size+row*cell_border,
                    height=cell_size,
                    width=cell_size,
                    rx=corner_radius,
                    style=shape_style
                ))
        return pieces

    def piece_labels():
        labels = elem("g")
        text_height = text_scale*cell_size
        for row in range(board_rows):
            for col in range(board_columns):
                letter_label = elem(
                    "text",
                    x=col*cell_size+col*cell_border+text_pad,
                    y=row*cell_size+row*cell_border+text_height+.5*text_pad,
                    font_size=text_height,
                    font_family="{font}".format(font=font),
                    #text_anchor="left",
                    fill="red",
                    dominant_baseline="top"
                )
                letter_label.text = str(chr(ord('A')+row))
                number_label = elem(
                    "text",
                    x=col*cell_size+col*cell_border+cell_size-text_pad,
                    y=row*cell_size+row*cell_border+cell_size-text_pad,
                    font_size=text_height,
                    font_family="{font}".format(font=font),
                    text_anchor="end",
                    fill="red",
                    #dominant_baseline="bottom"
                )
                number_label.text=str(col+1)
                labels.append(letter_label)
                labels.append(number_label)
        return labels

    def board_outline():
        return elem("rect", width=board_width, height=board_height, rx=corner_radius, style=style)

    def root_node():
        return elem(
            "svg",
            height= "{0}cm".format(board_height),
            width= "{0}cm".format(board_width),
            viewBox= "0 0 {board_width} {board_height}".format(**locals()),
            xmlns="http://www.w3.org/2000/svg",
            version="1.1",
            baseProfile="full"
        )


    lower_board = et.Element("g")
    lower_board.append(board_outline())
    lower_labels = elem("g", transform="translate({x} {y})".format(x=outer_border, y=outer_border))
    lower_labels.append(piece_labels())
    #if you want engraved outlines of the piece shapes
    #lower_labels.append(piece_outlines("fill: none; stroke: red; stroke-width: {stroke}".format(**locals())))
    lower_board.append(lower_labels)

    upper_board = elem("g")
    upper_board.append(board_outline())
    upper_board_pieces = elem("g", transform="translate({x} {y})".format(x=outer_border, y=outer_border))
    upper_board_pieces.append(piece_outlines())
    #Don't actually want these on the upper board cutout because
    #the holes are going to get discarded
    #upper_board_pieces.append(piece_labels())
    upper_board.append(upper_board_pieces)

    pieces = elem("g", transform="translate({x} {y})".format(x=outer_border, y=outer_border))
    pieces.append(piece_outlines())
    pieces.append(piece_labels())


    for node, filename in [(upper_board, 'upper.svg'), (lower_board, 'lower.svg'), (pieces, 'pieces.svg')]:
        root = root_node()
        root.append(node)
        document = et.ElementTree(root)
        with open(filename, 'wb') as f:
            document.write(f, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    render_board()
