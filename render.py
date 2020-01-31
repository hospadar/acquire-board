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
    stroke = .1,
    corner_radius_ratio = .15,
    text_scale=.4,
    text_vpad=.1 #height of text relative to cell
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

    def piece_outlines():
        pieces = elem("g")
        for row in range(board_rows):
            for col in range(board_columns):
                pieces.append(elem("rect",
                    x=col*cell_size+col*cell_border,
                    y=row*cell_size+row*cell_border,
                    height=cell_size,
                    width=cell_size,
                    rx=corner_radius,
                    style=style
                ))
        return pieces

    def piece_labels():
        labels = elem("g")
        text_height = text_scale*cell_size
        for row in range(board_rows):
            for col in range(board_columns):
                label = elem("text",
                    x=col*cell_size+col*cell_border+.5*cell_size,
                    y=row*cell_size+row*cell_border+.5*cell_size-text_vpad,
                    font_size=text_height,
                    font_family="sans-serif",
                    text_anchor="middle",
                    dominant_baseline="middle"
                )
                label.text="{letter}-{number}".format(letter=chr(ord('A')+row), number=col)
                labels.append(label)
        return labels

    def board_outline():
        return elem("rect", width=board_width, height=board_height, rx=corner_radius, style=style)


    doc = elem("svg",
        height= "{0}cm".format(document_height),
        width= "{0}cm".format(board_width),
        viewBox= "0 0 {board_width} {document_height}".format(**locals()),
        xmlns="http://www.w3.org/2000/svg",
        version="1.1",
        baseProfile="full"
    )

    lower_board = et.Element("g")
    lower_board.append(board_outline())
    lower_labels = elem("g", transform="translate({x} {y})".format(x=outer_border, y=outer_border))
    lower_labels.append(piece_labels())
    lower_board.append(lower_labels)

    doc.append(lower_board)

    upper_board = elem("g", transform="translate({x} {y})".format(x=0, y=board_height+outer_border))
    upper_board.append(board_outline())
    upper_board_pieces = elem("g", transform="translate({x} {y})".format(x=outer_border, y=outer_border))
    upper_board_pieces.append(piece_outlines())
    #Don't actually want these on the upper board cutout because
    #the holes are going to get discarded
    #upper_board_pieces.append(piece_labels())
    upper_board.append(upper_board_pieces)

    pieces = elem("g", transform="translate({x} {y})".format(x=outer_border, y=board_height*2 + outer_border*2))
    pieces.append(piece_outlines())
    pieces.append(piece_labels())

    doc.append(pieces)


    doc.append(upper_board)


    #print("<!")
    sys.stdout.buffer.write(et.tostring(doc, encoding='utf-8', pretty_print=True))


if __name__ == '__main__':
    render_board()
