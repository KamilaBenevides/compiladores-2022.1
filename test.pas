program teste;
	var entrada: integer;

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
  fat(3);
end.
