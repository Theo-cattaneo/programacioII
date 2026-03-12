<?php

    #Declaro las variables para poder conectarme al mysql(mariaDB)
        $SERVER="127.0.0.1";
        $USer="root";
        $pass="";
        $Base="ipetyn246";

    #creamos la conexion a la base de datos
    
    $conexion=mysqli_connect($SERVER,$USer,$pass,$Base);
    



?>