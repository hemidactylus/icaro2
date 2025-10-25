import drawsvg as draw

DOTS_PER_CELL = 30
SEGMENT_WIDTH = 4
BORDER_WIDTH = 10
GUTTER = 5  # half of border width for neat bordering

def render_svg(l):
    n=len(l) - 1
    m=len(l[0]) - 1
    w = n * DOTS_PER_CELL
    h = m * DOTS_PER_CELL
    d = draw.Drawing(w + 2 * GUTTER, h + 2 * GUTTER, origin=(0, 0))

    # Framing rectangle
    d.append(
        draw.Rectangle(
            GUTTER, GUTTER,
            w, h,
            stroke_width=BORDER_WIDTH,
            fill="none",
            stroke="black",
        ),
    )

    for i in range(n + 1):
        x0 = i * DOTS_PER_CELL + GUTTER
        x1 = x0 + DOTS_PER_CELL
        for j in range(m + 1):
            y0 = GUTTER + h - j * DOTS_PER_CELL
            y1 = y0 - DOTS_PER_CELL
            if i>0 and i < n and l[i][j][1]:
                # vertical line
                d.append(draw.Line(
                    x0, y0, x0, y1,
                    stroke="black",
                    stroke_linecap="round",
                    stroke_width=SEGMENT_WIDTH,
                ))
            if j > 0 and j < m and l[i][j][0]:
                # horizontal line
                d.append(draw.Line(
                    x0, y0, x1, y0,
                    stroke="black",
                    stroke_linecap="round",
                    stroke_width=SEGMENT_WIDTH,
                ))

    return d
