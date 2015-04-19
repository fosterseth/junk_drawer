$(document).ready(function() {
/*This script runs on the client's browser.
Data passed in from php:
	confirmation_code - code given to Turk user at the end
	allsavenames - where to save results
	allresults - if task has been done before, data from results file
	allimages - image file names
	allconfig - configuration of task (image dimensions, pixel size, color of squares, etc.)

User begins by clicking on "start" button. The first image is loaded. Each time "submit" button is clicked, the results are saved and the next image is loaded. This is repeated until all images are accounted for, after which a confirmation screen is displayed with the confirmation_code.

There are two panels in the task, left and right. By default, the left panel is active. If the image name includes "right", then the right panel is activated. In the code, obj.right is the parameter that determines which panel is active, with obj.right = 1 indicating the right panel.

e.g.,
both_ctx = [left panel, right panel], so both_ctx[obj.right] will reference the correct panel objects.

Squares on the grid are referenced by their index number in the array. Top left is 0, counting downwards, e.g.,
0 4 8 12 ..
1 5 9 13 
2 6 10 14
3 7 11 15
..

There is only one grid array maintained throughout the code, despite there being two panels. For that reason, and others, it's only possible to code from a single panel at a time. The code would have to be restructured (which I'd be willing to do if need be) to handle displaying and coding two panels simultaneously.

Author: sbf@umail.iu.edu
Updated: 08/12/2014
*/

enabledrag = false;
delaydrag = false;

c=0; //c refers to the index of the main task loop. Normally 2 loops total, training and then official task. However, any amount is possible.
//set canvas variables. "2" appended at the end refers to the right-side panel
$canvas_first = $('#mycanvas_first');
$ctx_first = $canvas_first[0].getContext('2d');
$image = $('#mycanvas');
$ctx = $image[0].getContext('2d');

$canvas_first2 = $('#mycanvas_first2');
$ctx_first2 = $canvas_first2[0].getContext('2d');
$image2 = $('#mycanvas2');
$ctx2 = $image2[0].getContext('2d');

//objects are stored into array. Whenever an image name includes "right", the code will enact on the right side panel
both_canvas_first = [$canvas_first, $canvas_first2];
both_ctx_first = [$ctx_first, $ctx_first2];
both_image = [$image, $image2];
both_ctx = [$ctx, $ctx2];
imgPos = [];
//console.log(both_image);
//disable back button for now
$("#back").prop("disabled", true);
$("#back").off("click");

//click button to initiate everything
$("#button").one("click",(function(){
$("#button").html("submit");
initialize();
}));

//write configuration settings to results file, set up configuration object, run main
function initialize(){
//do not save results if a results files already existed before starting this task.
if (c < allconfig.length){
obj = allconfig[c];
if (allresults[c] != false){
obj.results_save = 0;
}else{
obj.results_save = 1;
obj.savefilename = allsavenames[c];
obj.confirmation_code = confirmation_code;
obj.taskcode = taskcode;
};
//also, if results file name is set to empty or -1, do not save results
if (allsavenames[c] == "" || allsavenames[c] == "-1"){
obj.results_save = 0;
};

//for left and right panels, set the canvas width and height and get their locations on the screen
for (i=0;i<=1;i++){
$this_image = both_image[i];
$this_image.width(obj.image_width).height(obj.height);
imgPos[i] = [
    $this_image.offset().left,
    $this_image.offset().top,
    $this_image.offset().left + $this_image.outerWidth(),
    $this_image.offset().top + $this_image.outerHeight()
];
$this_ctx = both_ctx[i];
$this_ctx.canvas.width = obj.image_width;
$this_ctx.canvas.height = obj.image_height;

$this_ctx_first = both_ctx_first[i];
$this_ctx_first.canvas.width = obj.image_width;
$this_ctx_first.canvas.height = obj.image_height;

};

ftowrite = "";
//writes the configuration parameters into the results file for future reference
if (obj.results_save == 1){
initialize_results();
};

//creates main object with all of the information for this task iteration (determined by c)
set_config(allconfig[c],allfiles[c],allresults[c]);
$("#textbox_label").text(obj.textbox_label + " ");
new_grid();
if (obj.randomize_images == 1){
shuffle(obj.image_names);
};



//for each task run through main and increment c for next task
c+=1;

main();
//after all tasks are run, display confirmation screen and write "end" into results file
}else{
if (obj.results_save == 1){
////console.log("end");
for (var i=0;i<obj.towrite.length;i++){
write_to_file(obj.towrite[i]);
};
write_to_file("#end\n", JSON.stringify(1));
write_to_file("#textbox\n", JSON.stringify(1));
for (var i=0;i<obj.towrite.length;i++){
write_to_file(obj.towrite2[i]);
};
write_to_file("#end", JSON.stringify(1));
write_to_results(ftowrite, JSON.stringify(1));
};

$("#all").remove();
$("#endtext").show();
$("#code").html(confirmation_code);
//location.replace("../misc/finish.html");
};
};

//main enables the submit button to call "next_img" each click
function main(){
//console.log("main");
//load first image
$("#back").on("click", back_button);
next_img();
//initialize button
$("#button").off("click");
$("#button").on("click", button_task); //listens for submit clicks
};

/*loads next image file, resets the grid and determines whether to show on the left or right panel
If "text", turn off grid and disable squares
If "right", turn grid on for right panel and disable square clicks for left panel
If viewing previous results, the panel is square clicks are disabled IF the grid is allocated with squares. Otherwise, the panel allows square clicks
*/
function next_img(){
//default is that right is turned off and left is turned on
obj.right = 1;
turn_grid_off();
disable_square_task();
obj.right = 0;
turn_grid_off();
turn_grid_on();
disable_square_task();
enable_square_task();
disable_button();
//console.log(obj.image_index);
if (obj.image_index == 0){
$("#back").prop("disabled", true);
};
if (obj.image_index == 1){
$("#back").prop("disabled", false);
};

//get next image name
if (obj.image_index <= obj.image_names.length-1){
this_image_name = obj.image_names[obj.image_index];

var match_idx = obj.results_image_names.indexOf(this_image_name);
var is_right = this_image_name.indexOf('right') != -1;
var is_text = this_image_name.indexOf('text') != -1;

if (is_right == 1){
new_grid();
obj.right = 0;
disable_square_task();
obj.right = 1;
enable_square_task();
turn_grid_on();
$("#img2").attr("src", this_image_name);
$("#img2").load(enable_button());
}else{
obj.right = 1;
clear_grid();
obj.right = 0;
clear_grid();
$("#img").attr("src", this_image_name);
$("#img").load(enable_button());
$("#img2").attr("src", "../misc/startimg2.png");
};

//determine whether to display grid
if (is_text == 1){
turn_grid_off();
disable_square_task();
};

//preallocate grid with previous results
if (match_idx != -1){
preallocate_grid(match_idx);
};
}else{
initialize();
};
};

function back_button(){
obj.image_index -= 1;
next_img();
};

function disable_button(){
//$("#button").off('click');
$("#button").prop("disabled",true);
};

function enable_button(){
//$("#button").on('click', button_task());
$("#button").prop("disabled",false);
};

//draw the horizontal and vertical black lines on the active panel
function turn_grid_on(){
draw_lines();
};

function enable_square_task(){
both_image[obj.right].on('mousedown', square_task);
$(document).on('mouseup', (function () {
	enabledrag = false;
	clearTimeout(delaydrag);
    both_image[obj.right].off("mousemove");}));
};

function disable_square_task(){
//console.log("disabled");
both_image[obj.right].off("mousedown");
both_image[obj.right].off("mousemove");
both_image[obj.right].off("click");
};

//http://stackoverflow.com/questions/4648444/jquery-fire-mousemove-events-less-often
timer = window.setInterval(function(){enablesquareclick = true;}, 10);

function square_task(e1){
$("#xy").text(e1.pageX + "," + e1.pageY);
enabledrag = true;
square_clicked((e1.pageX-imgPos[obj.right][0]), (e1.pageY-imgPos[obj.right][1]), 1);
delaydrag = setTimeout(function () {both_image[obj.right].on("mousemove", (function (e) {
    if (enabledrag && enablesquareclick) {
        square_clicked((e.pageX-imgPos[obj.right][0]), (e.pageY-imgPos[obj.right][1]), 0);
        enablesquareclick = false;
        };
}))}, 100);

};

//determines which square was clicked based on x,y coordinates and then fills that square
function square_clicked(x,y,click){
var nx = Math.floor(x/obj.pixel_size);
var ny = Math.floor(y/obj.pixel_size);
var index = sub2ind(nx,ny);
var ps = obj.pixel_size;
fill_square(index,nx,ny,ps,click);
};

function fill_square(index,nx,ny,ps,click){
smallobj = [];
smallobj.index = index;
smallobj.nx = nx;
smallobj.ny = ny;
smallobj.bothimg1 = both_image;
smallobj.ps = ps;
//console.log(smallobj);
if (obj.grid[index]==false){
//set fill style
both_ctx[obj.right].fillStyle = 'rgba('+obj.highlight_color+','+obj.highlight_transparency+')';

both_ctx[obj.right].fillRect(nx*ps,ny*ps,ps,ps);
obj.grid[index] = true;
} else if (click == 1) {
both_ctx[obj.right].clearRect(nx*ps,ny*ps,ps,ps);
obj.grid[index] = false;
}
};

//If viewing previous results, preallocate the grid with that result's data for each image file. Note, if there is nothing to preallocate, the square task for the panel is not disabled.
function preallocate_grid(match_idx){
//console.log("preallocate_grid");
var indices = obj.results_data[match_idx];
var ps = obj.pixel_size;
if (indices.length > 0){
disable_square_task();
for (var v=0;v<indices.length;v++){
var index = indices[v];
var n = ind2sub(index);
fill_square(index,n[0],n[1],ps,1);
};
};
};

function turn_grid_off(){
both_ctx_first[obj.right].clearRect(0,0,obj.image_width,obj.image_height);
};

//each time submit button is pressed, save the results, increment image index by one, and load the image
function button_task(){
if (obj.results_save == 1){
save_grid();
save_textbox();
};
//var d = $('input:radio[name=box]:checked').val();
obj.image_index += 1;

next_img();
};

function save_grid(){
var towrite = grid_to_index();
towrite = JSON.stringify(towrite);
towrite = towrite.slice(1,towrite.length-1);
towrite = obj.image_names[obj.image_index]+","+towrite+"\n";
//console.log("writing " + towrite);
obj.towrite[obj.image_index] = towrite;
};

function save_textbox(){
var towrite = $("#textboxinput").val();
//towrite = JSON.stringify(towrite);
towrite = obj.image_names[obj.image_index] + "," + towrite + "\n";
obj.towrite2[obj.image_index] = towrite;	
console.log("writing " + towrite);
}

function draw_lines(){
//draw vertical lines on image
both_ctx_first[obj.right].lineWidth = obj.line_width;
var lwf = obj.line_width_factor
for (var i=1;i<obj.num_vert_lines;i++){
both_ctx_first[obj.right].moveTo(obj.pixel_size*i+lwf,lwf);
both_ctx_first[obj.right].lineTo(obj.pixel_size*i+lwf,obj.image_height+lwf);
both_ctx_first[obj.right].stroke();
};
//draw horizontal lines on image
for (var i=1;i<obj.num_horz_lines;i++){
both_ctx_first[obj.right].moveTo(lwf,obj.pixel_size*i+lwf);
both_ctx_first[obj.right].lineTo(obj.image_width+lwf,obj.pixel_size*i+lwf);
both_ctx_first[obj.right].stroke();
};
};

function initialize_results(){
//open results text file and write in configuration parameters
var keys = Object.keys(obj);

var towrite = "#config\n";
var towrite2 = "";
for(var i=0; i<keys.length; i++){
towrite = towrite + keys[i] + "," + obj[keys[i]] + "\n";
};
towrite = towrite + "#selection\n";
write_to_file(towrite, JSON.stringify(0));
};

//converts x,y coordinates to square index
function sub2ind(x,y){
var out = x*obj.num_horz_lines + y;
return out
};

//converts square index into x,y coordinates
function ind2sub(index){
var outx = Math.floor(index/obj.num_horz_lines);
var outy = index - outx*obj.num_horz_lines;
return [outx, outy]
};

//sets every element of the grid array to false
function new_grid(){
obj.grid = [];
for (var i=0; i<(obj.num_horz_lines*obj.num_vert_lines);i++){
	obj.grid.push(false);
};
};

function clear_grid(){
both_ctx[obj.right].clearRect(0,0,obj.image_width,obj.image_height);
new_grid();
};

//returns indices of the squares selected
function grid_to_index(){
var indices = [];
var idx = obj.grid.indexOf(true);
while (idx!=-1){
indices.push(idx);
idx = obj.grid.indexOf(true, idx+1);
};
return indices;
};

function write_to_file(towrite, file_append_flag){
ftowrite = ftowrite + towrite;
};
function write_to_results(towrite, file_append_flag){
$.post("../php/write.php", {data: towrite, path: obj.savefilename, flag: file_append_flag});
};

function set_config(config,files,results){
obj = config;
obj.grid = [];
obj.pixel_size = parseInt(config['pixel_size']);
obj.image_width = parseInt(config['image_width']);
obj.image_height = parseInt(config['image_height']);
obj.randomize_images = parseInt(config['randomize_images']);
obj.radio_buttons = parseInt(config['radio_buttons']);
obj.textbox_label = config['textbox_label'];
obj.line_width = parseInt(config['line_width']);
if (obj.line_width % 2 == 0){
obj.line_width_factor = 0;
}else{
obj.line_width_factor = 0.5;
};
if (obj.radio_buttons == 1){
$('#form').show();
};
obj.image_names = files;
obj.image_index = 0;
obj.right = 0;
obj.num_vert_lines = obj.image_width/obj.pixel_size;
obj.num_horz_lines = obj.image_height/obj.pixel_size;
obj.results_image_names = [];
obj.results_data = [];
obj.towrite = [];
obj.towrite2 = [];
if (results != false){
selection_index = results.indexOf('#selection\n');
end_index = results.indexOf('#end\n');

var res = results.slice(selection_index+1,end_index);
for (r=0;r<res.length;r++){
var ar = res[r].split("\n");
ar = ar[0];
var str = ar.split(",");
obj.results_image_names[r] = str[0];
var data = str.slice(1);
obj.results_data[r] = JSON.parse("[" + data + "]");
};
};
};

//Knuth shuffler
function shuffle(array) {
  var currentIndex = array.length
    , temporaryValue
    , randomIndex
    ;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
};
});
