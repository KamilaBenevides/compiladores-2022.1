program teste;
	var aux, aux1: integer;

	function fatorial(n : integer) : integer;
		begin
			if (n <= 1) then
				begin
				fatorial := 1;
				end
			else
				begin
				fatorial(n-1);
				fatorial := n * fatorial;
				end;
		end;
	
	procedure pot(n : integer);
		var aux, count : integer;
		begin
			aux := 1;
            for count := 0 to n - 1 do
            begin
                aux := aux * 10;
            end;
			pot := aux; 
		end;

begin
	read(aux);
	fatorial(aux);
	write(fatorial);
	pot(2);
	write(pot);
end
.
