import numpy as np
import wx

import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import gcf, setp

from matplotlib.ticker import IndexLocator, NullFormatter, ScalarFormatter

from pygeom.geometry import blue, red, green, Geometry

from pygeom.field import FiniteField
from pygeom.core import Line, Point
from pygeom.conic import Conic
from pygeom.pairs import PointLine, Vertex, LineSegment


class ObjectLine(object):
    def __init__(self, parent, panel, object):
        self.object = object
        self.panel = panel
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        print type(object[0])
        print type(object[0]) == Line

        if type(object[0]) == Point:
            label = "(%d, %d): %s " % (object[0].x.value, object[0].y.value, object[1])
        elif type(object[0]) == Line:
            label = "<%d:%d:%d>: %s " % (object[0].a.value, object[0].b.value, object[0].c.value, object[1])
        else:
            label = "<%d:%d:%d:%d:%d:%d>: %s " % (object[0].a.value, object[0].b.value, object[0].c.value, 
                                                  object[0].d.value, object[0].e.value, object[0].f.value, object[1])

        self.label = wx.StaticText(parent, label=label)
        self.edit_button = wx.Button(parent, label="EDIT")
        self.del_button = wx.Button(parent, label="DELETE")
        self.check = wx.CheckBox(parent)
       
        self.sizer.Add(self.check, 0, wx.EXPAND)
        self.sizer.Add(self.label, 0, wx.EXPAND)
        self.sizer.Add(self.edit_button, 0, wx.EXPAND)
        self.sizer.Add(self.del_button, 0, wx.EXPAND)

        self.edit_button.Bind(wx.EVT_BUTTON, self.edit_button_handler)
        self.del_button.Bind(wx.EVT_BUTTON, self.del_button_handler)

    def edit_button_handler(self, evt):
        print "EDIT", self

    def del_button_handler(self, evt):
        self.panel.delete_object(self)
        self.sizer.Clear(True)
        self.panel.sizer.Remove(self.sizer)
        self.panel.sizer.Layout()
        self.panel.plot.draw()


class ObjectPanel(object):

    def __init__(self, parent, plot):
        self.parent = parent
        self.plot = plot
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.field = FiniteField
        self.field.base = 37

        self.main_label = wx.StaticText(parent, label="Objects")
        self.point_label = wx.StaticText(parent, label="Points")
        self.line_label = wx.StaticText(parent, label="Lines")
        self.conic_label = wx.StaticText(parent, label="Conics")

        self.points = []
        self.lines = []
        self.conics = []

        self._arrange_objects()

    def add_point(self, point):
        obj_line = ObjectLine(self.parent, self, point)
        self.points.append(obj_line)
        self.sizer.Insert(1 + len(self.points), obj_line.sizer, 0, wx.EXPAND)
        self.sizer.Layout()
        self.plot.draw()

    def add_line(self, line):
        obj_line = ObjectLine(self.parent, self, line)
        self.lines.append(obj_line)
        self.sizer.Insert(2 + len(self.points) + len(self.lines), obj_line.sizer, 0, wx.EXPAND)
        self.sizer.Layout()
        self.plot.draw()

    def add_conic(self, conic):
        obj_line = ObjectLine(self.parent, self, conic)
        self.conics.append(obj_line)
        self.sizer.Insert(3 + len(self.points) + len(self.lines) + len(self.conics), obj_line.sizer, 0, wx.EXPAND)
        self.sizer.Layout()
        self.plot.draw()


    def get_objects(self):
        return [obj_line.object for obj_line in self.points + self.lines + self.conics]

    def _arrange_objects(self):
        self.sizer.Clear()

        self.sizer.Add(self.main_label, 0, wx.EXPAND)

        self.sizer.Add(self.point_label, 0, wx.EXPAND)
        for point in self.points:
            self.sizer.Add(ObjectLine(self.parent, self, point).sizer, 0, wx.EXPAND)

        self.sizer.Add(self.line_label, 0, wx.EXPAND)
        for line in self.lines:
            self.sizer.Add(ObjectLine(self.parent, self, line).sizer, 0, wx.EXPAND)

        self.sizer.Add(self.conic_label, 0, wx.EXPAND)
        for conic in self.conics:
            self.sizer.Add(ObjectLine(self.parent, self, conic).sizer, 0, wx.EXPAND)


    def delete_object(self, object):
        for list in [self.points, self.lines, self.conics]:
            try:
                list.remove(object)
            except ValueError:
                pass


