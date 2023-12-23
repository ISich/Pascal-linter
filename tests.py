import unittest
from unittest.mock import MagicMock, mock_open, patch
import pytest
from Linter import check_tabs, check_empty_lines
import pdb


class TestCheckTabs:
    @pytest.mark.parametrize("file_value, tabs_count, expected", [
        ("", 4, []),
        ("", 0, [])
    ])
    def test_empty_file(self, file_value, expected, tabs_count):
        assert HelperTestingMethods.test_func(
            check_tabs, file_value, 'file_path', [], tabs_count) == expected

    @pytest.mark.parametrize("file_value, tabs_count, expected", [
        ("Program a", 1, []),
        ("      a := 12", 2, ['file_path: Tab error in 1 line\n']),
        (" b:= 3", 4, ['file_path: Tab error in 1 line\n'])
    ])
    def test_on_single_line(self, file_value, expected, tabs_count):
        assert HelperTestingMethods.test_func(
            check_tabs, file_value, 'file_path', [], tabs_count) == expected

    @pytest.mark.parametrize("file_value, tabs_count, expected", [
        ('''Program MIN;
Var
  A, I : Integer;
  Min : Integer;

Begin
    For I:=1 to 10 do
      Begin
        Write('Vvedi chislo ');
      end;
  Writeln('MIN=',Min);
end.''', 2,
         ['file_path: Tab error in 3 line\n', 'file_path: Tab error in 4 line\n', 'file_path: Tab error in 7 line\n', 'file_path: Tab error \
in 8 line\n', 'file_path: Tab error in 9 line\n', 'file_path: Tab error in 10 line\n', 'file_path: Tab error in 11 line\n']),

        ('''var n,i,k,a:integer;
begin
writeln('введите количество чисел');
readln(n);
a:=0;
for i:=1 to n do begin
                 writeln('введите ',i:1,'-е число');
                 readln(a);
                 if a mod 2=0 then k:=k+1;
                 end;
writeln('кол-во четных чисел ',k);
readln;
end.''', 4, ['file_path: Tab error in 3 line\n', 'file_path: Tab error in 4 line\n', 'file_path: Tab error in 5 line\n', 'file_path: Tab error \
in 6 line\n', 'file_path: Tab error in 7 line\n', 'file_path: Tab error in 8 line\n', 'file_path: Tab error in 9 line\n', 'file_path: Tab error in 10 line\n']),
        ('''var n,p1,p2,p3,p4:integer;
begin
readln;
end.''', 1, ['file_path: Tab error in 3 line\n']),
        ('''var n,p1,p2,p3,p4:integer;
begin
readln;
end.''', 0, []),
        ('''var n,p1,p2,p3,p4:integer;
begin
        readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 2, ['file_path: Tab error in 4 line\n', 'file_path: Tab error in 5 line\n', 'file_path: Tab error in 6 line\n', 'file_path: Tab error \
in 8 line\n', 'file_path: Tab error in 9 line\n', 'file_path: Tab error in 10 line\n']),
        ('''var n,p1,p2,p3,p4:integer;
begin
    readln;
    begin
        readln;
    end.
    n := 3;
    begin
        p1 := 4;
    end.
end.''', 1, [])
    ])
    def test_on_multiple_lines(self, file_value, tabs_count, expected):
        assert HelperTestingMethods.test_func(
            check_tabs, file_value, 'file_path', [], tabs_count) == expected

    @pytest.mark.parametrize("file_value, tabs_count, block_lines, expected", [
        ('''var n,p1,p2,p3,p4:integer;
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 1, [3], ['file_path: Tab error in 7 line\n', 'file_path: Tab error in 8 line\n', 'file_path: Tab error in 9 line\n', 'file_path: Tab error \
in 10 line\n']),
        ('''var n,i,k,a:integer;
begin
                writeln('введите количество чисел');
    readln(n);
    a:=0;
    for i:=1 to n do begin
                                writeln('введите ',i:1,'-е число');
                 readln(a);
                                if a mod 2=0 then k:=k+1;
                 end;
writeln('кол-во четных чисел ',k);
readln;
end.''', 4, [4, 5, 6, 7, 8, 9, 10], []),
        ('''var n,i,k,a:integer;
begin
                writeln('введите количество чисел');
    readln(n);
    a:=0;
    for i:=1 to n do begin
                                writeln('введите ',i:1,'-е число');
                 readln(a);
                                if a mod 2=0 then k:=k+1;
                 end;
writeln('кол-во четных чисел ',k);
readln;
end.''', 4, [4, 5, 7, 8], ['file_path: Tab error in 6 line\n', 'file_path: Tab error in 9 line\n', 'file_path: Tab error in 10 line\n'])
    ])
    def test_with_blocking_lines(self, file_value, tabs_count, block_lines, expected):
        assert HelperTestingMethods.test_func(
            check_tabs, file_value, 'file_path', block_lines, tabs_count) == expected


class TestCheskEmptyLines:
    @pytest.mark.parametrize("file_value, possible, block_lines, expected", [
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [], ['file_path: Empty string error in 2 line\n']),
        ('''

var n,p1,p2,p3,p4:integer;          
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 0, [], ['file_path: Empty string error in 1 line\n', 'file_path: Empty string error in 2 line\n']),
        ('''
var n,p1,p2,p3,p4:integer;          
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 0, [], ['file_path: Empty string error in 1 line\n']),
        ('''var n,p1,p2,p3,p4:integer;          
begin
           

readln;
    begin
           

        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 2, [], []),
        ('''var n,p1,p2,p3,p4:integer;          
begin
           
readln;
    begin
        readln
    end
           

           
    n := 3
  begin
    p1 := 4
           

  end
end.''', 1, [], ['file_path: Empty string error in 8 line\n', 'file_path: Empty string error in 9 line\n', 'file_path: Empty string error in 14 line\n']),
        ('''var n,p1,p2,p3,p4:integer;          
begin         

           



end.''', 3, [], ['file_path: Empty string error in 3 line\n', 'file_path: Empty string error in 4 line\n']),
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [1, 3], ['file_path: Empty string error in 2 line\n']),
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [2], []),
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [1, 2], []),
        ('''

var n,p1,p2,p3,p4:integer;          
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 0, [1], ['file_path: Empty string error in 2 line\n']),
        ('''

var n,p1,p2,p3,p4:integer;          
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end.''', 0, [1, 2, 3, 4, 5], [])
    ])
    def test_empty_lines(self, file_value, possible, block_lines, expected):
        assert HelperTestingMethods.test_func(
            check_empty_lines, file_value, 'file_path', block_lines, "", possible) == expected
        



class HelperTestingMethods:
    @staticmethod
    def immitate_readlines(st):
        if "\n" not in st:
            return [st + '\n']
        splitted = st.split('\n')
        for i in range(len(splitted) - 1):
            splitted[i] += "\n"
        return splitted

    @staticmethod
    def test_func(func, file_value, *args, **kwargs):
        file_mock = mock_open()
        file_mock.return_value.readlines.return_value = HelperTestingMethods.immitate_readlines(
            file_value)
        with patch('builtins.open', file_mock):
            result = func(*args, **kwargs)
        return result
