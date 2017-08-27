
use <paths.scad>
use <spiral.scad>

module hotplate()
{

    difference () {
        union () {
            difference () {
                poly_baseplate(12.3);
                union () {
                    translate ( [0,0,6] ) cylinder( r= 175/2, h=20, $fn=100 );
                }
            }
            translate ([0,0,1]) {
                union () {
            	    poly_legs(11.3);
                	poly_walls(10);
					//poly_thermscew(10-.01);
                }
            }
        }
		union () {
	        translate ([0,0,6-.3]) union () {
            	poly_hole_middle(20);
            	poly_hole_bottom(20);
            	poly_hole_left(20);
//            poly_hole_right(20);
			}
			translate ([0,0,2]) poly_thermholes(20);
            translate ([0,0,10+1-7.5+3.95]) spiral();
        }
    }

}


render() { hotplate(); }