art_list = [
    wx.ART_ADD_BOOKMARK, 
    wx.ART_DEL_BOOKMARK, 
    wx.ART_HELP_SIDE_PANEL,
    wx.ART_HELP_SETTINGS, 
    wx.ART_HELP_BOOK, 
    wx.ART_HELP_FOLDER,
    wx.ART_HELP_PAGE, 
    wx.ART_GO_BACK, 
    wx.ART_GO_FORWARD,
    wx.ART_GO_UP,
    wx.ART_GO_DOWN,
    wx.ART_GO_TO_PARENT,
    wx.ART_GO_HOME,
    wx.ART_FILE_OPEN,
    wx.ART_FILE_SAVE,
    wx.ART_FILE_SAVE_AS,
    wx.ART_PRINT,
    wx.ART_HELP,
    wx.ART_TIP,
    wx.ART_REPORT_VIEW,
    wx.ART_LIST_VIEW,
    wx.ART_NEW_DIR,
    wx.ART_HARDDISK,
    wx.ART_FLOPPY,
    wx.ART_CDROM,
    wx.ART_REMOVABLE,
    wx.ART_FOLDER,
    wx.ART_FOLDER_OPEN,
    wx.ART_GO_DIR_UP,
    wx.ART_EXECUTABLE_FILE,
    wx.ART_NORMAL_FILE,
    wx.ART_TICK_MARK,
    wx.ART_CROSS_MARK,
    wx.ART_ERROR,
    wx.ART_QUESTION,
    wx.ART_WARNING,
    wx.ART_INFORMATION,
    wx.ART_MISSING_IMAGE,
    wx.ART_COPY,
    wx.ART_CUT,
    wx.ART_PASTE,
    wx.ART_DELETE,
    wx.ART_NEW,
    wx.ART_UNDO,
    wx.ART_REDO,
    wx.ART_QUIT,
    wx.ART_FIND,
    wx.ART_FIND_AND_REPLACE
    ]

