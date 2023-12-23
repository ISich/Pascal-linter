import unittest
from unittest.mock import MagicMock, mock_open, patch
import pytest
from Linter import check_tabs, check_empty_lines, check_space, check_space_line, check_max_spaces, check_lines_len
from Linter import check_line_len, check_identificators
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
        ("      a := 12", 2, ['Tab error in 1 line\n']),
        (" b:= 3", 4, ['Tab error in 1 line\n'])
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
         ['Tab error in 3 line\n', 'Tab error in 4 line\n', 'Tab error in 7 line\n', 'Tab error \
in 8 line\n', 'Tab error in 9 line\n', 'Tab error in 10 line\n', 'Tab error in 11 line\n']),

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
end.''', 4, ['Tab error in 3 line\n', 'Tab error in 4 line\n', 'Tab error in 5 line\n', 'Tab error \
in 6 line\n', 'Tab error in 7 line\n', 'Tab error in 8 line\n', 'Tab error in 9 line\n', 'Tab error in 10 line\n']),
        ('''var n,p1,p2,p3,p4:integer;
begin
readln;
end.''', 1, ['Tab error in 3 line\n']),
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
end.''', 2, ['Tab error in 4 line\n', 'Tab error in 5 line\n', 'Tab error in 6 line\n', 'Tab error \
in 8 line\n', 'Tab error in 9 line\n', 'Tab error in 10 line\n']),
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
end.''', 1, [3], ['Tab error in 7 line\n', 'Tab error in 8 line\n', 'Tab error in 9 line\n', 'Tab error \
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
end.''', 4, [4, 5, 7, 8], ['Tab error in 6 line\n', 'Tab error in 9 line\n', 'Tab error in 10 line\n'])
    ])
    def test_with_blocking_lines(self, file_value, tabs_count, block_lines, expected):
        assert HelperTestingMethods.test_func(
            check_tabs, file_value, 'file_path', block_lines, tabs_count) == expected


class TestCheskEmptyLines:
    @pytest.mark.parametrize("file_value, possible, block_lines, expected", [
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [], ['Empty string error in 2 line\n']),
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
end.''', 0, [], ['Empty string error in 1 line\n', 'Empty string error in 2 line\n']),
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
end.''', 0, [], ['Empty string error in 1 line\n']),
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
end.''', 1, [], ['Empty string error in 8 line\n', 'Empty string error in 9 line\n', 'Empty string error in 14 line\n']),
        ('''var n,p1,p2,p3,p4:integer;          
begin         

           



end.''', 3, [], ['Empty string error in 3 line\n', 'Empty string error in 4 line\n']),
        ('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [1, 3], ['Empty string error in 2 line\n']),
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
end.''', 0, [1], ['Empty string error in 2 line\n']),
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


class TestCheckSpace:

    @pytest.mark.parametrize("line, expected", [
        ("var a,b,c: int", [5, 7]),
        ("var a,b, c: int", [5]),
        ("var a, b, c: int", []),
        ('''var a: int;
a:=3 +1;
''', [17]),
        ('''var a: int;
a:=3+ 1;
''', [16]),
        ('''var a: int;
a:=3+ 1 *5 - 2;
''', [16, 20]),
        ('''var a: int;
a := 3+ 1 *5 - 2/ 5;
''', [18, 22, 28])
    ])
    def test_check_space_line(self, line, expected):
        assert check_space_line(line, ['+', '-', '*', '/']) == expected

    @pytest.mark.parametrize("line, max_spaces, expected", [
        ("a:=b", 0, False),
        ("a:= b", 0, True),
        (" a := b ", 1, False),
        ("  a := b ", 1, False),
        ("if (a != (b + c))", 2, False),
        ("if (a !=   (b + c  ))", 2, True)
    ])
    def test_check_max_spaces(self, line, max_spaces, expected):
        assert check_max_spaces(line, max_spaces) == expected

    @pytest.mark.parametrize("file_value, max_space, block_lines, expected", [
        ('''var n,p1,p2,p3,p4:integer;
begin
readln    ;
end.''', 1, [], ['Space error in 1 line 5 pos by element ,\n', 'Space error in 1 line 8 pos by element ,\n', 'Space error in 1 line 11 pos by element ,\n', 'Space error in 1 line 14 pos by element ,\n', 'Space in too much in 3 line\n']),
        ('''var n,p1,p2,p3,p4:integer;''', 1, [], ['Space error in 1 line 5 pos by element ,\n', 'Space error in 1 line 8 pos by element ,\n',
         'Space error in 1 line 11 pos by element ,\n', 'Space error in 1 line 14 pos by element ,\n']),
        ('''var n,p4:integer;''', 1, [], [
         'Space error in 1 line 5 pos by element ,\n']),
        ('''var n,    p1:integer;''', 1, [], ['Space in too much in 1 line\n']),
        ('''var n,    p1,p2:integer;''', 1, [], [
         'Space in too much in 1 line\n', 'Space error in 1 line 12 pos by element ,\n']),
        ('''begin
n :=  3;
end.''', 1, [], ['Space in too much in 2 line\n']),
        ('''begin
n :=3;
end.''', 1, [], []),
        ('''begin
n :=3;
end     .''', 1, [], ['Space in too much in 3 line\n']),
        ('''begin
                n :=3;
end.''', 1, [], [])
    ])
    def test_spaces(self, file_value, max_space, block_lines, expected):
        space_elements = ['+', '-', '*', '/']
        assert HelperTestingMethods.test_func(
            check_space, file_value, 'file_path', block_lines, max_space, space_elements) == expected


class TestCheckLinesLen:
    @pytest.mark.parametrize('line, max_len, expected', [
        ('a', 1, False),
        ('aa', 1, True),
        ('  ', 2, False),
        ('abcd   ', 7, False),
        ('aeddfbcd   ', 7, True)
    ])
    def test_check_line_len(self, line, max_len, expected):
        assert check_line_len(line, max_len) == expected

    @pytest.mark.parametrize("file_value, max_len, block_lines, expected", [
        ('''Program aboba
begin
    readln;
end.''', 15, [], []),
        ('''Program aboba
begin
    readln    ;
end.''', 15, [], ['3 line in too large: 16 > 15\n']),
        ('''Program aboba
begin
    readln    ;
end               .''', 15, [], ['3 line in too large: 16 > 15\n', '4 line in too large: 19 > 15\n']),
        ('''''', 15, [], [])
    ])
    def test_check_lines_len(self, file_value, max_len, block_lines, expected):
        assert HelperTestingMethods.test_func(
            check_lines_len, file_value, 'file_path', block_lines, max_len) == expected


class TestCheckIdentificators:

    @pytest.mark.parametrize("file_value, block_lines, expected", [
        ('''var a:array[1..n] of integer;
    i,j,x:integer;''', [], []),
        ('''var a_:array[1..n] of integer;
    i,j,x:integer;''', [], ['incorrect identifier name a_ (not in CamelCase)\n']),
        ('''var a_:array[1..n] of integer;
    i_notCC,j,x:integer;''', [], ['incorrect identifier name a_ (not in CamelCase)\n', 'incorrect identifier name i_notCC (not in CamelCase)\n']),
        ('''''', [], []),
        ('''CamelCased :=not_cCcC''', [], [
         'incorrect identifier name not_cCcC (not in CamelCase)\n'])
    ])
    def test_check_lines_len(self, file_value, block_lines, expected):
        assert HelperTestingMethods.test_func(
            check_identificators, file_value, 'file_path', block_lines) == expected


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
