# Explanation of the map

## Used symbols

```
X - wall
# - wall
$ - can/diamond
. - goal
* - can/diamond on a goal
@ - robot/man
a - robot on a goal
```

## Dimensions

```
Width:  9 characters
Height: 9 characters
```

# Coordinate system

Tiles are addressed by tile IDs starting from 1 and increasing from left to right.
The tile ID numbers wrap around on the end of each line. The last tile ID is 81.

## Example with one can

```
XXXXXXXXX
X@      X   <--- Robot (tile ID = 11)
X X X X X
X  $    X   <--- Can on an intersection (tile ID = 31)
X X X X X
X       X
X X X X X
X  .    X   <--- Goal on an intersection (tile ID = 67)
XXXXXXXXX
```

## Useful Coordinates

### Corners
- Top left = 1
- Top right = 9
- Bottom left = 73
- Bottom right = 81

### Inner Walls
- row 3 = 21, 23, 25
- row 5 = 39, 41, 43
- row 7 = 57, 59, 61
