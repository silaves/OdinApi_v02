INSERT INTO "auth_group" (id, name) values
(1,'administrador'),
(2,'cliente'),
(3,'empresario'),
(4,'taxista');

INSERT INTO "auth_group_permissions" (id, group_id, permission_id) VALUES
(1,1,48),
(2,1,52),
(3,2,48),
(4,2,52),
(5,3,48),
(6,3,52),
(7,4,48),
(8,4,52);

INSERT INTO "USUARIO" (id, password, is_superuser, username, email, is_staff, is_active, fecha_registro, nombres, apellidos, foto) VALUES
(2,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'pablobedoya','pablobedoya@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Pablo','Bedoya','perfiles/no-img.jpg'),
(3,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'pabloguardia','pabloguardia@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Pablo','Guardia','perfiles/no-img.jpg'),
(4,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'marioanglarillsalvatierra','marioanglarillsalvatierra@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Mario','Anglarill Salvatierra','perfiles/no-img.jpg'),
(5,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'rosariopazgutierrez','rosariopazgutierrez@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Rosario','Paz Gutierrez','perfiles/no-img.jpg'),
(6,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'iboblazicevic','iboblazicevic@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Ibo','Blazicevic','perfiles/no-img.jpg'),
(7,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'herbertvargas','herbertvargas@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Herbert','Vargas','perfiles/no-img.jpg'),
(8,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'francoismarchand','francoismarchand@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Francois','Marchand','perfiles/no-img.jpg'),
(9,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'ceciliazelaya','ceciliazelaya@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Cecilia','Zelaya','perfiles/no-img.jpg'),
(10,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'julioleonprado','julioleonprado@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Julio','Leon Prado','perfiles/no-img.jpg'),
(11,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'luisfernandobarbery','luisfernandobarbery@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Luis Fernando','Barbery','perfiles/no-img.jpg'),
(12,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'carmelopazduran','carmelopazduran@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Carmelo','Paz Duran','perfiles/no-img.jpg'),
(13,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'hernanatella','hernanatella@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Hernan','Atella','perfiles/no-img.jpg'),
(14,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'christianschilling','christianschilling@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Christian','Schilling','perfiles/no-img.jpg'),
(15,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'marcelotrigo','marcelotrigo@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Marcelo','Trigo','perfiles/no-img.jpg'),
(16,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'marianoaguilera','marianoaguilera@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Mariano','Aguilera','perfiles/no-img.jpg'),
(17,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'enriquepagola','enriquepagola@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Enrique','Pagola','perfiles/no-img.jpg'),
(18,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'darkozuazo','darkozuazo@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Darko','Zuazo','perfiles/no-img.jpg'),
(19,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'miguelcastedo','miguelcastedo@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Miguel','Castedo','perfiles/no-img.jpg'),
(20,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'lauraperdomo','lauraperdomo@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Laura','Perdomo','perfiles/no-img.jpg'),
(21,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'laurenmuller','laurenmuller@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Lauren','Muller','perfiles/no-img.jpg'),
(22,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'alexandercapela','alexandercapela@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Alexander','Capela','perfiles/no-img.jpg'),
(23,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'juanpablocalvo','juanpablocalvo@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Juan Pablo','Calvo','perfiles/no-img.jpg'),
(24,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'ronaldcasso','ronaldcasso@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Ronald','Casso','perfiles/no-img.jpg'),
(25,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'antoniovalda','antoniovalda@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Antonio','Valda','perfiles/no-img.jpg'),
(26,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'danielaguilar','danielaguilar@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Daniel','Aguilar','perfiles/no-img.jpg'),
(27,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'ivokuljis','ivokuljis@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Ivo','Kuljis','perfiles/no-img.jpg'),
(28,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'cristobalroda','cristobalroda@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Cristobal','Roda','perfiles/no-img.jpg'),
(29,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'guillermogonzalesquint-reina','guillermogonzalesquint-reina@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Guillermo','Gonzales Quint-Reina','perfiles/no-img.jpg'),
(30,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'jaimeyapur','jaimeyapur@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Jaime','Yapur','perfiles/no-img.jpg'),
(31,'pbkdf2_sha256$180000$oRHMhB4OjKi1$4cXF8zIS1kHGhXqhHqJ/TZNsWcmmxDrWoUcmCbYheUg=',false,'joseluiscamacho','joseluiscamacho@gmail.com',false,true,'2020-04-12 18:38:47.39342-04','Jose Luis','Camacho','perfiles/no-img.jpg');

