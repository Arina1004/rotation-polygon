from tkinter import *
import math
from variables import *

root = Tk()


def set_state(new_state):
    global state, last_state

    last_state, state = state, new_state


def get_figure(point):
    for polygon_id in range(len(polygons)):
        flag = polygons[polygon_id].is_intersection(point)
        if flag > -1:
            return polygon_id, flag

    return -1, -1


def key(event):
    global action

    action = 'start' if action == 'stop' else 'stop'
    print(action)


class Polygon(object):
    def __init__(self, point):
        self.points = point.copy()
        self.current_points = self.points.copy()
        self.count = len(self.current_points) // 2
        self.center_figure = -1
        self.child_offset = -1
        self.calculate_center_and_offset()
        self.angle = 0
        self.perimeter = 0
        self.lines_ids = {}
        self.points_ids = {}

        self.points_ids[0] = self.draw_vertex(point)
    def draw_vertex(self, point):
        canvas.create_oval(point[0] - 6,
                            point[1] - 6,
                            point[0] + 6,
                            point[1] + 6,
                            fill="#900C3F")


    def add_vertex(self, point):
        self.points.insert(self.count, point[0])
        self.points.append(point[1])

        if self.center_figure != -1:
            canvas.delete(self.center_figure)

        self.lines_ids[str(self.count - 1) + ' ' + str(self.count)] = canvas.create_line(point[0],
                                                                                         point[1],
                                                                                         self.points[self.count - 1],
                                                                                         self.points[self.count * 2],
                                                                                         fill="#900C3F")

        self.points_ids[self.count] = self.draw_vertex(point)

        self.count += 1

        self.current_points = self.points.copy()

        self.calculate_center_and_offset()

        self.center_figure = canvas.create_oval(self.center[0] - 3,
                                                self.center[1] - 3,
                                                self.center[0] + 3,
                                                self.center[1] + 3,
                                                fill="#FF0000")

    def set_vertex(self, id, point):
        print('DELETING ' + str(id))
        print(self.points_ids)
        print(self.lines_ids)
        self.current_points[id] = point[0]
        self.current_points[id + self.count] = point[1]

        x = self.center[0] + (point[0] - self.center[0]) * math.cos(-1 * self.angle) - (
            point[1] - self.center[1]) * math.sin(-1 * self.angle)
        y = self.center[1] + (point[0] - self.center[0]) * math.sin(-1 * self.angle) + (
            point[1] - self.center[1]) * math.cos(-1 * self.angle)

        self.points[id] = x
        self.points[id + self.count] = y

        if self.center_figure != -1:
            canvas.delete(self.center_figure)

        right_index = (id + 1) % self.count

        if right_index > id:
            left, right = id, right_index
        else:
            left, right = right_index, id

        if str(left) + ' ' + str(right) in self.lines_ids:
            canvas.delete(self.lines_ids[str(left) + ' ' + str(right)])

            self.lines_ids[str(left) + ' ' + str(right)] = canvas.create_line(self.current_points[left],
                                                                              self.current_points[left + self.count],
                                                                              self.current_points[right],
                                                                              self.current_points[right + self.count],
                                                                              fill="#900C3F")

        left_index = id - 1 if id > 0 else id - 1 + self.count

        if left_index < id:
            left2, right2 = left_index, id
        else:
            left2, right2 = id, left_index

        if str(left2) + ' ' + str(right2) in self.lines_ids:
            canvas.delete(self.lines_ids[str(left2) + ' ' + str(right2)])

            self.lines_ids[str(left2) + ' ' + str(right2)] = canvas.create_line(self.current_points[right2],
                                                                                self.current_points[right2 + self.count],
                                                                                self.current_points[left2],
                                                                                self.current_points[left2 + self.count],
                                                                                fill="#900C3F")

        canvas.delete(self.points_ids[id])
        self.points_ids[id] = self.draw_vertex(point)

        self.calculate_center_and_offset()
        self.calculate_perimeter()

        self.center_figure = canvas.create_oval(self.center[0] - 3, self.center[1] - 3,
                                                self.center[0] + 3, self.center[1] + 3,
                                                fill="#FF0000")

    def last_vertex(self):
        self.calculate_perimeter()

        self.lines_ids[str(0) + ' ' + str(self.count - 1)] = canvas.create_line(self.points[0],
                                                                                self.points[self.count],
                                                                                self.points[self.count - 1],
                                                                                self.points[self.count * 2 - 1],
                                                                                fill="#900C3F")

    def set_center(self, center):
        self.center = center.copy()

        self.points = [0, 0] * self.count

        for i in range(self.count):
            self.points[i] = self.center[0] + self.offset[i]
            self.points[i + self.count] = self.center[1] + \
                self.offset[i + self.count]

    def calculate_center(self):
        summa_x = 0
        summa_y = 0

        for i in range(self.count):
            summa_x += self.current_points[i]
            summa_y += self.current_points[i + self.count]

        self.center = [summa_x // self.count, summa_y // self.count]

    def calculate_offset(self):
        self.offset = dict()

        for i in range(self.count):
            self.offset[i] = self.points[i] - self.center[0]
            self.offset[i + self.count] = self.points[i + self.count] - self.center[1]


    def calculate_center_and_offset(self):
        self.calculate_center()
        self.calculate_offset()


    def calculate_perimeter(self):
        self.perimeter = 0

        for i in range(self.count):
            right_index = (i + 1) % self.count

            dx = self.points[i] - self.points[right_index]
            dy = self.points[i + self.count] - \
                self.points[right_index + self.count]

            self.perimeter += math.sqrt(dx ** 2 + dy ** 2)

    def rotation(self, angle):
            self.angle = angle
            for i in range(self.count):
                self.current_points[i] = self.center[0] + (self.points[i] - self.center[0]) * math.cos(angle) - (
                    self.points[i + self.count] - self.center[1]) * math.sin(angle)
                self.current_points[i + self.count] = self.center[1] + (self.points[i] - self.center[0]) * math.sin(angle) + (
                    self.points[i + self.count] - self.center[1]) * math.cos(angle)

            self.move_child()

    def draw(self):
        self.center_figure = canvas.create_oval(self.center[0] - 3,
                                                self.center[1] - 3,
                                                self.center[0] + 3,
                                                self.center[1] + 3,
                                                fill="#FF0000")

        for i in range(0, self.count):
            right_index = (i + 1) % self.count

            if right_index > i:
                left, right = i, right_index
            else:
                left, right = right_index, i
            self.lines_ids[str(left) + ' ' + str(right)] = canvas.create_line(self.current_points[i],
                                                                              self.current_points[i + self.count],
                                                                              self.current_points[right_index],
                                                                              self.current_points[right_index + self.count],
                                                                              fill="#900C3F")

            self.points_ids[i] = canvas.create_oval(self.current_points[i] - 6,
                                                    self.current_points[i + self.count] - 6,
                                                    self.current_points[i] + 6,
                                                    self.current_points[i + self.count] + 6,
                                                    fill="#900C3F")

    def is_intersection(self, point):
        for i in range(self.count):
            x_condition = self.current_points[i] - \
                6 <= point[0] and self.current_points[i] + 6 >= point[0]
            y_condition = self.current_points[i + self.count] - \
                6 <= point[1] and self.current_points[i +
                                                      self.count] + 6 >= point[1]

            if x_condition and y_condition:
                return i

        return -1

    def get_child_position(self):
        if self.child_offset != -1:
            right_index = (self.child_offset[0] + 1) % self.count
            left_index = self.child_offset[0]

            dx = self.current_points[right_index] - \
                self.current_points[left_index]
            dy = self.current_points[right_index + self.count] - \
                self.current_points[left_index + self.count]

            x = self.current_points[left_index] + dx * \
                self.child_offset[1] / math.sqrt(dx ** 2 + dy ** 2)
            y = self.current_points[left_index + self.count] + dy * \
                self.child_offset[1] / math.sqrt(dx ** 2 + dy ** 2)

            return [x, y]

        self.child_offset = [0, 0]
        return [self.current_points[0], self.current_points[self.count]]

    def move_child(self):
        if self.child_offset != -1:
            right_index = (self.child_offset[0] + 1) % self.count

            dx = self.current_points[self.child_offset[0]
                                     ] - self.current_points[right_index]
            dy = self.current_points[self.child_offset[0] + self.count] - \
                self.current_points[right_index + self.count]

            if math.sqrt(dx ** 2 + dy ** 2) < (self.child_offset[1] + 0.001 * self.perimeter):
                movement = 0.001 * self.perimeter + \
                    self.child_offset[1] - math.sqrt(dx ** 2 + dy ** 2)
                self.child_offset = [right_index, movement]
                self.calculate_child_offset()
            else:
                self.child_offset[1] += 0.001 * self.perimeter

    def calculate_child_offset(self):
        right_index = (self.child_offset[0] + 1) % self.count

        dx = self.current_points[self.child_offset[0]
                                 ] - self.current_points[right_index]
        dy = self.current_points[self.child_offset[0] + self.count] - \
            self.current_points[right_index + self.count]

        if self.child_offset[1] > math.sqrt(dx ** 2 + dy ** 2):
            movement = self.child_offset[1] - math.sqrt(dx ** 2 + dy ** 2)
            self.child_offset = [right_index, movement]
            self.calculate_child_offset()


def on_click_canvas(point):
    global state, polygons, action, moving_point
    print(state)
    if state == INIT:
        polygons.append(Polygon(point))
        set_state(DRAW_START)
    else:
        polygon_id, point_id = get_figure(point)
        if polygon_id > -1:
            if polygon_id == 0 and point_id == 0 and state == ADD_VERTEX:
                polygons[0].last_vertex()
                set_state(NEW_POLYGON)
                return
            if polygon_id == 1 and point_id == 0 and state == ADD_VERTEX_POLYGON:
                polygons[1].last_vertex()
                polygons[1].set_center(polygons[0].get_child_position())
                set_state(DRAW_END)
                return
            else:
                moving_point = [polygon_id, point_id]
                action = 'stop'
                return

        if moving_point != -1:
            polygons[moving_point[0]].set_vertex(moving_point[1], point)

            # set_state(last_state)

            moving_point = -1
            return

        if state == DRAW_START:
            polygons[0].add_vertex(point)
            set_state(ADD_VERTEX)

        elif state == ADD_VERTEX:
            polygons[0].add_vertex(point)

        elif state == NEW_POLYGON:
            polygons.append(Polygon(point))
            set_state(ADD_VERTEX_POLYGON)

        elif state == ADD_VERTEX_POLYGON:
            polygons[1].add_vertex(point)


def callback(event):
    canvas.focus_set()
    on_click_canvas([event.x, event.y])


canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.pack()


def draw():
    global time
    if action == 'start':
        canvas.delete('all')
        polygons[0].rotation(time)
        polygons[0].draw()

        polygons[1].set_center(polygons[0].get_child_position())
        polygons[1].rotation(-1 * time)
        polygons[1].draw()

        time += math.pi / 180
    root.after(10, draw)


draw()

root.mainloop()
