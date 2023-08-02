clc;clear;

y1  = [0, 0, 25, 40];
md1 = [30, 38, 50, 60];
o1  = [50, 65, 100, 100];

y = zeros(100,1);
y(1:y1(3)) = 1;

m = (1/(y1(4)-y1(3)));

for i = y1(3)+1:y1(4)-1
    y(i) = y(i-1) - m;
end

o = zeros(100,1);
o(o1(2):o1(3)) = 1;

m = 1/(o1(2)-o1(1));

for i = o1(1)+1:o1(2)-1
    o(i) = o(i-1) + m;
end

md = zeros(100, 1);
md(md1(2):md1(3)) = 1;

m1 = 1/(md1(2)-md1(1));
m2 = 1/(md1(4)-md1(3));

for i = md1(1)+1:md1(2)-1
    md(i) = md(i-1) + m1;
end

for i = md1(3)+1:md1(4)-1
    md(i) = md(i-1) - m2;
end


x = linspace(0,100,100);

plot(x, y, '-g', 'LineWidth', 3);
hold on
plot(x, md, '-b', 'LineWidth', 3);
plot(x, o, '-r', 'LineWidth', 3);
legend('young', 'middle', 'old')