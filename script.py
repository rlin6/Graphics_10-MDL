import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    comm = ["push", "pop", "move", "rotate", "scale", "box", "sphere", "torus", "line", "save", "display"]
    
    print(symbols)
    for command in commands:
        print(command)
        
        if command["op"] in comm:
            op = command["op"]
            args = command["args"]

            if op in ["sphere", "torus", "box"]:
                if command["constants"]:
                    reflect = command["constants"]
                else:
                    reflect = ".white"

            if op == "push":
                stack.append([x[:] for x in stack[-1]])

            if op == "pop":
                stack.pop()

            elif op == "move":
                y = make_translate(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult(stack[-1], y)
                stack[-1] = [ x[:] for x in y]

            elif op == "rotate":
                theta = float(args[1]) * (math.pi / 180)
                if args[0] == "x":
                    y = make_rotX(theta)
                elif args[0] == "y":
                    y = make_rotY(theta)
                else:
                    y = make_rotZ(theta)
                matrix_mult(stack[-1], y)
                stack[-1] = [ x[:] for x in y]

            elif op == "scale":
                y = make_scale(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult(stack[-1], y)
                stack[-1] = [ x[:] for x in y]

            elif op == "box":
                add_box(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []

            elif op == "sphere":
                add_sphere(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []

            elif op == "torus":
                add_torus(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []

            elif op == "line":
                add_edge(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                matrix_mult(stack[-1], edges)
                draw_lines(edges, screen, zbuffer, [255, 255, 255])
                edges = []

            elif op == "save":
                fn = args[0] + ".png"
                save_extension(screen, fn)

            elif op == "display":
                display(screen)
