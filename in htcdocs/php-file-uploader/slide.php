<!doctype html>

<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<title>Title</title>
		<meta name="language" content="en" />  
		<meta name="description" content="" />  
		<meta name="keywords" content="" />
		<style type="text/css">
			ul li {list-style: none; margin-bottom: 15px;}
			ul li img {display: block;}
			ul li span {display: block;}
		</style>
	</head>
	<body>

		<?php

		// open this directory 
		$myDirectory = opendir("uploads");

		// get each entry
		while($entryName = readdir($myDirectory)) {
			$dirArray[] = $entryName;
		}

		// close directory
		closedir($myDirectory);

		//	count elements in array
		$indexCount	= count($dirArray);
		echo $indexCount

		?>
		
		<ul>

			<?php
			// loop through the array of files and print them all in a list
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				if ($extension == 'jpg' || $extension == 'png'){ 
					// $dirArray[$index] IS THE NAME OF THE FILE CAN USE THAT IN SOME HTML
					// save this in an array and use for slideshow
					echo '<li><img src="./uploads/' . $dirArray[$index] . '" alt="Image" />';
				}	
			}
			?>

		</ul>	
	
	
	</body>
</html>