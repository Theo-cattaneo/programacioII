<?php

    $Barrio=$_POST["Barrio"];
    $Zona=$_POST["Zona"];

    #muestra los datos
    echo "Barrio: ". $Barrio. "<br>" ;
    echo "Zona: ". $Zona. "<br>";

    #delaclro  las variables de las BDD
    $SERVER="127.0.0.1";
    $Usuario="root";
    $pass="";
    $Base="ipetyn246";
    #me conecto a la Base de datos
    $conexion=mysqli_connect($SERVER,$Usuario,$pass,$Base);
    #creo la Query a enviar al motor de la BDD
    $Query=INSERT INTO `barrio`(`id_Barrio`, `Nombre_barrios`, `ZONA_BARRIOS`) VALUES (0,'','');
    #mando a ejecutar la Query a la BBDD

   $Resultado=mysqli_Query($conexion,$Query);

    if ($Resultado)
        {

            echo " Los datos se guardaron";

        }
    else 
        {
            echo "Erro la carga";
        }
    mysqli_close($conexion);


?>