import math, cmath
import sys

import spiral

s = spiral.spiral

def split_poly(p):
	return [ [p[0], p[i], p[i+1]] for i in range(1, len(p)-1) ]

def get_rotation(a, b, c):
	a = complex(a[0],a[1])
	b = complex(b[0],b[1])
	c = complex(c[0],c[1])
	t_ba, t_cb = cmath.phase(b-a), cmath.phase(c-b)
	d_angle = (t_cb-t_ba+cmath.pi) % (cmath.pi*2.) - cmath.pi
	mid_angle = t_ba + d_angle/2
	dir_ = cmath.rect(1., mid_angle-cmath.pi/2.)
	return dir_.real, dir_.imag

def get_rotation_end(a, b, phase):
	a = complex(a[0],a[1])
	b = complex(b[0],b[1])
	t_ba = cmath.phase(b-a)
	dir_ = cmath.rect(1., t_ba-cmath.pi/2.-phase)
	return dir_.real, dir_.imag

def extrude_along_path(path, shape, ends=True):

	x1, y1 = path[0]
	x2, y2 = path[1]
	pre = [x1+x1-x2, y1+y1-y2]
	x1, y1 = path[-1]
	x2, y2 = path[-2]
	post = [x1+x1-x2, y1+y1-y2]
	expath=[pre]+path+[post]

	points = []
	faces = []

	for i in xrange(1, len(expath)-1):
		a, b, c = expath[i-1:i+2]
		dx, dy = get_rotation(a, b, c)
		points += [ [b[0]+dx*x, b[1]+dy*x, y] for x, y in shape ]

	n = len(shape)

	for i in xrange(len(path)-1):
		for a in xrange(n):
			b=(a+1)%n
			faces.extend( split_poly( [ i*n+b, i*n+a, (i+1)*n+a, (i+1)*n+b ] ) )

	if ends:
		faces.extend( split_poly(list(range(n))) )
		faces.extend( split_poly(list(range(len(points)-1, len(points)-n-1, -1))) )

	return points, faces

def nested_array_string(array):
	return '['+', '.join('['+','.join(str(e) for e in p)+']' for p in array)+']'

def arch(r=1, w=2, fn=40):
	points = [ ]
	for i in xrange(1-fn/2, fn/2):
		c = cmath.rect(r, cmath.pi*i/fn)
		points.append( [-c.imag, -c.real] )
	return [ [0, w], [w/2, w], [r, 0] ] + points + [ [-r, 0], [-w/2, w] ]

def extrude_along_path_round_ends(path, shape, fn=40):
	assert len(shape) & 1 == 0
	points, faces = extrude_along_path(path, shape, ends=False)
	half_shape = shape[:len(shape)/2+1]
	p_len = len(points)

	indices_first_shape = [ x for x in range(len(shape)) ]
	indices_last_shape =  [ len(points)-len(shape)+(-x)%len(shape) for x in range(len(shape))]

	for indices_shape, p0, p1 in ( (indices_first_shape, path[0], path[1]),
	                               (indices_last_shape, path[-1], path[-2]) ):
		indices = indices_shape[:len(half_shape)]
		for i in xrange(1, fn):
			dx, dy = get_rotation_end(p0, p1, cmath.pi*i/fn)
			indices += [indices_shape[0]] + [ c-1+len(points) for c in range(1, len(half_shape)-1) ] + [ indices_shape[len(half_shape)-1] ]
			points += [ [p0[0]+dx*x, p0[1]+dy*x, y] for x, y in half_shape[1:-1] ]
		indices += [indices_shape[0]] + [ indices_shape[x] for x in xrange(len(shape)-1, len(half_shape)-2, -1) ]

		n = len(half_shape)
		for i in xrange(fn):
			for j in xrange(len(half_shape)-1):
				a, b = j, j+1
				p, q, r, s = indices[i*n+a], indices[i*n+b], indices[(i+1)*n+b], indices[(i+1)*n+a]
				if p == s:
					faces.append([p, q, r])
				elif q == r:
					faces.append([p, q, s])
				else:
					faces.extend(split_poly([p, q, r, s]))

	return points, faces

#points, faces = extrude_along_path(spiral.spiral, [ [-1, 0], [0, -1], [1, 0], [0, 1] ] )
#points, faces = extrude_along_path(spiral.spiral, arch(r=3.9, w=8.5) )
points, faces = extrude_along_path_round_ends(spiral.spiral, arch(r=3.95, w=8.3) )

print 'module spiral() {'
print 'polyhedron( points = '+nested_array_string(points)+', faces = '+nested_array_string(faces)+', convexity=10);'
print '}'
print 'render() { spiral(); }'
