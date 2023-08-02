%% Speed
clc;clear;

y1  = [0, 0, 15, 40];
md1 = [15, 25, 70, 80];
o1  = [70, 70, 80, 100];


y = zeros(100,1);
y(1:y1(3)) = 1;

m = (1/(y1(4)-y1(3)));

for i = y1(3)+1:y1(4)-1
    y(i) = y(i-1) - m;
end

o = zeros(100,1);
o(o1(3):o1(4)) = 1;

m = 1/(o1(3)-o1(2));

for i = o1(2)+1:o1(3)-1
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

x = linspace(0,1,100);

plot(x, y, '-g', 'LineWidth', 3);
hold on
plot(x, md, '-b', 'LineWidth', 3);
plot(x, o, '-r', 'LineWidth', 3);
legend('Low', 'Medium', 'High')


%% Help Robot

clc;clear;

y1  = [0, 0, 50, 65];
md1 = [50, 60, 70, 80];
o1  = [70, 70, 85, 100];


y = zeros(100,1);
y(1:y1(3)) = 1;

m = (1/(y1(4)-y1(3)));

for i = y1(3)+1:y1(4)-1
    y(i) = y(i-1) - m;
end

o = zeros(100,1);
o(o1(3):o1(4)) = 1;

m = 1/(o1(3)-o1(2));

for i = o1(2)+1:o1(3)-1
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

x = linspace(0,1,100);

plot(x, y, '-g', 'LineWidth', 3);
hold on
plot(x, md, '-b', 'LineWidth', 3);
plot(x, o, '-r', 'LineWidth', 3);
legend('Low', 'Medium', 'High')


%% Efficiency

clc;clear;

y1  = [0, 0, 25, 50];
o1  = [0, 50, 75, 100];
md1 = [25, 40, 60, 75];

y = zeros(100,1);
y(1:y1(3)) = 1;

m = (1/(y1(4)-y1(3)));

for i = y1(3)+1:y1(4)-1
    y(i) = y(i-1) - m;
end

o = zeros(100,1);
o(o1(3):o1(4)) = 1;

m = 1/(o1(3)-o1(2));

for i = o1(2)+1:o1(3)-1
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

x = linspace(0,1,100);

plot(x, y, '-g', 'LineWidth', 3);
hold on
plot(x, md, '-b', 'LineWidth', 3);
plot(x, o, '-r', 'LineWidth', 3);
legend('Low', 'Medium', 'High')

%% Score

clc;clear;

y1  = [0, 0, 25, 50];
o1  = [0, 50, 75, 100];
md1 = [25, 40, 60, 75];

y = zeros(100,1);
y(1:y1(3)) = 1;

m = (1/(y1(4)-y1(3)));

for i = y1(3)+1:y1(4)-1
    y(i) = y(i-1) - m;
end

o = zeros(100,1);
o(o1(3):o1(4)) = 1;

m = 1/(o1(3)-o1(2));

for i = o1(2)+1:o1(3)-1
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

x = linspace(0,1,100);

plot(x, y, '-g', 'LineWidth', 3);
hold on
plot(x, md, '-b', 'LineWidth', 3);
plot(x, o, '-r', 'LineWidth', 3);
legend('Low', 'Medium', 'High')

