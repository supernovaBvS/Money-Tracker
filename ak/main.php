<?php
session_start();

    $_SESSION;
    
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>main</title>
    <h2 align="left">main</h1>
</head>
<body align="left">
<form action="/action_page.php">
  <label for="fname">First name:</label><br>
  <input type="text" id="fname" name="fname"><br>
  <label for="lname">Last name:</label><br>
  <input type="text" id="lname" name="lname"><br><br>
</form>
<form>
    <input type="radio" id="clothes" name="fav_language" value="HTML">
    <label for="clothes">clothes</label><br>
    <input type="radio" id="food_and_beverage" name="fav_language" value="CSS">
    <label for="food_and_beverage">food_and_beverage</label><br>
    <input type="radio" id="income" name="fav_language" value="JavaScript">
    <label for="income">income</label><br><br>
</form>
<form>
    <input type="submit" value="Submit">
</form>

<p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>
</body>
</html>