INSERT INTO "PERFIL" (id, telefono, calificacion, disponibilidad, usuario_id) VALUES
(1,76191111,0,'N',1),
(2,77171234,0,'N',2),
(3,77171235,0,'N',3),
(4,77171236,0,'N',4),
(5,77171237,0,'N',5),
(6,77171238,0,'N',6),
(7,77171239,0,'N',7),
(8,77171240,0,'N',8),
(9,77171241,0,'N',9),
(10,77171242,0,'N',10),
(11,77171243,0,'N',11),
(12,77171244,0,'N',12),
(13,77171245,0,'N',13),
(14,77171246,0,'N',14),
(15,77171247,0,'N',15),
(16,77171248,0,'N',16),
(17,77171249,0,'N',17),
(18,77171250,0,'N',18),
(19,77171251,0,'N',19),
(20,77171252,0,'N',20),
(21,77171253,0,'N',21),
(22,77171254,0,'N',22),
(23,77171255,0,'N',23),
(24,77171256,0,'N',24),
(25,77171257,0,'N',25),
(26,77171258,0,'N',26),
(27,77171259,0,'N',27),
(28,77171260,0,'N',28),
(29,77171261,0,'N',29),
(30,77171262,0,'N',30),
(31,77171263,0,'N',31);


INSERT INTO "USUARIO_GRUPO" (id, usuario_id, group_id) VALUES
(1,2,3),
(2,3,3),
(3,4,3),
(4,5,3),
(5,6,3),
(6,7,3),
(7,8,3),
(8,9,3),
(9,10,3),
(10,11,3),
(11,12,3),
(12,13,3),
(13,14,2),
(14,15,2),
(15,16,2),
(16,17,2),
(17,18,2),
(18,19,2),
(19,20,2),
(20,21,2),
(21,22,4),
(22,23,4),
(23,24,4),
(24,25,4),
(25,26,4),
(26,27,4),
(27,28,4),
(28,29,4),
(29,30,4),
(30,31,4);

INSERT INTO "USUARIO_PERMISO" (id, usuario_id, permission_id) VALUES
(1,2,48),
(2,3,48),
(3,4,48),
(4,5,48),
(5,6,48),
(6,7,48),
(7,8,48),
(8,9,48),
(9,10,48),
(10,11,48),
(11,12,48),
(12,13,48),
(13,14,48),
(14,15,48),
(15,16,48),
(16,17,48),
(17,18,48),
(18,19,48),
(19,20,48),
(20,21,48),
(21,22,48),
(22,23,48),
(23,24,48),
(24,25,48),
(25,26,48),
(26,27,48),
(27,28,48),
(28,29,48),
(29,30,48),
(30,31,48);

INSERT INTO "MOVIL" (id, placa, color, modelo, foto, taxista_id) VALUES
(1,'ABC-123','negro','Toyota S 2017','moviles/no-img.jpg',22),
(2,'ABD-124','rojo','Toyota S 2018','moviles/no-img.jpg',23),
(3,'ABE-125','blanco','Toyota S 2019','moviles/no-img.jpg',24),
(4,'ABF-116','verde','Toyota S 2020','moviles/no-img.jpg',25),
(5,'ABG-117','azul marino','nissan sentra','moviles/no-img.jpg',26),
(6,'ABH-128','azul','nissan sentra','moviles/no-img.jpg',27),
(7,'ABI-129','gris','nissan sentra','moviles/no-img.jpg',28),
(8,'ABJ-130','negro','corolla sedan','moviles/no-img.jpg',29),
(9,'ABK-131','blanco','corolla sedan','moviles/no-img.jpg',30),
(10,'ABL-132','gris','corolla sedan','moviles/no-img.jpg',31);

INSERT INTO "CATEGORIA_EMPRESA" (id, nombre, estado) VALUES
(1,'comida',true),
(2,'electrodomestico',true),
(3,'discoteca',false);

