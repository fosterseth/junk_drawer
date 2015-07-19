$(document).ready(function() {
	function Canvas(){
		var t = this;
		t.cont = $("#cont");
        
        t.lay1 = $(document.createElement("canvas"));
        t.cont.append(t.lay1);
        t.lay1.addClass("canvas");
        t.ctx1 = t.lay1[0].getContext("2d");
        t.ctx1.canvas.width = 640;
        t.ctx1.canvas.height = 480;
        
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
        
        t.drawLines = function(){
            for (var i=1; i<t.numVert;i++){
                t.ctx1.moveTo(t.pixelSize*i,0);
                t.ctx1.lineTo(t.pixelSize*i, 480);
                t.ctx1.stroke();
            }
            for (var i=1; i<t.numHorz;i++){
                t.ctx1.moveTo(0,t.pixelSize*i);
                t.ctx1.lineTo(640,t.pixelSize*i);
                t.ctx1.stroke();
            }
        }
        
        t.down = function(e){
            t.flag_down = true;
            t.fillsquare(e, 1);
            t.delaydrag = setTimeout(function () {
                console.log("setting timeout");
                t.lay2.on("mousemove", (function (e) {
                t.fillsquare(e, 0);
            }))}, 150);
        }
		
        t.fillsquare = function(e, flag_clicked){
			t.ctx2.fillStyle = t.fillstyle;
            var relxy = t.xy(e);
            var relx = relxy[0];
            var rely = relxy[1];
            var gridx = Math.floor(relx/t.pixelSize);
            var gridy = Math.floor(rely/t.pixelSize);
            var offx = gridx*t.pixelSize;
            var offy = gridy*t.pixelSize;
            
            var idx = t.sub2ind(gridx, gridy);
            //console.log(relx, rely, "--", gridx, gridy, "--", idx);
            
            if (t.grid[idx] == false){
                t.grid[idx] = true;
                t.ctx2.fillRect(offx,offy,t.pixelSize,t.pixelSize);
            } else if (flag_clicked == 1) {
                t.grid[idx] = false;
                t.ctx2.clearRect(offx,offy,t.pixelSize,t.pixelSize);
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
        
        t.up = function(){
            // cancel the setTimeout schedule
            clearTimeout(t.delaydrag);
            // turn off mousemove callbacks
            t.lay2.off("mousemove");
        }
        
		t.xy = function(e){
            var parentOffset = t.lay2.parent().offset();
            var relx = e.pageX - parentOffset.left;
            var rely = e.pageY - parentOffset.top;
            $("#xy").text(relx + "," + rely );
            return [relx, rely]
        }
        
        
        t.lay2.on("mousedown", t.down);
        $(document).on("mouseup", t.up);
        t.grid = t.newGrid();
        t.drawLines();

	}
	
	var can1 = new Canvas();
})
