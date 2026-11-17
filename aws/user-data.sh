#!/bin/bash
# Lab 6 · lo script di avvio delle tre istanze rossi-web
# EC2 → Launch instances → Advanced details → User data: si incolla tutto.
# Parte una volta sola, al primo avvio: installa Apache e scrive una pagina
# con l'identificativo dell'istanza e la sua zona.
dnf install -y httpd
ID=$(ec2-metadata -i | cut -d" " -f2)
ZONA=$(ec2-metadata -z | cut -d" " -f2)
echo "<h1>Flotta: risponde $ID</h1>
<p>zona $ZONA</p>" > /var/www/html/index.html
systemctl enable --now httpd
