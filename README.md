# Acquire Board
Renders svg files for cutting out a board and tiles for the board game Acquire.

The upper and lower board pieces are intended to be cemented together.

The upper should be made from a material thinner than the tiles so that you can get the tiles in and out of the board once it's assembled

You'll need to furnish your own play money, stock certificates, and corporation markers.

## Running

```sh
#maybe you want to do this in a virtualenv like a pro?
pip3 install -r requirements.txt

#will create 3 files
python3 render.py
```

## Other thoughts
- I found the font on dafont.com - author's homepage is here: http://www.04.jp.org/
    - if you want to use a different font, find the font option in the main function and change to whatever
- I ordered acrylic laser cuts from ponoko.com - if you use them, you'll need to convert the text to paths.  I used inkscape's "object to path" functionalty for this.
- The blue tile outlines on the lower board are indended to be etched, not cut.  I added them so that it would be easy to leave the laser mask on the lower part while gluing the lower and upper boards together.
    - If you don't want them, you can comment out where they're added to the lower board group.
