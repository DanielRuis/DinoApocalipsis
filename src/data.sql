CREATE OR REPLACE FUNCTION actualizar_max(puntaje_param INTEGER)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE puntaje SET max_puntaje = puntaje_param WHERE id = 1 AND max_puntaje < puntaje_param;
END;
$$;


create table puntaje (id serial primary key, max_puntaje int default(0) not null);
insert into puntaje (max_puntaje) values (0);
