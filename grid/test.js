$(document).ready(function() {
	function Canvas(){
		var t = this;
		t.cont = $("#cont");
		t.lay2 = $(document.createElement("canvas"));
		t.cont.append(t.lay2);
		t.lay2.addClass("canvas");
		t.ctx2 = t.lay2[0].getContext("2d");
        t.ctx2.canvas.width = 640;
        t.ctx2.canvas.height = 480;
        t.pixelSize = 40
		t.fillstyle = "rgba(255, 0, 0, 0.5)"
        t.numVert = 640/40;
        t.numHorz = 480/40;
        
        t.down = function(){
            t.flag_down = true;
            
        }
		
        t.fillsquare = function(e){
			t.ctx2.fillStyle = t.fillstyle;
            var relxy = t.xy(e);
            var relx = relxy[0];
            var rely = relxy[1];
            var gridx = Math.floor(relx/t.pixelSize);
            var gridy = Math.floor(rely/t.pixelSize);
            var offx = gridx*t.pixelSize;
            var offy = gridy*t.pixelSize;
            
            var idx = t.sub2ind(gridx, gridy);
            console.log(relx, rely, "--", gridx, gridy, "--", idx);
            
            if (t.grid[idx] == false){
                t.grid[idx] = true;
                t.ctx2.fillRect(offx,offy,t.pixelSize,t.pixelSize);
            } else {
                t.grid[idx] = false;
                t.ctx2.clearRect(offx,offy,t.pixelSize,t.pixelSize);
            }
            t.flag_fillsquare = false;
		}
        
        t.mouseMoved = function(e){
            if (t.flag_down == true){
                if (t.flag_fillsquare == true){
                    t.fillsquare(e);
                }
            }
        }
        
        t.newGrid = function(){
            grid = [];
            for (var i=0; i<(t.numHorz*t.numVert);i++){
                grid.push(false);
            }
            return grid
        }
        
        t.sub2ind = function(x,y){
            return x*t.numHorz + y;
        }
        
		t.xy = function(e){
            var parentOffset = t.lay2.parent().offset();
            var relx = e.pageX - parentOffset.left;
            var rely = e.pageY - parentOffset.top;
            $("#xy").text(relx + "," + rely );
            return [relx, rely]
        }
        
        
        t.lay2.on("mousedown", (function(){t.flag_down = true;}));
        $(document).on("mouseup", (function(){t.flag_down = false;}));
        t.lay2.on("mousemove", t.mouseMoved);
        t.grid = t.newGrid();
        window.setInterval(function(){t.flag_fillsquare = true;}, 10);
	}
	
	var can1 = new Canvas();
})
