Program MIN;
Var
  A, I_ : Integer;
  Min : Integer;

Begin
  Min:=32767;
    For I_:=1 to 10 do
      Begin
    Readln(A);
                If A < Min then Min:=A;
      end;
  Writeln('MIN=',Min);
  Readln;
end.