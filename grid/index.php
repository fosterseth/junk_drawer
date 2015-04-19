<html>
<?php
//get query from request and look up task configuration
$csv_file_path = "tasks.csv";

$taskcode = $_SERVER['QUERY_STRING'];
//open csv file and find taskcode
$fid = fopen($csv_file_path, 'r');
while (($line = fgetcsv($fid)) !== FALSE){
$this_taskcode = $line[0];
if ($this_taskcode == $taskcode){
$hit = $line;
break;
};
};
fclose($fid);

//parse each field with the ; delimiter
$ini_config_path = explode(';', $hit[1]);
$images = explode(';', $hit[2]);
$results = explode(';', $hit[3]);
$confirmation_code = $hit[4];

//set up empty arrays that will be sent to clients browser
$num_config = count($ini_config_path);
$allconfig = array();
$allfiles = array();
$allresults = array();
$allsavenames = array();

//loop through each configuration and append data to empty arrays
for ($x=0; $x<$num_config; $x++){
$config = parse_ini_file($ini_config_path[$x]);
$image_directory = $images[$x];
$files = glob($image_directory . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);
$results_file = $results[$x];
$allresults[$x] = file($results_file);
$allconfig[$x] = $config;
$allfiles[$x] = $files;
$allsavenames[$x] = $results_file;
};
?>
<link rel="stylesheet" type="text/css" href="../javascript/index.css">
</head>

<script type="text/javascript">
	var taskcode = <?php echo json_encode($taskcode); ?>;
	var confirmation_code = <?php echo json_encode($confirmation_code); ?>;
	var allsavenames = <?php echo json_encode($allsavenames); ?>;
	var allfiles = <?php echo json_encode($allfiles); ?>;
	var allconfig = <?php echo json_encode($allconfig); ?>;
	var allresults = <?php echo json_encode($allresults); ?>;
</script>
<script src="../javascript/jq.js"></script>
<script src="../javascript/grid_task_v6.js"></script>

<div id="all">
<table>
<tr>
<td>
<div style="position: relative">
<img id="img" src="../misc/startimg.png" />

<canvas class="canvas" id="mycanvas_first"></canvas>

<canvas class="canvas" id="mycanvas"></canvas>

</div>
</td>
<td>
<div style="position: relative">
<img id="img2" src="../misc/startimg2.png" />

<canvas class="canvas" id="mycanvas_first2"></canvas>

<canvas class="canvas" id="mycanvas2"></canvas>
</div>
</td>
</tr>
</table>

<button id ="button">start</button>
<button id="back">back</button>
<span id="textbox_label">Default</span><input id="textboxinput" type="textbox">
<form id ="form" action="" style="display:none">
<input type="radio" name="box" value="One">Just one object in view (default)<br>
<input type="radio" name="box" value="Morethan1">More than two objects in view<br>
<input type="radio" name="box" value="None">No object in view 
</form>
</div>
<div id="endtext" style="display:none">
<p>Thank you for completing the task. Be sure to copy and paste the following confirmation code into the space provided in your open Mechanical Turk window or tab.</p>
<p id="code">code</p>
</div>

</html>
</html>
</html>
