program teste;
	var entrada, aux: integer;

  function fat(n:integer) : integer;
  begin
    if (n <= 1) then
      begin
        fat := 1;
      end
    else
      begin
        fat(n - 1);
        fat := n * fat;
      end;
  end;

  function fibo(n:integer): integer;
    var aux : integer;

    function fat(n:integer) : integer;
    begin
      if (n <= 1) then
        begin
          fat := 1;
        end
      else
        begin
          fat(n - 1);
          fat := n * fat;
        end;
    end;

  begin
    if (n <= 1) then
      begin
        fibo := n;
      end
    else
      begin
        fat(n);
        fibo(n-1);
        aux := fibo;
        fibo(n-2);
        fibo := aux + fibo;
        write(fibo, fat);
      end;
  end;


begin
  repeat
    read(aux);
    fibo(aux);
    write(fibo);
  until (aux = 0);
end.
