program teste;
	var entrada, lenght, aux, output : integer;
			isover, print : boolean;

    function pot(n:integer; m:boolean) : integer;
    var count : integer ;
    begin
        pot := 1;
        for count := 0 to n - 1 do
        begin
            pot := pot * 10;
        end;
    end;

begin
	read(entrada);
    aux := 0;
    isover := 0;
    print := 1;

    while (not isover and print) do
    begin
        lenght := 0;
        output := 0;
        repeat
            pot := 1;
            pot(lenght, isover);
            output := pot*entrada + output;
            lenght := lenght + 1;
        until (lenght > aux);
        
        write(output);
        aux := aux + 1;

        if (aux >= entrada) then
        begin
            isover := 1;
        end;        
    end;

end.