class ControlPanel(object):

    def __init__(self, parent):

        self.parent = parent
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.state = None
        self.new_point(None)

        self.field = FiniteField
        self.field.base = 37

    def _get_colour(self):
        colour = self.colours.GetValue()
        return {"blue": blue(self.field),
                "red": red(self.field),
                "green": green(self.field)}[colour]

    def _add_common(self, callback):
        self.colours = wx.ComboBox(self.parent, value="blue", choices=["blue", "red", "green"], style=wx.CB_READONLY)
        self.sizer.Add(self.colours, 0, wx.EXPAND)

        self.name = wx.TextCtrl(self.parent, size=(150, 1))
        self.sizer.Add(self.name, 0, wx.EXPAND)

        self.button = wx.Button(self.parent, label="ADD")
        self.button.Bind(wx.EVT_BUTTON, callback)
        self.sizer.Add(self.button, 0, wx.EXPAND)

        self.parent.main_sizer.Layout()

    def _spinner(self):
        return wx.SpinCtrl(self.parent, min=0, max=37, initial=1)

    def _add_point_box(self):
        point_names = [point.object[1] for point in self.parent.object_panel.points]
        points = wx.ComboBox(self.parent, value="a", choices=point_names, style=wx.CB_READONLY)
        self.sizer.Add(points, 0, wx.EXPAND)
        return points

    def _add_line_box(self):
        line_names = [line.object[1] for line in self.parent.object_panel.lines]
        lines = wx.ComboBox(self.parent, value="a", choices=line_names, style=wx.CB_READONLY)
        self.sizer.Add(lines, 0, wx.EXPAND)
        return lines

    def _get_point(self, points):
        point_name = points.GetValue()
        for point in self.parent.object_panel.points:
            if point.object[1] == point_name:
                return point.object[0]

    def _get_line(self, lines):
        line_name = lines.GetValue()
        for line in self.parent.object_panel.lines:
            if line.object[1] == line_name:
                return line.object[0]

    def new_point(self, evt):
        if self.state != "NEW_POINT":
            self.state = "NEW_POINT"
            self.sizer.Clear(True)
            self.x = self._spinner()
            self.y = self._spinner()
            self.sizer.Add(self.x, 0, wx.EXPAND)
            self.sizer.Add(self.y, 0, wx.EXPAND)

            self._add_common(self.add_point)
    
    def add_point(self, evt):
        x = self.x.GetValue()
        y = self.y.GetValue()
        name = self.name.GetValue()
        point = Point(self.field(x), self.field(y), self._get_colour()), name, "s", self.colours.GetValue()
        self.parent.object_panel.add_point(point)
            
    def new_line(self, evt):
        if self.state != "NEW_LINE":
            self.state = "NEW_LINE"
            self.sizer.Clear(True)
            self.a = self._spinner()
            self.b = self._spinner()
            self.c = self._spinner()
            self.sizer.Add(self.a, 0, wx.EXPAND)
            self.sizer.Add(self.b, 0, wx.EXPAND)
            self.sizer.Add(self.c, 0, wx.EXPAND)

            self._add_common(self.add_line)

    def add_line(self, evt):
        a = self.a.GetValue()
        b = self.b.GetValue()
        c = self.c.GetValue()
        name = self.name.GetValue()
        line = Line(self.field(a), self.field(b), self.field(c), self._get_colour()), name, "o", self.colours.GetValue()
        self.parent.object_panel.add_line(line)

    def new_conic(self, evt):
        if self.state != "NEW_CONIC":
            self.state = "NEW_CONIC"
            self.sizer.Clear(True)
            self.a = self._spinner()
            self.b = self._spinner()
            self.c = self._spinner()
            self.d = self._spinner()
            self.e = self._spinner()
            self.f = self._spinner()
            self.sizer.Add(self.a, 0, wx.EXPAND)
            self.sizer.Add(self.b, 0, wx.EXPAND)
            self.sizer.Add(self.c, 0, wx.EXPAND)
            self.sizer.Add(self.d, 0, wx.EXPAND)
            self.sizer.Add(self.e, 0, wx.EXPAND)
            self.sizer.Add(self.f, 0, wx.EXPAND)

            self._add_common(self.add_conic)

    def add_conic(self, evt):
        a = self.a.GetValue()
        b = self.b.GetValue()
        c = self.c.GetValue()
        d = self.d.GetValue()
        e = self.e.GetValue()
        f = self.f.GetValue()
        name = self.name.GetValue()
        conic = Conic(self.field(a), self.field(b), self.field(c), self.field(d), self.field(e), self.field(f), self._get_colour()), name, "x", self.colours.GetValue()
        self.parent.object_panel.add_conic(conic)


    def new_circle(self, evt):
        if self.state != "NEW_CIRCLE":
            self.state = "NEW_CIRCLE"
            self.sizer.Clear(True)
            self.k = self._spinner()
            self.sizer.Add(self.k, 0, wx.EXPAND)

            self.points = self._add_point_box()

            self._add_common(self.add_circle)

    def add_circle(self, evt):
        k = self.k.GetValue()
        centre = self._get_point(self.points)
        name = self.name.GetValue()
        if centre is not None:
            conic = centre.circle(k), name, "x", self.colours.GetValue()
            self.parent.object_panel.add_conic(conic)


    def new_parabola(self, evt):
        if self.state != "NEW_PARABOLA":
            self.state = "NEW_PARABOLA"
            self.sizer.Clear(True)
            
            self.points = self._add_point_box()
            self.lines = self._add_line_box()

            self._add_common(self.add_parabola)

    def add_parabola(self, evt):
        line_name = self.lines.GetValue()
        directrix = None
        focus = self._get_point(self.points)

        directrix = self._get_line(self.lines)

        if focus and directrix:
            pl = PointLine(focus, directrix)
            name = self.name.GetValue()
            conic = pl.parabola(), name, "x", self.colours.GetValue()
            self.parent.object_panel.add_conic(conic)


    def new_altitude(self, evt):
        if self.state != "NEW_ALTITUDE":
            self.state = "NEW_ALTITUDE"
            self.sizer.Clear(True)
            
            self.points = self._add_point_box()
            self.lines = self._add_line_box()

            self._add_common(self.add_altitude)

    def add_altitude(self, evt):
        point_ = self._get_point(self.points)
        line_ = self._get_line(self.lines)

        if point_ and line_:
            pl = PointLine(point_, line_)
            name = self.name.GetValue()
            altitude = pl.altitude(), name, "o", self.colours.GetValue()
            self.parent.object_panel.add_line(altitude)

    def new_parallel(self, evt):
        if self.state != "NEW_PARALLEL":
            self.state = "NEW_PARALLEL"
            self.sizer.Clear(True)
            
            self.points = self._add_point_box()
            self.lines = self._add_line_box()

            self._add_common(self.add_parallel)

    def add_parallel(self, evt):
        point_ = self._get_point(self.points)
        line_ = self._get_line(self.lines)

        if point_ and line_:
            pl = PointLine(point_, line_)
            name = self.name.GetValue()
            parallel = pl.parallel(), name, "o", self.colours.GetValue()
            self.parent.object_panel.add_line(parallel)

    def new_conick(self, evt):
        if self.state != "NEW_CONICK":
            self.state = "NEW_CONICK"
            self.sizer.Clear(True)

            self.k = self._spinner()
            self.sizer.Add(self.k, 0, wx.EXPAND)
            
            self.points = self._add_point_box()
            self.lines = self._add_line_box()

            self._add_common(self.add_conick)


    def add_conick(self, evt):
        k = self.k.GetValue()
        focus = self._get_point(self.points)
        directrix = self._get_line(self.lines)

        if focus and directrix:
            pl = PointLine(focus, directrix)
            name = self.name.GetValue()
            conic = pl.conic(k), name, "x", self.colours.GetValue()
            self.parent.object_panel.add_conic(conic)


    def new_midpoint(self, evt):
        if self.state != "NEW_MIDPOINT":
            self.state = "NEW_MIDPOINT"
            self.sizer.Clear(True)

            self.points1 = self._add_point_box()
            self.points2 = self._add_point_box()

            self._add_common(self.add_midpoint)

    def add_midpoint(self, evt):
        p1 = self._get_point(self.points1)
        p2 = self._get_point(self.points2)

        if p1 and p2:
            line_segment = LineSegment(p1, p2)
            name = self.name.GetValue()
            mid = line_segment.midpoint(), name, "s", self.colours.GetValue()
            self.parent.object_panel.add_point(mid)

    def new_quadrola(self, evt):
        if self.state != "NEW_QUADROLA":
            self.state = "NEW_QUADROLA"
            self.sizer.Clear(True)

            self.k = self._spinner()
            self.sizer.Add(self.k, 0, wx.EXPAND)

            self.points1 = self._add_point_box()
            self.points2 = self._add_point_box()

            self._add_common(self.add_quadrola)

    def add_quadrola(self, evt):
        k = self.k.GetValue()
        p1 = self._get_point(self.points1)
        p2 = self._get_point(self.points2)

        if p1 and p2:
            line_segment = LineSegment(p1, p2)
            name = self.name.GetValue()
            quadrola = line_segment.quadrola(k), name, "x", self.colours.GetValue()
            self.parent.object_panel.add_conic(quadrola)

    def new_grammola(self, evt):
        if self.state != "NEW_GRAMMOLA":
            self.state = "NEW_GRAMMOLA"
            self.sizer.Clear(True)

            self.k = self._spinner()
            self.sizer.Add(self.k, 0, wx.EXPAND)

            self.lines1 = self._add_line_box()
            self.lines2 = self._add_line_box()

            self._add_common(self.add_grammola)

    def add_grammola(self, evt):
        k = self.k.GetValue()
        l1 = self._get_line(self.lines1)
        l2 = self._get_line(self.lines2)

        if l1 and l2:
            vertex = Vertex(l1, l2)
            name = self.name.GetValue()
            grammola = vertex.grammola(k), name, "x", self.colours.GetValue()
            self.parent.object_panel.add_conic(grammola)


    def new_reflection(self, evt):
        if self.state != "NEW_REFLECTION":
            self.state = "NEW_REFLECTION"
            self.sizer.Clear(True)

            self.points = self._add_point_box()
            self.lines = self._add_line_box()

            self._add_common(self.add_reflection)

    def add_reflection(self, evt):
        point = self._get_point(self.points)
        line = self._get_line(self.lines)

        if point and line:
            point_line = PointLine(point, line)
            name = self.name.GetValue()
            ref = point_line.reflection(), name, "s", self.colours.GetValue()
            self.parent.object_panel.add_point(ref)



class FinitePlotFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.plot = FinitePlotWindow(self)
        self.object_panel = ObjectPanel(self, self.plot)
        self.control_panel = ControlPanel(self)

        self.plot.draw()


        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.plot, 1, wx.EXPAND)
        sizer.Add(self.object_panel.sizer, 0, wx.EXPAND)

        self.main_sizer.Add(self.control_panel.sizer, 0, wx.EXPAND)
        self.main_sizer.Add(sizer, 0, wx.EXPAND)

        self.SetSizer(self.main_sizer)

        ADD_POINT = wx.NewId()
        ADD_LINE = wx.NewId()
        ADD_CONIC = wx.NewId()
        ADD_CIRCLE = wx.NewId()
        ADD_PARABOLA = wx.NewId()
        ADD_CONICK = wx.NewId()
        ADD_ALTITUDE = wx.NewId()
        ADD_PARALLEL = wx.NewId()
        ADD_MIDPOINT = wx.NewId()
        ADD_QUADROLA = wx.NewId()
        ADD_GRAMMOLA = wx.NewId()
        ADD_REFLECTION = wx.NewId()

        self.toolbar = self.CreateToolBar(wx.TB_TEXT|wx.NO_BORDER|wx.TB_HORIZONTAL|wx.TB_3DBUTTONS)
        self.toolbar.AddLabelTool(ADD_POINT, "Add Point", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_LINE, "Add Line", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_CONIC, "Add Conic", wx.NullBitmap, shortHelp="ber")
        self.toolbar.AddLabelTool(ADD_CIRCLE, "Add Circle", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_PARABOLA, "Add Parabola", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_CONICK, "Add Conic(2)", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_ALTITUDE, "Add Altitude", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_PARALLEL, "Add Parallel", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_QUADROLA, "Add Quadrola", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_GRAMMOLA, "Add Grammola", wx.NullBitmap)
        self.toolbar.AddLabelTool(ADD_REFLECTION, "Add Relfection", wx.NullBitmap)

        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.control_panel.new_point, id=ADD_POINT)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_line, id=ADD_LINE)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_conic, id=ADD_CONIC)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_circle, id=ADD_CIRCLE)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_parabola, id=ADD_PARABOLA)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_conick, id=ADD_CONICK)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_altitude, id=ADD_ALTITUDE)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_parallel, id=ADD_PARALLEL)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_midpoint, id=ADD_MIDPOINT)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_quadrola, id=ADD_QUADROLA)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_grammola, id=ADD_GRAMMOLA)
        self.Bind(wx.EVT_TOOL, self.control_panel.new_reflection, id=ADD_REFLECTION)



