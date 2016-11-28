<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Lumos | Send Light</title>

    <!-- Bootstrap core CSS -->
    <link href="boostrap/css/bootstrap.min.css" rel="stylesheet">
   
  </head>

  <body>

    <!-- Static navbar -->
    <div class="navbar navbar-default navbar-static-top">
      <div class="container">
        <div class="navbar-header">
          <div class="navbar-brand">LUMOS | Send Light</div>
        </div>
      </div>
    </div>


    <div class="form-container"><strong>Enter security code:</strong>
		<?php
		$pass = $_POST['pass'];

		if($pass == "lumos")
		{
		       include("upload.php");
		}
		else
		{
		    if(isset($_POST))
		    {?>

		            <form method="POST" action="upload.php">
		            <input type="password" name="pass"></input><br/>
		            <input type="submit" name="submit" class="go-button" value="Go"></input>
		            <!-- <input type="submit" name="submit" class="go-button" value="Go"></input> -->
		            </form>
		    <?}
		}
		?>


<!--   		<form>
		  Enter security code:<br>
		  <input type="password" name="psw">
		</form>
		<a href="upload.php" target="_self">
		<div class="btn btn-lg btn-primary">Enter</div>
		</a>
 -->
    </div> <!-- /container -->

  </body>
</html>