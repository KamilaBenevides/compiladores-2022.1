program teste;
	var entrada, entrada2, aux, result, limiter, limiter2: integer;
      control1, control2 : boolean;

begin
  limiter := 0;
  limiter2 := 1;
  repeat
    write(limiter2, limiter2, limiter2, limiter2, limiter2, limiter2, limiter2);
    read(aux);
    if (aux > 0) then
      begin
        control1 := 1;
      end
    else
      begin
        control1 := 0;
        write(aux);
      end;
    if (aux < 5) then
      begin
        control2 := 1;
      end
    else
      begin
        control2 := 0;
      end;
    write(aux, control1, control2);
    if (control1 and control2) then
      begin
        write(limiter, limiter, limiter, limiter, limiter, limiter, limiter);
        read(entrada, entrada2);
        write(limiter, limiter, limiter, limiter, limiter, limiter, limiter);

        if (aux = 1) then
          begin
            result := entrada + entrada2;
          end
        else
          begin
            if (aux = 2) then
              begin
                result := entrada - entrada2;
              end
            else
              begin
                if (aux = 3) then
                  begin
                    result := entrada * entrada2;
                  end
                else
                  begin
                    if (aux = 4) then
                      begin
                        result := entrada / entrada2;
                      end
                    else
                      begin
                        result := 0 - 127;
                      end;
                  end;
              end;
          end;
        write(result);
      end;
  until(aux = 0);
end.