INSERT INTO "EMPRESA" (id, nombre, descripcion, estado, categoria_id, empresario_id) VALUES
(1,'Crocan Pollo','venta de pollos a la broaster',true,1,2),
(2,'Pizzas Elis','venta de pizzas',true,1,3),
(3,'Rico Pollo','venta de pollos a la broaster',true,1,4),
(4,'GattoPardo','bar restaurante',true,1,5),
(5,'Gloria Helados','helados',true,1,6),
(6,'Cafe Mokka','venta de caffe y otros similares',true,1,7),
(7,'El Marques','bar restaurante',true,1,8),
(8,'Cabania Don Pedro','venta de comida especial',true,1,9),
(9,'Cavas de Altura','comidas, cenas',false,1,10),
(10,'Xoxo','bar restaurante',true,1,11),
(11,'Papi Pollo','venta de pollos a la broaster',true,1,12),
(12,'Macondo de Pizza Pazza Hotel - RestoBar','venta de pizzas',true,1,13);

INSERT INTO "SUCURSAL" (id, nombre, telefono, direccion, hora_inicio, hora_fin, foto, empresa_id) VALUES
(1,'Centro',46636448,'Gral Trigo 655, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',1),
(2,'Centro',46658800,'Calle. Padilla 110, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',2),
(3,'Centro',46649666,'Calle Sucre entre Bolívar y Domingo Paz, Tarija Bolivia','10:00:00','23:30:00','sucursal/no-img.jpg',3),
(4,'Centro',46630656,'La Madrid esq. Sucre, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',4),
(5,'Centro',69322200,'Gral Trigo entre Ingavi y Madrid, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',5),
(6,'Centro',46650505,'Calle 15 de Abril | Plaza Sucre, Tarija','08:00:00','23:00:00','sucursal/no-img.jpg',6),
(7,'Centro',46650506,'La madrid 372 | Frente a la Plaza Principal, Tarija','10:00:00','23:00:00','sucursal/no-img.jpg',7),
(8,'Centro',46650507,'Puente Bolivar s/n, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',8),
(9,'Centro',46663057,'calle 15 de Abril #130 | entre Colon y Daniel Campons, Tarija','11:00:00','00:00:00','sucursal/no-img.jpg',9),
(10,'Centro',46650000,'Abril Pasando G. Trigo 15 | Plaza Principal, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',10),
(11,'Centro',78227757,'Calle Bolivar #366, Tarija','10:00:00','23:30:00','sucursal/no-img.jpg',11),
(12,'Centro',46642107,'Calle 15 de Abril | Esq. Sucre, Tarija','09:00:00','15:00:00','sucursal/no-img.jpg',12);

