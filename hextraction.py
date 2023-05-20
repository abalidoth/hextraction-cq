#!/usr/bin/env python
# coding: utf-8


import cadquery as cq




#Basic tile dimensions
#You shouldn't need to update anything here, except possibly `tile_height`.

tile_height = 15 #This one might need modified for your design.
tile_width = 50
tile_radius = tile_width/3**0.5
base_width = 46
upper_edge_fillet = 1
lower_edge_chamfer = (tile_width - base_width)/2
corner_fillet = 4

socket_height = 3
socket_depth = 5
socket_width = 13

top_height = tile_height - socket_height

# Dimensions of the basic ball channel.

channel_width = 11
channel_radius = channel_width/2
channel_flat_distance = 2
channel_throat_depth = 1
channel_throat_restriction = 1
channel_throat_flat = 0.5

channel_throat_width = channel_width - 2*channel_throat_restriction


# This code produces the basic blank Hextraction tile.

hex_base = (
    cq.Workplane("XY")
    .polygon(6,tile_width, circumscribed=True)
    .extrude(top_height)
    .edges("|Z").fillet(corner_fillet)
    .edges(">Z").fillet(upper_edge_fillet)
    .edges("<Z").chamfer(lower_edge_chamfer)
    .wires("<Z").toPending()
    .extrude(-socket_height)
    .faces("<Z").workplane()
    .polarArray(radius= base_width/2-socket_depth/2, angle=360, count=6, startAngle=0)
    .rect(socket_depth, socket_width)
    .cutBlind(-socket_height)
)

# And an example hex with a channel through it.

channel_profile = (
    cq.Workplane("YZ")
    .center(0,top_height/2)
    .moveTo(-channel_throat_width/2, 0)
    .vLine(-channel_throat_flat)
    .line(-channel_throat_restriction,-channel_throat_depth)
    .vLine(-channel_flat_distance)
    .tangentArcPoint((channel_width,0))
    .vLine(channel_flat_distance)
    .line(-channel_throat_restriction, channel_throat_depth)
    .vLine(channel_throat_flat)
    .close()
)


channel_end = (3*tile_radius/4, 3*tile_width/4)

channel_path = (
    cq.Workplane("YX")
    .move(0,-1)
    .vLine(1, forConstruction=True)
    .tangentArcPoint(channel_end)
)

channel_example = channel_profile.sweep(channel_path)

channel_tile = (
    hex_base -
    channel_example
    .translate((-tile_width/2,0,top_height/2))
)

if __name__ == "__main__":
    cq.exporters.export(channel_tile, "hextraction_example_tile.stl")