class FinitePlotWindow(wx.Window):
    def __init__(self, parent, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.lines = []
        self.figure = Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        #self.canvas.callbacks.connect('button_press_event', self.mouseDown)
        #self.canvas.callbacks.connect('motion_notify_event', self.mouseMotion)
        #self.canvas.callbacks.connect('button_release_event', self.mouseUp)
        self.state = ''
        self.mouseInfo = (None, None, None, None)
        #self.f0 = Param(2., minimum=0., maximum=6.)
        #self.A = Param(1., minimum=0.01, maximum=2.)
        self.Bind(wx.EVT_SIZE, self.sizeHandler)

       
    def sizeHandler(self, *args, **kwargs):
        self.canvas.SetSize(self.GetSize())
    
    def draw(self):
        if not hasattr(self, 'ax'):
            self.ax = self.figure.add_subplot(111)
        ax = self.ax
        ax.clear()

        handles = []
        labels = []
        self.field = self.parent.object_panel.field

        for object, name, marker, color in self.parent.object_panel.get_objects():
            xs = []
            ys = []
            l = object
            for x in range(self.field.base):
                for y in range(self.field.base):
                    if object.eval(x, y) == 0:
                        xs.append(x)
                        ys.append(y)
            handles.append(ax.scatter(xs, ys, marker=marker, s=100, color=color))
            labels.append(name)

        ax.set_xlim(-0.5, self.field.base - 0.5)
        ax.set_ylim(-0.5, self.field.base - 0.5)

        ax.xaxis.set_major_locator( IndexLocator(-0.5, 1) )
        ax.xaxis.set_minor_locator( IndexLocator(0, 1) )
        ax.yaxis.set_major_locator( IndexLocator(-0.5, 1) )
        ax.yaxis.set_minor_locator( IndexLocator(0, 1) )
        
        ax.xaxis.set_major_formatter( NullFormatter() )
        ax.xaxis.set_minor_formatter( ScalarFormatter() )
        ax.yaxis.set_major_formatter( NullFormatter() )
        ax.yaxis.set_minor_formatter( ScalarFormatter() )

        ax.set_xticks(range(0, self.field.base), minor=True)
        ax.set_yticks(range(0, self.field.base), minor=True)

        ax.set_xticks([x + 0.5 for x in range(0, self.field.base)])
        ax.set_yticks([x + 0.5 for x in range(0, self.field.base)])

        ax.grid(True)
        self.repaint()


    def repaint(self):
        self.canvas.draw()


class App(wx.App):
    def OnInit(self):
        sys.stdout = stdout
        sys.stderr = stderr
        self.frame1 = FinitePlotFrame(parent=None, title="Finite Field Geometry Demo", size=(640, 480))
        self.frame1.Show()
        return True
        


import sys
stdout = sys.stdout
stderr = sys.stderr
app = App()
app.MainLoop()