INSERT INTO "PRODUCTO_FINAL" (id, nombre, descripcion, precio, estado, foto, sucursal_id) VALUES
(1,'crocan pollo','pollo a la broaster ¼ de pollo','25.0 ',true,'productos/e1_1.jpg',1),
(2,'pipocas de pollo','pequenias porciones de pollo picado','25.0 ',true,'productos/e1_2.jpg',1),
(3,'coca cola 3L','','15.0 ',true,'productos/e1_3.jpg',1),
(4,'coca cola 2L','','10.0 ',true,'productos/e1_4.jpg',1),
(5,'crocan pollo, 1 pollo','pollo a la broaster entero','75.0 ',true,'productos/e1_5.jpg',1),
(6,'hamburgesa','hamburgesa con queso y jamon al estilo crocan','25.0 ',true,'productos/e1_6.jpg',1),
(7,'crocan spiedo','pollo al spiedo ¼ de pollo','25.0 ',true,'productos/e1_7.jpg',1),
(8,'crocan spiedo 1 pollo','pollo al spiedo 1 pollo entero','75.0 ',true,'productos/e1_8.jpg',1),
(9,'crocan pork','con salsa barbacoa','25.0 ',true,'productos/e1_9.jpg',1),
(10,'salsa de mani','','5.0 ',false,'productos/e1_10.jpg',1),
(11,'alitas','Deliciosas alitas con salsa a elección + papas ','49.0 ',true,'productos/e2_1.jpg',2),
(12,'Grande Fugazzeta con Jamón','','40.0 ',true,'productos/e2_2.png',2),
(13,'Grande de Jamón y Palmitos','','40.0 ',true,'productos/e2_3.png',2),
(14,'Grande napolitana','','40.0 ',true,'productos/e2_4.png',2),
(15,'Grande calabresa','','40.0 ',true,'productos/e2_5.png',2),
(16,'Grande jamón y morrones','','40.0 ',true,'productos/e2_6.png',2),
(17,'Grande Verdura con Salsa Blanca','','40.0 ',true,'productos/e2_7.png',2),
(18,'Grande muzzarella','','40.0 ',true,'productos/e2_8.png',2),
(19,'Grande de Roquefort','','40.0 ',true,'productos/e2_9.png',2),
(20,'Grande de Provolone','','40.0 ',false,'productos/e2_10.png',2),
(21,'ChaufaDeQuinua','pidelo de pollo, mixto o de veggie!','15.0 ',true,'productos/e3_1.jpg',3),
(22,'hamburgesa','prueba nuestras deliciosas hamburgesas','20.0 ',true,'productos/e3_2.jpg',3),
(23,'pollo al spiedo','disfruta del 1/4 de pollo','25.0 ',true,'productos/e3_3.jpg',3),
(24,'pollo al spiedo','1 pollo','75.0 ',true,'productos/e3_4.jpg',3),
(25,'alitas','Aprovecha nuestra promo y ven a compartir despues de la oficina, con la familia o los amigos ','25.0 ',true,'productos/e3_5.jpg',3),
(26,'milanesa','Aprovecha la promo del día y pedí tu milanesa','21.0 ',true,'productos/e3_6.jpg',3),
(27,'sandwich de Lomito','es uno de nuestros productos más demandados','20.0 ',true,'productos/e3_7.png',3),
(28,'frijoles o porotos','guarnicion, Puede ser una buena opción a la hora de acompañar una milaneza, un pollo al spiedo, un buen lomito, con lo que tu gustes, disfrútalos!!!','15.0 ',true,'productos/e3_8.png',3),
(29,'clasico pollo con arroz y papa','','25.0 ',true,'productos/e3_9.jpg',3),
(30,'ensaladadefrutas','ada mejor en este clima que una #ensaladadefrutas fresca !! ','10.0 ',false,'productos/e3_10.jpg',3),
(31,'pizza gato','','40.0 ',true,'productos/e4_1.jpg',4),
(32,'frappe de frutilla','delicioso!!','15.0 ',true,'productos/e4_2.png',4),
(33,'spagueti al aglio e olio','Ya no pienses en que almorzaras.','25.0 ',true,'productos/e4_3.png',4),
(34,'pie de manzana','','30.0 ',true,'productos/e4_4.jpg',4),
(35,'empanadas','','5.0 ',true,'productos/e4_5.jpg',4),
(36,'bife chorizo','on dos acompañamientos a elección','30.0 ',true,'productos/e4_6.jpg',4),
(37,'lasania','Pensando que Almorzar? Listo','40.0 ',true,'productos/e4_7.jpg',4),
(38,'chili de carne','Ahora también puedes tener una experiencia MEXICANA','30.0 ',true,'productos/e4_8.jpg',4),
(39,'ensalada cesar','Pensando que cenar?','20.0 ',true,'productos/e4_9.jpg',4),
(40,'filete mignon','','30.0 ',false,'productos/e4_10.jpg',4);








