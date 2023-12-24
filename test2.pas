Program MIN;
Var
  A, i_ : Integer;
  Min : Integer;

Begin
  Min:=32767;
    For i_:=1 to 10 do
      Begin
    Readln(A);
                If A < Min then Min:=A;
      end;
  Writeln('MIN=',Min);
  Readln;
end.