var x >=0 integer;
var y >= 0;

maximize z: x + y;

subject to r:
  x + y <= 10;
subject to s:
  x + 10*y <= 1;
subject to t:
  10*x + y <= 1;

end;