INSERT INTO "CATEGORIA_ARTICULO" (id, nombre, codigo, estado) VALUES
(1,'Vehiculos','1.',true),
(2,'Propiedades – Inmuebles','2.',true),
(3,'Electronica','3.',true),
(4,'Telefonos – Tablets','4.',true),
(5,'Hogar – Muebles – Jardin','5.',true),
(6,'Deportes – Bicicletas','6.',true),
(7,'Moda – Belleza','7.',true),
(8,'Bebes y Ninios','8.',true),
(9,'Hobbies – Musica – Arte – Libros','9.',true),
(10,'Animales Mascotas','10.',true),
(11,'Herramientas – Industria – Oficina','11.',true),
(12,'Trabajo – Empleo','12.',true),
(13,'Servicios','13.',true),
(14,'Accesorios para Autos','1.1.',true),
(15,'Autos','1.2.',true),
(16,'Motos','1.3.',true),
(17,'Otros Vehiculos','1.4.',true),
(18,'Camiones – Vehiculos Comerciales','1.5.',true),
(19,'Departamentos - Casas - VENTA','2.1.',true),
(20,'Departamentos - Casas – ALQUILER','2.2.',true),
(21,'Alquiler temporario','2.3.',true),
(22,'Inmuebles comerciales – VENTA','2.4.',true),
(23,'Inmuebles comerciales – ALQUILER','2.5.',true),
(24,'Estacionamiento – Cocheras – VENTA','2.6.',true),
(25,'Estacionamiento – Cocheras – ALQUILER','2.7.',true),
(26,'Terrenos – VENTA','2.8.',true),
(27,'Emprendimientos – VENTA','2.9.',true),
(28,'TV – Audio – Video','3.1.',true),
(29,'Computadoras – Notebooks','3.2.',true),
(30,'Videojuegos – Consolas','3.3.',true),
(31,'Camaras y accesorios','3.4.',true),
(32,'Celulares – Telefonos','4.1.',true),
(33,'Accesorios para celulares','4.2.',true),
(34,'Tablets','4.3.',true),
(35,'Muebles','5.1.',true),
(36,'Decoracion – Jardin – Accesorios','5.2.',true),
(37,'Electrodomesticos','5.3.',true),
(38,'Bicicletas – Ciclismo','6.1.',true),
(39,'Otros Deportes','6.2.',true),
(40,'Futbol','6.3.',true),
(41,'Aerbicos y Fitness','6.4.',true),
(42,'Camping y Pesca','6.5.',true),
(43,'Deportes Extremos – Acuaticos','6.6.',true),
(44,'Ropa y Calzado','7.1.',true),
(45,'Relojes – Joyas – Accesorios','7.2.',true),
(46,'Salud – Belleza','7.3.',true),
(47,'Ropa de Bebes y Ninios','8.1.',true),
(48,'Cunas – Cochecitos – Accesorios','8.2.',true),
(49,'Juegos y Juguetes','8.3.',true),
(50,'Libros y Revistas','9.4.',true),
(51,'Arte y Antiguedades','9.5.',true),
(52,'Instrumentos Musicales','9.6.',true),
(53,'Cds – DVDs','9.7.',true),
(54,'Perros – Gatos','10.1.',true),
(55,'Accesorios para Mascota','10.2.',true),
(56,'Otros Animales','10.3.',true),
(57,'Herramientas','11.1.',true),
(58,'Industria','11.2.',true),
(59,'Muebles para Negocios y Oficinas','11.3.',true),
(60,'Ofertas de Trabajo','12.1.',true),
(61,'Busqueda de Trabajo – Cvs','12.2.',true),
(62,'Otros Servicios','13.1.',true),
(63,'Clases – Cursos','13.2.',true),
(64,'Reparaciones – Tecnicos','13.3.',true),
(65,'Organizacion de eventos','13.4.',true),
(66,'Transporte – Mudanzas','13.5.',true),
(67,'Servicio Domestico – Limpieza','13.6.',true),
(68,'Turismo – Paquetes Turisticos','13.7.',true);

INSERT INTO "SUB_CATEGORIA_ARTICULO" (hijo_id, padre_id) VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10),
(11,11),
(12,12),
(13,13),
(14,1),
(15,1),
(16,1),
(17,1),
(18,1),
(19,2),
(20,2),
(21,2),
(22,2),
(23,2),
(24,2),
(25,2),
(26,2),
(27,2),
(28,3),
(29,3),
(30,3),
(31,3),
(32,4),
(33,4),
(34,4),
(35,5),
(36,5),
(37,5),
(38,6),
(39,6),
(40,6),
(41,6),
(42,6),
(43,6),
(44,7),
(45,7),
(46,7),
(47,8),
(48,8),
(49,8),
(50,9),
(51,9),
(52,9),
(53,9),
(54,10),
(55,10),
(56,10),
(57,11),
(58,11),
(59,11),
(60,12),
(61,12),
(62,13),
(63,13),
(64,13),
(65,13),
(66,13),
(67,13),
(68,13);