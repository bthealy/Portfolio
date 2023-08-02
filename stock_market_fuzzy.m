clc; clear;

fis1 = readfis('equiv_price.fis');
fis2 = readfis('action_fuzzy.fis');

my_money = 10000;
my_stocks = 0;

XYZ_history = [];

my_money_his = [my_money];

% Run simulation
days = 365;

for i = 0:days
    r = randi([-1000,1000])/1000;

    XYZ = 10 + 2.8*sin((2*pi*i)/19) + 0.9*cos((2*pi*i)/19) + (0.6*r*rem(i,3)) + 0.014*i;
    XYZ_history = vertcat(XYZ_history, XYZ);

    MAD = 0.6*cos(0.4*i) - sin(0.5*i) + 0.5*r*rem(i,3);
    MAD = MAD / 2.6;
    
    % normalize based on last n days
    XYZ_history1 = zeros(size(XYZ_history));

    if i > 20
        XYZ_history1(i-19:i+1) = XYZ_history(i-19:i+1)/max(XYZ_history(i-19:i+1));
        XYZ_history1(i-19:i+1) = XYZ_history1(i-19:i+1) - mean(XYZ_history1(i-19:i+1));
    else
        XYZ_history1 = XYZ_history/max(XYZ_history);
        XYZ_history1 = XYZ_history1 - mean(XYZ_history1);
    end
    
    XYZ = -1 * XYZ_history1(end);

    % after x days, have enough info for TMA
    if i > 9
        TMA = sum(XYZ_history1(i-9:i))/10;

        equivalent_price = evalfis(fis1, [XYZ TMA]);
        action           = evalfis(fis2, [equivalent_price MAD]);

        stocks = abs(round(action*3000,0));

        if stocks > 600
            stocks = 600;
        end
        
        % Sell Stocks
        if action < -0.05

              if my_stocks < stocks
                stocks = my_stocks;
              end

            my_stocks = my_stocks - stocks;
            my_money = my_money + stocks*XYZ_history(i);

        elseif action < 0.05
            % Do nothing

        % Buy Stocks
        else
            cost = stocks*XYZ_history(i);

            if cost > my_money
                stocks = floor(my_money/XYZ_history(i));
            end

            my_stocks = my_stocks + stocks;
            my_money = my_money - stocks*XYZ_history(i);
    
        end
          my_money_his = vertcat(my_money_his, my_money);
    end
end

my_money
my_stocks

plot(my_money_his, 'LineWidth', 2)
